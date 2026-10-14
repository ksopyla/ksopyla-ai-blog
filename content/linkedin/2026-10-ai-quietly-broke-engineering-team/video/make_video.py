"""Explainer video (1080x1350, 4:5) for the LinkedIn post "What AI quietly broke in my engineering team".

Narration lives in scenes.json; the engine (captions, voiceover, encoding) in the explainer-video skill.
From the repo root:
    uv run --with Pillow content/linkedin/2026-10-ai-quietly-broke-engineering-team/video/make_video.py --stills
    uv run --with Pillow content/linkedin/2026-10-ai-quietly-broke-engineering-team/video/make_video.py
"""

import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / ".git").exists())
sys.path.insert(0, str(ROOT / ".cursor/skills/explainer-video/scripts"))

import video_kit as vk  # noqa: E402
from video_kit import (BG, BODY, HEAD, LINE, MUTED, ORANGE, PANEL, TEAL, VIOLET, WHITE, H, W,  # noqa: E402
                       alpha, bottom_shade, check_mark, cover_fit, cue, ease, ease_out, mix, mono, overlay, paste_emoji, seg,
                       text_c, top_shade)

FEATURE = Image.open(ROOT / "content/posts/what-ai-quietly-broke-in-my-engineering-team/"
                            "feature_ai_quietly_broke_engineering_teams.jpg").convert("RGB")


def fit(d, text, font_fn, size, max_w):
    """Largest font size <= size that keeps text within max_w."""
    while size > 20 and d.textlength(text, font=font_fn(size)) > max_w:
        size -= 2
    return font_fn(size)


def header(frame, t, icon, title, sub):
    """Section header shared by the three 'things': emoji, title, one-line subtitle."""
    a = ease(seg(t, 0.05, 0.45))
    paste_emoji(frame, icon, W / 2, 105, 84, a)

    def draw(d, _):
        text_c(d, (W / 2, 200 + 12 * (1 - a)), title, HEAD(60), alpha(WHITE, a))
        text_c(d, (W / 2, 262), sub, BODY(34), alpha(MUTED, a))
    overlay(frame, draw)


def person(d, x, y, col, a=1.0, s=1.0):
    """Minimal person icon standing on (x, y)."""
    d.ellipse([x - 24 * s, y - 112 * s, x + 24 * s, y - 64 * s], fill=alpha(col, a))
    d.rounded_rectangle([x - 32 * s, y - 56 * s, x + 32 * s, y], 18 * s, fill=alpha(col, a))


def bubble(d, x, y, text, f, fg, bg, a, tail_dx=0):
    w = d.textlength(text, font=f) + 48
    h = f.size + 34
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 22, fill=alpha(bg, a))
    d.polygon([(x + tail_dx - 14, y + h / 2 - 2), (x + tail_dx + 14, y + h / 2 - 2), (x + tail_dx, y + h / 2 + 22)],
              fill=alpha(bg, a))
    text_c(d, (x, y), text, f, alpha(fg, a))


def dashed(d, pts, fill, width, dash=22, gap=14):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        u = 0.0
        while u < L:
            v = min(u + dash, L)
            d.line([(x0 + (x1 - x0) * u / L, y0 + (y1 - y0) * u / L), (x0 + (x1 - x0) * v / L, y0 + (y1 - y0) * v / L)],
                   fill=fill, width=width)
            u += dash + gap

# ---------------------------------------------------------------- scenes


# the question I kept asking: "we", because I am part of the team
OLD_Q = "Why can't we ship faster?"


