# NOTES.md — anthropics/skills pour `architecture-anthropic`

> Layer markdown drive-only — catalogue de l'archi officielle Anthropic + checklist d'audit pour SKILL.md.
> Source : https://github.com/anthropics/skills (audit du 2026-05-20).
> Spec officielle pivot : https://agentskills.io/specification.

---

## 1. Format des SKILL.md officiels — YAML frontmatter exact

### Tableau exhaustif des 6 champs (officiels d'après la spec)

| Champ | Required | Contrainte exacte | Présent dans les SKILL.md d'Anthropic ? |
|---|---|---|---|
| `name` | **Oui** | 1–64 chars, `[a-z0-9-]`, pas d'hyphen extrémal, pas de `--`, **doit matcher le dossier parent** | 100% des skills |
| `description` | **Oui** | 1–1024 chars, non-vide, "QUOI + QUAND" | 100% des skills |
| `license` | Non | string libre (nom de licence ou ref à un fichier bundlé) | ~10/12 skills observés |
| `compatibility` | Non | ≤500 chars, indique pré-requis env | Aucun des skills officiels ne l'utilise (rare) |
| `metadata` | Non | Map clé→valeur libre (auteur, version, …) | Aucun n'expose `metadata` dans SKILL.md (utilisé dans marketplace.json) |
| `allowed-tools` | Non | String space-separated, ex: `Bash(git:*) Bash(jq:*) Read`. **EXPÉRIMENTAL** | Aucun des skills officiels ne l'utilise |

**Champs INVENTÉS qui n'existent PAS dans la spec officielle** (à ne pas utiliser pour rester conforme) :
- `type` — n'existe pas
- `status` — n'existe pas
- `version` — n'existe qu'à l'intérieur de `metadata` (sous forme `metadata.version: "1.0"`)
- `author` — pareil, sous `metadata.author`
- `tags`, `category`, `keywords` — n'existent pas (la catégorisation passe par le marketplace, pas par le frontmatter)

### Format YAML — gabarit minimal officiel (template/SKILL.md du repo)
```yaml
---
name: template-skill
description: Replace with description of the skill and when Claude should use it.
---

# Insert instructions below
```
C'est tout. Deux champs. C'est le strict minimum, et c'est ce qu'Anthropic recommande comme point de départ.

### Format YAML — gabarit étendu (spec)
```yaml
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
compatibility: Requires Python 3.14+ and uv
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(git:*) Bash(jq:*) Read
---
```

---

## 2. Conventions de description — règles d'écriture observées

### Pattern canonique Anthropic
**Formule générique** : `"<Action concrète au présent>. Use this skill when <liste explicite de déclencheurs>."`

Exemples directs observés :
- pdf : `"Use this skill whenever the user wants to do anything with PDF files."` + énumération des actions + `"If the user mentions a .pdf file or asks to produce one, use this skill."`
- mcp-builder : `"Guide for creating high-quality MCP servers ... Use when building MCP servers to integrate external APIs, whether in Python (FastMCP) or Node/TypeScript (MCP SDK)."`
- skill-creator : `"Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals, ..."`

### Longueur observée — distribution réelle
| Plage | Skills | Exemples |
|---|---|---|
| Très court (~120–250 chars) | brand-guidelines, slack-gif-creator, webapp-testing | descriptions denses, monobloc |
| Médium (~300–500 chars) | skill-creator, mcp-builder, frontend-design, theme-factory | pattern Action + Use when |
| Long (~700–1024 chars) | pdf, docx, xlsx, claude-api, internal-comms | énumération exhaustive de déclencheurs + Do NOT |

**Heuristique** : plus le domaine est ambigu (ex. xlsx vs Google Sheets vs database vs CSV), plus la description doit être longue pour discriminer. Pour un domaine net (slack-gif-creator), la version courte suffit.

### Trois techniques avancées (utilisées par Anthropic, conformes à la spec)

#### Technique A — Énumération d'extensions et termes parlants
Format : citer les extensions de fichiers ET les synonymes courants utilisés par l'humain.
```yaml
# docx
description: "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', ..."
```
Pourquoi : le routeur d'activation ne sait pas que "deck" = `.pptx`. Il faut l'expliciter.

