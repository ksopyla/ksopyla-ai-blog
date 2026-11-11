"""Explainer video (1080x1350, 4:5; --shorts for 9:16) for the post "Claude forgets. I measured how much,
and built a simple memory to bring it back".

Narration lives in scenes.json; the engine (captions, voiceover, encoding) in the explainer-video skill;
Cogi the squirrel comes from branding/cogi/cogi_art.py.
From the repo root:
    uv run --with Pillow content/linkedin/2026-11-cogi-memory-claude-forgets/video/make_video.py --stills
    uv run --with Pillow content/linkedin/2026-11-cogi-memory-claude-forgets/video/make_video.py
    uv run --with Pillow content/linkedin/2026-11-cogi-memory-claude-forgets/video/make_video.py --shorts
"""

import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / ".git").exists())
sys.path.insert(0, str(ROOT / ".cursor/skills/explainer-video/scripts"))
sys.path.insert(0, str(ROOT / "branding/cogi"))

import video_kit as vk  # noqa: E402
from cogi_art import cogi  # noqa: E402
from video_kit import (BG, BODY, HEAD, LINE, MUTED, ORANGE, PANEL, TEAL, VIOLET, WHITE, H, W,  # noqa: E402
                       alpha, bottom_shade, check_mark, cover_fit, cue, ease, ease_out, mix, mono, overlay, seg,
                       text_c, top_shade)

FEATURE = Image.open(ROOT / "content/posts/cogi-memory-evals/feature_cogi_memory.jpg").convert("RGB")
PAPER = (255, 251, 244)  # Cogi's cream
INK = (43, 32, 23)


def fit(d, text, font_fn, size, max_w):
    """Largest font size <= size that keeps text within max_w."""
    while size > 20 and d.textlength(text, font=font_fn(size)) > max_w:
        size -= 2
    return font_fn(size)


def paste_cogi(frame, cx, cy, size, a=1.0):
    """Cogi centred on (cx, cy), faded by a."""
    if a <= 0:
        return
    img = cogi(size)
    if a < 1:
        img = img.copy()
        img.putalpha(img.getchannel("A").point(lambda v: int(v * a)))
    frame.alpha_composite(img, (int(cx - size / 2), int(cy - size / 2)))


def heading(d, t, title, sub=None, col=WHITE, y=150):
    a = ease(seg(t, 0.05, 0.45))
    text_c(d, (W / 2, y + 12 * (1 - a)), title, fit(d, title, HEAD, 68, W - 120), alpha(col, a))
    if sub:
        text_c(d, (W / 2, y + 70), sub, fit(d, sub, BODY, 36, W - 140), alpha(MUTED, a))


def text_lines(d, x0, y0, w, n, col, a, gap=16, seed=0):
    """A few grey 'text' bars standing in for a message."""
    rng = random.Random(seed)
    for k in range(n):
        lw = w * (rng.uniform(0.55, 0.95) if k == n - 1 else rng.uniform(0.85, 1.0))
        d.rounded_rectangle([x0, y0 + k * gap, x0 + lw, y0 + k * gap + 7], 4, fill=alpha(col, a))


def pill(d, cx, cy, text, f, fg, bg, a, outline=None):
    if a <= 0:
        return
    w = d.textlength(text, font=f) + 56
    h = f.size + 30
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], h / 2, fill=alpha(bg, a),
                        outline=alpha(outline or bg, a), width=3)
    text_c(d, (cx, cy), text, f, alpha(fg, a))

# ---------------------------------------------------------------- scenes


EARLY = "Keep the same parameter count."


