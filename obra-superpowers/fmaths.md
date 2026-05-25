---
name: superpowers-fmaths
description: Ontologie formelle obra/superpowers — 7 primitives, ensembles, 4 tensions, 6 invariants, axes de variation, seuils d'effondrement, couplages. Charger pour analyse architecturale ou debug structurel.
---

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