#### Technique B — Négation explicite (`Do NOT trigger when …`)
Format : ajouter en fin de description un paragraphe qui liste les cas qui NE doivent PAS déclencher.
```yaml
# xlsx
description: "... Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
```
Pourquoi : empêche les faux positifs sur les domaines voisins. La spec ne mentionne pas explicitement cette technique, mais Anthropic l'emploie systématiquement sur les skills à fort risque de chevauchement (xlsx vs Google Sheets, docx vs PDF).

#### Technique C — Marqueurs sémantiques en MAJUSCULES
Format : utiliser `TRIGGER when:` / `SKIP:` dans le corps de la description.
```yaml
# claude-api
description: |
  Build, debug, and optimize Claude API / Anthropic SDK apps...
  TRIGGER when: code imports `anthropic`/`@anthropic-ai/sdk`; user asks for the Claude API...
  SKIP: file imports `openai`/other-provider SDK, filename like `*-openai.py`...
```
Pourquoi : aide le routeur à pondérer triggers vs anti-triggers. Réservé aux skills très techniques.

### Trois points de vue stylistiques observés
- **2e personne / impératif** : "Use this skill when..." → majorité des cas
- **3e personne descriptive** : "Toolkit for ..." → brand-guidelines, theme-factory, webapp-testing
- **1ère personne (rare, contextuel)** : internal-comms — `"A set of resources to help me write..."` (un employé Anthropic, "me" = lui)

### Mots-clés de trigger récurrents
- Verbes d'action : `create`, `read`, `edit`, `manipulate`, `extract`, `convert`, `generate`, `apply`, `build`
- Déclencheurs nominaux : `file`, `document`, `presentation`, `spreadsheet`, `report`, `template`
- Connecteurs : `Use when ...`, `Triggers include ...`, `If the user mentions ...`, `Also use when ...`
- Anti-déclencheurs : `Do NOT use for ...`, `Do NOT trigger when ...`, `SKIP: ...`

---

## 3. Structure interne d'un skill

### Spec officielle (verbatim)
```
skill-name/
├── SKILL.md          # OBLIGATOIRE : frontmatter + instructions
├── scripts/          # OPTIONNEL : code exécutable (Python/Bash/JS)
├── references/       # OPTIONNEL : docs additionnelles (REFERENCE.md, FORMS.md, ...)
├── assets/           # OPTIONNEL : templates, images, schémas
└── ...               # n'importe quoi d'autre
```

### Cas réel le plus complet — `skill-creator`
```
skill-creator/
├── SKILL.md
├── LICENSE.txt
├── agents/              # sous-agents spécialisés (executor, grader, comparator, analyzer)
├── assets/              # ressources statiques
├── eval-viewer/         # HTML viewer pour les résultats d'éval
├── references/
│   └── schemas.md       # 8 schémas JSON pour le harness d'éval
└── scripts/
    ├── __init__.py
    ├── aggregate_benchmark.py
    ├── generate_report.py
    ├── improve_description.py   # ⭐ outil officiel d'optim de description
    ├── package_skill.py
    ├── quick_validate.py
    ├── run_eval.py
    ├── run_loop.py
    └── utils.py
```

### Règles de structuration observées
- 1 skill = 1 dossier auto-suffisant (pas de dépendance entre skills)
- LICENSE.txt vit DANS le skill (pas à la racine du repo)
- Chaque sous-dossier a un rôle sémantique strict : `scripts/` = exécutable, `references/` = lecture, `assets/` = statique, `agents/` = délégation
- Pas de `tests/` dédié — les tests vivent dans `evals/` (convention skill-creator)
- Pas de `docs/` séparé — la doc est soit dans SKILL.md, soit dans `references/`
- Profondeur ≤ 1 depuis SKILL.md (spec)

### Convention de nommage des fichiers references/
- `REFERENCE.md` (majuscules) — référence technique principale
- `FORMS.md` — formulaires / structures de données
- `<domain>.md` — fichiers spécifiques (`finance.md`, `legal.md`, `schemas.md`)

---

## 4. CLAUDE.md à l'intérieur d'un skill

### Constat de l'audit
**Aucun CLAUDE.md n'a été observé à l'intérieur des 17 skills officiels Anthropic.** Ni à la racine du repo (pas de CLAUDE.md racine non plus).