def scene_forget(frame, t, dur, speech, sc):
    n = sc["narration"]
    start = cue(n, "at the start", 0.6) * speech
    measured = cue(n, "So I measured", 0.75) * speech
    # a long session scrolls up; the early messages, my requirement among them, leave Claude's view
    scroll = 430 * ease(seg(t, max(1.2, start - 0.3), max(2.4, start + 1.2)))

    def draw(d, _):
        heading(d, t, "In a long Claude Code session", None, WHITE, y=130)
        top, bottom = 300, 930
        y = 330 - scroll
        for k in range(14):
            mine = k % 2 == 0
            h = 96 if k else 110
            x0, x1 = (110, 760) if mine else (320, 970)
            if y + h > top and y + h < bottom:
                # fade out as the message leaves the window at the top
                fade = ease(seg(y, top - 40, top + 80))
                col = TEAL if mine else VIOLET
                if k == 0:
                    col = ORANGE
                if fade > 0:
                    d.rounded_rectangle([x0, y, x1, y + h], 22, fill=alpha(PANEL, fade),
                                        outline=alpha(col, 0.9 * fade), width=3)
                    if k == 0:
                        text_c(d, (x0 + 32, y + h / 2 - 4), EARLY, BODY(38), alpha(WHITE, fade), anchor="lm")
                        text_c(d, (x1 + 20, y + h / 2), "me, at the start", BODY(28), alpha(ORANGE, fade), anchor="lm")
                    else:
                        text_lines(d, x0 + 30, y + 28, x1 - x0 - 60, 3, MUTED, 0.7 * fade, gap=20, seed=k)
            y += h + 26
        # the window edge: above this line Claude no longer sees the words
        d.line([80, top, W - 80, top], fill=alpha(LINE, 1), width=3)
        text_c(d, (W - 90, top - 26), "what Claude still sees ↓", BODY(28), alpha(MUTED, ease(seg(t, 0.3, 0.8))),
               anchor="rm")
        am = ease(seg(t, measured - 0.1, measured + 0.4))
        text_c(d, (W / 2, 1010), "How much survives?", HEAD(56), alpha(ORANGE, am))
    overlay(frame, draw)


STAGES = [("start", 72), ("first summary", 50), ("middle", 11), ("end", 7)]


def scene_decay(frame, t, dur, speech, sc):
    n = sc["narration"]
    s1 = cue(n, "replaces it", 0.3) * speech
    s2 = cue(n, "then summarises", 0.5) * speech
    s3 = cue(n, "only one in ten", 0.85) * speech
    times = [0.0, s1 + 0.3, s2 + 0.4, s3]
    order = list(range(72))
    random.Random(11).shuffle(order)
    rank = {i: r for r, i in enumerate(order)}

    def lit(i):
        """1 while fact i is still fully there, fading out at the stage that drops it."""
        v = 1.0
        for (_, keep), ts in zip(STAGES[1:], times[1:]):
            if rank[i] >= keep:
                v = min(v, 1 - ease(seg(t, ts, ts + 0.6)))
        return v

    def draw(d, _):
        heading(d, t, "72 early facts from my sessions", "requirements, rejected ideas, results", WHITE, y=120)
        cols, rows, step = 12, 6, 62
        gx, gy = W / 2 - (cols - 1) * step / 2, 330
        a = ease(seg(t, 0.2, 0.7))
        for i in range(72):
            r, c = divmod(i, cols)
            x, y = gx + c * step, gy + r * step
            v = lit(i)
            col = mix(LINE, ORANGE, v)
            d.ellipse([x - 20, y - 20, x + 20, y + 20], fill=alpha(col, a))
        # the session squeezed into a summary
        bw = 860 - 800 * ease(seg(t, s1, s1 + 0.9))
        by = 760
        d.rounded_rectangle([W / 2 - bw / 2, by - 34, W / 2 + bw / 2, by + 34], 16, fill=alpha(PANEL, a),
                            outline=alpha(VIOLET, a), width=3)
        lab = "the session: 782,000 tokens" if t < s1 + 0.4 else "summary: 13,000 tokens"
        text_c(d, (W / 2, by + 70), lab, BODY(34), alpha(VIOLET, a))
        # stage chips with the share of facts still fully there
        xs = [190, 420, 660, 890]
        for k, ((name, keep), ts) in enumerate(zip(STAGES, times)):
            ak = ease(seg(t, ts, ts + 0.4)) if k else a
            on = k == max(j for j, tj in enumerate(times) if t >= tj)
            col = ORANGE if on else MUTED
            text_c(d, (xs[k], 900), f"{round(100 * keep / 72)}%", HEAD(58), alpha(col, ak))
            text_c(d, (xs[k], 955), name, BODY(30), alpha(col, ak))
        ae = ease(seg(t, s3 + 0.2, s3 + 0.7))
        text_c(d, (W / 2, 1025), "fully there at the end: 1 in 10", BODY(36), alpha(WHITE, ae))
    overlay(frame, draw)


