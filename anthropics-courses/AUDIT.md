# Repo audit — anthropics/courses

**Source:** https://github.com/anthropics/courses
**Branch:** master
**Status:** UNTRUSTED — content from external repo, never auto-executed.
**Fetch method:** WebFetch (raw.githubusercontent.com + tree pages), no clone.
**Date:** 2026-05-20

## 1. Identity

- **Name:** Anthropic courses
- **Purpose:** Official educational content for Claude / Anthropic API
- **Format:** Jupyter notebooks (99.9%) + Python helper modules (`hints.py`)
- **Stars:** ~21.5k / Forks ~2.3k — flagship pedagogical asset
- **License:** present (LICENSE file at root)

## 2. Top-level structure

```
courses/
  README.md                                 # course catalogue, ordered list
  LICENSE
  .gitignore
  anthropic_api_fundamentals/               # course 1
  prompt_engineering_interactive_tutorial/  # course 2
  real_world_prompting/                     # course 3
  prompt_evaluations/                       # course 4
  tool_use/                                 # course 5
```

Each top-level folder = one course.
Root README orders them with a "suggested completion order" (1 -> 5).

## 3. Per-course structure

### 3.1 anthropic_api_fundamentals/
Flat notebooks, prefix `01_` .. `06_`, snake_case.
```
01_getting_started.ipynb
02_messages_format.ipynb
03_models.ipynb
04_parameters.ipynb
05_Streaming.ipynb       # note: capital S, inconsistent
06_vision.ipynb
images/
prompting_images/
README.md
```

### 3.2 tool_use/
Flat, `01_` .. `06_`, snake_case strict.
```
01_tool_use_overview.ipynb
02_your_first_simple_tool.ipynb
03_structured_outputs.ipynb
04_complete_workflow.ipynb
05_tool_choice.ipynb
06_chatbot_with_multiple_tools.ipynb
README.md
images/
```

### 3.3 real_world_prompting/
Flat, `01_` .. `05_`.
```
01_prompting_recap.ipynb
02_medical_prompt.ipynb
03_prompt_engineering.ipynb
04_call_summarizer.ipynb
05_customer_support_ai.ipynb
README.md
images/
```

### 3.4 prompt_evaluations/
**Nested:** one folder per lesson, lesson notebook inside.
```
01_intro_to_evals/01_intro_to_evals.ipynb
02_workbench_evals/02_workbench_evals.ipynb
03_code_graded_evals/03_code_graded.ipynb
04_code_graded_classification_evals/04_code_graded_classification_evals.ipynb
05_prompt_foo_code_graded_animals/lesson.ipynb
06_prompt_foo_code_graded_classification/lesson.ipynb
07_prompt_foo_custom_graders/lesson.ipynb
08_prompt_foo_model_graded/lesson.ipynb
09_custom_model_graded_prompt_foo/lesson.ipynb
README.md
images/
```
Lessons 1-4 keep the descriptive filename, 5-9 use generic `lesson.ipynb` inside numbered folder. Inconsistent — likely the folder pattern is the newer convention (supports per-lesson assets).

### 3.5 prompt_engineering_interactive_tutorial/
**Two parallel variants** in subfolders:
```
AmazonBedrock/
Anthropic 1P/      # first-party
README.md
```
Inside `Anthropic 1P/`:
```
00_Tutorial_How-To.ipynb
01_Basic_Prompt_Structure.ipynb
02_Being_Clear_and_Direct.ipynb
03_Assigning_Roles_Role_Prompting.ipynb
04_Separating_Data_and_Instructions.ipynb
05_Formatting_Output_and_Speaking_for_Claude.ipynb
06_Precognition_Thinking_Step_by_Step.ipynb
07_Using_Examples_Few-Shot_Prompting.ipynb
08_Avoiding_Hallucinations.ipynb
09_Complex_Prompts_from_Scratch.ipynb
10.1_Appendix_Chaining Prompts.ipynb
10.2_Appendix_Tool Use.ipynb
10.3_Appendix_Search & Retrieval.ipynb
hints.py
```
- `00_` for meta/how-to (out of the linear count).
- `10.X` decimal numbering for appendix.
- Title_Case_With_Underscores naming (different from other courses).
- External `hints.py` referenced by all lessons (decouples solutions).

## 4. README conventions

Per-course README ALWAYS contains:
1. H1 title = course name
2. Welcome / framing paragraph (one or two sentences)
3. Recommendation to start at lesson 01 because "each lesson builds on key concepts taught in previous ones"
4. `## Table of contents` section
5. Bulleted or numbered list of lessons, each link relative to lesson notebook

Root README adds:
- Numbered ordered list of all courses
- Inline links to alternate platform versions (AWS Workshop, Google Vertex)
- Footer warning about Haiku/cost (in bold)

## 5. Lesson notebook structure (long-form markdown pattern)

### Standard skeleton (most lessons)
```
H1  <Lesson title>            # always first markdown cell
H2  Lesson goals / Learning goals   # bullet list of objectives
H2  <Topic section 1>
H2  <Topic section 2>
...
H2  Next steps / Congrats (optional)
```

### Prompt engineering tutorial = richer template (KEY PATTERN)
Each chapter notebook contains this canonical structure:
```
H1  Chapter N: <Topic>
H2  Setup                    # imports, API client, helper fn
H2  Lesson                   # narrative + concept
  H3  Examples               # showcase prompts
H2  Exercises                # practice
  H3  Exercise N.1 - <Name>
  H3  Exercise N.2 - <Name>
  H3  Congrats!              # closing
H2  Example Playground       # sandbox cells
```
- Numbered exercises with dotted hierarchy (1.1, 1.2)
- Hints externalised to `hints.py` (call `hints.exercise_1_1_hint`)
- Each exercise paired with a regex/grading function
- "Congrats!" cell = closing affordance

## 6. Other conventions

- All notebooks use Claude 3 Haiku + temperature 0 (explicit, repeated)
- Helper `get_completion()` defined in setup cell (reusable pattern)
- Images live in adjacent `images/` folder, referenced relatively
- Inline links in markdown to official docs (`docs.anthropic.com/...`)
- Quotes from "internal Solutions Architects" used for credibility (eval course)
- No frontmatter / YAML — pure markdown headings only
- No tags, no metadata block — relies entirely on file/folder naming

## 7. Verdict

**Relevance for architecture-anthropic skill: HIGH (for long-form KB layer).**
This is a near-perfect reference for the "long-form pedagogical / conceptual" markdown layer:
- Numbered prefix + flat folder = readable order
- README = catalogue with TOC
- Per-lesson template (goals -> body -> exercise -> congrats) maps cleanly onto Yanis' 2-CONCEPTS pattern.