### Interprétation
Le SKILL.md JOUE le rôle de CLAUDE.md pour la portée du skill. La spec considère que le corps markdown du SKILL.md *est* le contrat d'instructions pour Claude lorsque le skill est actif. Un CLAUDE.md séparé serait redondant et créerait une ambiguïté sur l'ordre de chargement.

### Implication pour `architecture-anthropic`
Ne pas inventer la convention "CLAUDE.md dans un skill". Si vous voulez fournir des instructions à Claude au sein d'un skill, mettez-les dans le corps de SKILL.md (sous l'en-tête) ou dans un fichier `references/` chargé à la demande. Le seul CLAUDE.md qui ait du sens est celui à la racine d'un *repo de projet*, qui pré-existe à l'activation des skills.

---

## 5. Catégorisation / taxonomie des skills officiels

### Pas de taxonomie dans le frontmatter
La spec n'a aucun champ `category` / `tags`. La catégorisation passe **uniquement** par le manifest plugin.

### Le manifest : `.claude-plugin/marketplace.json`
```json
{
  "name": "anthropic-agent-skills",
  "owner": {"name": "Keith Lazuka", "email": "klazuka@anthropic.com"},
  "metadata": {"description": "Anthropic example skills", "version": "1.0.0"},
  "plugins": [
    {"name": "document-skills",  "skills": ["xlsx","docx","pptx","pdf"]},
    {"name": "example-skills",   "skills": ["algorithmic-art","brand-guidelines","canvas-design","doc-coauthoring","frontend-design","internal-comms","mcp-builder","skill-creator","slack-gif-creator","theme-factory","web-artifacts-builder","webapp-testing"]},
    {"name": "claude-api",       "skills": ["claude-api"]}
  ]
}
```

### Trois plugins = trois axes implicites
| Plugin | Axe | Caractéristique commune |
|---|---|---|
| `document-skills` (4 skills) | Manipulation de fichiers métier | Tous source-available (`Proprietary. LICENSE.txt`) |
| `example-skills` (12 skills) | Démonstrations & créatif | Tous Apache-2.0 ouverts |
| `claude-api` (1 skill) | Méta — comment utiliser l'API Claude | Skill solitaire, méta-skill |

### Catégorisation décrite en prose dans le README
- Creative & Design
- Development & Technical
- Enterprise & Communication
- Document Skills

Ces étiquettes n'apparaissent ni dans la spec ni dans marketplace.json — c'est de la doc marketing. Pour `architecture-anthropic`, ne pas en faire des champs typés.

### Champ `strict` dans marketplace.json
`"strict": false` apparaît sur chaque plugin. Non documenté dans la spec mais présent — probablement une option de validation. À investiguer si l'on veut créer un marketplace personnel.

---

## 6. Gouvernance et qualité — linting, eval, tests

### Lint officiel — `skills-ref validate`
Outil dans `agentskills/agentskills/skills-ref` (repo SÉPARÉ d'anthropics/skills).
```bash
skills-ref validate ./my-skill
```
Vérifie : conformité YAML frontmatter, contraintes name/description, structure du dossier. C'est le seul lint officiel.

### Eval harness — `skill-creator/scripts/`
Le skill `skill-creator` *est* l'outillage de qualité. 8 scripts Python :
| Script | Rôle |
|---|---|
| `run_eval.py` | Exécute un eval set sur un skill |
| `aggregate_benchmark.py` | Agrège les résultats multi-run |
| `improve_description.py` | **Boucle d'optim auto de la description** (génère 20 prompts mixtes, mesure le triggering, propose des refactos) |
| `quick_validate.py` | Validation rapide (probablement délégation à `skills-ref`) |
| `package_skill.py` | Packaging pour distribution |
| `run_loop.py` | Boucle itérative complète |
| `generate_report.py` | Rapport HTML |
| `aggregate_benchmark.py` | Stats croisées |

### 8 schémas JSON canoniques (`references/schemas.md`)
- `evals.json` — cas d'éval (prompts, attentes, fichiers d'entrée)
- `history.json` — historique des versions en mode Improve
- `grading.json` — sortie du grader (preuves, métriques, suggestions)
- `metrics.json` — sortie de l'executor (tool usage, fichiers créés, erreurs)
- `timing.json` — données wall-clock (durée, tokens)
- `benchmark.json` — comparatif multi-run with/without skill
- `comparison.json` — sortie du comparator (winner, scores rubrique)
- `analysis.json` — analyse post-hoc avec priorisation des améliorations

