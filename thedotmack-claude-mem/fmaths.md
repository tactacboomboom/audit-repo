---
name: claude-mem-fmaths
description: Ontologie formelle thedotmack/claude-mem v13.3.0 — 7 primitives, ensembles, 5 tensions, 8 invariants, axes de variation, seuils d'effondrement, couplages, probabilités. Charger pour analyse architecturale ou debug structurel.
---

# Fmaths — thedotmack/claude-mem

## L0 — Ontologie (7 primitives non-redondantes)

1. **Observation** — unité atomique de mémoire : une action d'agent (tool call, réponse, résultat) capturée avec métadonnées (session_id, platform_source, timestamp, projet)
2. **Session** — conteneur temporel d'observations, borné par SessionStart/SessionEnd hooks, isolé par platform_source
3. **Hook** — déclencheur événementiel (6 types) qui capture, compresse ou injecte le contexte à des moments précis du cycle de vie agent
4. **Worker** — service HTTP persistant (Bun, port 37777) qui orchestre le pipeline de compression, l'indexation SQLite/ChromaDB, et le Web UI
5. **Skill** — protocole NL de requête mémoire (mem-search + skills satellites) exposant les observations via MCP en 3 couches (search → timeline → get_observations)
6. **Corpus** — agrégat persistant multi-sessions : SQLite (FTS5) + ChromaDB (vecteurs) + summaries AI — la "prothèse mnésique" matérialisée
7. **Gate** — garde-fou conditionnel (PreToolUse, quota, privacy-tag) contrôlant ce qui entre et sort du corpus

## L1 — Ensembles et relations

- `Observations` ⊂ Sessions ⊂ Corpus — relation d'inclusion stricte
- `Agents_supportés` = {Claude Code, Gemini CLI, OpenCode, Codex, Windsurf, Claude Desktop, OpenClaw} — 7 membres
- `Hooks` = {SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd, PreToolUse} — 6 événements
- `Storage` = SQLite(FTS5) ∪ ChromaDB(vecteurs) — union hybride requêtable
- `Skills` = {mem-search, design-is, weekly-digests, oh-my-issues, wowerpoint, babysit, knowledge-agent, make-plan, timeline-report, version-bump, ...}
- Relations :
  - `Hook → Observation` (1:N capture)
  - `Worker → Corpus` (1:1 gestion)
  - `Skill → MCP → Corpus` (N:1 lecture)
  - `Gate ↔ Observation` (filtrage bidirectionnel entrée/sortie)
  - `Session → platform_source` (isolation par agent)

## L2 — Logique et tensions

**Invariant de capture :**
`valid_memory ⟺ Hook_fired ∧ Worker_running ∧ ¬privacy_tag ∧ ¬quota_exceeded`

**Invariant de récupération :**
`context_injected ⟺ SessionStart_fired ∧ Corpus_accessible ∧ relevance(query, obs) > θ`

**XOR architectural critique :**
`Worker_mode ⊕ ServerBeta_mode` — mutuellement exclusifs à l'exécution (v13.0.0)

**5 tensions structurelles :**

| # | Tension | Pôle A | Pôle B |
|---|---------|--------|--------|
| T1 | Richesse vs Coût | Corpus exhaustif (tout capturer) | Budget token (injection sélective) |
| T2 | Vitesse vs Qualité | Compression immédiate (hooks sync) | Compression AI différée (Worker async) |
| T3 | Universalité vs Isolation | 7 agents supportés en parallèle | platform_source isolation par agent |
| T4 | Légèreté vs Puissance | Worker simple (SQLite + Bun) | Server Beta (Postgres + Redis + BullMQ) |
| T5 | Ouverture vs Contrôle | Apache 2.0, API publique, ext. libres | Privacy gates, quota hard-stop, env isolation |

## L3 — Invariants