def scene_cogi(frame, t, dur, speech, sc):
    n = sc["narration"]
    plain = cue(n, "plain search", 0.2) * speech
    word = cue(n, "word for word", 0.6) * speech
    laptop = cue(n, "on my laptop", 0.7) * speech
    noai = cue(n, "no AI call", 0.85) * speech
    a0 = ease(seg(t, 0.1, 0.6))
    paste_cogi(frame, 270, 640 + 20 * (1 - a0), 400, a0)

    def draw(d, _):
        text_c(d, (W / 2, 140 + 12 * (1 - a0)), "So I built Cogi", HEAD(76), alpha(ORANGE, a0))
        ap = ease(seg(t, plain - 0.1, plain + 0.4))
        text_c(d, (W / 2, 220), "plain search, not a new kind of memory", BODY(38), alpha(WHITE, ap))
        # the memory: every message filed with its date, word for word
        bx0, by0, bx1, by1 = 520, 330, 990, 860
        d.rounded_rectangle([bx0, by0, bx1, by1], 28, fill=alpha(PANEL, a0), outline=alpha(LINE, a0), width=3)
        text_c(d, ((bx0 + bx1) / 2, by0 + 40), "every message, word for word", BODY(30), alpha(MUTED, a0))
        start = max(0.5, plain - 0.3)
        for k in range(7):
            s = start + k * 0.45
            if t < s:
                continue
            p = ease_out(seg(t, s, s + 0.6))
            ty = by0 + 90 + k * 66
            x = bx0 + 24 + (W + 40 - (bx0 + 24)) * (1 - p)
            d.rounded_rectangle([x, ty, x + 420, ty + 52], 12, fill=alpha(mix(PANEL, WHITE, 0.08), 1),
                                outline=alpha(TEAL if k % 2 == 0 else VIOLET, 0.9), width=2)
            text_c(d, (x + 20, ty + 26), f"11 Nov {9 + k // 2:02d}:{(k * 17) % 60:02d}", mono(22), alpha(MUTED, 1),
                   anchor="lm")
            text_lines(d, x + 190, ty + 16, 205, 2, MUTED, 0.75, gap=14, seed=20 + k)
        f = BODY(34)
        pill(d, 300, 935, "word for word", f, WHITE, PANEL, ease(seg(t, word - 0.1, word + 0.3)), outline=TEAL)
        pill(d, 700, 935, "on my laptop", f, WHITE, PANEL, ease(seg(t, laptop - 0.1, laptop + 0.3)), outline=TEAL)
        pill(d, W / 2, 1020, "no AI call to save", HEAD(36), BG, ORANGE, ease(seg(t, noai - 0.1, noai + 0.3)))
    overlay(frame, draw)


QUESTION = "What did I say about the parameter count?"


def scene_page(frame, t, dur, speech, sc):
    n = sc["narration"]
    page = cue(n, "one page", 0.3) * speech
    own = cue(n, "my own words", 0.4) * speech
    ans = cue(n, "fully answered", 0.75) * speech
    aq = ease(seg(t, 0.1, 0.5))
    ap = ease(seg(t, page - 0.2, page + 0.5))
    ar = ease(seg(t, ans - 0.1, ans + 0.6))
    paste_cogi(frame, 165, 360, 200, aq)

    def draw(d, _):
        # Claude asks
        f = fit(d, QUESTION, BODY, 38, 700)
        w = d.textlength(QUESTION, font=f) + 60
        d.rounded_rectangle([W / 2 + 40 - w / 2, 110, W / 2 + 40 + w / 2, 190], 26, fill=alpha(TEAL, aq))
        text_c(d, (W / 2 + 40, 150), QUESTION, f, alpha(BG, aq))
        text_c(d, (W / 2 + 40, 225), "Claude searches the memory", BODY(30), alpha(MUTED, aq))
        # one page comes back: my own words, with dates
        if ap > 0:
            px0, py0, px1, py1 = 300, 290 + 30 * (1 - ap), 930, 840 + 30 * (1 - ap)
            d.rounded_rectangle([px0, py0, px1, py1], 18, fill=alpha(PAPER, ap))
            text_c(d, (px0 + 36, py0 + 44), "one page · about 750 words", mono(26), alpha(INK, 0.6 * ap), anchor="lm")
            rows = [("14 Oct 21:07", None), ("14 Oct 21:09", "“Keep the same parameter count.”"),
                    ("14 Oct 21:12", None), ("16 Oct 19:40", None), ("16 Oct 19:44", None)]
            for k, (stamp, said) in enumerate(rows):
                y = py0 + 110 + k * 92
                text_c(d, (px0 + 36, y), stamp, mono(24), alpha(INK, 0.55 * ap), anchor="lm")
                if said:
                    ah = ease(seg(t, own - 0.1, own + 0.4))
                    if ah > 0:
                        d.rounded_rectangle([px0 + 24, y + 18, px1 - 24, y + 74], 10,
                                            fill=alpha(mix(PAPER, ORANGE, 0.45 * ah), ap))
                    text_c(d, (px0 + 36, y + 46), said, BODY(32), alpha(INK, ap), anchor="lm")
                else:
                    text_lines(d, px0 + 36, y + 30, px1 - px0 - 72, 2, (150, 135, 120), 0.8 * ap, gap=18, seed=40 + k)
        # how often that page was enough, on my own sessions
        if ar > 0:
            cx, cy, r = 190, 930, 84
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=alpha(LINE, ar), width=16)
            d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * 0.79 * ar, fill=alpha(ORANGE, 1), width=16)
            text_c(d, (cx, cy), "79%", HEAD(50), alpha(WHITE, ar))
            text_c(d, (330, 905), "fully answered", HEAD(46), alpha(WHITE, ar), anchor="lm")
            text_c(d, (330, 962), "88% at least partly · 24 questions", BODY(32), alpha(MUTED, ar), anchor="lm")
    overlay(frame, draw)


