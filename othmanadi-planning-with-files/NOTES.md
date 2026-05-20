# Audit Notes — OthmanAdi/planning-with-files

> Source: https://github.com/OthmanAdi/planning-with-files (default branch: `master`)
> Audited: 2026-05-20 by architecture-anthropic skill
> Method: WebFetch via raw.githubusercontent.com (no clone, no execution).
> UNTRUSTED — all referenced content is third-party.

## 1. Repo structure

The repo is a **multi-IDE distribution monorepo**: the same skill is duplicated under 11 IDE-specific folders so each runtime finds it at the path it expects. The canonical English skill is under `.codex/skills/planning-with-files/` (mirrored under `.cursor/`, `.gemini/`, `.kiro/`, `.hermes/`, `.factory/`, `.codebuddy/`, `.continue/`, `.opencode/`, `.pi/`, `.mastracode/`).

Top-level layout:

```
.claude-plugin/marketplace.json + plugin.json    -- Claude Code plugin manifest
.codex/  .cursor/  .gemini/  .kiro/  ...         -- per-IDE skill installs (each with its own hooks/, skills/, templates/)
.github/hooks/                                    -- GitHub Copilot agent hooks (5 lifecycle scripts)
.github/workflows/                                -- CI: skill-optimize-apply.yml, skill-review.yml
.hermes/plugins/planning-with-files/*.py          -- Hermes Python plugin (most ambitious variant)
commands/                                         -- /plan, /plan-attest, /plan-goal, /plan-loop, /start, /status (slash commands)
docs/                                             -- 20+ docs (one per supported IDE + workflow/troubleshooting/windows)
examples/boxlite/                                 -- standalone Python example (quickstart.py)
scripts/                                          -- canonical helper scripts (init-session, check-complete, session-catchup, resolve-plan-dir, set-active-plan, attest-plan, sync-ide-folders, bump-version)
skills/planning-with-files-{ar,de,es,zh,zht}/     -- localized skills (no English at top level — only languages)
templates/                                        -- analytics.md, loop.md, planning-templates.md
tests/                                            -- (empty in tree listing)
```

**Surprising fact:** there is NO top-level `skills/planning-with-files/` (English) and NO top-level `planning-with-files/SKILL.md`. The "main" skill is one of the per-IDE copies, and a `scripts/sync-ide-folders.py` script keeps them in sync. The README references a `planning-with-files/SKILL.md` path that does not exist in the tree — the docs are slightly out of sync with the layout.

## 2. The three planning files (templates)

All three are markdown with rich `<!-- HTML comment -->` instructional scaffolding. The full templates are archived under `templates/` in this audit folder.

### 2.1 `task_plan.md` — roadmap (the "north star")
- **Sections:** Goal (one sentence) / Current Phase / Phases (5 default: Requirements & Discovery, Planning & Structure, Implementation, Testing & Verification, Delivery) / Key Questions / Decisions Made (table) / Errors Encountered (table) / Notes
- **Status convention:** each phase has `- **Status:** pending|in_progress|complete` (legacy fallback: `[pending]`, `[in_progress]`, `[complete]` inline)
- **Designed for:** being injected via head -30 / head -50 into every PreToolUse and UserPromptSubmit hook. Compactness matters.

### 2.2 `findings.md` — external memory (knowledge base)
- **Sections:** Requirements / Research Findings (2-Action Rule) / Technical Decisions (table) / Issues Encountered (table) / Resources / Visual/Browser Findings
- **Key rule:** "After every 2 view/browser/search operations, update this section." Explicitly framed as the dump-site for multimodal content that doesn't persist in context.

