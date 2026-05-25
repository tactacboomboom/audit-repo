#!/usr/bin/env python3
"""
Génère superpowers_context.md — contexte compressé obra/superpowers pour sessions Claude Code.
Usage : python obra-superpowers/scripts/compress_context.py
Output : obra-superpowers/superpowers_context.md
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent  # obra-superpowers/

SOURCE_ORDER = [
    "findings.md",
    "fmaths.md",
    "recit.md",
    "verdict.md",
    "installation.md",
]


def strip_frontmatter(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
        if end is not None:
            return "\n".join(lines[end + 1:]).lstrip("\n")
    return text


def main():
    parts = []
    loaded = []
    missing = []

    for fname in SOURCE_ORDER:
        path = ROOT / fname
        if path.exists():
            body = strip_frontmatter(path.read_text(encoding="utf-8")).rstrip()
            parts.append(f"<!-- {fname} -->\n{body}")
            loaded.append(fname)
        else:
            missing.append(fname)

    if not parts:
        print("[ERR] Aucun fichier source trouvé dans obra-superpowers/", file=sys.stderr)
        sys.exit(1)

    header = (
        "---\n"
        "name: superpowers-context\n"
        "description: Contexte compressé obra/superpowers v5.1.0 — findings + fmaths + recit + verdict + installation."
        " Charger pour toute session travaillant sur superpowers.\n"
        "generated: compress_context.py (auto)\n"
        "---\n\n"
        "# Contexte obra/superpowers — compressé\n\n"
        f"Sources : {', '.join(loaded)}\n\n"
    )

    output = header + "\n\n---\n\n".join(parts)
    out_path = ROOT / "superpowers_context.md"
    out_path.write_text(output, encoding="utf-8")

    print(f"[OK] {out_path.name} — {len(output):,} chars · {output.count(chr(10))} lignes · {len(loaded)} sources")
    if missing:
        print(f"[WARN] Manquants : {', '.join(missing)}")


if __name__ == "__main__":
    main()
