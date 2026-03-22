---
title: "Midjourney prompts for enterprise agents carousel"
date: 2026-03-21
platform: linkedin
asset_type: midjourney-prompts
status: draft
related_blog_post: "posts/enterprise-agents-new-systems-mindset"
---

# Midjourney Prompts — LinkedIn Carousel Templates

## How To Use These Prompts

### Setup

1. Upload both Torchenstein reference images to Midjourney first.
2. Use `--cref [URL]` with the avatar image for character consistency.
3. Use `--sref [URL]` with either image for style consistency.
4. All prompts use `--ar 4:5` for LinkedIn portrait carousel format (1080x1350).

### Workflow

1. Run each slide prompt in Midjourney.
2. Pick the best variation for each slide.
3. Upscale to full resolution.
4. Import all 6 images into Canva, Figma, or PowerPoint.
5. Overlay the text from `carousel_agentic_systems_rest_fascade.md` onto each slide.
6. Export as a single PDF.

### Text Overlay Zones

Every prompt is designed to leave a clear zone for text:
- **top 30-35%** of the slide is kept relatively empty or uses simple gradients for headline placement
- **bottom 15%** stays clean for footer text or branding
- Prof. Torchenstein is positioned to the side or bottom-right so he does not block the headline

### Consistency Notes

- Keep `--cw` (character weight) between 60-80 so the character matches but the scene can vary.
- Keep `--sw` (style weight) around 100-150 for consistent color palette across slides.
- If a generation drifts from the purple/charcoal/neon palette, re-roll or adjust `--sw`.
- Run all 6 prompts in the same Midjourney session for best visual consistency.


## Base Style Block

Use this style block at the end of every prompt (before the parameters):

```
dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, deep moody purple and charcoal grey palette with neon cyan and orange accents, gothic tech steampunk AI laboratory aesthetic, clean composition with clear negative space for text overlay
```


## Slide 1 — Cover / Hook

Purpose: Stop the scroll. Bold visual. Prof. Torchenstein looking directly at the viewer with a knowing smirk. The vibe is "I'm about to tell you something uncomfortable."

```
An elderly mad scientist character with wild gray-white hair and goggles on his forehead, wearing a purple lab coat, standing in a dimly lit steampunk AI laboratory. He faces the viewer with a confident smirk and one eyebrow raised, arms crossed. Behind him, a wall of rigid server racks and API endpoint diagrams glow faintly in neon orange, but some of them are cracked and sparking. The top third of the image is a dark gradient fading to near-black, creating clear space for a headline. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, deep moody purple and charcoal grey palette with neon cyan and orange accents, gothic tech steampunk AI laboratory aesthetic, clean composition with clear negative space for text overlay --ar 4:5 --cref [TORCHENSTEIN_AVATAR_URL] --cw 70 --sref [TORCHENSTEIN_AVATAR_URL] --sw 120 --s 300 --v 6.1
```


## Slide 2 — The Old Model (REST = Smarter API)

Purpose: Visualize the rigid, outdated mental model. Torchenstein gestures dismissively at a brittle system.

```
An elderly mad scientist character with wild gray-white hair and goggles on his forehead, wearing a purple lab coat, standing to the right side of the frame. He gestures dismissively with one hand toward a large glowing holographic diagram on the left showing a rigid pipeline: boxes connected by straight arrows in a strict linear chain, labeled-looking nodes glowing in dull orange. The pipeline looks brittle and mechanical. The top third of the image is dark negative space for text. The lab background is dark charcoal with faint steampunk machinery silhouettes. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, deep moody purple and charcoal grey palette with neon cyan and orange accents, gothic tech steampunk AI laboratory aesthetic, clean composition with clear negative space for text overlay --ar 4:5 --cref [TORCHENSTEIN_AVATAR_URL] --cw 70 --sref [TORCHENSTEIN_AVATAR_URL] --sw 120 --s 300 --v 6.1
```


## Slide 3 — The Better Model (Dynamic Teams)

Purpose: Visualize the new mental model. Torchenstein is excited, presenting a living, organic system.

```
An elderly mad scientist character with wild gray-white hair and goggles on his forehead, wearing a purple lab coat, positioned at the bottom-right corner of the frame, looking up with excitement and pointing upward. Above him, a large glowing holographic network of interconnected agent nodes forms a dynamic organic cluster — nodes are different sizes and colors (cyan, purple, orange), connected by flowing curved energy lines instead of rigid arrows. The network looks alive, adaptive, and self-organizing. The top quarter of the image is dark gradient for headline space. Background is a dark steampunk laboratory with tesla coils emitting faint purple sparks. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, deep moody purple and charcoal grey palette with neon cyan and orange accents, gothic tech steampunk AI laboratory aesthetic, clean composition with clear negative space for text overlay --ar 4:5 --cref [TORCHENSTEIN_AVATAR_URL] --cw 70 --sref [TORCHENSTEIN_AVATAR_URL] --sw 120 --s 300 --v 6.1
```


