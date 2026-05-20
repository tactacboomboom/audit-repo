#!/usr/bin/env python3
"""
Source: scripts/session-catchup.py @ master (heavily abridged archive copy)
Full file is ~350 lines. See canonical repo for complete logic.

Behavior:
- Detects IDE (claude-code via ~/.claude/projects/*.jsonl OR opencode via ~/.local/share/opencode/opencode.db)
- For claude-code: scans previous sessions' jsonl, finds the last Write/Edit on task_plan.md|findings.md|progress.md,
  collects all conversation AFTER that point across all sessions until current, prints up to 100 messages
- For opencode: same idea against the SQLite "part" table (json_extract on data.tool == write|edit|patch)
- Outputs a "SESSION CATCHUP DETECTED" report with USER/CLAUDE messages and Tool summaries

COST: When invoked from SessionStart hook, can inject up to ~100 lines of "unsynced context"
into the first turn — anywhere from 2k to 8k tokens. Expensive but only fires ONCE per session.
"""

# See https://raw.githubusercontent.com/OthmanAdi/planning-with-files/master/scripts/session-catchup.py
# for the full implementation including:
#   - detect_ide()
#   - get_project_dir_claude() — converts /path/to/project to ~/.claude/projects/-path-to-project
#   - get_sessions_sorted() — newest first by mtime
#   - scan_for_planning_update() — returns (line_num, filename) of last Write/Edit on planning files
#   - extract_messages_from_session(after_line=-1) — collects user+assistant messages
#   - opencode_catchup() — SQLite variant
#   - main() — orchestrates detection -> scan -> extract -> print

if __name__ == '__main__':
    print("[planning-with-files] session-catchup.py archive stub — see canonical source.")
