# Personal audit checklist — patterns to import / reject

Layer: markdown drive-only (vault Yanis)
Source: anthropics/courses
Decision context: comparing official Anthropic pedagogy with vault\1-CONVERSATIONS\ and vault\2-CONCEPTS\

## IMPORT (high-confidence, fits vault long-form layer)

- [ ] **Two-digit zero-padded numeric prefix** (`01_`, `02_`) for ordered series in a folder
- [ ] **`00_` prefix for meta / how-to / overview** that sits outside the linear count
- [ ] **Decimal suffix `10.1_`, `10.2_`** for appendix / addendum to a main entry
- [ ] **README.md as a catalogue with TOC** at every folder level (root + sub)
- [ ] **Standard opening sentence** for per-folder README ("Welcome to ... <N> lessons / notes / etc.")
- [ ] **TOC as relative-link list** (no absolute paths)
- [ ] **H1 title = first content line** (no preamble, no frontmatter)
- [ ] **H2 "Goals" / "Objectives" bullet list right after title** for any conceptual note
- [ ] **"We recommend starting from..."** orientation phrase in series READMEs
- [ ] **`hints.py`-style externalisation** — anything that is "solution / answer / reveal" lives in a separate companion file, not the main note
- [ ] **Adjacent `images/` folder** with relative references (no central asset dir)
- [ ] **Closing "Next steps" / "See also" mini-section** as navigation affordance
- [ ] **Inline blockquotes (`>`) for expert quotes** — sufficient without callout extension

## REJECT (not used in source, keep vault convention)

- [ ] No YAML frontmatter — Anthropic doesn't use it, but vault DOES (tags, dates needed for Yanis system)
- [ ] No tags — vault needs them for the knowledge graph
- [ ] No backlinks footer — vault generates them
- [ ] No callouts `> [!note]` — Anthropic stays plain markdown; vault may use Obsidian extensions

## INCONSISTENCIES to AVOID copying

- [ ] Don't mix `Snake_case` and `Title_Case_Underscored` (Anthropic does — bad)
- [ ] Don't mix flat layout + nested folder-per-entry in the same series (prompt_evaluations does — confusing)
- [ ] Don't use generic `lesson.ipynb` filenames when in nested folders — kill searchability; always keep descriptive filename even when folder name duplicates it

## Mapping to vault Yanis

### vault\2 - CONCEPTS\
Best fit for **Template B** structure (rich, exercise-driven):
```
00_overview.md
01_<concept>.md     # H1 + Goals + Lesson + Examples + Exercises + Playground
02_<concept>.md
...
README.md          # TOC
hints.md           # optional reveal layer
images/
```

### vault\1 - CONVERSATIONS\
Best fit for **Template A** structure (minimal narrative):
```
README.md
2026-05-20_<topic>.md   # H1 + Goals + body sections
2026-05-21_<topic>.md
images/
```
- Use date prefix instead of `01_` for conversations (chronological > ordinal)
- Keep H1-then-Goals opening even for chat captures — forces decanting

### Universal rules to enforce
- Every folder has a `README.md` catalogue
- Every long-form note opens with H1, then `## Goals`, then sections
- No orphan files: each entry linked from at least one README TOC
- Reveal/solution content always in a *separate* sibling file
