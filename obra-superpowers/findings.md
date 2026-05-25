# Findings — obra/superpowers

**Repo :** https://github.com/obra/superpowers  
**Date collecte :** 2026-05-25  
**Version :** 5.1.0 (2026-04-30)

## Stats brutes
- Stars : 206 000 | Forks : 18 300 | Issues ouvertes : 139
- Langages : Shell 66.4%, JavaScript 24.8%, HTML 3.3%, Python 2.8%, TypeScript 2.1%
- Licence : MIT | Pas de dépendances runtime

## Description officielle
> "An agentic skills framework & software development methodology that works"

## Architecture root
```
.claude-plugin/ .codex-plugin/ .cursor-plugin/ .opencode/
assets/ docs/ hooks/ scripts/ skills/ tests/
AGENTS.md  CLAUDE.md  CODE_OF_CONDUCT.md  GEMINI.md  README.md  RELEASE-NOTES.md
gemini-extension.json  package.json  LICENSE
```

## package.json
- name: superpowers, version: 5.1.0
- type: module, main: ".opencode/plugins/superpowers.js"
- Aucune dépendance runtime ni devDependency

## Skills (14 dossiers)
brainstorming / dispatching-parallel-agents / executing-plans / finishing-a-development-branch /
receiving-code-review / requesting-code-review / subagent-driven-development / systematic-debugging /
test-driven-development / using-git-worktrees / using-superpowers / verification-before-completion /
writing-plans / writing-skills

## Hooks
hooks.json / hooks-cursor.json / run-hook.cmd / session-start

## Workflow 7 étapes
1. Brainstorming (Socratic questioning)
2. Git Worktrees (branches isolées)
3. Writing Plans (tasks 2-5 min)
4. Executing Plans + Subagent-driven development
5. Test-Driven Development (RED-GREEN-REFACTOR)
6. Code Review (requesting + receiving)
7. Branch Completion (merge/PR)

## Installation agents
- Claude Code : `/plugin install superpowers@claude-plugins-official`
- Codex CLI : marketplace officiel
- Factory Droid : `droid plugin install superpowers@superpowers`
- Gemini CLI : `gemini extensions install https://github.com/obra/superpowers`
- Cursor : `/add-plugin superpowers`
- GitHub Copilot CLI : `copilot plugin install superpowers@superpowers-marketplace`

## Breaking changes v5.1.0
- Named agent dispatch supprimé → generic templates
- Legacy slash commands supprimés (/brainstorm, /execute-plan, /write-plan)
- Integration sections supprimées de l'architecture skills

## Historique versions
2025-10: v3.x (base) | 2025-12: v4.0.0 | 2026-02: v4.3 | 2026-03: v5.0.x | 2026-04: v5.1.0
