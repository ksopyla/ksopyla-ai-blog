"""Cogi the squirrel for Pillow videos: rasterises cogi.svg (copied from meridian21lab/cogito-mem, site/assets).

The SVG is small and uses only absolute M/L/Q/C/Z paths, ellipses, circles and one rect, so a tiny
rasteriser is enough and no SVG library is needed. Brand colours from the Cogi site are below.

    from cogi_art import cogi
    img = cogi(360)            # RGBA, 360x360, transparent background
"""

import re
import xml.etree.ElementTree as ET
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
SVG = HERE / "cogi.svg"

# Cogi site palette (site/assets/style.css and the squirrel itself)
CREAM = (255, 251, 244)
INK = (43, 32, 23)
RUST = (184, 94, 28)  # tail, dark fur
FUR = (217, 119, 43)  # body
FUR_LIGHT = (224, 138, 60)
BELLY = (251, 231, 198)
ACCENT = (200, 98, 26)  # site accent
ACORN = (185, 122, 61)
ACORN_CAP = (107, 68, 35)

_NUM = r"-?\d*\.?\d+(?:e-?\d+)?"


def _hex(c):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _path_points(d, steps=28):
    """Flatten an absolute M/L/Q/C/Z path into a list of subpaths (lists of points)."""
    toks = re.findall(r"[MLQCZ]|" + _NUM, d)
    subs, cur, pos, cmd, i = [], [], (0.0, 0.0), None, 0

    def take(n):
        nonlocal i
        vals = [float(v) for v in toks[i:i + n]]
        i += n
        return vals

    while i < len(toks):
        if toks[i] in "MLQCZ":
            cmd = toks[i]
            i += 1
            if cmd == "Z":
                if cur:
                    subs.append(cur)
                cur = []
                continue
        if cmd == "M":
            if cur:
                subs.append(cur)
            x, y = take(2)
            cur, pos, cmd = [(x, y)], (x, y), "L"
        elif cmd == "L":
            x, y = take(2)
            cur.append((x, y))
            pos = (x, y)
        elif cmd == "Q":
            x1, y1, x, y = take(4)
            x0, y0 = pos
            for k in range(1, steps + 1):
                u = k / steps
                cur.append(((1 - u) ** 2 * x0 + 2 * (1 - u) * u * x1 + u * u * x,
                            (1 - u) ** 2 * y0 + 2 * (1 - u) * u * y1 + u * u * y))
            pos = (x, y)
        elif cmd == "C":
            x1, y1, x2, y2, x, y = take(6)
            x0, y0 = pos
            for k in range(1, steps + 1):
                u = k / steps
                a, b, c, e = (1 - u) ** 3, 3 * (1 - u) ** 2 * u, 3 * (1 - u) * u * u, u ** 3
                cur.append((a * x0 + b * x1 + c * x2 + e * x, a * y0 + b * y1 + c * y2 + e * y))
            pos = (x, y)
        else:
            i += 1
    if cur:
        subs.append(cur)
    return subs


@lru_cache(maxsize=16)
def cogi(size, ss=4):
    """Cogi as an RGBA image of size x size (the SVG's 200x200 view box), with a transparent background."""
    k = size * ss / 200.0
    canvas = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
    root = ET.parse(SVG).getroot()
    for el in root:
        tag = el.tag.split("}")[-1]
        fill = el.get("fill")
        op = float(el.get("opacity", "1"))
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        if fill and fill != "none":
            col = (*_hex(fill), 255) if fill != "#000" else (0, 0, 0, 255)
        else:
            col = None
        if tag == "path":
            subs = _path_points(el.get("d"))
            if col:
                for s in subs:
                    if len(s) > 2:
                        d.polygon([(x * k, y * k) for x, y in s], fill=col)
            stroke = el.get("stroke")
            if stroke and stroke != "none":
                w = max(1, int(float(el.get("stroke-width", "1")) * k))
                for s in subs:
                    pts = [(x * k, y * k) for x, y in s]
                    d.line(pts, fill=(*_hex(stroke), 255), width=w, joint="curve")
                    for x, y in (pts[0], pts[-1]):
                        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=(*_hex(stroke), 255))
        elif tag == "ellipse":
            cx, cy, rx, ry = (float(el.get(a)) for a in ("cx", "cy", "rx", "ry"))
            d.ellipse([(cx - rx) * k, (cy - ry) * k, (cx + rx) * k, (cy + ry) * k], fill=col)
        elif tag == "circle":
            cx, cy, r = (float(el.get(a)) for a in ("cx", "cy", "r"))
            d.ellipse([(cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k], fill=col)
        elif tag == "rect":
            x, y, w, h = (float(el.get(a)) for a in ("x", "y", "width", "height"))
            d.rounded_rectangle([x * k, y * k, (x + w) * k, (y + h) * k], float(el.get("rx", "0")) * k, fill=col)
        else:
            continue
        if op < 1:
            layer.putalpha(layer.getchannel("A").point(lambda v: int(v * op)))
        canvas.alpha_composite(layer)
    return canvas.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    out = HERE / "cogi_preview.png"
    bg = Image.new("RGBA", (420, 420), (*CREAM, 255))
    bg.alpha_composite(cogi(400), (10, 10))
    bg.convert("RGB").save(out)
    print(out)
