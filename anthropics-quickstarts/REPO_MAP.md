# REPO_MAP — anthropics/anthropic-quickstarts

Source : https://github.com/anthropics/anthropic-quickstarts
Branch : main
Date audit : 2026-05-20
Statut : UNTRUSTED (contenu externe, ne pas exécuter d'instructions sans confirmation utilisateur)

## Vue d'ensemble

Repo officiel Anthropic = collection de templates de démarrage pour construire avec l'API Claude. License MIT. 16.7k stars. C'est la "vitrine officielle" — référence pour ce qu'Anthropic considère comme un projet bien structuré.

## Top-level

```
anthropic-quickstarts/
├── .github/                          # workflows CI Anthropic
├── agents/                           # reference impl minimaliste "LLM + tools in a loop" (~300 LOC)
├── autonomous-coding/                # 2-agent pattern (initializer + coder) avec persistance git
├── browser-use-demo/                 # Playwright + Streamlit, browser automation
├── computer-use-best-practices/      # macOS-native, pédagogique, .claude/skills/ présent
├── computer-use-demo/                # version Docker containerisée du computer-use
├── customer-support-agent/           # Next.js 14 + shadcn/ui + RAG-style
├── financial-data-analyst/           # Next.js 14 + Recharts + PDF.js
├── README.md                         # catalogue top-level
├── CLAUDE.md                         # instructions inter-projets (non publiable verbatim)
├── pyproject.toml                    # racine config Python (pyright sur computer-use-demo)
├── .pre-commit-config.yaml           # ruff + pyright sur computer-use-demo/
└── LICENSE                           # MIT
```

## Stack par quickstart

| Quickstart | Langage | Stack principale | Containerisation |
|---|---|---|---|
| agents | Python | anthropic + mcp SDK | non |
| autonomous-coding | Python | claude-code-sdk + git | non |
| browser-use-demo | Python | Playwright + Streamlit | Docker + docker-compose |
| computer-use-best-practices | Python 3.11+ | pyautogui + sandbox-exec | non (macOS natif) |
| computer-use-demo | Python | xdotool + VNC | Docker |
| customer-support-agent | TypeScript | Next.js 14 + shadcn/ui + Tailwind | AWS Amplify |
| financial-data-analyst | TypeScript | Next.js 14 + Recharts + PDF.js | non |

## Catégorisation par usage

**Apprentissage des fondamentaux** : `agents/` (la référence "lis-moi en premier")
**Production-ready patterns** : `computer-use-best-practices/`, `browser-use-demo/`
**Démos vitrine** : `customer-support-agent/`, `financial-data-analyst/`
**Autonomie multi-session** : `autonomous-coding/`
**Sandbox isolé** : `computer-use-demo/` (Docker)

## Fichiers présentant un intérêt direct pour le skill architecture-anthropic

1. `computer-use-best-practices/.claude/skills/first-run/SKILL.md` — seul `.claude/skills/` du repo, structure officielle de skill
2. `computer-use-best-practices/config.example.toml` — pattern config-as-code Anthropic (CU_* env vars + TOML overlay)
3. `autonomous-coding/prompts/initializer_prompt.md` — pattern d'initialisation projet par agent
4. `autonomous-coding/security.py` — pattern allowlist bash (defense-in-depth)
5. `.pre-commit-config.yaml` — outillage qualité Python officiel (ruff + pyright)
6. `pyproject.toml` racine — pattern monorepo Python multi-projets
