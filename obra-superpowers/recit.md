---
name: superpowers-recit
description: Synthèse narrative obra/superpowers — règles fondamentales, leviers de transformation, points de rupture, posture d'adoption. Charger pour comprendre la philosophie du framework ou convaincre une équipe.
---

# Récit — obra/superpowers

## Essence

Framework de développement universel : une méthodologie écrite une fois, fonctionnant sur 6 agents. 206k ★, 14 skills, 5 formats d'installation, zéro dépendance runtime.

## 3 règles fondamentales

1. **Tu ne codes pas avant un test qui échoue** — RED-GREEN-REFACTOR est un invariant, pas une option
2. **1 feature = 1 worktree = 1 branche** — pas d'entrelacement, pas de "juste ça en plus"
3. **Plus de dispatch nommé (≥ v5.1)** — templates génériques : moins expressif, plus portable

## 3 leviers de transformation

| Levier | Mécanisme | Impact |
|--------|-----------|--------|
| Parallélisme subagents | dispatching-parallel-agents → N trajectoires simultanées | throughput × N |
| Extension ouverte | writing-skills inclus dans le repo | customisation sans fork |
| Portabilité multi-agent | Cursor → Claude Code = changement de manifest seulement | 0 perte de méthodologie |

## Points de rupture

| Signal | Risque |
|--------|--------|
| Tâche plan > 5 min | Plan trop vague → redécouper |
| TDD sans RED au départ | Test de complaisance → bugs cachés |
| Skill mis à jour sans màj 5 manifests | Comportement divergent selon agent |
| Hooks non chargés | Skills silencieusement absents — le plus insidieux |
| Merge sans verification-before-completion | Régression non détectée |

## Posture d'adoption

**Adopter** pour tout projet avec agent de code. **Épingler** la version (`/plugin install superpowers@5.1.0`). **Tester** les upgrades en worktree isolé — le framework enseigne lui-même cette pratique.

**Ne pas intégrer** dans un produit B2B à SLA strict : ~30 releases en 8 mois, breaking change majeur v4→v5, V6 probable H2 2026.
