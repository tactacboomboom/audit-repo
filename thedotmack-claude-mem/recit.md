---
name: claude-mem-recit
description: Synthèse narrative thedotmack/claude-mem — la prothèse mnésique de l'agent, ses règles du jeu, ses points de rupture, sa posture d'adoption. Charger pour comprendre la philosophie ou convaincre un décideur.
---

# Récit — thedotmack/claude-mem

## Le décor

Il y a un problème que tout utilisateur de Claude Code a rencontré sans pouvoir le nommer : l'agent oublie. Chaque session repart de zéro. Le contexte accumulé — les bugs résolus, les décisions d'architecture, les chemins qu'il ne faut plus emprunter — s'évapore avec le token final de la session précédente.

claude-mem est la réponse directe à ce problème. Ce n'est pas un simple logger. C'est une **prothèse mnésique complète** : un service qui s'insère dans le cycle de vie de l'agent, capture tout ce qu'il fait, compresse ce flux avec un modèle AI, et réinjecte le contexte pertinent au démarrage de la session suivante. 78 000 étoiles. 271 releases. Une infrastructure TypeScript de plusieurs milliers de lignes. Le projet a la carrure d'un produit, pas d'un script.

## Les règles du jeu

Le système repose sur une chaîne de causalité stricte. Trois lois non négociables :

1. **Le Worker doit tourner** — sans ce service Bun en arrière-plan, les hooks s'exécutent dans le vide. Aucune erreur visible. Les observations sont perdues en silence. C'est le risque le plus insidieux du système.

2. **La progressive disclosure est la seule porte d'entrée** — pas d'accès brut au corpus. On passe toujours par search (50-100 tokens), puis timeline, puis get_observations (500-1000 tokens). La discipline est architecturale, pas optionnelle.

3. **Le quota token est un mur, pas une suggestion** — si l'injection dépasse la limite, elle s'arrête. Jamais de dépassement silencieux. Le budget a préséance sur la richesse mémorielle.

> *"Tout le système tient sur un processus Bun qui doit rester vivant. C'est le talon d'Achille d'une architecture autrement remarquable."*

## Le socle immuable

Certaines propriétés ne changent pas quelle que soit la configuration. Chaque observation appartient à une session, une seule. Chaque session appartient à un agent source, un seul — Claude Code et Codex ne partagent pas leur mémoire, par design. Les `<private>` tags excluent définitivement le contenu marqué : pas de backdoor, pas de récupération possible. SQLite reste la source de vérité même quand ChromaDB tombe — les vecteurs sont rebuildables, les faits ne le sont pas.

Deux avertissements majeurs : l'installation modifie les fichiers de configuration de l'agent hôte. Désinstaller proprement demande une intervention manuelle sur ces fichiers. Et la compression AI ne se déclenche qu'à la terminaison propre de la session — un crash agent laisse la session non compressée dans le corpus.

## Les leviers de transformation

Trois axes font de claude-mem autre chose qu'un simple logger :

| Levier | Mécanisme | Impact |
|--------|-----------|--------|
| Compression AI | Summaries générés à SessionEnd | Corpus compact même sur 1000 sessions |
| Hybrid search | FTS5 + ChromaDB vecteurs | Rappel sémantique + exact-match simultanés |
| Progressive disclosure | search → timeline → get_obs | ~10× économie tokens vs fetch brut |

Et le levier de la prothèse PM en particulier : la mémoire cross-session transforme l'agent en **continuateur** plutôt qu'en débutant perpétuel. Un agent qui sait ce qu'il a déjà essayé, ce qui a échoué, et pourquoi — c'est une différence de nature, pas de degré.

## Les points de rupture

| Signal | Risque |
|--------|--------|
| Worker down sans supervision | Observations perdues en silence — le plus dangereux |
| Session terminée sans SessionEnd propre | Compression AI manquée — corpus tronqué |
| Hooks non rechargés après install | mem-search présent mais 0 observation capturée |
| Server Beta activé sans Postgres/Redis | Crash Worker — rollback requis |
| Release majeure sans migration guide | Hooks désynchronisés avec l'agent hôte |

## Le chemin de moindre résistance

```
npx claude-mem install → redémarrer l'agent → travailler normalement
```

C'est tout. Le reste est automatique. La session capture, compresse, injecte. L'agent gagne de la mémoire sans changer son comportement. C'est le génie d'installation de claude-mem : l'UX est transparente.

La friction arrive après : quand on veut requêter activement la mémoire (`mem-search`), quand on veut comprendre ce qui est stocké (Web UI sur port 37777), quand on veut éviter les fuites de contexte sensible (balises `<private>`). Ces couches existent et sont bien documentées — mais elles supposent une implication active de l'utilisateur.

## L'équilibre du risque

claude-mem est un projet au zénith de sa courbe d'adoption. 78k étoiles, cadence de releases soutenue, écosystème croissant (skills satellites, 7 agents supportés, Server Beta en cours de stabilisation). La relicence de AGPL-3.0 vers Apache 2.0 en v13.0.0 est un signal fort : le projet cherche l'adoption enterprise, pas seulement la communauté.

Mais la cadence de 271 releases en ~18 mois est aussi un avertissement. Le code évolue vite. Les hooks qui fonctionnent aujourd'hui peuvent être incompatibles demain. Sans version épinglée, l'upgrade automatique peut casser silencieusement le pipeline de mémoire — et comme les pertes d'observations sont silencieuses, le problème peut passer inaperçu pendant plusieurs sessions.

> *"La mémoire persistante est une promesse. La réaliser exige que le Worker tourne, que les hooks soient chargés, et que la session se termine proprement. Trois conditions. Toutes invisibles pour l'agent. Toutes critiques."*

**Pour une prothèse PM** : c'est le candidat le plus mature du marché pour transformer un agent de code en collaborateur à mémoire longue. L'adopter sur des projets where la continuité de contexte est critique — en épinglant la version et en monitorant le Worker.
