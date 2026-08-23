#!/usr/bin/env bash

bp_repo_root() {
    cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd
}

bp_info() { printf "\n==> %s\n" "$*"; }
bp_ok()   { printf "    [OK] %s\n" "$*"; }
bp_warn() { printf "    [WARN] %s\n" "$*" >&2; }
bp_die()  { printf "\n    [ERROR] %s\n" "$*" >&2; exit 1; }

bp_strip_manifest() {
    local file="$1"
    [[ -f "$file" ]] || return 0
    sed -E 's/[[:space:]]+#.*$//' "$file" \
        | sed -E '/^[[:space:]]*(#|$)/d' \
        | awk '{$1=$1; print}'
}

bp_normalize_profile() {
    case "${1:-}" in
        gaming|game) printf '%s\n' gaming ;;
        work|office) printf '%s\n' work ;;
        laboratory|lab|dev|dev-laboratory) printf '%s\n' laboratory ;;
        *) return 1 ;;
    esac
}

bp_is_vm() {
    case "$(systemd-detect-virt 2>/dev/null || true)" in
        kvm|qemu) return 0 ;;
        *) return 1 ;;
    esac
}

bp_product_name() {
    cat /sys/class/dmi/id/product_name 2>/dev/null || true
}

bp_is_zenbook() {
    [[ "$(bp_product_name)" == *"UX3405CA"* ]]
}

bp_root_partuuid() {
    local src dev
    src="$(findmnt -no SOURCE /)"
    dev="${src%%[*}"
    dev="$(readlink -f "$dev")"
    lsblk -no PARTUUID "$dev" 2>/dev/null | head -n1 | xargs
}

bp_state_dir() {
    printf '%s\n' "${XDG_STATE_HOME:-$HOME/.local/state}/devillionner-os"
}

bp_config_dir() {
    printf '%s\n' "${XDG_CONFIG_HOME:-$HOME/.config}/devillionner-os"
}
