# NOTES — `anthropics/anthropic-cookbook`

> Layer markdown drive-only pour le skill `architecture-anthropic`.
> Source : audit du repo officiel `anthropics/anthropic-cookbook` (main).
> Audité le 2026-05-20. Repo : 43.4k ★, MIT, 95 % notebooks.
>
> **Postulat** : la forme que prend Anthropic dans SES exemples est un signal
> direct sur la forme attendue côté utilisateur. Ce qui suit est donc
> simultanément un catalogue de patterns *et* une checklist d'audit perso.

---

## 0 — Verdict pertinence

**Haute.** C'est la référence canonique pour deux questions :

1. Comment Anthropic catégorise ses propres recettes (taxonomie).
2. Comment Anthropic structure une unité de connaissance reproductible
   (un notebook = une recette = une capability isolée).

Tout skill qui prétend cartographier "l'architecture Anthropic" doit
au minimum coller à cette taxonomie comme épine dorsale.

---

## 1 — Squelette d'organisation (top-level)

Le repo découpe le territoire en **8 axes de capability** + 4 axes
"transverses" (skills, agents, SDK, managed) :

```
capabilities/           ← briques cognitives (classif, RAG, summ, KG, T2SQL…)
tool_use/               ← protocole d'outillage (15 notebooks)
multimodal/             ← vision + sub-agents perceptifs
extended_thinking/      ← reasoning budgeté (2 notebooks)
misc/                   ← API features transverses (caching, batch, JSON…)
patterns/agents/        ← patterns "Building Effective Agents"
skills/                 ← skills framework (Excel/PPT/PDF/Word + custom)
claude_agent_sdk/       ← tutoriels SDK Agent (numérotés 00..06)
managed_agents/         ← Claude Managed Agents (CMA_*)
third_party/            ← intégrations externes (Pinecone, LlamaIndex…)
finetuning/             ← Bedrock fine-tuning
observability/          ← admin/usage API
coding/                 ← exemples coding spécifiques
```

**Lecture pour le skill** :

- `capabilities/` = "ce que Claude *fait*" (verbe sortant).
- `tool_use/` + `patterns/agents/` = "comment Claude *agit*" (orchestration).
- `skills/` + `claude_agent_sdk/` + `managed_agents/` = "comment on
  *encapsule* Claude" (3 niveaux d'encapsulation : skill < SDK < managed).
- `misc/` = features API à plat — caching, batch, JSON, citations, PDF.
- `multimodal/`, `extended_thinking/`, `third_party/` = axes orthogonaux
  qui se composent avec les précédents.

→ **Checklist d'audit perso** : un projet "architecture Anthropic" qui n'expose
pas explicitement *où* il se range dans ces 8+4 axes est mal cartographié.

---

## 2 — Granularité d'une unité (la règle d'or)

> **"One concept per notebook"** — règle explicite du `CONTRIBUTING.md`.

Conséquences observables :

- `capabilities/<topic>/guide.ipynb` — un dossier par capability, **un
  seul fichier nommé `guide.ipynb`**. Pas de version_v2, pas de variantes.
  Le dossier porte le sens, le nom du notebook est inerte.
- `tool_use/calculator_tool.ipynb`, `tool_use/parallel_tools.ipynb`,
  `tool_use/tool_choice.ipynb` — un notebook = une dimension du tool use.
  Pas de "calculator_advanced", on découpe par concept.
- `claude_agent_sdk/00_The_one_liner_research_agent.ipynb` …
  `06_The_vulnerability_detection_agent.ipynb` — **préfixe numérique
  quand il y a une progression pédagogique linéaire**.
- `managed_agents/CMA_*.ipynb` — **préfixe acronyme** pour les notebooks
  appartenant à une même famille produit.

**Pattern de naming résumé** :

| Cas | Convention |
|---|---|
| Capability isolée (briques cognitives) | `<topic>/guide.ipynb` |
| Recette indépendante | `snake_case_descriptif.ipynb` |
| Série pédagogique ordonnée | `NN_The_<topic>_<noun>.ipynb` |
| Famille produit | `<ACRONYME>_<verbe>_<objet>.ipynb` |

→ **Checklist** : si je nomme un truc `agent_v2_final.ipynb`, je viole
la règle. Si je mets deux concepts dans le même notebook, je viole la règle.

---

## 3 — Documentation des exemples (README pattern)

Le README racine fonctionne comme **table de matières plate**, regroupée
en 5 sections fixes :

1. Capabilities
2. Tool Use and Integration
3. Third-Party Integrations
4. Multimodal Capabilities
5. Advanced Techniques

Chaque entrée = `[Titre court](chemin/relatif.ipynb)` + 1 phrase de description.

**Pas de métadonnées YAML en tête des notebooks**. Les métadonnées vivent
dans deux fichiers séparés :

- `registry.yaml` — registre central : path, titre, description, tags,
  auteur(s). C'est le fichier qui alimente le site web public.
- `authors.yaml` — mapping `github_username → {name, website, avatar}`.

