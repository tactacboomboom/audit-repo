#!/usr/bin/env bash
# Source: scripts/init-session.sh @ master (canonical version)
# Supports two modes:
#   Legacy:    ./init-session.sh                    -> ./task_plan.md, ./findings.md, ./progress.md
#   Slug mode: ./init-session.sh "My Project"      -> .planning/<date>-my-project/{task_plan,findings,progress}.md
# Slug mode also writes .planning/.active_plan to pin the active plan id.

set -e

TEMPLATE="default"
PROJECT_NAME=""
USE_PLAN_DIR=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --template|-t) TEMPLATE="$2"; shift 2 ;;
        --plan-dir)    USE_PLAN_DIR=1; shift ;;
        *)             [ -z "$PROJECT_NAME" ] && PROJECT_NAME="$1" || PROJECT_NAME="$PROJECT_NAME $1"; shift ;;
    esac
done

DATE=$(date +%Y-%m-%d)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATE_DIR="$SKILL_ROOT/templates"

SLUG_MODE=0
if [ -n "$PROJECT_NAME" ] || [ "$USE_PLAN_DIR" -eq 1 ]; then SLUG_MODE=1; fi

slugify() {
    printf '%s' "$1" | tr '[:upper:]' '[:lower:]' \
        | sed -e 's/[^a-z0-9]/-/g' -e 's/-\{2,\}/-/g' -e 's/^-//' -e 's/-$//' | cut -c1-40
}

# (template writers and slug-mode dir creation omitted in this archived copy;
# see canonical source for full body — ~250 lines.)
echo "Initializing planning files for: ${PROJECT_NAME:-project} (template: $TEMPLATE)"
echo "See canonical source: scripts/init-session.sh in OthmanAdi/planning-with-files @ master"
