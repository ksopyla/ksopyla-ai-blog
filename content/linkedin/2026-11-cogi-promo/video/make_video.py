"""Promo video for Cogi (cogito-mem), in Cogi's own branding: cream page, ink text, orange accent, the squirrel.
1080x1350 (4:5); --shorts writes the 9:16 YouTube Short. The story is Cogi's "acorn" demo from its README.

Narration lives in scenes.json; the engine in the explainer-video skill; the squirrel in branding/cogi/cogi_art.py.
From the repo root:
    uv run --with Pillow content/linkedin/2026-11-cogi-promo/video/make_video.py --stills
    uv run --with Pillow content/linkedin/2026-11-cogi-promo/video/make_video.py --shorts
"""

import random
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / ".git").exists())
sys.path.insert(0, str(ROOT / ".cursor/skills/explainer-video/scripts"))
sys.path.insert(0, str(ROOT / "branding/cogi"))

import video_kit as vk  # noqa: E402
from cogi_art import ACORN, ACORN_CAP, CREAM, INK, cogi  # noqa: E402
from video_kit import (BODY, HEAD, H, W, alpha, check_mark, cue, ease, ease_out, mix, mono, overlay,  # noqa: E402
                       seg, text_c)

# Cogi's page instead of the blog's night palette: the kit reads BG when it builds frames and the Shorts background
vk.BG = CREAM
INK2 = (88, 74, 61)
ACCENT = (200, 98, 26)
BARK = (139, 97, 66)
HOLLOW = (58, 38, 23)
LEAF = (46, 122, 74)
TERM = (36, 28, 22)
TERM_INK = (246, 231, 207)
TERM_DIM = (170, 150, 128)
TILE = (233, 222, 205)


def fit(d, text, font_fn, size, max_w):
    while size > 20 and d.textlength(text, font=font_fn(size)) > max_w:
        size -= 2
    return font_fn(size)


def paste_cogi(frame, cx, cy, size, a=1.0):
    if a <= 0:
        return
    img = cogi(size)
    if a < 1:
        img = img.copy()
        img.putalpha(img.getchannel("A").point(lambda v: int(v * a)))
    frame.alpha_composite(img, (int(cx - size / 2), int(cy - size / 2)))


def acorn(d, cx, cy, s, a=1.0):
    """A small acorn: Cogi's picture of one saved message."""
    if a <= 0:
        return
    d.ellipse([cx - 0.36 * s, cy - 0.28 * s, cx + 0.36 * s, cy + 0.5 * s], fill=alpha(ACORN, a))
    d.chord([cx - 0.46 * s, cy - 0.5 * s, cx + 0.46 * s, cy + 0.06 * s], 180, 360, fill=alpha(ACORN_CAP, a))
    d.rectangle([cx - 0.05 * s, cy - 0.62 * s, cx + 0.05 * s, cy - 0.44 * s], fill=alpha(ACORN_CAP, a))


def pill(d, cx, cy, text, f, fg, bg, a, outline=None):
    if a <= 0:
        return
    w = d.textlength(text, font=f) + 56
    h = f.size + 30
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], h / 2, fill=alpha(bg, a),
                        outline=alpha(outline or bg, a), width=3)
    text_c(d, (cx, cy), text, f, alpha(fg, a))


def terminal(d, box, a):
    """A Claude Code window: dark card with three dots."""
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 26, fill=alpha(TERM, a))
    for k, col in enumerate([(232, 106, 94), (236, 190, 84), (110, 190, 110)]):
        d.ellipse([x0 + 30 + k * 30, y0 + 24, x0 + 46 + k * 30, y0 + 40], fill=alpha(col, a))
    text_c(d, ((x0 + x1) / 2, y0 + 32), "claude", mono(24), alpha(TERM_DIM, a))


def line(d, x, y, text, col, a, prompt=False):
    if a <= 0:
        return
    f = mono(30)
    if prompt:
        text_c(d, (x, y), "›", f, alpha(ACCENT, a), anchor="lm")
        x += 30
    text_c(d, (x, y), text, f, alpha(col, a), anchor="lm")


SAY = 'Let\'s call the staging server "acorn".'
ASK = "What did we call the staging server?"

# ---------------------------------------------------------------- scenes


