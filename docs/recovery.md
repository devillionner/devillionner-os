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

## Coverage limits found on the existing host

The 2026-09-09 read-only audit found root on `/@` and `/home` on the
separate `/@home` subvolume. Only the Snapper `root` config is present.
Btrfs snapshots do not recursively capture nested/separate subvolumes: the
current root-only recovery helper therefore does **not** protect the user's
home dotfiles on this layout. A root snapshot must not be described as a
complete package-and-dotfile rollback point.

The host records `snapper:223`; snapshot existence and contents still require
privileged verification. A nonempty `last-checkpoint` file proves only that an
identifier was recorded. No rollback was attempted.

Before production restore, implement and validate coordinated recovery for all
modified subvolumes (including home), verify the recorded snapshots still
exist, and exercise recovery on the reserved test environment after the KVM
gates. Do not use the production partition to develop or test rollback.
