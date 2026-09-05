# Roadmap

This is the working backlog after the v0.3 profile + reusable-feature refactor. See `docs/validation-status.md` for the distinction between CI/source checks, existing-host runtime checks, fresh KVM installs and the reserved physical test partition.

## P0 — validate the new installer

- [x] Add repository-level CI for Bash syntax, JSON syntax, manifest duplicates and core restore/check wiring.
- [x] Merge-manage Caelestia `shell.json` and validate the common idle/app policy without overwriting unrelated local settings.
- [x] Detect and automatically rebuild stale `quickshell-git` after Qt ABI changes, with `rebuild-detector` + runtime validation.
- [x] Make `bash scripts/check` the single full runtime contract used both by restore and post-reboot validation.
- [x] Exercise focused Quickshell, Caelestia, Dolphin, Spotify and cursor runtime checks on the existing ASUS UX3405CA host without running a production restore.
- [ ] Re-test the **current three-mode TV Cast** contract on the physical host + Miracast TV, including Low Latency 720p30 / 5 Mbps.
- [ ] Resolve the intended keyboard layout/switch state on the existing host and rerun the current full `bash scripts/check` aggregate.
- [ ] Fresh **Gaming** install in KVM.
- [ ] Fresh **Work** install in KVM.
- [ ] Fresh **Laboratory** install in KVM (virtualization enabled by default).
- [ ] Reboot each VM and run `bash scripts/check`.
- [ ] Exercise the automatic Quickshell ABI rebuild after a real Qt update in a clean KVM.
- [ ] Validate the virtualization feature on a physical Linux host with `/dev/kvm`.
- [ ] Verify a Linux/Hyprland guest uses virtio/virgl rather than `llvmpipe` when 3D acceleration is enabled.
- [ ] After VM passes, test on the reserved physical Blueprint partition.
- [ ] Verify the Blueprint Snapper/Btrfs recovery checkpoint is actually usable before touching the main installation.

## P1 — visible desktop / UX

- [ ] New calculator. Work profile temporarily keeps GNOME Calculator until the replacement is chosen and tested.
- [ ] Tasks on the top menu.
- [ ] Fix the “5 строчками” issue after reproducing it on the clean profile.
- [ ] Replace/customize the login screen.
- [x] Standardize music on Spotify + Spicetify with a Caelestia-adaptive theme and managed launcher.
- [ ] Visually recheck the latest Spotify continuous pane-border tweak on the physical host.
- [x] Complete Dolphin preview UX: Information panel, global thumbnails and image/video/document preview backends.
- [x] Standardize the cursor on **Bibata Modern Ice** at 24 px while keeping **Colloid-Dark** as the current common icon theme.
- [ ] Confirm Bibata Modern Ice visually across the compositor/XWayland after the next logout/login.
- [ ] Add an OCR region hotkey: select area → OCR → clipboard (ukr/eng/rus).
- [x] Add explicit validation for every current Caelestia UI/runtime package patch after upstream updates.

## P1 — system / performance

- [ ] Baseline boot time, RAM, CPU wakeups and idle power on a clean profile before further tuning.
- [ ] System optimization pass based on measurements, not generic “gaming tweak” lists.
- [ ] Final gaming/GPU runtime test for Steam + Project Zomboid + Discord/Vesktop.
- [ ] Review `ananicy-cpp`, GameMode and launch wrappers together so they do not fight each other.
- [ ] Run `bash scripts/audit-disk`, review large directories and remove only confirmed unnecessary data/packages.
- [ ] Review services after clean install and remove anything not needed by the three profiles.

## P1 — virtualization

- [x] Add reusable `virtualization` feature for any profile.
- [x] Make Laboratory enable virtualization by default.
- [x] Standardize on KVM/QEMU + libvirt + virt-manager.
- [x] Prepare libvirt NAT network, storage pool, UEFI/OVMF, swtpm and virglrenderer.
- [x] Add `devos-vm` helper and desktop launcher.
- [ ] Create a reproducible one-command **Blueprint Test VM** template only after the host clean-install validation gates above pass.
- [ ] Decide whether a lighter launcher/UI should sit on top of libvirt while keeping libvirt as the backend.
- [ ] Add portable export/import instructions for VM XML + qcow2 images without committing huge VM disks to Git.

## P2 — hardware-specific

- [ ] Zenbook color profile: compare the current panel behavior with an official/model-specific ICC or measured profile. Do **not** install a random generic OLED ICC.
- [ ] Verify Zenbook `eq-laptop`, `eq-dolby`, `eq-sony` from a completely clean profile.
- [ ] Verify generic laptop exposes only `eq-laptop` + `eq-dolby`.
- [ ] Verify generic desktop exposes only `eq-pc` + `eq-dolby`.
- [ ] Review battery/power behavior on ASUS hardware separately from VM results.

## P2 — application cleanup

- [x] Active manifests no longer install Alacritty/Ptyxis; Kitty is the single default terminal.
- [ ] Review remaining duplicated viewers/utilities after real use of a fresh system.
- [ ] Decide whether GNOME-oriented helper packages can be reduced further without hurting login, portals, keyring or file dialogs.
- [ ] Review whether the current media/video apps should be consolidated.

## Documentation

- [x] Three install profiles documented.
- [x] Reusable virtualization feature documented.
- [x] Keyboard chooser documented.
- [x] Recovery-point behavior documented.
- [x] Hardware-aware audio behavior documented.
- [x] Helper commands documented.
- [x] Caelestia shell policy documented.
- [x] Quickshell ABI recovery documented.
- [x] Adaptive Spotify integration documented.
- [x] Repository CI / source-integrity validation documented.
- [x] Validate repository-local documentation links and referenced `docs/*.md` paths in CI.
- [x] Track validation level separately for CI/source, existing host, fresh KVM and physical test partition.
- [ ] Add screenshots only after the clean-install UI is stable.
