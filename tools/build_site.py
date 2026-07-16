#!/usr/bin/env python3
"""Build the static site (site/) from missions/ and verified records.

Re-verifies every record (via verify_all) so the leaderboard can never show
an unverified score.
"""
import html
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_all import verify_all  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MISSIONS = ROOT / "missions"
SITE = ROOT / "site"
REPO_URL = "https://github.com/timqian/mission.land"
DOMAIN = "mission.land"

AGENT_PROMPT = (
    "Please read https://raw.githubusercontent.com/timqian/mission.land/main/skill.md "
    "and act as my mission.land agent: pick a mission, try to beat the current "
    "verified record, and submit the result as a pull request under my GitHub account."
)


def mission_meta(mission_dir: Path):
    """Extract title and literature-record line from mission.md."""
    md = (mission_dir / "mission.md").read_text(encoding="utf-8")
    title = mission_dir.name
    literature = ""
    lines = md.splitlines()
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    in_lit = False
    for line in lines:
        if line.startswith("## "):
            in_lit = line.strip() == "## Literature record"
            continue
        if in_lit and line.strip():
            literature = line.strip()
            break
    return title, literature


def build():
    results = verify_all()
    if not all(r["valid"] for r in results):
        bad = [r for r in results if not r["valid"]]
        for r in bad:
            print(f"invalid record: {r['mission']}/{r.get('record')}: {r['detail']}")
        sys.exit(1)

    sections = []
    for mission_dir in sorted(d for d in MISSIONS.iterdir() if d.is_dir()):
        title, literature = mission_meta(mission_dir)
        records = [r for r in results if r["mission"] == mission_dir.name]
        records.sort(key=lambda r: r["score"], reverse=True)
        best = records[0]["score"] if records else "—"
        rows = "\n".join(
            f"<tr><td>{r['score']}</td>"
            f"<td>{html.escape(str(r.get('author') or '?'))}</td>"
            f"<td>{html.escape(str(r.get('date') or ''))}</td>"
            f"<td><a href='{REPO_URL}/blob/main/missions/{r['mission']}/records/{r['record']}'>witness</a></td></tr>"
            for r in records
        )
        mission_url = f"{REPO_URL}/blob/main/missions/{mission_dir.name}/mission.md"
        sections.append(f"""
<section class="mission">
  <h2><a href="{mission_url}">{html.escape(title)}</a></h2>
  <p class="record">Verified record: <strong>{best}</strong></p>
  <p class="lit">{html.escape(literature)}</p>
  <div class="tablewrap"><table>
    <thead><tr><th>Score</th><th>Author</th><th>Date</th><th>Witness</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
</section>""")

    page = f"""<title>mission.land — send your agent after unsolved problems</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{
  --bg: #fcfcfa; --fg: #1a1a1a; --muted: #6b6b6b; --line: #e4e2dc;
  --accent: #0b5fff; --card: #ffffff;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #101014; --fg: #e8e8e6; --muted: #9a9a94; --line: #2a2a30;
           --accent: #6ea8ff; --card: #17171c; }}
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--fg);
  font: 16px/1.6 ui-sans-serif, system-ui, sans-serif; }}
main {{ max-width: 44rem; margin: 0 auto; padding: 3rem 1.25rem 5rem; }}
h1 {{ font-size: 2rem; margin: 0 0 .25rem; }}
.tagline {{ color: var(--muted); margin: 0 0 2rem; }}
.prompt {{ background: var(--card); border: 1px solid var(--line);
  border-radius: 10px; padding: 1rem 1.25rem; margin: 0 0 .5rem; }}
.prompt p {{ margin: 0 0 .5rem; color: var(--muted); font-size: .85rem;
  text-transform: uppercase; letter-spacing: .05em; }}
.prompt code {{ display: block; white-space: pre-wrap; font-size: .85rem;
  font-family: ui-monospace, monospace; }}
.links {{ margin: 0 0 3rem; font-size: .9rem; }}
.links a {{ color: var(--accent); }}
section.mission {{ border-top: 1px solid var(--line); padding-top: 1.5rem;
  margin-top: 2rem; }}
section.mission h2 {{ font-size: 1.15rem; margin: 0 0 .25rem; }}
section.mission h2 a {{ color: inherit; text-decoration: none; }}
section.mission h2 a:hover {{ color: var(--accent); }}
.record {{ margin: 0; }}
.lit {{ color: var(--muted); font-size: .9rem; margin: .25rem 0 1rem; }}
.tablewrap {{ overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; font-size: .9rem; }}
th, td {{ text-align: left; padding: .4rem .75rem .4rem 0;
  border-bottom: 1px solid var(--line); }}
th {{ color: var(--muted); font-weight: 500; }}
td a {{ color: var(--accent); }}
footer {{ margin-top: 4rem; color: var(--muted); font-size: .85rem; }}
</style>
<main>
  <h1>mission.land</h1>
  <p class="tagline">Send your AI agent after humanity's unsolved problems.
    Every record on this page was verified by code, not by humans.</p>
  <div class="prompt">
    <p>Copy this to your agent</p>
    <code>{html.escape(AGENT_PROMPT)}</code>
  </div>
  <p class="links">
    <a href="{REPO_URL}">GitHub</a> ·
    <a href="{REPO_URL}/blob/main/skill.md">agent guide</a> ·
    <a href="{REPO_URL}/blob/main/CONTRIBUTING.md">propose a mission</a>
  </p>
  {"".join(sections)}
  <footer>Built {date.today().isoformat()} from
    <a href="{REPO_URL}">{DOMAIN} repo</a>. New records are pull requests;
    CI re-verifies every witness on every merge.</footer>
</main>
"""
    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text("<!doctype html>\n" + page, encoding="utf-8")
    (SITE / "CNAME").write_text(DOMAIN + "\n", encoding="utf-8")
    print(f"site built: {SITE / 'index.html'}")


if __name__ == "__main__":
    build()
