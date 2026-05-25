---
name: superpowers-verdict
description: Évaluation obra/superpowers v5.1.0 — score 8.3/10, forces/faiblesses, matrice use-cases, roadmap. Charger pour décision d'adoption ou préparer une recommandation.
---

# Verdict PM — obra/superpowers

## Score 3 dimensions

| Dimension | Score | Justification |
|---|---|---|
| Pertinence PM (framework agent / méthodologie) | 9/10 | Unique en son genre : méthodologie complète 7 étapes pour agents IA, multi-agent, 206k ★ |
| Maturité prod | 8/10 | v5.1, MIT, 2+ ans d'itération, mais breaking changes fréquents (tous les 4-6 mois) |
| Facilité onboarding | 8/10 | 1 commande d'install, happy path documenté, mais 5 manifests à maintenir si on personnalise |

**Score global : 8.3/10**

---

## Forces

| | Titre | Description |
|---|---|---|
| ✅ | Multi-agent universel | 6 agents supportés (Claude Code, Cursor, Codex, Gemini, Factory, Copilot) — migration sans perte de méthodologie |
| ✅ | Workflow 7 étapes battle-tested | 2+ ans d'itération, 206k ★, 18.3k forks — la méthodologie a prouvé sa valeur à grande échelle |
| ✅ | TDD non-négociable | Le framework impose RED-GREEN-REFACTOR — élimine la tentation de sauter les tests sous pression |
| ✅ | Zero dépendance runtime | Aucune dépendance npm, pas de build step — installation atomique, pas de supply chain attack surface |
| ✅ | Extensible par design | `writing-skills` inclus — la méthodologie se documente elle-même et encourage l'extension custom |
| ✅ | Parallélisme natif | `dispatching-parallel-agents` → N subagents simultanés → throughput de développement multiplié |

---

## Faiblesses / Risques

| | Titre | Description + Impact |
|---|---|---|
| ⚠️ | Breaking changes fréquents | ~30 releases en 8 mois, breaking change majeur v4→v5. Impact : migration manuelle obligatoire sur chaque upgrade majeur |
| ⚠️ | 5 manifests agents hétérogènes | Chaque skill update = potentiellement 5 fichiers à maintenir en sync. Impact : comportement divergent selon l'agent si désync |
| ⚠️ | Pas de frontmatter YAML | Contrairement à anthropics/skills, pas de validation automatisée possible. Impact : skill mal écrit invisible jusqu'à l'exécution |
| ⚠️ | Fragmentation multi-agent permanente | 6 agents évoluent leurs specs indépendamment. Impact : décalage entre le framework et les agents — risque de feature gap |
| 🔴 | Hooks silencieusement absents | Si session-start ne charge pas, les skills disparaissent sans erreur visible. Impact : l'agent fonctionne mais sans la méthodologie |

---

## Matrice Use Cases

### ✅ Oui — Usage approprié

| Use Case | Pourquoi |
|---|---|
| Onboarding équipe sur méthodologie agent | Framework clé-en-main, 7 étapes documentées, skills install en 1 commande |
| Projet multi-agent (Claude + Cursor) | Même méthodologie sur 6 agents — cohérence garantie |
| Adoption TDD sur codebase legacy | Le skill TDD impose la discipline sans effort de conviction |
| Développement de skills custom | writing-skills inclus — le framework se self-documente |

### ❌ Attendre / Non — Usage à risque

| Use Case | Pourquoi |
|---|---|
| Intégration dans produit B2B à SLA strict | Pas de support officiel, breaking changes trop fréquents |
| Équipe qui n'adopte pas d'agent de code | Le framework nécessite un agent — pas de valeur sans lui |
| Projet où les étapes workflow sont incompatibles | Le séquencement 7 étapes est rigide — mauvais fit pour flux ad-hoc |
| Adoption sans version épinglée | Risque de régression silencieuse à chaque update auto |

---

## Roadmap (extraite des RELEASE-NOTES)

| Feature | Statut | Impact |
|---|---|---|
| Generic template dispatch | ✅ v5.1.0 | Rompt les named agents — portabilité accrue |
| Git worktree rewrite | ✅ v5.1.0 | Détection environment + consent requirements |
| Codex plugin mirror tooling | ✅ v5.1.0 | Sync OpenAI marketplace automatisé |
| Code review via "general-purpose" agent | ✅ v5.1.0 | Plus de dispatch nommé pour la review |
| Session hooks Windows (Cursor) | ✅ v5.1.0 | Routing amélioré — correction UX critique |
| V6 (probable H2 2026) | ⏳ Non annoncé | Attendre RELEASE-NOTES avant upgrade |

---

## Recommandation finale

**Superpowers est le framework de référence pour toute équipe qui utilise des agents de code.** Rien d'autre sur le marché ne propose une méthodologie aussi complète, aussi battle-tested (206k ★, 2+ ans), aussi portable (6 agents). Le fait qu'il n'ait aucune dépendance runtime le rend quasiment sans risque à l'installation.

**Action recommandée :** adopter immédiatement pour tout nouveau projet avec agent de code. Épingler la version à `5.1.0` dans les configs d'installation. Créer un worktree dédié pour tester les upgrades avant de les pousser en production (le framework enseigne lui-même cette pratique). Si votre équipe utilise Cursor sur Windows, valider manuellement le chargement de `hooks-cursor.json` après install. Pour les équipes qui veulent étendre la méthodologie : lire `writing-skills` en premier — c'est la porte d'entrée vers la customisation.
