#!/usr/bin/env python3
"""
Génère indie_context_T1.md (essentiel) + indie_context_T2.md (complet) — projets indie-dev.
Usage : python indie-dev/scripts/indie_context.py
Output : indie-dev/indie_context_T1.md  ·  indie-dev/indie_context_T2.md
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent  # indie-dev/

# Tier1 — charge rapide : projet courant, état, prochaine action
TIER1_FILES = ["projects.md", "current.md", "blockers.md", "next.md"]

# Tier2 — contexte complet : tous les projets, stack, décisions, revenue
TIER2_FILES = [
    "projects.md",
    "current.md",
    "stack.md",
    "decisions.md",
    "blockers.md",
    "revenue.md",
    "progress.md",
    "next.md",
    "references.md",
]


def strip_frontmatter(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
        if end is not None:
            return "\n".join(lines[end + 1:]).lstrip("\n")
    return text


def build_tier(tier_label: str, files: list, description: str):
    parts = []
    loaded = []
    missing = []

    for fname in files:
        path = ROOT / fname
        if path.exists():
            body = strip_frontmatter(path.read_text(encoding="utf-8")).rstrip()
            parts.append(f"<!-- {fname} -->\n{body}")
            loaded.append(fname)
        else:
            missing.append(fname)

    out_path = ROOT / f"indie_context_{tier_label}.md"

    if not loaded:
        placeholder = (
            f"---\nname: indie-context-{tier_label.lower()}\n"
            f"description: {description}\ngenerated: indie_context.py\n---\n\n"
            f"# Contexte Indie-Dev — {tier_label}\n\n"
            "_Aucune source disponible. Créer les fichiers sources dans indie-dev/_\n\n"
            f"Fichiers attendus : {', '.join(files)}\n"
        )
        out_path.write_text(placeholder, encoding="utf-8")
        print(f"[PLACEHOLDER] {out_path.name} — sources manquantes : {', '.join(missing)}")
        return

    header = (
        f"---\nname: indie-context-{tier_label.lower()}\n"
        f"description: {description}\n"
        f"generated: indie_context.py (auto)\n---\n\n"
        f"# Contexte Indie-Dev — {tier_label}\n\n"
        f"Sources : {', '.join(loaded)}\n\n"
    )
    output = header + "\n\n---\n\n".join(parts)
    out_path.write_text(output, encoding="utf-8")

    print(f"[OK] {out_path.name} — {len(output):,} chars · {output.count(chr(10))} lignes · {len(loaded)}/{len(files)} sources")
    if missing:
        print(f"  [WARN] Manquants : {', '.join(missing)}")


def main():
    build_tier(
        "T1",
        TIER1_FILES,
        "Contexte essentiel indie-dev — projets courants + état + next. Charger en début de session.",
    )
    build_tier(
        "T2",
        TIER2_FILES,
        "Contexte complet indie-dev — tous projets + stack + décisions + revenue. Charger pour analyse approfondie.",
    )


if __name__ == "__main__":
    main()
