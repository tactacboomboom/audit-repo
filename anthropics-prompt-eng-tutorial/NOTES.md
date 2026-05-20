# NOTES — anthropics/prompt-eng-interactive-tutorial

> Repo officiel Anthropic. Pertinence pour le skill `architecture-anthropic` : **HAUTE**.
> Source d'autorité citable. Branche : `master`. ~35.8k stars.
> Tout le contenu ci-dessous est extrait verbatim ou paraphrasé des notebooks Anthropic.

---

## 1. Structure du tutorial

### Progression pédagogique
```
Beginner       : 01 → 02 → 03   (Structure / Clarté / Roles)
Intermediate   : 04 → 05 → 06 → 07   (Data sep / Format / CoT / Few-shot)
Advanced       : 08 → 09   (Hallucinations / Complex prompts from scratch)
Appendix       : 10.1 → 10.2 → 10.3   (Chaining / Tool use / Search & Retrieval)
```

### Naming des leçons
- Pattern strict : `NN_Title_With_Underscores.ipynb`
- 2-digit prefix (`01_`, `02_`, …) → ordre lexicographique = ordre pédagogique
- Appendix : dot-decimal `10.1_`, `10.2_`, `10.3_`
- Préfixe `Appendix_` discrimine le contenu hors-cursus
- Fichier helper Python autonome : `hints.py`
- Deux versions parallèles du cursus : `Anthropic 1P/` (SDK natif) et `AmazonBedrock/` (même contenu, SDK Bedrock)

### Chapitrage interne d'un notebook
Chaque leçon suit la même structure :
1. **Lesson** (markdown) — concept exposé
2. **Examples** (code cells) — démonstration exécutable
3. **Exercises** (code cells avec TODO) — l'utilisateur modifie le prompt
4. **Example Playground** (code cells libres) — bac à sable pour expérimenter

### Setup (Lesson 00)
- Prérequis : Python + `pip install anthropic` + clé API
- Pattern d'init : variables globales `API_KEY`, `MODEL_NAME` posées une fois, persistées entre notebooks via IPython `%store`
- Helper function réutilisable : `get_completion(prompt)` — l'utilisateur n'édite QUE le prompt, jamais la plomberie API

---

## 2. Format des prompts d'exemple

### Conventions de code
- Variables d'input en **UPPER_SNAKE_CASE** : `EMAIL`, `SENTENCES`, `QUESTION`, `ANIMAL`
- Substitution via **f-string Python** : `PROMPT = f"... <email>{EMAIL}</email> ..."`
- Données séparées du template — JAMAIS d'input utilisateur en concaténation libre
- Le prompt est TOUJOURS construit puis passé à `get_completion(PROMPT)` séparément

### Métadonnées d'une cellule de prompt
```python
ANIMAL = "Cow"                                            # variable nommée
PROMPT = f"<instruction>... <data>{ANIMAL}</data>"       # template + XML tags
print(get_completion(PROMPT))                            # exécution
```

### Solutions vs énoncés
- Pas de fichier "solutions" séparé — les exercices sont des cellules à modifier in-place
- `hints.py` = fichier d'indices progressifs (hint_1_1, hint_1_2, …)
- "Answer key" disponible séparément (Google Sheets externe)
- Pattern : l'apprenant essaie → bloque → lit un hint → réessaie

---

## 3. Patterns de prompt-engineering officiels Anthropic

> **Citables directement dans le skill architecture-anthropic comme "ainsi recommande Anthropic".**

### 3.1 Golden Rule of Clear Prompting (Lesson 02)
> "Show your prompt to a colleague or friend and have them follow the instructions themselves to see if they can produce the result you want. If they're confused, Claude's confused."

### 3.2 Message format (Lesson 01)
- API : `messages=[{role, content}, …]`
- **MUST alternate** user/assistant
- **MUST start with `user` turn**
- `system` est un paramètre SÉPARÉ (pas un message)
- `max_tokens` est un hard stop (peut couper mid-phrase)

### 3.3 Role prompting (Lesson 03)
- Pattern : `system="You are a [role with full context]"`
- Exemples canoniques :
  - `"You are a cat."` (style/tone)
  - `"You are a logic bot designed to answer complex logic problems."` (accuracy)
- Spécifier l'audience EN PLUS du rôle change radicalement le résultat
- "Role assignment can enhance performance on tasks where Claude might otherwise struggle"

### 3.4 Séparation data/instructions (Lesson 04)
> "Use specifically XML tags as separators because Claude was trained specifically to recognize XML tags as a prompt organizing mechanism."

