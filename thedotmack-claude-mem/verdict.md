---
name: claude-mem-verdict
description: Évaluation thedotmack/claude-mem v13.3.0 — score 8.6/10, forces/faiblesses, matrice use-cases prothèse mnésique, roadmap. Charger pour décision d'adoption ou préparer une recommandation.
---

# Verdict PM — thedotmack/claude-mem

## Score 3 dimensions

| Dimension | Score | Justification |
|---|---|---|
| Pertinence PM (prothèse mnésique pour agent) | 9.5/10 | Unique : seul outil qui résout le problème de l'oubli inter-sessions de façon complète et automatique. Use case central = memory agent. |
| Maturité prod | 8/10 | v13.3.0, 271 releases, Apache 2.0, 78k ★ — mais cadence accélérée et Worker non supervisé = risque opérationnel |
| Facilité onboarding | 8.5/10 | `npx claude-mem install` = 1 commande. Happy path très fluide. Friction arrive sur la config avancée et le monitoring Worker. |

**Score global : 8.6/10**

---

## Forces

| | Titre | Description |
|---|---|---|
| ✅ | Prothèse mnésique complète | Seul outil qui capture → compresse → injecte le contexte cross-session de façon entièrement automatique, sans friction pour l'agent |
| ✅ | Progressive disclosure token-efficient | Pipeline 3 couches (search → timeline → get_obs) = ~10× économie de tokens vs injection brute |
| ✅ | Multi-agent universel | 7 agents supportés (Claude Code, Gemini, OpenCode, Codex, Windsurf, Claude Desktop, OpenClaw) — migration sans perte de mémoire |
| ✅ | Privacy by design | Balises `<private>` excluent le contenu sensible de façon irréversible — pas de fuite silencieuse |
| ✅ | Hybrid search robuste | FTS5 + ChromaDB vecteurs = rappel sémantique + exact-match simultanés, citations par ID |
| ✅ | Écosystème skills satellite | Skills optionnels (design-is, weekly-digests, babysit, wowerpoint...) — la mémoire devient une plateforme |

---

## Faiblesses / Risques

| | Titre | Description + Impact |
|---|---|---|
| ⚠️ | Worker sans supervision native | Process Bun non daemonisé — redémarrage machine = Worker down = observations perdues en silence. Impact : corpus incomplet sans alerte |
| ⚠️ | Cadence de releases non bornée | 271 releases en ~18 mois, jusqu'à 7/10 jours. Impact : hook API instable, upgrade auto peut casser silencieusement le pipeline |
| ⚠️ | Lock-in SQLite + ChromaDB | Export du corpus non documenté. Impact : migration vers un autre système = re-capture from scratch |
| ⚠️ | Server Beta prématuré | Phases 4-13 event pipeline en cours de stabilisation (v13.1.0). Impact : Postgres + Redis = stack DevOps non triviale pour solo dev |
| 🔴 | Perte d'observations silencieuse | Worker down, crash session non propre, hooks non rechargés = corpus troué sans notification. Impact : fausse confiance dans la mémoire |

---

## Matrice Use Cases

### ✅ Oui — Usage approprié

| Use Case | Pourquoi |
|---|---|
| Prothèse mnésique pour agent PM | Résout exactement le problème : continuité de contexte cross-session, mémoire des décisions et des blockers |
| Projet long (> 1 semaine, > 50 sessions) | La valeur du corpus croît avec le temps — indispensable pour ne pas réexpliquer l'historique |
| Onboarding nouveau collaborateur agent | `mem-search` permet à un agent de retrouver l'historique d'un projet sans re-lire toute la codebase |
| Multi-agent sur même projet | Platform isolation garantit que Claude Code et Codex ne polluent pas leur mémoire respective |

### ❌ Attendre / Non — Usage inapproprié ou risqué

| Use Case | Pourquoi |
|---|---|
| Projet B2B à SLA strict | Pas de supervision Worker native, perte silencieuse possible — trop risqué en production sensible |
| Environnement sans contrôle du Worker | Serveur partagé, machine redémarrée régulièrement = Worker instable = corpus non fiable |
| Intégration dans pipeline CI/CD | Les hooks sont conçus pour sessions interactives, pas pour batch — comportement non spécifié en CI |
| Adoption sans version épinglée | 271 releases → risque de régression silencieuse à chaque update auto du hook |

---

## Roadmap

| Feature | Statut | Impact |
|---|---|---|
| Server Beta (Postgres + BullMQ) | ✅ v13.0.0 opt-in, stabilisation en cours | Scalabilité enterprise, multi-worker |
| Event pipeline complet (phases 4-13) | ✅ v13.1.0 | Observabilité temps réel des observations |
| Codex native hooks | ✅ v12.7.0 | Parité OpenAI Codex avec Claude Code |
| OAuth keychain reader | ✅ v12.6.0 | Sécurité accrue multi-env |
| Skills satellite (design-is, weekly-digests) | ✅ v13.3.0 | Mémoire → plateforme |
| Daemon/supervisor natif | ⏳ Non annoncé | Nécessaire pour robustesse prod |
| Export corpus | ⏳ Non annoncé | Indispensable pour migration |
| V14 (probable H2 2026) | ⏳ Non annoncé | Attendre CHANGELOG avant upgrade majeur |

---

## Recommandation finale

**claude-mem est la prothèse mnésique de référence pour tout agent de code qui travaille sur des projets longs.** Le problème qu'il résout — l'oubli inter-sessions — est structurel à tous les LLM actuels, et aucun concurrent ne propose une solution aussi complète, aussi automatique, et aussi bien intégrée dans l'écosystème Claude. La relicence Apache 2.0, les 78k étoiles, et la diversité des agents supportés confirment que ce projet a passé le stade du proof-of-concept.

**Dans le contexte prothèse PM** : c'est le chaînon manquant entre une série de sessions isolées et un vrai projet suivi. Un agent qui sait ce qu'il a déjà tenté, qui reconnaît les patterns d'échec, qui réinjecte les décisions de la semaine passée — c'est une différence de nature sur la qualité du travail produit.

**Action recommandée :** adopter immédiatement pour tout projet où la continuité de contexte est critique. Épingler la version (`npx claude-mem@13.3.0 install`). Mettre en place un monitoring simple du Worker (health check port 37777 toutes les 5 minutes). Ne pas activer le Server Beta avant d'avoir Postgres + Redis en place. Pour les projets sensibles : tester les balises `<private>` sur les données confidentielles avant de mettre en production.
