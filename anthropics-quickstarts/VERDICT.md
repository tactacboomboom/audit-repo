# VERDICT PM — anthropics/anthropic-quickstarts

## Note globale : 9/10

Repo officiel Anthropic. Référence canonique pour "comment Anthropic veut qu'un projet démarre". À traiter comme source de vérité.

## Points forts

1. **Modularité parfaite** : 7 quickstarts isolés, aucun couplage, démarrables indépendamment.
2. **README discipline** : chaque sous-projet a son README autonome, structure quasi-identique (Overview → Prerequisites → Quick Start → Structure → License).
3. **Friction minimale** : 3 commandes max pour démarrer (install → API key → run).
4. **Pattern PWF natif** : `autonomous-coding` formalise la persistance disque (feature_list.json + claude-progress.txt + git) — c'est l'origine officielle du pattern "Planning With Files".
5. **`.claude/skills/first-run/`** : le seul exemple Anthropic-officiel de skill embarqué dans un projet user. C'est LA référence pour SKILL.md.
6. **Defense-in-depth** : security.py + allowlist bash + sandbox-exec + filesystem restrictions. Pattern reproductible.
7. **Config-as-code** : `config.example.toml` + env vars `CU_*` overlay. Pattern propre, sans `settings.json` hardcodé.

## Points faibles

1. **Pas de `.claude/settings.json` racine** : aucun pattern de configuration projet-level pour Claude Code. Le seul usage de `.claude/` est pour les skills.
2. **CLAUDE.md racine privé** : marqué "Internal Anthropic use" → non reproductible verbatim. Limite la valeur pédagogique.
3. **Hétérogénéité Python/TS** : pas de cohérence inter-projets sur le choix de stack (assumé, mais complique le mimétisme).
4. **Pas de hooks Claude Code** : aucun exemple de `hooks/` dans le repo. Lacune pour qui cherche à automatiser.

## Usages recommandés pour le skill architecture-anthropic

1. **Template de SKILL.md** : copier la structure YAML frontmatter de `computer-use-best-practices/.claude/skills/first-run/SKILL.md`.
2. **Template de README quickstart** : reproduire la charpente Overview / Prerequisites / Quick Start / How It Works / Structure / Customization / Troubleshooting / License de `autonomous-coding/README.md`.
3. **Pattern persistance session** : reprendre le triptyque `feature_list.json` (immuable) + `claude-progress.txt` (passation) + git (historique).
4. **Pattern security sandbox** : reprendre `autonomous-coding/security.py` comme base d'allowlist bash.
5. **Pattern config layered** : reprendre `config.example.toml` + env var overlay au lieu de hardcoded settings.

## Verdict pertinence pour le skill : HAUT

C'est la référence Anthropic-officielle. À indexer en priorité dans le catalogue archi.
