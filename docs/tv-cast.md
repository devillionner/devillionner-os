# TV Cast / Miracast

TV Cast is a shared Blueprint feature installed for **Gaming, Work and Laboratory**.

It mirrors the Hyprland display over **Wi-Fi Direct / Miracast (WFD)** using FluxCast. It does not use Chromecast, AirPlay or DLNA.

## Use

1. Put the TV into Wireless Screen / Miracast mode.
2. Press **Super+P** (the display/project hardware key on the ASUS Zenbook).
3. Choose one of the three supported modes:
   - **30 FPS — 1080p** — quality mode, 8 Mbps
   - **60 FPS — 720p** — smoothness mode, 8 Mbps
   - **Low Latency — 720p 30 FPS / 5 Mbps** — minimum-latency mode
4. Wait for the real WFD RTSP connection. The notification changes to connected only after TCP 7236 is established.
5. Stop only with **Stop casting** in the menu.

Pressing Super+P again only closes/reopens the Fuzzel menu; it never toggles the active cast.

## Runtime behavior

- FluxCast scans in short WFD iterations (`--wfd-timeout 3`) until a compatible TV appears.
- Casting runs in the background in tmux session `cast-tv`.
- `systemd-inhibit` blocks sleep/idle/lid-switch only while the cast is active.
- The laptop sink is muted during casting and its previous mute state is restored on stop.
- Switching between 30 FPS, 60 FPS and Low Latency tears down the previous WFD session before starting the new mode.
- Connection status is based on an established RTSP TCP 7236 session, not merely on tmux or a NetworkManager profile.
- TV scaling uses the tested `fast_bilinear` wf-recorder wrapper; the laptop's display mode is not changed.
- The supported mode set is intentionally fixed at exactly three; new modes are not added without a new measured requirement.

## Localization

The menu uses GNU gettext and follows `LANGUAGE`, `LC_ALL`, `LC_MESSAGES`, and `LANG`. English is the fallback.

For a temporary translation test:

```bash
TVCAST_LANG=ja /usr/local/bin/cast-tv-menu
```

Source `.po` catalogs live in `components/tv-cast/locale/`; restore generates `.mo` catalogs with `msgfmt`.

## FluxCast upgrades

`/etc/pacman.d/hooks/99-cast-tv-fluxcast-tune.hook` re-runs `cast-tv-fluxcast-tune` after `fluxcast-git` install/upgrade.

The tuner only rewrites known FluxCast patterns:

- `thread_queue_size` → `32`
- x264 preset → `ultrafast`

If upstream changes those structures, it prints a warning instead of guessing and corrupting the Python file.

## Firewall

The Blueprint already uses UFW. TV Cast adds only the two rules from the tested host:

- TCP `7236` — Miracast RTSP
- UDP `67` — Wi-Fi Direct DHCP

It does not disable the firewall or copy unrelated virtualization rules.

## Validation

```bash
bash scripts/check-tv-cast
```

The runtime validator checks the exact three-mode contract in addition to packages, installed helper files, syntax, bindings, catalogs and FluxCast patch state. A VM can validate those static/runtime contracts, but an end-to-end WFD connection still requires physical compatible Wi-Fi hardware and a Miracast TV.
