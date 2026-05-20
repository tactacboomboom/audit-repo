# Installation — anthropics/skills

Le repo `anthropics/skills` n'est PAS un package à installer, c'est un **dépôt de skills à consommer**. Deux scénarios distincts.

## Scénario A — Utiliser les skills officiels Anthropic

### Prérequis
| Outil | Version | Vérification |
|---|---|---|
| Claude Code | ≥ récente | `claude --version` |
| Git | ≥ 2.30 | `git --version` |

### Option A1 — Via `/plugin install` (le plus rapide)
```powershell
# Dans Claude Code, depuis le repl
/plugin install document-skills
/plugin install example-skills
/plugin install claude-api
```
Les trois plugins du marketplace sont définis dans `.claude-plugin/marketplace.json`. Chacun référence un sous-ensemble des 17 skills.

### Option A2 — Skill par skill (manuel)
```powershell
# Cloner shallow uniquement le repo
git clone --depth 1 https://github.com/anthropics/skills.git $env:TEMP\anthropics-skills

# Copier un skill spécifique dans le dossier skills global
Copy-Item -Recurse "$env:TEMP\anthropics-skills\skills\skill-creator" "$env:USERPROFILE\.claude\skills\"
```
> **Alert (warn)** : sur Windows, les chemins avec espace doivent être quotés. PowerShell utilise `$env:USERPROFILE`, pas `$HOME` (qui marche aussi mais convention).

## Scénario B — Créer ses propres skills en suivant la spec

### Prérequis
| Outil | Version | Vérification |
|---|---|---|
| Python | ≥ 3.10 | `python --version` |
| uv (optionnel, rapide) | dernière | `uv --version` |
| skills-ref (linter spec) | dernière | `skills-ref --version` |

### Installation du linter officiel
```powershell
# Depuis le repo agentskills/agentskills (PAS anthropics/skills)
pip install skills-ref
# OU avec uv
uv tool install skills-ref
```

### Workflow minimal
```powershell
# 1. Cloner le template
mkdir my-skill
Set-Location my-skill

# 2. Créer SKILL.md
@'
---
name: my-skill
description: <Action concrète>. Use this skill when <liste de déclencheurs explicites>.
---

# My Skill

## Quand utiliser
...

## Comment faire
...
'@ | Out-File -Encoding utf8 SKILL.md

# 3. Valider
skills-ref validate .

# 4. (Optionnel) Eval harness via skill-creator
# Suivre la procédure skill-creator/SKILL.md
```

### Config minimale `SKILL.md`
```yaml
---
name: my-skill              # OBLIGATOIRE — doit matcher le dossier parent
description: <≤1024 chars>  # OBLIGATOIRE — QUOI + QUAND avec mots-clés
license: Complete terms in LICENSE.txt  # optionnel
compatibility: Requires Python 3.14+    # optionnel, ≤500 chars
metadata:                                # optionnel, libre
  author: yanis
  version: "1.0"
allowed-tools: Bash(git:*) Read         # optionnel, EXPÉRIMENTAL
---

# Corps markdown ici
```

### Vérification que tout fonctionne
```powershell
# Lint
skills-ref validate ./my-skill

# Test d'activation (depuis Claude Code)
# 1. Installer le skill : copier dans ~/.claude/skills/
# 2. Lancer Claude Code
# 3. Vérifier dans la liste des skills disponibles : votre name doit apparaître
```

## Points d'attention OS-specific (Windows / PowerShell)

> **Alert (warn)** — Encodage : PowerShell 5.1 par défaut écrit en UTF-16 LE avec BOM. Pour SKILL.md utilisez `Out-File -Encoding utf8` ou éditez avec VS Code.

> **Alert (warn)** — Chemins avec espaces : toujours quoter (`"G:\Mon Drive\..."`).

> **Alert (warn)** — `&&` PowerShell 5.1 : pas supporté. Utilisez `;` ou `if ($?) { ... }`.

> **Alert (danger)** — `allowed-tools` : champ EXPÉRIMENTAL d'après la spec. Ne jamais en faire dépendre la sécurité d'un workflow critique. Toujours valider côté agent.

## Désinstallation
```powershell
# Skill installé manuellement
Remove-Item -Recurse "$env:USERPROFILE\.claude\skills\<skill-name>"

# Plugin installé via /plugin
/plugin uninstall <plugin-name>
```
