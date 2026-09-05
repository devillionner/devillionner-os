#!/usr/bin/env python3
"""Safely own only Caelestia's fileExplorer override.

The Blueprint must not replace an entire user hypr-vars.lua just to change one
application target. This helper preserves unrelated entries/comments and writes
through an existing symlink when Caelestia or the user's dotfile manager owns it.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DESIRED = "/usr/local/bin/devos-dolphin"
STRING_ASSIGNMENT = re.compile(
    r'(?m)^(?P<indent>\s*)fileExplorer\s*=\s*["\'][^"\']*["\']'
    # Caelestia may compact the final table entry so the closing brace lives on
    # the same line: fileExplorer = "dolphin",}. Treat that as a normal string
    # assignment while still refusing function/expression values we do not know
    # how to rewrite safely.
    r'(?P<tail>\s*,?\s*\}?\s*(?:--.*)?)$'
)
ANY_ASSIGNMENT = re.compile(r"(?m)^\s*fileExplorer\s*=")
RETURN_TABLE = re.compile(r"(?m)^\s*return\s*\{\s*$")


def update_text(current: str, desired: str = DESIRED) -> str:
    """Return Lua text with exactly the supported fileExplorer value updated."""
    match = STRING_ASSIGNMENT.search(current)
    if match:
        indent = match.group("indent")
        tail = match.group("tail")
        # Preserve the exact supported suffix (comma, compact closing brace and
        # comment) instead of reformatting the surrounding user/Caelestia Lua.
        replacement = f'{indent}fileExplorer = "{desired}"{tail}'
        return current[: match.start()] + replacement + current[match.end() :]

    if ANY_ASSIGNMENT.search(current):
        raise ValueError(
            "existing fileExplorer uses an unfamiliar value format; refusing to add a duplicate"
        )

    table = RETURN_TABLE.search(current)
    if not table:
        raise ValueError("expected a Lua 'return {' table")

    insert_at = table.end()
    return current[:insert_at] + f'\n    fileExplorer = "{desired}",' + current[insert_at:]


def update_file(canonical_path: Path, destination: Path) -> None:
    canonical = canonical_path.read_text(encoding="utf-8")

    if destination.is_dir() and not destination.is_symlink():
        raise ValueError(f"expected a file at {destination}, found a directory")

    try:
        current = destination.read_text(encoding="utf-8")
    except FileNotFoundError:
        current = canonical
    except OSError as exc:
        raise OSError(f"could not read {destination}: {exc}") from exc

    if not current.strip():
        current = canonical

    updated = update_text(current)
    if updated == current and destination.exists():
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        # Path.write_text follows a symlink instead of replacing it, which is
        # exactly what we want for Caelestia/user-managed config links.
        destination.write_text(updated, encoding="utf-8")
    except OSError as exc:
        raise OSError(f"could not update {destination}: {exc}") from exc


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "usage: set-caelestia-file-explorer.py CANONICAL_HYPR_VARS DESTINATION",
            file=sys.stderr,
        )
        return 2

    try:
        update_file(Path(argv[1]), Path(argv[2]))
    except (OSError, ValueError) as exc:
        print(f"set-caelestia-file-explorer: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
