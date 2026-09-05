# Quickshell ABI recovery

Caelestia depends on `quickshell-git`, which is a compiled Qt application. A Qt private-ABI update can leave an already-installed Quickshell package present in Pacman while its binaries are no longer compatible with the current Qt libraries.

## Blueprint policy

`rebuild-detector` is a common package in all three profiles. During package reconciliation the Blueprint treats Quickshell as needing a rebuild when any of these conditions is true:

- `quickshell-git` is not installed;
- `qs` is missing or `qs --version` fails;
- `checkrebuild` reports `quickshell-git` as linked against stale libraries.

When a rebuild is required, Blueprint builds the current AUR `quickshell-git` package directly with `makepkg -si --noconfirm`.

The rebuild deliberately does **not** use `--needed`. A Qt ABI break can require reinstalling the exact same VCS package version; `--needed` would allow that required same-version reinstall to be skipped.

After rebuilding, Blueprint requires all of the following before continuing:

- `quickshell-git` is installed;
- `qs --version` succeeds;
- `checkrebuild` no longer reports `quickshell-git`.

If any post-rebuild check still fails, restore stops instead of reporting the desktop as healthy.

## Validation

Run the installed-state check with:

```bash
bash scripts/check-quickshell
```

It checks the package, the `qs` executable/runtime and rebuild-detector ABI state.

Repository CI separately runs:

```bash
bash scripts/check-quickshell-rebuild-source
```

That source-level contract prevents future edits from accidentally restoring `--needed`, dropping `checkrebuild`, or removing Quickshell validation from the restore path.

## Remaining runtime test

The recovery path is implemented and source-validated, but it still needs to be exercised after a real Qt upgrade in a clean KVM Blueprint test machine. That test remains separate from repository CI because GitHub Actions does not reproduce the CachyOS/AUR/Qt runtime environment.