def scene_acorn(frame, t, dur, speech, sc):
    n = sc["narration"]
    clear = cue(n, "Clear the session", 0.25) * speech
    ask = cue(n, "ask again", 0.4) * speech
    gone = cue(n, "it's gone", 0.6) * speech
    forgets = cue(n, "Claude forgets", 0.75) * speech
    doesnt = cue(n, "Cogi doesn't", 0.9) * speech
    wipe = 1 - ease(seg(t, clear + 0.7, clear + 1.0))
    af = ease(seg(t, forgets - 0.1, forgets + 0.4))
    ad = ease(seg(t, doesnt - 0.1, doesnt + 0.4))
    paste_cogi(frame, 860, 860, 280, ad)

    def draw(d, _):
        a = ease(seg(t, 0.05, 0.4))
        terminal(d, (90, 110, 990, 640), a)
        line(d, 130, 130 + 80, SAY, TERM_INK, ease(seg(t, 0.3, 0.7)) * wipe, prompt=True)
        line(d, 130, 130 + 140, "Got it: the staging server is acorn.", TERM_DIM, ease(seg(t, 1.0, 1.4)) * wipe)
        line(d, 130, 130 + 200, "/clear", TERM_INK, ease(seg(t, clear - 0.1, clear + 0.2)) * wipe, prompt=True)
        aa = ease(seg(t, ask - 0.1, ask + 0.3))
        line(d, 130, 130 + 80, ASK, TERM_INK, aa, prompt=True)
        ag = ease(seg(t, gone - 0.2, gone + 0.3))
        line(d, 130, 130 + 140, "I don't have that in this conversation.", (214, 120, 104), ag)
        text_c(d, (110, 790), "Claude forgets.", HEAD(88), alpha(INK, af), anchor="lm")
        text_c(d, (110, 900), "Cogi doesn't.", HEAD(88), alpha(ACCENT, ad), anchor="lm")
    overlay(frame, draw)


def scene_keeps(frame, t, dur, speech, sc):
    n = sc["narration"]
    keeps = cue(n, "It keeps", 0.4) * speech
    word = cue(n, "word for word", 0.7) * speech
    time_ = cue(n, "with the time", 0.85) * speech
    a0 = ease(seg(t, 0.05, 0.45))
    slots = [(740 + c * 90, 520 + r * 92) for r in range(4) for c in range(3)]

    def draw(d, _):
        text_c(d, (W / 2, 140 + 10 * (1 - a0)), "A free, long-term memory", HEAD(64), alpha(INK, a0))
        text_c(d, (W / 2, 215), "for Claude Code", HEAD(56), alpha(ACCENT, a0))
        # the tree and its hollow, where every message goes
        d.rounded_rectangle([650, 320, 1010, 1050], 60, fill=alpha(BARK, a0))
        d.ellipse([680, 420, 980, 900], fill=alpha(HOLLOW, a0))
        # the conversation on the left
        for k in range(5):
            mine = k % 2 == 0
            y = 330 + k * 108
            x0, x1 = (80, 450) if mine else (160, 540)
            ab = ease(seg(t, 0.3 + k * 0.2, 0.6 + k * 0.2))
            d.rounded_rectangle([x0, y, x1, y + 84], 20, fill=alpha((255, 255, 255), ab),
                                outline=alpha(mix(INK2, CREAM, 0.6), ab), width=2)
            rng = random.Random(k)
            for j in range(2):
                lw = (x1 - x0 - 60) * rng.uniform(0.6, 1.0)
                d.rounded_rectangle([x0 + 28, y + 26 + j * 22, x0 + 28 + lw, y + 34 + j * 22], 4,
                                    fill=alpha(mix(INK2, CREAM, 0.45), ab))
        # each message becomes an acorn and flies into the hollow
        for k, (sx, sy) in enumerate(slots):
            s = keeps + k * 0.3
            if t < s:
                continue
            p = ease_out(seg(t, s, s + 0.7))
            src_y = 330 + (k % 5) * 108 + 42
            src_x = 500
            x = src_x + (sx - src_x) * p
            y = src_y + (sy - src_y) * p - 120 * p * (1 - p)
            acorn(d, x, y, 62)
            at = ease(seg(t, time_, time_ + 0.4)) * p
            if at > 0:
                text_c(d, (sx, sy + 46), f"{9 + k // 3}:{(k * 13) % 60:02d}", mono(20), alpha(TERM_INK, at))
        pill(d, 300, 1000, "word for word", BODY(36), INK, (255, 255, 255), ease(seg(t, word - 0.1, word + 0.3)),
             outline=ACCENT)
    overlay(frame, draw)
    paste_cogi(frame, 600, 935, 230, a0)


