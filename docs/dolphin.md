# Dolphin file manager

Dolphin is the single Blueprint file manager for Gaming, Work and Laboratory.

The configuration was captured from the tested host and deliberately reduced to reproducible settings instead of copying machine-specific runtime state.

## Restored behavior

- `Super+E` opens Dolphin.
- Dolphin is the default handler for directories.
- Colloid-Dark is the Qt/KDE icon theme.
- Dolphin uses double-click activation (`SingleClick=false`).
- Places icons use a fixed 16 px size.
- The menu bar is hidden.
- The Information panel is enabled on the first Blueprint configuration through Dolphin's own D-Bus action API.
- JPEG, PNG and WEBP open in Swappy, matching the tested host.
- Delete confirmation remains enabled.

Caelestia's CLI theme config is pinned to `Colloid-Dark` so a wallpaper/theme refresh does not silently restore the old Papirus icon theme.

## Minimal Colloid install

The Blueprint does **not** install `colloid-icon-theme-git`, because that package deploys the complete accent/colour-scheme matrix. Instead `scripts/configure-colloid-icons` checks out a pinned upstream Colloid revision and runs the upstream installer with its default theme/scheme selection.

Only the three linked standard variants are kept:

- `Colloid`
- `Colloid-Light`
- `Colloid-Dark`

This is important because `Colloid` and `Colloid-Dark` intentionally reuse assets from `Colloid-Light`; deleting Light would leave broken links. Existing Blueprint machines that previously installed the full AUR package are migrated away from it when the package has no reverse dependencies.

The pinned upstream revision is `ceac6608ecd0e40025cbc2ebbd32bf0e0f4ebc6a`.

## Intentionally not copied

`user-places.xbel` from the source host contains physical NVMe UDisks IDs, filesystem UUIDs and an absolute username path. Those values are hardware/user-specific and are not committed to the common Blueprint.

Dolphin creates Places for the current machine normally. Exact physical-drive hiding/renaming should be hardware-aware rather than hard-coded from one laptop.

Likewise, `dolphinstaterc` contains screen-size keys and a serialized Qt main-window state. The Blueprint recreates the Information-panel state using Dolphin itself instead of shipping the 1920x1200 binary state blob.

## Validation

`scripts/check-dolphin` verifies the installed Dolphin/Swappy commands, the exact three-theme Colloid set, double-click behavior, default directory/image handlers and the `Super+E` application target. A missing first-run Information-panel marker is a warning rather than a fatal error when restore was performed without a user D-Bus session.