→ **Pattern réutilisable** : séparer le *contenu* (notebook) de ses
*métadonnées* (registry.yaml). Le notebook reste exécutable pur,
le registre reste lisible/diffable.

→ **Checklist** : si je veux que mon skill catalogue scale, je crée
un `registry.yaml` à la racine plutôt que de stuffer des front-matters
dans chaque fichier markdown.

---

## 4 — Conventions techniques (du CLAUDE.md + CONTRIBUTING.md)

À copier tel quel quand on initialise un projet "à la cookbook" :

| Domaine | Convention Anthropic |
|---|---|
| Package manager | `uv` (lock + sync) |
| Python | `>=3.11,<3.13` |
| Build | `hatchling` |
| Lint/format | `ruff` — line 100, double quotes |
| Pre-commit | activé via Makefile |
| Tests notebooks | `nbval` + `tox` + marker `slow` |
| API key | **jamais commit**, `os.environ`/`os.getenv()`, `.env.example` |
| Modèles | **alias non datés** uniquement (`claude-sonnet-4-6`, `claude-haiku-4-5`) |
| Bedrock | base IDs Bedrock, préfixe `global.` optionnel |
| Commits | conventional commits (`feat/fix/docs/style/refactor/test/chore/ci`) |
| Branches | `<username>/<feature-description>` |
| PR | un feature/fix par PR, format conventional dans le titre |

→ **Checklist** : la mention "alias non datés" est le seul vrai red flag
si on m'envoie du code Anthropic qui hardcode `claude-3-5-sonnet-20241022`.

---

## 5 — Trois niveaux d'encapsulation d'un agent

C'est *la* lecture architecturale clé du repo. Anthropic expose trois
niveaux distincts, **du plus léger au plus lourd** :

### Niveau 1 — `skills/` (Skills framework)

- Format : `SKILL.md` (instructions) + `scripts/` (optionnel) +
  `resources/` (optionnel).
- Progressive Disclosure : ne charge que ce dont Claude a besoin.
- Beta headers requis : `code-execution-2025-08-25`,
  `files-api-2025-04-14`, `skills-2025-10-02`.
- Namespace API : `client.beta.*` (pas `client.messages`).
- 4 skills built-in : xlsx, pptx, pdf, docx.
- Cas d'usage : extension cognitive ponctuelle, document-centric.

### Niveau 2 — `claude_agent_sdk/` (Claude Agent SDK)

- Format : agent autonome avec subagents, plan mode, MCP servers.
- 7 tutoriels numérotés `00..06`.
- Cas d'usage : agent côté dev/local, contrôle fin du loop.
- Inclut un guide de migration depuis OpenAI Agents SDK
  (`04_migrating_from_openai_agents_sdk.ipynb`).

### Niveau 3 — `managed_agents/` (Claude Managed Agents — CMA)

- Format : agent géré côté Anthropic (sessions, mémoire, versioning,
  file mounting, vault credentials, webhooks).
- 9 notebooks `CMA_*` couvrant : iterate tests, issue→PR, codebase
  exploration, human-in-the-loop, prompt versioning/rollback, prod
  setup, user prefs memory, multi-agent team, outcome grader.
- Cas d'usage : agent en prod, hébergé, observable.

**Grille de décision** (à reprendre dans le skill) :

| Question | Niveau cible |
|---|---|
| "Je veux que Claude lise un Excel" | Skills |
| "Je veux un agent local qui tourne dans mon repo" | Agent SDK |
| "Je veux un agent en prod hébergé avec mémoire" | Managed Agents |

---

## 6 — Patterns SDK officiels (ordre canonique)

Ce que le repo *traite* comme features SDK first-class, dans l'ordre
où on les trouve dans `tool_use/` + `misc/` :

| Feature | Notebook(s) | Cookbook signal |
|---|---|---|
| **Tool use de base** | `tool_use/calculator_tool.ipynb` | obligatoire pour démarrer |
| **Tool choice** | `tool_use/tool_choice.ipynb` | `auto` vs `any` vs `tool` |
| **Parallel tools** | `tool_use/parallel_tools.ipynb` | batch meta-pattern |
| **Programmatic tool calling (PTC)** | `tool_use/programmatic_tool_calling_ptc.ipynb` | latence/coût |
| **Tool search w/ embeddings** | `tool_use/tool_search_with_embeddings.ipynb` | scale à ≥1000 tools |
| **Context engineering** | `tool_use/context_engineering/` | memory vs compact vs clear |
| **Automatic context compaction** | `tool_use/automatic-context-compaction.ipynb` | long-running |
| **Memory tool** | `tool_use/memory_cookbook.ipynb` + `memory_tool.py` | persistance |
| **Extended thinking** | `extended_thinking/extended_thinking.ipynb` | budget tokens |
| **Extended thinking + tools** | `extended_thinking/extended_thinking_with_tool_use.ipynb` | combo |
| **Prompt caching** | `misc/prompt_caching.ipynb` | cost reduc |
| **Speculative caching** | `misc/speculative_prompt_caching.ipynb` | warm cache pendant typing |
| **Batch processing** | `misc/batch_processing.ipynb` | -50 % coût async |
| **Citations** | `misc/using_citations.ipynb` | source attribution |
| **PDF upload** | `misc/pdf_upload_summarization.ipynb` | documents |
| **Files API** | (via Skills, beta header `files-api-2025-04-14`) | I/O fichiers |
| **JSON mode** | `misc/how_to_enable_json_mode.ipynb` | structured output |
| **Sampling past max_tokens** | `misc/sampling_past_max_tokens.ipynb` | continuation |
| **Session memory compaction** | `misc/session_memory_compaction.ipynb` | background thread |

