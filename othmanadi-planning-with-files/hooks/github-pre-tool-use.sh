#!/bin/bash
# Source: .github/hooks/scripts/pre-tool-use.sh @ master
# COST: head -30 of task_plan.md (~600-1500 tokens) BEFORE EVERY tool call.
# No matcher — fires for ALL tools. This is the heaviest steady-state cost
# because every tool use (read, grep, glob, write...) pays this tax.

INPUT=$(cat)
PLAN_FILE="task_plan.md"

if [ ! -f "$PLAN_FILE" ]; then
    echo '{}'
    exit 0
fi

CONTEXT=$(head -30 "$PLAN_FILE" 2>/dev/null || echo "")

if [ -z "$CONTEXT" ]; then
    echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}'
    exit 0
fi

PYTHON=""
for _p in /usr/bin/python3 /usr/local/bin/python3 /opt/homebrew/bin/python3; do
    [ -x "$_p" ] && { PYTHON="$_p"; break; }
done
[ -z "$PYTHON" ] && PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
ESCAPED=$(echo "$CONTEXT" | $PYTHON -c "import sys,json; print(json.dumps(sys.stdin.read(), ensure_ascii=False))" 2>/dev/null || echo "\"\"")

echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"additionalContext\":$ESCAPED}}"
exit 0