def scene_velocity(frame, t, dur, speech, sc):
    n = sc["narration"]
    swarm = cue(n, "We tried", 0.35) * speech
    didnt = cue(n, "but our velocity", 0.45) * speech
    burned = cue(n, "burned out", 0.85) * speech
    x0, x1, y0, y1 = 150, 950, 360, 930

    def draw(d, _):
        a0 = ease(seg(t, 0.1, 0.5))
        text_c(d, (W / 2, 150), "AI will make us", HEAD(76), alpha(WHITE, a0))
        text_c(d, (W / 2, 240), "several times faster", fit(d, "several times faster", HEAD, 76, W - 120), alpha(ORANGE, a0))
        d.line([x0, y0 - 20, x0, y1, x1 + 20, y1], fill=alpha(LINE, a0), width=4)
        text_c(d, (x0 + 14, y0 - 10), "velocity", BODY(30), alpha(MUTED, a0), anchor="lm")
        text_c(d, (x1 + 20, y1 + 36), "this year", BODY(30), alpha(MUTED, a0), anchor="rm")
        # the expectation: a straight dashed line, steep
        pe = ease(seg(t, 0.4, max(1.2, swarm - 0.1)))
        ex = x0 + (x1 - x0) * pe
        ey = (y1 - 60) + ((y0 + 40) - (y1 - 60)) * pe
        if pe > 0:
            dashed(d, [(x0, y1 - 60), (ex, ey)], alpha(ORANGE, 1), 6)
        text_c(d, (x1 - 40, y0 + 10), "expected", HEAD(44), alpha(ORANGE, ease(seg(pe, 0.8, 1))), anchor="rm")
        # reality: a wobbly line that barely climbs
        pa = ease_out(seg(t, didnt, didnt + 1.6))
        pts = []
        for i in range(int(80 * pa) + 1):
            u = i / 80
            v = 0.1 + 0.32 * u + 0.035 * math.sin(u * 23) + 0.02 * math.sin(u * 61)
            pts.append((x0 + u * (x1 - x0), y1 - 60 - v * (y1 - y0 - 160) * 0.55))
        if len(pts) > 1:
            d.line(pts, fill=TEAL, width=7, joint="curve")
        text_c(d, (x1 - 10, pts[-1][1] - 50 if pts else y1), "what we got", HEAD(40),
               alpha(TEAL, ease(seg(pa, 0.85, 1))), anchor="rm")
        # the AI factory: a busy little plant with agents buzzing around it, while the real line barely climbs
        asw = ease(seg(t, swarm - 0.1, swarm + 0.4))
        if asw > 0:
            fx, fy = 330, 600
            roof = [(fx - 70, fy - 20)] + [p for k in range(3) for p in
                                            ((fx - 70 + k * 47 + 47, fy - 62), (fx - 70 + k * 47 + 47, fy - 20))]
            d.rectangle([fx + 30, fy - 105, fx + 50, fy - 40], fill=alpha(PANEL, asw), outline=alpha(VIOLET, asw), width=3)
            d.polygon(roof + [(fx + 70, fy + 40), (fx - 70, fy + 40)], fill=alpha(PANEL, asw),
                      outline=alpha(VIOLET, asw), width=3)
            for k in range(3):
                d.rectangle([fx - 52 + k * 40, fy + 2, fx - 30 + k * 40, fy + 22], fill=alpha(ORANGE, 0.8 * asw))
            rng = random.Random(5)
            for k in range(22):
                ang = rng.uniform(0, 2 * math.pi) + t * rng.uniform(1.5, 3.0) * (1 if k % 2 else -1)
                rad = rng.uniform(95, 125)
                bx, by = fx + rad * 1.3 * math.cos(ang), fy + rad * 0.75 * math.sin(ang)
                d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=alpha(VIOLET, 0.85 * asw))
            text_c(d, (fx, fy - 150), "AI factory", BODY(34), alpha(VIOLET, asw))
        ab = ease(seg(t, burned - 0.2, burned + 0.4))
        text_c(d, (W / 2, 1015), "anxious, then burned out", BODY(44), alpha(MUTED, ab))
    overlay(frame, draw)


THINGS = [("💸", "The cost of building", "it forced us to choose"),
          ("🪜", "The ladder of experience", "it gave people standing"),
          ("🙋", "Asking each other", "it held the team together")]


