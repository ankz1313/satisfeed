"""Build projects/review.html showing every finished video side by side, then open it.

Usage:
  python3 scripts/review.py           # build and open
  python3 scripts/review.py --no-open
"""
import html
import subprocess
import sys

from common import PROJECTS, load_json


def main():
    cards = []
    for run in sorted(PROJECTS.iterdir(), reverse=True):
        plan_path = run / "plan.json"
        final = run / "final.mp4"
        if not plan_path.exists() or not final.exists():
            continue
        plan = load_json(plan_path)
        prompts = "".join(
            "<li>%s</li>" % html.escape(s.get("prompt", "")) for s in plan.get("shots", []))
        cards.append("""
<article>
  <video src="%s/final.mp4" controls loop muted playsinline></video>
  <h2>%s</h2>
  <p class="meta">%s · %s · %s · ~$%.2f</p>
  <details><summary>Shot prompts</summary><ol>%s</ol></details>
</article>""" % (
            html.escape(run.name), html.escape(plan.get("theme", "")),
            html.escape(run.name), html.escape(plan.get("model", "")),
            "music" if plan.get("music") else "no music",
            plan.get("estimated_cost_usd", 0), prompts))

    page = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>satisfeed review</title>
<style>
:root{--bg:#f6f3ee;--card:#fff;--ink:#2b2a28;--muted:#7a756d}
@media (prefers-color-scheme:dark){:root{--bg:#1c1b1a;--card:#262523;--ink:#eee9e1;--muted:#a39d93}}
body{margin:0;padding:24px 16px;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}
h1{font-weight:600;margin:0 0 16px}
main{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}
article{background:var(--card);border-radius:14px;padding:12px}
video{width:100%%;border-radius:10px;background:#000}
h2{font-size:16px;margin:8px 0 2px;text-transform:capitalize}
.meta{color:var(--muted);font-size:13px;margin:0 0 6px}
details{font-size:13px;color:var(--muted)}
</style></head><body><h1>satisfeed review</h1><main>%s</main></body></html>""" % (
        "".join(cards) or "<p>No finished videos yet.</p>")

    out = PROJECTS / "review.html"
    out.write_text(page, encoding="utf-8")
    print(out)
    if "--no-open" not in sys.argv:
        subprocess.call(["open", str(out)])


if __name__ == "__main__":
    main()
