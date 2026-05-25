# Fmaths — obra/superpowers

## L0 — Ontologie (primitives non-redondantes)

1. **Skill** — protocole markdown auto-suffisant définissant un comportement agent (sans frontmatter YAML — différence structurelle vs anthropics/skills)
2. **Agent** — moteur d'exécution consommateur (Claude Code, Cursor, Codex, Gemini CLI, Factory Droid, Copilot)
3. **Plugin** — bundle d'installation multi-agents encapsulant N skills sous un format d'agent spécifique
4. **Hook** — déclencheur événementiel (session-start, pre/post-tool) qui orchestre le bootstrapping du workflow
5. **Plan** — artefact structuré de tâches temporées (2-5 min chacune), produit par writing-plans et consommé par executing-plans
6. **Worktree** — espace de travail Git isolé sur branche dédiée, activé par using-git-worktrees
7. **Subagent** — processus délégué lancé par dispatching-parallel-agents pour exécution parallèle

## L1 — Ensembles et relations

- `Skills = {brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills}` (14 éléments)
- `Agents_supportés = {Claude Code, Codex CLI, Factory Droid, Gemini CLI, Cursor, GitHub Copilot CLI}` (6 éléments)
- `Manifests = {.claude-plugin/, .codex-plugin/, .cursor-plugin/, .opencode/, gemini-extension.json}` (5 formats distincts)
- `Hooks = {hooks.json, hooks-cursor.json, run-hook.cmd, session-start}`
- `Workflow_stages = {Brainstorm, Worktree, Plan, Execute, TDD, Review, Finish}` (7 étapes ordonnées)
- Relations :
  - `encapsulates: Plugin → Skills` (1:N)
  - `targets: Plugin → Agent` (1:1 par agent)
  - `ordered: Workflow_stages` (séquence stricte)
  - `consumes: Agent → Skills` (M:N via Plugin)

## L2 — Logique et tensions

- **AND** : `valid_delivery ⟺ brainstorm_done ∧ worktree_isolated ∧ plan_approved ∧ tdd_red_green_refactor ∧ code_review_passed ∧ verification_ok`
- **XOR** (historique) : `named_dispatch(< v5.1) ⊕ generic_template_dispatch(≥ v5.1)` — rupture backward-incompatible
- **OR** : agent peut consommer skills en séquentiel OU via dispatching-parallel-agents (deux modes légitimes)

- **Tension #1 — Universalité vs Fidélité** : 6 agents supportés → 5 formats de manifests distincts à maintenir en sync. Toute évolution d'un skill = 6 mises à jour potentielles.
- **Tension #2 — Légèreté vs Richesse** : installation en une commande (frictionless) ↔ 14 skills + hooks + worktrees = complexité cachée post-install.
- **Tension #3 — Discipline vs Agilité** : workflow 7 étapes ordonné ↔ tendance naturelle des agents à sauter des étapes sous pression de complétion (p. ex. TDD ignoré).
- **Tension #4 — Agnosticisme vs Spécialisation** : skills sans frontmatter YAML (agnostiques) ↔ manifests hyper-spécialisés par agent (CLAUDE.md, AGENTS.md, GEMINI.md, etc.).

## L3 — Invariants (I1...In)