## Slide 4 — What Changes (Four Consequences)

Purpose: Framework slide. Torchenstein in a teaching pose. Background shows four distinct glowing quadrants or panels.

```
An elderly mad scientist character with wild gray-white hair and goggles on his forehead, wearing a purple lab coat, standing at the bottom-center of the frame in a teaching pose, one hand raised with index finger up as if making a key point. Behind him, a large dark wall is divided into four glowing quadrants, each containing a different abstract symbol: a magnifying glass with network nodes (discovery), interlocking gears with flowing energy (runtime), a glowing budget meter or gauge (cost control), and a shield with a keyhole (identity). Each quadrant glows in a different accent color: cyan, orange, neon green, and warm red. The top quarter is dark for headline text. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, deep moody purple and charcoal grey palette with neon cyan and orange accents, gothic tech steampunk AI laboratory aesthetic, clean composition with clear negative space for text overlay --ar 4:5 --cref [TORCHENSTEIN_AVATAR_URL] --cw 70 --sref [TORCHENSTEIN_AVATAR_URL] --sw 120 --s 300 --v 6.1
```


## Slide 5 — Demos vs Production

Purpose: Show the contrast between a clean demo and messy production reality. Torchenstein looks knowing and slightly tired.

```
An elderly mad scientist character with wild gray-white hair and goggles on his forehead, wearing a purple lab coat, positioned at the bottom-right of the frame with a knowing, slightly weary expression and arms folded. The background is split vertically: the left half shows a clean, simple, glowing single agent node on a pristine dark surface (the demo), the right half shows a chaotic tangle of interconnected systems — wires, pipelines, registry boxes, evaluation loops, policy shields, all overlapping and sparking with neon accents (the production reality). The contrast is dramatic. The top quarter is dark gradient for headline text. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, deep moody purple and charcoal grey palette with neon cyan and orange accents, gothic tech steampunk AI laboratory aesthetic, clean composition with clear negative space for text overlay --ar 4:5 --cref [TORCHENSTEIN_AVATAR_URL] --cw 70 --sref [TORCHENSTEIN_AVATAR_URL] --sw 120 --s 300 --v 6.1
```


## Slide 6 — Closing Question

Purpose: Minimalist. Torchenstein faces the viewer with an open hand gesture, inviting a response. The background is sparse and contemplative.

```
An elderly mad scientist character with wild gray-white hair and goggles on his forehead, wearing a purple lab coat, positioned at the bottom-left of the frame with an open palm gesture toward the viewer, as if asking a genuine question. His expression is curious and inviting, not manic. The background is mostly dark charcoal with a single large glowing question mark made of flowing neon cyan energy, floating in the center-right of the frame. Faint steampunk lab silhouettes in the deep background. The composition is sparse and contemplative with abundant dark negative space in the top half and right side for text overlay. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, deep moody purple and charcoal grey palette with neon cyan and orange accents, gothic tech steampunk AI laboratory aesthetic, clean composition with clear negative space for text overlay --ar 4:5 --cref [TORCHENSTEIN_AVATAR_URL] --cw 70 --sref [TORCHENSTEIN_AVATAR_URL] --sw 120 --s 300 --v 6.1
```


## Optional: Texture / Pattern Background (No Character)

If you want a simpler slide template without Torchenstein on every page (e.g., for slides 2 and 4 where text density is higher), use this background-only prompt:

```
Dark steampunk AI laboratory wall texture, moody purple and charcoal grey tones, faint glowing circuit board patterns and neural network node traces in neon cyan and orange, subtle tesla coil sparks in corners, dramatic chiaroscuro lighting from the left, clean negative space in the center and top half for text overlay, no characters, no people, atmospheric and mysterious, graphic novel style with bold linework --ar 4:5 --s 300 --v 6.1
```


## Parameter Reference

| Parameter | Value | Why |
|-----------|-------|-----|
| `--ar 4:5` | portrait | LinkedIn carousel optimal mobile format |
| `--cref` | Torchenstein avatar URL | character consistency |
| `--cw 70` | character weight | enough likeness without locking the pose |
| `--sref` | Torchenstein avatar URL | palette and art style consistency |
| `--sw 120` | style weight | strong style match without over-constraining |
| `--s 300` | stylize | push toward more artistic rendering |
| `--v 6.1` | model version | best current version for character + style refs |


## Color Reference for Text Overlay

When adding text in Canva/Figma/PowerPoint, use these colors to match the brand:

| Element | Color | Hex |
|---------|-------|-----|
| Headline text | White or very light grey | `#F5F5F5` |
| Body text | Light grey | `#D0D0D0` |
| Accent / highlight words | Neon cyan | `#00E5FF` |
| Secondary accent | Neon orange | `#FF6D00` |
| Footer / subtle text | Muted purple-grey | `#9E9EB8` |
| Background fill (if needed) | Deep charcoal | `#1A1A2E` |
| Brand purple (borders, lines) | Electric purple | `#7B2FBE` |




