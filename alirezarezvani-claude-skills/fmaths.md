# Fmaths — alirezarezvani/claude-skills

> Analyse formelle 8 couches · Généré le 2026-05-26

---

## L0 — Ontologie (primitives non-redondantes)

| Primitive | Définition |
|---|---|
| **Skill** | Instruction exécutable encapsulée dans SKILL.md — grain = 1 intention |
| **Persona** | Identité + jugement — filtrent COMMENT un agent raisonne |
| **Agent** | Compositeur de Persona + Skills sur un domaine métier |
| **Tool** | Script Python stdlib (0 dépendance) attaché à un Skill |
| **Orchestration** | Protocole de coordination Persona ↔ Skills ↔ Agents entre phases |
| **Platform** | Cible de déploiement (Claude Code, Cursor, Gemini CLI, Aider…) |
| **Domain** | Cluster fonctionnel (engineering, product, marketing, c-level…) |

7 primitives. Fermées, non-redondantes, génératives.

---

## L1 — Ensembles et relations

```
Skill ∈ Domain
Domain ⊆ Agent (un agent agrège plusieurs domaines)
Persona → filtre(Agent)
Orchestration coordonne(Persona × Skills → Phase)
Tool est-attaché-à(Skill) [optionnel]
Platform consomme(Skill | Agent)

Skills : ~329  (répartis sur ~12 Domains)
Tools  : ~402  (stdlib Python uniquement)
Agents : ~10 composites (engineering, product, marketing…)
Personas : 3+ (Startup CTO, Growth Marketer, Solo Founder)
Platforms : 12+ (Claude Code, Cursor, Aider, Windsurf, Gemini CLI…)
```

**Relations critiques :**
- Skill ↛ Skill (pas de linéage entre skills — isolation forte)
- Persona ↛ Document (les personas ne produisent pas de traçabilité)
- Domain → SKILL.md (seul artefact persistant par skill)

---

## L2 — Logique et tensions

| Connecteur | Application |
|---|---|
| AND | Persona + Skills = agent opérationnel (les deux requis) |
| OR | Skills s'activent indépendamment (pas de dépendance inter-skill) |
| XOR | 1 persona active par prompt — exclusion mutuelle |
| → | Orchestration : Phase N → Hand Off → Phase N+1 |

**Tensions identifiées :**
- `T1` Skills sont **isolés** — aucun mécanisme de linéage entre eux. Viola A₅ traçabilité si on veut nilpotence globale.
- `T2` **329 skills** = richesse ET risque de dispersion. Sans filtre, le Solo Founder se noie.
- `T3` Orchestration est **procédurale** (Skill Chain) OU **opportuniste** (persona switching). Pas de garantie formelle de convergence.
- `T4` Platform-agnostic = force ET faiblesse : adaptation `convert.sh` déléguée à l'utilisateur.

---

## L3 — Invariants

| ID | Invariant |
|---|---|
| I1 | Chaque Skill = 1 SKILL.md — grain immuable |
| I2 | 0 dépendance externe pour les Tools (stdlib Python only) |
| I3 | 1 seule Persona active par prompt (exclusion mutuelle) |
| I4 | MIT License — réutilisation libre, modification libre |
| I5 | Context forward : lors d'un handoff, le contexte précédent se transmet |
| I6 | Skills stack freely — pas de conflit de charge possible |

---

## L4 — Axes de variation

| Axe | Min | Max | État actuel |
|---|---|---|---|
| Couverture domaines | 1 domain | 12+ domains | ✅ 12 domains couverts |
| Profondeur par skill | 1 ligne instruction | 50+ lignes + scripts | Mixte : léger→dense |
| Maturité orchestration | Ad hoc prompt | Protocole 5 étapes formalisé | ⚠️ v2.8.4, récent |
| Conformité Anthropic | Non-conforme | name+description seulement | ⚠️ frontmatter étendu (non-standard) |
| Linéage documentaire | 0 (actuel) | LINEAGE.md par skill | ❌ absent |
| Support multi-platform | Claude Code only | 12 plateformes | ✅ via convert.sh |

---

## L5 — Seuils et stabilité

| Seuil | Valeur critique | Risque |
|---|---|---|
| Surcharge cognitive | >20 skills actifs simultanément | Persona switching becomes noise |
| Breaking changes | ~10 releases/mois observés | Pins de version nécessaires |
| Conformité frontmatter | Champs supplémentaires (type, version…) | Incompatibilité avec marketplace Anthropic officiel |
| Linéage manquant | 0 skills avec LINEAGE.md | Opacité totale du DAG de provenance |
| Onboarding friction | `/plugin install` → 1 commande | ✅ sous le seuil d'abandon |

---

## L6 — Catégories (cohérence interne)

| Couche | Contenu | Couplage |
|---|---|---|
| Instruction | SKILL.md + frontmatter | ✅ découplé par design |
| Exécution | Python Tools (~402) | ✅ stdlib-only, 0 coupling |
| Identité | Personas (3+) | ⚠️ peu documentées |
| Coordination | Orchestration protocol | ⚠️ récent, en évolution |
| Déploiement | Platform scripts | ✅ isolé dans scripts/ |
| Gouvernance | Standards/, templates/ | ⚠️ partiellement formalisé |

Audit couplages : Skills ↔ Tools = ✅ faible / Personas ↔ Skills = ⚠️ implicite / Orchestration ↔ Domaines = ⚠️ non formalisé

---

## L7 — Topologie (chemin de moindre résistance)

**Happy path :**
```
1. /plugin install engineering-skills@claude-code-skills      (30s)
2. Choisir une Persona dans agents/personas/                  (1 min)
3. Invoquer /skill domain/skill-name                          (immédiat)
4. Si cross-domain → orchestration/ORCHESTRATION.md           (5 min lecture)
5. Solo Sprint : CTO → PO → Founder (switch persona)          (par phase)
```

**Nœuds de friction :**
- F1 : 329 skills → sélection non guidée (pas de recommandation par cas d'usage)
- F2 : Frontmatter étendu → incompatibilité potentielle avec Claude Code marketplace officiel
- F3 : Orchestration sans linéage → handoff perd la traçabilité documentaire
- F4 : Windows : `convert.sh` est bash → nécessite WSL ou Git Bash

---

## L8 — Probabilités

| Dimension | Estimation | Source |
|---|---|---|
| P(lock-in plateforme) | 15% | MIT + multi-platform, faible |
| P(breaking change impactant) | 40%/mois | ~10 releases récentes, actif |
| P(adoption communauté) | 85% maintenu | 16.2k ★, 2.2k forks, 4 issues |
| P(conformité Anthropic officielle) | 30% tel quel | Frontmatter non-standard |
| P(nilpotence globale sans refactor) | 5% | Linéage absent, pas de chaîne formelle |

**Vecteur cognitif — bilan :**
- Abstraction : ✅ fort (Personas, Orchestration bien abstraits)
- Concrétude : ✅ très fort (402 outils Python concrets, exemples d'usage)
- Affect : ⚠️ absent (pas de signal émotionnel/motivation dans les skills)
- Normativité : ⚠️ implicite (pas de DoR/DoD, pas de critères de done formels)
- Incertitude : ⚠️ non signalée (aucun "⚠️" dans les skills eux-mêmes)
- Altérité : ✅ fort (12 plateformes, multi-rôles, multi-domaines)
- Cohérence : ⚠️ partielle (orche. récent, linéage absent, frontmatter non-standard)
