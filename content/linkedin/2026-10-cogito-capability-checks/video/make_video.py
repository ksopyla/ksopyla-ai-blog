"""Render the Cogito Capability Checks explainer video (1080x1350, 4:5) for LinkedIn.

Usage (from the repo root):
    uv run --with Pillow content/linkedin/2026-10-cogito-capability-checks/video/make_video.py           # voiceover
    uv run --with Pillow content/linkedin/2026-10-cogito-capability-checks/video/make_video.py --silent  # no audio

Voiceover needs ELEVENLABS_API_KEY (environment, or a KEY=VALUE line in the repo-root .env);
behind a credential-injecting HTTPS proxy (Claude Code cloud) the key may be absent.
ELEVENLABS_VOICE_ID is optional. Per-scene MP3s are cached in video/audio/ and only
re-generated when the narration or voice changes (or with --regen).
Frames are drawn with Pillow and piped to ffmpeg; captions are burned in.
Outputs (the mp4, cover.jpg and audio/) are build artifacts and are gitignored: rebuild, don't commit.
"""

import argparse
import hashlib
import json
import math
import os
import random
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
POST_DIR = HERE.parent
AUDIO_DIR = HERE / "audio"
OUT = HERE / "cogito-capability-checks.mp4"
COVER = HERE / "cover.jpg"
COVER_DUR = 1.0  # silent title card held at the start, so the first frame (LinkedIn's thumbnail) is not black
DEFAULT_VOICE = "JBFqnCBsd6RMkjVDRZzb"
TTS_MODEL = "eleven_multilingual_v2"


def find_repo_root():
    for p in [HERE, *HERE.parents]:
        if (p / ".git").exists():
            return p
    return HERE.parents[3]


ROOT = find_repo_root()
ASSETS = ROOT / ".cursor/skills/linkedin-carousel/assets"

W, H = 1080, 1350
FPS = 30
BG = (11, 15, 26)
ORANGE = (255, 154, 60)
TEAL = (58, 209, 200)
VIOLET = (155, 123, 255)
WHITE = (245, 246, 250)
MUTED = (150, 160, 185)
CONTENT_BOTTOM = 1140  # captions live below this line

# ---------------------------------------------------------------- fonts


def font(name, size):
    return ImageFont.truetype(str(ASSETS / name), size)


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


HEAD = lambda s: font("Outfit-Bold.ttf", s)  # noqa: E731
BODY = lambda s: font("WorkSans-Regular.ttf", s)  # noqa: E731

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


# ---------------------------------------------------------------- scenes
# Each scene: draw(frame, t, dur, speech, sc) where t is seconds into the scene,
# speech is the length of the spoken part, sc is the scene dict.

JOURNEY = Image.open(POST_DIR / "cogito-long-mem-reasoning-journey.jpg").convert("RGB")
BOARD = Image.open(POST_DIR / "cogito_ladder_board.png").convert("RGB")
END_BG = None


def top_shade(frame, height=520, strength=0.85):
    grad = Image.new("L", (1, height))
    for y in range(height):
        grad.putpixel((0, y), int(255 * strength * (1 - y / height) ** 1.3))
    mask = grad.resize((W, height))
    black = Image.new("RGBA", (W, height), (*BG, 255))
    black.putalpha(mask)
    frame.alpha_composite(black, (0, 0))


def bottom_shade(frame, height=420, strength=0.8):
    grad = Image.new("L", (1, height))
    for y in range(height):
        grad.putpixel((0, y), int(255 * strength * (y / height) ** 1.5))
    black = Image.new("RGBA", (W, height), (*BG, 255))
    black.putalpha(grad.resize((W, height)))
    frame.alpha_composite(black, (0, H - height))


