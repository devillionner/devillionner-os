# Dolphin file manager

Dolphin is the single Blueprint file manager for Gaming, Work and Laboratory.

The configuration was captured from the tested host and deliberately reduced to reproducible settings instead of copying machine-specific runtime state.

## Restored behavior

- `Super+E` opens Dolphin.
- Dolphin is the default handler for directories.
- Colloid-Dark is the active Qt/KDE icon theme.
- Folder tint remains adaptive to the Caelestia-generated palette when the wallpaper/theme changes.
- Dolphin uses double-click activation (`SingleClick=false`).
- Places icons use a fixed 16 px size.
- The menu bar is hidden.
- The Information panel is enabled on the first Blueprint configuration through Dolphin's own D-Bus action API.
- File thumbnails/previews are enabled globally and small previews may be enlarged.
- JPEG, PNG and WEBP open in Swappy, matching the tested host.
- Delete confirmation remains enabled.

Caelestia's CLI theme config is pinned to `Colloid-Dark` so a wallpaper/theme refresh does not silently restore the old Papirus icon theme.

## Preview stack

The Blueprint treats previews as part of the file-manager experience rather than an accidental dependency of another application. The common profile therefore installs:

- `ffmpegthumbs` for video thumbnails;
- `kdegraphics-thumbnailers` for additional graphics/document thumbnailers;
- `kimageformats` for KDE/Qt 6 image formats such as HEIF/AVIF when their codec libraries are available;
- `qt6-imageformats` for additional Qt image formats such as TIFF/TGA/JP2/WebP support.

Dolphin's current upstream default for `PreviewsShown` is `true`, but Blueprint writes a global view property explicitly so an old per-machine state cannot silently disable previews after restore. `GlobalViewProps=true` and `EnlargeSmallPreviews=true` are also explicit Blueprint settings.

The global view file lives under `~/.local/share/dolphin/view_properties/global/.directory`, matching Dolphin's current `QStandardPaths::AppDataLocation/view_properties/global` storage model. The Information panel remains a separate main-window state and is initialized through Dolphin's own action API.

## Dolphin-only Qt style override

Darkly remains the global Qt widget style. Current Dolphin item highlight/focus rendering can produce an over-bright selected+hover state with Darkly, while the same palette behaves correctly through qtengine's widget style.

The Blueprint therefore installs `/usr/local/bin/devos-dolphin`, which sets `QT_QPA_PLATFORMTHEME=qtengine` and `QT_STYLE_OVERRIDE=qtengine` only for Dolphin before executing `/usr/bin/dolphin`.

`Super+E` targets this wrapper. A user-level override of `org.kde.dolphin.desktop` preserves Dolphin's upstream desktop metadata/actions but rewrites its `Exec=` entries to the wrapper and disables D-Bus activation so app-menu and default-directory launches use the same fixed path.

`configure-dolphin` owns only the `fileExplorer` key in `~/.config/caelestia/hypr-vars.lua`. It preserves unrelated Caelestia/user overrides and follows an existing symlink instead of deleting the whole override file. Validation requires exactly one `fileExplorer` entry and that entry must target the Blueprint wrapper.

The restore rsync deliberately excludes `caelestia/hypr-vars.lua` and `caelestia/cli.json`. Those files are merge-managed by the Dolphin/Spotify configurators, so an existing custom override survives a full restore instead of being overwritten before the safe merge runs.

No fixed selection colour is written. The adaptive Caelestia palette remains the source of colours, so changing wallpaper can continue to retint Colloid folders normally.

Upstream context: Darkly issue #316 documents the Dolphin/QStyle focus/highlight compatibility problem.

## Minimal Colloid install

The Blueprint does **not** install `colloid-icon-theme-git`, because that package deploys the complete accent/colour-scheme matrix. Instead `scripts/configure-colloid-icons` checks out a pinned upstream Colloid revision and runs the upstream installer with its default theme/scheme selection.

Only the three linked standard variants are kept:

- `Colloid`
- `Colloid-Light`
- `Colloid-Dark`

`Colloid-Dark` is active. The normal Colloid installer mode is retained (no `--notint`), because disabling tinting would freeze folder colour instead of following Caelestia's adaptive palette.

`Colloid` and `Colloid-Dark` intentionally reuse assets from `Colloid-Light`; deleting Light would leave broken links. Existing Blueprint machines that previously installed the full AUR package are migrated away from it when the package has no reverse dependencies.

The pinned upstream revision is `ceac6608ecd0e40025cbc2ebbd32bf0e0f4ebc6a`.

## Intentionally not copied

`user-places.xbel` from the source host contains physical NVMe UDisks IDs, filesystem UUIDs and an absolute username path. Those values are hardware/user-specific and are not committed to the common Blueprint.

Dolphin creates Places for the current machine normally. Exact physical-drive hiding/renaming should be hardware-aware rather than hard-coded from one laptop.

Likewise, `dolphinstaterc` contains screen-size keys and a serialized Qt main-window state. The Blueprint recreates the Information-panel state using Dolphin itself instead of shipping the 1920x1200 binary state blob.

## Validation

`scripts/check-dolphin` verifies the preview backend packages, global preview state, exact three-theme Colloid set, active Colloid-Dark theme, Dolphin-only qtengine wrapper, launcher/default-directory routing, double-click behavior, Swappy image handlers and the `Super+E` target. A missing first-run Information-panel marker is a warning rather than a fatal error when restore was performed without a user D-Bus session.
