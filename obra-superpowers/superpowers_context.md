---
name: superpowers-context
description: Contexte compressé obra/superpowers v5.1.0 — findings + fmaths + recit + verdict + installation. Charger pour toute session travaillant sur superpowers.
generated: compress_context.py (auto)
---

# Contexte obra/superpowers — compressé

Sources : findings.md, fmaths.md, recit.md, verdict.md, installation.md

<!-- findings.md -->
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

---

<!-- fmaths.md -->
# Fmaths — obra/superpowers

## L0 — Primitives (7 concepts non-redondants)

1. **Skill** — protocole markdown auto-suffisant définissant un comportement agent (sans frontmatter YAML)
2. **Agent** — moteur d'exécution consommateur (Claude Code, Cursor, Codex, Gemini CLI, Factory Droid, Copilot)
3. **Plugin** — bundle d'installation multi-agents encapsulant N skills sous un format d'agent spécifique
4. **Hook** — déclencheur événementiel (session-start, pre/post-tool) qui bootstrappe le workflow
5. **Plan** — artefact de tâches temporées 2-5 min, produit par writing-plans, consommé par executing-plans
6. **Worktree** — espace Git isolé sur branche dédiée, activé par using-git-worktrees
7. **Subagent** — processus délégué lancé par dispatching-parallel-agents pour exécution parallèle

## L1 — Ensembles

- `Skills` = 14 éléments (voir findings.md)
- `Agents_supportés` = 6 éléments (Claude Code, Codex CLI, Factory Droid, Gemini CLI, Cursor, GitHub Copilot CLI)
- `Manifests` = 5 formats distincts (.claude-plugin/, .codex-plugin/, .cursor-plugin/, .opencode/, gemini-extension.json)
- Relations : `Plugin → Skills` (1:N) · `Plugin → Agent` (1:1) · `Workflow_stages` (séquence stricte 7) · `Agent → Skills` (M:N via Plugin)

## L2 — Logique et tensions

**Logique :**
- `valid_delivery ⟺ brainstorm ∧ worktree_isolated ∧ plan_approved ∧ tdd_red_green_refactor ∧ review_passed ∧ verification_ok`
- `named_dispatch(< v5.1) ⊕ generic_template_dispatch(≥ v5.1)` — rupture backward-incompatible

**4 tensions structurelles :**

| # | Tension | Pôle A | Pôle B |
|---|---------|--------|--------|
| T1 | Universalité vs Fidélité | 6 agents supportés | 5 manifests à maintenir en sync |
| T2 | Légèreté vs Richesse | 1 commande install | 14 skills + hooks + worktrees (complexité post-install) |
| T3 | Discipline vs Agilité | workflow 7 étapes ordonné | tendance agents à sauter étapes sous pression |
| T4 | Agnosticisme vs Spécialisation | skills sans frontmatter (portables) | manifests hyper-spécialisés par agent |

## L3 — Invariants

