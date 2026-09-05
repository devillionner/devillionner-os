# TV Cast component

Shared source for the Blueprint's WFD/Miracast TV Cast feature.

The runtime scripts, wf-recorder scaling wrapper, Fuzzel menu config and pacman hook were captured from the tested working CachyOS host on 2026-08-27. The FluxCast tuner keeps the tested transformations but adds conservative upstream-pattern checks. Existing compiled gettext catalogs were converted back to source `.po` files; restore generates `.mo` catalogs with `msgfmt`.

The final supported runtime modes are intentionally limited to exactly three:

- 30 FPS — 1920x1080 / 8 Mbps (quality)
- 60 FPS — 1280x720 / 8 Mbps (smoothness)
- Low Latency — 1280x720 / 30 FPS / 5 Mbps

Runtime state is intentionally not stored here: no tmux sessions, logs, PID/profile files, temporary NetworkManager P2P connections or Wi-Fi secrets.
