# Installation — alirezarezvani/claude-skills

> Guide d'installation OS-specific · Windows PowerShell · 2026-05-26

---

## Prérequis

| Outil | Version min | Vérification |
|---|---|---|
| Python | 3.8+ | `python --version` |
| Git | 2.x | `git --version` |
| Claude Code | dernière | `claude --version` |
| Node.js (optionnel) | 18+ | `node --version` (pour convert.sh via Node) |

---

## Option A — Installation rapide via Plugin (Claude Code)

```bash
# Installer le bundle complet
/plugin marketplace add alirezarezvani/claude-skills

# Ou installer un bundle spécifique
/plugin install product-team@claude-code-skills
/plugin install engineering-skills@claude-code-skills
```

> ✅ Méthode recommandée. Aucune commande système requise.

---

## Option B — Depuis le repo source (pour contribuer ou modifier)

```powershell
# 1. Cloner
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# 2. Placer les skills dans Claude Code
# Windows PowerShell :
$skillsDir = "$env:USERPROFILE\.claude\skills"
New-Item -ItemType Directory -Force -Path $skillsDir

# Copier le bundle product-team
Copy-Item -Recurse -Force ".\product-team\*" "$skillsDir\"

# Copier le bundle engineering
Copy-Item -Recurse -Force ".\engineering\*" "$skillsDir\"
```

---

## Config minimale

Les skills ne nécessitent pas de fichier de configuration. L'activation se fait via frontmatter SKILL.md.

Pour les **Personas**, placer dans :
```
~/.claude/skills/personas/
```

Pour les **Agents composites**, placer dans :
```
~/.claude/skills/agents/
```

---

## Commandes de vérification

```bash
# Vérifier que les skills sont visibles dans Claude Code
/skills list

# Tester un skill product-team
/skill product-team/agile-product-owner

# Tester un outil Python (exemple)
python product-team/skills/agile-product-owner/scripts/story_generator.py --help
```

---

## Points d'attention Windows

> ⚠️ **convert.sh** — Le script de conversion multi-platform est bash. Sur Windows :
> - Option 1 : WSL (`wsl bash convert.sh --tool cursor`)
> - Option 2 : Git Bash (`"C:\Program Files\Git\bin\bash.exe" convert.sh --tool cursor`)
> - Option 3 : Ignorer convert.sh si vous utilisez uniquement Claude Code

> ⚠️ **Encodage** — Les SKILL.md contiennent des caractères UTF-8. Si PowerShell affiche des symboles corrompus : `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`

> ⚠️ **Chemins longs** — Si git clone échoue sur Windows : activer les long paths via `git config --global core.longpaths true`
