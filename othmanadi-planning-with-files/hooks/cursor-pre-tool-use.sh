#!/bin/bash
# Source: .cursor/hooks/pre-tool-use.sh @ master
# planning-with-files: Pre-tool-use hook for Cursor
# Reads the first 30 lines of task_plan.md to keep goals in context.
# Returns {"decision": "allow"} — this hook never blocks tools.
#
# COST: ~30 lines (~600-1500 tokens) BEFORE EVERY Write/Edit/Shell/Read.
# Multiply by tool calls per turn (often 5-20). 3k-30k tokens per turn.
# Second offender after userPromptSubmit. The matcher includes Read which fires very often.

PLAN_FILE="task_plan.md"

if [ -f "$PLAN_FILE" ]; then
    # Log plan context to stderr (visible in Cursor's hook logs)
    head -30 "$PLAN_FILE" >&2
fi

echo '{"decision": "allow"}'
exit 0