def scene_three(frame, t, dur, speech, sc):
    n = sc["narration"]
    ask = cue(n, "analysing why", 0.2) * speech
    deeper = cue(n, "something deeper", 0.55) * speech
    how = cue(n, "how AI", 0.7) * speech
    three = how + 0.4
    cards_y = [520, 720, 920]
    # the shipping question opens big in the middle; while analysing it, something deeper shows up,
    # so the question steps aside (it stays valid, it is not crossed out)
    aq = ease(seg(t, ask - 0.2, ask + 0.4))
    mv = ease(seg(t, deeper - 0.2, deeper + 0.6))
    qy = 560 + (120 - 560) * mv

    def draw(d, _):
        text_c(d, (W / 2, qy), OLD_Q, HEAD(int(66 - 26 * mv)), alpha(mix(WHITE, MUTED, mv), aq * (1 - 0.3 * mv)))
        ad = ease(seg(t, deeper - 0.1, deeper + 0.4)) * (1 - ease(seg(t, how - 0.1, how + 0.2)))
        text_c(d, (W / 2, 660), "…and noticed something deeper", BODY(40), alpha(MUTED, ad))
        a = ease(seg(t, how - 0.1, how + 0.4))
        q = "How AI quietly changed our team"
        text_c(d, (W / 2, 225 + 14 * (1 - a)), q, fit(d, q, HEAD, 72, W - 100), alpha(ORANGE, a))
        text_c(d, (W / 2, 335), "These are my observations:", BODY(40), alpha(WHITE, a))
        for i, (_, title, sub) in enumerate(THINGS):
            ai = ease(seg(t, three + i * 0.3, three + i * 0.3 + 0.4))
            if ai <= 0:
                continue  # an invisible card would erase whatever is underneath it
            y = cards_y[i] + 30 * (1 - ai)
            d.rounded_rectangle([110, y - 80, W - 110, y + 80], 26, fill=alpha(PANEL, ai),
                                outline=alpha(LINE, ai), width=2)
            text_c(d, (290, y - 20), title, HEAD(46), alpha(WHITE, ai), anchor="lm")
            text_c(d, (290, y + 32), sub, BODY(32), alpha(MUTED, ai), anchor="lm")
    overlay(frame, draw)
    # a magnifying glass while the question is being analysed
    paste_emoji(frame, "🔍", W / 2, 440, 96, aq * (1 - mv))
    for i, (icon, _, _) in enumerate(THINGS):
        ai = ease(seg(t, three + i * 0.3, three + i * 0.3 + 0.4))
        paste_emoji(frame, icon, 200, cards_y[i] + 30 * (1 - ai), 92, ai)


def scene_bottleneck(frame, t, dur, speech, sc):
    n = sc["narration"]
    now = cue(n, "Now every idea", 0.4) * speech
    neck = cue(n, "Code was never", 0.7) * speech
    header(frame, t, "💸", "The cost of building", "it forced us to choose")
    gate_x = 850
    spawn = [0.7, 1.9] + [now + 0.2 + 0.2 * k for k in range(13)]
    spawn = [s for s in spawn if s < dur - 0.3]

    def slot(k):
        col, row = divmod(k, 3)
        return gate_x - 80 - col * 86, 600 + row * 78

    def draw(d, _):
        a = ease(seg(t, 0.2, 0.6))
        # build box and decision gate
        d.rounded_rectangle([80, 540, 320, 820], 24, outline=alpha(TEAL, a), width=4, fill=alpha(TEAL, 0.08 * a))
        text_c(d, (200, 500), "build", HEAD(44), alpha(TEAL, a))
        text_c(d, (200, 862), "fast", BODY(36), alpha(TEAL, a))
        pulse = 0.5 + 0.5 * math.sin(t * 6) if t > neck else 0
        gw = 4 + 4 * pulse
        d.rounded_rectangle([gate_x - 6, 520, gate_x + 30, 840], 12, outline=alpha(ORANGE, a), width=int(gw),
                            fill=alpha(ORANGE, 0.12 * a))
        text_c(d, (gate_x + 12, 480), "decide", HEAD(44), alpha(ORANGE, a))
        text_c(d, (gate_x + 12, 882), "slow", BODY(36), alpha(ORANGE, a))
        # demo cards fly from build to the queue in front of the gate
        for k, s in enumerate(spawn):
            if t < s:
                continue
            p = ease_out(seg(t, s, s + 0.55))
            sx, sy = slot(k)
            x = 300 + (sx - 300) * p
            y = 680 + (sy - 680) * p
            d.rounded_rectangle([x - 34, y - 26, x + 34, y + 26], 8, fill=alpha(mix(PANEL, WHITE, 0.15), 1),
                                outline=alpha(VIOLET, 0.9), width=2)
            d.line([x - 22, y - 10, x + 14, y - 10], fill=alpha(VIOLET, 0.9), width=3)
            d.line([x - 22, y + 4, x + 22, y + 4], fill=alpha(MUTED, 0.8), width=3)
            d.line([x - 22, y + 14, x + 6, y + 14], fill=alpha(MUTED, 0.8), width=3)
        if t > now:
            text_c(d, (590, 925), "every idea, a working demo", BODY(36), alpha(VIOLET, ease(seg(t, now, now + 0.5))))
        aq = ease(seg(t, neck - 0.1, neck + 0.5))
        if aq > 0 and len(spawn) > 3:
            cols = (len(spawn) - 1) // 3
            left = gate_x - 80 - cols * 86 - 50
            d.rounded_rectangle([left, 556, gate_x - 30, 802], 20, outline=alpha(ORANGE, aq), width=4)
            text_c(d, (590, 1000), "waiting for a decision", HEAD(52), alpha(ORANGE, aq))
    overlay(frame, draw)


