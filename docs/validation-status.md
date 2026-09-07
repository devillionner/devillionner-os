# Validation status

This file records **what has actually been exercised**. A green source/CI check is not treated as proof that a fresh installation or a physical-device workflow works.

## Validation levels

| Level | Meaning |
| --- | --- |
| **CI / source** | Repository contracts, syntax, managed-file logic and static integration checks pass in GitHub Actions. |
| **Existing host** | The component has been applied/checked on the current ASUS UX3405CA CachyOS installation. This is useful migration/runtime evidence, but it is not a clean-install test. |
| **Fresh KVM** | A new CachyOS VM has been installed from a pinned temporary Blueprint source bundle, rebooted, and `devos-blueprint check` passes against the same revision. |
| **Physical test partition** | A fresh restore has passed on the reserved physical Blueprint partition after all clean-KVM gates. |

## Current matrix

| Component / gate | CI / source | Existing UX3405CA host | Fresh KVM | Physical test partition | Notes |
| --- | --- | --- | --- | --- | --- |
| Repository integrity | ✅ | n/a | ⏳ | ⏳ | GitHub Actions runs repository, documentation and component source contracts. |
| Clone-less bootstrap / source identity | ✅ | ⏳ | ⏳ | ⏳ | `bootstrap` resolves a ref to an exact commit, downloads a temporary source archive and removes it after the action. `devos-blueprint check` prefers the recorded installed revision. Source/CI is green; live host use is still pending. |
| Four-profile identity | ✅ | n/a | ⏳ | ⏳ | Gaming, Work, Laboratory/Dev and University/Uni are distinct profile identities. University is not a Work alias and currently has a deliberately common-only profile-specific package layer. |
| SDDM login/display manager | ✅ | ⏳ | ⏳ | ⏳ | Blueprint uses the CachyOS Hyprland-aligned SDDM baseline, forces the next-boot `display-manager.service` alias without restarting the current graphical session, and treats the old Blueprint GDM package as retired. |
| Service manifests | ✅ | ⏳ | ⏳ | ⏳ | `check-services` verifies that every selected system/user unit exists and is enabled. TV Cast remains daemon-free. Runtime evidence is still pending. |
| Quickshell runtime / ABI check | ✅ | ✅ | ⏳ | ⏳ | `check-quickshell` passed on the existing host. A deliberate real Qt-update rebuild exercise is still pending. |
| Caelestia merge policy + package patches | ✅ | ✅ | ⏳ | ⏳ | `check-caelestia` passed after applying the managed settings and QML patches on the existing host. |
| Dolphin | ✅ | ✅ | ⏳ | ⏳ | `check-dolphin`: 30 OK, 0 FAIL on the existing host; legacy Thunar only produced a warning. |
| Spotify integration | ✅ | ✅ core runtime | ⏳ | ⏳ | Themed launch, playback, `Super+M` and wallpaper-driven recolor were exercised. The latest pane-border cosmetic tweak still needs a visual recheck on the host. |
| Bibata Modern Ice cursor | ✅ | ✅ config/runtime | ⏳ | ⏳ | `check-cursor`: 10 OK, 0 FAIL. A logout/login visual check is still needed for compositor-side XCursor refresh. |
| TV Cast / Miracast | ✅ current three-mode source | ⚠️ previous two-mode runtime | ⏳ | ⏳ | The previously installed 1080p30/720p60 implementation passed the host check. The current **three-mode** contract, including Low Latency 720p30/5 Mbps, still needs a physical host + TV retest. |
| Full aggregate `devos-blueprint check` | ✅ contract | ⏳ | ⏳ | ⏳ | Internally runs the canonical `scripts/check` contract from an exact temporary revision. Existing-host rerun is pending, including keyboard/state, SDDM and service-manifest differences. |
| Gaming profile install | ✅ source wiring | — | ⏳ | ⏳ | Fresh KVM must prove virtualization defaults off, reboot, and aggregate PASS. |
| Work profile install | ✅ source wiring | partial migration only | ⏳ | ⏳ | Existing host work-profile components are not equivalent to a fresh Work install. |
| Laboratory / Dev profile install | ✅ source wiring | — | ⏳ | ⏳ | Clean KVM must prove virtualization defaults on and the nested-KVM limitation is reported honestly if present. |
| University / Uni profile install | ✅ source wiring | — | ⏳ | ⏳ | Distinct University identity is wired with virtualization off by default. University-specific apps are intentionally not guessed before the real study workflow is defined. |
| Recovery checkpoint / rollback | ✅ source wiring | ⏳ | ⏳ | ⏳ | Automatic package-manager Snapper snapshots have been observed, but the Blueprint recovery-point record and a usable rollback have not yet been validated as an installer gate. |
| Virtualization + accelerated Linux guest | ✅ source wiring | ⏳ | ⏳ | ⏳ | Physical `/dev/kvm`, libvirt runtime and virtio/virgl vs `llvmpipe` remain pending. |

Legend: ✅ exercised at that level · ⚠️ useful evidence but current code differs · ⏳ pending · — not applicable/not attempted.

## Next validation order

1. On the existing ASUS host, install/test the clone-less helper, then run the current aggregate without relying on `/tmp/devillionner-os-check`.
2. Finish the small host checks: SDDM/service state, Spotify pane border and Bibata cursor after relogin.
3. Apply the current TV Cast component and exercise all **three** modes against the physical Miracast TV, especially Low Latency.
4. Resolve the intended keyboard layout/switch policy, then rerun `devos-blueprint check` on the host.
5. Fresh **Gaming** KVM → reboot → pinned `devos-blueprint check`.
6. Fresh **Work** KVM → reboot → pinned `devos-blueprint check`.
7. Fresh **Laboratory / Dev** KVM → reboot → pinned `devos-blueprint check`, including virtualization state.
8. Fresh **University / Uni** KVM → reboot → pinned `devos-blueprint check` and verify the saved profile remains `university`.
9. Exercise a real Qt update in a clean KVM and confirm automatic `quickshell-git` ABI rebuild.
10. Validate physical-host KVM/virgl behavior.
11. Only after all four VM profiles pass, use the reserved physical Blueprint test partition.
12. Verify the pre-restore Snapper/Btrfs recovery point is actually usable before any production restore is considered.

## Rule

Do not upgrade a status from source/CI to runtime merely because the corresponding script exists or CI is green. Runtime levels are checked only after the real environment has been exercised and the observed result is recorded here.
