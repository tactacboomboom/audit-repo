#!/bin/bash
# Source: .cursor/hooks/post-tool-use.sh @ master
# COST: ~30 tokens of static reminder text, fires only after Write|Edit. CHEAP.

if [ -f task_plan.md ]; then
    echo "[planning-with-files] Update progress.md with what you just did. If a phase is now complete, update task_plan.md status."
fi
exit 0
