# Profiles and hardware behavior

## Common core

Every profile receives the same lean desktop core: Hyprland, Caelestia, Quickshell, Kitty, Fish, Helium, PipeWire/WirePlumber, EasyEffects, Thunar, common viewers, fonts, firmware and basic maintenance tools.

The active manifests intentionally do not install several duplicate applications from the old full-system capture. In particular, the Blueprint has one default terminal: **Kitty**.

The old `manifests/packages-explicit-with-versions.txt` remains an audit/reference snapshot; it is not the active install set.

## Gaming

Adds Steam, Gamescope, MangoHud, GameMode, the 32-bit Mesa/Vulkan stack, `ananicy-cpp`, Vesktop and Vulkan tools.

The installer does not force a permanent performance power profile. That is intentionally avoided on laptops; game-specific performance behavior can be applied at launch time.

## Work

Adds Telegram Desktop, Vesktop, GNOME Calculator (temporary choice until the calculator redesign), Baobab Disk Usage Analyzer, Simple Scan, Meld and the OpenVPN NetworkManager plugin.

## Laboratory

Adds Clang, CMake, Ninja, GDB, Python pip/virtualenv, Node.js + npm, GitHub CLI + Git LFS, Lazygit, direnv, shellcheck and VS Code (`visual-studio-code-bin`).

Aliases `lab`, `dev` and `dev-laboratory` normalize to `laboratory`.

## Keyboard layouts

All profiles configure `us,ua`.

- `windows` → Alt+Shift via XKB
- `mac` → Super+Space
- `copilot` → Super+Shift+F23 plus Menu fallback

ASUS UX3405CA defaults to `copilot`; generic hardware defaults to `windows`.

## Audio / hardware

### ASUS Zenbook UX3405CA

Keeps `eq-laptop`, `eq-dolby`, `eq-sony` and the existing Zenbook/EasyEffects configuration.

### Other laptops

Receives a generic `eq-laptop` helper plus `eq-dolby`. Zenbook-specific `eq-sony` is removed from the restored user config.

### Desktop / PC

Receives a generic `eq-pc` helper plus `eq-dolby`. Zenbook-specific helpers are not exposed.

This is intentionally hardware-aware: the Blueprint should not claim that one speaker EQ is safe for every laptop.
