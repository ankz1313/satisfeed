"""Shared helpers for satisfeed scripts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
PROJECTS = ROOT / "projects"
AUDIO = ROOT / "assets" / "audio"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def settings():
    return load_json(CONFIG / "settings.json")


def themes():
    return load_json(CONFIG / "themes.json")


def resolve_project(name_or_path):
    """Accept a project folder name, a path, or 'latest'."""
    if name_or_path == "latest":
        runs = sorted(p for p in PROJECTS.iterdir() if (p / "plan.json").exists())
        if not runs:
            raise SystemExit("No projects yet. Run scripts/new_project.py first.")
        return runs[-1]
    p = Path(name_or_path)
    if not p.is_absolute() and not p.exists():
        p = PROJECTS / name_or_path
    if not (p / "plan.json").exists():
        raise SystemExit("Not a satisfeed project (no plan.json): %s" % p)
    return p
