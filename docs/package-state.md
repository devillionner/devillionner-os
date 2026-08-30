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

Dependencies are deliberately not recorded as owned packages. Software installed manually by the user is therefore outside the Blueprint ownership boundary and is never removed merely because it is absent from a profile manifest.

## Profile switching

Running the installer for another profile performs a state transition rather than layering the new profile forever on top of the old one.

For example:

```bash
bash scripts/install --profile gaming --keyboard windows --without virtualization --vm
```

on a previously managed Work VM will:

1. calculate the desired `common + gaming + tvcast` package set;
2. compare it with the previous Blueprint-managed package set;
3. remove only obsolete Blueprint-managed packages that are no longer part of the target;
4. retain packages that another installed package still requires;
5. install/update the new target packages;
6. record the new ownership set only after package reconciliation succeeds;
7. continue with dotfiles, profile configuration and validation.

The same mechanism applies to Gaming, Work and Laboratory, with reusable features such as `tvcast` and `virtualization` included in the desired state when enabled.

## Older Blueprint installs

Installs created before managed-package state existed are bootstrapped from the stored profile/features plus `manifests/legacy-managed-packages.txt`. That legacy list contains only packages known to have been explicitly managed by earlier Blueprint revisions.

## AUR dependency-layout migrations

Normal package-manager upgrades are always attempted first. If the desired AUR transaction fails because an already-installed Blueprint-managed AUR package blocks its own new dependency layout, the reconciler can temporarily remove only affected managed packages that `paru` reports as upgradeable, then immediately reinstall the complete desired AUR target.

This replaces package-specific migration code such as the Caelestia 2.3 → 2.4 transition with a general managed-package recovery path.

## Safety

The reconciler never performs a blanket cleanup of foreign or explicitly installed packages. Removal is restricted to the previous Blueprint ownership set. It also avoids forced removal for ordinary obsolete-package cleanup; packages with active reverse dependencies are retained with a warning.
