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

## Safe apply and validation

After pulling Blueprint changes, apply only the managed Caelestia shell settings with:

```bash
bash scripts/configure-caelestia
```

Validate the installed state with:

```bash
bash scripts/check-caelestia
```

For a manual edit, validate JSON before restarting the shell:

```bash
jq empty ~/.config/caelestia/shell.json
```

A full restore excludes `caelestia/shell.json` from the broad rsync and runs `configure-caelestia` afterward, so the same merge behavior is used on both existing and clean systems.
