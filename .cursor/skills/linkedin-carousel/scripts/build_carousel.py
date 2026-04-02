#!/usr/bin/env python3
"""
LinkedIn Carousel Builder — Prof. Torchenstein Brand (v4)
Design-forward compositing with gradient blending, Outfit-Bold typography.
"""
import json, argparse, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SLIDE_W, SLIDE_H = 1200, 1500
YELLOW = (255, 193, 7)
BODY_COLOR = (245, 225, 180)


def load_font(path, size):
    try: return ImageFont.truetype(path, size)
    except:
        try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        except: return ImageFont.load_default()


def remove_black_bg(img, threshold=30):
    img = img.convert("RGBA")
    arr = np.array(img)
    mask = (arr[:,:,0]<threshold) & (arr[:,:,1]<threshold) & (arr[:,:,2]<threshold)
    arr[mask,3] = 0
    return Image.fromarray(arr)


def wrap(text, font, max_w):
    d = ImageDraw.Draw(Image.new("RGBA",(1,1)))
    words = text.split(); lines=[]; cur=""
    for w in words:
        t = f"{cur} {w}".strip()
        if d.textbbox((0,0),t,font=font)[2] <= max_w: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def meas(text, font):
    d = ImageDraw.Draw(Image.new("RGBA",(1,1)))
    bb = d.textbbox((0,0), text, font=font)
    return bb[2]-bb[0], bb[3]-bb[1]


def draw_text(draw, x, y, text, font, fill=YELLOW, shadow=3):
    """Draw text with subtle drop shadow."""
    draw.text((x+shadow, y+shadow), text, font=font, fill=(0,0,0,50))
    draw.text((x, y), text, font=font, fill=fill)


def add_top_fade(scene, fade_h=200):
    """Gradient fade at top of scene image for seamless blending with template."""
    arr = np.array(scene.convert("RGBA")).astype(float)
    for y in range(min(fade_h, arr.shape[0])):
        arr[y,:,3] *= y / fade_h
    return Image.fromarray(arr.astype(np.uint8))


def paint_purple_bar_dark(img, start_y=960):
    """Replace bottom purple bar with dark gradient continuation."""
    draw = ImageDraw.Draw(img)
    for row_y in range(start_y, SLIDE_H):
        p = (row_y - start_y) / (SLIDE_H - start_y)
        r = int(15 * (1 - p * 0.7))
        g = int(4 * (1 - p * 0.7))
        b = int(18 * (1 - p * 0.7))
        draw.line([(0, row_y), (SLIDE_W, row_y)], fill=(r, g, b, 255))
    return img


def prepare_scene(assets, scene_file, target_h=750):
    """Load, scale, crop and fade a scene image for the bottom zone."""
    sp = os.path.join(assets, scene_file)
    if not os.path.exists(sp):
        return None
    scene = Image.open(sp).convert("RGBA")
    sc = SLIDE_W / scene.width
    nh = int(scene.height * sc)
    scene = scene.resize((SLIDE_W, nh), Image.LANCZOS)

    if nh > target_h:
        crop_top = (nh - target_h) // 4  # bias top to keep faces visible
        scene = scene.crop((0, crop_top, SLIDE_W, crop_top + target_h))
    elif nh < target_h:
        s2 = target_h / nh
        scene = scene.resize((int(SLIDE_W * s2), target_h), Image.LANCZOS)
        if scene.width > SLIDE_W:
            left = (scene.width - SLIDE_W) // 2
            scene = scene.crop((left, 0, left + SLIDE_W, target_h))

    return add_top_fade(scene, fade_h=200)


# ─── COVER ──────────────────────────────────────────────────────────────

def build_cover(cfg, assets, font_dir, output):
    tmpl = Image.open(os.path.join(assets, "carousel_cover_template_empty.png")).convert("RGBA")
    tmpl = paint_purple_bar_dark(tmpl)

    ft = load_font(os.path.join(font_dir, "Outfit-Bold.ttf"),
                    cfg.get("title_font_size", 120))

    # Character — large, face visible in bottom half
    cf = cfg.get("character_image", "torchenstein_empty_background.png")
    cp = os.path.join(assets, cf)
    if os.path.exists(cp):
        ch = remove_black_bg(Image.open(cp).convert("RGBA"), 25)
        tw = int(SLIDE_W * 2.5)
        s = tw / ch.width
        ch = ch.resize((tw, int(ch.height * s)), Image.LANCZOS)
        cx = (SLIDE_W - tw) // 2 - int(tw * 0.02)
        cy = 340
        tmpl.paste(ch, (cx, cy), ch)

    # Title — Outfit-Bold, same style as slides, no italic shear
    d = ImageDraw.Draw(tmpl)
    y = cfg.get("title_y_start", 130)
    x = 70
    for line in cfg.get("title_lines", []):
        tw, th = meas(line, ft)
        draw_text(d, x, y, line, ft, fill=YELLOW, shadow=3)
        y += th + 16

    out = os.path.join(output, "slide_00_cover.png")
    tmpl.convert("RGB").save(out, quality=95)
    print(f"  [OK] Cover: {out}")
    return out


# ─── INNER SLIDES ───────────────────────────────────────────────────────

def build_slide(cfg, idx, assets, font_dir, output):
    tmpl = Image.open(os.path.join(assets, "carousel_cover_template_empty.png")).convert("RGBA")

    fh = load_font(os.path.join(font_dir, "Outfit-Bold.ttf"),
                    cfg.get("heading_font_size", 85))
    fb = load_font(os.path.join(font_dir, "WorkSans-Regular.ttf"),
                    cfg.get("body_font_size", 46))

    # Scene image at bottom with gradient fade blending
    sf = cfg.get("scene_image", "")
    if sf:
        scene = prepare_scene(assets, sf, target_h=750)
        if scene:
            tmpl.paste(scene, (0, 750), scene)

    d = ImageDraw.Draw(tmpl)
    y = cfg.get("heading_y", 180)
    x = 70
    max_w = 980

    # Heading — Outfit-Bold, yellow
    for line in wrap(cfg.get("heading", ""), fh, max_w):
        tw, th = meas(line, fh)
        draw_text(d, x, y, line, fh, fill=YELLOW, shadow=2)
        y += th + 16

    # Body — WorkSans-Regular, warm cream
    y += 30
    for line in wrap(cfg.get("body", ""), fb, max_w):
        tw, th = meas(line, fb)
        draw_text(d, x, y, line, fb, fill=BODY_COLOR, shadow=1)
        y += th + 14

    out = os.path.join(output, f"slide_{idx:02d}.png")
    tmpl.convert("RGB").save(out, quality=95)
    print(f"  [OK] Slide {idx}: {out}")
    return out


# ─── MAIN ───────────────────────────────────────────────────────────────

def build_carousel(config_path, assets, font_dir, output):
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)
    os.makedirs(output, exist_ok=True)
    files = []
    print("Building carousel slides...")
    if "cover" in config:
        files.append(build_cover(config["cover"], assets, font_dir, output))
    for i, s in enumerate(config.get("slides", []), 1):
        files.append(build_slide(s, i, assets, font_dir, output))
    print(f"\n[OK] Carousel complete! {len(files)} slides in {output}")
    return files


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--assets", required=True)
    p.add_argument("--font-dir", required=True, help="Directory containing font files")
    p.add_argument("--output", required=True)
    a = p.parse_args()
    build_carousel(a.config, a.assets, a.font_dir, a.output)
