"""Shared engine for short explainer videos (LinkedIn / X), extracted from the Cogito capability-checks build.

A post's video lives in content/linkedin/<post>/video/ as two files:
  scenes.json    - title, size, fps and the scene list: {id, visual, narration}
  make_video.py  - one draw function per `visual`, a cover function, then `video_kit.run(...)`

Frames are drawn with Pillow and piped to ffmpeg; captions are burned in; narration comes from
ElevenLabs (ELEVENLABS_API_KEY in the environment or the repo-root .env). Per-scene MP3s are cached
in video/audio/ and only re-generated when the narration or voice changes.

Run from the repo root:
  uv run --with Pillow content/linkedin/<post>/video/make_video.py --stills   # one PNG per scene, no encode
  uv run --with Pillow content/linkedin/<post>/video/make_video.py --silent   # timing from word count
  uv run --with Pillow content/linkedin/<post>/video/make_video.py            # with voiceover
"""

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350  # 4:5 portrait: the largest feed footprint on LinkedIn
FPS = 30
BG = (11, 15, 26)
ORANGE = (255, 154, 60)
TEAL = (58, 209, 200)
VIOLET = (155, 123, 255)
WHITE = (245, 246, 250)
MUTED = (150, 160, 185)
PANEL = (18, 24, 40)
LINE = (60, 72, 104)
CONTENT_BOTTOM = 1060  # visuals stay above this line; captions live below it
CAPTION_Y = 1150  # caption box centre: clear of the bottom ~10% where players draw their controls bar
COVER_DUR = 1.0  # title card held at the start, so the first frame (the feed thumbnail) is not black
DEFAULT_VOICE = "JBFqnCBsd6RMkjVDRZzb"
TTS_MODEL = "eleven_multilingual_v2"
WORDS_PER_SEC = 2.5  # --silent / --stills timing estimate (the default ElevenLabs voice reads ~2.5 words/s)


def find_repo_root(start):
    for p in [start, *start.parents]:
        if (p / ".git").exists():
            return p
    return start


ROOT = find_repo_root(Path(__file__).resolve().parent)
ASSETS = ROOT / ".cursor/skills/linkedin-carousel/assets"

# ---------------------------------------------------------------- fonts


def font(name, size):
    return ImageFont.truetype(str(ASSETS / name), size)


def HEAD(size):
    return font("Outfit-Bold.ttf", size)


def BODY(size):
    return font("WorkSans-Regular.ttf", size)


def mono(size):
    for cand in ["DejaVuSansMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                 "/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Courier.ttc",
                 "/Library/Fonts/Courier New.ttf", "Courier New.ttf", "cour.ttf",
                 "/usr/share/fonts/truetype/freefont/FreeMono.ttf"]:
        try:
            return ImageFont.truetype(cand, size)
        except OSError:
            continue
    sys.exit("No monospace font found (tried DejaVuSansMono, Menlo, Courier).")


_EMOJI_FONT = None
_EMOJI_CACHE = {}


def emoji(ch, size):
    """RGBA image of a colour emoji `size` px tall, or None when no colour emoji font is available.

    Apple Color Emoji only renders at fixed strikes, so draw at 160 px and resize."""
    global _EMOJI_FONT
    key = (ch, size)
    if key in _EMOJI_CACHE:
        return _EMOJI_CACHE[key]
    if _EMOJI_FONT is None:
        for cand in ["/System/Library/Fonts/Apple Color Emoji.ttc",
                     "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"]:
            try:
                _EMOJI_FONT = ImageFont.truetype(cand, 160 if "Apple" in cand else 109)
                break
            except OSError:
                continue
        else:
            _EMOJI_FONT = False
    if not _EMOJI_FONT:
        _EMOJI_CACHE[key] = None
        return None
    canvas = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
    ImageDraw.Draw(canvas).text((110, 110), ch, font=_EMOJI_FONT, embedded_color=True, anchor="mm")
    bbox = canvas.getbbox()
    img = canvas.crop(bbox) if bbox else canvas
    img = img.resize((max(1, round(img.width * size / img.height)), size), Image.LANCZOS)
    _EMOJI_CACHE[key] = img
    return img