| ID | Invariant |
|----|-----------|
| I1 | 1 skill = 1 dossier dans `skills/` avec protocole markdown (pas de frontmatter YAML — choix portabilité) |
| I2 | workflow séquentiel ordonné : Brainstorm → Worktree → Plan → Execute → TDD → Review → Finish |
| I3 | TDD RED-GREEN-REFACTOR non-négociable — test failing obligatoire avant implémentation |
| I4 | verification-before-completion est le dernier garde-fou avant tout merge |
| I5 | 1 feature = 1 worktree = 1 branche (pas d'entrelacement) |
| I6 | les hooks bootstrappent le workflow à chaque session — sans eux les skills sont silencieusement absents |

## L4 — Axes de variation

| Axe | Min | v5.1.0 | Max |
|-----|-----|---------|-----|
| Agents supportés | 1 | 6 | N (spec ouverte) |
| Skills actifs | 1 | 14 | Extensible via writing-skills |
| Automatisation hooks | 0 hook | session-start auto | Full pre/post each tool |
| Parallélisme | Séquentiel | Subagent + parallel dispatch | N subagents simultanés |

## L5 — Seuils d'effondrement

| Seuil | Valeur | Conséquence |
|-------|--------|-------------|
| Durée tâche plan | > 5 min | Tâche à redécouper |
| Cycle TDD | skip RED | Test de complaisance → bugs cachés |
| Skill update | sans màj 5 manifests | Comportement divergent selon agent |
| Session | hooks non chargés | Skills silencieusement absents |
| Merge | sans verification-before-completion | Régression non détectée |

**3 effondrements système :**
- **E1** : brainstorming sauté → plans non validés → dette technique exponentielle
- **E2** : hooks non chargés → skills non disponibles → workflow silencieusement absent
- **E3** : skill mis à jour sans mise à jour des 5 manifests → comportement partiel

## L6 — Couplages

| Couche | Couplage |
|--------|----------|
| Skills discovery (brainstorming, writing-plans) | Indépendants ✅ |
| Skills exécution (executing-plans, subagent-driven, tdd) | Couplés séquentiellement ⚠️ |
| Skills qualité (review ×2, verification, debugging) | Découplables ✅ |
| Skills coordination (dispatching, git-worktrees, finishing) | Infrastructure transversale ✅ |
| Manifests agents (5 formats) | Couplage fort ⚠️ |
| Hooks (hooks.json vs hooks-cursor.json) | Couplage moyen ⚠️ (Cursor = fichier séparé) |

## L7 — Happy path + frictions

**Séquence :** `/brainstorm → worktree → /writing-plans → /executing-plans → /test-driven-development → /requesting-code-review → /receiving-code-review → /verification-before-completion → /finishing-a-development-branch`

**Points de friction :**
- F1 : 5 manifests agents à maintenir en sync (chaque skill update × 5 formats)
- F2 : Cursor Windows nécessite `hooks-cursor.json` dédié
- F3 : skills sans frontmatter YAML → pas de validation automatisée (contrairement à anthropics/skills)
- F4 : breaking change v4→v5 (named dispatch supprimé) = migration manuelle pour early adopters

---

<!-- recit.md -->
# Récit — obra/superpowers

## Essence

Framework de développement universel : une méthodologie écrite une fois, fonctionnant sur 6 agents. 206k ★, 14 skills, 5 formats d'installation, zéro dépendance runtime.

## 3 règles fondamentales

1. **Tu ne codes pas avant un test qui échoue** — RED-GREEN-REFACTOR est un invariant, pas une option
2. **1 feature = 1 worktree = 1 branche** — pas d'entrelacement, pas de "juste ça en plus"
3. **Plus de dispatch nommé (≥ v5.1)** — templates génériques : moins expressif, plus portable

## 3 leviers de transformation

| Levier | Mécanisme | Impact |
|--------|-----------|--------|
| Parallélisme subagents | dispatching-parallel-agents → N trajectoires simultanées | throughput × N |
| Extension ouverte | writing-skills inclus dans le repo | customisation sans fork |
| Portabilité multi-agent | Cursor → Claude Code = changement de manifest seulement | 0 perte de méthodologie |

## Points de rupture

| Signal | Risque |
|--------|--------|
| Tâche plan > 5 min | Plan trop vague → redécouper |
| TDD sans RED au départ | Test de complaisance → bugs cachés |
| Skill mis à jour sans màj 5 manifests | Comportement divergent selon agent |
| Hooks non chargés | Skills silencieusement absents — le plus insidieux |
| Merge sans verification-before-completion | Régression non détectée |

## Posture d'adoption

**Adopter** pour tout projet avec agent de code. **Épingler** la version (`/plugin install superpowers@5.1.0`). **Tester** les upgrades en worktree isolé — le framework enseigne lui-même cette pratique.

**Ne pas intégrer** dans un produit B2B à SLA strict : ~30 releases en 8 mois, breaking change majeur v4→v5, V6 probable H2 2026.

---

<!-- verdict.md -->
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

---

<!-- installation.md -->
# Installation — obra/superpowers v5.1.0

## Prérequis

| Outil | Version min | Vérification |
|---|---|---|
| Git | 2.30+ | `git --version` |
| Agent de code | Voir tableau ci-dessous | — |
| Node.js | Non requis (runtime) | — |

## Agents supportés

| Agent | Commande d'installation |
|---|---|
| Claude Code (CLI) | `/plugin install superpowers@claude-plugins-official` |
| Codex CLI / App | Rechercher "Superpowers" dans le marketplace officiel |
| Factory Droid | `droid plugin install superpowers@superpowers` |
| Gemini CLI | `gemini extensions install https://github.com/obra/superpowers` |
| Cursor | `/add-plugin superpowers` |
| GitHub Copilot CLI | `copilot plugin install superpowers@superpowers-marketplace` |

---

## Option A — Installation rapide (recommandée)

### Claude Code

```bash
# Dans une session Claude Code active
/plugin install superpowers@claude-plugins-official
```

Après installation, relancer la session. Les 14 skills sont disponibles. Le hook `session-start` s'initialise automatiquement.

### Gemini CLI

```bash
gemini extensions install https://github.com/obra/superpowers
```

---

## Option B — Depuis le source (pour contribuer ou personnaliser)

```bash
# 1. Cloner le repo
git clone https://github.com/obra/superpowers.git
cd superpowers

# 2. Lier localement à votre agent
# Pour Claude Code, copier le dossier plugin
cp -r .claude-plugin/ ~/.claude/plugins/superpowers/

# 3. Vérifier la structure
ls skills/
# Attendu : brainstorming/ dispatching-parallel-agents/ executing-plans/ ...
```

---

## Config minimale

Aucun fichier `.env` requis. Le `package.json` est minimal :

```json
{
  "name": "superpowers",
  "version": "5.1.0",
  "type": "module",
  "main": ".opencode/plugins/superpowers.js"
}
```

Les hooks se configurent automatiquement via `hooks/hooks.json` (tous agents) et `hooks/hooks-cursor.json` (Cursor spécifiquement).

---

## Commandes de vérification

Après installation Claude Code, dans une nouvelle session :

```
# Vérifier que les skills sont disponibles
/skills

# Lancer le premier skill
/brainstorm

# Confirmer le workflow complet
/using-superpowers
```

Résultat attendu : Claude propose une session de brainstorming socratique.

---

## Workflow de base post-install

```bash
# 1. Brainstorming
/brainstorm "Votre idée ou problème"

# 2. Isolation (créé automatiquement par le skill)
# → git worktree add ../feature-branch feature/ma-feature

# 3. Planification
/writing-plans

# 4. Exécution (avec subagents optionnels)
/executing-plans

# 5. TDD (obligatoire — RED avant GREEN)
/test-driven-development

# 6. Review
/requesting-code-review
/receiving-code-review

# 7. Finalisation
/verification-before-completion
/finishing-a-development-branch
```

---

## Points d'attention Windows (PowerShell)

```
⚠️ WARN — hooks-cursor.json
Cursor sur Windows utilise un fichier de hooks séparé (hooks/hooks-cursor.json).
Si les skills ne s'activent pas dans Cursor, vérifier que ce fichier est bien chargé.
```

```
⚠️ WARN — run-hook.cmd
Le fichier hooks/run-hook.cmd est le wrapper Windows pour les hooks shell.
Il doit rester dans hooks/ — ne pas déplacer.
```

```
⚠️ WARN — Paths avec espaces
Si votre dossier de projet contient des espaces, encapsuler les paths dans les hooks :
  "C:\Users\mon nom\projects\..." → utiliser des guillemets doubles dans la config hook
```

```
⚠️ WARN — Version épinglée
Superpowers sort ~30 releases en 8 mois. Spécifier la version à l'install si vous
voulez de la stabilité :
  /plugin install superpowers@5.1.0
```