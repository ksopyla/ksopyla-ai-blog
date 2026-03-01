---
name: image-generation
description: Blog feature image style guide and prompt templates. Use when generating feature images for blog posts.
---
# Feature Image Style Guide

## Visual Identity

The blog's feature images use **vibrant, full-spectrum abstract digital art** — NOT minimal dark backgrounds.

Core characteristics:
- **Full color spectrum**: Rich saturation across warm oranges, yellows, teals, blues, greens, purples — all in one image
- **Abstract and conceptual**: Captures the *feeling* or *metaphor* of the topic, not a literal diagram
- **Textured and layered**: Digital painting, glitch art, flowing organic forms, or collage-like compositions
- **High visual density**: Complex, detailed, immersive — not sparse or minimal
- **No text, no watermarks, no labels**
- **16:9 aspect ratio** (1280x720 or higher)

Real examples from published posts:
- `feature_paht_to_ai_products.png` — glitch art silhouette walking through rainbow horizontal streaks
- `feature_blogging_platform.png` — warm orange/yellow flowing into teal/green, organic circuit-board forms
- `feature_abstract_face_thinking.png` — pixelated/tiled abstract face in multi-color digital collage

## Base Prompt Template

Use this as the foundation, adapting the `[CONCEPT]` and mood to the post's theme (e.g. technical architecture, research experiment, failure/debugging, efficiency, paper review, contrarian take):

```
abstract digital painting visualizing [CONCEPT], flowing data streams as luminous rivers
of light, warm oranges and teals merging into deep blues, organic and geometric forms
combined, rich color spectrum, textured digital art, high detail, no text, no watermark
```

## Priority

1. **Real data first** — WandB charts, training curves, architecture diagrams. Most credible.
2. **Generated concept art second** — When no real data visual exists.
3. **No image is better than a bad image** — Skip if nothing fits naturally.
