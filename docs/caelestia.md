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
- convert the four required Quickshell environment pragmas from `DefaultEnv` to `Env`.

`scripts/check-caelestia-patches` validates the installed package files after restore/update. It fails when a patch is missing or when the upstream QML structure moved enough that the known result can no longer be found.

Repository CI separately runs `scripts/check-caelestia-patch-source`, which keeps patch application and runtime validation coupled to the same QML targets and exact expected results. This catches a stale checker/patch pair before it reaches a clean install.

`scripts/check-caelestia` includes the package-patch check, so a restore cannot report a clean Caelestia validation while those runtime patches are absent.

## Safe apply and validation

After pulling Blueprint changes, apply the managed Caelestia JSON settings with:

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
