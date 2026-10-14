---
name: explainer-video
description: Build short narrated explainer videos (about 60 s, 4:5 portrait, burned-in captions, ElevenLabs voiceover) for LinkedIn or X posts, drawn frame by frame with Pillow and encoded with ffmpeg. Use when the user asks for an explainer video, a short video, an animated version of a post or article, a video for LinkedIn or X, or wants to tweak or re-render an existing post video.
---

# Explainer Video

A short video that carries one post's argument in about a minute: a title card, 6-8 animated scenes, a voiceover and burned-in captions. It sits next to a LinkedIn post (`linkedin-post` skill) or an X thread and sends people to the blog. It does not replace the text post or the article.

## One Story, Three Surfaces

The blog post, the LinkedIn post and the video are one story told at three depths. Krzysztof checks them against each other, so you should too.

| Surface | Job | Depth |
|---|---|---|
| Blog post | The full argument, the research, what he is trying as a lead | 10-15 min read |
| LinkedIn post | The same story as personal experience, in the post's own order | ~1,500 characters |
| Video | The post's spine, spoken, with one visual metaphor per beat | ~60 s |

- **Order of work**: blog → LinkedIn post → video. The video follows the post's order and beats, not the article's section order.
- **Reuse the strongest lines** from the blog and the post (the thesis, the key phrase of each section) instead of paraphrasing them. Paraphrases drift in meaning; he notices.
- **Keep them in sync.** When a line changes in one surface (framing, a key sentence, a heading), check the other two and propose the matching edit. In the first session a change of framing in the video led to edits in the post and a heading change in the blog.
- **The video ends with a call to action to the blog** ("Read the full, much deeper story on my blog"), with an end card that says what is there: the research and what he is trying as a lead. Not a question: the question for discussion belongs to the LinkedIn post.

## His Voice And What Matters To Him

Learned from the revision rounds of the first video (`content/linkedin/2026-10-ai-quietly-broke-engineering-team/`). Treat these as rules.

- **Experience first, told as it happened.** The story is his: expectations, trying, struggling, noticing. It is not a list of abstract claims. A good opening is a genuine confession that tech leaders recognise ("I spent the first half of the year chasing an AI speed-up that never came").
- **He is part of the team.** Never frame the team as the problem or set him against them. "What's wrong with my team?" was replaced by "Why can't we ship faster?" and "what AI had quietly taken from our team". Prefer "we" and "our".
- **Transitions must be logical, cause and effect.** Each scene follows from the one before it. A sudden pivot ("Wrong question.") reads as a trick. What worked: the insight came *as a by-product* of working on the real problem ("While analysing why we couldn't ship faster, I noticed something deeper").
- **Do not cross out a valid question.** The shipping question was still real; it steps aside on screen instead of being struck through.
- **Say exactly what he means.** He corrects lines whose logic is slightly off. "It's hard to adapt to something you haven't noticed" became "we have to adapt, but adapting well means watching the costs as closely as the gains". "Code was never the bottleneck" became "Code is no longer the bottleneck. Deciding is", the present-day point that the speed-up now comes from building the right thing, not from writing code.
- **Balanced, not doom.** He is positive about AI. A post about the negatives still says so, once, near the end.
- **No claims he did not make.** Numbers and timings come from him or the sources: "several times faster", not an invented "3x"; "fast/slow", not "days/weeks". Expectations are attributed carefully (colleagues read this).
- **No AI-sounding copy**: no "Wrong question. The better one:" twists, no arrow-bullet slogans, no paired slogan endings, no "In this video". Use his words from the post when they exist. On-screen text follows the same rule ("These are my observations", taken from the post, not an invented line).
- **His own edits are final.** Preserve his rewrites. Adapt wording only for flow (for example to avoid two sentences starting with "Now"), say that you did, and offer his exact wording.

## Story Arc That Worked

1. **Stakes**: the expectation and what was tried ("Leadership expected AI to make us several times faster. We tried to build an AI factory, but our velocity barely increased, and I burned out.").
2. **Discovery**: the real question, and the deeper finding that came out of it.
3-5. **The points**, introduced with "First / Second / Third", one concrete visual metaphor each.
6. **Why it matters**: why nobody sees it ("None of this shows up in a sprint report… Now it has to be built on purpose.").
7. **Close**: the balanced view, then the call to action to the blog.

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

The shared engine is `scripts/video_kit.py` in this skill: palette, fonts, easing, captions, emoji, ElevenLabs TTS with caching, rendering, audio muxing and the CLI. A post's `make_video.py` only draws its scenes. Start from the reference: `content/linkedin/2026-10-ai-quietly-broke-engineering-team/video/`.

## Requirements

- `uv` (runs the script with Pillow): `uv run --with Pillow <post>/video/make_video.py`
- `ffmpeg` and `ffprobe` on PATH (`brew install ffmpeg` on the Mac)
- `ELEVENLABS_API_KEY` in the environment or the repo-root `.env` (optional `ELEVENLABS_VOICE_ID`; default voice `JBFqnCBsd6RMkjVDRZzb`). Never print or commit the key.

## Workflow

