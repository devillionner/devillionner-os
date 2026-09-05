# devillionner-os

A reproducible CachyOS + Hyprland workstation blueprint focused on a clean Windows-to-Linux experience.

The repository restores programs, package choices, desktop configuration, services, themes and system behavior. Personal files, browser data, passwords, SSH keys and game saves are intentionally excluded.

## Install

Clone the repository on a fresh CachyOS install, then run:

```bash
git clone https://github.com/devillionner/devillionner-os.git
cd devillionner-os
bash scripts/install
```

The installer asks for a profile:

- **Gaming** — Steam, Gamescope, MangoHud, GameMode, gaming scheduler and Vesktop.
- **Work** — Helium, Telegram, calculator, scanner, disk analyzer and communication tools.
- **Laboratory** — compilers, Python/Node tooling, GitHub CLI, debugging tools, VS Code, and **KVM/QEMU virtual machines by default**.

**TV Cast / Miracast is a shared system feature and is installed in all three profiles.** Press `Super+P` to open its Fuzzel menu and choose 30 FPS / 1080p or 60 FPS / 720p.

All three profiles use **Dolphin** as the single file manager with the **Colloid-Dark** icon theme. `Super+E` opens Dolphin; JPEG, PNG and WEBP open in Swappy.

All three profiles also include **Spotify + Spicetify** with the `devillionner-text` theme. Its colors are generated from the active Caelestia/Hypr Material palette, update when the wallpaper palette changes, and use the same `0.95` compositor opacity as Dolphin in normal and fullscreen modes. `Super+M` opens the managed Spotify launcher.

Virtualization is a reusable feature, not hard-wired to one profile. Work or Gaming can enable the same KVM/libvirt/virt-manager stack during install or with:

```bash
bash scripts/install --profile work --with virtualization
bash scripts/install --profile gaming --with virtualization
```

The installer also asks for keyboard layout switching: **Alt+Shift**, **Super+Space**, or the **Copilot/Menu key**.

On the ASUS Zenbook UX3405CA, Copilot is the default layout switch and the Zenbook audio helpers are preserved. Other laptops/desktops receive generic audio helpers instead of Zenbook-specific ones.

## Safety

- The real/main CachyOS PARTUUID is hard-blocked.
- `scripts/install` auto-detects KVM/QEMU.
- Physical restore is currently allowed only on the reserved Blueprint test partition.
- A pre-restore Btrfs/Snapper recovery point is created before package/system changes.
- The scripts never repartition disks or touch Windows partitions.

Recommended validation order:

1. fresh KVM VM;
2. reserved physical test partition;
3. only after both pass, consider production use.

## Useful commands

```bash
bash scripts/check
bash scripts/check-dolphin
bash scripts/check-spotify
bash scripts/check-tv-cast
bash scripts/audit-disk
devos-vm
```

See:

- [Profiles and hardware behavior](docs/profiles.md)
- [Dolphin file manager](docs/dolphin.md)
- [Adaptive Spotify](docs/spotify.md)
- [TV Cast / Miracast](docs/tv-cast.md)
- [Virtual machines](docs/virtualization.md)
- [Recovery points](docs/recovery.md)
- [Tools and helper commands](docs/tools.md)
- [Roadmap](docs/roadmap.md)

## Current design decisions

- Kitty is the single default terminal. Alacritty/Ptyxis are not part of the active profile manifests.
- Dolphin is the single default file manager; Thunar is not part of the active manifests.
- Spotify uses the official Arch `spotify-launcher` plus Spicetify, with a pinned upstream `text` layout and Blueprint-owned adaptive Caelestia colors.
- Normal desktop translucency remains `0.95` in fullscreen; explicitly opaque apps and games opt out at `1.0`.
- Colloid-Dark is the common icon theme. Papirus is no longer declared by the Blueprint just to theme the file manager.
- System optimization is deliberately conservative: no experimental kernel flags or random sysctl tweaks.
- Quickshell runtime health is validated, so a Qt ABI break is caught instead of silently passing.
- Caelestia fullscreen and `Env` compatibility patches are applied during restore.
- TV Cast uses FluxCast/WFD + wf-recorder + Fuzzel and is shared by Gaming, Work and Laboratory.
- KVM/QEMU + libvirt + virt-manager is the standard general VM stack; VirtualBox is not the Blueprint default.
- Color/ICC tuning is not guessed on unknown displays; the Zenbook color-profile decision remains a measured/researched task.