def scene_ladder(frame, t, dur, speech, sc):
    n = sc["narration"]
    lifts = cue(n, "With AI", 0.25) * speech
    conf = cue(n, "sound sure", 0.4) * speech
    hedge = cue(n, "Seniors still", 0.55) * speech
    fix = cue(n, "who fixes", 0.85) * speech
    header(frame, t, "🪜", "The ladder of experience", "it gave people standing")
    p = ease(seg(t, lifts, lifts + 1.4))
    gap = 150 - 114 * p
    base = 1010
    rungs = [base - i * gap for i in range(5)]
    jx, sx = 450, 640
    jy = rungs[0] + (rungs[2] - rungs[0]) * p  # the junior climbs while the ladder flattens
    sy = rungs[4]

    def draw(d, _):
        a = ease(seg(t, 0.2, 0.6))
        top = rungs[4] - 60
        d.line([300, top, 300, base + 50], fill=alpha(LINE, a), width=9)
        d.line([780, top, 780, base + 50], fill=alpha(LINE, a), width=9)
        for y in rungs:
            d.line([300, y, 780, y], fill=alpha(LINE, a), width=9)
        person(d, jx, jy - 5, TEAL, a, 1.1)
        person(d, sx, sy - 5, VIOLET, a, 1.1)
        text_c(d, (240, jy - 60), "junior", BODY(32), alpha(TEAL, a), anchor="rm")
        text_c(d, (840, sy - 60), "senior", BODY(32), alpha(VIOLET, a), anchor="lm")
        ac = ease(seg(t, conf - 0.1, conf + 0.4))
        if ac > 0:
            bubble(d, 310, jy - 250, "Easy. Ship it!", HEAD(50), BG, ORANGE, ac, tail_dx=130)
        ah = ease(seg(t, hedge - 0.1, hedge + 0.4))
        if ah > 0:
            bubble(d, 790, sy - 230, "it depends…", BODY(32), WHITE, LINE, ah, tail_dx=-80)
    overlay(frame, draw)
    af = ease(seg(t, fix - 0.1, fix + 0.4))
    paste_emoji(frame, "🔧", sx + 85, sy - 60, 64, af)


