# Roadmap

This is the working backlog after the v0.2 profile refactor.

## P0 — validate the new installer

- [ ] Fresh **Gaming** install in KVM.
- [ ] Fresh **Work** install in KVM.
- [ ] Fresh **Laboratory** install in KVM.
- [ ] Reboot each VM and run `bash scripts/check`.
- [ ] After VM passes, test on the reserved physical Blueprint partition.
- [ ] Verify Snapper/Btrfs checkpoint is usable before touching the main installation.
- [ ] Verify Quickshell rebuild logic after a Qt update.

## P1 — visible desktop / UX

- [ ] New calculator. Work profile temporarily keeps GNOME Calculator until the replacement is chosen and tested.
- [ ] Tasks on the top menu.
- [ ] Fix the “5 строчками” issue after reproducing it on the clean profile.
- [ ] Replace/customize the login screen.
- [ ] Choose a better/stylish audio player if it improves the current setup.
- [ ] Replace cursor and possibly icon theme after checking consistency with Caelestia/Darkly.
- [ ] Add an OCR region hotkey: select area → OCR → clipboard (ukr/eng/rus).
- [ ] Add explicit validation for every Caelestia UI patch after upstream updates.

## P1 — system / performance

- [ ] Baseline boot time, RAM, CPU wakeups and idle power on a clean profile before further tuning.
- [ ] System optimization pass based on measurements, not generic “gaming tweak” lists.
- [ ] Final gaming/GPU runtime test for Steam + Project Zomboid + Discord/Vesktop.
- [ ] Review `ananicy-cpp`, GameMode and launch wrappers together so they do not fight each other.
- [ ] Run `bash scripts/audit-disk`, review large directories and remove only confirmed unnecessary data/packages.
- [ ] Review services after clean install and remove anything not needed by the three profiles.

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
- [x] Keyboard chooser documented.
- [x] Recovery-point behavior documented.
- [x] Hardware-aware audio behavior documented.
- [x] Helper commands documented.
- [x] Manual YouTube Music + Better Lyrics theme guide retained.
- [ ] Add screenshots only after the clean-install UI is stable.
