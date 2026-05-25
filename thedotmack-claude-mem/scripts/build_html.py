#!/usr/bin/env python3
"""
Génère claude-mem-analysis.html depuis les 4 .md + marked.min.js caché.
Usage : python thedotmack-claude-mem/scripts/build_html.py
"""
import json
import sys
from datetime import date
from pathlib import Path

ROOT   = Path(__file__).parent.parent          # thedotmack-claude-mem/
CACHE  = Path.home() / ".claude/cache/marked.min.js"
OUT    = ROOT / "claude-mem-analysis.html"

SOURCES = {
    "recit":   ROOT / "recit.md",
    "fmaths":  ROOT / "fmaths.md",
    "install": ROOT / "installation.md",
    "verdict": ROOT / "verdict.md",
}


def strip_frontmatter(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
        if end is not None:
            return "\n".join(lines[end + 1:]).lstrip("\n")
    return text


def main():
    if not CACHE.exists():
        print(f"[ERR] marked.min.js absent : {CACHE}", file=sys.stderr)
        sys.exit(1)

    marked_js = CACHE.read_text(encoding="utf-8")

    contents = {}
    for key, path in SOURCES.items():
        if not path.exists():
            print(f"[ERR] Fichier manquant : {path}", file=sys.stderr)
            sys.exit(1)
        contents[key] = strip_frontmatter(path.read_text(encoding="utf-8"))

    # json.dumps produit un littéral JS valide, tous caractères spéciaux échappés
    today = date.today().isoformat()

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🧠 claude-mem — Analyse</title>
<style>
  :root {{
    --bg:#1e1e1e; --surface:#252526; --surface2:#2d2d30;
    --border:#3e3e42; --accent:#007acc; --accent2:#0e639c;
    --green:#4ec9b0; --yellow:#dcdcaa; --orange:#ce9178;
    --red:#f44747; --purple:#c586c0; --blue:#9cdcfe;
    --text:#d4d4d4; --text-dim:#858585;
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;font-size:14px;line-height:1.6}}
  .topbar{{background:var(--surface);border-bottom:1px solid var(--border);padding:0 24px;display:flex;align-items:center;position:sticky;top:0;z-index:100}}
  .topbar-title{{color:var(--blue);font-weight:700;font-size:15px;padding:12px 20px 12px 0;border-right:1px solid var(--border);margin-right:16px;white-space:nowrap}}
  .tab-btn{{background:none;border:none;color:var(--text-dim);cursor:pointer;padding:14px 20px;font-size:13px;font-family:inherit;border-bottom:2px solid transparent;transition:all .15s;white-space:nowrap}}
  .tab-btn:hover{{color:var(--text);background:var(--surface2)}}
  .tab-btn.active{{color:var(--accent);border-bottom-color:var(--accent)}}
  .content{{display:none;padding:32px 48px;max-width:1000px;margin:0 auto}}
  .content.active{{display:block}}
  h1{{color:var(--blue);font-size:22px;margin:0 0 24px;border-bottom:1px solid var(--border);padding-bottom:12px}}
  h2{{color:var(--yellow);font-size:16px;margin:28px 0 12px}}
  h3{{color:var(--green);font-size:14px;margin:20px 0 8px}}
  p{{margin-bottom:12px}}
  strong{{color:var(--orange)}}
  em{{color:var(--text-dim);font-style:italic}}
  ul,ol{{padding-left:24px;margin-bottom:12px}}
  li{{margin-bottom:4px}}
  blockquote{{border-left:3px solid var(--accent);padding:8px 16px;margin:16px 0;background:var(--surface2);color:var(--text-dim);font-style:italic;border-radius:0 4px 4px 0}}
  table{{width:100%;border-collapse:collapse;margin:16px 0;font-size:13px}}
  th{{background:var(--surface2);color:var(--yellow);text-align:left;padding:8px 12px;border:1px solid var(--border)}}
  td{{padding:7px 12px;border:1px solid var(--border);vertical-align:top}}
  tr:nth-child(even){{background:rgba(255,255,255,.02)}}
  tr:hover{{background:rgba(0,122,204,.05)}}
  code{{background:#0d0d0d;color:var(--orange);padding:2px 6px;border-radius:3px;font-family:'Cascadia Code','Consolas',monospace;font-size:12px}}
  pre{{background:#0d0d0d;padding:16px;border-radius:6px;overflow-x:auto;margin:12px 0;border:1px solid var(--border)}}
  pre code{{background:none;color:var(--text);padding:0;font-size:12px}}
  .card{{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:16px 20px;margin:16px 0}}
  .tag{{display:inline-block;padding:2px 8px;border-radius:3px;font-size:11px;font-weight:600;margin:2px}}
  .tag.green{{background:rgba(78,201,176,.15);color:var(--green);border:1px solid rgba(78,201,176,.3)}}
  .tag.yellow{{background:rgba(220,220,170,.12);color:var(--yellow);border:1px solid rgba(220,220,170,.25)}}
  .tag.red{{background:rgba(244,71,71,.12);color:var(--red);border:1px solid rgba(244,71,71,.25)}}
  .tag.blue{{background:rgba(156,220,254,.12);color:var(--blue);border:1px solid rgba(156,220,254,.25)}}
  .tag.purple{{background:rgba(197,134,192,.12);color:var(--purple);border:1px solid rgba(197,134,192,.25)}}
  .alert{{padding:10px 16px;border-radius:4px;margin:12px 0;font-size:13px;border-left:3px solid}}
  .alert.warn{{background:rgba(220,220,170,.08);border-color:var(--yellow);color:var(--yellow)}}
  .alert.danger{{background:rgba(244,71,71,.08);border-color:var(--red);color:var(--red)}}
  .score-row{{display:flex;align-items:center;gap:16px;margin:8px 0}}
  .score-label{{min-width:280px;color:var(--text-dim);font-size:13px}}
  .score-bar-wrap{{flex:1;background:var(--surface2);border-radius:4px;height:8px}}
  .score-bar{{height:8px;border-radius:4px;background:linear-gradient(90deg,var(--accent),var(--green))}}
  .score-num{{min-width:40px;text-align:right;color:var(--green);font-weight:700}}
  .hero{{background:linear-gradient(135deg,var(--surface) 0%,var(--surface2) 100%);border:1px solid var(--border);border-radius:8px;padding:24px 28px;margin-bottom:28px;display:flex;justify-content:space-between;align-items:flex-start;gap:24px}}
  .hero-title{{font-size:20px;color:var(--blue);font-weight:700;margin-bottom:6px}}
  .hero-desc{{color:var(--text-dim);font-size:13px;max-width:500px}}
  .hero-stats{{display:grid;grid-template-columns:repeat(2,auto);gap:8px 20px;text-align:right}}
  .stat-num{{font-size:18px;font-weight:700;color:var(--yellow)}}
  .stat-label{{font-size:11px;color:var(--text-dim);text-transform:uppercase;letter-spacing:.5px}}
  hr{{border:none;border-top:1px solid var(--border);margin:24px 0}}
  footer{{text-align:center;padding:32px;color:var(--text-dim);font-size:12px;border-top:1px solid var(--border);margin-top:48px}}
  footer a{{color:var(--accent);text-decoration:none}}
</style>
</head>
<body>

<div class="topbar">
  <div class="topbar-title">🧠 claude-mem — Analyse</div>
  <button class="tab-btn active" onclick="switchTab('recit',this)">📖 Récit</button>
  <button class="tab-btn" onclick="switchTab('fmaths',this)">🔬 Fmaths</button>
  <button class="tab-btn" onclick="switchTab('install',this)">⚙️ Installation</button>
  <button class="tab-btn" onclick="switchTab('verdict',this)">⚖️ Verdict</button>
</div>

<div id="tab-recit" class="content active">
  <div class="hero">
    <div>
      <div class="hero-title">🧠 thedotmack/claude-mem</div>
      <div class="hero-desc">Prothèse mnésique persistante pour agents IA — capture, compresse et réinjecte le contexte cross-session automatiquement.</div>
      <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
        <span class="tag blue">v13.3.0</span>
        <span class="tag green">Apache 2.0</span>
        <span class="tag purple">TypeScript 91.5%</span>
        <span class="tag yellow">7 agents</span>
        <span class="tag green">8.6/10</span>
      </div>
    </div>
    <div class="hero-stats">
      <div><span class="stat-num">78k</span><br><span class="stat-label">Stars</span></div>
      <div><span class="stat-num">6.7k</span><br><span class="stat-label">Forks</span></div>
      <div><span class="stat-num">271</span><br><span class="stat-label">Releases</span></div>
      <div><span class="stat-num">1906</span><br><span class="stat-label">Commits</span></div>
    </div>
  </div>
  <div id="md-recit"></div>
  <footer>Analyse fmaths + décodeur narratif · thedotmack/claude-mem v13.3.0 · Généré le {today} · <a href="https://github.com/thedotmack/claude-mem" target="_blank">GitHub ↗</a></footer>
</div>

<div id="tab-fmaths" class="content">
  <div id="md-fmaths"></div>
  <footer>Analyse fmaths + décodeur narratif · thedotmack/claude-mem v13.3.0 · Généré le {today} · <a href="https://github.com/thedotmack/claude-mem" target="_blank">GitHub ↗</a></footer>
</div>

<div id="tab-install" class="content">
  <div id="md-install"></div>
  <footer>Analyse fmaths + décodeur narratif · thedotmack/claude-mem v13.3.0 · Généré le {today} · <a href="https://github.com/thedotmack/claude-mem" target="_blank">GitHub ↗</a></footer>
</div>

<div id="tab-verdict" class="content">
  <div class="card" style="margin-bottom:24px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <h2 style="margin:0;color:var(--yellow)">Score global</h2>
      <span style="font-size:28px;font-weight:700;color:var(--green)">8.6<span style="font-size:14px;color:var(--text-dim)">/10</span></span>
    </div>
    <div class="score-row"><span class="score-label">Pertinence PM (prothèse mnésique)</span><div class="score-bar-wrap"><div class="score-bar" style="width:95%"></div></div><span class="score-num">9.5</span></div>
    <div class="score-row"><span class="score-label">Maturité prod</span><div class="score-bar-wrap"><div class="score-bar" style="width:80%"></div></div><span class="score-num">8.0</span></div>
    <div class="score-row"><span class="score-label">Facilité onboarding</span><div class="score-bar-wrap"><div class="score-bar" style="width:85%"></div></div><span class="score-num">8.5</span></div>
  </div>
  <div id="md-verdict"></div>
  <footer>Analyse fmaths + décodeur narratif · thedotmack/claude-mem v13.3.0 · Généré le {today} · <a href="https://github.com/thedotmack/claude-mem" target="_blank">GitHub ↗</a></footer>
</div>

<script>
{marked_js}
</script>
<script>
function switchTab(name, btn) {{
  document.querySelectorAll('.content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  btn.classList.add('active');
}}

marked.setOptions({{ breaks: true, gfm: true }});

var contents = {{
  recit:   {json.dumps(contents['recit'])},
  fmaths:  {json.dumps(contents['fmaths'])},
  install: {json.dumps(contents['install'])},
  verdict: {json.dumps(contents['verdict'])}
}};

document.getElementById('md-recit').innerHTML   = marked.parse(contents.recit);
document.getElementById('md-fmaths').innerHTML  = marked.parse(contents.fmaths);
document.getElementById('md-install').innerHTML = marked.parse(contents.install);
document.getElementById('md-verdict').innerHTML = marked.parse(contents.verdict);
</script>
</body>
</html>"""

    OUT.write_text(html, encoding="utf-8")
    size_kb = OUT.stat().st_size / 1024
    print(f"[OK] {OUT.name} — {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
