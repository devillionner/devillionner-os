# Tools and helper commands

## Validation

```bash
bash scripts/check
```

Checks the selected profile, core binaries, Quickshell runtime, Caelestia compatibility patches, keyboard mode, hardware/audio helper selection, services and Git state.

## Disk audit

```bash
bash scripts/audit-disk
```

Reports the largest top-level home directories, `/var` usage, Pacman cache size, orphan packages and journal size. It deletes nothing.

The Work profile also installs Baobab for a visual disk-usage view.

## Audio helpers

ASUS Zenbook UX3405CA: `eq-laptop`, `eq-dolby`, `eq-sony`.

Generic laptop: `eq-laptop`, `eq-dolby`.

Desktop: `eq-pc`, `eq-dolby`.

## Caelestia restart

```bash
qs -c caelestia kill
caelestia shell -d
```

The Blueprint validates `qs --version` because Quickshell can require a rebuild after a Qt private-ABI update.

## YouTube Music

YouTube Music is intentionally manual for now. See `docs/youtube-music.md`.
