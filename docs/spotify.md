# Spotify experience

Blueprint uses the Arch `spotify-launcher` package together with `spicetify-cli`, then prepares one curated desktop experience automatically after Spotify has created its normal `prefs` file.

## Visual base: current Lucid

The visual base is the **current Lucid** theme by `sanoojes/spicetify-lucid`, not the unmaintained `Lucid V2 (Legacy)` entry. Blueprint records the upstream manifest/source identity at commit `5c5bead49d5dad971e0bb38d64e7dee88463cf83` and installs the same three assets exposed by Lucid's Marketplace manifest: `user.css`, `color.ini` and `theme.js`.

Lucid owns the main visual language. Blueprint applies a restrained preset rather than redrawing Lucid's panes:

- page mode: `default`;
- panel gap: `0`;
- player: default, non-floating, no auto-hide;
- next-song card: enabled but non-floating;
- library/right sidebar/global navigation: no auto-hide;
- global navigation: non-floating;
- colors: dynamic dark/tinted.

The preset is stored through Lucid's own persisted `lucid:settings` state and is applied once by the managed extension.

## Lyrics: ivLyrics

Blueprint installs **ivLyrics 6.6.13** as a Spicetify custom app. Its release ZIP is pinned by SHA-256:

`b3e77eaaf0f1d25276a009beefbfa30ab0478c9468712f8a96c7641f5ea2c476`

The app provides the dedicated lyrics experience, including synchronized/karaoke-style presentation and its own fullscreen view. Optional AI translation remains optional and is not configured with a secret by Blueprint.

## Curated cleanup + playback detail

`devos-clean-ui.js` is the only Blueprint-owned Spotify visual extension. It deliberately stays narrow and layers on top of Lucid. The cleanup is based on the corresponding Spicetify Marketplace snippets at Marketplace revision `ec6f772891bad4bf08b645447c2ade6b06c4f991`.

It currently:

- removes Popular shelves from Home;
- hides Recently Played Home sections;
- hides Podcasts and What's New buttons;
- hides Mini Player and Spotify fullscreen buttons;
- hides the album/playlist “Scroll through previews” action;
- keeps the video action but makes it compact;
- removes Artists/Credits cards from Now Playing while preserving queue/lyrics;
- renders the playback progress as a thin repeating wave inspired by Caelestia;
- places a pinned Oneko animation on the actual playback position.

`Declutter now playing bar` is intentionally not stacked on top because the narrower sidebar cleanup already removes the unwanted pieces without deleting useful controls. Basify is also intentionally excluded because it is an artist/distributor trust-filtering extension, not part of the desired UI experience.

## Automatic bootstrap

`devos-spotify-experience` owns the experience setup. It:

1. installs/refreshes Lucid assets;
2. installs the Blueprint cleanup/wave extension;
3. downloads and SHA-verifies pinned ivLyrics;
4. configures Lucid + dark scheme + required Spicetify injection flags;
5. adds `devos-clean-ui.js` and `ivLyrics` without deleting unrelated extension/custom-app entries.

`configure-spotify` runs the helper with `--apply` when Spotify has already completed its first launch. The normal `devos-spotify` wrapper also runs the helper before `spicetify auto`, so a fresh system becomes configured automatically on the first managed launch after the initial sign-in.

The old Blueprint Bloom bootstrap, Caelestia palette watcher, `spicetify watch -s`, remote-debugging port and custom pane/frame CSS are retired.

## Desktop integration and Spotify Connect

The desktop entry routes `%U` and `x-scheme-handler/spotify` through `devos-spotify`. The wrapper preserves the native Spotify client, so Spotify Connect behavior is not replaced by a third-party music backend.

When a `spotify:` URI is opened while Spotify is already running, `devos-spotify` first uses MPRIS `OpenUri`. If MPRIS is unavailable, it falls back to `spotify-launcher`'s positional URI support.

`devos-spotify` holds `~/.local/state/devillionner-os/spotify-wrapper.lock` with `flock` for the managed session, so repeated menu or `Super+M` launches do not create duplicate managed sessions.

The desktop entry keeps upstream `StartupWMClass=spotify`. Blueprint accepts both `Spotify` and `spotify` classes plus the initial titles `Spotify` / `Spotify Free`; Hyprland's music-workspace rules and Caelestia's music toggle share that identity contract.

## Transparency

Window transparency remains a Hyprland policy rather than a theme hack. Spotify uses the same Blueprint `windowOpacity = 0.95` policy as Dolphin, including fullscreen; apps/games explicitly tagged opaque still opt out at `1.0`.

## First launch

Spicetify requires Spotify to create `~/.config/spotify/prefs`. On a fresh installation, the first managed launch opens vanilla Spotify so the user can sign in. Leave it open for roughly a minute. On the next managed launch, Lucid, ivLyrics and the curated extension are prepared automatically before Spicetify applies.

## Validation

`check-spotify` validates the installed wrapper/helper paths, Caelestia/Hyprland identity, URI routing, single-instance guard, retirement of legacy Bloom automation, Lucid assets/revision, ivLyrics version, managed extension identity and Spicetify selections.

`check-spotify-wrapper-source` validates the same architecture at repository level, including exact ivLyrics release hash and representative cleanup/wave/Oneko source contracts.

```bash
bash scripts/check-spotify
bash scripts/check-spotify-wrapper-source
```

Source/CI validation does not prove that Spotify's current DOM still renders every third-party selector perfectly. A real full-window physical-host screenshot/playback test remains the final visual acceptance gate after Spotify, Lucid or ivLyrics updates.


## Native Wayland launcher

Blueprint manages `~/.config/spotify-launcher.conf` with `UseOzonePlatform` and `--ozone-platform=wayland`. The user-level config takes precedence over `/etc/spotify-launcher.conf`, so Blueprint keeps Spotify on the tested native Wayland GPU path without editing the distribution-owned `/etc` file.
