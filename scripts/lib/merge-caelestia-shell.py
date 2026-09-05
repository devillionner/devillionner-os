#!/usr/bin/env python3
"""Merge Blueprint-owned Caelestia shell settings without replacing user config."""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


def deep_merge(current: dict[str, Any], managed: dict[str, Any]) -> dict[str, Any]:
    """Overlay managed values recursively while preserving unrelated keys."""
    result = deepcopy(current)
    for key, value in managed.items():
        existing = result.get(key)
        if isinstance(existing, dict) and isinstance(value, dict):
            result[key] = deep_merge(existing, value)
        else:
            result[key] = deepcopy(value)
    return result


def read_json_object(path: Path, *, missing_ok: bool) -> dict[str, Any]:
    if not path.exists():
        if missing_ok:
            return {}
        raise ValueError(f"missing JSON file: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON in {path} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    except OSError as exc:
        raise OSError(f"could not read {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return data


def merge_file(canonical_path: Path, destination: Path) -> None:
    managed = read_json_object(canonical_path, missing_ok=False)

    if destination.is_dir() and not destination.is_symlink():
        raise ValueError(f"expected a file at {destination}, found a directory")

    # Refuse to overwrite malformed user config. This is intentionally strict:
    # a typo should be repaired or restored from backup, not silently discarded.
    current = read_json_object(destination, missing_ok=True)
    merged = deep_merge(current, managed)
    rendered = json.dumps(merged, indent=4, ensure_ascii=False) + "\n"

    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        # write_text follows an existing symlink, preserving the user's config
        # ownership model instead of replacing the link itself.
        destination.write_text(rendered, encoding="utf-8")
    except OSError as exc:
        raise OSError(f"could not write {destination}: {exc}") from exc


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "usage: merge-caelestia-shell.py CANONICAL_SHELL_JSON DESTINATION",
            file=sys.stderr,
        )
        return 2

    try:
        merge_file(Path(argv[1]), Path(argv[2]))
    except (OSError, ValueError) as exc:
        print(f"merge-caelestia-shell: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
