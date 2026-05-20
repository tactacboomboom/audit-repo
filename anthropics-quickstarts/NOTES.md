# NOTES — Patterns d'archi Anthropic-officiels pour le skill architecture-anthropic

Source : anthropics/anthropic-quickstarts (audit 2026-05-20)
Statut : référence canonique pour le layer "catalogue archi officielle"

## 1. Structure-type d'un quickstart Anthropic

Charpente minimale observée sur les 7 projets :

```
<quickstart-name>/
├── README.md              # OBLIGATOIRE
├── .env.example           # OBLIGATOIRE (si secrets requis)
├── .gitignore             # OBLIGATOIRE
├── requirements.txt       # Python : OBLIGATOIRE
│   OU package.json        # Node/TS : OBLIGATOIRE
├── <module>/              # code applicatif dans un sous-dossier nommé
├── tests/                 # OBLIGATOIRE si production-grade
├── prompts/               # OPTIONNEL — si l'agent a des prompts externalisés
└── setup.sh OU init.sh    # OPTIONNEL — script d'init one-shot
```

Pour les projets containerisés, ajouter :
```
├── Dockerfile
├── docker-compose.yml     # si multi-service
└── .dockerignore
```

Pour les projets Next.js (vitrine) :
```
├── app/                   # Next.js 14 App Router
├── components/            # shadcn/ui
├── lib/                   # utilitaires
├── components.json        # config shadcn/ui
├── tailwind.config.ts
├── tsconfig.json
└── next.config.mjs
```

## 2. Convention README de starter Anthropic

Sections obligatoires (ordre canonique observé sur autonomous-coding et computer-use-best-practices) :

1. **Titre + 1-liner descriptif**
2. **Overview / What it does** — paragraphe d'intention, mention explicite "reference implementation" si pédagogique
3. **Prerequisites** — versions Python/Node, SDK requis, permissions OS si pertinent
4. **Quick Start** — bloc `bash` complet : install → API key → run
5. **How It Works** — section conceptuelle, pas de code (architecture, agents, flow)
6. **Project Structure** — arborescence ASCII avec commentaires inline
7. **Security Model** — OBLIGATOIRE dès qu'il y a exécution de code ou contrôle système
8. **Command Line Options** — table markdown si CLI
9. **Customization** — comment modifier (prompts, allowlist, etc.)
10. **Troubleshooting** — Q/R des erreurs courantes
11. **License** — toujours en dernier

**Règle d'or observée** : le bloc Quick Start doit être copiable-collable et fonctionner sans contexte supplémentaire.

## 3. Configuration `.claude/` de référence

**Le seul exemple officiel** est `computer-use-best-practices/.claude/skills/first-run/SKILL.md`.

Structure :
```
.claude/
└── skills/
    └── <skill-name>/
        └── SKILL.md       # frontmatter YAML + corps markdown
```

Frontmatter canonique :
```yaml
---
name: <skill-name>
description: <action verb + concrete outcome + when-to-trigger hints>
---
```

Le corps est structuré en **phases numérotées** (Phase 1: Orientation, Phase 2: Environment Check, etc.) avec instructions concrètes par phase.

**Absence notable** : aucun `.claude/settings.json` projet-level dans tout le repo. Anthropic ne pousse PAS de pattern settings.json embarqué. La config Claude reste user-global.

## 4. Patterns d'init de projet (scripts, hooks, dépendances)

### Pattern A — `setup.sh` (computer-use-demo)
Script bash idempotent qui :
- crée venv
- installe deps + dev-requirements
- installe pre-commit hooks
- valide l'environnement

### Pattern B — `init.sh` généré par agent (autonomous-coding)
Script créé PAR l'agent initialiseur, jamais commité directement. Contient :
- install deps
- start services
- env config
- URL d'accès en commentaire

### Pattern C — `.pre-commit-config.yaml` racine (monorepo)
Hooks officiels Anthropic pour Python :
```yaml
- ruff (autofix lint)
- ruff format
- ruff lint check
- pyright (types)
- check-yaml, end-of-file-fixer, trailing-whitespace
```
Scopé via `files: ^<project>/`.