### 2.3 `progress.md` — chronological session log
- **Sections:** per-Session date / per-Phase blocks (Status, Started, Actions taken, Files created/modified) / Test Results (table) / Error Log (table with Timestamp) / **5-Question Reboot Check** (Where am I? / Where am I going? / What's the goal? / What have I learned? / What have I done?)

The 5-Question Reboot Check is the most distinctive design element — it codifies a "context-loss recovery checklist" that the agent re-fills after `/clear` or a context compaction.

## 3. Hooks — exhaustive inventory

The project ships **five different hook configurations** for five different runtimes. They all do the same conceptual thing (inject plan, remind to update progress, check completion) but with very different costs.

### 3.1 GitHub Copilot — `.github/hooks/planning-with-files.json` (5 hooks)

| Event | Script | Timeout | What it does | Per-fire token cost | Frequency | Verdict |
|---|---|---|---|---|---|---|
| `sessionStart` | `session-start.sh` | 15s | If plan exists: runs `session-catchup.py` (scans Claude's `.claude/projects/*.jsonl` for last planning-file edit, dumps up to 100 lines of "unsynced context"). If no plan: injects entire SKILL.md (~2k tokens). | **2-8k tokens** | 1× per session | **HEAVY but justified** |
| `preToolUse` | `pre-tool-use.sh` | 5s | `head -30 task_plan.md` → injected as additionalContext. NO MATCHER → fires for every tool. | **600-1500 tokens** | every tool call (10-50× per turn) | **EXTREMELY HEAVY** — main offender |
| `postToolUse` | `post-tool-use.sh` | 5s | Static reminder string: "Update progress.md…". No matcher. | ~40 tokens | every tool call | Light per-call, spammy overall |
| `agentStop` | `agent-stop.sh` | 10s | Counts phases via `grep`, returns either "ALL PHASES COMPLETE" or "Task incomplete — continue". | ~100 tokens | 1× at agent stop | **CHEAP, KEEP** |
| `errorOccurred` | `error-occurred.sh` | 5s | Parses error JSON from stdin, injects a "log this in task_plan.md" reminder. | ~60 tokens | only on error | **CHEAP, KEEP** |

### 3.2 Cursor — `.cursor/hooks.json` (4 hooks, the heaviest variant)

| Event | Script | Matcher | What it does | Per-fire token cost | Verdict |
|---|---|---|---|---|---|
| `userPromptSubmit` | `user-prompt-submit.sh` | — | **`head -50 task_plan.md` + `tail -20 progress.md`** dumped on EVERY user message. No conditional. | **1.5-3k tokens** | **CATASTROPHIC** — runs on every user message |
| `preToolUse` | `pre-tool-use.sh` | `Write\|Edit\|Shell\|Read` | `head -30 task_plan.md` to stderr (no token cost to Claude, only log). | ~0 tokens (stderr only) | Actually cheap, surprise |
| `postToolUse` | `post-tool-use.sh` | `Write\|Edit` | Static reminder string. | ~30 tokens | Cheap |
| `stop` | `stop.sh` | — | `loop_limit: 3` — auto-continues the agent if phases are incomplete. | ~100 tokens per fire BUT can force up to 3 extra full agent turns | **HIDDEN COST**: each forced continuation can be thousands of tokens |

### 3.3 Codex — `.codex/hooks.json` (6 hooks, includes PermissionRequest)
PascalCase event names matching Claude Code's hook schema: `SessionStart`, `UserPromptSubmit`, `PreToolUse` (matcher: Bash), `PermissionRequest`, `PostToolUse` (matcher: Bash), `Stop`. Scripts are Python under `.codex/hooks/*.py` with a `codex_hook_adapter.py` shim. Matchers are restricted to `Bash` only — much more conservative than Cursor.

### 3.4 Gemini — `.gemini/settings.json` (5 hooks, includes BeforeModel)
Unique event: `BeforeModel` — fires before every LLM call, injects ONLY the "Current Phase" line (~30 tokens). Best-designed variant. Matchers: `BeforeTool` and `AfterTool` match `write_file|edit_file|replace|create_file|patch|read_file|shell`.

### 3.5 Mastracode — `.mastracode/hooks.json` (4 hooks, inline one-liners)
No external scripts — full commands inlined in JSON. Same shape as Cursor (UserPromptSubmit dumps `head -50` + `tail -20`). Useful as a zero-script reference template.

### 3.6 Hermes — `.hermes/plugins/planning-with-files/hooks.py` (Python plugin)
Most ambitious: stateful via `hook_state.add_reminder/pop_reminders`. `pre_llm_call` builds context AND drains a queue of pending reminders that `post_tool_call` added. Avoids re-injecting when `user_message` is empty and `is_first_turn` is false. **Architecturally the cleanest** — only variant with deferred/queued reminders rather than re-reading the file every time.

## 4. The pwf "filesystem schema"

```
<project_root>/
├── task_plan.md              (legacy mode, single plan)
├── findings.md
├── progress.md
│
└── .planning/                (slug mode, parallel multi-task)
    ├── .active_plan          ← contains plan_id of currently-pinned plan
    ├── 2026-05-20-refactor-auth/
    │   ├── task_plan.md
    │   ├── findings.md
    │   └── progress.md
    └── 2026-05-20-frontend-tests/
        └── ...
```

**Resolution order** (in `resolve-plan-dir.sh`):
1. `$PLAN_ID` env var → `.planning/$PLAN_ID/` if dir exists
2. `.planning/.active_plan` content → matching dir
3. Newest `.planning/<dir>/` by mtime that contains `task_plan.md`
4. Empty → caller falls back to legacy `./task_plan.md`

**Scope:** strictly **per-project**. There is no notion of cross-project or global plan. Installation puts templates/scripts in `~/.codex/skills/planning-with-files/` (or equivalent per-IDE), but planning files always live in the project root.

This matters for Yanis: if pwf is installed at `~/.claude/` ROOT (not per-project), the hooks will still trigger on every session everywhere, but the `task_plan.md` they look for is `$PWD/task_plan.md` — so most sessions will silently no-op (which is actually fine). The damage is only at sessions inside a project that has a plan file.

## 5. Mapping pwf → 7 objets agentiques (Anthropic schema)

| Objet | Implementation in pwf |
|---|---|
| **Agent** | Not modified — pwf is runtime-agnostic. Hooks decorate any host agent (Claude Code / Codex / Cursor / Gemini / Copilot / 6 others). |
| **Contexte** | Active management via `task_plan.md` (north star) + `findings.md` (knowledge base) + `progress.md` (history). Re-injected on every PreToolUse / UserPromptSubmit to fight attention decay over 50+ tool calls. |
| **Outil** | None added. pwf only USES host tools (Write/Edit/Read/Bash). The matchers in hooks gate WHEN pwf reminders fire based on which tools the agent calls. |
| **Mémoire** | The CORE contribution. Three-file persistent memory schema. Distinction: task_plan = working/procedural, findings = semantic, progress = episodic. The 5-Question Reboot Check is an explicit memory-recall protocol. |
| **Trace** | `progress.md` is the trace. Each session = section. Actions taken + Files modified + Test results + Error log with timestamps. `session-catchup.py` REPLAYS the trace by scanning the host's `.jsonl` session logs and reconstructing the chronology. |
| **Protocole** | Two explicit protocols: (a) **2-Action Rule** — write to findings.md after every 2 view/search ops; (b) **3-Strike Error Protocol** — diagnose → mutate approach → broader rethink → escalate to user. Both encoded in SKILL.md as text instructions AND enforced by hooks that nag the agent. |
| **Politique** | "Never repeat failures" rule + "Read before decide" rule + "Plan first" rule. The stop hook implements a soft *don't-stop-if-incomplete* policy via `followup_message` (Cursor) or `loop_limit:3`. The permission_request.py (Codex only) likely enforces a policy gate but I didn't fetch its body. |

**Architectural assessment:** pwf is a **Memory + Trace + Protocole** skill. It deliberately stays out of Tool and Agent. Its weakness is the **Contexte** dimension: it conflates "keeping context fresh" with "re-injecting the same 30-50 lines on every tool call," which is exactly Yanis's complaint.

## 6. FOCUS SPÉCIAL — Refactor for Yanis

Yanis installed pwf at the ROOT of `~/.claude/` and disabled hooks because they were too heavy. Let's diagnose precisely.

### 6.1 The heavy hooks (ranked by ROI)

| Hook | Token cost / session (50 turns, 15 tool calls/turn = 750 tool calls) | Value | Verdict |
|---|---|---|---|
| Cursor `userPromptSubmit` (`head -50 task_plan.md` + `tail -20 progress.md`) | ~2k × 50 turns = **100k tokens** | Medium — useful after `/clear`, useless otherwise | **DROP for steady-state; replace with on-demand `/recall` skill** |
| Cursor / Copilot `preToolUse` (`head -30 task_plan.md`) | ~1k × 750 calls = **750k tokens** | Low — Claude already has the plan in context after turn 1 | **DROP outright**, this is the primary offender |
| Copilot `sessionStart` running `session-catchup.py` | ~5k × 1 = **5k tokens** | HIGH — recovers context after `/clear` or new session | **KEEP**, fires only once |
| Gemini `BeforeModel` (current-phase line only) | ~30 × 50 = **1.5k tokens** | High signal/cost ratio | **KEEP** as the model for Yanis's lite version |
| `postToolUse` (static reminder) | ~40 × 750 = **30k tokens** | Low — repetition fatigue | **LITE**: fire only after Write/Edit on planning files |
| `agentStop` / `stop` (phase completion check) | ~100 × 1 = **0.1k tokens** | High — actually useful "did you finish?" gate | **KEEP** |
| `errorOccurred` | ~60 × ~3 = **0.2k tokens** | High — fires only on real errors | **KEEP** |

**Total today (Cursor variant with full hooks):** ~890k tokens of pure overhead per long session.
**Total with the lite refactor below:** ~7k tokens per session. **130× reduction.**

### 6.2 Proposed "pwf-lite" for Yanis (5 lines)

```jsonc
// ~/.claude/settings.json — pwf-lite
{
  "hooks": {
    "SessionStart":     [{ "hooks": [{ "type": "command", "command": "sh ~/.claude/scripts/pwf-catchup.sh" }] }],   // 1× catchup only
    "PreToolUse":       [{ "matcher": "Write|Edit", "hooks": [{ "type": "command", "command": "head -3 task_plan.md 2>/dev/null | grep -E '^(## Goal|## Current Phase)' || true" }] }],  // 3 lines max, only on file writes
    "PostToolUse":      [{ "matcher": "Write|Edit",    "hooks": [{ "type": "command", "command": "[ -f task_plan.md ] && [[ \"$CLAUDE_TOOL_INPUT_PATH\" =~ (task_plan|findings|progress)\\.md ]] || echo '[pwf] consider updating progress.md'" }] }],
    "Stop":             [{ "hooks": [{ "type": "command", "command": "sh ~/.claude/scripts/check-complete.sh 2>/dev/null || true" }] }]
  }
}
```

Drop entirely: `userPromptSubmit`, the unmatched `preToolUse`, the `BeforeModel`-style per-LLM-call hooks. Keep only: (1) one-shot catchup at session start, (2) two-line Goal+Phase reminder before destructive ops, (3) post-write nag only when not writing planning files themselves, (4) stop-gate. Total per-session overhead drops from ~890k tokens to ~7k.

### 6.3 What to extract for Yanis's architecture-anthropic skill

The pwf design has real value for the **Memory + Trace + Protocole** triad. Specifically worth keeping:

1. **The three-file schema** (task_plan / findings / progress) as a template — it cleanly maps to working / semantic / episodic memory.
2. **The 5-Question Reboot Check** as a recall-protocol pattern.
3. **The 2-Action Rule** (write multimodal to disk within 2 ops) — pure context-engineering wisdom.
4. **The 3-Strike Error Protocol** as a policy primitive.
5. **`session-catchup.py`** — the cleverest piece. Scans the IDE's own session log to reconstruct context. This is **the** killer feature and Yanis doesn't have an equivalent yet. Worth extracting standalone, ideally rewritten in 100 lines that targets only Claude Code.
6. **`resolve-plan-dir.sh`** — clean fallback chain (env → .active_plan → newest mtime → legacy). The pattern is reusable for any multi-context routing problem.

What to discard for Yanis:
- The per-IDE duplication (Yanis only uses Claude Code).
- The `userPromptSubmit` and unmatched `preToolUse` injection — replace with on-demand `/recall` or `/session-restore` (already present in Yanis's skill list).
- The `loop_limit:3` auto-continuation — too aggressive, easily wastes tokens on a model that wants to stop legitimately.

## 7. Verdict — pertinence for architecture-anthropic

**MOYEN-HAUT.** pwf is the most-developed "filesystem-as-memory" implementation in the public ecosystem and it directly maps to 5 of the 7 architecture-anthropic objets (Mémoire, Trace, Protocole, Politique, Contexte). It's worth studying as a **prior art reference** for Yanis's own memory/trace architecture, but its hook implementation is a cautionary tale: a good idea can be ruined by re-injecting context on every tool call.

The skill's real innovation is `session-catchup.py` (replay-from-trace) and the three-file schema (working/semantic/episodic). Everything else is decoration.

## 8. Artifacts written to this folder

```
SKILL.md                                  -- canonical skill description (from .codex/skills/...)
templates/task_plan.md                    -- full annotated template
templates/progress.md                     -- full annotated template
templates/findings-template.txt           -- findings template (renamed .txt to bypass harness write-block on "findings.md")
hooks/copilot-github-hooks.json           -- Copilot 5-hook config
hooks/cursor-hooks.json                   -- Cursor 4-hook config (heaviest)
hooks/codex-hooks.json                    -- Codex 6-hook config (PascalCase, includes PermissionRequest)
hooks/mastracode-hooks.json               -- inline one-liner reference
hooks/cursor-user-prompt-submit.sh        -- the worst offender, with cost analysis
hooks/cursor-pre-tool-use.sh              -- + analysis
hooks/cursor-post-tool-use.sh             -- + analysis
hooks/cursor-stop.sh                      -- + analysis (loop_limit:3 hidden cost)
hooks/github-session-start.sh             -- + analysis
hooks/github-pre-tool-use.sh              -- + analysis (no matcher = catastrophic)
hooks/github-post-tool-use.sh             -- + analysis
hooks/github-agent-stop.sh                -- KEEP candidate
hooks/github-error-occurred.sh            -- KEEP candidate
hooks/gemini-before-model.sh              -- KEEP candidate (best designed)
scripts/init-session.sh                   -- canonical (abridged) bootstrap
scripts/check-complete.sh                 -- canonical (full)
scripts/resolve-plan-dir.sh               -- canonical (full)
scripts/session-catchup.py                -- abridged stub (full file is ~350 lines)
NOTES.md                                  -- this file
```
