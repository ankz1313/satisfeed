# satisfeed

Makes short, soothing, hands-only satisfying videos (puzzle making, squishy toys) with Seedance via the Tein MCP (`.mcp.json`, server `tein`).

## Commands the user may type
| Command | What to do |
|---|---|
| `make puzzle` / `make squishy` (optionally "with music", "quality", "wide") | Use the `make-video` skill |
| `review` | `python3 scripts/review.py` |
| `themes` | List themes from `config/themes.json` with one line each |

## Layout
- `config/themes.json` — theme presets (subject, hands, camera, lighting, sound cues, shot ideas)
- `config/settings.json` — model, prices, clip length/count, aspect, music volume, style rules
- `scripts/` — `new_project.py`, `fetch_clips.py`, `assemble.py` (ffmpeg), `review.py`
- `assets/audio/` — the user's own royalty-free music (git-ignored)
- `projects/<run>/` — `plan.json`, `clips/`, `final.mp4` (git-ignored)

## Rules
- The Tein key is only ever the `TEIN_API_KEY` environment variable. Never write it to a file.
- Default to the cheap model (Seedance 2.5 LITE). Confirm before any run estimated over $3.
- Scripts must stay compatible with Python 3.9 (macOS system Python), standard library only.