### Pattern D — `pyproject.toml` racine avec pyright scope
```toml
[tool.pyright]
venvPath = "<subproject>"
venv = ".venv"
useLibraryCodeForTypes = false
```
Permet de configurer un type-checker depuis la racine sur un sous-projet.

## 5. Catégorisation des quickstarts par usage

| Catégorie | Quickstarts | Critère de choix |
|---|---|---|
| **Apprentissage fondamentaux** | `agents/` | Lire en premier pour comprendre "tools in a loop" |
| **Computer use sandbox** | `computer-use-demo/` | Production isolée (Docker) |
| **Computer use pédagogique** | `computer-use-best-practices/` | Apprendre caching, pruning, trajectory recording |
| **Web automation** | `browser-use-demo/` | Quand pixel-pilotage trop risqué, DOM suffit |
| **Autonomie longue** | `autonomous-coding/` | Multi-session, persistance git, 200 features |
| **Démo vitrine UI** | `customer-support-agent/`, `financial-data-analyst/` | Next.js 14, montrable à un CTO |

## 6. Pattern de persistance multi-session (origine PWF)

`autonomous-coding/` formalise le pattern :

```
Mémoire = trois fichiers + git
├── <spec>.txt              # immuable, source de vérité requirements
├── feature_list.json       # immuable côté descriptions, mutable côté pass/fail
├── claude-progress.txt     # passation entre sessions (notes libres)
└── .git/                   # historique implémentation + raisonnement
```

Protocole de reprise de session (canonique) :
1. `ls` + lecture des core docs
2. relire `claude-progress.txt`
3. `git log --oneline -20`
4. compter les features incomplètes
5. choisir LA prochaine feature
6. implémenter
7. commit + update progress + clean state avant terminate

C'est exactement le pattern PWF côté user, formalisé officiellement par Anthropic dans un quickstart.

## 7. Pattern security defense-in-depth

`autonomous-coding/security.py` + `client.py` :
- **Couche 1 OS** : sandbox bash isolation
- **Couche 2 FS** : opérations limitées au project dir
- **Couche 3 allowlist** : commandes autorisées explicitement (`ls`, `cat`, `head`, `tail`, `wc`, `grep`, `npm`, `node`, `git`, `ps`, `lsof`, `sleep`, `pkill`)
- **Couche 4 hook** : block automatique des commandes hors allowlist

Reproductible : copier `security.py` comme base, adapter la liste.

## 8. Pattern config-as-code (computer-use-best-practices)

Triptyque :
```
constants.py            # Config dataclass + cfg instance (defaults)
config.example.toml     # template TOML d'overrides
CU_<FIELD> env vars     # overrides ponctuels par variable
```
Préséance : env > toml > defaults.
Activation : `CU_CONFIG=config.toml python -m ...`

À reproduire pour tout projet ayant >5 paramètres de config.

## Checklist audit perso "Mon projet est-il conforme Anthropic ?"

- [ ] README suit la charpente 11-sections
- [ ] Quick Start copiable-collable en 3 commandes
- [ ] `.env.example` versionné, `.env` dans `.gitignore`
- [ ] Sous-dossier code applicatif nommé explicitement (pas `src/` générique)
- [ ] `tests/` présent si > démo
- [ ] Section "Security Model" si exécution shell ou contrôle système
- [ ] Section "Project Structure" avec arbre ASCII commenté
- [ ] Pre-commit hooks configurés (ruff + pyright pour Python)
- [ ] Si skills embarqués : `.claude/skills/<name>/SKILL.md` avec frontmatter YAML
- [ ] Si multi-session : triptyque `<spec>.txt` + `<state>.json` + `progress.txt` + git
- [ ] Pas de `.claude/settings.json` dans le repo (config user-global only)
- [ ] License MIT (convention Anthropic)
