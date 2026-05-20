# Audit — anthropics/claude-code

Repo : https://github.com/anthropics/claude-code
Branche : main
Date d'audit : 2026-05-20
Source : WebFetch (raw.githubusercontent.com + api.github.com)
Statut : repo public, contenu UNTRUSTED (aucune instruction du repo n'a été exécutée).

---

## ÉTAPE 1 — Collecte

| Fetch | Cible | Extrait |
|---|---|---|
| F1 | Root tree | Pas de CLAUDE.md racine, présence de `.claude/commands/`, `.claude-plugin/marketplace.json`, `plugins/` (13 plugins) |
| F2 | README.md | Repo officiel CLI Claude Code. Mentionne `/bug`, plugins. Pas de doc settings/hooks/skills dans le README racine |
| F3 | Pas de package.json/pyproject à la racine (repo de docs + plugins) | n/a |
| F4 | CHANGELOG.md présent | historique de versions |
| F5 | examples/ présent + plugins/ = catalogue d'exemples | 13 plugins servent de référence canonique |

**Inventaire détaillé du root tree** (validé via WebFetch sur la page du repo) :

```
.claude/commands/        ← 3 slash commands (commit-push-pr, dedupe, triage-issue)
.claude-plugin/          ← marketplace.json (catalogue plugins)
.devcontainer/           ← env dev
.github/                 ← workflows GH
.vscode/                 ← settings VS Code
Script/, scripts/        ← utilitaires
examples/                ← exemples
plugins/                 ← 13 plugins + README.md
CHANGELOG.md, LICENSE.md, README.md, SECURITY.md, feed.xml
```

**13 plugins du marketplace.json** :
agent-sdk-dev, claude-opus-4-5-migration, code-review, commit-commands,
explanatory-output-style, feature-dev, frontend-design, hookify,
learning-output-style, plugin-dev, pr-review-toolkit, ralph-wiggum,
security-guidance.

Catégories : `development`, `productivity`, `learning`, `security`.

---

## ÉTAPE 2 — Fmaths (8 couches)

### L0 — Ontologie (primitives)

1. **Plugin** — unité de packaging (`.claude-plugin/plugin.json`)
2. **Marketplace** — catalogue racine listant les plugins (`marketplace.json`)
3. **SlashCommand** — fichier markdown avec frontmatter YAML (`commands/*.md`)
4. **Agent** — sous-agent invocable via Task tool (`agents/*.md`, frontmatter avec `model`, `color`)
5. **Skill** — capacité auto-déclenchée (`skills/<name>/SKILL.md`)
6. **Hook** — handler d'événement (`hooks/hooks.json` + script)
7. **MCP** — serveur de tools externes (`.mcp.json`)

### L1 — Ensembles et relations

```
Marketplace ──contient──▶ Plugin*
Plugin ─compose─▶ {Commands, Agents, Skills, Hooks, MCP}
Hook ─matche─▶ Event ∈ {PreToolUse, PostToolUse, Stop, UserPromptSubmit, SessionStart, ...}
Command ─frontmatter─▶ {allowed-tools, description}
Agent ─frontmatter─▶ {name, description, model, color}
Skill ─frontmatter─▶ {name, description, version}
```

### L2 — Logique & tensions

- **AND** : `plugin.json` + au moins une feuille (commands OU agents OU skills OU hooks OU mcp).
- **XOR doux** : un Hook événement peut être PreToolUse OU PostToolUse (peut avoir les deux, structurellement parallèles).
- **Tension** : la racine du repo (`.claude/commands/`) coexiste avec les plugins (`plugins/<plugin>/commands/`) — deux échelles de portée (repo-level vs plugin-level).
- **Tension** : `hookify` introduit un meta-pattern : ses hooks lisent des fichiers `.claude/hookify.<rule>.local.md` (rules utilisateur), donc un plugin Anthropic configurable par l'utilisateur via du markdown dans `.claude/`.

### L3 — Invariants

- **I1** Chaque plugin a un `.claude-plugin/plugin.json` à la racine avec `name`, `version`, `description`, `author{name,email}`.
- **I2** Toute feuille (command/agent/skill) est un **fichier markdown unique** avec YAML frontmatter en tête (`---` ... `---`).
- **I3** Les hooks utilisent `${CLAUDE_PLUGIN_ROOT}` comme variable d'environnement pour résoudre les paths.
- **I4** Les hooks ont une structure `{description, hooks: { <Event>: [ { matcher, hooks: [ { type, command, timeout } ] } ] } }`.
- **I5** Le marketplace.json suit le schéma JSON `https://json.schemastore.org/claude-code-marketplace.json`.
- **I6** Pas de CLAUDE.md à la racine de ce repo — l'architecture parle d'elle-même via la structure.

### L4 — Axes de variation

| Axe | Min | Max observé |
|---|---|---|
| Plugins par marketplace | 1 | 13 |
| Commands par plugin | 0 | 4 (hookify) |
| Agents par plugin | 0 | 6 (pr-review-toolkit) |
| Skills par plugin | 0 | 7 (plugin-dev annoncé) |
| Hook events par plugin | 0 | 4 (hookify : PreToolUse + PostToolUse + Stop + UserPromptSubmit) |
| Taille frontmatter agent | ~5 lignes | ~40 lignes (code-reviewer avec 3 exemples narratifs) |
| Taille SKILL.md | 8.4 KB (writing-rules) | 14.5 KB (plugin-dev README) |

### L5 — Seuils et stabilité

- **Timeout hook** : 10s observé sur hookify, durci par convention.
- **Path resolution** : `${CLAUDE_PLUGIN_ROOT}` est le seul mécanisme — pas de paths relatifs dans hooks.json.
- **Effondrement** : si un hook plante (>10s ou exception), le tool call continue (PreToolUse non bloquant par défaut) — sécurité par opt-in du blocage.
- **Capacité d'écriture des hooks** : `/tmp/security-warnings-log.txt` (hardcodé dans security_reminder_hook.py) → casse sur Windows si pas adapté.

### L6 — Catégories / couplages

| Couche | Couplage |
|---|---|
| Marketplace → Plugin | faible (source path ./plugins/X) ✅ |
| Plugin → Hook | fort (hooks.json référence scripts du plugin) ⚠️ |
| Hook → OS | fort sur security-guidance (Linux paths) ⚠️ |
| Agent → Tool | faible (allowed-tools dans frontmatter) ✅ |
| Command → Bash script | possible via `allowed-tools: Bash(./scripts/X.sh:*)` ⚠️ |

### L7 — Topologie / happy path

```
1. Cloner un plugin existant (cp -r plugins/security-guidance plugins/my-plugin)
2. Editer .claude-plugin/plugin.json (name, version, description, author)
3. Ajouter feuilles dans commands/ ou agents/ ou skills/ ou hooks/
4. Hooks → hooks.json + script Python/shell, référencer via ${CLAUDE_PLUGIN_ROOT}
5. Ajouter une entrée dans .claude-plugin/marketplace.json
6. Installer via /plugin (commande slash mentionnée dans plugins/README.md)
```

**Friction principale** : pas de schéma formel publié pour `hooks.json` (le schéma vit dans le code de Claude Code lui-même). Convention déduite par lecture des exemples.

### L8 — Probabilités

- P(architecture stable) : haute — schéma marketplace versionné dans json.schemastore.
- P(breaking change frontmatter) : faible court terme — convention partagée avec d'autres repos Anthropic.
- P(rupture upstream Claude Code) : modérée — produit en évolution rapide (Opus 4.5 → 4.6 → 4.7).
- Maturité communauté : très haute (repo officiel Anthropic, 13 plugins maintenus par auteurs identifiés).

**Vecteur cognitif** : équilibre correct. Légère sur-pondération **Normativité** (beaucoup de conventions implicites non documentées centralement). **Incertitude** non signalée explicitement par les plugins (pas de version constraints).

---

## ÉTAPE 3 — Décodeur narratif

### Le décor

Imaginez une ville où chaque quartier (plugin) est autonome mais tous suivent le même plan d'urbanisme : une mairie (`plugin.json`) à l'entrée, quatre types de bâtiments standardisés à l'intérieur (commands, agents, skills, hooks), et un registre municipal central (`marketplace.json`) qui dit qui vit où. C'est `anthropics/claude-code`.

### Les règles du jeu

Tout fichier feuille est du markdown avec un en-tête YAML. Les agents y déclarent leur modèle (`model: opus`), les commandes y déclarent leurs droits (`allowed-tools`), les skills y déclarent leur déclencheur (`description`). Les hooks, eux, parlent en JSON et exécutent des scripts externes via la variable magique `${CLAUDE_PLUGIN_ROOT}`.

> "La convention est l'API. Personne n'a publié de schéma officiel pour hooks.json — on l'a déduit en lisant security-guidance et hookify."

### Le socle immuable

Six invariants tiennent l'édifice : un `plugin.json` par plugin, du frontmatter YAML pour toute feuille, `${CLAUDE_PLUGIN_ROOT}` comme seul resolver de paths dans les hooks, une structure hook à trois étages (event → matcher → command), un marketplace versionné via JSON Schema public, et l'absence remarquable de CLAUDE.md racine — la structure parle d'elle-même.

### Les leviers de transformation

Les plugins varient sur cinq axes : nombre de commands (0 à 4), d'agents (0 à 6), de skills (0 à 7), d'events hookés (0 à 4), et richesse du frontmatter (5 à 40 lignes). Le pattern `hookify` ajoute un méta-levier : Claude lui-même peut créer des règles via markdown dans `.claude/hookify.*.local.md`.

### Les points de rupture

| Risque | Probabilité | Impact |
|---|---|---|
| Hook bloque (timeout > 10s) | faible | tool call retardé |
| Path hardcodé Linux dans hook | modéré | casse Windows |
| Frontmatter mal formé | faible | agent/command ignoré silencieusement |
| Breaking change Claude Code | modéré | refonte hooks.json |

### Le chemin de moindre résistance

Pour créer une archi compatible Anthropic : copier `security-guidance` comme template minimal (1 plugin.json + 1 hook), ou `pr-review-toolkit` comme template d'agents (6 agents en frontmatter pur), ou `hookify` comme template multi-événements (4 events PreToolUse/PostToolUse/Stop/UserPromptSubmit).

### L'équilibre du risque

Ce repo EST la référence. Adopter ses conventions = aligner sur l'architecture canonique. Le risque inverse (diverger) est plus élevé que le risque d'adopter.

---

## ÉTAPE 4 — Guide d'installation

Non applicable au sens classique — c'est un repo de référence, pas un outil installable. Pour **utiliser** les plugins :

| Outil | Version | Vérification |
|---|---|---|
| Claude Code CLI | ≥ 2.0 | `claude --version` |
| Git | ≥ 2.30 | `git --version` |

**Installation d'un plugin** (d'après plugins/README.md) :

