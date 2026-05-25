---
name: claude-mem-installation
description: Installation thedotmack/claude-mem v13.3.0 — commandes par agent (Claude Code, Gemini, OpenCode, Codex), config settings.json, warnings Windows PowerShell, vérification Worker. Charger quand on installe ou configure.
---

# Installation — thedotmack/claude-mem v13.3.0

## Prérequis

| Outil | Version min | Vérification |
|---|---|---|
| Node.js | 20.0.0+ | `node --version` |
| Bun | 1.0.0+ | `bun --version` (auto-installé si absent) |
| uv (Python pkg mgr) | Toute | `uv --version` (auto-installé si absent) |
| SQLite 3 | Bundlé | — (pas besoin d'installer) |
| Claude Code | Plugin support requis | `claude --version` |
| **Server Beta uniquement** | Postgres + Redis | `psql --version` · `redis-cli --version` |

---

## Option A — Installation rapide (recommandée)

### Claude Code (défaut)

```powershell
# Dans un terminal PowerShell
npx claude-mem install
```

Puis relancer Claude Code. Les hooks sont injectés automatiquement dans `~/.claude/settings.json`.

### Gemini CLI

```powershell
npx claude-mem install --ide gemini-cli
```

### OpenCode

```powershell
npx claude-mem install --ide opencode
```

### Via Plugin Marketplace (Claude Code)

```
# Dans une session Claude Code
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

### OpenClaw Gateway

```powershell
# Installe via script shell (nécessite bash ou Git Bash sur Windows)
curl -fsSL https://install.cmem.ai/openclaw.sh | bash
```

---

## Option B — Depuis le source (pour contribuer ou déboguer)

```powershell
# 1. Cloner le repo
git clone https://github.com/thedotmack/claude-mem.git
cd claude-mem

# 2. Installer les dépendances
bun install

# 3. Builder le projet
bun run build

# 4. Lier localement
npm link

# 5. Installer dans l'agent
claude-mem install
```

---

## Config minimale

Fichier créé automatiquement : `~/.claude-mem/settings.json`

```json
{
  "CLAUDE_MEM_MODE": "code",
  "worker": {
    "port": 37777,
    "dataDir": "~/.claude-mem"
  },
  "context": {
    "maxTokens": 4000,
    "progressive": true
  },
  "privacy": {
    "tags": ["<private>", "</private>"]
  }
}
```

**Modes disponibles :**
- `"code"` — Anglais (défaut)
- `"code--zh"` — Chinois simplifié
- `"code--ja"` — Japonais
- Pattern : `"code--[ISO-639-1]"` pour toute autre langue

---

## Commandes de vérification

Après installation Claude Code, dans une nouvelle session :

```powershell
# 1. Vérifier que le Worker tourne
Invoke-WebRequest -Uri "http://localhost:37777" -UseBasicParsing | Select-Object StatusCode
# Attendu : StatusCode 200

# 2. Ouvrir le Web UI (vérification visuelle)
Start-Process "http://localhost:37777"

# 3. Dans Claude Code — requêter la mémoire
# Taper dans la session :
# /mem-search "test installation"
```

---

## Workflow de base post-install

```
# Session 1 — travail normal, la mémoire capture automatiquement
# (SessionStart hook injecte le passé, PostToolUse capture, SessionEnd compresse)

# Session 2 — mem-search pour retrouver contexte
search(query="bug authentication", type="bugfix", limit=10)
→ identifier les IDs pertinents
→ get_observations(ids=[42, 87, 103])
→ travailler avec le contexte récupéré
```

---

## Points d'attention Windows (PowerShell)

```
⚠️ WARN — Bun sur Windows
Bun s'installe via PowerShell si absent :
  powershell -c "irm bun.sh/install.ps1 | iex"
Si l'auto-install échoue derrière un proxy corporate, installer manuellement
depuis https://bun.sh avant de lancer npx claude-mem install
```

```
⚠️ WARN — Worker Process
Le Worker est un process Bun (port 37777). Il n'est pas registré comme service Windows.
Si vous redémarrez la machine, relancer manuellement :
  cd ~/.claude/plugins/... && bun run worker:start
Sans Worker actif, les hooks s'exécutent sans capturer les observations (perte silencieuse).
```

```
⚠️ WARN — curl sur Windows
La commande OpenClaw utilise curl Unix. Sur Windows PowerShell 5.1, curl est un alias
pour Invoke-WebRequest — utiliser Git Bash ou WSL pour cette commande spécifique.
```

```
⚠️ WARN — Version épinglée obligatoire
claude-mem publie ~15-20 releases/mois. Sans version épinglée, un npm update peut
introduire une breaking change sur les hooks. Recommandation :
  npx claude-mem@13.3.0 install
```

```
⚠️ WARN — Fichiers hooks modifiés à l'install
L'installation modifie ~/.claude/settings.json (section hooks).
Faire un backup avant install si vous avez des hooks custom :
  Copy-Item ~/.claude/settings.json ~/.claude/settings.json.bak
```

```
⚠️ WARN — Server Beta (opt-in v13.0.0)
N'activer le Server Beta que si Postgres ET Redis sont disponibles.
Sans ces prérequis, le Worker crashe au démarrage.
Le mode Worker (SQLite + Bun) reste la valeur par défaut et ne nécessite pas Postgres/Redis.
```
