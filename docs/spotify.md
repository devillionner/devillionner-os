# Adaptive Spotify

The Blueprint uses the official Arch `spotify-launcher` package together with `spicetify-cli`.

## Visual base

The UI starts from Spicetify's upstream `text` theme, pinned to commit `3f55a3702bd6d87799dc97023e0fe2b11d88c704` (the 2026-09-04 Spotify 1.2.98 compatibility update). `devos-spotify-theme-bootstrap` downloads that exact CSS once, removes remote font imports, and appends the Blueprint's layout layer. JetBrains Mono Nerd Font is already installed locally.

The Blueprint does not copy 43PR's static Monochrome palette. The text-theme structure remains recognizable, but Blueprint now adds its own Caelestia-oriented surface system on top:

- compact 10 px panel gaps;
- 14 px primary pane radius and 10 px control/card radius;
- search, cards, menus and filter controls use the adaptive `surfaceContainer` semantic color;
- hover/selected surfaces use adaptive `surfaceContainerHigh`;
- borders follow `outlineVariant` / `primary` through the generated Spicetify palette;
- keyboard focus uses the adaptive accent instead of browser-default outlines;
- media corners, library rows and track rows share the same shape language;
- no extra CSS transparency is introduced.

All of those rules reference Spicetify semantic variables. `devillionner-overrides.css` intentionally contains no hard-coded hex/RGB/HSL colors, so a wallpaper change can recolor the interface without leaving static UI fragments behind.

The generated theme cache tracks two revisions independently: the pinned upstream commit and the SHA-256 fingerprint of Blueprint-owned `devillionner-overrides.css`. If either changes, `user.css` is rebuilt automatically. This prevents a Blueprint UI update from being skipped merely because the upstream Spicetify theme pin stayed the same.

## Caelestia colors

`devos-spotify-theme-sync` reads `~/.config/hypr/scheme/current.lua`, the same Material palette consumed by the Hyprland/Caelestia configuration, and generates `[Devillionner]` in Spicetify `color.ini`.

Mapping:

- accent / active border / banner -> `primary`
- background -> `surface`
- header / elevated surface -> `surfaceContainer`
- hover/highlight -> `surfaceContainerHigh`
- inactive border -> `outlineVariant`
- text -> `onSurface`
- secondary text -> `onSurfaceVariant`
- notification -> `secondary`
- error -> `error`

`devos-spotify-theme.path` watches the Caelestia/Hypr scheme directory. When wallpaper-derived colors change, it rewrites `color.ini`. Spotify is launched through `devos-spotify`, which keeps `spicetify watch -s` attached while Spotify is running, so the active client hot-reloads the new palette.

The restore rsync excludes `~/.config/caelestia/cli.json` from blind copying. One central `configure-caelestia-cli` merge owns both the Colloid-Dark theme key and the Spotify toggle while preserving unrelated Caelestia CLI settings. `configure-spotify` invokes that central owner when run standalone instead of parsing or rewriting `cli.json` itself.

## Transparency

Actual window transparency belongs to Hyprland, not the Spotify CSS. Spotify therefore uses the same Blueprint `windowOpacity = 0.95` as Dolphin. The fullscreen rule keeps the same 0.95 value instead of jumping to 1.0. Apps explicitly tagged `opaque` and games still opt out at 1.0.

The Caelestia surface layer uses opaque semantic theme colors inside the Spotify window rather than stacking another alpha layer. This keeps visual hierarchy without making Spotify more transparent than Dolphin.

## Desktop integration and links

The Blueprint shadows the stock `spotify-launcher.desktop`, but preserves the upstream desktop contract: `%U`, `TryExec` and `x-scheme-handler/spotify` remain present and route through `devos-spotify` instead of bypassing the adaptive theme.

The desktop entry keeps upstream `StartupWMClass=spotify` (lowercase). Runtime Spotify windows are not fully consistent across client/XWayland/Wayland modes, so Blueprint deliberately accepts both `Spotify` and `spotify` classes and then falls back to the initial titles `Spotify` / `Spotify Free`. Hyprland's `special:music` routing and Caelestia's music toggle share that same identity contract.

`configure-spotify` also sets `x-scheme-handler/spotify=spotify-launcher.desktop` in `~/.config/mimeapps.list`. It owns only that protocol mapping and preserves unrelated browser/MIME defaults, so clicking a `spotify:` link consistently enters the managed themed launcher instead of depending on whichever desktop association happened to exist before restore.

When a `spotify:` URI is opened while Spotify is already running, `devos-spotify` first uses the standard MPRIS `OpenUri` method so it does not unnecessarily re-run Spicetify or disturb the existing client. If MPRIS is unavailable, it falls back to `spotify-launcher`'s native positional URI support. The same native URI support is preserved on the first vanilla launch before Spotify has generated its prefs.

## Caelestia music toggle

`~/.config/caelestia/cli.json` keeps the `Super+M` music toggle on the managed `devos-spotify` command. Spotify is matched by both known class variants and then by `initialTitle` values `Spotify` / `Spotify Free`. `initialTitle` is the current Caelestia CLI JSON key; the older Blueprint `initial_title` spelling was invalid for this schema and could silently disable the title fallback when Spotify exposed no useful class.

The toggle is part of the canonical merge-managed CLI policy rather than Spotify-specific ad-hoc JSON editing. Repository CI and `check-spotify` validate the same identity aliases across Caelestia, Hyprland and the desktop entry so future client or window-system changes cannot silently split special-workspace behavior from launcher behavior.

## Single managed launcher

`devos-spotify` holds `~/.local/state/devillionner-os/spotify-wrapper.lock` with `flock` for the lifetime of the managed Spotify session. That guarantees one wrapper owns `spicetify watch -s`, so repeated app-menu or `Super+M` launches do not accumulate duplicate theme watcher processes.

A `spotify:` link is handled specially: if another managed wrapper is still starting Spotify, the new invocation waits for MPRIS and forwards the URI to the first client. Normal duplicate launches become no-ops. The lock is inherited through the vanilla fallback on first launch/theme failure, so the same single-session rule remains valid there too.

## First launch

Spicetify requires Spotify to create `~/.config/spotify/prefs`. On a fresh system, the first `devos-spotify` launch opens vanilla Spotify. Sign in and leave it open for about a minute, then close and reopen. From the second launch onward `spicetify auto` handles backup/re-apply after Spotify updates and launches the adaptive theme.

`Super+M` uses `devos-spotify` through Caelestia's music toggle configuration. Normal app-launcher starts and `spotify:` links use that same managed path.

`check-spotify` verifies the shared window identity contract, Caelestia toggle schema, real protocol association, single-wrapper guard, desktop URI contract, themed launcher routing, semantic Caelestia surface layer, no-hard-coded-color rule and both generated-theme revision markers, so a stale or partially bypassed Spotify integration is reported as a failure rather than silently behaving differently from the repository state.

Validate with:

```bash
bash scripts/check-spotify
```