def scene_needle(frame, t, dur, speech, sc):
    n = sc["narration"]
    top5 = cue(n, "top five", 0.6) * speech
    pct = cue(n, "ninety-three", 0.8) * speech
    cols, rows = 24, 20
    gx0, gy0, cw, ch = 132, 300, 34, 24
    rng = random.Random(7)
    picks = rng.sample(range(cols * rows), 5)
    right = picks[2]

    def draw(d, _):
        heading(d, t, "Over a million tokens of history", "about 480 past chats per question", WHITE, y=130)
        a = ease(seg(t, 0.2, 0.7))
        scan = (t - 0.6) / max(0.8, top5 - 0.6)
        ah = ease(seg(t, top5 - 0.1, top5 + 0.4))
        for i in range(cols * rows):
            r, c = divmod(i, cols)
            x, y = gx0 + c * cw, gy0 + r * ch
            # a scan line sweeps the grid until the top five light up
            glow = max(0.0, 1 - abs(r / rows - scan) * 6) if 0 < scan < 1 and ah == 0 else 0
            col = mix(PANEL, VIOLET, 0.35 + 0.5 * glow)
            if i in picks:
                col = mix(col, TEAL if i == right else ORANGE, ah)
            d.rounded_rectangle([x, y, x + cw - 6, y + ch - 6], 4, fill=alpha(col, a))
        if ah > 0:
            r, c = divmod(right, cols)
            x, y = gx0 + c * cw + (cw - 6) / 2, gy0 + r * ch + (ch - 6) / 2
            d.ellipse([x - 40, y - 40, x + 40, y + 40], outline=alpha(TEAL, ah), width=5)
            text_c(d, (W / 2, 820), "top five results", BODY(34), alpha(ORANGE, ah))
        ap = ease(seg(t, pct - 0.1, pct + 0.5))
        if ap > 0:
            text_c(d, (W / 2, 910), "93%", HEAD(110), alpha(TEAL, ap))
            text_c(d, (W / 2, 1010), "4 other free memory plugins: 86.6–89.8%", BODY(32), alpha(MUTED, ap))
    overlay(frame, draw)