def scene_journey(frame, t, dur, speech, sc):
    p = ease(t / dur)
    base = max(W / JOURNEY.width, H / JOURNEY.height)
    s = base * (1.0 + 0.12 * p)
    # focus drifts from the figure at the foot of the ladder upwards
    fy = JOURNEY.height * (0.62 - 0.17 * p)
    fx = JOURNEY.width * 0.5
    ox = W / 2 - fx * s
    oy = H * 0.5 - fy * s
    ox = min(0, max(W - JOURNEY.width * s, ox))
    oy = min(0, max(H - JOURNEY.height * s, oy))
    tmp = Image.new("RGB", (W, H), BG)
    blit_cam(tmp, JOURNEY, s, ox, oy)
    frame.paste(tmp)
    top_shade(frame, 560, 0.9)
    bottom_shade(frame)

    half = cue(sc["narration"], "I'm scaling", 0.25) * speech
    a1 = ease(seg(t, 0.15, 0.6))
    a2 = ease(seg(t, half, half + 0.5))

    def draw(d, _):
        f = HEAD(92)
        sk = dict(stroke_width=3, stroke_fill=alpha(BG, 0.6))
        text_c(d, (W / 2, 150 + 20 * (1 - a1)), "Big labs scale up.", f, alpha(WHITE, a1), **sk)
        text_c(d, (W / 2, 262 + 24 * (1 - a2)), "I'm scaling down.", f, alpha(ORANGE, a2), **sk)
        text_c(d, (W / 2, 360 + 16 * (1 - a2)), "tiny reasoning models · from scratch · a few GPUs",
               BODY(36), alpha(WHITE, a2), stroke_width=2, stroke_fill=alpha(BG, a2 * 0.8))
    overlay(frame, draw)


def scene_idea(frame, t, dur, speech, sc):
    n_tok, tok, gap = 40, 34, 10
    strip_y = 300
    slots_y = 620
    slot_w, slot_h = 140, 96
    slot_x = [W / 2 + (i - 1.5) * (slot_w + 34) for i in range(4)]
    important = [4, 13, 22, 31]  # tokens that get written to memory
    rng = random.Random(7)
    shades = [rng.uniform(0.25, 0.55) for _ in range(n_tok)]
    q_at = cue(sc["narration"], "then reason", 0.4) * speech
    flow = seg(t, 0.2, q_at)  # 0..1: strip scrolls, picks drop into slots
    qa = seg(t, q_at, q_at + 1.6)
    span = n_tok * (tok + gap)
    offset = W + 40 - flow * (span + W * 0.2)  # strip scrolls from right to left

    def draw(d, _):
        text_c(d, (W / 2, 130), "The idea", HEAD(64), WHITE)
        text_c(d, (W / 2, 200), "a long book of tokens …", BODY(34), MUTED)
        filled = 0
        for i in range(n_tok):
            x = offset + i * (tok + gap)
            pick = i in important
            # once a picked token passes the reading head (x < W/2) it drops into its slot
            dropped = pick and x < W / 2
            if pick and dropped:
                k = important.index(i)
                filled = max(filled, k + 1)
                drop = ease(clamp((W / 2 - x) / 260))
                sx = slot_x[k]
                px = W / 2 + (sx - W / 2) * drop
                py = strip_y + (slots_y - strip_y) * drop
                if drop < 1:
                    d.rounded_rectangle([px - tok / 2, py - tok / 2, px + tok / 2, py + tok / 2], 6,
                                        fill=alpha(ORANGE, 1))
                continue
            if -tok < x < W + tok:
                col = ORANGE if pick else mix(BG, (120, 140, 190), shades[i])
                d.rounded_rectangle([x - tok / 2, strip_y - tok / 2, x + tok / 2, strip_y + tok / 2], 6, fill=col)
        # reading head
        d.line([W / 2, strip_y - 46, W / 2, strip_y + 46], fill=alpha(TEAL, 0.8), width=3)
        text_c(d, (W / 2, slots_y - 120), "write what matters", BODY(32), alpha(ORANGE, 0.95))
        # memory slots
        for k, sx in enumerate(slot_x):
            on = k < filled
            box = [sx - slot_w / 2, slots_y - slot_h / 2, sx + slot_w / 2, slots_y + slot_h / 2]
            d.rounded_rectangle(box, 16, outline=TEAL, width=4, fill=alpha(TEAL, 0.28 if on else 0.06))
            if on:
                d.rounded_rectangle([sx - tok / 2, slots_y - tok / 2, sx + tok / 2, slots_y + tok / 2], 6,
                                    fill=ORANGE)
        text_c(d, (slot_x[-1] + slot_w / 2 + 14, slots_y), "memory", BODY(28), MUTED, anchor="lm")
        # question answered from the slots
        if qa > 0:
            qx, qy = W / 2, 930
            for k, sx in enumerate(slot_x):
                lk = ease(seg(qa, 0.1 + k * 0.08, 0.5 + k * 0.08))
                ex, ey = sx + (qx - sx) * lk, (slots_y + slot_h / 2) + (qy - 60 - slots_y - slot_h / 2) * lk
                d.line([sx, slots_y + slot_h / 2, ex, ey], fill=alpha(VIOLET, 0.9), width=4)
            a = ease(seg(qa, 0.0, 0.3))
            d.ellipse([qx - 56, qy - 56, qx + 56, qy + 56], fill=alpha(VIOLET, a * 0.9))
            ans = ease(seg(qa, 0.65, 0.9))
            if ans < 0.5:
                text_c(d, (qx, qy - 4), "?", HEAD(72), alpha(WHITE, a))
            else:
                check_mark(d, qx, qy, 52, alpha(WHITE, a), 9)
            text_c(d, (W / 2, 1060), "write what matters → reason over it", HEAD(46),
                   alpha(WHITE, ease(seg(qa, 0.3, 0.7))))
    overlay(frame, draw)


