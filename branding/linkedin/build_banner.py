from PIL import Image, ImageDraw, ImageFont
import os

BANNER_W, BANNER_H = 1584, 396

ASSETS = os.path.join(os.path.dirname(__file__), 
    "../../.cursor/skills/linkedin-carousel/assets")
OUTPUT = os.path.join(os.path.dirname(__file__), "linkedin_banner_torchenstein.png")

PURPLE = (156, 39, 176)
DEEP_PURPLE = (90, 20, 110)
DARK_PURPLE = (30, 10, 40)
YELLOW = (255, 193, 7)
CREAM = (245, 225, 180)

def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def build_gradient(w, h):
    """Vertical purple gradient matching carousel brand: #9c27b0 top → dark bottom."""
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        if t < 0.3:
            color = PURPLE
        elif t < 0.8:
            blend = (t - 0.3) / 0.5
            color = lerp_color(PURPLE, DARK_PURPLE, blend)
        else:
            blend = (t - 0.8) / 0.2
            color = lerp_color(DARK_PURPLE, (15, 4, 20), blend)
        draw.line([(0, y), (w, y)], fill=color)
    return img

def main():
    banner = build_gradient(BANNER_W, BANNER_H)
    banner = banner.convert("RGBA")
    draw = ImageDraw.Draw(banner)

    char_path = os.path.join(os.path.dirname(__file__), "torchenstein_empty_background.png")
    char_img = Image.open(char_path).convert("RGBA")

    char_scale = (BANNER_H * 1.55) / char_img.height
    char_w = int(char_img.width * char_scale)
    char_h = int(char_img.height * char_scale)
    char_img = char_img.resize((char_w, char_h), Image.LANCZOS)

    char_x = -140
    char_y = BANNER_H - char_h + 60
    banner.paste(char_img, (char_x, char_y), char_img)

    font_verb = ImageFont.truetype(os.path.join(ASSETS, "Outfit-Bold.ttf"), 52)
    font_rest = ImageFont.truetype(os.path.join(ASSETS, "WorkSans-Regular.ttf"), 40)
    font_url = ImageFont.truetype(os.path.join(ASSETS, "Outfit-Bold.ttf"), 28)

    ascent_verb = font_verb.getmetrics()[0]
    ascent_rest = font_rest.getmetrics()[0]
    baseline_offset = ascent_verb - ascent_rest

    text_x = 950
    line_h = 90
    y_start = 40

    lines = [
        ("Build ", "agents by day"),
        ("Train ", "models by night"),
        ("Publish ", "the mess"),
    ]

    for i, (verb, rest) in enumerate(lines):
        y = y_start + i * line_h
        draw.text((text_x, y), verb, fill=YELLOW, font=font_verb)
        verb_bbox = draw.textbbox((text_x, y), verb, font=font_verb)
        verb_w = verb_bbox[2] - verb_bbox[0]
        draw.text((text_x + verb_w, y + baseline_offset), rest, fill=CREAM, font=font_rest)

    url_text = "ai.ksopyla.com"
    url_bbox = draw.textbbox((0, 0), url_text, font=font_url)
    url_w = url_bbox[2] - url_bbox[0]
    url_x = BANNER_W - url_w - 40
    url_y = BANNER_H - 50
    draw.text((url_x, url_y), url_text, fill=YELLOW, font=font_url)

    banner = banner.convert("RGB")
    banner.save(OUTPUT, "PNG")
    print(f"Banner saved to {OUTPUT}")
    print(f"Size: {banner.size}")

if __name__ == "__main__":
    main()