def scene_reread(frame, t, dur, speech, sc):
    n = sc["narration"]
    whole = cue(n, "rereading", 0.4) * speech
    less = cue(n, "nine times less", 0.8) * speech
    ap = ease(seg(t, 0.1, 0.6))
    aw = ease(seg(t, whole - 0.2, whole + 0.5))
    al = ease(seg(t, less - 0.1, less + 0.4))
    paste_cogi(frame, 330, 700, 150, ap)

    def bar(d, y, w, col, a, label, score, sub):
        text_c(d, (110, y - 70), label, HEAD(46), alpha(WHITE, a), anchor="lm")
        text_c(d, (W - 110, y - 70), score, HEAD(56), alpha(col, a), anchor="rm")
        d.rounded_rectangle([110, y - 30, 110 + w, y + 30], 14, fill=alpha(PANEL, a), outline=alpha(col, a), width=3)
        # text texture inside the bar
        for k in range(int(w // 22)):
            x = 126 + k * 22
            d.line([x, y - 12, x + 12, y - 12], fill=alpha(col, 0.45 * a), width=4)
            d.line([x, y + 8, x + 8, y + 8], fill=alpha(col, 0.35 * a), width=4)
        text_c(d, (110, y + 62), sub, BODY(30), alpha(MUTED, a), anchor="lm")

    def draw(d, _):
        heading(d, t, "Is one page enough?", "same questions, same answering model", WHITE, y=130)
        bar(d, 420, 860 * aw, VIOLET, aw, "Whole conversation", "94.1%", "rereading everything")
        bar(d, 690, 96 * ap, ORANGE, ap, "One page from Cogi", "89.4%", "")
        text_c(d, (W / 2, 880), "95% of the quality", HEAD(64), alpha(WHITE, al))
        text_c(d, (W / 2, 960), "from about 9× less text", BODY(40), alpha(ORANGE, al))
    overlay(frame, draw)


END_BG = None


def scene_end(frame, t, dur, speech, sc):
    global END_BG
    if END_BG is None:
        bg = cover_fit(FEATURE, zoom=1.05, fx=0.32).filter(ImageFilter.GaussianBlur(14))
        END_BG = Image.blend(Image.new("RGB", (W, H), BG), bg, 0.32).convert("RGBA")
    frame.alpha_composite(END_BG)

    n = sc["narration"]
    purpose = cue(n, "searches on purpose", 0.2) * speech
    read = cue(n, "The full story", 0.5) * speech

    def a(i):
        return ease(seg(t, 0.2 + i * 0.4, 0.7 + i * 0.4))

    ac = a(1)
    paste_cogi(frame, W / 2, 470, 230, ac)

    def draw(d, _):
        text_c(d, (W / 2, 190), "Claude forgets.", HEAD(96), alpha(WHITE, a(0)))
        text_c(d, (W / 2, 285), "Cogi brings it back.", HEAD(70), alpha(ORANGE, a(0)))
        apu = ease(seg(t, purpose - 0.2, purpose + 0.4))
        pill(d, W / 2, 640, "Ask Claude to check its memory", BODY(36), WHITE, PANEL, apu, outline=TEAL)
        ar = ease(seg(t, read - 0.2, read + 0.4))
        text_c(d, (W / 2, 770 + 16 * (1 - ar)), "Read the full story", HEAD(68), alpha(WHITE, ar))
        sub = "every test, the numbers and their limits"
        text_c(d, (W / 2, 850), sub, fit(d, sub, BODY, 36, W - 140), alpha(MUTED, ar))
        au = ease(seg(t, read + 0.3, read + 0.8))
        if au > 0:
            url, fu = "ai.ksopyla.com", mono(54)
            uw = d.textlength(url, font=fu)
            d.rounded_rectangle([W / 2 - uw / 2 - 44, 920, W / 2 + uw / 2 + 44, 1012], 46,
                                fill=alpha(ORANGE, au), outline=alpha(ORANGE, au), width=3)
            text_c(d, (W / 2, 966), url, fu, alpha(BG, au))
    overlay(frame, draw)


def make_cover():
    """Title card: the first frame of the video and the custom thumbnail (cover.jpg)."""
    frame = Image.new("RGBA", (W, H), (*BG, 255))
    frame.paste(cover_fit(FEATURE, zoom=1.0, fx=0.3, fy=0.5))
    top_shade(frame, 760, 0.95)
    bottom_shade(frame, 300, 0.85)

    def draw(d, _):
        sk = dict(stroke_width=3, stroke_fill=alpha(BG, 0.6))
        text_c(d, (W / 2, 95), "LAB NOTES · CLAUDE CODE MEMORY", mono(30), TEAL)
        text_c(d, (W / 2, 215), "Claude forgets.", HEAD(118), WHITE, **sk)
        text_c(d, (W / 2, 330), "I measured how much", fit(d, "I measured how much", HEAD, 80, W - 120), ORANGE, **sk)
        text_c(d, (W / 2, 430), "and built a simple memory to bring it back", BODY(40), WHITE, stroke_width=2,
               stroke_fill=alpha(BG, 0.8))
        text_c(d, (W / 2, 1290), "ai.ksopyla.com", mono(32), alpha(WHITE, 0.85))
    overlay(frame, draw)
    return frame.convert("RGB")


SCENES = {"forget": scene_forget, "decay": scene_decay, "cogi": scene_cogi, "page": scene_page,
          "needle": scene_needle, "reread": scene_reread, "end": scene_end}

if __name__ == "__main__":
    vk.run(HERE, SCENES, make_cover, "cogi-memory-claude-forgets.mp4")