def scene_problem(frame, t, dur, speech, sc):
    zero_at = cue(sc["narration"], "scored zero", 0.25) * speech
    loss_at = cue(sc["narration"], "And the loss", 0.4) * speech
    ign_at = cue(sc["narration"], "ignored", 0.75) * speech
    cx0, cy0, cx1, cy1 = 150, 610, 960, 1000

    def draw(d, _):
        za = ease(seg(t, max(0.2, zero_at - 0.3), zero_at + 0.4))
        text_c(d, (W / 2, 120), "long-context benchmarks", BODY(42), alpha(WHITE, za))
        text_c(d, (W / 2, 310), "0", HEAD(300), alpha(ORANGE, za))
        text_c(d, (W / 2, 480), "night after night", BODY(32), alpha(MUTED, za))
        # loss chart
        la = ease(seg(t, loss_at - 0.4, loss_at + 0.2))
        d.line([cx0, cy0, cx0, cy1, cx1, cy1], fill=alpha(MUTED, la * 0.8), width=3)
        text_c(d, (cx0 - 20, cy0 - 30), "loss", BODY(28), alpha(MUTED, la), anchor="lm")
        text_c(d, (cx1, cy1 + 34), "training steps", BODY(26), alpha(MUTED, la), anchor="rm")
        prog = ease(seg(t, loss_at, loss_at + 2.0))
        pts = []
        steps = 120
        for i in range(int(steps * prog) + 1):
            u = i / steps
            v = 0.12 + 0.82 * math.exp(-4.2 * u) + 0.025 * math.sin(u * 37) * (1 - u * 0.5)
            pts.append((cx0 + 10 + u * (cx1 - cx0 - 20), cy1 - v * (cy1 - cy0)))
        if len(pts) > 1:
            d.line(pts, fill=TEAL, width=6, joint="curve")
        ha = ease(seg(prog, 0.6, 1.0))
        text_c(d, (cx1 - 60, cy0 + 70), "loss looks healthy", BODY(36), alpha(TEAL, ha), anchor="rm")
        check_mark(d, cx1 - 25, cy0 + 70, 30, alpha(TEAL, ha), 5)
        ia = ease(seg(t, ign_at - 0.2, ign_at + 0.4))
        text_c(d, (W / 2, 1085), "memory: ignored", HEAD(56), alpha(ORANGE, ia))
    overlay(frame, draw)


