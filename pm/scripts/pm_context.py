#!/usr/bin/env python3
"""
Génère pm_context_T1.md (essentiel) + pm_context_T2.md (complet) — prothèse PM.
Usage : python pm/scripts/pm_context.py
Output : pm/pm_context_T1.md  ·  pm/pm_context_T2.md
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent  # pm/

# Tier1 — charge rapide (~2k tokens) : état courant, blockers, prochaine action
TIER1_FILES = ["goal.md", "decisions.md", "blockers.md", "next.md"]

# Tier2 — contexte complet (~8k tokens) : spec + archi + historique
TIER2_FILES = [
    "goal.md",
    "spec.md",
    "architecture.md",
    "decisions.md",
    "blockers.md",
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

    out_path = ROOT / f"pm_context_{tier_label}.md"

    if not loaded:
        placeholder = (
            f"---\nname: pm-context-{tier_label.lower()}\n"
            f"description: {description}\ngenerated: pm_context.py\n---\n\n"
            f"# Contexte PM — {tier_label}\n\n"
            "_Aucune source disponible. Créer les fichiers sources dans pm/_\n\n"
            f"Fichiers attendus : {', '.join(files)}\n"
        )
        out_path.write_text(placeholder, encoding="utf-8")
        print(f"[PLACEHOLDER] {out_path.name} — sources manquantes : {', '.join(missing)}")
        return

    header = (
        f"---\nname: pm-context-{tier_label.lower()}\n"
        f"description: {description}\n"
        f"generated: pm_context.py (auto)\n---\n\n"
        f"# Contexte PM — {tier_label}\n\n"
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
        "Contexte essentiel prothèse PM — goal + decisions + blockers + next. Charger en début de session.",
    )
    build_tier(
        "T2",
        TIER2_FILES,
        "Contexte complet prothèse PM — spec + architecture + historique complet. Charger pour analyse approfondie.",
    )


if __name__ == "__main__":
    main()