- **I1** : un skill = un dossier dans `skills/` avec un protocole markdown (NB : pas de frontmatter YAML — c'est un choix de portabilité)
- **I2** : le workflow est séquentiel et ordonné — Brainstorm → Worktree → Plan → Execute → TDD → Review → Finish
- **I3** : TDD RED-GREEN-REFACTOR est non-négociable — test failing obligatoire avant implémentation
- **I4** : verification-before-completion est le dernier garde-fou avant tout merge
- **I5** : 1 feature = 1 worktree = 1 branche (pas de multi-features entrelacées)
- **I6** : les hooks bootstrappent le workflow à chaque session — le contexte est rechargé automatiquement

## L4 — Axes de variation

| Axe | Min | Actuel (v5.1.0) | Max |
|---|---|---|---|
| Agents supportés | 1 | 6 | N (spec ouverte) |
| Skills actifs | 1 | 14 | Extensible (writing-skills inclus) |
| Automatisation hooks | Manuel (0 hook) | session-start auto | Full pipeline (pre/post chaque tool) |
| Parallélisme exécution | Séquentiel | Subagent-driven + parallel dispatch | N subagents simultanés |
| Maturité versioning | v1.0 (2025-10) | v5.1.0 (2026-04) | — |

## L5 — Seuils et stabilité

| Seuil | Valeur | Conséquence si dépassé |
|---|---|---|
| Durée tâche plan | 2-5 min | Tâche à redécouper → plan invalide |
| Cycle TDD | 1 test fail → 1 green → refactor | Skip RED → test de complaisance → bugs cachés |
| Code review | 2 passes (requesting + receiving) | 1 seule passe → angles morts non détectés |
| Worktrees simultanés | Non spécifié | Merge conflicts → résolution manuelle |
| Manifests agents | 5 formats | Désync → comportement divergent selon l'agent |

- **Effondrement #1** : brainstorming sauté → plans non validés → dette technique exponentielle
- **Effondrement #2** : hooks non chargés → skills non disponibles → workflow silencieusement absent
- **Effondrement #3** : mise à jour skill sans mise à jour de tous les manifests → comportement partiel

## L6 — Catégories et couplages

| Couche | Statut couplage |
|---|---|
| Skills discovery (brainstorming, writing-plans) | Indépendants ✅ |
| Skills exécution (executing-plans, subagent-driven, tdd) | Couplés séquentiellement ⚠️ |
| Skills qualité (review ×2, verification, debugging) | Découplables ✅, dépendent logiquement de l'exécution |
| Skills coordination (dispatching, git-worktrees, finishing) | Infrastructure transversale ✅ |
| Manifests agents (.claude-plugin, .codex-plugin, .cursor-plugin, .opencode, gemini-extension.json) | Couplage fort par agent ⚠️ (5 formats hétérogènes) |
| Hooks (hooks.json, hooks-cursor.json) | Couplage moyen — Cursor a son propre fichier ⚠️ |

## L7 — Topologie (chemin de moindre résistance)

**Happy path (7 étapes) :**
```
/brainstorm → [using-git-worktrees] → /writing-plans → /executing-plans
    → /test-driven-development → /requesting-code-review → /receiving-code-review
    → /verification-before-completion → /finishing-a-development-branch
```

**Nœuds de friction :**
- **F1** : 5 manifests agents à maintenir en sync (chaque skill update × 5 formats)
- **F2** : Cursor Windows nécessite `hooks-cursor.json` dédié (routing séparé)
- **F3** : installation via CLI propriétaires (Factory Droid, Gemini) = dépendance externe non controlée
- **F4** : `skills/` sans frontmatter YAML → pas de validation automatisée possible (contrairement à anthropics/skills)
- **F5** : breaking change v4→v5 (named dispatch supprimé) = migration manuelle pour early adopters

## L8 — Probabilités et incertitudes

| Variable | Probabilité | Justification |
|---|---|---|
| P(adoption stable 12 mois) | très haute | 206k ★, 18.3k forks, MIT, v5.1 stable |
| P(breaking change v6) | médium-haute | rythme historique : breaking change majeur tous les 4-6 mois |
| P(fragmentation multi-agent) | haute | 6 agents évoluent leurs specs indépendamment |
| P(lock-in Claude Code) | faible | by design agnostique — CLAUDE.md est l'un des 6 |
| P(adoption corporate) | médium | MIT + 206k ★ mais pas de support officiel, pas de SLA |
| Maturité communauté | très haute | 2+ ans, rythme release rapide (>30 versions), 206k ★ |

## Vecteur cognitif — bilan

- **Abstraction** : forte — le framework est une méthodologie, pas une lib ; les primitives sont claires
- **Concrétude** : forte — 14 skills opérationnels + happy path documenté + commandes d'install copiables
- **Affect** : médium — "methodology that works" = promesse pragmatique, ton CLI communautaire
- **Normativité** : forte — 7 étapes ordonnées, TDD non-négociable, vérification obligatoire
- **Incertitude** : médium — breaking changes fréquents, fragmentation multi-agent non résolue
- **Altérité** : forte — 6 agents différents, architecture ouverte à extension
- **Cohérence** : forte en interne, faible sur les manifests agents (hétérogénéité structurelle)
