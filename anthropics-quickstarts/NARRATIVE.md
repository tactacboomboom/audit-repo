# NARRATIVE — anthropics-quickstarts

Si Anthropic devait montrer à un dev "comment on démarre un projet chez nous", c'est ce repo qu'on lui tend. Sept quickstarts, chacun pose une question différente.

`agents/` répond à : "qu'est-ce qu'un agent au minimum ?" Réponse : 300 lignes, une classe Agent, une boucle, des outils enfichables. Pas de framework, pas de magie. C'est la version Hello-World de l'agent — exactement ce qu'un débutant doit lire en premier.

`computer-use-demo/` répond à : "comment je laisse Claude piloter une machine sans qu'il casse la mienne ?" Réponse : Docker, VNC, isolation totale. Containerisation comme garde-fou.

`computer-use-best-practices/` répond à la même question mais sans le filet : macOS natif, mais avec sandbox-exec, prompt caching, image pruning, trajectory recording. C'est le seul du repo à porter un dossier `.claude/skills/first-run/` — Anthropic montre ici comment intégrer ses propres skills dans un projet user.

`browser-use-demo/` répond à : "et si je veux juste le web, pas le bureau ?" Réponse : Playwright + Streamlit. DOM-aware, moins risqué que le pilotage pixel.

`autonomous-coding/` répond à la question la plus ambitieuse : "comment un agent peut-il construire une app sur plusieurs jours, plusieurs sessions, sans tout oublier entre deux ?" Réponse : git comme mémoire long-terme, `feature_list.json` comme source de vérité immuable, `claude-progress.txt` comme passation entre sessions. C'est littéralement le pattern PWF (Planning With Files) d'origine Anthropic. Le contexte volatile devient persistance disque.

`customer-support-agent/` et `financial-data-analyst/` répondent à : "comment je montre ça à mon CTO ?" Réponse : Next.js 14, shadcn/ui, démo léchée, déploiement Amplify.

Le pattern transverse — celui qu'Anthropic veut qu'on retienne — est la **discipline de la friction minimale** : chaque quickstart est démarrable en trois commandes (`install`, `set API key`, `run`), chacun a son README autonome, chacun isole son scope. Aucun couplage entre projets. Si tu veux faire ton propre quickstart conforme : un dossier, un README qui suit la même charpente, un SDK target unique, un init script clair, un `.env.example` versionné, un sandbox quand tu touches au système.