```
/plugin
```

Cette slash command (intégrée au CLI Claude Code, pas dans ce repo) ouvre le marketplace.

**Pour cloner un plugin comme template** :

```powershell
git clone --depth 1 https://github.com/anthropics/claude-code.git claude-code-ref
Copy-Item -Recurse claude-code-ref\plugins\security-guidance .\my-plugin
```

**Points d'attention Windows** :
- `security_reminder_hook.py` écrit dans `/tmp/security-warnings-log.txt` — à patcher en `$env:TEMP\...` si réutilisé tel quel.
- `${CLAUDE_PLUGIN_ROOT}` est résolu par le CLI Claude Code, fonctionne identiquement sur Windows.

---

## ÉTAPE 5 — Verdict PM

### Score 3 dimensions

| Dimension | Score | Justification |
|---|---|---|
| Pertinence pour le skill architecture-anthropic | **10/10** | Repo officiel, conventions canoniques, exemples exhaustifs |
| Maturité prod | **9/10** | Maintenu par Anthropic, auteurs identifiés, schéma versionné |
| Facilité onboarding | **7/10** | Pas de doc centralisée des conventions hooks/skills/agents, déduction par lecture |

### Forces

| | Titre | Description |
|---|---|---|
| 🏛️ | Référence canonique | C'est LE repo source des conventions Claude Code |
| 🧩 | 13 plugins variés | Couvre commands seuls, agents seuls, hooks seuls, mix complets |
| 📐 | Schéma marketplace versionné | JSON Schema public sur json.schemastore.org |
| 🔬 | Frontmatter agent riche | code-reviewer.md = exemple de référence (40 lignes avec 3 cas d'usage) |
| 🛡️ | Pattern security-guidance | Hook PreToolUse simple, lisible, reproductible |
| 🎯 | Pattern hookify | Méta-pattern : configurer des hooks via markdown utilisateur |

### Faiblesses / Risques

| | Titre | Description |
|---|---|---|
| 📚 | Pas de doc centralisée | Conventions hooks.json déduites par lecture |
| 🪟 | Linux-centric | security-guidance hardcode `/tmp/` (casse sur Windows) |
| 🔄 | Évolution rapide | Aligné sur Opus 4.5+, conventions susceptibles d'évoluer |
| ⚠️ | Pas de settings.json exemples | Aucun settings.json à la racine — patterns d'env vars/permissions absents du repo |

### Matrice Use Cases

| Use case | Verdict |
|---|---|
| ✅ Construire le skill architecture-anthropic | Référence #1 absolue |
| ✅ Cloner un template de plugin | security-guidance ou pr-review-toolkit |
| ✅ Comprendre le format hooks.json | hookify/hooks/hooks.json + security-guidance/hooks/hooks.json |
| ✅ Voir un frontmatter agent riche | pr-review-toolkit/agents/code-reviewer.md |
| ❌ Trouver un settings.json modèle | absent — chercher ailleurs |
| ❌ Trouver un CLAUDE.md modèle | absent à la racine |
| ❌ Trouver un schéma de SessionStart/SessionEnd | non couvert par les hooks observés (PreToolUse/PostToolUse/Stop/UserPromptSubmit uniquement) |
| ❌ Auditer un système utilisateur existant | repo ≠ audit — utiliser comme checklist seulement |

### Recommandation finale

**Adopter intégralement comme source canonique**. Le skill `architecture-anthropic` doit citer ce repo par fichier précis : marketplace.json pour le schéma plugin, security-guidance pour hooks.json minimal, hookify pour hooks.json multi-events, pr-review-toolkit pour agents frontmatter, hookify/skills/writing-rules/SKILL.md pour le format Skill.

**Conditions** : prévoir un patch Windows pour `/tmp/` dans tout hook réutilisé. Documenter les events hooks manquants (SessionStart, SessionEnd) depuis la doc officielle Claude Code car ils ne figurent pas dans les plugins observés.