def scene_symbols(frame, t, dur, speech, sc):
    n = sc["narration"]
    type_at = cue(n, "a key", 0.45) * speech
    fill_at = cue(n, "thousands", 0.6) * speech - 0.3
    # the question follows the filler bar, so the answer has time to land before the scene ends
    q_at = min(cue(n, "one question", 0.85) * speech, fill_at + 1.3)
    f = mono(52)
    lines = ["key alice val red .", "key bob   val blue ."]
    total = sum(len(s) for s in lines)
    typed = int(total * seg(t, type_at - 0.3, fill_at - 0.1))
    px0 = 120
    char_w = f.getlength("M")

    def draw(d, _):
        text_c(d, (W / 2, 120), "Step 1: no language", HEAD(64), WHITE)
        text_c(d, (W / 2, 190), "random symbols, almost like DNA", BODY(34), MUTED)
        d.rounded_rectangle([80, 270, W - 80, 1070], 24, fill=(18, 24, 40, 255), outline=(40, 50, 75, 255), width=2)
        left = typed
        for li, s in enumerate(lines):
            shown = s[:max(0, min(len(s), left))]
            left -= len(s)
            y = 350 + li * 80
            # the stored value 'red' turns orange once the answer appears
            if li == 0 and len(shown) == len(s) and t > q_at + 0.5:
                i0 = s.index("red")
                text_c(d, (px0, y), s[:i0], f, WHITE, anchor="lm")
                text_c(d, (px0 + char_w * i0, y), "red", f, ORANGE, anchor="lm")
                text_c(d, (px0 + char_w * (i0 + 3), y), s[i0 + 3:], f, WHITE, anchor="lm")
            else:
                text_c(d, (px0, y), shown, f, WHITE, anchor="lm")
            if 0 <= len(shown) < len(s) and int(t * 3) % 2 == 0 and typed > 0 and left < 0:
                d.rectangle([px0 + char_w * len(shown) + 2, y - 26, px0 + char_w * len(shown) + 6, y + 26],
                            fill=TEAL)
        # filler bar
        fp = ease_out(seg(t, fill_at, fill_at + 1.6))
        if t > fill_at - 0.2:
            bx0, bx1, by = 140, W - 140, 600
            d.rounded_rectangle([bx0, by - 30, bx1, by + 30], 14, outline=(60, 72, 104, 255), width=2)
            rng = random.Random(3)
            cells = 64
            cw = (bx1 - bx0 - 12) / cells
            for i in range(int(cells * fp)):
                c = mix((40, 52, 82), (90, 110, 150), rng.random())
                d.rectangle([bx0 + 6 + i * cw + 1, by - 22, bx0 + 6 + (i + 1) * cw - 1, by + 22], fill=c)
            count = int(round(4000 * fp / 50.0)) * 50
            text_c(d, (W / 2, by + 80), f"+{count:,} tokens of filler", mono(42), alpha(VIOLET, 1))
        # question + answer
        qa = ease(seg(t, q_at - 0.1, q_at + 0.4))
        if qa > 0:
            y = 840
            text_c(d, (px0, y), "Q alice →", f, alpha(WHITE, qa), anchor="lm")
            aa = ease(seg(t, q_at + 0.35, q_at + 0.7))
            text_c(d, (px0 + char_w * 10, y), "red", f, alpha(ORANGE, aa), anchor="lm")
            text_c(d, (W / 2, 970), "one fact, far back, one exact answer", BODY(34), alpha(MUTED, aa))
    overlay(frame, draw)


RUNGS = [
    ("Find", "find where someone lives"),
    ("Pick", "pick among look-alikes"),
    ("Track", "track where they live now"),
    ("Follow", "follow 2–3 hops"),
    ("Count", "count, deduce"),
]


def scene_ladder(frame, t, dur, speech, sc):
    n = sc["narration"]
    times = [cue(n, key, 0.2 + 0.15 * i) * speech - 0.25 for i, (key, _) in enumerate(RUNGS)]
    rx0, rx1 = 150, W - 150
    y_bottom, y_top = 1010, 330
    gap = (y_bottom - y_top) / (len(RUNGS) - 1)
    cols = [TEAL, mix(TEAL, VIOLET, 0.5), VIOLET, mix(VIOLET, ORANGE, 0.5), ORANGE]

    def draw(d, _):
        text_c(d, (W / 2, 120), "Step 2: children's stories", HEAD(64), WHITE)
        text_c(d, (W / 2, 190), "with planted facts, questions that slowly get harder", BODY(32), MUTED)
        d.line([rx0, y_top - 70, rx0, y_bottom + 60], fill=(60, 72, 104, 255), width=6)
        d.line([rx1, y_top - 70, rx1, y_bottom + 60], fill=(60, 72, 104, 255), width=6)
        for i, (_, label) in enumerate(RUNGS):
            y = y_bottom - i * gap
            on = ease(seg(t, times[i] - 0.1, times[i] + 0.35))
            c = cols[i]
            box = [rx0 - 10, y - 46, rx1 + 10, y + 46]
            d.rounded_rectangle(box, 18, fill=alpha(c, 0.08 + 0.32 * on), outline=alpha(c, 0.35 + 0.65 * on),
                                width=3)
            text_c(d, (rx0 + 30, y), f"{i + 1}", HEAD(44), alpha(c, 0.35 + 0.65 * on), anchor="lm")
            text_c(d, (rx0 + 90, y), label, BODY(42), alpha(WHITE, 0.3 + 0.7 * on), anchor="lm")
    overlay(frame, draw)


