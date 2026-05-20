#!/bin/bash
# Source: .github/hooks/scripts/session-start.sh @ master
# COST: HIGH on a session with an existing plan. Calls session-catchup.py which
# scans Claude's .claude/projects/*.jsonl history and may inject up to 100 lines
# of "unsynced context" plus tool summaries. Can easily be 3-10k tokens at startup.
# When no plan exists: injects the FULL SKILL.md (~2k tokens). Either way: expensive at SessionStart.

INPUT=$(cat)

PLAN_FILE="task_plan.md"
SKILL_DIR=".github/skills/planning-with-files"
PYTHON=""
for _p in /usr/bin/python3 /usr/local/bin/python3 /opt/homebrew/bin/python3; do
    [ -x "$_p" ] && { PYTHON="$_p"; break; }
done
[ -z "$PYTHON" ] && PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)

if [ -f "$PLAN_FILE" ]; then
    CATCHUP=""
    if [ -n "$PYTHON" ] && [ -f "$SKILL_DIR/scripts/session-catchup.py" ]; then
        CATCHUP=$($PYTHON "$SKILL_DIR/scripts/session-catchup.py" "$(pwd)" 2>/dev/null | head -100)
    fi

    if [ -n "$CATCHUP" ]; then
        CONTEXT="[planning-with-files] Previous session context (truncated to 100 lines):
$CATCHUP"
    else
        CONTEXT=$(head -5 "$PLAN_FILE" 2>/dev/null || echo "")
    fi
else
    if [ -f "$SKILL_DIR/SKILL.md" ]; then
        CONTEXT=$(cat "$SKILL_DIR/SKILL.md" 2>/dev/null || echo "")
    fi
fi

if [ -z "$CONTEXT" ]; then
    echo '{}'
    exit 0
fi

ESCAPED=$(echo "$CONTEXT" | $PYTHON -c "import sys,json; print(json.dumps(sys.stdin.read(), ensure_ascii=False))" 2>/dev/null || echo "\"\"")
echo "{\"hookSpecificOutput\":{\"hookEventName\":\"SessionStart\",\"additionalContext\":$ESCAPED}}"
exit 0