def paste_emoji(frame, ch, cx, cy, size, opacity=1.0):
    img = emoji(ch, size)
    if img is None or opacity <= 0:
        return
    if opacity < 1:
        img = img.copy()
        img.putalpha(img.getchannel("A").point(lambda v: int(v * opacity)))
    frame.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))

# ---------------------------------------------------------------- helpers


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def seg(t, a, b):
    """Progress 0..1 of t inside [a, b]."""
    return clamp((t - a) / max(b - a, 1e-6))


def mix(c1, c2, k):
    return tuple(int(round(a + (b - a) * k)) for a, b in zip(c1, c2))


def alpha(c, a):
    return (*c[:3], int(clamp(a) * 255))


def text_c(d, xy, s, f, fill, anchor="mm", **kw):
    # Drawing on an overlay layer replaces pixels instead of blending them, so fully transparent
    # text would erase whatever is already under it: skip it.
    if len(fill) == 4 and fill[3] == 0:
        return
    d.text(xy, s, font=f, fill=fill, anchor=anchor, **kw)


def overlay(frame, draw_fn):
    """Draw with alpha onto an RGBA layer, then composite."""
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer), layer)
    frame.alpha_composite(layer)


def blit_cam(frame, src, scale, ox, oy):
    """Draw src scaled by `scale` with its top-left at frame (ox, oy); only the visible part is resampled."""
    x0, y0 = max(0.0, ox), max(0.0, oy)
    x1, y1 = min(W, ox + src.width * scale), min(H, oy + src.height * scale)
    if x1 <= x0 or y1 <= y0:
        return
    dx0, dy0, dx1, dy1 = int(math.floor(x0)), int(math.floor(y0)), int(math.ceil(x1)), int(math.ceil(y1))
    box = ((dx0 - ox) / scale, (dy0 - oy) / scale, (dx1 - ox) / scale, (dy1 - oy) / scale)
    box = (max(0, box[0]), max(0, box[1]), min(src.width, box[2]), min(src.height, box[3]))
    tile = src.resize((dx1 - dx0, dy1 - dy0), Image.BICUBIC, box=box)
    frame.paste(tile, (dx0, dy0))


def cover_fit(src, zoom=1.0, fx=0.5, fy=0.5):
    """Return a W x H RGB image filled with src (like CSS object-fit: cover), focused on (fx, fy)."""
    s = max(W / src.width, H / src.height) * zoom
    ox = min(0, max(W - src.width * s, W / 2 - src.width * fx * s))
    oy = min(0, max(H - src.height * s, H / 2 - src.height * fy * s))
    out = Image.new("RGB", (W, H), BG)
    blit_cam(out, src, s, ox, oy)
    return out


def wrap(text, f, max_w, d):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def check_mark(d, cx, cy, size, fill, width=8):
    """Hand-drawn check mark (the bundled fonts have no ✓ glyph)."""
    d.line([(cx - size * 0.5, cy), (cx - size * 0.12, cy + size * 0.38), (cx + size * 0.55, cy - size * 0.42)],
           fill=fill, width=width, joint="curve")


def cue(narration, phrase, default):
    """Fraction of the narration (by characters) where `phrase` starts; used to time visuals to the voice."""
    i = narration.find(phrase)
    return i / len(narration) if i >= 0 else default


def top_shade(frame, height=520, strength=0.85):
    grad = Image.new("L", (1, height))
    for y in range(height):
        grad.putpixel((0, y), int(255 * strength * (1 - y / height) ** 1.3))
    black = Image.new("RGBA", (W, height), (*BG, 255))
    black.putalpha(grad.resize((W, height)))
    frame.alpha_composite(black, (0, 0))


def bottom_shade(frame, height=420, strength=0.8):
    grad = Image.new("L", (1, height))
    for y in range(height):
        grad.putpixel((0, y), int(255 * strength * (y / height) ** 1.5))
    black = Image.new("RGBA", (W, height), (*BG, 255))
    black.putalpha(grad.resize((W, height)))
    frame.alpha_composite(black, (0, H - height))

