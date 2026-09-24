# Fragments torrent client

Fragments is the Blueprint torrent client for **Gaming, Work, Laboratory/Dev and University/Uni**.

The goal is intentionally small: open `.torrent` / `magnet:` links, see basic transfer state, pause/resume downloads, and keep transfers running without a permanent full-size application window. The Blueprint does not install qBittorrent.

## Caelestia integration

Fragments is GTK4/libadwaita, so Blueprint keeps it on Caelestia's live GTK palette instead of maintaining a separate fixed theme.

- `~/.config/gtk-4.0/fragments.css` uses Caelestia GTK variables such as `@accent_color`, `@window_fg_color` and `@card_bg_color`.
- The Fragments window uses **0.85 compositor opacity**, matching the translucent Caelestia/Kitty visual language.
- `devos-fragments-gtk.path` watches Caelestia's generated `gtk.css`; after a wallpaper/theme refresh it restores the single `@import "fragments.css";` line that Caelestia's GTK generator replaces.
- The watcher is idempotent and does not copy or freeze palette values. New Caelestia colours flow through the GTK variables automatically.

## Background behavior

`Super+Q` keeps its normal meaning everywhere except Fragments:

- on a normal window, `Super+Q` closes the active window;
- on Fragments, `Super+Q` moves the window to hidden `special:fragments` instead of terminating it;
- the Fragments process and its `transmission-daemon` continue downloading;
- launching Fragments again restores and focuses the existing window instead of spawning a second UI instance.

The managed launcher is `~/.local/bin/fragments-caelestia`. The desktop entry disables D-Bus activation and routes app-menu, `.torrent` and `magnet:` launches through that wrapper.

## Caelestia tray menu

While Fragments is running, `~/.local/bin/fragments-tray` registers a StatusNotifierItem with Caelestia/Quickshell.

The normal Caelestia tray popout exposes:

- **Open Fragments**;
- **Torrents (N)** → dynamic submenu;
- **Pause all**;
- **Resume all**;
- **Quit Fragments**.

The torrent submenu is refreshed from `transmission-remote` whenever it is opened. Each row shows the useful lightweight state directly in the tray, for example:

```text
↓ Example download · 42% · 2.8 MB/s
⏸ Paused item · 15%
✓ Completed item · 100%
```

Selecting a torrent restores the Fragments window. The tray helper also re-registers itself if Caelestia/Quickshell restarts while Fragments stays alive.

## Packages and defaults

The common profile explicitly owns:

- `fragments`;
- `transmission-cli`, because the Blueprint tray integration directly uses `transmission-remote`;
- `python-dbus`, because the tray bridge implements StatusNotifierItem/DBusMenu on the session bus.

Blueprint sets both handlers to `de.haeckerfelix.Fragments.desktop`:

- `application/x-bittorrent`;
- `x-scheme-handler/magnet`.

qBittorrent is not part of the active Blueprint manifests. A manually installed qBittorrent package is not forcibly removed; Fragments remains the Blueprint default handler.

## Existing-host migration evidence

On the ASUS UX3405CA host on **2026-09-24**, the old qBittorrent UI was removed and the existing torrent session was imported into Fragments/Transmission without deleting downloaded data. Background hiding, continued transfer activity, tray registration, menu controls and the live torrent submenu were exercised on the real Caelestia session.

The imported torrent contents themselves are user data and are **not** committed to the Blueprint or recreated on a fresh install.

## Validation

Focused runtime validation:

```bash
bash scripts/check-fragments
```

Source/CI validation:

```bash
bash scripts/check-fragments-source
```

The aggregate `devos-blueprint check` also runs the focused Fragments validator.
