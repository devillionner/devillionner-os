# Clean KVM validation runbook

This runbook is the next installer gate. It deliberately uses **three separate fresh CachyOS guests** so profile validation is not confused with package reconciliation after switching profiles on one machine.

It is **not** the future one-command Blueprint Test VM template. Guest creation remains explicit in virt-manager until these clean-install tests pass.

The validation path is clone-less: each guest resolves one exact Blueprint commit, installs from a temporary source archive, and validates that same pinned revision after reboot. No persistent Git checkout is required inside the guest.

## Host prerequisite

The Linux host must have working KVM/libvirt support before starting this runbook. `devos-vm validate` can be used when the Blueprint virtualization feature is installed.

Do not mark the physical-host virtualization roadmap item complete merely because a VM can be created: `/dev/kvm`, libvirt services, networking and guest graphics still need their own runtime evidence.

## Fresh guest baseline

Prepare one clean CachyOS installation and either repeat the installation three times or take a **pre-Blueprint VM snapshot** and clone/revert it separately for each profile.

Baseline requirements:

- KVM/QEMU guest, not VirtualBox;
- normal non-root user with sudo access;
- Btrfs root so the mandatory Blueprint recovery checkpoint can be created;
- working network access for repo/AUR/Spotify downloads;
- enough disk space for the selected profile;
- boot into the graphical user session before running the Blueprint installer.

Do not reuse a guest after a Blueprint profile has already been installed when claiming a **fresh profile** pass.

## Pin one Blueprint revision per test

A clean-install test must use one exact repository revision from install through the post-reboot check. Resolve `main` once and save the resulting 40-character commit:

```bash
BOOTSTRAP_URL="https://raw.githubusercontent.com/devillionner/devillionner-os/main/bootstrap"
curl -fsSL "$BOOTSTRAP_URL" \
  | bash -s -- version \
  | tee ~/blueprint-tested-commit.txt
```

Verify the file contains exactly one commit SHA:

```bash
grep -Eq '^[0-9a-f]{40}$' ~/blueprint-tested-commit.txt
```

Every install and post-reboot check below explicitly uses that saved SHA. If `main` changes while a VM test is in progress, it does not affect the in-progress test.

## Why the profile commands use `--non-interactive`

The clean-profile tests must exercise the **actual installer defaults**, not reproduce them manually with `--with virtualization` / `--without virtualization` flags.

Each command therefore supplies the profile and keyboard, uses `--non-interactive`, and deliberately omits an explicit virtualization override:

- Gaming must resolve to virtualization **off** by default;
- Work must resolve to virtualization **off** by default;
- Laboratory must resolve to virtualization **on** by default.

The destructive restore confirmation is still interactive: the user must verify the KVM target and type `RESTORE`.

## Evidence to keep

For each profile, keep the tested commit plus two logs:

```text
~/blueprint-tested-commit.txt
~/blueprint-<profile>-install.log
~/blueprint-<profile>-postreboot-check.log
```

The install log proves the temporary source revision, recovery checkpoint, package reconciliation, configurators and first aggregate check. The post-reboot log proves the resulting system survives a clean session restart and satisfies the **same revision's** runtime contract.

A warning is not automatically a failure, but every warning must be understood before the profile is marked complete.

## Gaming

From the fresh Gaming guest, first resolve and save the revision as described above, then:

```bash
BOOTSTRAP_URL="https://raw.githubusercontent.com/devillionner/devillionner-os/main/bootstrap"
REV="$(cat ~/blueprint-tested-commit.txt)"

curl -fsSL "$BOOTSTRAP_URL" \
  | bash -s -- --ref "$REV" install \
      --profile gaming \
      --keyboard windows \
      --non-interactive \
      --vm \
  2>&1 | tee ~/blueprint-gaming-install.log
```

The bootstrap must print the pinned Blueprint source revision, and the installation plan must show `Virtualization: false`. If it shows anything else, stop the test: the Gaming default is wrong.

When the restore safety prompt appears, verify the printed target says KVM/QEMU VM and then type `RESTORE`.

Before reboot, require:

- main CachyOS PARTUUID gate did not trigger because this is a KVM guest;
- a Blueprint recovery checkpoint was created and recorded;
- profile state = `gaming`;
- features include mandatory `tvcast` and do not include virtualization;
- `devos-blueprint` was installed without a persistent Git checkout;
- declared system/user service manifests pass validation;
- installed source revision matches `~/blueprint-tested-commit.txt`;
- final installer validation reports `RESULT: PASS` / `Validation: PASS` or any difference is explained and fixed before proceeding.

Then reboot and run:

```bash
REV="$(cat ~/blueprint-tested-commit.txt)"
devos-blueprint --ref "$REV" check \
  2>&1 | tee ~/blueprint-gaming-postreboot-check.log
```

Gaming is not complete until the post-reboot aggregate reports `RESULT: PASS` and identifies the temporary remote source bundle at the same revision.

## Work

