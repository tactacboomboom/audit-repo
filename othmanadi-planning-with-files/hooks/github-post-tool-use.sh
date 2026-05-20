#!/bin/bash
# Source: .github/hooks/scripts/post-tool-use.sh @ master
# COST: ~40 tokens of static reminder text after EVERY tool use (no matcher).
# Cheap per call but multiplied by tool count. CHEAP overall but spammy.

INPUT=$(cat)
echo '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"[planning-with-files] Update progress.md with what you just did. If a phase is now complete, update task_plan.md status."}}'
exit 0
