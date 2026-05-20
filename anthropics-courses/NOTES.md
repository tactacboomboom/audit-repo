# NOTES — anthropics/courses pour `architecture-anthropic`

**Repo audité :** https://github.com/anthropics/courses (branche `master`)
**Layer ciblé :** markdown drive-only / catalogue archi officielle Anthropic
**Pertinence pour le skill :** **HAUTE** — meilleure référence publique disponible pour la couche "KB long-form pédagogique" du vault Yanis (1-CONVERSATIONS et 2-CONCEPTS).
**Date :** 2026-05-20

---

## 1. Pourquoi c'est pertinent pour Yanis

Le vault Yanis stocke deux types de contenu long-form :
- `vault\1 - CONVERSATIONS\` — capture chronologique de sessions
- `vault\2 - CONCEPTS\` — décantation conceptuelle réutilisable

Anthropic/courses montre **comment Anthropic eux-mêmes structurent un corpus pédagogique long-form en markdown plat (sans CMS, sans frontmatter, sans tags)**. C'est exactement la même contrainte que le vault : fichiers `.md` lus à plat depuis Drive.

Verdict : c'est **la** référence officielle à imiter pour la couche 2-CONCEPTS et à adapter (date-prefix) pour 1-CONVERSATIONS.

---

## 2. Structure pédagogique — numérotation, progression, naming

### Numérotation (convention forte, reproductible)
- **`01_` à `09_`** — deux chiffres zero-padded, ordre de lecture obligatoire
- **`00_`** — meta / how-to / overview, hors du compte linéaire
- **`10.1_`, `10.2_`, `10.3_`** — appendice en décimal (extensions au-delà du parcours principal)
- Lecture imposée : chaque README répète "we recommend that you start from the beginning... each lesson builds on key concepts taught in previous ones"

### Trois layouts coexistent (à choisir selon volume)

| Layout                  | Quand                                         | Exemple                           |
| ----------------------- | --------------------------------------------- | --------------------------------- |
| Flat numbered           | < 10 entrées, pas d'assets par entrée         | `tool_use/01_overview.ipynb`       |
| Folder-per-entry        | Chaque entrée a des fichiers compagnons       | `prompt_evaluations/01_intro_to_evals/01_intro_to_evals.ipynb` |
| Platform variants       | Même contenu, plusieurs cibles                | `prompt_engineering_*/AmazonBedrock/` + `Anthropic 1P/` |

### Naming
- Snake_case dominant (`01_tool_use_overview.ipynb`)
- Exception : prompt eng tutorial utilise `Title_Case_With_Underscores` — **incohérence à NE PAS reproduire**
- Verbes nominalisés courts : "overview", "recap", "fundamentals"
- Pas de date dans le nom de fichier — l'ordre est porté par le préfixe numérique

---

## 3. Format des leçons (notebooks) — patterns markdown

### Template A — minimal (4 courses sur 5)
```markdown
# <Titre de la leçon>          # H1, première cellule

## Lesson goals                # ou "Learning goals"
In this lesson, you'll learn how to:
- <objectif 1>
- <objectif 2>

## <Section 1>
<narratif + code>

## <Section 2>
<narratif + code>

(optionnel) ## Next steps
```

### Template B — exercise-driven (prompt engineering tutorial)
```markdown
# Chapter N: <Topic>

## Setup
<imports, helper get_completion()>

## Lesson
<concept narratif>
### Examples
<prompts d'exemple>

## Exercises
### Exercise N.1 - <Nom>
<tâche + grader regex>
### Exercise N.2 - <Nom>
### Congrats!                   # affordance de clôture

## Example Playground            # bac à sable libre
```

**Points clés du Template B (le plus riche) :**
- Exercices numérotés en hiérarchie pointée (`1.1`, `1.2`)
- Indices externalisés dans `hints.py` — séparation contenu/solution
- Chaque exercice a un grader automatique (regex / assertion)
- "Congrats!" comme micro-affordance de clôture

---

## 4. Métadonnées top-of-file — absence remarquable

**Anthropic n'utilise AUCUN de ces dispositifs :**
- Pas de YAML frontmatter
- Pas de tags
- Pas de bloc de prérequis structuré (juste un § narratif dans le README parent)
- Pas de "Sources" / "References" en footer (liens inline dans le corps)
- Pas de callouts Obsidian `> [!note]` (juste `>` blockquote standard)

**Tout repose sur :**
1. Le nom du fichier (préfixe numérique + titre snake_case)
2. La H1 dans la première cellule markdown
3. La section `## Lesson goals` immédiatement après
4. Le README parent qui sert de catalogue + TOC

**Implication pour vault Yanis :** la couche markdown drive-only PEUT s'en passer aussi pour la majorité des fichiers. Le frontmatter doit être réservé aux fichiers nécessitant indexation (knowledge graph, search) — pas une obligation systématique.

