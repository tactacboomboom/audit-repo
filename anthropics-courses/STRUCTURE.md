# Structure map — anthropics/courses

```
courses/
|-- README.md                                     # ordered course catalogue + meta note
|-- LICENSE
|-- .gitignore
|
|-- anthropic_api_fundamentals/                   # COURSE 1 — flat layout
|   |-- README.md                                  # TOC linking 01..06
|   |-- 01_getting_started.ipynb
|   |-- 02_messages_format.ipynb
|   |-- 03_models.ipynb
|   |-- 04_parameters.ipynb
|   |-- 05_Streaming.ipynb
|   |-- 06_vision.ipynb
|   |-- images/
|   `-- prompting_images/
|
|-- prompt_engineering_interactive_tutorial/      # COURSE 2 — platform variants
|   |-- README.md
|   |-- AmazonBedrock/                             # variant 1
|   `-- Anthropic 1P/                              # variant 2 (first-party)
|       |-- 00_Tutorial_How-To.ipynb               # meta lesson, prefix 00
|       |-- 01_Basic_Prompt_Structure.ipynb        # chapter template
|       |-- 02_Being_Clear_and_Direct.ipynb
|       |-- 03_Assigning_Roles_Role_Prompting.ipynb
|       |-- 04_Separating_Data_and_Instructions.ipynb
|       |-- 05_Formatting_Output_and_Speaking_for_Claude.ipynb
|       |-- 06_Precognition_Thinking_Step_by_Step.ipynb
|       |-- 07_Using_Examples_Few-Shot_Prompting.ipynb
|       |-- 08_Avoiding_Hallucinations.ipynb
|       |-- 09_Complex_Prompts_from_Scratch.ipynb
|       |-- 10.1_Appendix_Chaining Prompts.ipynb   # decimal = appendix
|       |-- 10.2_Appendix_Tool Use.ipynb
|       |-- 10.3_Appendix_Search & Retrieval.ipynb
|       `-- hints.py                                # externalised solutions
|
|-- real_world_prompting/                         # COURSE 3 — flat
|   |-- README.md
|   |-- 01_prompting_recap.ipynb
|   |-- 02_medical_prompt.ipynb
|   |-- 03_prompt_engineering.ipynb
|   |-- 04_call_summarizer.ipynb
|   |-- 05_customer_support_ai.ipynb
|   `-- images/
|
|-- prompt_evaluations/                           # COURSE 4 — nested (1 folder / lesson)
|   |-- README.md
|   |-- 01_intro_to_evals/01_intro_to_evals.ipynb
|   |-- 02_workbench_evals/02_workbench_evals.ipynb
|   |-- 03_code_graded_evals/03_code_graded.ipynb
|   |-- 04_code_graded_classification_evals/04_code_graded_classification_evals.ipynb
|   |-- 05_prompt_foo_code_graded_animals/lesson.ipynb
|   |-- 06_prompt_foo_code_graded_classification/lesson.ipynb
|   |-- 07_prompt_foo_custom_graders/lesson.ipynb
|   |-- 08_prompt_foo_model_graded/lesson.ipynb
|   |-- 09_custom_model_graded_prompt_foo/lesson.ipynb
|   `-- images/
|
`-- tool_use/                                     # COURSE 5 — flat
    |-- README.md
    |-- 01_tool_use_overview.ipynb
    |-- 02_your_first_simple_tool.ipynb
    |-- 03_structured_outputs.ipynb
    |-- 04_complete_workflow.ipynb
    |-- 05_tool_choice.ipynb
    |-- 06_chatbot_with_multiple_tools.ipynb
    `-- images/
```

## Three layout flavours coexisting

| Flavour                  | Used by                              | When to pick                                   |
| ------------------------ | ------------------------------------ | ---------------------------------------------- |
| Flat numbered            | api_fundamentals, real_world, tool_use | Small course (< 10 lessons), no per-lesson assets |
| Folder-per-lesson nested | prompt_evaluations                   | Lesson has data, configs, multiple files       |
| Platform variants split  | prompt_engineering_interactive       | Same content for multiple cloud platforms      |

## Numbering conventions

- `01_` .. `09_` — two-digit zero-padded, lessons in order
- `00_` — meta / how-to / overview (out of linear count)
- `10.1_`, `10.2_` — appendix using decimal suffix
- Snake_case (most) OR Title_Case_Underscored (prompt eng tutorial) — inconsistent across courses
