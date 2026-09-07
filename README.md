# devillionner-os

A reproducible CachyOS + Hyprland workstation blueprint focused on a clean Windows-to-Linux experience.

The repository restores programs, package choices, desktop configuration, services, themes and system behavior. Personal files, browser data, passwords, SSH keys and game saves are intentionally excluded.

## Install without keeping the repository

A normal Blueprint system does **not** need a persistent Git checkout. The public bootstrap resolves `main` to one exact commit, downloads that commit as a temporary archive under `/tmp`, runs the installer from it, and removes the source bundle when the command finishes:

```bash
curl -fsSL https://raw.githubusercontent.com/devillionner/devillionner-os/main/bootstrap | bash
```

Installer arguments can be forwarded without cloning the repository:

```bash
curl -fsSL https://raw.githubusercontent.com/devillionner/devillionner-os/main/bootstrap \
  | bash -s -- --profile work --keyboard windows --vm
```

The restore installs `/usr/local/bin/devos-blueprint`. After that, the canonical post-install validation is simply:

```bash
devos-blueprint check
```

`devos-blueprint check` automatically uses the exact installed revision recorded by Blueprint, downloads that revision temporarily, validates the system, then removes the source bundle. `--ref <40-character-commit>` can be used when an explicit revision is required.

A local `git clone` remains useful for development/debugging only; it is not part of the final installed-system architecture.

The installer has four first-class profiles:

- **Gaming** — Steam, Gamescope, MangoHud, GameMode, gaming scheduler and Vesktop.
- **Work** — Helium, Telegram, calculator, scanner, disk analyzer and communication tools.
- **Laboratory / Dev** — compilers, Python/Node tooling, GitHub CLI, debugging tools, VS Code, and **KVM/QEMU virtual machines by default**.
- **University / Uni** — a separate study system with its own profile identity and ownership boundary. It currently uses the common desktop baseline only; University-specific apps will be chosen from the real study workflow rather than guessed in advance.

**TV Cast / Miracast is a shared system feature and is installed in all four profiles.** Press `Super+P` to open its Fuzzel menu and choose exactly one of the three Blueprint modes: **30 FPS / 1080p** for quality, **60 FPS / 720p** for smoothness, or **Low Latency / 720p30 / 5 Mbps** for minimum latency.

All four profiles use **Dolphin** as the single file manager with the **Colloid-Dark** icon theme. `Super+E` opens Dolphin; JPEG, PNG and WEBP open in Swappy.

All four profiles also include **Spotify + Spicetify** with the `devillionner-text` theme. Its colors are generated from the active Caelestia/Hypr Material palette, update when the wallpaper palette changes, and use the same `0.95` compositor opacity as Dolphin in normal and fullscreen modes. `Super+M` opens the managed Spotify launcher.

The common cursor is **Bibata Modern Ice** at 24 px, managed across XCursor, GTK and session environment with an XCursor fallback for Hyprland/XWayland consumers.

Caelestia's `shell.json` and `cli.json` are merge-managed rather than blindly replaced. Blueprint owns the common app/idle policy, Colloid-Dark CLI theme setting and Spotify toggle while preserving unrelated local Caelestia settings. The idle policy locks at 30 min, turns the display off at 35 min and suspends/hibernates at 60 min.

Quickshell is ABI-checked after package reconciliation and restore. If `qs --version` fails or `rebuild-detector` flags `quickshell-git` after a Qt library update, Blueprint performs an intentional same-version-capable rebuild and validates the result before reporting success.

Virtualization is a reusable feature, not hard-wired to one profile. Laboratory enables it by default; Gaming, Work or University can opt into the same KVM/libvirt/virt-manager stack during install:

```bash
curl -fsSL https://raw.githubusercontent.com/devillionner/devillionner-os/main/bootstrap \
  | bash -s -- --profile university --with virtualization --vm
```

The installer also asks for keyboard layout switching: **Alt+Shift**, **Super+Space**, or the **Copilot/Menu key**.

On the ASUS Zenbook UX3405CA, Copilot is the default layout switch and the Zenbook audio helpers are preserved. Other laptops/desktops use the generic `eq-audio` helper with user-managed EasyEffects presets instead of inheriting Zenbook-specific tuning.

## Clone-less helper

On an existing system, the helper itself can be installed without cloning anything:

