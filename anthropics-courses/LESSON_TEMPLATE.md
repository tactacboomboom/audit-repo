# Lesson template extracted from anthropics/courses

Two canonical templates emerge — a **minimal** one (used in tool_use, api_fundamentals, real_world_prompting, prompt_evaluations) and a **rich exercise-driven** one (prompt_engineering_interactive_tutorial).

---

## Template A — Minimal lesson

```markdown
# <Lesson title>          (H1, first markdown cell)

## Lesson goals           (or "Learning goals")
In this lesson, you'll learn how to:
- <objective 1>
- <objective 2>
- <objective 3>

## <Topic section 1>
<narrative + code>

## <Topic section 2>
<narrative + code>

## <Topic section N>
<narrative + code>

(optional) ## Next steps
```

Observed in `01_getting_started.ipynb`, `01_tool_use_overview.ipynb`, `01_intro_to_evals.ipynb`, `01_prompting_recap.ipynb`.

---

## Template B — Exercise-driven lesson

```markdown
# Chapter N: <Topic>

## Setup
Imports, API client, helper function `get_completion()`.

## Lesson
Narrative explanation of the concept.

### Examples
One or more worked example prompts showing the technique.

## Exercises

### Exercise N.1 - <Name>
Task description.
Grading function (regex / assertion).
Hint available via `hints.exercise_n_1_hint`.

### Exercise N.2 - <Name>
...

### Congrats!
Closing affordance after exercises pass.

## Example Playground
Empty sandbox cells for free experimentation.
```

Observed in `01_Basic_Prompt_Structure.ipynb` and following chapters of the interactive tutorial.

---

## Recurring rhetorical patterns

1. **Open with H1 title** — never frontmatter, never preamble
2. **Lesson goals as bullet list** under H2 immediately after the title
3. **Quote internal experts** (`> "..."` — Solutions Architect) for credibility in conceptual content
4. **"Welcome to Anthropic's..."** opening sentence on per-course README
5. **"We recommend that you start from the beginning... each lesson builds on key concepts taught in previous ones"** — repeated almost verbatim across READMEs
6. **Closing "Congrats!" / "Next steps"** mini-section as completion affordance

## What is NOT used

- No YAML frontmatter
- No tags or metadata blocks
- No dataview-style queries
- No backlinks section
- No "Sources" / "References" footer (sources are inline)
- No callout blocks (Obsidian `> [!note]` style absent)
- Quotes use plain markdown `>` blockquote