---

## 5. Conventions markdown long-form — sections, exercices, solutions

### Sections récurrentes (par fréquence)
1. **`## Lesson goals` / `## Learning goals`** — quasi universel, juste après H1
2. **`## Setup`** — bloc d'amorce technique (imports, config)
3. **`## Lesson`** — corps conceptuel
4. **`### Examples`** — démonstrations
5. **`## Exercises`** — pratique
6. **`### Exercise N.M - <Name>`** — items individuels
7. **`### Congrats!`** — clôture
8. **`## Example Playground`** — bac à sable
9. **`## Next steps` / `## Table of contents`** — navigation

### Patterns rhétoriques
- **Ouverture en H1 direct** (jamais de préambule)
- **Goals en bullet list** immédiatement
- **Citations d'experts internes** en `>` blockquote pour crédibilité narrative ("Solutions Architect: ...")
- **"Welcome to Anthropic's ..."** — phrase d'ouverture standardisée du README
- **"each lesson builds on key concepts"** — phrase d'orientation quasi verbatim sur tous les READMEs

### Solutions / reveals
**Pattern d'or :** les solutions / indices sont **dans un fichier compagnon séparé** (`hints.py`), pas dans la note principale. Adaptation vault : créer un sibling `hints.md` pour les exercices conceptuels.

---

## 6. Patterns d'organisation de KB pédago — REUTILISABLES pour vault Yanis

### Pour `vault\2 - CONCEPTS\` — adopter Template B
Chaque concept = un dossier OU un fichier (selon volume d'assets) :
```
2 - CONCEPTS/
  README.md                              # TOC du domaine conceptuel
  00_overview.md                         # carte mentale du domaine
  01_<concept-fondateur>.md
    # H1 + ## Goals + ## Setup (prérequis) + ## Lesson + ### Examples + ## Exercises + ## Next steps
  02_<concept>.md
  10.1_appendix_<sujet>.md
  hints.md                                # reveals séparés
  images/
```

### Pour `vault\1 - CONVERSATIONS\` — Template A + date-prefix
Préfixe date au lieu d'ordinal (chronologique l'emporte sur l'ordinal) :
```
1 - CONVERSATIONS/
  README.md                              # TOC chronologique inverse
  2026-05-20_<topic-slug>.md
    # H1 + ## Goals (de la session) + sections narratives
  2026-05-21_<topic-slug>.md
  images/
```
Garde l'ouverture H1 + ## Goals même pour les captures brutes — force la décantation minimale.

### Règles universelles à imposer
1. Tout dossier a un `README.md` catalogue avec TOC en liens relatifs
2. Toute note longue ouvre par H1 puis `## Goals` puis sections
3. Aucun fichier orphelin : chaque entrée linkée depuis au moins un README TOC
4. Reveal/solution dans un fichier compagnon, jamais inline
5. Images dans un `images/` adjacent, références relatives

---

## 7. Top 5 patterns à importer dans `architecture-anthropic`

1. **Numérotation `00_` / `01_..09_` / `10.X_`** : meta / linéaire / appendice — convention complète et lisible
2. **README de dossier = catalogue TOC obligatoire** à chaque niveau (root + sub) avec phrase d'orientation standard
3. **Squelette de note long-form : H1 -> `## Goals` -> sections -> `## Next steps`** sans frontmatter ni tags
4. **Solutions/reveals dans un sibling séparé** (`hints.py` style) — jamais dans la note principale
5. **Trois layouts au choix** (flat / folder-per-entry / platform-variants) avec critère explicite — pas un seul dogme

---

## 8. Risques / pièges observés (ne pas reproduire)

- Mélange Snake_case et Title_Case_Underscored dans le même repo
- Mélange flat + nested folder-per-entry dans la même série (prompt_evaluations) — déstabilisant
- Fichiers `lesson.ipynb` génériques quand le dossier porte déjà le nom — perte de searchability
- Capitalisation inconsistante (`05_Streaming.ipynb` vs `06_vision.ipynb`)

---

## 9. Limites de cet audit

- Lecture WebFetch uniquement (pas de clone), donc seules les premières cellules markdown des notebooks ont été échantillonnées
- Contenu UNTRUSTED — patterns extraits structurellement, sans exécuter aucun code
- Pas d'inspection du dossier `AmazonBedrock/` ni de `prompt_evaluations/05_*` à `09_*` (templates redondants présumés)

---

## 10. Fichiers d'audit dans ce dossier

- `AUDIT.md` — audit complet (identité, structure, conventions, verdict)
- `STRUCTURE.md` — arborescence complète + tableau des 3 layouts
- `LESSON_TEMPLATE.md` — Template A et Template B extraits
- `PERSONAL_CHECKLIST.md` — import / reject / mapping vault Yanis
- `NOTES.md` — **ce fichier** (synthèse opérationnelle pour le skill)
