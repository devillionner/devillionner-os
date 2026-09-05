#!/usr/bin/env python3
"""Merge the Blueprint-owned Dolphin global preview flag into .directory.

KConfig's kwriteconfig utility is intended for config-file names in the KDE
config location; on a live host an absolute path under Dolphin's data directory
returned success without creating the requested file. This helper writes the
actual view-properties file directly while preserving unrelated sections,
keys, comments and an existing symlink.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SECTION_RE = re.compile(r"^(?P<indent>\s*)\[(?P<name>[^\]]+)\](?P<tail>\s*(?:[;#].*)?)$")
KEY_RE = re.compile(r"^(?P<indent>\s*)PreviewsShown\s*=.*$")


def merge_text(current: str) -> str:
    lines = current.splitlines()
    had_trailing_newline = current.endswith("\n")

    dolphin_start: int | None = None
    dolphin_end = len(lines)

    for index, line in enumerate(lines):
        match = SECTION_RE.match(line)
        if not match:
            continue
        if dolphin_start is not None:
            dolphin_end = index
            break
        if match.group("name") == "Dolphin":
            dolphin_start = index

    if dolphin_start is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend(["[Dolphin]", "PreviewsShown=true"])
    else:
        key_indexes = [
            index
            for index in range(dolphin_start + 1, dolphin_end)
            if KEY_RE.match(lines[index])
        ]
        if key_indexes:
            first = key_indexes[0]
            indent = KEY_RE.match(lines[first]).group("indent")  # type: ignore[union-attr]
            lines[first] = f"{indent}PreviewsShown=true"
            for duplicate in reversed(key_indexes[1:]):
                del lines[duplicate]
        else:
            lines.insert(dolphin_end, "PreviewsShown=true")

    result = "\n".join(lines)
    if lines and (had_trailing_newline or not current):
        result += "\n"
    return result


def merge_file(destination: Path) -> None:
    if destination.is_dir() and not destination.is_symlink():
        raise ValueError(f"expected a file at {destination}, found a directory")

    try:
        current = destination.read_text(encoding="utf-8")
    except FileNotFoundError:
        current = ""
    except OSError as exc:
        raise OSError(f"could not read {destination}: {exc}") from exc

    updated = merge_text(current)
    if updated == current and destination.exists():
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        # write_text follows an existing symlink, preserving user/dotfile-manager
        # ownership of the path instead of replacing the link itself.
        destination.write_text(updated, encoding="utf-8")
    except OSError as exc:
        raise OSError(f"could not update {destination}: {exc}") from exc


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: set-dolphin-global-view.py DESTINATION", file=sys.stderr)
        return 2
    try:
        merge_file(Path(argv[1]))
    except (OSError, ValueError) as exc:
        print(f"set-dolphin-global-view: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