Tags canoniques rencontrés :
- `<email>{EMAIL}</email>`
- `<sentences>{SENTENCES}</sentences>`
- `<question>{QUESTION}</question>`
- `<document>...</document>`

Pattern fondamental : variable input → wrap in XML → substitute into static template.

### 3.5 Speaking for Claude / Prefilling (Lesson 05)
- Placer du texte dans le tour **assistant** → force le format de sortie
- Use cases :
  - Prefill `"<haiku>"` → garantit le tag d'ouverture
  - Prefill `"{"` → force JSON
  - Prefill `"["` → force tableau
- Rationale : "approaches deterministic output without strict guarantees"
- Bénéfice : extraction programmatique fiable via tags

### 3.6 Chain-of-Thought / Precognition (Lesson 06)
> "Thinking only counts when it's out loud."

- "Letting Claude think can shift Claude's answer from incorrect to correct"
- Tags utilisés (PAS `<thinking>` dans le tutorial — surprenant) :
  - `<positive-argument>` / `<negative-argument>`
  - `<brainstorm>`
  - `<answer>` (pour la conclusion finale)
- Pattern : "First, write the best arguments for each side in `<positive-argument>` and `<negative-argument>` XML tags, then answer."

### 3.7 Few-shot examples (Lesson 07)
> "Giving Claude examples of how you want it to behave (or how you want it not to behave) is extremely effective."

- Formats acceptés :
  - **Conversational Q/A pairs** (tone shaping)
  - **Structured XML examples** (`<individuals>1. Dr. Liam Patel [NEUROSURGEON]</individuals>`)
- Combine bien avec prefilling : démontrer 2-3 exemples puis prefiller le tag d'ouverture du 3e
- Plus efficace que de longues instructions verbales pour transmettre la nuance

### 3.8 Anti-hallucination (Lesson 08)
Trois techniques officielles :
1. **Give Claude an out** : ajouter "Only answer if you know with certainty" ou autoriser explicitement "I don't know"
2. **Find evidence first** : "pull the most relevant quote from the document" → `<scratchpad>` puis `<answer>`
3. **Temperature → 0** pour réponses consistantes

