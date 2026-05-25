# Récit — obra/superpowers

## 1. Le décor

Il y a une dizaine d'agents de code sur le marché, chacun avec ses conventions, ses formats, ses chemins d'invocation. Superpowers est né d'une idée simple — et un peu folle : écrire une méthodologie de développement une seule fois, et la faire fonctionner partout.

Le résultat, c'est un repo de 206 000 étoiles, 14 skills opérationnels, et cinq formats d'installation différents — un par agent. Claude Code, Cursor, Codex, Gemini, Factory Droid, Copilot : tous peuvent consommer les mêmes protocoles. Le décor, c'est une bibliothèque de comportements codés en markdown, sans framework, sans build step, sans dépendance runtime. Juste des instructions.

Le coeur du système : seven stages. Brainstorming → isolation Git → planification → exécution → TDD → review → fin de branche. Pas une suggestion. Un ordre.

## 2. Les règles du jeu

La règle fondamentale est contre-intuitive dans un monde qui valorise la vitesse : **tu ne codes pas avant d'avoir un test qui échoue**.

RED-GREEN-REFACTOR n'est pas une option. C'est un invariant. L'agent doit produire un test failing, puis le faire passer, puis nettoyer. Tout autre ordre est explicitement interdit par le skill `test-driven-development`.

La deuxième règle : **une feature = un worktree = une branche**. Pas d'entrelacement, pas de "j'ai presque fini, je rajoute juste ça". La branche est sacrée jusqu'à la review.

La troisième règle, ajoutée en v5.1 après une phase de friction : **plus de dispatch nommé**. Les agents ne s'appellent plus par nom propre (`@agent-A`). On passe par des templates génériques. Un sacrifice d'expressivité pour gagner en portabilité.

> "La discipline est le prix de la vitesse sur le long terme."

## 3. Le socle immuable

Superpowers repose sur des invariants que deux ans d'itération n'ont pas bougés :

Le **workflow séquentiel** est intouchable. L'ordre des 7 étapes n'a jamais été remis en cause, même lors des refactors majeurs. C'est le squelette du système.

La **vérification avant completion** est le dernier filet. Le skill `verification-before-completion` ne peut pas être ignoré — c'est lui qui autorise le merge. Sauter cette étape, c'est introduire un bug silencieux dans la branche principale.

Les **hooks bootstrappent le contexte à chaque session**. Sans eux, les skills ne sont pas disponibles. Le fichier `session-start` est la condition d'existence du système.

⚠️ **Avertissement structurel** : les skills de superpowers n'ont pas de frontmatter YAML, contrairement au standard `anthropics/skills`. Il n'existe donc pas de validation automatisée possible. Un skill mal écrit passe inaperçu jusqu'à l'exécution.

## 4. Les leviers de transformation

Le premier levier, c'est le **parallélisme des subagents**. Le skill `dispatching-parallel-agents` permet de découper un plan en N trajectoires simultanées, chacune gérée par un sous-agent dédié. C'est là que le framework passe du "je code mieux" au "je code plus vite et mieux".

Le deuxième levier : **l'extension est ouverte**. Le skill `writing-skills` est dans le repo. La méthodologie se documente elle-même. N'importe quelle équipe peut créer ses propres skills et les distribuer via le même mécanisme de plugin.

Le troisième levier — souvent sous-estimé — est la **portabilité multi-agent**. Une équipe qui migre de Cursor vers Claude Code ne perd pas sa méthodologie. Elle change juste de manifest.

## 5. Les points de rupture

| Seuil | Signal d'alarme |
|---|---|
| Tâche > 5 min dans le plan | Le plan est trop vague → redécouper |
| TDD sans test RED au départ | Test de complaisance → bugs cachés |
| Skill mis à jour sans mise à jour des 5 manifests | Comportement divergent selon l'agent |
| Session sans hooks chargés | Skills silencieusement absents |
| Merge sans verification-before-completion | Régression non détectée |

Le risque le plus insidieux n'est pas l'erreur visible — c'est le **skill silencieusement absent**. Si les hooks ne chargent pas, l'agent continue de fonctionner, mais sans la méthodologie. Le développeur ne voit rien. Le résultat se dégrade lentement.

## 6. Le chemin de moindre résistance

Pour un projet neuf sur Claude Code :

```bash
/plugin install superpowers@claude-plugins-official
```

Puis la session démarre, les hooks s'initialisent, les 14 skills deviennent disponibles. L'agent propose `/brainstorm`. Le problème se précise en questions socratiques. Un plan en tâches 2-5 min est validé. Un worktree s'ouvre. Les subagents s'exécutent. Les tests rougissent avant de verdir.

C'est le chemin le plus court vers du code qui tient en production. Pas le chemin le plus immédiat — mais le chemin le moins cher sur la durée.

Les frictions arrivent ailleurs : quand il faut maintenir 5 manifests en parallèle, quand Cursor Windows exige son propre fichier de hooks, quand un breaking change (v4→v5 a supprimé le dispatch nommé) impose une migration manuelle à 18 000 forks.

## 7. L'équilibre du risque

Le risque principal de superpowers n'est pas la qualité du framework — elle est indéniable. C'est le **rythme des breaking changes**. Trente versions en huit mois. V4→V5 a cassé le dispatch nommé. V6 est probable en 2026.

Pour une adoption individuelle ou une équipe qui contrôle ses mises à jour : risque faible. Le système est bien documenté, les RELEASE-NOTES sont claires, la communauté Discord absorbe les questions.

Pour une intégration dans un produit qui dépend de la stabilité du comportement des agents : **épingler la version et auditer chaque upgrade**. Un breaking change non anticipé dans le manifest peut silencieusement désactiver toute la méthodologie.

La fragmentation multi-agent restera une tension permanente : six agents évoluent leurs specs indépendamment. Superpowers suit, mais avec un décalage. C'est le prix de l'universalité.

> Adoptez-le. Épinglez la version. Testez les upgrades en worktree isolé — le framework vous l'enseigne lui-même.
