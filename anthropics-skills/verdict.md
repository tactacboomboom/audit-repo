# Verdict PM — anthropics/skills

## Scores (sur 10)
| Dimension | Score | Justification |
|---|---|---|
| **Pertinence pour le skill `architecture-anthropic`** | **10/10** | C'est LA référence officielle ; tout ce que `architecture-anthropic` cherche à cataloguer vit ici. |
| **Maturité prod** | **9/10** | Spec stabilisée, 138k stars, 36 commits sur main (signe de maturité), CI inférée via `skills-ref`. -1 pour `allowed-tools` expérimental. |
| **Facilité onboarding** | **7/10** | Template ultra-minimal, mais spec hors-repo et linter dans un autre repo = friction. |

## Forces
| | Titre | Description |
|---|---|---|
| ⚓ | **Spec canonique formelle** | Contraintes typées (64/1024/500 chars), name format strict, validation outillée |
| 🎯 | **Pattern description normalisé** | `"<Action>. Use when X, Y, Z."` + `Do NOT trigger when ...` documenté par l'exemple |
| 🪜 | **Progressive disclosure** | Frontmatter (boot) → body (activation) → resources (à la demande) — 3 niveaux clairs |
| 🧪 | **Eval harness officiel** | skill-creator embarque 8 schémas JSON + `improve_description.py` pour optim empirique |
| 📦 | **Marketplace découplé** | `.claude-plugin/marketplace.json` groupe les skills sans coupler leur contenu |
| 🔒 | **Isolation par dossier** | 1 skill = 1 dossier auto-suffisant, pas de dépendance croisée |

## Faiblesses / Risques
| | Titre | Description + impact |
|---|---|---|
| 🌐 | **Spec hors-repo** | `spec/agent-skills-spec.md` n'est qu'un redirect vers agentskills.io → discoverability faible, dépendance réseau |
| 🧰 | **Linter externe** | `skills-ref` vit dans `agentskills/agentskills`, pas dans `anthropics/skills` → fragmentation outillage |
| 🧪 | **`allowed-tools` expérimental** | Champ marqué non-stable → ne pas en faire dépendre la sécurité |
| 📚 | **Pas de CONTRIBUTING.md** | Contributeurs externes n'ont pas de guide → friction PR |
| ⚠️ | **Pas de garantie d'API JS/Python** | Le runtime des skills (côté Claude Code) n'est pas dans ce repo → l'évolution upstream peut casser |

## Matrice Use Cases

### ✅ Oui — usages appropriés
| Use case | Pourquoi |
|---|---|
| Cataloguer l'archi officielle (objet du skill `architecture-anthropic`) | C'est la source primaire |
| Apprendre à rédiger un YAML frontmatter conforme | Spec + 17 exemples réels |
| Apprendre à écrire une description qui déclenche bien | xlsx, docx, claude-api sont des cas d'école |
| Comprendre la progressive disclosure | Documentée + visible dans skill-creator |

### ❌ Non / Attendre — usages risqués
| Use case | Pourquoi |
|---|---|
| Implémenter un runtime de skills | Le runtime n'est pas dans ce repo |
| Distribuer commercialement les document-skills (xlsx/docx/pptx/pdf) | License "Proprietary, see LICENSE.txt" |
| Se reposer sur `allowed-tools` pour la sécurité | Champ explicitement expérimental |
| Forker la spec | Mieux vaut contribuer à agentskills.io |

## Roadmap inférée (depuis l'absence de ROADMAP.md)
| Feature | Statut | Impact |
|---|---|---|
| Spec frontmatter `name`, `description`, `license`, `compatibility`, `metadata` | ✅ stable | Fondations |
| Spec `allowed-tools` | 🟡 expérimental | À surveiller |
| Validation via `skills-ref` | ✅ stable | Lint reproductible |
| Eval harness (skill-creator) | ✅ disponible | Optim empirique des descriptions |
| Marketplace plugins | ✅ stable | Distribution |

## Recommandation finale

**Pourquoi c'est pertinent maintenant pour le skill `architecture-anthropic` :**
Ce repo est précisément la matière première dont le skill `architecture-anthropic` a besoin pour exister. Le skill `architecture-anthropic` est défini comme "layer markdown drive-only qui catalogue l'archi officielle Anthropic et sert de checklist d'audit" — or `anthropics/skills` EST cette archi officielle, sous forme exécutable et auditable. Le NOTES.md issu de cet audit peut servir directement de référentiel pivot.

**Action recommandée :**
1. Ne PAS cloner le repo entier (lourd) — pinner les URLs raw GitHub des fichiers clés
2. Adopter le pattern de description Anthropic mot-pour-mot pour les futurs skills personnels : `"<Action concrète>. Use this skill when <liste explicite>."` avec `"Do NOT trigger when ..."` si négation utile
3. Utiliser `skill-creator/scripts/improve_description.py` comme oracle pour optimiser les descriptions personnelles
4. Conditions de passage en prod du skill `architecture-anthropic` :
   - NOTES.md exhaustif sur les 6 champs frontmatter
   - Checklist d'audit dérivée des 8 invariants du fmath
   - Re-fetch trimestriel pour détecter changements de spec