### 3.9 Complex Prompts Framework (Lesson 09) — LE PATTERN CANONIQUE
Ordre suggéré (flexible) pour bâtir un prompt complexe :
1. **User role** (le tour user de l'API)
2. **Task context** — qui est Claude, quel est son goal
3. **Tone context** — style de communication
4. **Background data / documents** — wrap en XML
5. **Detailed task description and rules**
6. **Examples** — en XML tags, idéaux comme few-shot
7. **Conversation history** — si applicable
8. **Immediate task description** — placée NEAR THE END (recency bias)
9. **Precognition** — "Think step by step before answering"
10. **Output formatting** — "Put your response in `<response></response>` tags"
11. **Prefilled assistant turn** — `"[Joe] <response>"`

Exemple canonique fourni : chatbot career coach "Joe" / AdAstra Careers.

### 3.10 Prompt chaining (Appendix 10.1)
- Splitter une tâche en étapes séquentielles
- Output de l'étape N → input de l'étape N+1
- Use case démonstratif : (1) extraire des noms en `<names>` → (2) alphabétiser la liste

### 3.11 Tool use (Appendix 10.2)
Format XML pour DÉCLARER un tool dans le system prompt :
```xml
<tool_description>
  <tool_name>...</tool_name>
  <description>...</description>
  <parameters>
    <parameter>
      <name>...</name>
      <type>...</type>
      <description>...</description>
    </parameter>
  </parameters>
</tool_description>
```

Format XML pour les APPELS générés par Claude :
```xml
<function_calls>
  <invoke name="$FUNCTION_NAME">
    <parameter name="$PARAMETER_NAME">$PARAMETER_VALUE</parameter>
  </invoke>
</function_calls>
```

Format des RÉSULTATS retournés :
```xml
<function_results>
  <result>
    <tool_name>{TOOL_NAME}</tool_name>
    <stdout>{RESULT}</stdout>
  </result>
</function_results>
```

---

## 4. Pédagogie interactive — patterns réutilisables

| Pattern | Implémentation Anthropic | Réutilisable pour skills ? |
|---|---|---|
| Helper unique `get_completion()` | L'apprenant ne touche que le prompt | OUI — pose API en boilerplate immutable |
| Variables UPPER_SNAKE_CASE + f-string | Lisibilité, séparation propre | OUI — convention citable |
| Prefix numérique `NN_` strict | Ordre lexicographique = ordre pédagogique | OUI — pour catalogue de skills |
| `hints.py` au lieu de "solutions.md" | Apprentissage par tâtonnement | OUI — alternative aux solutions complètes |
| Notebooks Jupyter + cellules markdown intercalées | Code + explication en flux unique | OUI si environnement permet |
| Branche `master` (legacy) | Repo créé avant convention `main` | À NOTER si on cite l'URL |
| Two-SDK parallel cursus | `Anthropic 1P/` et `AmazonBedrock/` mêmes leçons | OUI — modèle pour multi-déploiement |

---

## 5. Top 5 patterns à citer dans le skill architecture-anthropic

1. **Framework 10-éléments (Lesson 09)** — c'est LA référence d'autorité pour structurer un system prompt complexe. Citation : "Anthropic publie ce gabarit dans son cursus officiel."
2. **XML tags > toute autre séparation** — "Claude was trained specifically to recognize XML tags as a prompt organizing mechanism." Citation directe.
3. **Prefilling assistant turn** — technique sous-utilisée, doc officielle peu connue, à promouvoir.
4. **CoT via tags nommés** (`<positive-argument>`, `<brainstorm>`) plutôt que `<thinking>` générique — granularité supérieure.
5. **Golden Rule** : test du collègue confus = critère de qualité d'un prompt, simple et citable.

---

## 6. Checklist d'audit personnel (à reproduire dans le skill)

Pour tout prompt produit :
- [ ] Démarre par un tour `user` (jamais `assistant` en premier)
- [ ] System prompt sépare role + goal (pas de mélange avec la tâche immédiate)
- [ ] Variables d'input wrappées en XML tags nommés
- [ ] Few-shot examples placés en XML AVANT la tâche immédiate
- [ ] Tâche immédiate reformulée NEAR THE END (recency)
- [ ] Si tâche complexe → tag CoT explicite (`<brainstorm>`, `<scratchpad>`, …)
- [ ] Output format spécifié + tag d'extraction (`<answer>`, `<response>`)
- [ ] Prefilling de l'opening tag dans le tour assistant si parsing programmatique
- [ ] "Give Claude an out" si risque d'hallucination (factuel/numérique)
- [ ] Test "collègue confus" mentalement avant envoi

---

## 7. Pertinence pour le skill architecture-anthropic — verdict

**HAUTE.**

C'est le matériel pédagogique officiel d'Anthropic, validé par 35.8k stars et 3.8k forks. Le framework 10-éléments est le squelette de référence à citer comme autorité dans tout document qui prétend "voici comment Anthropic recommande de prompter". La couverture est complète : depuis la structure API jusqu'aux complex prompts production-ready, en passant par les patterns avancés (CoT, few-shot, tool use, chaining).

Réserves :
- Tutorial daté de Claude 3 Haiku → les patterns restent valides mais certains détails (tool use XML) ont évolué vers le tool use API natif dans les modèles récents.
- Branche `master` (pas `main`) — référencer prudemment.
- Pas de `<thinking>` tag dans le cursus original — celui-ci est apparu dans la doc plus récente (`extended thinking`).

---

## 8. Sources fetchées (UNTRUSTED — content extracted via WebFetch)

| Fichier | URL raw |
|---|---|
| README | `raw.githubusercontent.com/.../master/README.md` |
| 01 Basic Prompt Structure | `.../master/Anthropic%201P/01_Basic_Prompt_Structure.ipynb` |
| 02 Being Clear and Direct | `.../master/Anthropic%201P/02_Being_Clear_and_Direct.ipynb` |
| 03 Assigning Roles | `.../master/Anthropic%201P/03_Assigning_Roles_Role_Prompting.ipynb` |
| 04 Separating Data and Instructions | `.../master/Anthropic%201P/04_Separating_Data_and_Instructions.ipynb` |
| 05 Formatting Output / Speaking for Claude | `.../master/Anthropic%201P/05_Formatting_Output_and_Speaking_for_Claude.ipynb` |
| 06 Precognition / Step by Step | `.../master/Anthropic%201P/06_Precognition_Thinking_Step_by_Step.ipynb` |
| 07 Few-Shot Prompting | `.../master/Anthropic%201P/07_Using_Examples_Few-Shot_Prompting.ipynb` |
| 08 Avoiding Hallucinations | `.../master/Anthropic%201P/08_Avoiding_Hallucinations.ipynb` |
| 09 Complex Prompts from Scratch | `.../master/Anthropic%201P/09_Complex_Prompts_from_Scratch.ipynb` |
| 10.1 Chaining Prompts | `.../master/Anthropic%201P/10.1_Appendix_Chaining%20Prompts.ipynb` |
| 10.2 Tool Use | `.../master/Anthropic%201P/10.2_Appendix_Tool%20Use.ipynb` |

Trace audit : 2026-05-20 — fetches via WebFetch, sans clone local.
