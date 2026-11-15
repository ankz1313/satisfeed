# satisfeed

Make short, soothing, **hands-only satisfying videos** — puzzle making, squishy toys — with AI, from inside [Claude Code](https://claude.ai/code).

Claude writes the shot prompts, generates clips with **Seedance 2.5** through the [Tein MCP](https://app.tein.ai/mcps), then joins them locally with soft crossfades, the clips' own click-and-squish sounds, and optional calm music.

## Themes

| Theme | What you get |
|---|---|
| `puzzle` | Overhead shots of hands assembling a jigsaw on a wooden table, soft clicks |
| `squishy` | Macro shots of hands squeezing a pastel slow-rise squishy, soft squish sounds |

Add your own in `config/themes.json`.

## Cost (Tein starter prices)

Default: 4 clips × 5 s with **Seedance 2.5 LITE** ($0.0719/s) ≈ **$1.44 per 20 s video**.
Ask for "quality" to use Seedance 2.5 ($0.1279/s ≈ $2.56). Joining, audio and export run locally for free.

## Setup

1. Install ffmpeg:
   ```bash
   brew install ffmpeg
   ```
2. Get a key at [app.tein.ai](https://app.tein.ai/mcps) and add it to your shell (not to this repo):
   ```bash
   echo 'export TEIN_API_KEY="your-key-here"' >> ~/.zshrc && source ~/.zshrc
   ```
3. Open this folder in Claude Code. The `tein` MCP server is configured in `.mcp.json`; `scripts/tein_headers.sh` reads the key from your shell when it connects, so it works even when Claude is opened from the Dock.
4. Optional: drop royalty-free calm music (`.mp3`, `.m4a`, `.wav`) into `assets/audio/`.

## Use

In Claude Code, type:

```
make puzzle
make squishy with music
make puzzle wide quality
review
```

Or run the steps yourself:

```bash
python3 scripts/new_project.py squishy --music
# ...generate clips with the Tein MCP and put the URLs in projects/<run>/plan.json...
python3 scripts/fetch_clips.py latest
python3 scripts/assemble.py latest
python3 scripts/review.py
```

## Layout

```
config/themes.json     theme presets
config/settings.json   model, prices, lengths, aspect, music volume, style rules
scripts/               new_project, fetch_clips, assemble (ffmpeg), review
assets/audio/          your music (git-ignored)
projects/<run>/        plan.json, clips/, final.mp4 (git-ignored)
```

Inspired by [gatherflix-ads](https://github.com/ankz1313/gatherflix-ads).

## Notes
- Hands only, no faces, no on-screen text — built into every prompt.
- Only use music you have the rights to.
- You're responsible for the content you generate and for following Tein's and Seedance's terms.

## License

MIT
