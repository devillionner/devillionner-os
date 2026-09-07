# Tools and helper commands

## Clone-less Blueprint command

Normal installed systems do not need to keep a Git checkout of this repository. Restore installs:

```text
/usr/local/bin/devos-blueprint
```

The command downloads an exact commit as a temporary archive, runs the requested action from that source, and removes the archive afterward.

```bash
devos-blueprint check
devos-blueprint check-repo
devos-blueprint version
devos-blueprint --ref <40-character-commit> check
```

`devos-blueprint check` prefers the revision recorded in `~/.config/devillionner-os/source-revision`, so a normal post-reboot validation does not silently compare an older installed system against a newer `main`.

On a machine where the helper is not installed yet, install only the helper without cloning the repository:

```bash
curl -fsSL https://raw.githubusercontent.com/devillionner/devillionner-os/main/bootstrap \
  | bash -s -- setup-cli
```

A local checkout remains useful for Blueprint development/debugging, but is not required by the installed system.

## Validation

```bash
devos-blueprint check
```

This is the canonical **full runtime validation** command after restore and after reboot. It validates the selected profile, mandatory shared TV Cast feature, optional virtualization state, core binaries, packages, keyboard mode, hardware/audio helper selection, declared service manifests and Blueprint source identity. It then runs the dedicated display-manager, service-manifest, Quickshell, Caelestia, Dolphin, Spotify, cursor and TV Cast validators and folds their exit status into one final `RESULT: PASS` / `RESULT: FAIL`.

Restore uses this same aggregate `scripts/check` internally, then records the source commit so the installed helper can fetch the same revision later.

For focused troubleshooting from a development checkout, the component validators remain available individually:

```bash
bash scripts/check-display-manager
bash scripts/check-services
bash scripts/check-quickshell
bash scripts/check-caelestia
bash scripts/check-dolphin
bash scripts/check-spotify
bash scripts/check-cursor
bash scripts/check-tv-cast
```

`check-display-manager` validates the SDDM package/service, enabled state and `display-manager.service` alias. `check-services` validates all system units selected by the common/profile/feature manifests plus the common user units, requiring each declared unit to exist and be enabled.

The dedicated Quickshell check validates that `quickshell-git` is installed, `qs --version` succeeds and `rebuild-detector` does not report the package as linked against stale libraries.

The TV Cast check validates Miracast dependencies, installed helper files, shell/Python syntax, FluxCast low-latency tuning, the exact three-mode contract, `fast_bilinear`, gettext catalogs, UFW rules and the single persistent `Super+P` bind.

## Clean KVM profile-default test

The KVM runbook tests the actual profile defaults rather than manually forcing virtualization state, using clone-less commit-pinned source for install and post-reboot validation.

Expected installation plans: Gaming = virtualization false, Work = false, Laboratory/Dev = true, University/Uni = false. See `docs/kvm-validation.md` for the full four-profile fresh-install/reboot evidence flow.

## Disk audit

From a development checkout:

```bash
bash scripts/audit-disk
```

Reports the largest top-level home directories, `/var` usage, Pacman cache size, orphan packages and journal size. It deletes nothing.

The Work profile also installs Baobab for a visual disk-usage view.

## TV Cast

TV Cast is installed in Gaming, Work, Laboratory/Dev and University/Uni.

```text
Super+P     → TV Cast menu
30 FPS      → 1080p / 8 Mbps (quality)
60 FPS      → 720p / 8 Mbps (smoothness)
Low Latency → 720p30 / 5 Mbps (minimum latency)
```

See `docs/tv-cast.md` for WFD/Miracast behavior, localization, firewall rules and validation.

## Virtual machines

If the virtualization feature is enabled:

```bash
devos-vm               # open virt-manager
devos-vm list          # list guests
devos-vm validate      # validate KVM/QEMU host support
```

The app launcher also contains **Virtual Machines**. Laboratory enables this feature by default; Gaming, Work and University default to off but can opt in. See `docs/virtualization.md`.

## Audio helpers

ASUS Zenbook UX3405CA: `eq-laptop`, `eq-dolby`, `eq-sony`.

Generic hardware: EasyEffects is installed, but presets are user-managed (`eq-audio`).

## Caelestia / Quickshell restart

```bash
qs -c caelestia kill
caelestia shell -d
```

A Qt private-ABI update can leave `quickshell-git` installed but stale. Package reconciliation checks both `qs --version` and `checkrebuild`; if either indicates a broken/stale Quickshell build, Blueprint rebuilds the current AUR package without `--needed` and verifies the ABI state again. See `docs/quickshell.md`.