def scene_local(frame, t, dur, speech, sc):
    n = sc["narration"]
    acct = cue(n, "No account", 0.4) * speech
    key = cue(n, "no API key", 0.6) * speech
    ai = cue(n, "no AI calls", 0.8) * speech
    a0 = ease(seg(t, 0.05, 0.45))

    def draw(d, _):
        text_c(d, (W / 2, 140 + 10 * (1 - a0)), "One folder on your computer", fit(d, "One folder on your computer",
                                                                                   HEAD, 64, W - 120), alpha(INK, a0))
        # a laptop with the memory folder on screen
        d.rounded_rectangle([200, 260, 880, 680], 26, fill=alpha(TERM, a0))
        d.polygon([(130, 700), (950, 700), (1000, 740), (80, 740)], fill=alpha(mix(INK2, CREAM, 0.3), a0))
        d.rounded_rectangle([300, 400, 470, 520], 14, fill=alpha(ACCENT, a0))
        d.rounded_rectangle([300, 380, 380, 410], 10, fill=alpha(ACCENT, a0))
        text_c(d, (385, 590), "~/.cogito-mem/", mono(34), alpha(TERM_INK, a0))
        f = BODY(36)
        for txt, c, x, y in [("no account", acct, 330, 830), ("no API key", key, 750, 830),
                             ("no AI calls to save a message", ai, W / 2, 930)]:
            pa = ease(seg(t, c - 0.1, c + 0.3))
            pill(d, x, y, txt, f, INK, (255, 255, 255), pa, outline=LEAF)
    overlay(frame, draw)
    paste_cogi(frame, 700, 470, 230, ease(seg(t, 0.5, 0.9)))


def scene_find(frame, t, dur, speech, sc):
    n = sc["narration"]
    search = cue(n, "Claude searches", 0.4) * speech
    exact = cue(n, "exact words", 0.65) * speech
    answer = cue(n, "Here, it answers", 0.85) * speech
    a0 = ease(seg(t, 0.05, 0.4))
    ac = ease(seg(t, search - 0.1, search + 0.4))
    paste_cogi(frame, 190, 760, 260, ac)

    def draw(d, _):
        terminal(d, (90, 110, 990, 470), a0)
        line(d, 130, 210, ASK, TERM_INK, ease(seg(t, 0.2, 0.6)), prompt=True)
        line(d, 130, 270, "searching Cogi…", TERM_DIM, ac * (1 - ease(seg(t, answer - 0.2, answer))))
        aa = ease(seg(t, answer - 0.1, answer + 0.3))
        if aa > 0:
            line(d, 130, 270, 'You called it "acorn".', (150, 214, 150), aa)
            check_mark(d, 560, 270, 34, alpha((150, 214, 150), aa), 6)
        # what Cogi brings back: the exact words, with when they were said
        if ac > 0:
            y0 = 610 + 20 * (1 - ac)
            hl = ease(seg(t, exact - 0.1, exact + 0.4))
            d.rounded_rectangle([360, y0, 1000, y0 + 230], 22, fill=alpha((255, 255, 255), ac),
                                outline=alpha(mix(mix(INK2, CREAM, 0.6), ACCENT, hl), ac), width=4)
            text_c(d, (395, y0 + 50), "from an earlier session · 11 Nov, 10:02", mono(24), alpha(INK2, ac), anchor="lm")
            text_c(d, (395, y0 + 125), "“" + SAY + "”", fit(d, "“" + SAY + "”", BODY, 36, 570), alpha(INK, ac),
                   anchor="lm")
            text_c(d, (395, y0 + 190), "your exact words", BODY(30), alpha(ACCENT, hl), anchor="lm")
            acorn(d, 960, y0 + 50, 44, ac)
    overlay(frame, draw)