def scene_board(frame, t, dur, speech, sc):
    p = ease(seg(t, 0.4, max(1.5, speech * 0.5)))
    # start: 1.4x zoom (relative to full-width fit) centred on the C0–C7 table
    s0 = 1.4 * W / BOARD.width
    fx, fy = 771, 900  # level names + first model columns of the table, in board pixels
    ox0, oy0 = W / 2 - fx * s0, 600 - fy * s0
    ox0 = min(0, max(W - BOARD.width * s0, ox0))
    oy0 = min(0, oy0)
    # end: whole board fitted above the caption band
    s1 = (CONTENT_BOTTOM - 16) / BOARD.height
    ox1, oy1 = (W - BOARD.width * s1) / 2, 12
    s = s0 + (s1 - s0) * p
    ox = ox0 + (ox1 - ox0) * p
    oy = oy0 + (oy1 - oy0) * p
    blit_cam(frame, BOARD, s, ox, oy)


def scene_end(frame, t, dur, speech, sc):
    global END_BG
    if END_BG is None:
        bg = Image.new("RGB", (W, H), BG)
        s = max(W / JOURNEY.width, H / JOURNEY.height) * 1.12
        blit_cam(bg, JOURNEY, s, W / 2 - JOURNEY.width * 0.5 * s, H / 2 - JOURNEY.height * 0.45 * s)
        bg = bg.filter(ImageFilter.GaussianBlur(14))
        END_BG = Image.blend(Image.new("RGB", (W, H), BG), bg, 0.28).convert("RGBA")
    frame.alpha_composite(END_BG)

    def a(i):
        return ease(seg(t, 0.2 + i * 0.45, 0.7 + i * 0.45))

    def draw(d, _):
        text_c(d, (W / 2, 250), "Cogito Capability", HEAD(96), alpha(WHITE, a(0)))
        text_c(d, (W / 2, 360), "Checks", HEAD(96), alpha(ORANGE, a(0)))
        text_c(d, (W / 2, 480), "Open datasets on Hugging Face", BODY(44), alpha(WHITE, a(1)))
        for j, line in enumerate(["5 datasets", "1K–128K tokens", "a known answer for every question"]):
            y = 600 + j * 64
            text_c(d, (W / 2, y), line, BODY(38), alpha(TEAL if j < 2 else WHITE, a(2 + j * 0.5)))
        text_c(d, (W / 2, 880), "huggingface.co/collections/ksopyla", mono(38), alpha(VIOLET, a(4)))
        text_c(d, (W / 2, 950), "ai.ksopyla.com", mono(38), alpha(VIOLET, a(4.5)))
    overlay(frame, draw)


def make_cover():
    """Title card: the first frame of the video and a custom thumbnail (cover.jpg)."""
    frame = Image.new("RGBA", (W, H), (*BG, 255))
    s = max(W / JOURNEY.width, H / JOURNEY.height)
    tmp = Image.new("RGB", (W, H), BG)
    blit_cam(tmp, JOURNEY, s, W / 2 - JOURNEY.width * 0.5 * s,
             min(0, max(H - JOURNEY.height * s, H * 0.5 - JOURNEY.height * 0.62 * s)))
    frame.paste(tmp)
    top_shade(frame, 640, 0.92)
    bottom_shade(frame, 300, 0.85)

    def draw(d, _):
        sk = dict(stroke_width=3, stroke_fill=alpha(BG, 0.6))
        text_c(d, (W / 2, 95), "MRCOGITO · OPEN DATASETS", mono(30), TEAL)
        text_c(d, (W / 2, 205), "Cogito Capability", HEAD(100), WHITE, **sk)
        text_c(d, (W / 2, 315), "Checks", HEAD(100), ORANGE, **sk)
        text_c(d, (W / 2, 420), "a ladder of simple tests for tiny models", BODY(40), WHITE,
               stroke_width=2, stroke_fill=alpha(BG, 0.8))
        text_c(d, (W / 2, 1290), "ai.ksopyla.com", mono(32), alpha(WHITE, 0.85))
    overlay(frame, draw)
    return frame.convert("RGB")


