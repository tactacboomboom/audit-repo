# Récit — anthropics/skills

## Le décor

Un skill, chez Anthropic, n'est pas un programme. C'est un dossier. Un seul fichier l'ouvre — SKILL.md — et tout le reste est satellite. Le frontmatter YAML est la carte d'identité que Claude consulte au démarrage ; le corps markdown est la doctrine qu'il ouvre une fois la mission acceptée. Autour gravitent trois orbites optionnelles : scripts/ pour exécuter, references/ pour approfondir, assets/ pour habiller. Dix-sept skills officiels peuplent le repo, regroupés en trois plugins distribuables — documents, exemples, et l'API Claude — orchestrés par un unique manifest. Et au-dessus de tout, une spec versionnée, hébergée hors du repo lui-même, sur agentskills.io.

## Les règles du jeu

Tout repose sur deux contrats inviolables : `name` doit matcher le dossier parent, et `description` doit dire à la fois ce que fait le skill ET quand l'utiliser. Le reste est libre — mais "libre" ne veut pas dire désinvolte. Anthropic montre par l'exemple deux écoles : la concise (brand-guidelines, slack-gif-creator) en deux phrases, et la maximaliste (xlsx, docx) en un paragraphe qui détaille fichiers, formats, et même les non-déclencheurs.

> "If the user mentions a .pdf file or asks to produce one, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs..."

Ce "Do NOT" est l'arme secrète : la négation officialisée. La spec n'oblige rien là-dessus, mais Anthropic l'utilise sciemment pour empêcher les déclenchements parasites.

## Le socle immuable

Six invariants tiennent la structure. Le dossier porte le nom du skill, qui porte le nom dans le frontmatter — triangle verrouillé. Le name n'accepte que minuscules, chiffres, et hyphens, jamais en bord, jamais doublés. La description ne dépasse pas 1024 caractères, le compatibility 500, le name 64. Les références entre fichiers restent en chemins relatifs, et la profondeur ne dépasse jamais un niveau depuis le SKILL.md — Anthropic refuse les arbres labyrinthiques. Le coût en tokens du frontmatter est multiplicatif : chaque skill installé consomme ~100 tokens au boot, ce qui explique l'obsession pour les descriptions denses mais bornées.

## Les leviers de transformation

Le levier majeur, c'est la description elle-même. Anthropic la traite comme un artefact à optimiser empiriquement, pas comme une notice écrite une fois. La preuve : `improve_description.py` enfoui dans skill-creator/scripts/ — un script dédié à la réécriture itérative de descriptions. La logique est radicale : 20 requêtes mixtes (qui-devraient-déclencher / qui-ne-devraient-pas), score de matching, boucle d'amélioration jusqu'à convergence.

Deuxième levier : la progressive disclosure. Le frontmatter est l'antichambre (~100 tokens, toujours chargée). Le SKILL.md est la pièce principale (chargée à l'activation). Les références/scripts/assets sont les archives — n'entrent en mémoire que sur demande explicite. Cette discipline impose une architecture : tout SKILL.md qui dépasse 500 lignes est suspect ; il faut éclater vers references/.

## Les points de rupture

| Seuil | Limite dure | Conséquence du dépassement |
|---|---|---|
| `name` | 64 caractères | Skill invalide, rejeté par le linter |
| `description` | 1024 caractères | Skill invalide |
| `compatibility` | 500 caractères | Skill invalide |
| Corps SKILL.md | ~5000 tokens (soft) | Activation onéreuse, attention diluée |
| Lignes SKILL.md | ~500 (soft) | Refactor obligatoire vers references/ |
| Profondeur refs | 1 niveau (soft) | Chaînes de fetch coûteuses |

> "Le routeur d'activation n'a que le frontmatter pour décider. Si la description omet le QUAND, le skill devient invisible."

## Le chemin de moindre résistance

Le bonheur d'un créateur de skill suit cinq étapes : copier `template/`, éditer le frontmatter (name = dossier parent, description = "Action. Use when X, Y, Z."), écrire les instructions dans le corps, lancer `skills-ref validate`, et — pour les skills à enjeu — créer un harness d'évals via skill-creator. Trois nœuds de friction subsistent : la spec n'est pas dans le repo (redirect externe), le linter dépend d'une lib séparée (`agentskills/agentskills/skills-ref`), et le meilleur outil pour optimiser sa description (`improve_description.py`) n'est pas exposé comme CLI globale — il faut le déterrer.

## L'équilibre du risque

Lock-in fournisseur : faible. La spec est ouverte, le format est markdown, et n'importe quel agent peut implémenter le runtime — ce sont juste des dossiers avec du YAML et du texte. Rupture upstream : très improbable. Anthropic a stabilisé la spec, le repo affiche 138k stars et 36 commits seulement sur main (signe d'un format mûr, pas en gestation). Le seul vrai risque est sur `allowed-tools`, explicitement marqué expérimental — toute logique de sécurité qui s'y appuierait est exposée.

La recommandation directionnelle est nette : pour qui veut construire des skills sérieux, ce repo est le manuel canonique. Pas la peine de chercher ailleurs. Le pattern Anthropic — description active + progressive disclosure + harness d'évals — est l'état de l'art tel qu'observé en mai 2026.
