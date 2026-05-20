#!/bin/sh
# Source: scripts/resolve-plan-dir.sh @ master
# Resolution order:
#   1. $PLAN_ID env var      → ./.planning/$PLAN_ID/
#   2. ./.planning/.active_plan content → matching dir
#   3. Newest ./.planning/<dir>/ by mtime that contains task_plan.md
#   4. Empty stdout (caller falls back to legacy ./task_plan.md)
# Always exits 0.

set -u
PLAN_ROOT="${1:-${PWD}/.planning}"
ACTIVE_FILE="${PLAN_ROOT}/.active_plan"

resolve_from_env() {
    plan_id="${PLAN_ID:-}"
    [ -z "${plan_id}" ] && return 1
    candidate="${PLAN_ROOT}/${plan_id}"
    [ -d "${candidate}" ] && { printf "%s\n" "${candidate}"; return 0; }
    return 1
}

resolve_from_active_file() {
    [ -f "${ACTIVE_FILE}" ] || return 1
    plan_id="$(tr -d '\r\n' < "${ACTIVE_FILE}")"
    [ -z "${plan_id}" ] && return 1
    candidate="${PLAN_ROOT}/${plan_id}"
    [ -d "${candidate}" ] && { printf "%s\n" "${candidate}"; return 0; }
    return 1
}

resolve_latest_dir() {
    [ -d "${PLAN_ROOT}" ] || return 1
    latest=""; latest_mtime=0
    for entry in "${PLAN_ROOT}"/*/; do
        [ -d "${entry}" ] || continue
        clean="${entry%/}"
        case "$(basename "${clean}")" in .*) continue ;; esac
        [ -f "${clean}/task_plan.md" ] || continue
        mtime="$(date -r "${clean}" +%s 2>/dev/null || stat -c '%Y' "${clean}" 2>/dev/null || echo 0)"
        if [ "${mtime}" -gt "${latest_mtime}" ] 2>/dev/null; then
            latest_mtime="${mtime}"; latest="${clean}"
        fi
    done
    [ -n "${latest}" ] && { printf "%s\n" "${latest}"; return 0; }
    return 1
}

if resolve_from_env; then exit 0; fi
if resolve_from_active_file; then exit 0; fi
if resolve_latest_dir; then exit 0; fi
exit 0
