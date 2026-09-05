# Validation status

This file records **what has actually been exercised**. A green source/CI check is not treated as proof that a fresh installation or a physical-device workflow works.

## Validation levels

| Level | Meaning |
| --- | --- |
| **CI / source** | Repository contracts, syntax, managed-file logic and static integration checks pass in GitHub Actions. |
| **Existing host** | The component has been applied/checked on the current ASUS UX3405CA CachyOS installation. This is useful migration/runtime evidence, but it is not a clean-install test. |
| **Fresh KVM** | A new CachyOS VM has been installed from the Blueprint, rebooted, and `bash scripts/check` passes. |
| **Physical test partition** | A fresh restore has passed on the reserved physical Blueprint partition after the KVM gates. |

## Current matrix

| Component / gate | CI / source | Existing UX3405CA host | Fresh KVM | Physical test partition | Notes |
| --- | --- | --- | --- | --- | --- |
| Repository integrity | ✅ | n/a | ⏳ | ⏳ | GitHub Actions runs repository, documentation and component source contracts. |
| Quickshell runtime / ABI check | ✅ | ✅ | ⏳ | ⏳ | `check-quickshell` passed on the existing host. A deliberate real Qt-update rebuild exercise is still pending. |
| Caelestia merge policy + package patches | ✅ | ✅ | ⏳ | ⏳ | `check-caelestia` passed after applying the managed settings and QML patches on the existing host. |
| Dolphin | ✅ | ✅ | ⏳ | ⏳ | `check-dolphin`: 30 OK, 0 FAIL on the existing host; legacy Thunar only produced a warning. |
| Spotify integration | ✅ | ✅ core runtime | ⏳ | ⏳ | Themed launch, playback, `Super+M` and wallpaper-driven recolor were exercised. The latest pane-border cosmetic tweak still needs a visual recheck on the host. |
| Bibata Modern Ice cursor | ✅ | ✅ config/runtime | ⏳ | ⏳ | `check-cursor`: 10 OK, 0 FAIL. A logout/login visual check is still needed for compositor-side XCursor refresh. |
| TV Cast / Miracast | ✅ current three-mode source | ⚠️ previous two-mode runtime | ⏳ | ⏳ | The previously installed 1080p30/720p60 implementation passed the host check. The current **three-mode** contract (including Low Latency 720p30/5 Mbps and 1080p30 at 8 Mbps) still needs a physical host + TV retest. |
| Full aggregate `bash scripts/check` | ✅ contract | ⏳ | ⏳ | ⏳ | The first existing-host aggregate run correctly exposed migration drift; focused components were then repaired. A current full-host rerun is still pending, and keyboard/state differences must be resolved deliberately. |
| Gaming profile install | ✅ source wiring | — | ⏳ | ⏳ | Fresh KVM install is the next clean-install gate. |
| Work profile install | ✅ source wiring | partial migration only | ⏳ | ⏳ | Existing host work-profile components are not equivalent to a fresh Work install. |
| Laboratory profile install | ✅ source wiring | — | ⏳ | ⏳ | Must include virtualization by default in the clean KVM test. |
| Recovery checkpoint / rollback | ✅ source wiring | ⏳ | ⏳ | ⏳ | Automatic package-manager Snapper snapshots have been observed, but the Blueprint recovery-point record and a usable rollback have not yet been validated as an installer gate. |
| Virtualization + accelerated Linux guest | ✅ source wiring | ⏳ | ⏳ | ⏳ | Physical `/dev/kvm`, libvirt runtime and virtio/virgl vs `llvmpipe` remain pending. |

Legend: ✅ exercised at that level · ⚠️ useful evidence but current code differs · ⏳ pending · — not applicable/not attempted.

## Next validation order

1. Finish the two small existing-host visual checks when the laptop is available: Spotify pane border and Bibata cursor after relogin.
2. Apply the current TV Cast component and exercise all **three** modes against the physical Miracast TV, especially Low Latency.
3. Resolve the intended keyboard layout/switch policy, then rerun the current aggregate `bash scripts/check` on the existing host.
4. Fresh **Gaming** install in KVM → reboot → `bash scripts/check`.
5. Fresh **Work** install in KVM → reboot → `bash scripts/check`.
6. Fresh **Laboratory** install in KVM → reboot → `bash scripts/check`, including virtualization state.
7. Exercise a real Qt update in a clean KVM and confirm automatic `quickshell-git` ABI rebuild.
8. Validate physical-host KVM/virgl behavior.
9. Only after the VM gates pass, use the reserved physical Blueprint test partition.
10. Verify the pre-restore Snapper/Btrfs recovery point is actually usable before any production restore is considered.

## Rule

Do not upgrade a status from source/CI to runtime merely because the corresponding script exists or CI is green. Runtime levels are checked only after the real environment has been exercised and the observed result is recorded here.