Start from a separate fresh baseline guest, resolve/save its test revision, then:

```bash
BOOTSTRAP_URL="https://raw.githubusercontent.com/devillionner/devillionner-os/main/bootstrap"
REV="$(cat ~/blueprint-tested-commit.txt)"

curl -fsSL "$BOOTSTRAP_URL" \
  | bash -s -- --ref "$REV" install \
      --profile work \
      --keyboard windows \
      --non-interactive \
      --vm \
  2>&1 | tee ~/blueprint-work-install.log
```

The installation plan must show `Virtualization: false`. If it does not, stop the test rather than overriding the result with a flag.

Type `RESTORE` only after confirming the target is the KVM guest.

After the installer finishes, reboot and run:

```bash
REV="$(cat ~/blueprint-tested-commit.txt)"
devos-blueprint --ref "$REV" check \
  2>&1 | tee ~/blueprint-work-postreboot-check.log
```

Work is not complete until the post-reboot aggregate reports `RESULT: PASS` on the same revision.

Spotify may legitimately warn that a first login is still required; that warning does not replace the structural Spotify checks. Do not sign in just to make the clean-install test pass.

## Laboratory

Start from another fresh baseline guest. This test must prove that Laboratory enables virtualization **by default**, so do not pass either an explicit `--with virtualization` or `--without virtualization` override:

```bash
BOOTSTRAP_URL="https://raw.githubusercontent.com/devillionner/devillionner-os/main/bootstrap"
REV="$(cat ~/blueprint-tested-commit.txt)"

curl -fsSL "$BOOTSTRAP_URL" \
  | bash -s -- --ref "$REV" install \
      --profile laboratory \
      --keyboard windows \
      --non-interactive \
      --vm \
  2>&1 | tee ~/blueprint-laboratory-install.log
```

The installation plan must show `Virtualization: true` before restore begins. That output is part of the runtime evidence that the Laboratory default itself works.

The outer guest may not expose nested `/dev/kvm`. That is acceptable only if Blueprint reports the limitation honestly instead of pretending nested acceleration is available. The package/service/configuration contract must still be reviewed.

After reboot:

```bash
REV="$(cat ~/blueprint-tested-commit.txt)"
devos-blueprint --ref "$REV" check \
  2>&1 | tee ~/blueprint-laboratory-postreboot-check.log
```

Laboratory is not complete until the aggregate result and virtualization-specific output are understood. If nested KVM is unavailable, record that separately; it does **not** satisfy the later physical-host `/dev/kvm` validation item.

## Per-profile visual sanity check

After the post-reboot aggregate passes, do a short manual sanity pass without changing configuration:

- SDDM completed the reboot/login path and the intended Hyprland session starts;
- Caelestia shell loads without ERROR-level startup failure;
- Kitty opens;
- `Super+E` opens Dolphin through the managed wrapper;
- Dolphin thumbnails/Information panel are functional;
- Bibata Modern Ice is visible after the fresh login;
- `Super+M` launches the managed Spotify path (first-login warning is acceptable);
- `Super+P` opens the TV Cast menu and shows exactly three choices plus Stop: 1080p30, 720p60, Low Latency 720p30/5 Mbps;
- no duplicate launcher/window is created by the tested hotkeys.

A KVM guest cannot prove a real Miracast/WFD connection. The current three-mode TV Cast implementation must still be retested later against the physical TV.

## Quickshell Qt ABI exercise

Only after at least one clean profile is stable:

1. snapshot the VM;
2. record the Blueprint commit being exercised;
3. perform a real system update that changes the relevant Qt libraries;
4. confirm `rebuild-detector`/`checkrebuild` identifies stale `quickshell-git` when applicable;
5. run the normal Blueprint package reconciliation/restore path rather than manually rebuilding Quickshell first;
6. confirm the same-version-capable rebuild occurs without `--needed` blocking it;
7. require `qs --version` and `devos-blueprint --ref <tested-sha> check` to pass afterward.

If the chosen update does not actually create an ABI mismatch, record the test as inconclusive rather than marking the rebuild path validated.

## Passing the KVM gate

The KVM milestone is complete only when all of these are true:

- Gaming: its real default resolves virtualization off, then fresh install + reboot + aggregate PASS on one pinned Blueprint revision;
- Work: its real default resolves virtualization off, then fresh install + reboot + aggregate PASS on one pinned Blueprint revision;
- Laboratory: its real default resolves virtualization on, then fresh install + reboot + aggregate PASS on one pinned Blueprint revision, with virtualization state understood;
- no persistent Blueprint Git checkout is required in the guest;
- declared system/user service manifests pass the aggregate contract;
- no restore safety gate was weakened to obtain a pass;
- each install created a usable-looking recovery-point record;
- all unexplained WARN/FAIL output has been resolved or documented as an intentional environment limitation.

Only then move to the reserved physical Blueprint partition. Do not use successful existing-host migration checks as a substitute for this gate.