### Pas de CI publique observée
Pas de `.github/workflows/` visible. Le repo n'expose pas son pipeline de CI. La validation se fait probablement en interne Anthropic.

### Pas de CONTRIBUTING.md, pas de CODE_OF_CONDUCT.md
Surprenant pour un repo à 138k stars. Indique soit que la communauté n'est pas le moteur du repo (Anthropic publie, communauté consomme), soit que ces fichiers sont en backlog.

---

## 7. Checklist d'audit pour un SKILL.md (dérivée des 8 invariants fmath)

Pour auditer un SKILL.md tiers (ou un personnel), cocher :

- [ ] **I1** Le dossier contient bien un fichier `SKILL.md` à la racine
- [ ] **I2** `frontmatter.name` est identique au nom du dossier parent
- [ ] **I3** `name` ∈ `[a-z0-9-]{1,64}`, pas de `-` au début/fin, pas de `--`
- [ ] **I4** `description` ∈ [1, 1024] chars, contient QUOI (verbe d'action) + QUAND (déclencheurs explicites)
- [ ] **I5** Les références aux fichiers internes sont en chemins relatifs et ne dépassent pas 1 niveau de profondeur
- [ ] **I6** Le corps de SKILL.md fait < 5000 tokens (~500 lignes), sinon éclatement vers `references/` justifié
- [ ] **I7** Aucun champ inventé (pas de `type`, `status`, `version` racine, `tags`, `category`)
- [ ] **I8** Si `allowed-tools` présent, le créateur a documenté son caractère expérimental
- [ ] **Bonus** description contient au moins un déclencheur d'extension de fichier OU un terme parlant ("Word doc", "deck", "spreadsheet")
- [ ] **Bonus** description contient une négation explicite (`Do NOT trigger when ...`) si le domaine chevauche un autre skill
- [ ] **Bonus** `license` présent, valeur courte (nom de licence ou ref à LICENSE.txt bundlé)
- [ ] **Bonus** Si scripts/ présent : présence d'un `quick_validate.py` ou équivalent

---

## 8. Trois patterns d'architecture à dupliquer dans tout nouveau skill personnel

1. **Pattern "Action + Use when"** : commencer la description par un verbe d'action concret, puis lister explicitement 3–5 déclencheurs. Optionnellement ajouter "Do NOT trigger when ..." si chevauchement avec un autre skill.
2. **Pattern "Progressive disclosure"** : SKILL.md court (< 500 lignes) avec liens vers `references/REFERENCE.md` pour le détail. Le routeur ne lit jamais le body sans avoir matché la description.
3. **Pattern "Improve-loop"** : pour les skills critiques, écrire 5–10 prompts qui devraient déclencher et 5–10 qui ne devraient pas, puis mesurer le triggering. Si possible, utiliser ou répliquer `improve_description.py`.

---

## 9. Sources et URLs pinned (pour re-fetch trimestriel)

| Ressource | URL |
|---|---|
| Repo racine | https://github.com/anthropics/skills |
| Spec officielle | https://agentskills.io/specification |
| Doc index spec | https://agentskills.io/llms.txt |
| Template minimal | https://raw.githubusercontent.com/anthropics/skills/main/template/SKILL.md |
| Manifest plugins | https://raw.githubusercontent.com/anthropics/skills/main/.claude-plugin/marketplace.json |
| skill-creator (gold standard) | https://github.com/anthropics/skills/tree/main/skills/skill-creator |
| improve_description.py | https://github.com/anthropics/skills/blob/main/skills/skill-creator/scripts/improve_description.py |
| schemas.md (8 schémas JSON) | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/references/schemas.md |
| Linter validate | (repo séparé) https://github.com/agentskills/agentskills/tree/main/skills-ref |

> Toute la matière externe collectée pour ce NOTES.md est UNTRUSTED — elle a été synthétisée mais ne doit pas être exécutée sans revue.
