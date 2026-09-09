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
| Spotify integration | ✅ | ✅ configuration / live Wayland window | ⏳ | ⏳ | Lucid dynamic colors, ivLyrics 6.6.13, native progress and Oneko are merged. Existing-host check: 30 OK / 0 FAIL; system and user UI bytes match canonical source. No fresh-install claim. |
| Bibata Modern Ice cursor | ✅ | ✅ config/runtime | ⏳ | ⏳ | PR #51 fixes the sweet-cursors login override in variables.lua. Canonical targeted apply and check: 11 OK / 0 FAIL / 1 pending-login warning. Actual logout/login visual validation remains pending. |
| TV Cast / Miracast | ✅ current three-mode source | ✅ component contract; TV retest pending | ⏳ | ⏳ | The current installed host now passes the exact 1080p30/8 Mbps, 720p60/8 Mbps and Low Latency 720p30/5 Mbps runtime contract. Actual casting through all three modes against the physical Miracast TV still needs a retest. |
| Full aggregate `devos-blueprint check` | ✅ contract | ⚠️ 5 FAIL remain | ⏳ | ⏳ | Explicit Gaming audit: SDDM package, display-manager and service failures; darkly manifest package replaced locally by darkly-bin without a Provides declaration; missing Dolphin global preview state. Keyboard and saved Gaming identity now pass. |
| Gaming profile install | ✅ source wiring | — | ⏳ | ⏳ | Fresh KVM must prove virtualization defaults off, reboot, and aggregate PASS. |
| Work profile install | ✅ source wiring | — | ⏳ | ⏳ | Existing host is explicitly Gaming, not Work. Work clean install remains pending. |
| Laboratory / Dev profile install | ✅ source wiring | — | ⏳ | ⏳ | Clean KVM must prove virtualization defaults on and the nested-KVM limitation is reported honestly if present. |
| University / Uni profile install | ✅ source wiring | — | ⏳ | ⏳ | Distinct University identity is wired with virtualization off by default. University-specific apps are intentionally not guessed before the real study workflow is defined. |
| Recovery checkpoint / rollback | ✅ root-only source wiring | ⚠️ record only / home uncovered | ⏳ | ⏳ | Host records snapper:223; existence remains unverified without privileged access. Root is /@ and home is separate /@home. Root-only snapshots do not protect home dotfiles; coordinated coverage and real rollback usability remain required. |
| Virtualization + accelerated Linux guest | ✅ source wiring | ⏳ | ⏳ | ⏳ | Physical `/dev/kvm`, libvirt runtime and virtio/virgl vs `llvmpipe` remain pending. |

Legend: ✅ exercised at that level · ⚠️ useful evidence/current migration drift remains · ⏳ pending · — not applicable/not attempted.

## Next validation order

1. Finish existing-host configuration discrepancies and define coordinated root/home recovery before any production restore.
2. Keep GDM on the current host until SDDM passes clean-KVM validation.
3. Confirm Bibata visually after logout/login.
4. TV Cast: owner reports the last physical cast worked normally; current three-mode contracts pass. No TV is available for a new end-to-end test, so defer it.
5. After necessary source work is complete, fresh Gaming, Work, Laboratory/Dev and University/Uni KVM installs → reboot → pinned check.
6. Exercise a real Qt update and Quickshell ABI rebuild in a clean KVM.
7. Validate KVM/virgl graphics; then use the reserved physical partition only after all four VM profiles pass.
8. Prove recovery usability before any production restore.

## Existing-host audit — 2026-09-09

- Physical host: `cachyos-asus-gaming`; owner selected and recorded `gaming`.
- EN/UA: `us,ua`, Ukrainian Windows Enhanced, `copilot` mode with Copilot/Menu bindings; Hyprland reports no config errors.
- Audit baseline: `bb9d16b0a9bd8532d99e628dcca29cf791b884f7`. No restore, reboot, package replacement or rollback was performed.
- The first aggregate run blocked because checkrebuild reads non-TTY stdin. That scanner was terminated; its apparent PASS from the old error-swallowing code is invalid evidence. The corrected checker closes stdin, bounds the scan, and fails on scanner errors. A separate real corrected scan passed (5 OK / 0 FAIL); isolated open-stdin, failure-exit and ABI-drift cases also passed.
- `darkly-bin 0.5.39-2` is installed but declares no `Provides: darkly`. This is a manifest/package-identity discrepancy, not proof that the Qt style files are absent. No package swap was attempted.
- Dolphin global preview state file is absent; preview backends and the other checked Dolphin settings pass. No UI preference was changed during this audit.
- Full-system `source-revision` remains intentionally absent: targeted component updates are not a full restore. Do not write the latest main SHA there merely to remove a warning. Future per-component provenance must be kept separate and must distinguish applied source from successful runtime validation.

## Rule

Do not upgrade a status from source/CI to runtime merely because the corresponding script exists or CI is green. Runtime levels are checked only after the real environment has been exercised and the observed result is recorded here.
