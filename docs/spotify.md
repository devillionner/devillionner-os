# Adaptive Spotify

The Blueprint uses the official Arch `spotify-launcher` package together with `spicetify-cli`.

## Visual base

The UI starts from Spicetify's upstream `text` theme, pinned to commit `3f55a3702bd6d87799dc97023e0fe2b11d88c704` (the 2026-09-04 Spotify 1.2.98 compatibility update). `devos-spotify-theme-bootstrap` downloads that exact CSS once, removes remote font imports, and appends the Blueprint's small layout layer. JetBrains Mono Nerd Font is already installed locally.

The Blueprint does not copy 43PR's static Monochrome palette. Only the text-theme layout language is retained.

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

## First launch

Spicetify requires Spotify to create `~/.config/spotify/prefs`. On a fresh system, the first `devos-spotify` launch opens vanilla Spotify. Sign in and leave it open for about a minute, then close and reopen. From the second launch onward `spicetify auto` handles backup/re-apply after Spotify updates and launches the adaptive theme.

`Super+M` uses `devos-spotify` through Caelestia's music toggle configuration. The user desktop entry also shadows the stock `spotify-launcher.desktop`, so normal app-launcher starts use the same path.

Validate with:

```bash
bash scripts/check-spotify
```
