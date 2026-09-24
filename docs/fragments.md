# Fragments torrent client

Fragments is the Blueprint torrent client for **Gaming, Work, Laboratory/Dev and University/Uni**.

The UI is intentionally lightweight: open `.torrent` / `magnet:` links, see basic transfer state, pause/resume downloads and inspect progress. The long-running BitTorrent backend is separate from the Fragments window, so the UI does not need to stay open or occupy a special workspace. The Blueprint does not install qBittorrent.

## Caelestia integration

Fragments is GTK4/libadwaita, so Blueprint keeps it on Caelestia's live GTK palette instead of maintaining a separate fixed theme.

- `~/.config/gtk-4.0/fragments.css` uses Caelestia GTK variables such as `@accent_color`, `@window_fg_color` and `@card_bg_color`.
- The Fragments window uses **0.85 compositor opacity**, matching the translucent Caelestia/Kitty visual language.
- `devos-fragments-gtk.path` watches Caelestia's generated `gtk.css`; after a wallpaper/theme refresh it restores the single `@import "fragments.css";` line that Caelestia's GTK generator replaces.
- The watcher is idempotent and does not copy or freeze palette values. New Caelestia colours flow through the GTK variables automatically.

## Background architecture

Blueprint runs Transmission independently as a user service:

```text
devos-fragments-daemon.service
└─ transmission-daemon --config-dir ~/.config/fragments
```

RPC is restricted to `127.0.0.1:9091`. Fragments is configured with a persistent non-local connection named **This computer** pointing to `http://127.0.0.1:9091/transmission/rpc`.

That separation gives the desired desktop behavior:

- `Super+Q` closes the Fragments UI normally;
- there is **no `special:fragments` workspace**;
- the Transmission service keeps downloading after the Fragments window closes;
- Fragments appears on screen only when it is explicitly opened;
- launching Fragments reconnects to the already-running localhost backend instead of spawning another daemon;
- active downloads survive a UI restart and continue automatically after login.

The managed launcher is `~/.local/bin/fragments-caelestia`. It ensures the backend/tray services are running and then launches the normal Fragments window on the current workspace.

## Caelestia tray menu

`devos-fragments-tray.service` keeps `~/.local/bin/fragments-tray` registered as a StatusNotifierItem independently of the Fragments UI.

The normal Caelestia tray popout exposes:

- **Open Fragments**;
- **Torrents (N)** → dynamic submenu;
- **Pause all**;
- **Resume all**;
- **Stop torrent service**.

The torrent submenu is refreshed from `transmission-remote` whenever it is opened. Each row shows the useful lightweight state directly in the tray, for example:

```text
↓ Example download · 42% · 2.8 MB/s
⏸ Paused item · 15%
✓ Completed item · 100%
```

Selecting a torrent opens Fragments. The tray helper re-registers itself if Caelestia/Quickshell restarts while the backend remains alive.

Stopping the torrent service is explicit because it stops background transfers and removes the tray item. Starting Fragments again starts both managed services automatically.

## Packages and defaults

The common profile explicitly owns:

- `fragments`;
- `transmission-cli`, which provides `transmission-daemon` and `transmission-remote`;
- `python-dbus`, because the tray bridge implements StatusNotifierItem/DBusMenu on the session bus.

Blueprint sets both handlers to `de.haeckerfelix.Fragments.desktop`:

- `application/x-bittorrent`;
- `x-scheme-handler/magnet`.

qBittorrent is not part of the active Blueprint manifests. A manually installed qBittorrent package is not forcibly removed; Fragments remains the Blueprint default handler.

## Existing-host migration evidence

On the ASUS UX3405CA host on **2026-09-24**, the old qBittorrent session was imported into Fragments/Transmission without deleting downloaded data. The first Blueprint Fragments integration kept the UI alive in `special:fragments`; it was then simplified to the current model with an independent Transmission user service and a normal on-demand Fragments window.

The current host exercise verifies that downloads continue while Fragments itself is closed, no `special:fragments` workspace remains, the tray stays available, and reopening Fragments reconnects to the existing daemon without creating a second one.

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
