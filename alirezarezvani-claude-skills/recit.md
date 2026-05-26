# Récit — alirezarezvani/claude-skills

> Décodeur narratif · transmutation de l'analyse fmaths · 2026-05-26

---

## Le décor

Imaginez une armurerie de 329 pièces, chacune rangée par métier : une étagère pour l'ingénieur, une pour le product owner, une pour le directeur marketing, une pour le CFO. Chaque pièce est légère — un fichier SKILL.md, parfois accompagné d'un outil Python sans installation. On entre, on prend, on part. L'armurerie ne sait pas qui vous êtes ni dans quel ordre vous venez piocher.

C'est la force et la limite du projet.

---

## Les règles du jeu

> *"You combine them. The pattern is always the same."*

L'orchestration repose sur trois composantes : une **Persona** (qui êtes-vous, comment jugez-vous), des **Skills** (quelles armes prenez-vous), et des **Agents** (des combinaisons pré-configurées pour un domaine). Le protocole dit : un seul persona actif par prompt. Les skills, eux, s'empilent librement.

Quatre patterns de jeu émergent :
- **Solo Sprint** — vous jouez successivement CTO, PO, Founder. Chaque switch = un chapeau différent sur la même tête.
- **Domain Deep-Dive** — même persona, 5 skills chargés, plongée intensive.
- **Multi-Agent Handoff** — une persona relit le travail d'une autre. Contrôle qualité distribué.
- **Skill Chain** — aucun persona, séquence procédurale pure.

**Tension critique :** Le Solo Sprint est exactement le rêve du solo founder qui veut la stack de 50 personnes. Mais l'armurerie ne tient pas de registre des armes empruntées. Quand vous revenez le lendemain, vous recommencez à zéro.

---

## Le socle immuable

Trois choses ne bougent pas dans ce repo :

1. **Grain = 1 SKILL.md = 1 intention.** Pas de skills composites, pas de hiérarchie d'héritages. Chaque skill est atomique.
2. **Zéro dépendance externe.** Les 402 outils Python tournent avec la stdlib uniquement. Pas de pip, pas de virtualenv, pas de surprise à 23h.
3. **MIT.** Vous prenez, vous modifiez, vous redistribuez. Sans dette.

> ⚠️ Ce qui n'est **pas** immuable : la conformité frontmatter. Le repo ajoute des champs (`type`, `version`, `compatibility`) que le marketplace Anthropic officiel ne reconnaît pas. Si Claude Code fait évoluer son parser, ces skills peuvent casser silencieusement.

---

## Les leviers de transformation

Six leviers pour adapter ce repo à votre usage :

| Levier | Action | Gain |
|---|---|---|
| Sélection domaine | Ne charger que product-team + engineering | Réduire de 329 → ~40 skills actifs |
| Ajout LINEAGE.md | Un fichier par skill chargé | Traçabilité documentaire, nilpotence locale |
| Normalisation frontmatter | Réduire à name + description | Conformité Anthropic officielle |
| Personas Scrum | Créer PO / SM / Dev / Stakeholder / Dev Anthropic | Simuler l'équipe Scrum complète |
| Orchestration ↔ chaîne nilpotente | Mapper les phases sur R1→R4 | Convergence garantie MRD→Code |
| Spec day | Forcer TOUS les documents une fois | Remplir la chaîne avant le premier sprint |

---

## Les points de rupture

| Seuil | Si franchi |
|---|---|
| >20 skills actifs simultanément | Le signal se noie dans le bruit — persona switching devient du code-switching sans sens |
| 0 LINEAGE.md | Chaque session repart de zéro — le Solo Sprint devient Groundhog Day |
| Frontmatter étendu + mise à jour Claude Code | Skills silencieusement invisibles dans le marketplace |
| Orchestration sans DoR/DoD | Handoff sans critère de done = phase suivante commence sur du flou |

---

## Le chemin de moindre résistance

Pour Yanis, solo founder cherchant la stack de 50 personnes :

```
1. Installer le bundle product-team + engineering-team          (2 commandes)
2. Créer 5 personas : PO · SM · Dev · Stakeholder · DevAnthro  (1 après-midi)
3. Mapper les personas sur R1→R4 de la chaîne nilpotente        (1 session)
4. Ajouter LINEAGE.md à chaque skill chargé                     (1h par skill)
5. Spec day : invoquer PO pour MRD → BRD → PRD avant sprint 1   (1 journée)
```

Le repo vous donne les pièces. L'assemblage reste votre travail.

---

## L'équilibre du risque

Ce repo est une bibliothèque, pas un système. Sa valeur est dans sa **densité** (329 skills battle-tested, 16k étoiles) et son **absence de friction** (0 dépendance, MIT). Son risque principal n'est pas technique — il est architectural : charger 329 skills sans gouvernance produit du bruit, pas de la clarté.

**Pour le rêve "dreamteam solo" :** ce repo est un accélérateur de matière première. Il ne résout pas le problème du linéage, de la volatilité documentaire, ni du dashboard de convergence. Ces couches sont à construire par-dessus — et c'est exactement ce que fait le projet claude-prostheses.

> La bonne question n'est pas "est-ce que ce repo remplace la dreamteam ?" mais "quels skills de ce repo dois-je greffer sur quels personnages de ma matrice ?"
