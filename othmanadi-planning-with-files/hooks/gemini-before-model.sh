#!/bin/bash
# Source: .gemini/hooks/before-model.sh @ master
# Gemini-only BeforeModel event — injects on EVERY LLM call.
# Designed to be light: only the "current phase" line, not the whole plan.
# COST: ~30 tokens per LLM call. Cheap and well-designed.

INPUT=$(cat)
PLAN_FILE="task_plan.md"

if [ ! -f "$PLAN_FILE" ]; then
    echo '{}'
    exit 0
fi

CURRENT_PHASE=$(grep -m1 "^## Current Phase" "$PLAN_FILE" 2>/dev/null || grep -m1 "in_progress" "$PLAN_FILE" 2>/dev/null || echo "")

if [ -n "$CURRENT_PHASE" ]; then
    PYTHON=$(command -v python3 || command -v python)
    ESCAPED=$($PYTHON -c "import sys,json; print(json.dumps(sys.stdin.read(), ensure_ascii=False))" <<< "[planning-with-files] Current: $CURRENT_PHASE" 2>/dev/null || echo "\"\"")
    echo "{\"additionalContext\":$ESCAPED}"
else
    echo '{}'
fi
exit 0