def scene_asking(frame, t, dur, speech, sc):
    n = sc["narration"]
    ask = cue(n, "for help", 0.15) * speech
    alone = cue(n, "we ask a chatbot", 0.3) * speech
    header(frame, t, "🙋", "Asking each other", "it held the team together")
    p = ease(seg(t, alone, alone + 1.2))
    cx, cy, r = W / 2, 690, 250 + 70 * p
    nodes = [(cx + r * math.cos(-math.pi / 2 + i * 2 * math.pi / 7), cy + r * math.sin(-math.pi / 2 + i * 2 * math.pi / 7))
             for i in range(7)]
    edges = [(i, (i + 1) % 7) for i in range(7)] + [(i, (i + 3) % 7) for i in range(7)]

    def draw(d, _):
        a = ease(seg(t, 0.2, 0.6))
        ea = a * (1 - p)
        for i, j in edges:
            d.line([nodes[i], nodes[j]], fill=alpha(ORANGE, 0.55 * ea), width=4)
        # small requests travelling along the links
        if ea > 0:
            for k, (i, j) in enumerate(edges[::2]):
                u = (t * 0.6 + k * 0.37) % 1
                x = nodes[i][0] + (nodes[j][0] - nodes[i][0]) * u
                y = nodes[i][1] + (nodes[j][1] - nodes[i][1]) * u
                d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=alpha(WHITE, 0.9 * ea))
        for (x, y) in nodes:
            col = mix(ORANGE, TEAL, p)
            person(d, x, y + 44, col, a, 0.75)
            if p > 0:  # each person gets a private screen
                sxp, syp = x + 52, y + 10
                for g in range(3, 0, -1):
                    d.rounded_rectangle([sxp - 26 - g * 6, syp - 20 - g * 6, sxp + 26 + g * 6, syp + 20 + g * 6], 10,
                                        fill=alpha(TEAL, 0.07 * p))
                d.rounded_rectangle([sxp - 26, syp - 20, sxp + 26, syp + 20], 8, fill=alpha(mix(TEAL, WHITE, 0.3), p))
        aa = ease(seg(t, ask, ask + 0.4)) * (1 - ease(seg(t, alone - 0.2, alone + 0.3)))
        if aa > 0:
            bx, by = (nodes[0][0] + nodes[1][0]) / 2 - 20, (nodes[0][1] + nodes[1][1]) / 2 - 90
            bubble(d, bx, by, "why is this container out of memory?", BODY(32), BG, WHITE, aa, tail_dx=-160)
    overlay(frame, draw)


REPORT = ["tasks closed", "PRs merged", "demos shipped"]


def scene_report(frame, t, dur, speech, sc):
    n = sc["narration"]
    free = cue(n, "It used to", 0.4) * speech
    built = cue(n, "Now it has", 0.65) * speech
    rows_y = [730, 830, 930]
    hb = ease(seg(t, built - 0.1, built + 0.5))

    def draw(d, _):
        a = ease(seg(t, 0.1, 0.5))
        d.rounded_rectangle([140, 110, W - 140, 560], 28, fill=alpha(PANEL, a), outline=alpha(LINE, a), width=2)
        text_c(d, (W / 2, 180), "Sprint report", HEAD(54), alpha(WHITE, a))
        for i, row in enumerate(REPORT):
            ai = ease(seg(t, 0.4 + i * 0.3, 0.8 + i * 0.3))
            y = 290 + i * 85
            text_c(d, (230, y), row, BODY(42), alpha(WHITE, ai), anchor="lm")
            if ai > 0:
                check_mark(d, 830, y, 44, alpha(TEAL, ai), 8)
        al = ease(seg(t, 1.0, 1.5))
        text_c(d, (W / 2, 630), "not on the report", BODY(38), alpha(MUTED, al))
        for i, (_, title, _) in enumerate(THINGS):
            ai = ease(seg(t, 1.2 + i * 0.25, 1.6 + i * 0.25))
            if ai <= 0:
                continue
            y = rows_y[i]
            d.rounded_rectangle([140, y - 46, W - 140, y + 46], 20, fill=alpha(PANEL, ai * (0.5 + 0.5 * hb)),
                                outline=alpha(mix(LINE, ORANGE, hb), ai), width=3)
            text_c(d, (300, y), title, BODY(40), alpha(mix(MUTED, WHITE, hb), ai), anchor="lm")
        af = ease(seg(t, free, free + 0.4)) * (1 - ease(seg(t, built - 0.5, built - 0.1)))
        text_c(d, (W / 2, 1020), "it used to come for free", BODY(40), alpha(MUTED, af))
        text_c(d, (W / 2, 1020), "now: built on purpose", HEAD(52), alpha(ORANGE, hb))
    overlay(frame, draw)
    for i, (icon, _, _) in enumerate(THINGS):
        ai = ease(seg(t, 1.2 + i * 0.25, 1.6 + i * 0.25))
        paste_emoji(frame, icon, 220, rows_y[i], 60, ai * (0.4 + 0.6 * hb))


END_BG = None
TITLE = "3 things AI quietly eroded"


