# Profiles and hardware behavior

## Common core

Every profile receives the same lean desktop core: Hyprland, Caelestia, Quickshell, Kitty, Fish, Helium, PipeWire/WirePlumber, EasyEffects, Dolphin, common viewers, fonts, firmware and basic maintenance tools.

The active manifests intentionally do not install several duplicate applications from the old full-system capture. In particular, the Blueprint has one default terminal (**Kitty**) and one default file manager (**Dolphin**).

Dolphin uses Colloid-Dark, double-click activation, compact 16 px Places icons and Swappy for JPEG/PNG/WEBP. Machine-specific Places/UDisks entries are deliberately not copied from one host. See `docs/dolphin.md`.

The old `manifests/packages-explicit-with-versions.txt` remains an audit/reference snapshot; it is not the active install set.

## Reusable features

Capabilities that may make sense in more than one profile live separately from the profile manifests. `virtualization` is optional/reusable, while TV Cast is a mandatory shared feature installed by every profile.

This means the same tested VM stack can be attached to Laboratory, Work or Gaming without duplicating package/configuration logic, while TV Cast stays part of the common Blueprint contract.

## Gaming

Adds Steam, Gamescope, MangoHud, GameMode, the 32-bit Mesa/Vulkan stack, `ananicy-cpp`, Vesktop and Vulkan tools.

Virtualization defaults to **off**, but can be enabled during installation.

The installer does not force a permanent performance power profile. That is intentionally avoided on laptops; game-specific performance behavior can be applied at launch time.

## Work

Adds Telegram Desktop, Vesktop, GNOME Calculator (temporary choice until the calculator redesign), Baobab Disk Usage Analyzer, Simple Scan, Meld and the OpenVPN NetworkManager plugin.

Virtualization defaults to **off**, but can be enabled during installation.

## Laboratory

Adds Clang, CMake, Ninja, GDB, Python pip/virtualenv, Node.js + npm, GitHub CLI + Git LFS, Lazygit, direnv, shellcheck and VS Code (`visual-studio-code-bin`).

Laboratory enables the reusable **virtualization** feature by default: KVM/QEMU, libvirt, virt-manager, virt-viewer, OVMF/UEFI, swtpm, virglrenderer, NAT networking and a VM storage pool.

Aliases `lab`, `dev` and `dev-laboratory` normalize to `laboratory`.

## Keyboard layouts

All profiles configure `us,ua`.

- `windows` → Alt+Shift via XKB
- `mac` → Super+Space
- `copilot` → Super+Shift+F23 plus Menu fallback

ASUS UX3405CA defaults to `copilot`; generic hardware defaults to `windows`.

## Audio / hardware

### ASUS Zenbook UX3405CA

Keeps the captured owner-specific `eq-laptop`, `eq-dolby`, `eq-sony` helpers and restores the matching EasyEffects presets for this machine only.

### Generic hardware

The Blueprint deliberately does **not** reuse the owner's Zenbook/Sony/Dolby speaker tuning on another laptop, desktop or VM. It removes `eq-laptop`, `eq-dolby`, `eq-sony` and the old `eq-pc` helper from the restored Fish functions, then exposes only:

- `eq-audio` → opens EasyEffects so presets appropriate to that machine can be created or selected manually.

The hardware profile is recorded as `generic`, and no Zenbook EasyEffects preset files are treated as a valid generic-machine default.

This is intentionally hardware-aware: a preset tuned for one laptop's speakers must not be presented as safe for unrelated hardware.
