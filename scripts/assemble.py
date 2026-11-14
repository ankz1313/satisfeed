"""Join a project's clips with soft crossfades, optionally mix in calm music, export final.mp4.

Usage:
  python3 scripts/assemble.py latest
  python3 scripts/assemble.py latest --music            # force music on
  python3 scripts/assemble.py latest --music-file assets/audio/calm.mp3
  python3 scripts/assemble.py latest --no-music

Requires ffmpeg and ffprobe (brew install ffmpeg).
"""
import argparse
import random
import shutil
import subprocess
from pathlib import Path

from common import AUDIO, load_json, resolve_project, settings

AUDIO_EXT = {".mp3", ".m4a", ".wav", ".aac", ".flac", ".ogg"}


def need(tool):
    if not shutil.which(tool):
        raise SystemExit("%s not found. Install it with: brew install ffmpeg" % tool)


def probe_duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", str(path)])
    return float(out.strip())


def has_audio(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "a",
        "-show_entries", "stream=index", "-of", "csv=p=0", str(path)])
    return bool(out.strip())


def pick_music(explicit):
    if explicit:
        p = Path(explicit)
        if not p.exists():
            raise SystemExit("Music file not found: %s" % p)
        return p
    tracks = [p for p in AUDIO.iterdir() if p.suffix.lower() in AUDIO_EXT]
    if not tracks:
        print("No music in assets/audio — exporting without music.")
        return None
    return random.choice(tracks)


def main():
    need("ffmpeg")
    need("ffprobe")
    s = settings()
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--music", action="store_true")
    g.add_argument("--no-music", action="store_true")
    ap.add_argument("--music-file")
    ap.add_argument("--fade", type=float, default=s["crossfade_seconds"])
    args = ap.parse_args()

    run = resolve_project(args.project)
    plan = load_json(run / "plan.json")
    w, h = s["output_sizes"][plan.get("aspect", s["aspect"])]

    clips = sorted((run / "clips").glob("*.mp4"))
    if not clips:
        raise SystemExit("No clips in %s/clips — generate and fetch them first." % run)

    use_music = plan.get("music", False)
    if args.music or args.music_file:
        use_music = True
    if args.no_music:
        use_music = False
    music = pick_music(args.music_file) if use_music else None

    fade = args.fade
    durations = [probe_duration(c) for c in clips]
    if len(clips) > 1:
        fade = min(fade, min(durations) / 2.0)

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for c in clips:
        cmd += ["-i", str(c)]
    music_idx = None
    if music:
        music_idx = len(clips)
        cmd += ["-stream_loop", "-1", "-i", str(music)]

    f = []
    # Normalise every clip to the same size, frame rate and audio format.
    for i, c in enumerate(clips):
        f.append(
            "[%d:v]scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,"
            "setsar=1,fps=30,format=yuv420p,settb=AVTB[v%d]" % (i, w, h, w, h, i))
        if has_audio(c):
            f.append("[%d:a]aresample=48000,aformat=channel_layouts=stereo,"
                     "volume=%.2f[a%d]" % (i, s["clip_audio_volume"], i))
        else:
            f.append("anullsrc=r=48000:cl=stereo,atrim=duration=%.3f[a%d]" % (durations[i], i))

    # Chain crossfades.
    vlast, alast = "v0", "a0"
    offset = 0.0
    for i in range(1, len(clips)):
        offset += durations[i - 1] - fade
        f.append("[%s][v%d]xfade=transition=fade:duration=%.3f:offset=%.3f[vx%d]"
                 % (vlast, i, fade, offset, i))
        f.append("[%s][a%d]acrossfade=d=%.3f[ax%d]" % (alast, i, fade, i))
        vlast, alast = "vx%d" % i, "ax%d" % i
    total = sum(durations) - fade * (len(clips) - 1)

    # Gentle fade in/out on the whole piece.
    edge = min(0.5, total / 4)
    f.append("[%s]fade=t=in:st=0:d=%.2f,fade=t=out:st=%.3f:d=%.2f[vout]"
             % (vlast, edge, total - edge, edge))

    if music_idx is not None:
        f.append("[%d:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration=%.3f,"
                 "volume=%.2f,afade=t=in:st=0:d=1.5,afade=t=out:st=%.3f:d=1.5[mus]"
                 % (music_idx, total, s["music_volume"], max(0, total - 1.5)))
        f.append("[%s][mus]amix=inputs=2:duration=first:normalize=0[amix]" % alast)
        alast = "amix"
    f.append("[%s]afade=t=in:st=0:d=%.2f,afade=t=out:st=%.3f:d=%.2f[aout]"
             % (alast, edge, total - edge, edge))

    out = run / "final.mp4"
    cmd += ["-filter_complex", ";".join(f), "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
            "-t", "%.3f" % total, str(out)]
    subprocess.check_call(cmd)
    print("Exported %s (%.1fs, %dx%d%s)"
          % (out, total, w, h, ", music: %s" % music.name if music else ""))


if __name__ == "__main__":
    main()
