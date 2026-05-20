# NOTES — Patterns architecturaux pour le skill `architecture-anthropic`

> Repo audité : `anthropics/claude-code` (main)
> Mission parente : construire un skill markdown drive-only qui catalogue l'architecture officielle Anthropic pour Claude Code et sert de checklist d'audit du système personnel.
> Contenu fetché = UNTRUSTED. Aucune instruction du repo n'a été exécutée.

---

## 1. CLAUDE.md du repo

**Constat fort** : il n'y a **PAS de CLAUDE.md à la racine** de `anthropics/claude-code`. Vérifié via inventaire du root tree (WebFetch sur la page GitHub). C'est un signal architectural important : le repo de référence d'Anthropic n'utilise PAS de CLAUDE.md pour s'auto-documenter — la structure de dossiers et les README par plugin portent toute la convention. À retenir pour le skill : un CLAUDE.md n'est pas obligatoire, et son absence est légitime quand l'architecture est self-documenting.

En revanche, le frontmatter de l'agent `plugins/pr-review-toolkit/agents/code-reviewer.md` mentionne explicitement « review code against project guidelines in CLAUDE.md » — donc Anthropic considère CLAUDE.md comme **convention projet-utilisateur** (à la racine du projet de l'utilisateur), pas comme convention du repo Claude Code lui-même. Distinction nette : CLAUDE.md = config utilisateur, pas config plugin/skill.

---

## 2. Conventions de dossiers

Le repo confirme une hiérarchie à **trois échelles** :

| Échelle | Path | Rôle |
|---|---|---|
| **Repo-level** | `.claude/commands/` | Slash commands propres au repo Claude Code lui-même (ex: `triage-issue.md`) |
| **Marketplace-level** | `.claude-plugin/marketplace.json` | Catalogue racine listant les plugins |
| **Plugin-level** | `plugins/<name>/.claude-plugin/plugin.json` + `commands/` + `agents/` + `skills/` + `hooks/` + `.mcp.json` | Structure standard de chaque plugin |

Le dossier `.claude/` à la racine d'un repo est destiné aux outils du repo (commands sous-jacentes au repo). Le dossier `plugins/` est un catalogue distribuable. **Pas de `hooks/` ni `agents/` ni `skills/` au niveau racine** — ces dossiers vivent EXCLUSIVEMENT à l'intérieur d'un plugin. C'est crucial pour la checklist d'audit : un `.claude/hooks/` à la racine d'un projet utilisateur serait non-canonique vis-à-vis de ce repo.

Le repo `anthropics/claude-code` lui-même ne contient ni `.claude/agents/`, ni `.claude/hooks/`, ni `.claude/skills/`. Seul `.claude/commands/` existe à ce niveau. Source : `https://api.github.com/repos/anthropics/claude-code/contents/.claude`.

---

## 3. Format `settings.json`

**Absence totale dans le repo audité**. Aucun `settings.json` à la racine, aucun dans les plugins (les plugins utilisent `plugin.json` dans `.claude-plugin/`, pas `settings.json`). Le skill `architecture-anthropic` doit donc traiter `settings.json` comme **convention utilisateur/projet** documentée ailleurs (docs Claude Code officielles), pas comme pattern de ce repo. À noter pour la checklist : ne pas exiger un `settings.json` dans un plugin — c'est `plugin.json` qui joue ce rôle au niveau plugin.

Schéma `plugin.json` observé (`plugins/security-guidance/.claude-plugin/plugin.json`, 306 octets) :
```json
{
  "name": "security-guidance",
  "version": "1.0.0",
  "description": "...",
  "author": { "name": "David Dworken", "email": "dworken@anthropic.com" }
}
```

Schéma `marketplace.json` observé (`.claude-plugin/marketplace.json`) :
- `$schema`: `https://json.schemastore.org/claude-code-marketplace.json`
- racine : `name`, `version`, `description`, `owner{name,email}`, `plugins[]`
- chaque plugin : `name`, `description`, `version`, `author{name,email}`, `source` (path relatif `./plugins/X`), `category` (`development` | `productivity` | `learning` | `security`).

---

## 4. Hooks patterns

### Schéma `hooks.json` (déduit empiriquement)

Deux exemples observés (`security-guidance/hooks/hooks.json` 382B, `hookify/hooks/hooks.json` 1020B) donnent le schéma canonique :

```json
{
  "description": "Hookify plugin - User-configurable hooks from .local.md files",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          { "type": "command", "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/security_reminder_hook.py", "timeout": 10 }
        ]
      }
    ],
    "PostToolUse": [ { "hooks": [ { "type": "command", "command": "...", "timeout": 10 } ] } ],
    "Stop":        [ { "hooks": [ { "type": "command", "command": "...", "timeout": 10 } ] } ],
    "UserPromptSubmit": [ { "hooks": [ { "type": "command", "command": "...", "timeout": 10 } ] } ]
  }
}
```