# ---------------------------------------------------------------- captions


def caption_chunks(narration, max_chars=34):
    words, lines, cur = narration.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) <= max_chars or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    chunks = [lines[i:i + 2] for i in range(0, len(lines), 2)]
    total = sum(len(" ".join(c)) for c in chunks)
    out, acc = [], 0
    for c in chunks:
        n = len(" ".join(c))
        out.append((acc / total, (acc + n) / total, c))
        acc += n
    return out


_CAP_FONT = None


def draw_caption(frame, t, speech, chunks):
    global _CAP_FONT
    _CAP_FONT = _CAP_FONT or BODY(44)
    u = (t - 0.1) / max(speech, 0.1)
    cur = None
    for a, b, lines in chunks:
        if a <= u < b:
            cur = lines
    if cur is None:
        cur = chunks[-1][2] if u >= 1 else chunks[0][2]

    def draw(d, _):
        lh = 58
        bw = max(d.textlength(s, font=_CAP_FONT) for s in cur) + 70
        bh = lh * len(cur) + 36
        cy = CAPTION_Y
        d.rounded_rectangle([W / 2 - bw / 2, cy - bh / 2, W / 2 + bw / 2, cy + bh / 2], 20, fill=(0, 0, 0, 165))
        for i, s in enumerate(cur):
            text_c(d, (W / 2, cy - (len(cur) - 1) * lh / 2 + i * lh), s, _CAP_FONT, WHITE)
    overlay(frame, draw)

# ---------------------------------------------------------------- audio


def load_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    voice = os.environ.get("ELEVENLABS_VOICE_ID")
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip().removeprefix("export ").strip(), v.strip().strip('"').strip("'")
            if k == "ELEVENLABS_API_KEY" and not key:
                key = v
            if k == "ELEVENLABS_VOICE_ID" and not voice:
                voice = v
    return key, voice or DEFAULT_VOICE


def tts(text, key, voice, dest):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128"
    body = json.dumps({"text": text, "model_id": TTS_MODEL}).encode()
    headers = {"Content-Type": "application/json", "Accept": "audio/mpeg"}
    if key:  # without a key we rely on a proxy that injects it (Claude Code cloud sessions)
        headers["xi-api-key"] = key
    req = urllib.request.Request(url, data=body, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs TTS failed: HTTP {e.code} {e.read()[:300]!r}")
    if len(data) < 1000:
        sys.exit(f"ElevenLabs returned a suspiciously small file ({len(data)} bytes) for {dest.name}")
    dest.write_bytes(data)


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def prepare_audio(scenes, audio_dir, regen):
    key, voice = load_key()
    if not key and not os.environ.get("HTTPS_PROXY"):
        sys.exit("No ELEVENLABS_API_KEY in the environment or .env. Add it, or run with --silent.")
    if not key:
        print("No ELEVENLABS_API_KEY; trying the HTTPS proxy's credential injection.")
    audio_dir.mkdir(exist_ok=True)
    manifest_path = audio_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for sc in scenes:
        mp3 = audio_dir / f"{sc['id']}.mp3"
        sig = hashlib.sha256(f"{voice}|{TTS_MODEL}|{sc['narration']}".encode()).hexdigest()[:16]
        if regen or not mp3.exists() or manifest.get(sc["id"]) != sig:
            print(f"TTS {sc['id']} …", flush=True)
            tts(sc["narration"], key, voice, mp3)
            manifest[sc["id"]] = sig
        sc["audio"] = mp3
        sc["speech"] = probe_duration(mp3)
        sc["dur"] = sc["speech"] + 0.4
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"voice: {voice}")


def estimate_timing(scenes):
    for sc in scenes:
        sc["speech"] = len(sc["narration"].split()) / WORDS_PER_SEC
        sc["dur"] = sc["speech"] + 0.6

# ---------------------------------------------------------------- render


def scene_frame(scene_fns, sc, t, chunks):
    frame = Image.new("RGBA", (W, H), (*BG, 255))
    scene_fns[sc["visual"]](frame, t, sc["dur"], sc["speech"], sc)
    draw_caption(frame, t, sc["speech"], chunks)
    return frame


