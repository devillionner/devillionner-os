#!/usr/bin/env python3
"""Coordinated root/home checkpoints; never mount, delete or roll back."""
import datetime
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import uuid

BASE = Path("/.snapshots/devillionner-os")


def run(*args):
    return subprocess.run(args, check=True, text=True, capture_output=True,
                          stdin=subprocess.DEVNULL,
                          env={**os.environ, "LC_ALL": "C"}).stdout.strip()


def mount(path):
    data = json.loads(run("findmnt", "--json", "--target", str(path),
                          "--output", "TARGET,FSTYPE,UUID,FSROOT"))
    item = data["filesystems"][0]
    if item["fstype"] != "btrfs" or not item.get("uuid"):
        raise ValueError(f"Automatic recovery points currently require a Btrfs root and home: {path}")
    return item


def subvolume(path):
    text = run("btrfs", "subvolume", "show", str(path))
    result = {}
    for label, key in (("UUID", "uuid"), ("Parent UUID", "parent_uuid"),
                       ("Subvolume ID", "id")):
        matches = re.findall(r"^\s*" + label + r":\s*(\S+)\s*$", text, re.M)
        if len(matches) != 1:
            raise ValueError(f"Cannot identify subvolume {path}: {label}")
        result[key] = matches[0]
    uuid.UUID(result["uuid"])
    if result["parent_uuid"] == "-":
        result["parent_uuid"] = None
    elif not re.fullmatch(r"[0-9a-f-]{36}", result["parent_uuid"]):
        raise ValueError(f"Invalid parent UUID: {path}")
    if not result["id"].isdigit():
        raise ValueError(f"Invalid subvolume ID: {path}")
    return result


def rootid(path):
    value = run("btrfs", "inspect-internal", "rootid", str(path))
    if not value.isdigit():
        raise ValueError(f"Cannot determine containing subvolume: {path}")
    return value


def within(path, parent):
    return path == parent or path.startswith(parent.rstrip("/") + "/")


def preflight(home):
    home = str(Path(home))
    if not home.startswith("/home/") or str(Path(home).resolve(strict=True)) != home:
        raise ValueError("Recovery requires a real user directory beneath /home, without symlink ancestors")
    root_mount = mount("/")
    root = subvolume("/")
    home_mount = mount(home)
    if home_mount["uuid"] != root_mount["uuid"]:
        raise ValueError("Separate home filesystem requires a separately validated recovery plan")
    home_id = rootid(home)
    sources = [{"source": "/", **root, "filesystem_uuid": root_mount["uuid"]}]
    if home_id != root["id"]:
        home_subvol = subvolume("/home")
        if home_subvol["id"] != home_id or str(Path("/home").resolve()) != "/home":
            raise ValueError("Nested/per-user home subvolumes require a separately validated recovery plan")
        sources.append({"source": "/home", **home_subvol,
                        "filesystem_uuid": root_mount["uuid"]})

    # Snapshots are not recursive. Reject holes in restore-owned trees;
    # nested logs, caches and other unrelated data are outside this contract.
    protected = ["/etc", "/usr", "/var/lib", home + "/.config",
                 home + "/.local", home + "/.icons"]
    mounts = json.loads(run("findmnt", "--json", "--list", "--output", "TARGET"))["filesystems"]
    for path in protected:
        nearest = Path(path)
        while not nearest.exists():
            nearest = nearest.parent
        expected = home_id if within(path, home) else root["id"]
        if str(nearest.resolve()) != str(nearest) or rootid(nearest) != expected:
            raise ValueError(f"Uncovered or relocated restore directory: {path}")
        for item in mounts:
            if within(item["target"], path):
                raise ValueError(f"Nested mount in restore directory: {item['target']}")

    # The protected paths above must resolve to exactly the source subvolume.
    # We intentionally reject nested mounts there; unrelated subvolumes outside
    # restore-owned paths are recorded as excluded in the manifest.
    return sources


def secure_directory(path):
    if path != Path("/"):
        secure_directory(path.parent)
    if not path.exists():
        path.mkdir(mode=0o700)
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
        raise ValueError(f"Unsafe recovery destination: {path}")


def verify_entry(entry):
    current = subvolume(entry["snapshot"])
    if current["parent_uuid"] != entry["uuid"] or current["uuid"] != entry["snapshot_uuid"]:
        raise ValueError("Snapshot identity/parent UUID differs")
    if mount(entry["snapshot"])["uuid"] != entry["filesystem_uuid"]:
        raise ValueError("Snapshot filesystem differs")
    if run("btrfs", "property", "get", "-t", "s", entry["snapshot"], "ro") != "ro=true":
        raise ValueError("Recovery snapshot is not read-only")


