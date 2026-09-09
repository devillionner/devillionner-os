# Recovery points

Before a profile restore changes packages or dotfiles, `scripts/create-recovery-point` creates and verifies a recovery bundle.

The helper requires Btrfs and an existing Snapper `root` configuration. Root is snapshotted through Snapper, which stores the read-only root snapshot outside the live root subvolume. If `/home` is a separate subvolume on the same Btrfs filesystem, the helper creates a second read-only Btrfs snapshot for `/home` in the root-side recovery bundle.

The last checkpoint is recorded only after both snapshots and their manifest validate:

```text
bundle:/.snapshots/devillionner-os/<bundle-id>/manifest.json
```

The manifest records source and snapshot UUIDs, the filesystem UUID, read-only state, home coverage, and explicit limits. If preflight or verification fails, the previous checkpoint record remains unchanged and restore stops before package or dotfile mutation.

## Why restore requires this

A Blueprint profile can touch hundreds of packages and system/UI files. A clean recovery point is required before restore. Unsupported filesystems, separate home filesystems, relocated XDG directories, nested mounts in Blueprint-owned paths and unsupported nested home layouts fail closed.

The root and home snapshots are created sequentially, so this is a recovery point rather than an application-consistent transaction. Btrfs snapshots are local recovery points, not protection from disk or filesystem failure; use an external backup for that.

## Rollback

Inspect a recorded bundle before recovery:

```bash
sudo python3 /path/to/Blueprint/scripts/lib/recovery.py verify /path/to/manifest.json
sudo snapper -c root list
```

The Blueprint does not automate destructive rollback. Use the normal CachyOS/Snapper recovery flow, and validate it on the reserved physical test partition after all clean-KVM gates.

The existing host audit found root on `/@` and `/home` on the separate `/@home` subvolume. That topology is now covered by the coordinated bundle design, but no production snapshot or rollback has been attempted.