def render(scenes, scene_fns, make_cover, out_video, cover_path):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out_video)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    cover = make_cover()
    cover.save(cover_path, quality=92)
    for _ in range(int(round(COVER_DUR * FPS))):
        proc.stdin.write(cover.tobytes())
    fade_from = cover  # the first scene cross-fades from the title card, later ones from black
    for sc in scenes:
        chunks = caption_chunks(sc["narration"])
        n = int(round(sc["dur"] * FPS))
        print(f"{sc['id']}: {sc['dur']:.2f}s, {n} frames", flush=True)
        for i in range(n):
            t = i / FPS
            rgb = scene_frame(scene_fns, sc, t, chunks).convert("RGB")
            fade = ease(t / 0.3)
            if fade < 1:
                rgb = Image.blend(fade_from, rgb, fade)
            proc.stdin.write(rgb.tobytes())
        fade_from = Image.new("RGB", (W, H), (0, 0, 0))
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg video encode failed")


def mux(scenes, video, out):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video)]
    for sc in scenes:
        cmd += ["-i", str(sc["audio"])]
    filt = "".join(f"[{i + 1}:a]aresample=44100,apad,atrim=0:{sc['dur']:.3f},asetpts=N/SR/TB[a{i}];"
                   for i, sc in enumerate(scenes))
    filt += "".join(f"[a{i}]" for i in range(len(scenes))) + f"concat=n={len(scenes)}:v=0:a=1,"
    filt += f"adelay={int(COVER_DUR * 1000)}:all=1[aout]"  # audio starts after the title card
    cmd += ["-filter_complex", filt, "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac",
            "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)


def write_stills(scenes, scene_fns, make_cover, stills_dir, at=(0.35, 0.95)):
    """Review mode: the cover plus frames at fractions `at` of each scene, as PNGs. No encoding."""
    stills_dir.mkdir(exist_ok=True)
    make_cover().save(stills_dir / "00_cover.png")
    for k, sc in enumerate(scenes, start=1):
        chunks = caption_chunks(sc["narration"])
        for frac in at:
            t = sc["dur"] * frac
            scene_frame(scene_fns, sc, t, chunks).convert("RGB").save(stills_dir / f"{k:02d}_{sc['id']}_{int(frac * 100)}.png")
    print(f"wrote stills to {stills_dir}")


def run(here, scene_fns, make_cover, out_name):
    """CLI entry point for a post's make_video.py."""
    here = Path(here)
    ap = argparse.ArgumentParser(description="Render a short explainer video from scenes.json.")
    ap.add_argument("--silent", action="store_true", help="no voiceover; timing from word count")
    ap.add_argument("--stills", action="store_true", help="write review PNGs to video/stills/ and stop")
    ap.add_argument("--regen", action="store_true", help="re-generate all TTS clips")
    ap.add_argument("--out", type=Path, default=here / out_name)
    args = ap.parse_args()

    spec = json.loads((here / "scenes.json").read_text())
    assert spec["size"] == [W, H] and spec["fps"] == FPS, "scenes.json size/fps differ from the renderer"
    scenes = spec["scenes"]
    missing = {sc["visual"] for sc in scenes} - set(scene_fns)
    assert not missing, f"no draw function for visuals: {sorted(missing)}"

    if args.silent or args.stills:
        estimate_timing(scenes)
    else:
        prepare_audio(scenes, here / "audio", args.regen)

    if args.stills:
        write_stills(scenes, scene_fns, make_cover, here / "stills")
        return
    cover_path = here / "cover.jpg"
    if args.silent:
        render(scenes, scene_fns, make_cover, args.out, cover_path)
    else:
        tmp = args.out.with_suffix(".video.mp4")
        render(scenes, scene_fns, make_cover, tmp, cover_path)
        mux(scenes, tmp, args.out)
        tmp.unlink()
    total = COVER_DUR + sum(sc["dur"] for sc in scenes)
    print(f"wrote {args.out} ({total:.1f}s, {args.out.stat().st_size / 1e6:.1f} MB)")