def scene_end(frame, t, dur, speech, sc):
    global END_BG
    if END_BG is None:
        bg = cover_fit(FEATURE, zoom=1.05).filter(ImageFilter.GaussianBlur(14))
        END_BG = Image.blend(Image.new("RGB", (W, H), BG), bg, 0.32).convert("RGBA")
    frame.alpha_composite(END_BG)

    n = sc["narration"]
    read = cue(n, "Read the full", 0.75) * speech
    adapt = cue(n, "we have to adapt", 0.2) * speech
    watch = cue(n, "watching the costs", 0.45) * speech

    def a(i):
        return ease(seg(t, 0.2 + i * 0.4, 0.7 + i * 0.4))

    def draw(d, _):
        text_c(d, (W / 2, 250), TITLE, fit(d, TITLE, HEAD, 88, W - 120), alpha(WHITE, a(0)))
        text_c(d, (W / 2, 350), "in my engineering team", fit(d, "in my engineering team", HEAD, 70, W - 140),
               alpha(ORANGE, a(0)))
        # adapt, but weigh both sides: a balance that swings and settles level once the costs are watched too
        ab = ease(seg(t, adapt - 0.2, adapt + 0.4))
        if ab > 0:
            settle = ease(seg(t, watch, watch + 1.2))
            tilt = (1 - settle) * 0.16 * math.sin(t * 2.2) + (1 - ease(seg(t, adapt, watch))) * 0.12
            cx, by, half = W / 2, 500, 230
            lx, ly = cx - half * math.cos(tilt), by + half * math.sin(tilt)
            rx, ry = cx + half * math.cos(tilt), by - half * math.sin(tilt)
            d.polygon([(cx, by + 6), (cx - 34, by + 90), (cx + 34, by + 90)], fill=alpha(LINE, ab))
            d.line([(lx, ly), (rx, ry)], fill=alpha(WHITE, ab), width=7)
            for (px, py), col, label in [((lx, ly), TEAL, "gains"), ((rx, ry), ORANGE, "costs")]:
                d.line([(px, py), (px - 46, py + 70)], fill=alpha(col, ab), width=3)
                d.line([(px, py), (px + 46, py + 70)], fill=alpha(col, ab), width=3)
                d.chord([px - 62, py + 40, px + 62, py + 100], 0, 180, fill=alpha(col, 0.85 * ab))
                text_c(d, (px, py + 132), label, HEAD(40), alpha(col, ab))
        # call to action: the blog carries the full story, the research and what I am trying as a lead
        ar = ease(seg(t, read - 0.2, read + 0.4))
        text_c(d, (W / 2, 760 + 16 * (1 - ar)), "Read the full story", HEAD(68), alpha(WHITE, ar))
        sub = "the research behind it, and 4 things I'm trying as a lead"
        text_c(d, (W / 2, 840), sub, fit(d, sub, BODY, 34, W - 140), alpha(MUTED, ar))
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
    frame.paste(cover_fit(FEATURE, zoom=1.0, fx=0.5, fy=0.55))
    top_shade(frame, 700, 0.93)
    bottom_shade(frame, 320, 0.85)

    def draw(d, _):
        sk = dict(stroke_width=3, stroke_fill=alpha(BG, 0.6))
        text_c(d, (W / 2, 95), "FIELD NOTES · AI LEADERSHIP", mono(30), TEAL)
        text_c(d, (W / 2, 210), TITLE, fit(d, TITLE, HEAD, 96, W - 100), WHITE, **sk)
        text_c(d, (W / 2, 320), "in my engineering team", fit(d, "in my engineering team", HEAD, 76, W - 120), ORANGE,
               **sk)
        text_c(d, (W / 2, 425), "after an AI speed-up that never came", BODY(42), WHITE, stroke_width=2,
               stroke_fill=alpha(BG, 0.8))
        text_c(d, (W / 2, 1290), "ai.ksopyla.com", mono(32), alpha(WHITE, 0.85))
    overlay(frame, draw)
    return frame.convert("RGB")


SCENES = {"velocity": scene_velocity, "three": scene_three, "bottleneck": scene_bottleneck, "ladder": scene_ladder,
          "asking": scene_asking, "report": scene_report, "end": scene_end}

if __name__ == "__main__":
    vk.run(HERE, SCENES, make_cover, "ai-quietly-broke-engineering-team.mp4")
