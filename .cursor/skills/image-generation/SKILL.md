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

## Generating With The Canva Connector (Claude Code)

When the Canva MCP tools are connected, generate the image with `generate-image` and save the full-size file yourself. The visible result shows only a ~200×112 thumbnail, but the raw tool result also holds signed links to the original file:

1. Run `generate-image` (16:9) with the prompt above. Poll `get-generate-image-job` until it reports `SUCCESS`.
2. Find the original-file link in the session transcript (`~/.claude/projects/<project>/<session-id>.jsonl`). It looks like `https://media.canva.com/v2/files/uri:...`. The `media.canva.com/v2/image-resize/.../width:2400` variants also work. The links expire a few hours after generation, so download right away.
3. Download it with `curl -L` into a new, empty scratchpad folder. On 2026-11-17 the file was a 2720×1536 PNG.
4. Resize to **1680 px wide** and save as JPG, quality 85, into the post bundle. This matches earlier feature images:

   ```bash
   uv run --with Pillow python -I -c "
   from PIL import Image
   im = Image.open('<download>').convert('RGB')
   im = im.resize((1680, round(im.height * 1680 / im.width)), Image.LANCZOS)
   im.save('content/posts/<slug>/feature_<slug>.jpg', quality=85, optimize=True, progressive=True)"
   ```

5. Open the JPG with the Read tool and check it matches `featureAlt`. Then confirm that the Hugo build generates the `feature_*_hu_*` resized copies.

Do not try to export the image through a Canva design. If the links have expired, ask the author to download the image from the Canva link in the job result instead.

## When No Image Tool Is Available

If the Canva connector is not available, write the final prompt to `feature_prompt.txt` in the post bundle, tell the author, and leave `featureImage` unset until they add the file. Never ship a placeholder image.