1. **Read the blog post and the LinkedIn post** in full. Extract the post's beats and both texts' strongest lines.
2. **Write `scenes.json`** (narration rules below). For a new story, show the narration to the author before spending TTS credits.
3. **Draw the scenes** in `make_video.py`: `def scene_x(frame, t, dur, speech, sc)`, register it in `SCENES`, add `make_cover()`, end with `video_kit.run(HERE, SCENES, make_cover, "<slug>.mp4")`. The cover title is the post's hook.
4. **Review with stills**: `--stills` writes the cover plus each scene at 35% and 95% of its length to `video/stills/`, with no encoding and no TTS. Paste them into one contact sheet and look at every scene at once. Fix overlaps, empty stretches (a scene whose middle stays empty for seconds) and text near the caption band.
5. **Render**: the default run generates the voiceover (cached per scene by a narration hash) and times every scene to its clip. `--silent` renders without audio, using a word-count estimate.
6. **QA the mp4**: `ffprobe` (h264 + aac, 1080x1350); extract frames at the narration cue points (`ffmpeg -ss <t> -i video.mp4 -frames:v 1 f.png`) and check that each visual lands with its words, not at the very end of its line. Scan the caption band to confirm the captions are present throughout.
7. **Hand over**: send the mp4 (and `cover.jpg`) to the author after every round, and keep `post.md`'s `video:` line current. On LinkedIn: upload the video natively, set `cover.jpg` as the thumbnail, use the post text as the caption, and keep links out of the post.

## Revision Loop

- **Snapshot-commit before every change** (local commit on `drafts`, message "... (snapshot before <change>)"), so each round can be compared or reverted.
- When the author gives feedback, first **assess each narration sentence**: what job it does, whether it dangles, whether it matches the post and the blog. Report it as a short old → problem → new table.
- Fix the visuals that a narration change affects (cue phrases, on-screen labels) in the same round, then re-render only what changed: TTS is cached per scene.
- After each change, name the matching edit in the post or the blog and ask before applying it. Blog edits go live on merge to `main`.

## Narration Rules

- 6-8 scenes, at most ~28 words each, 130-165 words in total. The default voice reads ~2.5 words/s and each scene adds a 0.4 s pause: 160 words runs to ~63 s. About 60 s is the target, and up to ~67 s is fine when every line earns its place: content beats the clock.
- Every sentence earns its place: it sets up a later payoff, carries one of the post's points, or lands an emotional beat. No dangling references ("too", "those questions") to things the narration never said. Set up what a later scene pays off (a question asked in scene 2 must be posed before it is answered).
- Scene 1 is the hook: tension within the first 3 seconds (a broken expectation, a confession). No "In this video...".
- Spoken English: short sentences, first person, "we" for the team, contractions are fine. No numbers or terms the listener cannot parse without the screen.
- One idea per scene. "First / Second / Third" when the post has a list.
- Same voice rules as the blog: modest, specific, no hype words.

## Visual Rules

- **Format**: 1080x1350 (4:5), 30 fps, H.264 + AAC. The title card is held for 1 s as the first frame, so the feed thumbnail is never black.
- **Layout**: visuals stay above `CONTENT_BOTTOM` (y=1060); captions are centred at `CAPTION_Y` (y=1150). Captions are burned in because LinkedIn autoplays muted. Keep them out of the bottom ~10% of the frame: players (LinkedIn, the Claude app preview) draw their controls bar there and hide anything underneath, which looks like "the subtitles are gone".
- **One concrete metaphor per scene**, animated on its key phrase with `cue(narration, "phrase", default) * speech`. Metaphors that worked: an expected line against a flat real one, with an "AI factory" buzzing with agents; demo cards piling up at a "decide" gate; a ladder flattening while "Easy. Ship it!" outshouts "it depends…"; a team network whose links fade as each person gets their own screen; a sprint report full of ticks with the three losses greyed out below; a gains/costs balance settling level.
- **On-screen text adds to the captions instead of repeating them**: a header, labels, at most ~8 words of extra text per scene, preferably his words.
- **Wayfinding**: reuse the post's emoji (the post uses them as item markers) as scene headers with `paste_emoji`, so the video, the post and the blog look like one system.
- **Brand**: palette from the kit (`BG`, `ORANGE`, `TEAL`, `VIOLET`, `WHITE`, `MUTED`), fonts Outfit Bold (`HEAD`), Work Sans (`BODY`) and a monospace (`mono`). The blog feature image is the cover background and the blurred end-card background.
- **End card**: the post's title, the balanced closing visual, "Read the full story" with what the blog adds, and the blog address as a button. The address is on-screen text, not a link, so it does not break the "no link in the post" rule.
- **Fit text**: measure with `d.textlength` and shrink long titles; nothing within 50 px of the frame edges.

## Gotchas

- An overlay layer **replaces** pixels instead of blending them: a shape or text drawn with alpha 0 erases what is underneath (an invisible card once erased the question behind it), and two semi-transparent items in one layer do not blend. `text_c` skips zero-alpha text; guard shapes with `if a > 0`, and do not cross-fade two labels in the same spot at the same time.
- Colour emoji need Apple Color Emoji (Mac) or Noto Color Emoji (Linux); `paste_emoji` draws nothing when neither is installed, so every scene must still read without them.
- The bundled fonts lack some glyphs (✓, ↑): draw them (`check_mark`) or avoid them. "→" and "…" work.
- Every animated value must be a pure function of `t`. Random layouts use a fixed seed (`random.Random(11)`), or they jump between frames.
- Rendering is ~1 min for a 60 s video on a Mac. Use `--stills` for iteration, not full renders.
- TTS is cached per scene: editing one narration regenerates one clip; `--regen` regenerates all of them.
- Do not use `rm -f $VAR/*` in review commands: the sandbox blocks it. Write samples to a fresh folder instead.