| ID | Invariant |
|----|-----------|
| I1 | Le Worker doit tourner pour que les hooks fonctionnent — sans lui, les observations sont perdues silencieusement |
| I2 | Chaque observation appartient à exactement 1 session + 1 platform_source — pas de partage cross-platform natif |
| I3 | Les `<private>` tags excluent le contenu du corpus de façon irréversible (pas de backdoor) |
| I4 | La progressive disclosure (search → timeline → get_obs) est la seule interface MCP — pas d'accès brut direct au corpus |
| I5 | Le budget token est un hard-stop (quota_exceeded → gate bloque l'injection) — jamais de dépassement silencieux |
| I6 | SQLite est la source de vérité — ChromaDB est un index secondaire rebuildable |
| I7 | SessionEnd + Stop hooks sont le seul moment de compression AI — la session doit se terminer proprement |
| I8 | L'installation modifie les fichiers hooks de l'agent hôte — désinstaller = fichiers hooks à restaurer manuellement |

## L4 — Axes de variation

| Axe | Min | v13.3.0 | Max |
|-----|-----|---------|-----|
| Agents supportés | 1 | 7 | N (spec MCP ouverte) |
| Storage backend | SQLite seul | SQLite + ChromaDB | Server Beta : Postgres + Redis |
| Langues i18n | EN | EN + ZH + JA | N (ISO 639-1) |
| Skills satellites | 0 | ~10 | Extensible via skill API |
| Releases/mois | ~2 | ~15-20 (pic) | ∞ (cadence non bornée) |
| Budget token injection | 0 | configurable | hard-stop quota |

## L5 — Seuils et conditions d'effondrement

| Seuil | Valeur | Conséquence |
|-------|--------|-------------|
| Worker down | > 0 sessions sans Worker | Observations perdues — aucune erreur visible pour l'agent |
| Quota token | Configurable (défaut inconnu) | Hard-stop injection → session sans mémoire injectée |
| Corpus size | Dépend du stockage dispo | Dégradation perfs FTS5, puis ChromaDB |
| Release gap | > 2 semaines sans màj | Risque désync API hooks agent hôte |
| Hooks non chargés | Identique à superpowers | Skills mem-search silencieusement absents |
| Server Beta sans Postgres/Redis | Activation sans prérequis | Crash Worker — rollback Worker mode requis |

**3 effondrements système :**
- **E1 (silencieux)** : Worker down → observations perdues sans notification → corpus incomplet non détecté
- **E2 (partiel)** : Hooks non rechargés après install → mem-search disponible mais 0 observation capturée
- **E3 (dépendance)** : Release breaking sur API hooks agent hôte (Claude Code / Gemini CLI) → désync jusqu'au patch

## L6 — Couplages

| Couche | Couplage |
|--------|----------|
| Hooks → Worker | Couplage fort ⚠️ — HTTP sync requis pour chaque observation |
| Worker → SQLite | Couplage fort ⚠️ — SQLite = source de vérité, pas de fallback |
| Worker → ChromaDB | Couplage moyen ⚠️ — ChromaDB = index rebuildable, perte performance si down |
| MCP → Worker | Couplage fort ⚠️ — Skill mem-search dépend du Worker pour les requêtes |
| Agent hôte → Hooks | Couplage fort ⚠️ — hooks dans config de l'agent, migration si specs changent |
| Agents entre eux | Découplés ✅ — platform_source isolation garantie |
| Skills satellites | Découplés ✅ — indépendants du core memory pipeline |
| Server Beta | Découplé ✅ (opt-in) — Worker mode non affecté si Server Beta inactif |

## L7 — Topologie (happy path + frictions)

**Séquence happy path :**
```
install (npx claude-mem install)
→ Worker démarre (Bun, port 37777)
→ Hooks injectés dans agent config
→ Session 1 : SessionStart (inject passé) → travail → PostToolUse (capture obs) → SessionEnd (compress AI)
→ Session 2 : SessionStart (inject contexte session 1) → mem-search NL → timeline → get_observations → travail informé
```

**4 points de friction :**
- F1 : Worker à maintenir actif entre sessions (pas de daemon systemd natif — risque de perte silencieuse)
- F2 : Bun requis — chaîne d'installation plus longue que pure Node (Bun auto-install peut échouer derrière proxy)
- F3 : 271 releases en ~18 mois → API instable, hook config peut changer sans préavis
- F4 : Server Beta (Postgres + Redis) = stack DevOps non triviale — gap onboarding solo dev vs équipe

## L8 — Probabilités et incertitude

| Risque | Probabilité | Impact | Justification |
|--------|------------|--------|---------------|
| Breaking change hooks dans 6 mois | 0.85 | Élevé | 271 releases, 3 majeurs en 2026, cadence accélérée |
| Lock-in fort à l'écosystème | 0.70 | Moyen | SQLite + ChromaDB propriétaires au Worker ; export non documenté |
| Worker down en prod | 0.40 | Élevé | Aucun supervisor natif, Bun process fragile si machine redémarre |
| Dépendance upstream (Claude API) | 0.60 | Élevé | @anthropic-ai/claude-agent-sdk = breaking changes fréquents |
| Adoption long terme | 0.75 | Positif | 78k ★, Apache 2.0, momentum fort, use case unique |
| Maturité Server Beta | 0.50 | Variable | v13.1.0 = phases 4-13 event pipeline, encore en stabilisation |

**Vecteur cognitif — bilan :**
- **Abstraction** ✅ — L0-L3 bien couverts, primitives claires
- **Concrétude** ✅ — Happy path documenté, commandes copiables
- **Affect** ⚠️ — Cadence de releases anxiogène pour équipes conservatrices
- **Normativité** ⚠️ — Pas de SLA, pas de contrat de stabilité API
- **Incertitude** ⚠️ — E1 (Worker silencieux) = risque non visible, difficile à monitorer
- **Altérité** ✅ — 7 agents supportés, i18n, modes multiples
- **Cohérence** ⚠️ — Worker mode et Server Beta coexistent mais doc de migration incomplète