→ **Checklist d'audit** : un projet "architecture Anthropic" mature
exploite typiquement **3 de ces patterns combinés** (ex : caching +
batch + tool use). Un projet qui n'en utilise qu'un seul est probablement
sous-architecturé.

---

## 7 — Patterns d'agents (`patterns/agents/`)

Source : papier *Building Effective Agents* (Schluntz & Zhang, Anthropic).

**Building blocks** (basique) :

1. **Prompt Chaining** — séquentiel.
2. **Routing** — diriger vers le bon handler.
3. **Multi-LLM Parallelization** — concurrent.

**Workflows avancés** :

4. **Orchestrator-Subagents** — coordinateur + spécialistes.
5. **Evaluator-Optimizer** — boucle eval → optim.

3 notebooks (un par workflow avancé) + `util.py` + `prompts/`.

→ **Pattern d'organisation réutilisable** : un dossier `patterns/X/`
contient `README.md` (théorie), N notebooks (un par pattern), `util.py`
(code partagé), `prompts/` (assets externalisés). C'est le squelette
canonique d'un "pack pédagogique" Anthropic.

---

## 8 — Catégorisation officielle (du `registry.yaml`)

Le `registry.yaml` partitionne les ~70 recettes en **11 buckets** :

```
1. Claude Managed Agents          (8)
2. Claude Agent SDK               (7)
3. Tool Use & Agents              (15)
4. Knowledge & Retrieval          (8)
5. Vision & Multimodal            (7)
6. Extended Thinking              (2)
7. Fine-Tuning & Optimization     (8)
8. Evaluation & Assessment        (5)
9. Multi-Agent Patterns           (6)
10. Skills Framework              (3)
11. Third-Party Integrations      (11)
+ Observability & Admin           (1)
+ Frontend & Responses            (4)
```

→ **Cette partition est *la* nomenclature de référence**. Le skill
`architecture-anthropic` devrait l'adopter telle quelle comme axe
principal de classification. Toute déviation doit être justifiée.

---

## 9 — Top 5 patterns réutilisables (pour MON skill)

1. **Taxonomie 11 buckets** (registry.yaml) — colonne vertébrale du skill.
2. **3 niveaux d'encapsulation agent** (Skills < SDK < Managed) — grille
   de décision systématique pour ranger n'importe quel projet d'agent.
3. **"One concept per file"** + naming par préfixe (numérique = série,
   acronyme = famille produit, snake_case = standalone).
4. **Métadonnées hors-fichier** via `registry.yaml` + `authors.yaml`,
   notebook ou markdown reste pur.
5. **README plat avec 5 sections fixes** + 1 phrase par entrée — pas
   d'arborescence profonde dans le README, la profondeur vit dans le
   filesystem.

---

## 10 — Anti-patterns à éviter (déduits par contraste)

- Pas de versioning dans les noms de fichiers (`_v2`, `_final`).
- Pas de YAML front-matter dans les notebooks (registre externe).
- Pas de modèles datés en dur dans le code.
- Pas de README profond / d'arborescence ToC : la table de matières
  reste plate, les sous-niveaux sont implicites par dossier.
- Pas de "kitchen-sink notebook" — strict 1 concept par notebook.

---

## 11 — Pointeurs URL (raw) utiles pour re-fetch

```
README                 raw.githubusercontent.com/anthropics/anthropic-cookbook/main/README.md
CLAUDE.md              raw.githubusercontent.com/anthropics/anthropic-cookbook/main/CLAUDE.md
CONTRIBUTING.md        raw.githubusercontent.com/anthropics/anthropic-cookbook/main/CONTRIBUTING.md
registry.yaml          raw.githubusercontent.com/anthropics/anthropic-cookbook/main/registry.yaml
authors.yaml           raw.githubusercontent.com/anthropics/anthropic-cookbook/main/authors.yaml
pyproject.toml         raw.githubusercontent.com/anthropics/anthropic-cookbook/main/pyproject.toml
patterns/agents/README raw.githubusercontent.com/anthropics/anthropic-cookbook/main/patterns/agents/README.md
skills/README          raw.githubusercontent.com/anthropics/anthropic-cookbook/main/skills/README.md
skills/CLAUDE.md       raw.githubusercontent.com/anthropics/anthropic-cookbook/main/skills/CLAUDE.md
```

---

*Fin NOTES.md — alimente `architecture-anthropic`. Re-audit recommandé
si le registry.yaml gagne un nouveau bucket ou si un 4e niveau
d'encapsulation apparaît au-dessus de Managed Agents.*
