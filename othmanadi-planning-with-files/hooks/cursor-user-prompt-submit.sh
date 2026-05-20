#!/bin/bash
# Source: .cursor/hooks/user-prompt-submit.sh @ master
# planning-with-files: User prompt submit hook for Cursor
# Injects plan context on every user message.
# Critical for session recovery after /clear — dumps actual content, not just advice.
#
# COST ANALYSIS: Fires on EVERY user prompt. Dumps up to 50 lines of task_plan.md
# + 20 lines of progress.md = ~70 lines (~1.5-3k tokens) per turn.
# Over a 50-turn session that is 75k-150k injected tokens of pure repetition.
# THIS IS THE PRIMARY OFFENDER FOR THE "TOO HEAVY" COMPLAINT.

if [ -f task_plan.md ]; then
    echo "[planning-with-files] ACTIVE PLAN — current state:"
    head -50 task_plan.md
    echo ""
    echo "=== recent progress ==="
    tail -20 progress.md 2>/dev/null
    echo ""
    echo "[planning-with-files] Read findings.md for research context. Continue from the current phase."
fi
exit 0
