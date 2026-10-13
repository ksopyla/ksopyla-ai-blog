---
name: explainer-video
description: Build short narrated explainer videos (45-60 s, 4:5 portrait, burned-in captions, ElevenLabs voiceover) for LinkedIn or X posts, drawn frame by frame with Pillow and encoded with ffmpeg. Use when the user asks for an explainer video, a short video, an animated version of a post or article, a video for LinkedIn or X, or wants to tweak or re-render an existing post video.
---

# Explainer Video

A short video that carries one post's argument in under a minute: a title card, 6-8 animated scenes, a voiceover and burned-in captions. It sits next to a LinkedIn post (`linkedin-post` skill) or an X thread; it does not replace the text post.

## Files

```
content/linkedin/YYYY-MM-<slug>/
├── post.md              # frontmatter gets  video: "video/<slug>.mp4 ..."
└── video/
    ├── scenes.json      # title, size, fps, scenes [{id, visual, narration}]   (committed)
    ├── make_video.py    # one draw function per visual + make_cover()          (committed)
    ├── <slug>.mp4       # build output                                          (gitignored)
    ├── cover.jpg        # custom thumbnail = first frame                        (gitignored)
    ├── audio/           # cached TTS clips + manifest                           (gitignored)
    └── stills/          # review PNGs                                           (gitignored)
```

The shared engine is `scripts/video_kit.py` in this skill: palette, fonts, easing, captions, emoji, ElevenLabs TTS with caching, rendering, audio muxing and the CLI. A post's `make_video.py` only draws its scenes. Start from the newest reference: `content/linkedin/2026-10-ai-quietly-broke-engineering-team/video/`.

## Requirements

- `uv` (runs the script with Pillow): `uv run --with Pillow <post>/video/make_video.py`
- `ffmpeg` and `ffprobe` on PATH (`brew install ffmpeg` on the Mac)
- `ELEVENLABS_API_KEY` in the environment or the repo-root `.env` (optional `ELEVENLABS_VOICE_ID`; default voice `JBFqnCBsd6RMkjVDRZzb`). Never print or commit the key.

## Workflow

1. **Find the spine.** One thesis and 5-7 beats, taken from the LinkedIn post, not from the article's section order. The video and the post should tell the same story in the same order.
2. **Write `scenes.json`** (narration rules below). Show the narration to the author before spending TTS credits when the story is new.
3. **Draw the scenes** in `make_video.py`: `def scene_x(frame, t, dur, speech, sc)`, register it in `SCENES`, add `make_cover()`, end with `video_kit.run(HERE, SCENES, make_cover, "<slug>.mp4")`.
4. **Review with stills**: `--stills` writes the cover plus each scene at 35% and 95% of its length to `video/stills/`, with no encoding and no TTS. Paste them into one contact sheet and look at all the scenes at once. Fix overlaps, empty stretches and text that collides with the caption band. Repeat.
5. **Render**: the default run generates the voiceover (cached per scene by a narration hash) and times every scene to its clip. `--silent` renders without audio, using a word-count timing estimate.
6. **QA the mp4**: `ffprobe` (h264 + aac, 1080x1350, under 60 s); extract frames at the narration cue points (`ffmpeg -ss <t> -i video.mp4 -frames:v 1 f.png`) and check that each visual lands with its words. Watch it once with sound before handing it over.
7. **Hand over**: send the mp4 to the author, and update `post.md` with the `video:` line. On LinkedIn: upload the video natively, set `cover.jpg` as the thumbnail, use the post text as the caption, and keep links out of the post.

## Narration Rules

- 6-8 scenes, at most ~25 words each, 120-150 words in total: roughly 45-60 s at ~2.6 words/s.
- Scene 1 is the hook: tension within the first 3 seconds (a broken expectation, a number, a confession). No "In this video...".
- Spoken English: short sentences, first person, contractions are fine. No numbers or terms the listener cannot parse without the screen.
- One idea per scene. Say "First / Second / Third" when the post has a list; it helps listeners who are not watching.
- Last scene: one closing line plus where to read more (the blog). No hard sell.
- Same voice rules as the blog: modest, specific, no hype words.

## Visual Rules

- **Format**: 1080x1350 (4:5), 30 fps, H.264 + AAC. The title card is held for 1 s as the first frame, so the feed thumbnail is never black.
- **Layout**: visuals stay above `CONTENT_BOTTOM` (y=1140); captions live in the bottom band (y~1240). Captions are burned in because LinkedIn autoplays muted.
- **One motion per scene** that carries the idea (a line that falls short of a target, cards piling up at a gate, a ladder flattening, links fading). Time its key moment to a phrase with `cue(narration, "phrase", default) * speech`.
- **On-screen text adds to the captions instead of repeating them**: a header, labels, at most ~8 words of extra text per scene.
- **Wayfinding**: reuse the post's emoji or icons as scene headers (`paste_emoji`), so the video, the post and the blog look like one system.
- **Brand**: palette from the kit (`BG`, `ORANGE`, `TEAL`, `VIOLET`, `WHITE`, `MUTED`), fonts Outfit Bold (`HEAD`), Work Sans (`BODY`) and a monospace (`mono`). Use the blog feature image for the cover and the end card when it fits (`cover_fit` + `top_shade`).
- **Fit text**: measure with `d.textlength` and shrink long titles; nothing within 50 px of the frame edges.

## Gotchas

- An overlay layer **replaces** pixels instead of blending them: a shape or text drawn with alpha 0 erases what is underneath, and two semi-transparent items in one layer do not blend. `text_c` skips zero-alpha text; guard shapes with `if a > 0`, and do not cross-fade two labels in the same spot at the same time.
- Colour emoji need Apple Color Emoji (Mac) or Noto Color Emoji (Linux); `paste_emoji` draws nothing when neither is installed, so every scene must still read without them.
- The bundled fonts lack some glyphs (✓, ↑): draw them (`check_mark`) or avoid them. "→" and "…" work.
- Every animated value must be a pure function of `t`. Random layouts use a fixed seed (`random.Random(11)`), or they jump between frames.
- Rendering is ~1 min for a 50 s video on a Mac. Use `--stills` for iteration, not full renders.
- TTS is cached per scene: editing one narration regenerates one clip; `--regen` regenerates all of them.
