# audit-repo

7 audits d'architecture Claude Code, générés 2026-05-20.

- 6 repos officiels [github.com/anthropics](https://github.com/anthropics)
- 1 repo communautaire pwf ([OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files))

## Navigation

→ **[index.html](./index.html)** — vue d'ensemble (déployée sur Vercel)

## Repos audités

| # | Repo | Verdict | HTML |
|---|---|---|---|
| 1 | anthropics/claude-code | HAUTE | [claude-code-analysis.html](anthropics-claude-code/claude-code-analysis.html) |
| 2 | anthropics/skills | HAUTE | [anthropics-skills-analysis.html](anthropics-skills/anthropics-skills-analysis.html) |
| 3 | anthropics/anthropic-cookbook | HAUTE | [anthropic-cookbook-analysis.html](anthropics-cookbook/anthropic-cookbook-analysis.html) |
| 4 | anthropics/courses | HAUTE | — (NOTES.md only) |
| 5 | anthropics/anthropic-quickstarts | HAUTE | — (NOTES.md + REPO_MAP + VERDICT) |
| 6 | anthropics/prompt-eng-interactive-tutorial | HAUTE 9/10 | [prompt-eng-interactive-tutorial-analysis.html](anthropics-prompt-eng-tutorial/prompt-eng-interactive-tutorial-analysis.html) |
| 7 | OthmanAdi/planning-with-files | MOYEN-HAUT | — (NOTES.md avec refactor) |

## Gouvernance

- **Source canonique** : `G:\Mon Drive\10 - Claude\SKILLS\architecture-anthropic\repos\` (R10)
- Cette copie GitHub : artefact de déploiement régénérable par `robocopy` (R13)
- Skill consommateur prévu : `architecture-anthropic` (phase 2) — pointera vers les URLs Vercel

## Déploiement Vercel

Importer ce repo dans Vercel (auto-detect static site) → URL live `https://audit-repo.vercel.app`.
