# Caelestia shell policy

`~/.config/caelestia/shell.json` is merge-managed by the Blueprint. It is not copied wholesale during restore.

## Why

Caelestia intentionally allows users to keep only the settings they override. Replacing the entire file during restore would erase unrelated local options, while manual JSON edits can accidentally break the object structure with a misplaced brace or comma.

`scripts/configure-caelestia` therefore overlays only the Blueprint-owned keys from `dotfiles/.config/caelestia/shell.json` and preserves every unrelated key already present in the user's file.

If the existing file is malformed JSON, the configurator refuses to overwrite it and reports the line/column of the parse failure. An existing symlink is followed rather than replaced.

## Blueprint-owned settings

The current common policy owns:

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

After pulling Blueprint changes, apply only the managed Caelestia shell settings with:

```bash
bash scripts/configure-caelestia
```

Validate the installed state and package patches with:

```bash
bash scripts/check-caelestia
```

For a manual edit, validate JSON before restarting the shell:

```bash
jq empty ~/.config/caelestia/shell.json
```

A full restore excludes `caelestia/shell.json` from the broad rsync and runs `configure-caelestia` afterward, so the same merge behavior is used on both existing and clean systems.
