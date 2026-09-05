# Tools and helper commands

## Validation

```bash
bash scripts/check
bash scripts/check-quickshell
bash scripts/check-tv-cast
```

The main check validates the selected profile, enabled features, core binaries, Quickshell runtime, Caelestia compatibility patches, keyboard mode, hardware/audio helper selection, services and Git state.

The dedicated Quickshell check validates that `quickshell-git` is installed, `qs --version` succeeds and `rebuild-detector` does not report the package as linked against stale libraries.

The TV Cast check validates Miracast dependencies, installed helper files, shell/Python syntax, FluxCast low-latency tuning, the two cast modes, `fast_bilinear`, gettext catalogs, UFW rules and the single persistent `Super+P` bind.

## Disk audit

```bash
bash scripts/audit-disk
```

Reports the largest top-level home directories, `/var` usage, Pacman cache size, orphan packages and journal size. It deletes nothing.

The Work profile also installs Baobab for a visual disk-usage view.

## TV Cast

TV Cast is installed in Gaming, Work and Laboratory.

```text
Super+P → TV Cast menu
30 FPS  → 1080p
60 FPS  → 720p
```

See `docs/tv-cast.md` for WFD/Miracast behavior, localization, firewall rules and validation.

## Virtual machines

If the virtualization feature is enabled:

```bash
devos-vm               # open virt-manager
devos-vm list          # list guests
devos-vm validate      # validate KVM/QEMU host support
```

The app launcher also contains **Virtual Machines**. See `docs/virtualization.md`.

## Audio helpers

ASUS Zenbook UX3405CA: `eq-laptop`, `eq-dolby`, `eq-sony`.

Generic hardware: EasyEffects is installed, but presets are user-managed (`eq-audio`).

## Caelestia / Quickshell restart

```bash
qs -c caelestia kill
caelestia shell -d
```

A Qt private-ABI update can leave `quickshell-git` installed but stale. Package reconciliation checks both `qs --version` and `checkrebuild`; if either indicates a broken/stale Quickshell build, Blueprint rebuilds the current AUR package without `--needed` and verifies the ABI state again. See `docs/quickshell.md`.