def verify(manifest):
    path = Path(manifest)
    if path.name != "manifest.json" or path.parent.parent != BASE:
        raise ValueError("Invalid recovery manifest location")
    data = json.loads(path.read_text())
    if data.get("version") != 1 or data.get("status") != "complete":
        raise ValueError("Recovery bundle is incomplete or unsupported")
    sources = [item["source"] for item in data["snapshots"]]
    if sources not in [["/"], ["/", "/home"]]:
        raise ValueError("Invalid recovery source set")
    if data["home_coverage"] != ("root" if sources == ["/"] else "home"):
        raise ValueError("Home coverage record differs")
    for entry in data["snapshots"]:
        name = "root" if entry["source"] == "/" else "home"
        if name == "root":
            if not entry["snapshot"].startswith("/.snapshots/") or not entry["snapshot"].endswith("/snapshot"):
                raise ValueError("Root snapshot is outside Snapper storage")
        elif entry["snapshot"] != str(path.parent / "home"):
            raise ValueError("Home snapshot outside its recovery bundle")
        verify_entry(entry)
    return data


def create(home, description):
    sources = preflight(home)
    secure_directory(BASE)
    if mount(BASE)["uuid"] != sources[0]["filesystem_uuid"]:
        raise ValueError("Snapshot destination must be on the root Btrfs filesystem")
    # Root snapshots must be created by Snapper, whose .snapshots storage is
    # outside the live root subvolume. Never pass a path below / as a Btrfs
    # snapshot destination for the / source itself.
    config = run("snapper", "-c", "root", "get-config")
    if not re.search(r"(?m)^SUBVOLUME(?:=|\s+)[\"\']?/?[\"\']?$", config):
        raise ValueError("Snapper root configuration does not target /")
    number = run("snapper", "-c", "root", "create", "--type", "single",
                 "--description", description, "--userdata", "important=yes",
                 "--print-number")
    if not number.isdigit():
        raise ValueError("Snapper returned an invalid root snapshot number")
    root_target = Path(f"/.snapshots/{number}/snapshot")
    root_source = sources[0]
    entry_root = {**root_source, "snapshot": str(root_target),
                  "snapshot_uuid": subvolume(root_target)["uuid"]}
    verify_entry(entry_root)

    bundle = BASE / str(uuid.uuid4())
    bundle.mkdir(mode=0o700)
    print(f"Recovery bundle in progress: {bundle}", file=sys.stderr)
    entries = [entry_root]
    if len(sources) == 2:
        source = sources[1]
        target = bundle / "home"
        # /home is a separate source, so a destination in the root subvolume is
        # outside it and remains valid without mounting the Btrfs top level.
        run("btrfs", "subvolume", "snapshot", "-r", source["source"], str(target))
        entry = {**source, "snapshot": str(target),
                 "snapshot_uuid": subvolume(target)["uuid"]}
        verify_entry(entry)
        entries.append(entry)
    if preflight(home) != sources:
        raise ValueError("Recovery topology changed during snapshot creation")
    data = {"version": 1, "status": "complete", "description": description,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "home": home, "home_coverage": "root" if len(sources) == 1 else "home",
            "snapshots": entries,
            "limits": ["Sequential snapshots, not an application-consistent atomic pair",
                       "Separate /boot, EFI, nested logs/caches and other data subvolumes excluded"]}
    temp = bundle / "manifest.pending"
    with temp.open("x") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    manifest = bundle / "manifest.json"
    temp.rename(manifest)
    run("btrfs", "filesystem", "sync", str(BASE))
    verify(manifest)
    return manifest


def main():
    if os.geteuid() != 0:
        raise ValueError("Privileged access is required to inspect/create recovery snapshots")
    if len(sys.argv) == 4 and sys.argv[1] == "create":
        print(create(sys.argv[2], sys.argv[3]))
    elif len(sys.argv) == 3 and sys.argv[1] == "verify":
        verify(sys.argv[2])
        print("Recovery bundle exists; snapshot identities and read-only flags verified")
    else:
        raise ValueError("Usage: recovery.py create HOME DESCRIPTION | verify MANIFEST")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"Recovery failed: {error}", file=sys.stderr)
        sys.exit(1)