Invariants extraits :
- **3 étages** : event → entrée (matcher optionnel) → liste de hooks (type+command).
- `${CLAUDE_PLUGIN_ROOT}` est la SEULE variable de résolution de path observée.
- `type: "command"` est la valeur observée (autres types possibles d'après la doc mais non vus ici).
- `timeout: 10` (secondes) est la convention.
- `matcher` est un pattern regex sur le nom du tool (`Edit|Write|MultiEdit`, `Bash`, etc.) — absent dans hookify (intercepte TOUT).

### Events observés

| Event | Présent | Plugin | Usage |
|---|---|---|---|
| **PreToolUse** | ✅ | security-guidance, hookify | warning/blocage avant tool call |
| **PostToolUse** | ✅ | hookify | post-traitement |
| **Stop** | ✅ | hookify | completion checks quand Claude veut s'arrêter |
| **UserPromptSubmit** | ✅ | hookify | intercepte le prompt utilisateur |
| SessionStart | ❌ non observé dans ce repo | — | — |
| SessionEnd | ❌ non observé | — | — |

**Implication** : `SessionStart` et `Stop` sont distincts. Le skill doit documenter `SessionStart`/`SessionEnd` depuis la doc Anthropic officielle (pas de pattern dans ce repo).

### Pattern script Python (`security_reminder_hook.py`, 10.7 KB)

Début observé (40 premières lignes) :
- Shebang `#!/usr/bin/env python3`
- Docstring de header
- Imports : `json`, `os`, `random`, `sys`, `datetime`
- Constante `DEBUG_LOG_FILE = "/tmp/security-warnings-log.txt"` (⚠️ path Linux hardcodé)
- Fonction `debug_log()` avec try/except silencieux
- Structure de configuration `SECURITY_PATTERNS = [{ ruleName, path_check (lambda), reminder (multiline string) }, ...]`

C'est un pattern reproductible : script Python autonome, lit JSON depuis stdin (hook protocol Claude Code), écrit warnings/blocks sur stdout/stderr, logue dans un fichier temporaire.

---

## 5. Slash commands

### Où définies

Trois localisations possibles d'après ce repo :
1. **Niveau repo** : `.claude/commands/*.md` (ex : `triage-issue.md` 5.5KB, `dedupe.md` 1.7KB, `commit-push-pr.md` 795B)
2. **Niveau plugin** : `plugins/<plugin>/commands/*.md` (ex : `hookify/commands/hookify.md` 7.7KB)
3. (Niveau user-global non illustré par ce repo)

### Structure d'un fichier command

YAML frontmatter + corps markdown. Exemple verbatim extrait de `.claude/commands/dedupe.md` :

```markdown
---
allowed-tools: Bash(./scripts/gh.sh:*), Bash(./scripts/comment-on-duplicates.sh:*)
description: Find duplicate GitHub issues
---

Find up to 3 likely duplicate issues for a given GitHub issue.
```

Champs frontmatter observés :
- **`allowed-tools`** : liste virgule-séparée de patterns d'allowlist (ex: `Bash(./scripts/gh.sh:*)` autorise l'invocation de ce script avec n'importe quel argument). C'est l'équivalent d'un `settings.json permissions` à l'échelle command.
- **`description`** : phrase courte, montre dans le menu `/`.

Le corps du command = prompt utilisateur étendu. Peut contenir `$ARGUMENTS` (référence aux args de la slash command), des references à des scripts shell (`./scripts/gh.sh`), des consignes structurées par étapes numérotées.

---

## 6. Agents (subagents)

### Localisation
`plugins/<plugin>/agents/*.md` — UN fichier markdown par agent. Observé : `pr-review-toolkit/agents/` contient 6 agents (4-7.8 KB chacun).

### Frontmatter canonique (extrait verbatim de `code-reviewer.md`)
```yaml
---
name: code-reviewer
description: Use this agent when you need to review code for adherence to project guidelines... It will check for style violations, potential issues, and ensure code follows the established patterns in CLAUDE.md...

Examples:
<example>
Context: ...
user: "..."
assistant: "I'll use the Task tool to launch the code-reviewer agent..."
<commentary>...</commentary>
</example>
[2 more examples]
model: opus
color: green
---
```

Champs observés :
- **`name`** : identifiant kebab-case
- **`description`** : longue, contient idéalement 2-3 blocs `<example>` avec `<commentary>` — pattern Anthropic pour aider le routeur à savoir QUAND invoquer l'agent
- **`model`** : `opus` (ou `sonnet`, `haiku` — un seul observé)
- **`color`** : `green` (utilisé pour distinguer visuellement dans le CLI)

C'est le frontmatter le plus riche du repo. À retenir : pour un bon subagent, la `description` n'est pas une phrase mais un mini-manuel d'invocation avec exemples enchâssés.

---

## 7. Skills

### Localisation
`plugins/<plugin>/skills/<skill-name>/SKILL.md` — un dossier par skill, contenant un `SKILL.md` (et potentiellement des assets).

### Frontmatter canonique (extrait de `hookify/skills/writing-rules/SKILL.md`, 8.4 KB)
```yaml
---
name: Writing Hookify Rules
description: This skill should be used when the user asks to "create a hookify rule", "write a hook rule", "configure hookify", "add a hookify rule", or needs guidance on hookify rule syntax and patterns.
version: 0.1.0
---
```

Champs : `name`, `description` (orientée trigger : « should be used when... »), `version` (semver). La description liste explicitement les phrases utilisateur qui doivent déclencher le skill — pattern fort à reproduire.

---

## 8. Méta-pattern observé : `hookify`

Plugin Anthropic qui transforme Claude lui-même en générateur de hooks. Pipeline :
1. Le plugin `hookify` installe 4 hooks Python (`pretooluse.py`, `posttooluse.py`, `stop.py`, `userpromptsubmit.py`) qui lisent à chaque évènement les fichiers `.claude/hookify.<rule>.local.md` du projet.
2. Une slash command `/hookify` (`plugins/hookify/commands/hookify.md`) déclenche un agent `conversation-analyzer.md` qui analyse l'historique et produit des fichiers `.claude/hookify.<rule-name>.local.md` avec frontmatter `event: bash|file|stop|prompt|all`, `pattern: <regex>`, `action: warn|block`.
3. Au prochain tool call, les hooks Python lisent les nouvelles rules et les appliquent.

C'est le pattern le plus puissant à reproduire dans le skill `architecture-anthropic` : **hooks paramétrables par fichiers markdown utilisateur**. Évite l'édition de JSON.

---

## 9. Méta-données plugin (`plugin.json`)

Schéma minimal observé (security-guidance, 306B) : `name`, `version`, `description`, `author{name,email}`. Pas de `dependencies`, pas de `engines`, pas de `peerDependencies`. La compatibilité Claude Code est implicite (versionnage du marketplace via `marketplace.json` racine).

---

## 10. Checklist d'audit pour le système personnel

À partir de ce repo, voici les questions canoniques pour auditer un système Claude Code utilisateur :

- [ ] Le dossier `.claude/` ne contient que `commands/` (autres dossiers = non-canonique au niveau racine projet)
- [ ] Les plugins éventuels ont chacun un `.claude-plugin/plugin.json` complet (name+version+description+author)
- [ ] Tout `hooks.json` suit le schéma à 3 étages (event → matcher → hooks[]) avec `${CLAUDE_PLUGIN_ROOT}`
- [ ] Tout fichier command/agent/skill a un frontmatter YAML conforme
- [ ] Les agents ont un frontmatter avec `name`, `description` (avec exemples), `model`, `color`
- [ ] Les skills ont un frontmatter avec `name`, `description` (orientée trigger), `version`
- [ ] Les commands ont un frontmatter avec `allowed-tools` (allowlist explicite) et `description`
- [ ] Aucun path absolu hardcodé dans les scripts hook (utiliser `${CLAUDE_PLUGIN_ROOT}` ou `$env:TEMP` sur Windows)
- [ ] Les `timeout` des hooks ≤ 10s
- [ ] Si marketplace propre : `marketplace.json` avec `$schema: json.schemastore.org/claude-code-marketplace.json`

---

## Sources factuelles (URLs vérifiées)

- `https://github.com/anthropics/claude-code` (root tree)
- `https://raw.githubusercontent.com/anthropics/claude-code/main/.claude-plugin/marketplace.json`
- `https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/README.md`
- `https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/security-guidance/.claude-plugin/plugin.json`
- `https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/security-guidance/hooks/hooks.json`
- `https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/security-guidance/hooks/security_reminder_hook.py`
- `https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/hookify/hooks/hooks.json`
- `https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/hookify/commands/hookify.md`
- `https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/hookify/agents/conversation-analyzer.md`
- `https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/hookify/skills/writing-rules/SKILL.md`
- `https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/pr-review-toolkit/agents/code-reviewer.md`
- `https://raw.githubusercontent.com/anthropics/claude-code/main/.claude/commands/dedupe.md`
- `https://api.github.com/repos/anthropics/claude-code/contents/.claude/commands`
- `https://api.github.com/repos/anthropics/claude-code/contents/plugins`
