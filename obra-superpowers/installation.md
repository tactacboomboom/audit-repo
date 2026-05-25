---
name: superpowers-installation
description: Installation obra/superpowers v5.1.0 — commandes par agent (Claude Code, Cursor, Gemini, Codex, Factory, Copilot), workflow 7 étapes post-install, warnings Windows PowerShell. Charger quand on installe ou configure.
---

# Installation — obra/superpowers v5.1.0

## Prérequis

| Outil | Version min | Vérification |
|---|---|---|
| Git | 2.30+ | `git --version` |
| Agent de code | Voir tableau ci-dessous | — |
| Node.js | Non requis (runtime) | — |

## Agents supportés

| Agent | Commande d'installation |
|---|---|
| Claude Code (CLI) | `/plugin install superpowers@claude-plugins-official` |
| Codex CLI / App | Rechercher "Superpowers" dans le marketplace officiel |
| Factory Droid | `droid plugin install superpowers@superpowers` |
| Gemini CLI | `gemini extensions install https://github.com/obra/superpowers` |
| Cursor | `/add-plugin superpowers` |
| GitHub Copilot CLI | `copilot plugin install superpowers@superpowers-marketplace` |

---

## Option A — Installation rapide (recommandée)

### Claude Code

```bash
# Dans une session Claude Code active
/plugin install superpowers@claude-plugins-official
```

Après installation, relancer la session. Les 14 skills sont disponibles. Le hook `session-start` s'initialise automatiquement.

### Gemini CLI

```bash
gemini extensions install https://github.com/obra/superpowers
```

---

## Option B — Depuis le source (pour contribuer ou personnaliser)

```bash
# 1. Cloner le repo
git clone https://github.com/obra/superpowers.git
cd superpowers

# 2. Lier localement à votre agent
# Pour Claude Code, copier le dossier plugin
cp -r .claude-plugin/ ~/.claude/plugins/superpowers/

# 3. Vérifier la structure
ls skills/
# Attendu : brainstorming/ dispatching-parallel-agents/ executing-plans/ ...
```

---

## Config minimale

Aucun fichier `.env` requis. Le `package.json` est minimal :

```json
{
  "name": "superpowers",
  "version": "5.1.0",
  "type": "module",
  "main": ".opencode/plugins/superpowers.js"
}
```

Les hooks se configurent automatiquement via `hooks/hooks.json` (tous agents) et `hooks/hooks-cursor.json` (Cursor spécifiquement).

---

## Commandes de vérification

Après installation Claude Code, dans une nouvelle session :

```
# Vérifier que les skills sont disponibles
/skills

# Lancer le premier skill
/brainstorm

# Confirmer le workflow complet
/using-superpowers
```

Résultat attendu : Claude propose une session de brainstorming socratique.

---

## Workflow de base post-install

```bash
# 1. Brainstorming
/brainstorm "Votre idée ou problème"

# 2. Isolation (créé automatiquement par le skill)
# → git worktree add ../feature-branch feature/ma-feature

# 3. Planification
/writing-plans

# 4. Exécution (avec subagents optionnels)
/executing-plans

# 5. TDD (obligatoire — RED avant GREEN)
/test-driven-development

# 6. Review
/requesting-code-review
/receiving-code-review

# 7. Finalisation
/verification-before-completion
/finishing-a-development-branch
```

---

## Points d'attention Windows (PowerShell)

```
⚠️ WARN — hooks-cursor.json
Cursor sur Windows utilise un fichier de hooks séparé (hooks/hooks-cursor.json).
Si les skills ne s'activent pas dans Cursor, vérifier que ce fichier est bien chargé.
```

```
⚠️ WARN — run-hook.cmd
Le fichier hooks/run-hook.cmd est le wrapper Windows pour les hooks shell.
Il doit rester dans hooks/ — ne pas déplacer.
```

```
⚠️ WARN — Paths avec espaces
Si votre dossier de projet contient des espaces, encapsuler les paths dans les hooks :
  "C:\Users\mon nom\projects\..." → utiliser des guillemets doubles dans la config hook
```

```
⚠️ WARN — Version épinglée
Superpowers sort ~30 releases en 8 mois. Spécifier la version à l'install si vous
voulez de la stabilité :
  /plugin install superpowers@5.1.0
```
