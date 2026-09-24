# Blueprint package ownership and profile switching

The Blueprint treats `common + profile + enabled features` as the desired package state.

## Ownership boundary

Only packages explicitly listed in Blueprint manifests are considered Blueprint-managed. The reconciler records that explicit ownership under:

```text
~/.config/devillionner-os/managed-packages/
├── repo.txt
├── aur.txt
└── schema
```

Dependencies are deliberately not recorded as owned packages. Software installed manually by the user is therefore outside the normal Blueprint ownership boundary and is never removed merely because it is absent from a profile manifest.

There is one deliberately narrow system-role exception for the visible desktop layer. The reconciler removes `network-manager-applet` and `nm-connection-editor` because Caelestia is the canonical NetworkManager UI, and also removes the pure CachyOS desktop extras `cachyos-hello`, `cachyos-packageinstaller` and `cachyos-wallpapers`. These removals apply even when the packages came from the base image rather than an older Blueprint revision. The reconciler first verifies that none of them appears in the desired target set, uses normal dependency-aware removal, and aborts instead of forcing through a conflict. CachyOS kernels, repositories, mirrors, hooks, performance settings and recovery tooling are not part of this exception.

## Profile switching

Running the installer for another profile performs a state transition rather than layering the new profile forever on top of the old one.

For example, a clone-less install can switch a managed Work VM to Gaming while keeping the same ownership rules:

```bash
curl -fsSL https://raw.githubusercontent.com/devillionner/devillionner-os/main/bootstrap \
  | bash -s -- --profile gaming --keyboard windows --without virtualization --vm
```

It will:

1. calculate the desired `common + gaming + tvcast` package set;
2. remove the explicit Caelestia/network-UI conflicts and pure CachyOS desktop extras if present, while preserving the technical CachyOS base;
3. compare the result with the previous Blueprint-managed package set;
4. remove only obsolete Blueprint-managed packages that are no longer part of the target;
5. retain packages that another installed package still requires;
6. install/update the new target packages;
7. record the new ownership set only after package reconciliation succeeds;
8. continue with dotfiles, profile configuration and validation.

The same mechanism applies independently to Gaming, Work, Laboratory/Dev and University/Uni. University has its own ownership identity even while its current profile-specific manifests are intentionally minimal. Reusable features such as `tvcast` and `virtualization` are included in the desired state when enabled.

## Older Blueprint installs

Installs created before managed-package state existed are bootstrapped from the stored profile/features plus `manifests/legacy-managed-packages.txt`. That legacy list contains only packages known to have been explicitly managed by earlier Blueprint revisions.

## AUR dependency-layout migrations

Normal package-manager upgrades are always attempted first. If the desired AUR transaction fails because an already-installed Blueprint-managed AUR package blocks its own new dependency layout, the reconciler can temporarily remove only affected managed packages that `paru` reports as upgradeable, then immediately reinstall the complete desired AUR target.

This replaces package-specific migration code such as the Caelestia 2.3 → 2.4 transition with a general managed-package recovery path.

## Safety

The reconciler never performs a blanket cleanup of foreign or explicitly installed packages. Ordinary removal is restricted to the previous Blueprint ownership set; the documented Caelestia-first desktop conflicts are the only current base-image role exceptions. Their removal uses normal dependency checks and aborts on failure. Ordinary obsolete-package cleanup still avoids forced removal; packages with active reverse dependencies are retained with a warning.
