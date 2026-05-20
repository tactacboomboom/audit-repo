# Fmaths — anthropics/skills

## L0 — Ontologie (primitives non-redondantes)
1. **Skill** — dossier auto-suffisant contenant un contrat de comportement pour Claude
2. **SKILL.md** — point d'entrée unique : YAML frontmatter + corps markdown
3. **Frontmatter** — métadonnées chargées au boot (name, description, license, compatibility, metadata, allowed-tools)
4. **Description** — sonde sémantique qui pilote l'activation
5. **Body** — instructions chargées à l'activation (< 5000 tokens recommandés)
6. **Resource** — fichier sous scripts/ | references/ | assets/ chargé à la demande
7. **Marketplace** — manifest qui regroupe N skills en plugins distribuables
8. **Eval harness** — boucle empirique de mesure de qualité d'un skill

## L1 — Ensembles et relations
- `Skills = {algorithmic-art, brand-guidelines, ..., xlsx}` (17 éléments)
- `Plugins = {document-skills, example-skills, claude-api}` (3 éléments)
- `Frontmatter_fields = {name*, description*, license, compatibility, metadata, allowed-tools}` (* = required)
- `Resources(skill) = scripts(skill) ∪ references(skill) ∪ assets(skill)`
- Relations : `belongs_to: Skills → Plugins` (M:1) · `parent_dir_name(skill) ≡ frontmatter.name` (égalité forcée)

## L2 — Logique et tensions
- **AND** : `valid(skill) ⟺ has(SKILL.md) ∧ valid(frontmatter) ∧ name ≡ parent_dir`
- **OR** : description longue (xlsx, docx) **OU** description courte (brand-guidelines, slack-gif-creator) — les deux sont officiellement valides
- **XOR caché** : open-source (Apache-2.0, license absent) ⊕ source-available ("Proprietary. LICENSE.txt has complete terms")
- **Tension #1** : description courte ↔ description longue. Courtes (~150 chars) plus lisibles ; longues (~800 chars) plus précises pour le routeur. Anthropic utilise les deux selon l'ambiguïté du domaine.
- **Tension #2** : progressive disclosure ↔ self-containment. Plus on disclose, plus on doit naviguer ; moins on disclose, plus le SKILL.md gonfle.

## L3 — Invariants (I1...In)
- **I1** : un skill = un dossier = un SKILL.md à la racine
- **I2** : `parent_dir_name ≡ frontmatter.name` (vérifié par `skills-ref validate`)
- **I3** : `name` ∈ `[a-z0-9-]{1,64}`, pas de hyphen extrémal, pas de `--`
- **I4** : `description` ∈ `[1, 1024]` chars
- **I5** : références de fichiers en chemins relatifs, profondeur ≤ 1 depuis SKILL.md
- **I6** : `name` + `description` = budget ~100 tokens au boot, multiplié par N skills installés (coût linéaire)
- **I7** : pas de champ `type` ni `status` dans la spec officielle (à ne pas inventer)
- **I8** : `allowed-tools` est expérimental → ne pas en dépendre pour la sécurité

## L4 — Axes de variation
| Axe | Min | État actuel (Anthropic) | Max |
|---|---|---|---|
| Longueur description | 1 char | 150–900 chars | 1024 chars |
| Profondeur arborescence skill | SKILL.md seul | scripts+references+assets | + agents/ + eval-viewer/ (skill-creator) |
| Catégorisation | aucune | 3 plugins via marketplace.json | taxonomie multi-niveau |
| Licence | Apache-2.0 ouvert | mix (open + proprietary) | tout proprietary |
| Style description | très court | "Action. Use when X, Y, Z." | longue + "Do NOT trigger when ..." |
| Couverture validation | manuelle | `skills-ref validate` (linter externe) | + evals quantitatives (`run_eval.py`) |

## L5 — Seuils et stabilité
- **Seuil description** : 1024 chars (hard cap spec). Dépassement = invalide.
- **Seuil name** : 64 chars (hard cap spec).
- **Seuil compatibility** : 500 chars.
- **Seuil tokens body** : ~5000 tokens recommandés (soft). Au-delà : éclatement obligatoire vers references/.
- **Seuil lignes SKILL.md** : 500 lignes (soft). Au-delà : risque de noyade attentionnelle.
- **Seuil profondeur refs** : 1 niveau depuis SKILL.md. Au-delà : chaînes de références déconseillées.
- **Effondrement attendu** : si la description omet le QUAND, le routeur d'activation tombe sous le bruit → faux négatifs systématiques.

## L6 — Catégories et couplages
| Couche | Statut couplage |
|---|---|
| Couche spec (`spec/`) | Découplée ✅ (vit sur agentskills.io) |
| Couche template (`template/`) | Découplée ✅ (1 fichier) |
| Couche skills (`skills/*`) | Indépendance forte ✅ (chaque skill auto-suffisant) |
| Couche marketplace (`.claude-plugin/marketplace.json`) | Couplage souple ✅ (référence par chemin, pas par contrat) |
| Couche eval (skill-creator/scripts/) | Couplage interne ⚠️ (8 schémas JSON inter-dépendants — voir references/schemas.md) |

## L7 — Topologie (chemin de moindre résistance)
**Happy path création d'un skill** :
1. `cp -r template/ my-skill/` (point de départ minimal)
2. Édit du frontmatter (name = dossier parent, description = "Action. Use when X, Y, Z.")
3. Édit du body markdown
4. `skills-ref validate ./my-skill` (linter spec)
5. (Optionnel) Création d'evals via skill-creator : `evals/evals.json` → `run_eval.py`
6. Installation locale ou publication via plugin

**Nœuds de friction** :
- Friction #1 : la spec n'est PAS dans le repo (redirect vers agentskills.io) → discoverability faible
- Friction #2 : aucun lint local sans installer `skills-ref` (dépendance externe à `agentskills/agentskills`)
- Friction #3 : `improve_description.py` (le meilleur outil pour optimiser une description) est enfoui dans `skill-creator/scripts/` plutôt qu'exposé comme CLI
- Friction #4 : pas de CONTRIBUTING.md → contributeurs perdus

## L8 — Probabilités et incertitudes
| Variable | Probabilité | Justification |
|---|---|---|
| P(adoption stable) | très haute | 138k stars, repo officiel Anthropic |
| P(breaking spec change court terme) | très faible | spec hébergée, versionnée, stabilisée |
| P(breaking sur `allowed-tools`) | médium-haute | champ explicitement marqué expérimental |
| P(extension du frontmatter avec nouveaux champs) | médium | `metadata` libre = soupape de pression |
| P(lock-in fournisseur) | faible | spec ouverte, format markdown standard |
| P(rupture upstream Claude Code) | très faible | format pivot officiel Anthropic |
| Maturité communauté | élevée | 138k stars, 16.3k forks, 614 PRs ouvertes |

## Vecteur cognitif — bilan
- **Abstraction** : OK — spec formelle propre, contraintes typées
- **Concrétude** : OK — 17 skills exemple + scripts opérationnels
- **Affect** : faible — ton corporate Anthropic, peu d'incarnation
- **Normativité** : forte — bornes dures (64, 1024, 500), interdits (no hyphens, no consecutive)
- **Incertitude** : médium — `allowed-tools` expérimental signalé
- **Altérité** : OK — taxonomie 3 plugins + marketplace ouverte
- **Cohérence** : très forte — tous les SKILL.md observés respectent strictement la spec
