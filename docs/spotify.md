# Adaptive Spotify

The Blueprint uses the official Arch `spotify-launcher` package together with `spicetify-cli`.

## Visual base

The UI starts from Spicetify's upstream `text` theme, pinned to commit `3f55a3702bd6d87799dc97023e0fe2b11d88c704` (the 2026-09-04 Spotify 1.2.98 compatibility update). `devos-spotify-theme-bootstrap` downloads that exact CSS once, removes remote font imports, and appends the Blueprint's small layout layer. JetBrains Mono Nerd Font is already installed locally.

The Blueprint does not copy 43PR's static Monochrome palette. Only the text-theme layout language is retained.

The generated theme cache tracks two revisions independently: the pinned upstream commit and the SHA-256 fingerprint of Blueprint-owned `devillionner-overrides.css`. If either changes, `user.css` is rebuilt automatically. This prevents a Blueprint UI update from being skipped merely because the upstream Spicetify theme pin stayed the same.

## Caelestia colors

`devos-spotify-theme-sync` reads `~/.config/hypr/scheme/current.lua`, the same Material palette consumed by the Hyprland/Caelestia configuration, and generates `[Devillionner]` in Spicetify `color.ini`.

Mapping:

- accent / active border / banner -> `primary`
- background -> `surface`
- header -> `surfaceContainer`
- hover/highlight -> `surfaceContainerHigh`
- inactive border -> `outlineVariant`
- text -> `onSurface`
- secondary text -> `onSurfaceVariant`
- notification -> `secondary`
- error -> `error`

`devos-spotify-theme.path` watches the Caelestia/Hypr scheme directory. When wallpaper-derived colors change, it rewrites `color.ini`. Spotify is launched through `devos-spotify`, which keeps `spicetify watch -s` attached while Spotify is running, so the active client hot-reloads the new palette.

## Transparency

Actual window transparency belongs to Hyprland, not the Spotify CSS. Spotify therefore uses the same Blueprint `windowOpacity = 0.95` as Dolphin. The fullscreen rule keeps the same 0.95 value instead of jumping to 1.0. Apps explicitly tagged `opaque` and games still opt out at 1.0.

This avoids stacking CSS alpha on top of compositor alpha, which would make Spotify more transparent than Dolphin.

## Desktop integration and links

The Blueprint shadows the stock `spotify-launcher.desktop`, but preserves the upstream desktop contract: `%U`, `TryExec` and `x-scheme-handler/spotify` remain present and route through `devos-spotify` instead of bypassing the adaptive theme.

When a `spotify:` URI is opened while Spotify is already running, `devos-spotify` first uses the standard MPRIS `OpenUri` method so it does not unnecessarily re-run Spicetify or disturb the existing client. If MPRIS is unavailable, it falls back to `spotify-launcher`'s native positional URI support. The same native URI support is preserved on the first vanilla launch before Spotify has generated its prefs.

## First launch

Spicetify requires Spotify to create `~/.config/spotify/prefs`. On a fresh system, the first `devos-spotify` launch opens vanilla Spotify. Sign in and leave it open for about a minute, then close and reopen. From the second launch onward `spicetify auto` handles backup/re-apply after Spotify updates and launches the adaptive theme.

`Super+M` uses `devos-spotify` through Caelestia's music toggle configuration. Normal app-launcher starts and `spotify:` links use that same managed path.

`check-spotify` verifies the desktop URI contract, themed launcher routing and both generated-theme revision markers, so a stale or partially bypassed Spotify integration is reported as a failure rather than silently behaving differently from the repository state.

Validate with:

```bash
bash scripts/check-spotify
```
