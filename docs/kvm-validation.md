# Clean KVM validation runbook

This runbook is the next installer gate. It deliberately uses **three separate fresh CachyOS guests** so profile validation is not confused with package reconciliation after switching profiles on one machine.

It is **not** the future one-command Blueprint Test VM template. Guest creation remains explicit in virt-manager until these clean-install tests pass.

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

A clean-install test must use one exact repository revision from install through the post-reboot check. Do **not** `git pull` between those two stages.

Immediately after cloning, record the tested revision:

```bash
cd ~/devillionner-os
git rev-parse HEAD | tee ~/blueprint-tested-commit.txt
```

After reboot, verify the same revision is still checked out before validation:

```bash
cd ~/devillionner-os
test "$(git rev-parse HEAD)" = "$(cat ~/blueprint-tested-commit.txt)"
```

If `main` changes while a VM test is in progress, finish or discard that test first. Update to the newer commit only before starting a new clean validation cycle.

## Evidence to keep

For each profile, keep the tested commit plus two logs:

```text
~/blueprint-tested-commit.txt
~/blueprint-<profile>-install.log
~/blueprint-<profile>-postreboot-check.log
```

The install log proves the recovery checkpoint, package reconciliation, configurators and first aggregate check. The post-reboot log proves the resulting system survives a clean session restart and satisfies the **same revision's** runtime contract.

A warning is not automatically a failure, but every warning must be understood before the profile is marked complete.

## Gaming

From the fresh Gaming guest:

```bash
git clone https://github.com/devillionner/devillionner-os.git ~/devillionner-os
cd ~/devillionner-os
git rev-parse HEAD | tee ~/blueprint-tested-commit.txt

bash scripts/install \
  --profile gaming \
  --keyboard windows \
  --without virtualization \
  --vm \
  2>&1 | tee ~/blueprint-gaming-install.log
```

When the restore safety prompt appears, verify the printed target says KVM/QEMU VM and then type `RESTORE`.

Before reboot, require:

- main CachyOS PARTUUID gate did not trigger because this is a KVM guest;
- a Blueprint recovery checkpoint was created and recorded;
- profile state = `gaming`;
- features include mandatory `tvcast` and do not include virtualization;
- final installer validation reports `RESULT: PASS` / `Validation: PASS` or any difference is explained and fixed before proceeding.

Then reboot and run:

```bash
cd ~/devillionner-os
test "$(git rev-parse HEAD)" = "$(cat ~/blueprint-tested-commit.txt)"
bash scripts/check 2>&1 | tee ~/blueprint-gaming-postreboot-check.log
```

Gaming is not complete until the post-reboot aggregate reports `RESULT: PASS`.

## Work

Start from a separate fresh baseline guest:

```bash
git clone https://github.com/devillionner/devillionner-os.git ~/devillionner-os
cd ~/devillionner-os
git rev-parse HEAD | tee ~/blueprint-tested-commit.txt

bash scripts/install \
  --profile work \
  --keyboard windows \
  --without virtualization \
  --vm \
  2>&1 | tee ~/blueprint-work-install.log
```

Type `RESTORE` only after confirming the target is the KVM guest.

After the installer finishes, reboot and run:

```bash
cd ~/devillionner-os
test "$(git rev-parse HEAD)" = "$(cat ~/blueprint-tested-commit.txt)"
bash scripts/check 2>&1 | tee ~/blueprint-work-postreboot-check.log
```

Work is not complete until the post-reboot aggregate reports `RESULT: PASS`.

Spotify may legitimately warn that a first login is still required; that warning does not replace the structural Spotify checks. Do not sign in just to make the clean-install test pass.

## Laboratory

Start from another fresh baseline guest. This profile must test its **default virtualization feature**, so do not pass `--without virtualization`:

```bash
git clone https://github.com/devillionner/devillionner-os.git ~/devillionner-os
cd ~/devillionner-os
git rev-parse HEAD | tee ~/blueprint-tested-commit.txt

bash scripts/install \
  --profile laboratory \
  --keyboard windows \
  --with virtualization \
  --vm \
  2>&1 | tee ~/blueprint-laboratory-install.log
```

The outer guest may not expose nested `/dev/kvm`. That is acceptable only if Blueprint reports the limitation honestly instead of pretending nested acceleration is available. The package/service/configuration contract must still be reviewed.

After reboot:

```bash
cd ~/devillionner-os
test "$(git rev-parse HEAD)" = "$(cat ~/blueprint-tested-commit.txt)"
bash scripts/check 2>&1 | tee ~/blueprint-laboratory-postreboot-check.log
```

Laboratory is not complete until the aggregate result and virtualization-specific output are understood. If nested KVM is unavailable, record that separately; it does **not** satisfy the later physical-host `/dev/kvm` validation item.

## Per-profile visual sanity check

After the post-reboot aggregate passes, do a short manual sanity pass without changing configuration:

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
7. require `qs --version` and `bash scripts/check-quickshell` to pass afterward.

If the chosen update does not actually create an ABI mismatch, record the test as inconclusive rather than marking the rebuild path validated.

## Passing the KVM gate

The KVM milestone is complete only when all of these are true:

- Gaming: fresh install + reboot + aggregate PASS on one pinned Blueprint revision;
- Work: fresh install + reboot + aggregate PASS on one pinned Blueprint revision;
- Laboratory: fresh install + reboot + aggregate PASS on one pinned Blueprint revision, with virtualization state understood;
- no restore safety gate was weakened to obtain a pass;
- each install created a usable-looking recovery-point record;
- all unexplained WARN/FAIL output has been resolved or documented as an intentional environment limitation.

Only then move to the reserved physical Blueprint partition. Do not use successful existing-host migration checks as a substitute for this gate.
