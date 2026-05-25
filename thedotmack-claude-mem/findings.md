---
name: claude-mem-findings
description: Données brutes thedotmack/claude-mem v13.3.0 — stats GitHub, architecture 5 composants, dépendances, 271 releases, hooks, MCP, Server Beta. Charger pour vérifier faits ou commandes d'installation.
---

# Findings — thedotmack/claude-mem

**Repo :** https://github.com/thedotmack/claude-mem
**Date collecte :** 2026-05-25
**Version :** 13.3.0 (2026-05-21)

## Stats brutes
- Stars : 78 000 | Forks : 6 700 | Issues ouvertes : 145 | PRs ouvertes : 94
- Watchers : 277 | Commits : 1 906 | Releases : 271
- Langages : TypeScript 91.5%, JavaScript 5.1%, Shell 1.6%, HTML 1.5%, Other 0.3%
- Licence : Apache 2.0 (migré depuis AGPL-3.0 en v13.0.0)
- Auteur : Alex Newman (@thedotmack)

## Description officielle
> "Persistent Context Across Sessions for Every Agent – Captures everything your agent does during sessions, compresses it with AI, and injects relevant context back into future sessions."

## Architecture root
```
.agent/ .agents/ .claude/ .claude-plugin/ .codex-plugin/ .github/ .plan/ .windsurf/
cursor-hooks/ docker/ docs/ evals/ install/ openclaw/ plans/ plugin/ ragtime/
scripts/ src/ tests/
README.md  package.json  tsconfig.json  LICENSE  CHANGELOG.md
Dockerfile.test-installer  docker-compose.yml  bunfig.toml
```

## Architecture src/
```
adapters/ bin/ cli/ core/schemas/ hooks/ integrations/opencode-plugin/
npx-cli/ sdk/ server/ servers/ services/ shared/ storage/
supervisor/ types/ ui/ utils/
```

## 5 composants principaux
1. **Lifecycle Hooks** — 6 scripts (SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd, + smart install pre-hook)
2. **Worker Service** — HTTP API port 37777 + Web UI, géré par Bun
3. **SQLite Database** — sessions + observations + summaries avec FTS5 full-text search
4. **Vector Search** — ChromaDB (hybrid sémantique + keyword)
5. **mem-search Skill** — interface NL query, progressive disclosure, 3 niveaux (search → timeline → get_observations)

## package.json
- name: claude-mem, version: 13.3.0
- type: module, bin: claude-mem → ./dist/npx-cli/index.js
- engines: Node >=20.0.0, Bun >=1.0.0
- Core deps: @anthropic-ai/claude-agent-sdk, @modelcontextprotocol/sdk, express, react, ioredis, bullmq, better-auth, zod
- Dev deps: TypeScript, tree-sitter grammars (24 langages), esbuild, tsx

## Agents supportés
Claude Code, Gemini CLI, OpenCode, Codex CLI/App, Windsurf, Claude Desktop, OpenClaw Gateway

## Installation (modes)
- Claude Code : `npx claude-mem install`
- Gemini CLI : `npx claude-mem install --ide gemini-cli`
- OpenCode : `npx claude-mem install --ide opencode`
- Plugin marketplace : `/plugin marketplace add thedotmack/claude-mem` puis `/plugin install claude-mem`
- OpenClaw : `curl -fsSL https://install.cmem.ai/openclaw.sh | bash`

## Prérequis runtime
- Node.js >= 20.0.0
- Bun >= 1.0.0 (auto-installé si absent)
- uv Python package manager (auto-installé si absent)
- SQLite 3 (bundlé)
- Server Beta uniquement : Postgres + Redis

## MCP — 3 couches token-efficient
1. `search` — index compact, IDs (~50-100 tokens) — full-text + type/date/project filters
2. `timeline` — contexte chronologique autour d'observations
3. `get_observations` — détails complets par IDs (~500-1000 tokens par lot)
Économies estimées : ~10× tokens via filtrage progressif

## Features clés
- Persistent memory cross-session
- Progressive disclosure (coût token visible)
- Privacy tags `<private>` pour exclure contenu sensible
- Web Viewer UI temps réel : http://localhost:37777
- Citations par ID via API `/api/observation/{id}`
- Modes i18n : code / code--zh / code--ja (ISO 639-1)
- Feeds optionnels : Telegram / Discord / Slack
- Beta "Endless Mode"

## Historique versions majeures
- v12.0.0 (2026-04-07) : Platform source isolation (Claude vs Codex sessions séparées), PreToolUse gate
- v13.0.0 (2026-05-08) : Server Beta opt-in (Postgres + BullMQ), relicence Apache-2.0
- v13.3.0 (2026-05-21) : Skills design-is, weekly-digests, oh-my-issues, MCP fixes

## Cadence de release
271 releases au total. Rythme : plusieurs releases/jour en période active (7 en 10 jours en mai 2026). Pattern : majeurs = shift architectural, mineurs/patchs = corrections régressions prod.

## Topics GitHub
ai, sqlite, embeddings, ai-agents, claude, memory-engine, long-term-memory, rag, anthropic, chromadb, ai-memory, mem0, claude-code, supermemory, openmemory, claude-agents, claude-agent-sdk, claude-code-plugin, claude-skills
