---
name: linkedin-carousel
description: Build branded LinkedIn carousel image sets featuring Prof. Torchenstein. Use this skill whenever the user asks to create a LinkedIn carousel, carousel slides, carousel post, swipeable LinkedIn content, or any multi-slide visual content for LinkedIn. Also trigger when the user mentions "Torchenstein carousel", "branded carousel", "LinkedIn slides", or wants to turn content/ideas into a visual LinkedIn carousel format. This skill composites text onto branded purple/yellow templates with Prof. Torchenstein character illustrations.
---

# LinkedIn Carousel Builder — Prof. Torchenstein Brand

Build polished LinkedIn carousel slide sets (1200×1500px PNGs) using the Prof. Torchenstein brand identity.

## Brand Identity

| Element | Value |
|---------|-------|
| Background | Purple gradient `#9c27b0` → black |
| Title/heading color | Yellow `#ffc107` / `(255, 193, 7)` |
| Body text color | Warm cream `(245, 225, 180)` |
| Heading font | **Outfit-Bold** (geometric sans-serif) |
| Body font | **WorkSans-Regular** (clean, readable) |
| Character | Prof. Torchenstein — eccentric scientist, purple lab coat, goggles, grey hair |

## Template Layout (1200×1500px)

Use `carousel_cover_template_empty.png` for ALL slides (cover + inner). It has three zones:

1. **Top purple zone** (y≈0–500) — solid `#9c27b0`. Text goes here.
2. **Gradient zone** (y≈500–966) — purple fading to black. Transition area.
3. **Bottom purple bar** (y≈966–1500) — solid purple with bookmark + arrow icons. **Images go here.**

### Cover-specific
For the cover, paint the bottom purple bar dark (continue the gradient to black) before compositing the character. This lets the character's transparent background blend seamlessly. Draw title text ON TOP of the character so text and character can overlap naturally.

### Inner slide-specific
Scene images are placed at y=750 (extending into the gradient zone) with a 200px transparent gradient fade at their top edge for seamless blending. Text stays in the upper purple zone starting at y≈180.

## Assets

All in the skill's `assets/` directory:

### Templates
- `carousel_cover_template_empty.png` — Clean empty template for all slides

### Fonts (bundled)
- `Outfit-Bold.ttf` — Headings (cover 120px, slides 85px)
- `WorkSans-Regular.ttf` — Body text (46px, warm cream color)

### Character Images
| Filename | Scene | Best for |
|----------|-------|----------|
| `torchenstein_empty_background.png` | Half-body, gesturing, black bg | **Cover slides** |
| `prof-torchenstein-assembling.png` | Tinkering at workbench | Building, prototyping |
| `prof-torchenstein-coding.png` | Typing, multiple screens | Coding, software, dev |
| `prof-torchenstein-coffee-v2.png` | Holding coffee in hallway | Intro, casual, reflection |
| `prof-torchenstein-crossed-hands-in-front-window_v2.png` | Arms crossed, confident | Leadership, strategy |
| `prof-torchenstein-empty-lab-servers-racks.png` | Server room | Infrastructure, scaling |
| `prof-torchenstein-in-lab.png` | Standing in lab, gesturing | Teaching, explaining |
| `prof-torchenstein-night-constellation.png` | Arms wide, sky | Vision, future, big picture |
| `prof-torchenstein-sitting-thinking.png` | Seated, reading notes | Analysis, conclusion |

## Workflow

### Step 1 — Parse content
From the user's natural language topic, determine:
1. **Cover title** — 3–6 words per line, max 5 lines
2. **5–10 inner slides** — heading (short, punchy) + body (1–3 sentences)
3. **Image mapping** — auto-pick character images by keyword matching

### Step 2 — Create config JSON

```json
{
  "cover": {
    "title_lines": ["Line one", "Line two"],
    "character_image": "torchenstein_empty_background.png",
    "character_position": "bottom-center"
  },
  "slides": [
    {
      "heading": "Slide heading",
      "body": "Body text here.",
      "scene_image": "prof-torchenstein-coding.png"
    }
  ]
}
```

### Step 3 — Build

```bash
python3 <skill_path>/scripts/build_carousel.py \
  --config /home/claude/carousel_config.json \
  --assets <skill_path>/assets \
  --font-dir <skill_path>/assets \
  --output /home/claude/carousel_output
```

### Step 4 — Deliver
View each slide to verify, copy to `/mnt/user-data/outputs/`, present to user.

## Design Rules

### Typography
- **Cover title**: Outfit-Bold 120px, yellow `(255,193,7)`, subtle shadow, no italic
- **Slide heading**: Outfit-Bold 85px, yellow, shadow, line spacing +16px
- **Slide body**: WorkSans-Regular 46px, warm cream `(245,225,180)`, line spacing +14px
- **Gap** between heading and body: 30px
- **Left margin**: 70px. **Max text width**: 980px
- **Cover top margin**: 130px. **Slide top margin**: 180px

### Image Compositing
- **Cover**: Character scaled 2.5× slide width, black bg removed, composited at y≈340. Purple bar painted dark first for seamless blending. Title drawn ON TOP.
- **Inner slides**: Scene images scaled to fill width, cropped to 750px height (bias toward top to keep faces). Top 200px faded transparent. Placed at y=750.

### Image Selection Keywords
- coding/programming/software → `prof-torchenstein-coding.png`
- building/assembling/creating → `prof-torchenstein-assembling.png`
- thinking/reflecting/conclusion → `prof-torchenstein-sitting-thinking.png`
- vision/future/big picture → `prof-torchenstein-night-constellation.png`
- infrastructure/servers/scaling → `prof-torchenstein-empty-lab-servers-racks.png`
- explaining/teaching/presenting → `prof-torchenstein-in-lab.png`
- confidence/opinion/leadership → `prof-torchenstein-crossed-hands-in-front-window_v2.png`
- intro/casual/coffee → `prof-torchenstein-coffee-v2.png`
- cover → `torchenstein_empty_background.png`

Rotate images across slides — never reuse the same image on consecutive slides.
