# Adaptive Spotify

The Blueprint uses the official Arch `spotify-launcher` package together with `spicetify-cli`.

## Visual base: Bloom

Spotify now uses **Bloom** by `nimsandu/spicetify-bloom` as the visual/layout base, pinned to commit `654cfed682b94613b0029997ffafc1eadccc5bef`.

`devos-spotify-theme-bootstrap` downloads only Bloom's pinned `user.css` and `theme.js` into the Blueprint-owned `devillionner-bloom` theme directory. The former custom `text`-theme pane/frame override has been retired completely: Blueprint no longer redraws Spotify panel borders, labels or corner geometry.

Bloom remains the visual owner; Blueprint owns only:

- the exact upstream revision pin;
- the generated Caelestia-adaptive `color.ini`;
- the managed launcher/protocol integration;
- Hyprland window policy;
- live palette synchronization.

Bloom recommends the Segoe UI family. Blueprint deliberately does not redistribute or silently download Microsoft's font files. On Linux Bloom therefore uses its normal CSS fallback when Segoe UI is not already installed. Font choice can be revisited separately after the theme itself is validated on the real host.

Bloom requires CSS color replacement, asset overrides and its theme JavaScript. `devos-spotify` therefore selects:

- `current_theme = devillionner-bloom`
- `color_scheme = Devillionner`
- `inject_css = 1`
- `replace_colors = 1`
- `overwrite_assets = 1`
- `inject_theme_js = 1`

## Caelestia colors

`devos-spotify-theme-sync` reads `~/.config/hypr/scheme/current.lua`, the same Material palette consumed by the Hyprland/Caelestia configuration, and writes a Bloom-compatible `[Devillionner]` scheme.

The main mapping is:

- Bloom `accent`, `button`, `button-active`, playback accent -> Caelestia `primary`
- main background -> `surface`
- player/card/elevated surfaces -> `surfaceContainer`
- selected/disabled surfaces -> `surfaceContainerHigh`
- contour/player border -> `outlineVariant`
- text -> `onSurface`
- secondary text -> `onSurfaceVariant`
- notification -> `secondary`
- error -> `error`

`devos-spotify-theme.path` watches the Caelestia/Hypr scheme directory. When wallpaper-derived colors change, it rewrites Bloom's `color.ini`. Spotify is launched through `devos-spotify`, which keeps `spicetify watch -s` attached while Spotify is running, so the active client can hot-reload palette changes.

The restore rsync excludes `~/.config/caelestia/cli.json` from blind copying. One central `configure-caelestia-cli` merge owns both the Colloid-Dark theme key and the Spotify toggle while preserving unrelated Caelestia CLI settings. `configure-spotify` invokes that central owner when run standalone instead of parsing or rewriting `cli.json` itself.

## Transparency

Actual window transparency belongs to Hyprland, not the Spotify theme. Spotify uses the same Blueprint `windowOpacity = 0.95` policy as Dolphin, including fullscreen. Apps explicitly tagged `opaque` and games still opt out at 1.0.

## Desktop integration and links

The Blueprint shadows the stock `spotify-launcher.desktop`, but preserves `%U`, `TryExec` and `x-scheme-handler/spotify`, routing them through `devos-spotify`.

The desktop entry keeps upstream `StartupWMClass=spotify` (lowercase). Runtime Spotify windows are not fully consistent across client/XWayland/Wayland modes, so Blueprint deliberately accepts both `Spotify` and `spotify` classes and then falls back to the initial titles `Spotify` / `Spotify Free`. Hyprland's `special:music` routing and Caelestia's music toggle share that identity contract.

`configure-spotify` sets `x-scheme-handler/spotify=spotify-launcher.desktop` in `~/.config/mimeapps.list` while preserving unrelated MIME/browser defaults.

When a `spotify:` URI is opened while Spotify is already running, `devos-spotify` first uses MPRIS `OpenUri`. If MPRIS is unavailable, it falls back to `spotify-launcher`'s native positional URI support.

## Single managed launcher

`devos-spotify` holds `~/.local/state/devillionner-os/spotify-wrapper.lock` with `flock` for the lifetime of the managed Spotify session. Repeated menu or `Super+M` launches therefore do not accumulate duplicate `spicetify watch -s` processes.

A URI launch that races with startup waits for the first client to expose MPRIS; ordinary duplicate launches become no-ops.

## First launch

Spicetify requires Spotify to create `~/.config/spotify/prefs`. On a fresh system, the first `devos-spotify` launch opens vanilla Spotify. Sign in and leave it open for about a minute, then close and reopen. From the second launch onward `spicetify auto` handles backup/re-apply after Spotify updates and launches Bloom.

## Validation

`check-spotify` verifies:

- the canonical system launcher and user-local shim;
- Caelestia/Hyprland Spotify identity aliases;
- real `spotify:` protocol routing;
- the single-wrapper guard;
- pinned Bloom `user.css` + `theme.js`;
- exact Bloom upstream revision;
- retirement of the old custom pane/frame CSS;
- Bloom-compatible adaptive `color.ini`;
- palette watcher;
- Bloom theme, scheme, asset override and `theme.js` Spicetify settings.

Validate with:

```bash
bash scripts/check-spotify
```

A green source/runtime check does not replace visual validation after a Spotify/Bloom update. Bloom is third-party UI code and Spotify updates frequently, so the physical-host visual test remains part of the acceptance gate.
