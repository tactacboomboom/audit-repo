# FMATH — anthropics/anthropic-quickstarts

Analyse formelle 8-couches du repo en tant que "système de templates de démarrage Anthropic".

## C1 — Objets

- **Quickstart** : projet isolé, autonome, démarrable indépendamment des autres
- **README** : porte d'entrée obligatoire de chaque quickstart
- **SDK target** : `anthropic` (Python), `@anthropic-ai/sdk` (TS), `claude-code-sdk` (autonomie), `mcp` (tooling externe)
- **API key gate** : `ANTHROPIC_API_KEY` env var (jamais en clair, jamais en fichier versionné)
- **Tool loop** : motif fondamental "LLM + tools in a loop" (formalisé dans `agents/`)
- **Trajectory** : enregistrement structuré des interactions (computer-use-best-practices)

## C2 — Relations

- README racine → README quickstart (1:N catalogage)
- Quickstart → SDK (1:1 dépendance principale)
- Quickstart → API key (1:1 gating)
- Agent → tools (1:N composition)
- Session N → Session N+1 via persistance disque (git + JSON + .txt)

## C3 — Invariants

**I1 — Isolation** : chaque quickstart démarrable sans toucher aux autres. Pas de cross-import.
**I2 — Minimum viable README** : titre + prerequisites + quickstart command + API key setup + structure + license.
**I3 — Secrets jamais versionnés** : `.env.example` versionné, `.env` dans `.gitignore`.
**I4 — Standalone first, container second** : version locale fonctionnelle avant Dockerfile.
**I5 — Tool loop centralisé** : un seul fichier orchestre `client.messages.create` + tool dispatch.

## C4 — Tensions

- **Minimalisme pédagogique vs production-ready** : résolue par doublon explicite (computer-use-demo = démo / computer-use-best-practices = pédagogique avec caching, pruning, sandbox)
- **Python vs TypeScript** : non choisie — coexistence assumée selon le cas d'usage (UI web → TS Next.js ; agent CLI → Python)
- **Dockerisé vs natif** : computer-use propose les deux ; autonomous-coding et best-practices restent natifs

## C5 — Topologie

DAG en étoile : README.md racine est la racine, chaque quickstart est une feuille indépendante. Pas d'arête entre feuilles. CLAUDE.md racine est une note transverse (instructions développeurs).

## C6 — Dynamique

Évolution observable : ajout incrémental de quickstarts (autonomous-coding et computer-use-best-practices sont les plus récents). Pattern d'archi qui se stabilise : `.claude/skills/` apparaît pour la première fois dans computer-use-best-practices → signal faible que les futurs quickstarts auront `.claude/skills/<topic>/SKILL.md`.

## C7 — Frontières

**Dans le périmètre** : structure projet, README, init scripts, security model, persistance session.
**Hors périmètre** : prompt engineering détaillé, fine-tuning, déploiement production cloud (sauf customer-support-agent → AWS Amplify).

## C8 — Verdict structurel

Repo cohérent, modulaire, sans dette architecturale visible. Le `.claude/skills/first-run/SKILL.md` dans computer-use-best-practices est le seul exemple **officiel Anthropic** d'un skill au sein d'un projet user — c'est la référence canonique pour produire un template de skill conforme.
