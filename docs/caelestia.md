# Caelestia configuration policy

Both `~/.config/caelestia/shell.json` and `~/.config/caelestia/cli.json` are merge-managed by the Blueprint. Neither file is copied wholesale during restore.

## Why

Caelestia intentionally allows users to keep only the settings they override. Replacing either JSON file during restore would erase unrelated local options, while manual JSON edits can accidentally break the object structure with a misplaced brace or comma.

`scripts/configure-caelestia` overlays only the Blueprint-owned keys from `dotfiles/.config/caelestia/shell.json`. `scripts/configure-caelestia-cli` does the same for `dotfiles/.config/caelestia/cli.json`. Both preserve every unrelated key already present in the user's file.

If an existing managed JSON file is malformed, its configurator refuses to overwrite it and reports the line/column of the parse failure. Existing symlinks are followed rather than replaced.

## Blueprint-owned shell settings

The current common `shell.json` policy owns:

- `appearance.transparency.enabled = true`;
- dashboard enabled, visible and hover-enabled;
- `general.showOverFullscreen = true`;
- `general.apps.explorer = ["dolphin"]`;
- `general.apps.playback = ["clapper"]`;
- `general.apps.terminal = ["kitty"]`;
- `services.brightnessIncrement = 0.05`;
- `services.defaultPlayer = "Spotify"`;
- now-playing toast disabled and fullscreen toasts allowed;
- the common idle policy below.

Unrelated settings such as weather location, audio application choice, battery options, launcher preferences or monitor-specific configuration are preserved.

## Blueprint-owned CLI settings

The common `cli.json` policy has one owner, `scripts/configure-caelestia-cli`, and currently manages:

- `theme.iconTheme = "Colloid-Dark"`;
- the Spotify music toggle;
- Spotify class aliases `Spotify` and `spotify`;
- `initialTitle` fallbacks `Spotify` and `Spotify Free`;
- managed command `["devos-spotify"]` and `move = true`.

Dolphin and Spotify no longer parse or rewrite `cli.json` independently. Their standalone configurators call the central CLI configurator instead, so the same safe merge behavior is used whether a component is configured directly or through a full restore.

Unrelated CLI theme keys, custom toggles and other user options remain intact. CI exercises preservation of custom keys, preservation of symlinks and refusal to overwrite malformed JSON.

## Idle policy

The Blueprint uses the current Caelestia `general.idle.timeouts` schema:

- 1800 seconds / 30 minutes: lock;
- 2100 seconds / 35 minutes: DPMS display off, DPMS on when activity returns;
- 3600 seconds / 60 minutes: `suspendThenHibernate`.

Audio playback inhibits idle actions. Charging does not inhibit them. `lockBeforeSleep` remains enabled.

## Package compatibility patches

The packaged Caelestia shell currently needs a small Blueprint compatibility/UI patch on this setup. `scripts/patch-caelestia-fullscreen` manages all current package-level changes:

- allow the sidebar shortcut while a fullscreen client is active;
- keep fullscreen input masked except while the sidebar is open;
- convert the four required Quickshell environment pragmas from `DefaultEnv` to `Env`;
- route secured unsaved Wi-Fi networks from Nexus directly to a password form before disconnecting the current network;
- preserve SSIDs exactly, including escaped backslashes, case and leading/trailing spaces from `nmcli` terse output;
- connect scanned networks with their exact SSID + BSSID instead of reconstructing a trimmed hidden-network profile;
- show password-specific errors only for authentication failures, while missing/disappeared SSIDs get a network-not-found message.

`scripts/check-caelestia-patches` validates the installed package files after restore/update. It fails when a patch is missing or when the upstream QML structure moved enough that the known result can no longer be found.

Repository CI separately runs `scripts/check-caelestia-patch-source`, which keeps patch application and runtime validation coupled to the same QML targets and exact expected results. This catches a stale checker/patch pair before it reaches a clean install.

`scripts/check-caelestia` includes the package-patch check, so a restore cannot report a clean Caelestia validation while those runtime patches are absent.

## Network UI ownership

Caelestia is the single NetworkManager UI in Blueprint. The backend remains the normal `NetworkManager` service and `nmcli`; the legacy GTK tray frontend is intentionally removed during package reconciliation.

The reconciler explicitly removes `network-manager-applet` and `nm-connection-editor`, stops and deletes stale per-user `nm-applet` service/autostart state, and leaves NetworkManager itself untouched. `libappindicator` stays explicit in the shared TV Cast manifest because FluxCast uses it as its Hyprland/KDE tray backend. The aggregate runtime check fails if either legacy frontend returns, if an nm-applet process/autostart survives, or if the FluxCast tray dependency disappears.

This package removal belongs to a full restore/reconciliation. Targeted `devos-blueprint apply caelestia` remains non-destructive and does not uninstall packages.

## Caelestia-first branding

Blueprint deliberately treats **CachyOS as the technical Arch-compatible base** and **Caelestia as the visible desktop identity**.

The managed Caelestia shell config sets `general.logo = "caelestia"`. Caelestia's own `SysInfo` logic therefore uses the Caelestia mark in the top-bar launcher, dashboard identity and lock screen instead of inheriting `LOGO=cachyos` from `/etc/os-release`. The real OS identity is not falsified: `/etc/os-release`, CachyOS repositories, kernels, mirrors, hooks, scheduler/performance settings and Snapper integration remain untouched.

The same configurator suppresses the branded background/launcher layer without removing useful technical tooling:

- the global Cachy-Update tray autostart is overridden per-user and its user timer is masked;
- any already-running Cachy-Update tray instance is stopped;
- launcher entries for Cachy-Update, CachyOS Hello, CachyOS Package Installer and CachyOS Kernel Manager are hidden;
- the kernel manager package itself may remain available as a recovery/technical tool even though it is not part of the normal launcher UX;
- full package reconciliation removes the pure desktop extras `cachyos-hello`, `cachyos-packageinstaller` and `cachyos-wallpapers`.

The reboot-sensitive boot splash and login-manager styling are intentionally separate. The existing physical host still uses GDM while Blueprint's clean-install baseline is SDDM, so boot/login branding is not changed on production until that path passes the clean-KVM + reboot gates.

## Safe apply and validation

After pulling Blueprint changes, apply the managed Caelestia JSON settings and user-level branding policy with:

```bash
bash scripts/configure-caelestia
bash scripts/configure-caelestia-cli
```

Then validate the installed state and package patches with:

```bash
bash scripts/check-caelestia
bash scripts/check-dolphin
bash scripts/check-spotify
```

For a manual edit, validate JSON before restarting the shell:

```bash
jq empty ~/.config/caelestia/shell.json
jq empty ~/.config/caelestia/cli.json
```

A full restore excludes both JSON files from the broad rsync and runs their central configurators afterward, so the same merge behavior is used on existing and clean systems.
