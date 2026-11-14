"""Download generated clip URLs recorded in plan.json into the project's clips/ folder.

Usage:
  python3 scripts/fetch_clips.py latest
  python3 scripts/fetch_clips.py 20261114-101500-puzzle
"""
import sys
import urllib.request

from common import load_json, resolve_project, save_json


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    run = resolve_project(sys.argv[1])
    plan = load_json(run / "plan.json")
    got = 0
    for shot in plan["shots"]:
        url = shot.get("url")
        if not url:
            continue
        dest = run / "clips" / ("%02d.mp4" % shot["index"])
        if dest.exists() and dest.stat().st_size > 0:
            shot["file"] = str(dest.relative_to(run))
            continue
        print("Downloading shot %d ..." % shot["index"])
        req = urllib.request.Request(url, headers={"User-Agent": "satisfeed/0.1"})
        with urllib.request.urlopen(req, timeout=300) as r, open(dest, "wb") as f:
            while True:
                chunk = r.read(1 << 16)
                if not chunk:
                    break
                f.write(chunk)
        shot["file"] = str(dest.relative_to(run))
        shot["status"] = "downloaded"
        got += 1
    save_json(run / "plan.json", plan)
    print("Downloaded %d new clip(s) into %s" % (got, run / "clips"))


if __name__ == "__main__":
    main()
