"""YouTube channel banner (2560x1440) for @ksopyla-ai, in the blog's and the explainer videos' visual identity.

Background: three blog feature images, one per content pillar (agents, research, leadership), blended
into one strip and darkened. Text sits inside YouTube's safe area (1546x423, centred), which is the
only part every device shows.

Run from the repo root:  uv run --with Pillow branding/youtube/build_banner.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / ".cursor/skills/linkedin-carousel/assets"
OUT = Path(__file__).resolve().parent / "youtube_banner.png"

W, H = 2560, 1440
SAFE_W, SAFE_H = 1546, 423
SX0, SY0 = (W - SAFE_W) // 2, (H - SAFE_H) // 2

BG = (11, 15, 26)  # same palette as the explainer videos (video_kit.py)
ORANGE = (255, 154, 60)
TEAL = (58, 209, 200)
VIOLET = (155, 123, 255)
WHITE = (245, 246, 250)
MUTED = (175, 185, 210)

PILLARS = [  # left to right: agents, research, leadership
    ROOT / "content/posts/mcp_best_practices/feature_mcp_capabilities_not_endpoints.png",
    ROOT / "content/posts/auto-research-and-human-ideas/feature_auto_research_human_ideas.jpg",
    ROOT / "content/posts/what-ai-quietly-broke-in-my-engineering-team/feature_ai_quietly_broke_engineering_teams.jpg",
]


def font(name, size):
    return ImageFont.truetype(str(ASSETS / name), size)


def mono(size):
    for cand in ["/System/Library/Fonts/Menlo.ttc", "DejaVuSansMono.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]:
        try:
            return ImageFont.truetype(cand, size)
        except OSError:
            continue
    raise SystemExit("no monospace font found")


def fill_slot(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def background():
    """Three images side by side, cross-faded over a wide overlap so there are no seams."""
    slot, overlap = W // 3 + 260, 260
    canvas = Image.new("RGB", (W, H), BG)
    for i, path in enumerate(PILLARS):
        img = fill_slot(Image.open(path).convert("RGB"), slot, H)
        x0 = i * (W // 3) - (overlap // 2 if i else 0)
        mask = Image.new("L", (slot, 1), 255)
        for x in range(slot):
            a = 255
            if i > 0 and x < overlap:
                a = int(255 * x / overlap)
            if i < len(PILLARS) - 1 and x > slot - overlap:
                a = min(a, int(255 * (slot - x) / overlap))
            mask.putpixel((x, 0), a)
        canvas.paste(img, (x0, 0), mask.resize((slot, H)))
    canvas = canvas.filter(ImageFilter.GaussianBlur(3))
    # darken overall, and much more behind the text band so the motto reads on any device
    dark = Image.new("RGB", (W, H), BG)
    canvas = Image.blend(canvas, dark, 0.35)
    band = Image.new("L", (1, H), 0)
    for y in range(H):
        d = abs(y - H / 2) / (SAFE_H * 0.95)
        band.putpixel((0, y), int(215 * max(0.0, 1 - d ** 2)))
    canvas.paste(dark, (0, 0), band.resize((W, H)))
    return canvas


def main():
    """Checked on the live channel (2026-10-15): desktop and mobile both show the full 2560-wide middle
    strip (2560x423, served as 1138x188), scaled down to the page or phone width. So: two large lines
    and one topics line, centred in that strip with margins, within ~1800 px for tablet crops. The name
    and the blog link are shown by YouTube right under the banner, so the banner does not repeat them."""
    img = background().convert("RGBA")
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, H / 2
    line1, line2 = "Build agents by day, train models by night,", "publish the mess."
    size = 112
    while d.textlength(line1, font=font("Outfit-Bold.ttf", size)) > 1800:
        size -= 2
    head = font("Outfit-Bold.ttf", size)
    d.text((cx, cy - 95), line1, font=head, fill=WHITE, anchor="mm")
    d.text((cx, cy + 15), line2, font=head, fill=ORANGE, anchor="mm")
    topics = "Agentic systems   ·   AI research in the open   ·   Leading AI teams"
    d.text((cx, cy + 118), topics, font=font("WorkSans-Regular.ttf", 50), fill=MUTED, anchor="mm")
    img.convert("RGB").save(OUT, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB), motto at {size}px")


if __name__ == "__main__":
    main()