def scene_tested(frame, t, dur, speech, sc):
    n = sc["narration"]
    top5 = cue(n, "top five", 0.6) * speech
    pct = cue(n, "ninety-three", 0.8) * speech
    cols, rows = 24, 16
    gx0, gy0, cw, ch = 132, 300, 34, 26
    picks = random.Random(7).sample(range(cols * rows), 5)
    right = picks[2]

    def draw(d, _):
        a = ease(seg(t, 0.05, 0.45))
        text_c(d, (W / 2, 140 + 10 * (1 - a)), "Tested in public", HEAD(66), alpha(INK, a))
        text_c(d, (W / 2, 210), "LongMemEval · 500 questions · about 1.2M tokens each", fit(
            d, "LongMemEval · 500 questions · about 1.2M tokens each", BODY, 34, W - 140), alpha(INK2, a))
        ah = ease(seg(t, top5 - 0.1, top5 + 0.4))
        for i in range(cols * rows):
            r, c = divmod(i, cols)
            x, y = gx0 + c * cw, gy0 + r * ch
            col = TILE
            if i in picks:
                col = mix(TILE, LEAF if i == right else ACCENT, ah)
            d.rounded_rectangle([x, y, x + cw - 6, y + ch - 6], 4, fill=alpha(col, a))
        if ah > 0:
            r, c = divmod(right, cols)
            x, y = gx0 + c * cw + (cw - 6) / 2, gy0 + r * ch + (ch - 6) / 2
            d.ellipse([x - 40, y - 40, x + 40, y + 40], outline=alpha(LEAF, ah), width=5)
            text_c(d, (W / 2, 760), "the right past session, in the top five", BODY(34), alpha(INK2, ah))
        ap = ease(seg(t, pct - 0.1, pct + 0.5))
        if ap > 0:
            text_c(d, (W / 2, 880), "93%", HEAD(120), alpha(ACCENT, ap))
            text_c(d, (W / 2, 990), "4 other local memory plugins: 86.6–89.8%", BODY(32), alpha(INK2, ap))
    overlay(frame, draw)


CMD = ["claude plugin install cogito-mem \\", "  --marketplace meridian21lab/cogito-mem"]


def scene_install(frame, t, dur, speech, sc):
    n = sc["narration"]
    tip = cue(n, "My tip", 0.4) * speech
    tryit = cue(n, "Try it", 0.8) * speech
    a0 = ease(seg(t, 0.05, 0.45))
    paste_cogi(frame, W / 2, 600, 300, ease(seg(t, 0.3, 0.7)))

    def draw(d, _):
        text_c(d, (W / 2, 130), "Open source · MIT · one command", fit(d, "Open source · MIT · one command", HEAD, 56,
                                                                      W - 120), alpha(INK, a0))
        d.rounded_rectangle([90, 200, 990, 400], 22, fill=alpha(TERM, a0))
        for k, s in enumerate(CMD):
            text_c(d, (130, 262 + k * 64), s, mono(32), alpha(TERM_INK, a0), anchor="lm")
        pill(d, W / 2, 820, "Tip: ask Claude to check its memory", BODY(38), INK, (255, 255, 255),
             ease(seg(t, tip - 0.1, tip + 0.3)), outline=ACCENT)
        au = ease(seg(t, tryit - 0.1, tryit + 0.4))
        if au > 0:
            url, fu = "meridian21lab.github.io/cogito-mem", mono(40)
            uw = d.textlength(url, font=fu)
            d.rounded_rectangle([W / 2 - uw / 2 - 40, 920, W / 2 + uw / 2 + 40, 1010], 45, fill=alpha(ACCENT, au))
            text_c(d, (W / 2, 965), url, fu, alpha(CREAM, au))
    overlay(frame, draw)


def make_cover():
    """Title card in the style of Cogi's social card: the first frame and the thumbnail."""
    frame = Image.new("RGBA", (W, H), (*CREAM, 255))
    paste_cogi(frame, W / 2, 860, 620)

    def draw(d, _):
        text_c(d, (W / 2, 110), "COGITO-MEM", mono(36), ACCENT)
        text_c(d, (W / 2, 235), "Claude forgets.", HEAD(116), INK)
        text_c(d, (W / 2, 360), "Cogi doesn't.", HEAD(116), ACCENT)
        text_c(d, (W / 2, 470), "A free, private memory for Claude Code.", BODY(44), INK2)
        text_c(d, (W / 2, 1290), "meridian21lab.github.io/cogito-mem", mono(32), ACCENT)
    overlay(frame, draw)
    return frame.convert("RGB")


SCENES = {"acorn": scene_acorn, "keeps": scene_keeps, "local": scene_local, "find": scene_find,
          "tested": scene_tested, "install": scene_install}

if __name__ == "__main__":
    vk.run(HERE, SCENES, make_cover, "cogi-promo.mp4")