```bash
curl -fsSL https://raw.githubusercontent.com/devillionner/devillionner-os/main/bootstrap \
  | bash -s -- setup-cli
```

Useful remote actions:

```bash
devos-blueprint check             # validate the installed revision
devos-blueprint check-repo        # repository integrity from a temporary bundle
devos-blueprint version           # resolve the revision that would be fetched
devos-blueprint --ref <sha> check # validate using an explicit pinned revision
```

## Safety

- The real/main CachyOS PARTUUID is hard-blocked.
- `scripts/install` auto-detects KVM/QEMU.
- Physical restore is currently allowed only on the reserved Blueprint test partition.
- A pre-restore Btrfs/Snapper recovery point is created before package/system changes.
- The scripts never repartition disks or touch Windows partitions.
- Remote bootstrap downloads the source archive by a resolved 40-character commit SHA rather than executing a mutable archive directly.
- Temporary source bundles are removed after the requested action completes.
- GitHub pull requests run repository-integrity and desktop-contract checks before changes reach `main`.
- Merge-managed Caelestia JSON refuses malformed existing files instead of silently overwriting them.
- Quickshell rebuilds are checked both by runtime validation and a source-level CI contract.
- Declared system/user service manifests are part of the aggregate runtime PASS; a failed service enablement cannot be hidden by a warning.

Recommended validation order:

1. repository CI / `devos-blueprint check-repo`;
2. fresh Gaming, Work, Laboratory and University KVM installs, each from a clean baseline and each followed by reboot + `devos-blueprint check` on the same pinned revision;
3. reserved physical test partition;
4. only after those gates pass, consider production use.

The current evidence at each validation level is tracked explicitly in [Validation status](docs/validation-status.md).

## Useful commands

```bash
devos-blueprint check
devos-blueprint check-repo
bash scripts/check-display-manager      # development checkout only
bash scripts/check-services             # development checkout only
bash scripts/check-quickshell            # development checkout only
devos-vm
```

See:

- [Profiles and hardware behavior](docs/profiles.md)
- [Caelestia configuration policy](docs/caelestia.md)
- [Quickshell ABI recovery](docs/quickshell.md)
- [Dolphin file manager](docs/dolphin.md)
- [Adaptive Spotify](docs/spotify.md)
- [TV Cast / Miracast](docs/tv-cast.md)
- [Virtual machines](docs/virtualization.md)
- [Recovery points](docs/recovery.md)
- [Tools and helper commands](docs/tools.md)
- [Validation status](docs/validation-status.md)
- [Roadmap](docs/roadmap.md)

## Current design decisions

- The installed system does not require a persistent Blueprint Git repository; normal install/check operations use commit-pinned temporary source bundles.
- Gaming, Work, Laboratory/Dev and University/Uni are distinct profile identities. University is not a Work alias.
- Kitty is the single default terminal. Alacritty/Ptyxis are not part of the active profile manifests.
- Dolphin is the single default file manager; Thunar is not part of the active manifests.
- SDDM is the common login/display manager baseline; login-screen styling is a separate UX task.
- Caelestia `shell.json` and `cli.json` are merge-managed so Blueprint-owned defaults can be updated without deleting unrelated user settings.
- Spotify uses the official Arch `spotify-launcher` plus Spicetify, with a pinned upstream `text` layout and Blueprint-owned adaptive Caelestia colors.
- Normal desktop translucency remains `0.95` in fullscreen; explicitly opaque apps and games opt out at `1.0`.
- Bibata Modern Ice at 24 px is the common cursor; Colloid-Dark remains the common icon theme.
- System optimization is deliberately conservative: no experimental kernel flags or random sysctl tweaks.
- Quickshell runtime + shared-library ABI state are validated; stale Qt-linked builds are rebuilt without `--needed` and checked again afterward.
- Caelestia fullscreen and `Env` compatibility patches are applied during restore and validated afterward.
- TV Cast uses FluxCast/WFD + wf-recorder + Fuzzel and is shared by all four profiles; its supported mode set is fixed at exactly 1080p30, 720p60 and Low Latency 720p30/5 Mbps.
- KVM/QEMU + libvirt + virt-manager is the standard general VM stack; VirtualBox is not the Blueprint default.
- Color/ICC tuning is not guessed on unknown displays; the Zenbook color-profile decision remains a measured/researched task.
