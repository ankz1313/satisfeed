---
name: make-video
description: Make a short, soothing hands-only satisfying video (puzzle making, squishy toys) with Seedance through the Tein MCP, then join the clips with soft crossfades and optional calm music. Use when the user says "make puzzle", "make squishy", "make a video", or asks for a new satisfying clip.
---

# Make a satisfying video

Follow these steps in order. Keep the user posted with one short line per step.

## 1. Start the run

Read `config/themes.json` and `config/settings.json`. Work out from the user's words:
- **theme**: `puzzle` or `squishy` (ask if unclear)
- **music**: on only if the user asks ("with music", "add music"); otherwise use `settings.music`
- **quality**: only if the user asks for higher quality ("best", "quality", "Seedance 2.5")
- **aspect**: 9:16 unless the user asks for wide/YouTube (16:9) or square (1:1)

Run:
```bash
python3 scripts/new_project.py <theme> [--music] [--quality] [--aspect 16:9] [--clips N]
```
Tell the user the estimated cost it prints. If it is over $3, confirm before generating.

## 2. Write the shot prompts

Fill `shots[].prompt` in the new `projects/<run>/plan.json`. See [PROMPTS.md](PROMPTS.md) for the template.
- Shots must flow as one continuous scene: same table/surface, same hands, same object, same light.
- Pick shots from the theme's `shot_ideas` in an order that builds to a satisfying ending.
- Every prompt must include all `style_rules` from settings and the theme's `sound_cues`.

## 3. Generate clips with Tein

Use the `tein` MCP server. Choose the model named in `plan.model` (default **Seedance 2.5 LITE**).
- Duration: `plan.clip_seconds`. Aspect ratio: `plan.aspect`. Ask for native audio if the tool offers it.
- If a tool needs a local file (e.g. a reference image), send it with `upload_asset`.
- Submit all shots, then check their status until each finishes. Don't resubmit a shot that is still running.
- Write each finished video URL to `shots[].url` and set `status` to `"done"`; on failure set `"failed"` and tell the user (retry once at most).

## 4. Download, join, review

```bash
python3 scripts/fetch_clips.py latest
python3 scripts/assemble.py latest          # add --music / --no-music to override
python3 scripts/review.py
```
Report: the output path, length, model, music on/off, and the estimated cost.

## Rules
- Never put the Tein key in any file in this repo. It lives in the shell as `TEIN_API_KEY`.
- Hands only — no faces. No text or logos on screen.
- Stay on the cheap model unless the user asks otherwise.
