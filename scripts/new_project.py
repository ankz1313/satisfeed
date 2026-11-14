"""Create a new video run folder with a plan.json skeleton and a cost estimate.

Usage:
  python3 scripts/new_project.py puzzle
  python3 scripts/new_project.py squishy --clips 3 --music --aspect 16:9 --quality
"""
import argparse
import datetime

from common import PROJECTS, save_json, settings, themes


def main():
    s = settings()
    t = themes()
    ap = argparse.ArgumentParser()
    ap.add_argument("theme", choices=sorted(t.keys()))
    ap.add_argument("--clips", type=int, default=s["clips"])
    ap.add_argument("--seconds", type=int, default=s["clip_seconds"], help="seconds per clip")
    ap.add_argument("--aspect", default=s["aspect"], choices=sorted(s["output_sizes"].keys()))
    ap.add_argument("--music", action="store_true", help="add calm music from assets/audio")
    ap.add_argument("--quality", action="store_true", help="use the pricier quality model")
    args = ap.parse_args()

    model = s["quality_model"] if args.quality else s["model"]
    price = s["price_per_second"].get(model, 0)
    total_seconds = args.clips * args.seconds
    est = round(total_seconds * price, 2)

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    run = PROJECTS / ("%s-%s" % (stamp, args.theme))
    (run / "clips").mkdir(parents=True)

    plan = {
        "theme": args.theme,
        "model": model,
        "aspect": args.aspect,
        "clip_seconds": args.seconds,
        "music": bool(args.music or s["music"]),
        "estimated_cost_usd": est,
        "shots": [
            {"index": i + 1, "prompt": "", "status": "todo", "url": "", "file": ""}
            for i in range(args.clips)
        ],
    }
    save_json(run / "plan.json", plan)
    print(run)
    print("Model: %s | %d clips x %ds = %ds | estimated cost ~$%.2f"
          % (model, args.clips, args.seconds, total_seconds, est))


if __name__ == "__main__":
    main()