SCENES = {"journey": scene_journey, "idea": scene_idea, "problem": scene_problem, "symbols": scene_symbols,
          "ladder": scene_ladder, "board": scene_board, "end": scene_end}

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


CAP_FONT = None


def draw_caption(frame, t, speech, chunks):
    global CAP_FONT
    CAP_FONT = CAP_FONT or BODY(44)
    lead = 0.1
    u = (t - lead) / max(speech, 0.1)
    cur = None
    for a, b, lines in chunks:
        if a <= u < b:
            cur = lines
    if cur is None:
        cur = chunks[-1][2] if u >= 1 else chunks[0][2]

    def draw(d, _):
        lh = 58
        widths = [d.textlength(s, font=CAP_FONT) for s in cur]
        bw = max(widths) + 70
        bh = lh * len(cur) + 36
        cy = 1240
        d.rounded_rectangle([W / 2 - bw / 2, cy - bh / 2, W / 2 + bw / 2, cy + bh / 2], 20, fill=(0, 0, 0, 165))
        for i, s in enumerate(cur):
            y = cy - (len(cur) - 1) * lh / 2 + i * lh
            text_c(d, (W / 2, y), s, CAP_FONT, WHITE)
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


def prepare_audio(scenes, regen):
    key, voice = load_key()
    if not key and not os.environ.get("HTTPS_PROXY"):
        sys.exit("No ELEVENLABS_API_KEY in the environment or .env. Add it, or run with --silent.")
    if not key:
        print("No ELEVENLABS_API_KEY; trying the HTTPS proxy's credential injection.")
    AUDIO_DIR.mkdir(exist_ok=True)
    manifest_path = AUDIO_DIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for sc in scenes:
        mp3 = AUDIO_DIR / f"{sc['id']}.mp3"
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


# ---------------------------------------------------------------- render


def render(scenes, out_video):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out_video)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    cover = make_cover()
    cover.save(COVER, quality=92)
    for _ in range(int(round(COVER_DUR * FPS))):
        proc.stdin.write(cover.tobytes())
    fade_from = cover  # the first scene cross-fades from the title card, later ones from black
    for sc in scenes:
        fn = SCENES[sc["visual"]]
        chunks = caption_chunks(sc["narration"])
        n = int(round(sc["dur"] * FPS))
        print(f"{sc['id']}: {sc['dur']:.2f}s, {n} frames", flush=True)
        for i in range(n):
            t = i / FPS
            frame = Image.new("RGBA", (W, H), (*BG, 255))
            fn(frame, t, sc["dur"], sc["speech"], sc)
            draw_caption(frame, t, sc["speech"], chunks)
            fade = ease(t / 0.3)
            rgb = frame.convert("RGB")
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--silent", action="store_true", help="no voiceover; timing from word count")
    ap.add_argument("--regen", action="store_true", help="re-generate all TTS clips")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    spec = json.loads((HERE / "scenes.json").read_text())
    assert spec["size"] == [W, H] and spec["fps"] == FPS, "scenes.json size/fps differ from the renderer"
    scenes = spec["scenes"]
    if args.silent:
        for sc in scenes:
            sc["speech"] = len(sc["narration"].split()) / 2.6
            sc["dur"] = sc["speech"] + 0.6
    else:
        prepare_audio(scenes, args.regen)

    if args.silent:
        render(scenes, args.out)
    else:
        tmp = args.out.with_suffix(".video.mp4")
        render(scenes, tmp)
        mux(scenes, tmp, args.out)
        tmp.unlink()
    total = COVER_DUR + sum(sc["dur"] for sc in scenes)
    print(f"wrote {args.out} ({total:.1f}s, {args.out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
