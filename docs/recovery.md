# Recovery points

Before a profile restore changes packages or dotfiles, `scripts/create-recovery-point` creates a rollback point.

Preferred path:

1. use the existing Snapper `root` configuration;
2. otherwise, on a Btrfs root subvolume, create a read-only Btrfs snapshot.

The last created checkpoint is recorded in:

```text
~/.local/state/devillionner-os/last-checkpoint
```

Examples:

```text
snapper:42
btrfs:/.snapshots/devillionner-os/pre-restore-20260823-200000
```

## Why restore currently requires Btrfs

A Blueprint profile can touch hundreds of packages and system/UI files. A clean rollback point is more valuable than pretending an unsupported filesystem has equivalent recovery.

If the root filesystem is not Btrfs, the installer stops before the profile restore.

## Rollback

For a Snapper checkpoint, inspect snapshots first:

```bash
sudo snapper -c root list
```

For full boot/root rollback, use the normal CachyOS/Snapper recovery flow rather than deleting or replacing the live root while it is mounted.

The Blueprint intentionally does not automate destructive rollback.
