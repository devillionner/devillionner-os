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
| Clone-less bootstrap / source identity | ✅ | ✅ | ⏳ | ⏳ | `devos-blueprint setup-cli`, `version`, targeted `apply` and `check` were exercised on the host. Source was resolved to an exact commit, downloaded into a temporary directory, used successfully and removed without a persistent Git checkout. The host predates full Blueprint restore, so an installed full-system revision is intentionally not recorded yet. |
| Targeted clone-less component apply | ✅ | ✅ | ⏳ | ⏳ | Hardware, cursor, Dolphin and TV Cast were repaired on the existing host through `devos-blueprint apply` without restore/profile switching/package reconciliation. The apply path is source-guarded against package removal. |
| Four-profile identity | ✅ | n/a | ⏳ | ⏳ | Gaming, Work, Laboratory/Dev and University/Uni are distinct profile identities. University is not a Work alias and currently has a deliberately common-only profile-specific package layer. |
| SDDM login/display manager | ✅ | ⚠️ migration pending | ⏳ | ⏳ | Existing host still runs GDM and has no SDDM package. Blueprint clean installs standardize on SDDM, but the live production host is deliberately not migrated before clean-KVM/reboot validation. |
| Service manifests | ✅ | ⚠️ SDDM-only drift | ⏳ | ⏳ | All currently present common/user services passed on the existing host; the only service-manifest failure is the intentionally pending SDDM migration. |
| Hardware-aware audio policy | ✅ | ✅ | ⏳ | ⏳ | Targeted hardware apply identified ASUS UX3405CA, restored the matching EasyEffects presets and exposed `eq-laptop`, `eq-dolby` and `eq-sony`; aggregate audio validation then passed. |
| Quickshell runtime / ABI check | ✅ | ✅ | ⏳ | ⏳ | `check-quickshell` passed on the existing host. A deliberate real Qt-update rebuild exercise is still pending. |
| Caelestia merge policy + package patches | ✅ | ✅ | ⏳ | ⏳ | `check-caelestia` passed after applying the managed settings and QML patches on the existing host. |
| Dolphin | ✅ | ✅ | ⏳ | ⏳ | After clone-less targeted apply, `check-dolphin`: 30 OK, 0 FAIL; global previews are enabled and only legacy Thunar remains as a warning. |
| Spotify integration | ✅ | ✅ core runtime | ⏳ | ⏳ | Themed launch, playback, `Super+M` and wallpaper-driven recolor were exercised. The latest pane-border cosmetic tweak still needs a visual recheck on the host. |
| Bibata Modern Ice cursor | ✅ | ✅ config/runtime | ⏳ | ⏳ | After clone-less targeted apply, `check-cursor`: 10 OK, 0 FAIL including GSettings. A logout/login visual check is still needed for compositor-side XCursor refresh. |
| TV Cast / Miracast | ✅ current three-mode source | ✅ component contract; TV retest pending | ⏳ | ⏳ | The current installed host now passes the exact 1080p30/8 Mbps, 720p60/8 Mbps and Low Latency 720p30/5 Mbps runtime contract. Actual casting through all three modes against the physical Miracast TV still needs a retest. |
| Full aggregate `devos-blueprint check` | ✅ contract | ⚠️ 5 FAIL remain | ⏳ | ⏳ | Clone-less aggregate now reaches the live host correctly. Remaining failures are deliberate/unresolved host drift: keyboard policy, profile-dependent package identity, SDDM package/display-manager state and the corresponding SDDM service check. |
| Gaming profile install | ✅ source wiring | — | ⏳ | ⏳ | Fresh KVM must prove virtualization defaults off, reboot, and aggregate PASS. |
| Work profile install | ✅ source wiring | partial migration only | ⏳ | ⏳ | Current host has no saved profile state; the fallback Work check should not be treated as proof that this physical system is intended to be Work. |
| Laboratory / Dev profile install | ✅ source wiring | — | ⏳ | ⏳ | Clean KVM must prove virtualization defaults on and the nested-KVM limitation is reported honestly if present. |
| University / Uni profile install | ✅ source wiring | — | ⏳ | ⏳ | Distinct University identity is wired with virtualization off by default. University-specific apps are intentionally not guessed before the real study workflow is defined. |
| Recovery checkpoint / rollback | ✅ source wiring | ✅ record / ⏳ rollback | ⏳ | ⏳ | `devos-blueprint check` now confirms a Blueprint pre-restore recovery-point record exists on the host. A real usable rollback is still unverified. |
| Virtualization + accelerated Linux guest | ✅ source wiring | ⏳ | ⏳ | ⏳ | Physical `/dev/kvm`, libvirt runtime and virtio/virgl vs `llvmpipe` remain pending. |

Legend: ✅ exercised at that level · ⚠️ useful evidence/current migration drift remains · ⏳ pending · — not applicable/not attempted.

## Next validation order

1. Decide the intended identity of the current physical host (likely candidate: Gaming), then run an explicit non-mutating `devos-blueprint check --profile <profile>` before recording profile state.
2. Resolve the intended `EN ↔ UA` keyboard layout/switch policy on the existing host.
3. Keep the current GDM host unchanged until SDDM has passed a clean-KVM install + reboot; only then consider an explicit live-host migration.
4. Visually recheck the latest Spotify pane-border tweak and Bibata after logout/login.
5. Exercise all **three** current TV Cast modes against the physical Miracast TV, especially Low Latency.
6. Fresh **Gaming** KVM → reboot → pinned `devos-blueprint check`.
7. Fresh **Work** KVM → reboot → pinned `devos-blueprint check`.
8. Fresh **Laboratory / Dev** KVM → reboot → pinned `devos-blueprint check`, including virtualization state.
9. Fresh **University / Uni** KVM → reboot → pinned `devos-blueprint check` and verify the saved profile remains `university`.
10. Exercise a real Qt update in a clean KVM and confirm automatic `quickshell-git` ABI rebuild.
11. Validate physical-host KVM/virgl behavior.
12. Only after all four VM profiles pass, use the reserved physical Blueprint test partition.
13. Verify the pre-restore Snapper/Btrfs recovery point is actually usable before any production restore is considered.

## Rule

Do not upgrade a status from source/CI to runtime merely because the corresponding script exists or CI is green. Runtime levels are checked only after the real environment has been exercised and the observed result is recorded here.
