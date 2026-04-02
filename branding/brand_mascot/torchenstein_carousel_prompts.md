# Torchenstein Carousel Slide Prompts — Reusable Template Library

Generic Midjourney prompts for Prof. Torchenstein in various settings and moods, designed to be reused across any LinkedIn carousel topic. Each prompt maps to a slide purpose from the carousel pattern.

## How To Use

### Reference Setup

1. Upload your Torchenstein reference images to Midjourney.
2. Replace `[CREF_URL]` with your character reference image URL.
3. Replace `[SREF_URL]` with your style reference image URL.
4. All prompts use `--ar 4:5` for LinkedIn portrait format (1080×1350).

### Mix and Match

Pick **one prompt per slide purpose** from the options below. You do not need to use the same setting across all slides — variety keeps the carousel visually interesting. However, running all prompts in the same Midjourney session helps maintain color and style consistency.

### Text Overlay Zones

Every prompt is composed to leave clear space for text:
- **Top 30–35%**: dark gradient or simple background for headline placement
- **Bottom 15%**: clean for footer, branding, or page numbers
- Torchenstein is positioned to the side or lower portion so he does not block the headline

### Consistency Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--ar 4:5` | portrait | LinkedIn carousel optimal mobile format |
| `--cref [CREF_URL]` | character ref | character face/look consistency |
| `--cw 60-80` | character weight | enough likeness without locking the pose |
| `--sref [SREF_URL]` | style ref | palette and art style consistency |
| `--sw 100-150` | style weight | strong style match without over-constraining |
| `--s 250-350` | stylize | push toward artistic rendering |
| `--v 6.1` | model version | best for character + style refs |

### Parameter Block (append to every prompt)

```
--ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

---

## Slide 1 — Cover / Hook

Purpose: Stop the scroll. Bold, confident Torchenstein. Direct eye contact or dramatic pose. The image must feel like an invitation into something important.

### 1A — Lab Cover (confident, arms crossed)

```
A little mad but friendly scientist, happy with a smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands in a dimly lit steampunk laboratory, facing the viewer with a confident smirk and arms crossed. Behind him, old-fashioned computer terminals glow with green and cyan data streams. Tesla coils spark faintly in the corners. The top third of the image is a dark purple-to-black gradient, creating clear space for a headline. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech steampunk AI laboratory aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 1B — Lab Cover (leaning forward, hands on desk)

```
A little mad but friendly scientist, happy with a smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He leans forward on a cluttered workbench, both hands planted on the surface, looking directly at the viewer with a knowing grin as if about to share a secret. Scattered papers, glowing beakers, and a yellow coffee mug on the desk. The top third of the image is dark negative space for a headline. In the background, a retro computer science laboratory with steampunk terminals and dim lighting. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech steampunk AI laboratory aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 1C — Library Cover (holding a book, looking up)

```
A little mad but friendly scientist, happy with a smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands in an old British university library, looking directly at the viewer with a confident raised eyebrow, holding an open book in one hand. Tall wooden bookshelves filled with leather-bound volumes stretch behind him. Warm amber light mixes with cool shadows. The top third of the image is dark for headline text. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, warm academia aesthetic with moody lighting --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 1D — Computer Cover (turning from screen)

```
A little mad but friendly scientist, happy with a smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He sits at a desk with multiple monitors showing code and diagrams, turning toward the viewer with a confident expression and one eyebrow raised, as if interrupted mid-discovery. The monitors cast a blue-cyan glow on his face. The top third of the image is dark for headline space. Background is a dimly lit retro-tech workspace. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

---

## Slide 2 — The Problem / Old Mental Model

Purpose: Visualize what is wrong. Torchenstein looks skeptical, dismissive, or frustrated. He is reacting to something broken, outdated, or misunderstood.

### 2A — Lab (dismissive gesture at broken system)

```
A little mad but friendly scientist with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands to the right of the frame, gesturing dismissively with one hand toward something off-screen to the left. His expression is skeptical, one eyebrow raised, slight frown. Behind him, a dark steampunk laboratory with faint silhouettes of old machines. The top third of the image is dark negative space for a headline. The left side of the frame has space for text or diagram overlay. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech steampunk aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 2B — Computer (facepalm or frustrated look at screen)

```
A little mad but friendly scientist with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He sits at a computer desk, leaning back in his chair with a skeptical, unimpressed expression, arms folded. The monitor in front of him shows a glowing error or a tangled mess of connections. Red and orange warning lights reflect on his face. The top third of the image is dark for headline text. Background is a dimly lit lab workspace. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech aesthetic
```

### 2C — Blackboard (crossing out wrong idea)

```
A little mad but friendly scientist with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands in front of a large blackboard, drawing a big red X over a diagram with chalk. His expression is determined, slightly frustrated. The blackboard shows faint equations and flowcharts being crossed out. He is positioned to the right, leaving the left and top of the frame for text overlay. Warm overhead lighting on the blackboard, dark moody classroom background. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 2D — Library (closing a book with disappointment)

```
A little mad but friendly scientist with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He sits at a wooden library table, closing a thick book with a resigned expression, shaking his head slightly. Stacks of open books surround him. The atmosphere is warm but heavy, as if the answers he found are unsatisfying. The top third of the image is dark for text. Old British university library in the background. dramatic cartoon animation style, bold graphic novel linework, warm chiaroscuro lighting, moody academia aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

---

## Slide 3 — The Solution / New Way of Thinking

Purpose: The reveal. Torchenstein is excited, enlightened, presenting something new. Energy shifts from frustration to enthusiasm.

### 3A — Lab (presenting a glowing creation)

```
A mad scientist, happy with a smile showing his teeth, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands at the bottom-right of the frame, looking up with excitement and pointing upward with one hand. His other hand holds a glowing beaker or flask emitting cyan light. His expression is triumphant and excited. The top half of the image is dark with subtle steampunk laboratory silhouettes, leaving clear space for a headline. Tesla coils spark purple in the deep background. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech steampunk AI laboratory aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 3B — Blackboard (drawing a new diagram with excitement)

```
A mad scientist, happy with a smile showing his teeth, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands at a blackboard, chalk in hand, having just finished drawing a clean new diagram. He turns toward the viewer with an excited grin. The diagram on the board glows faintly with cyan and green chalk lines. He is positioned to the right, the blackboard and top area provide space for text overlay. Warm dramatic lighting from the side. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 3C — Computer (eureka moment at the screen)

```
A mad scientist, happy with a smile showing his teeth, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He sits at a computer desk, both hands raised in a eureka gesture, grinning broadly. The monitors show a successful result — green checkmarks or a clean flowing diagram. Cyan and green light from the screens illuminates his face. The top third is dark for headline text. Background is a retro-tech workspace. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 3D — Workshop (assembling something new)

```
A mad scientist, happy with a smile showing his teeth, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands behind a cluttered workbench, carefully assembling a small glowing device or mechanism. His expression is focused but joyful, like a craftsman completing a masterpiece. The device emits a warm cyan glow. Tools, wires, and components are scattered on the bench. The top third is dark for text. Steampunk laboratory background with warm dramatic lighting. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech steampunk aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

---

## Slide 4 — Deeper Insight / Framework / Supporting Evidence

Purpose: Teaching moment. Torchenstein in a thoughtful, explanatory pose. He is breaking things down, showing structure.

### 4A — Lab (teaching pose, finger raised)

```
A mad scientist, happy with a small smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands at the bottom-center of the frame in a teaching pose, one hand raised with index finger up as if making a key point. His expression is thoughtful and authoritative. Behind him, the lab wall is dark with faint glowing circuit patterns. The top half and sides have ample dark space for text and diagrams. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech steampunk AI laboratory aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 4B — Library (reading and explaining)

```
A mad scientist, happy with a small smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands in an old British university library holding an open book in one hand and gesturing with the other as if explaining a passage. His expression is engaged and articulate. Tall bookshelves and warm amber light in the background. The top third is dark for text. dramatic cartoon animation style, bold graphic novel linework, warm chiaroscuro lighting, moody academia aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 4C — Whiteboard (diagramming a framework)

```
A mad scientist, happy with a small smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands next to a large whiteboard covered with a structured diagram — boxes, arrows, and labels drawn in marker. He holds a marker and points at a specific part of the diagram. His expression is focused and explanatory. He is positioned to the right, leaving the board and top of the frame for text overlay. Bright overhead lighting, clean modern office or classroom background. dramatic cartoon animation style, bold graphic novel linework, high contrast lighting --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 4D — Computer (showing data on screen)

```
A mad scientist, happy with a small smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He sits at a desk with a large monitor, turned slightly toward the viewer while pointing at the screen. The screen shows charts, graphs, or structured data in cyan and green. His expression is calm and explanatory. The top third of the image is dark for headline text. Retro-tech lab workspace background. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

---

## Slide 5 — Practical Advice / Where to Start

Purpose: Supportive and encouraging. Torchenstein as a mentor offering a first step. The mood is warm, approachable, and practical.

### 5A — Coffee break (friendly advice over coffee)

```
A mad scientist, happy with a smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He sits in a cozy corner of his lab, holding a yellow coffee mug, leaning forward with a warm, encouraging expression as if giving friendly advice to a colleague. Steam rises from the mug. A small stack of papers and a notebook sit beside him. The atmosphere is warm and intimate. The top third of the image is dark for text. dramatic cartoon animation style, bold graphic novel linework, warm chiaroscuro lighting, cozy gothic tech aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 5B — Lab (handing something to the viewer)

```
A mad scientist, happy with a smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He extends one hand toward the viewer, palm up, offering a small glowing object or tool, with an encouraging and warm expression. His other hand is on his hip. He is positioned at the bottom-center of the frame. The background is a dark steampunk laboratory. The top half is dark for text. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech steampunk aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 5C — Workbench (showing a simple tool)

```
A mad scientist, happy with a smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands at a clean workbench, holding up a single simple tool or small device with an expression that says "start with this." The bench is uncluttered compared to his usual chaos — just a few carefully laid out components. The mood is practical and focused. The top third is dark for text overlay. Steampunk lab background. dramatic cartoon animation style, bold graphic novel linework, warm chiaroscuro lighting, gothic tech aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 5D — Notebook (writing down a checklist)

```
A mad scientist, happy with a small smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He sits at a desk writing in an open notebook with a pen, looking up at the viewer with an encouraging nod. The notebook shows a short checklist with a few items. A yellow coffee mug sits nearby. Warm focused lighting on the desk. The top third is dark for text. Background is a cozy lab or study. dramatic cartoon animation style, bold graphic novel linework, warm chiaroscuro lighting --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

---

## Slide 6 — The Destination / Vision

Purpose: Visionary and inspiring. Torchenstein looks ahead toward a bright future. The mood shifts from practical to aspirational.

### 6A — Lab (gazing at something magnificent)

```
A mad scientist, happy with a wide smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands at the bottom-right of the frame, gazing upward with wonder and satisfaction at something glowing and magnificent above him — abstract shapes of light and energy representing a completed vision. His expression is proud and inspired. The top half is filled with glowing abstract light and dark space for text. Deep steampunk lab silhouettes in the background. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech steampunk aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 6B — Window (looking out toward the horizon)

```
A mad scientist, happy with a small satisfied smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands in front of a large arched window in his laboratory, looking out toward a distant glowing horizon. His silhouette is backlit by warm golden and cyan light streaming through the window. His posture is calm and contemplative, hands clasped behind his back. The top third is dark for text. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, epic atmospheric aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 6C — Rooftop or balcony (surveying the landscape)

```
A mad scientist, happy with a confident smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands on a rooftop or balcony overlooking a cityscape at twilight, arms slightly spread as if embracing the future. Faint glowing network lines and nodes overlay the city below like a digital nervous system. The sky is deep purple with cyan and orange at the horizon. The top third is dark for text. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, epic futuristic aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

---

## Slide 7 — Closing / CTA / Question

Purpose: Intimate and engaging. Torchenstein invites the viewer into conversation. Open gestures, eye contact, warm energy.

### 7A — Lab (open hand gesture, inviting response)

```
A mad scientist, happy with a warm smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands at the bottom-left of the frame with an open palm gesture toward the viewer, as if asking a genuine question. His expression is curious and inviting. The background is mostly dark with faint steampunk lab silhouettes. The composition is sparse with abundant dark negative space in the top half and right side for text overlay. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech steampunk aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 7B — Coffee (raising mug in a toast)

```
A mad scientist, happy with a friendly smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He holds up a yellow coffee mug in a casual toast toward the viewer, as if saying cheers or inviting the viewer to join. His expression is warm and collegial. He is positioned at the bottom-center. The background is dark with warm ambient lighting and faint lab equipment silhouettes. The top half is dark for text overlay. dramatic cartoon animation style, bold graphic novel linework, warm chiaroscuro lighting, cozy gothic tech aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 7C — Library (leaning on bookshelf, relaxed)

```
A mad scientist, happy with a relaxed smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He leans casually against a tall bookshelf in an old university library, arms gently folded, looking at the viewer with a warm, open expression as if waiting to hear their thoughts. Warm amber light filters through the space. The composition is relaxed and inviting. The top third is dark for text. dramatic cartoon animation style, bold graphic novel linework, warm chiaroscuro lighting, moody academia aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### 7D — Minimal (dark background, spotlight)

```
A mad scientist, happy with a small warm smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands against a nearly black background, lit by a single dramatic spotlight from the side. Both hands are slightly open at waist level in a welcoming gesture. His expression is calm, genuine, and inviting. The composition is very minimal with maximum dark negative space for text on all sides. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, minimal dark composition --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

---

## Bonus — Standalone Setting Prompts

Generic Torchenstein images in specific settings, not tied to any particular slide mood. Useful for filler slides, social posts, or when you need a Torchenstein visual without a specific narrative role.

### Coding at night

```
A mad scientist, happy with a small smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He sits at a desk late at night, typing on a mechanical keyboard. Multiple monitors surround him showing lines of code in green and cyan text. His face is illuminated by the screen glow. An empty yellow coffee mug and crumpled papers sit on the desk. The lab is dark except for the monitor glow and a single desk lamp. The top third is dark for text. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, late night coding aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### Deep thinking (chin on hand)

```
A mad scientist with a thoughtful expression, gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles pushed up on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He sits in a worn leather chair, chin resting on his hand, looking slightly upward in deep thought. His eyes are narrowed with concentration. A notebook with sketches lies open on his knee. Warm moody lighting from a single lamp. The background is dark and out of focus. The top third is dark for text. dramatic cartoon animation style, bold graphic novel linework, warm chiaroscuro lighting, contemplative mood --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### Examining a paper or document

```
A mad scientist, happy with a small smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He holds a printed document or research paper in one hand and gestures with the other as if commenting on what he just read. His expression is engaged and analytical. He is in a retro computer science laboratory. In the background, old-fashioned steampunk computer terminals and wires. The top third is dark for text. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech steampunk aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### Walking with coffee

```
A mad scientist, happy with a smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He walks through a hallway carrying a yellow coffee mug, looking slightly to the side with a cheerful expression. The hallway has gothic architecture with arched doorways and warm light streaming through tall windows. His lab coat flows slightly with movement. The top third is dark for text. dramatic cartoon animation style, bold graphic novel linework, warm chiaroscuro lighting, atmospheric corridor aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### Eating chocolate and coffee (relaxed break)

```
A mad scientist, happy with a smile showing his teeth, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He sits in a cozy corner of his lab, eating a piece of dark chocolate from a small plate while holding a yellow coffee mug. His expression is content and relaxed. Steam rises from the mug. A messy desk with papers is visible behind him. Warm intimate lighting. The top third is dark for text. dramatic cartoon animation style, bold graphic novel linework, warm chiaroscuro lighting, cozy lab break aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### Conference / presentation (on stage)

```
A mad scientist, happy with a confident smile, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He stands on a conference stage behind a podium or lectern, one hand gesturing toward a large screen behind him. The audience area is dark. A spotlight illuminates him. The large screen behind him shows a faint abstract diagram in cyan. The top third is dark for text. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, conference stage dramatic aesthetic --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

### Celebrating a result (arms up)

```
A mad scientist, happy with a wide excited smile showing his teeth, with gravity-defying white-gray hair, a short beard and a prominent moustache, wearing goggles on his forehead. He is wearing a purple lab coat jacket with sleeves rolled up and a green shirt underneath. He throws both arms up in celebration in his steampunk laboratory. Sparks and glowing particles fly around him. His expression is pure triumphant joy. Tesla coils discharge purple energy behind him. The top third is dark for text. dramatic cartoon animation style, bold graphic novel linework, high contrast chiaroscuro lighting, gothic tech steampunk aesthetic, celebratory energy --ar 4:5 --cref [CREF_URL] --cw 70 --sref [SREF_URL] --sw 120 --s 300 --v 6.1
```

---

## Background-Only Prompts (No Character)

For slides where text density is high and Torchenstein would be distracting. Use as a textured background.

### Steampunk lab wall

```
Dark steampunk AI laboratory wall texture, moody purple and charcoal grey tones, faint glowing circuit board patterns and neural network node traces in neon cyan and orange, subtle tesla coil sparks in corners, dramatic chiaroscuro lighting from the left, clean negative space in the center and top half for text overlay, no characters, no people, atmospheric and mysterious, graphic novel style with bold linework --ar 4:5 --s 300 --v 6.1
```

### Library bookshelf

```
Old British university library bookshelf texture, warm amber and deep brown tones, leather-bound books with gold lettering, faint dust motes in warm light beams, dramatic chiaroscuro lighting from above, clean negative space in the top half for text overlay, no characters, no people, atmospheric and scholarly, graphic novel style with bold linework --ar 4:5 --s 300 --v 6.1
```

### Dark gradient with circuit traces

```
Abstract dark background with deep purple and charcoal gradient, faint glowing neural network topology traces in cyan and purple, subtle geometric patterns, minimal and clean composition with maximum negative space for text overlay, no characters, no people, moody and technical, graphic novel style with bold linework --ar 4:5 --s 300 --v 6.1
```

---

## Quick Reference — Slide Purpose to Prompt Mapping

| Slide Purpose | Mood | Best Settings | Recommended |
|---------------|------|---------------|-------------|
| Cover / Hook | Confident, bold, direct | Lab, Computer, Library | 1A, 1B, 1D |
| Problem | Skeptical, dismissive | Lab, Computer, Blackboard | 2A, 2B, 2C |
| Solution | Excited, revealing | Lab, Blackboard, Computer | 3A, 3B, 3C |
| Framework | Thoughtful, teaching | Lab, Library, Whiteboard | 4A, 4B, 4C |
| Advice | Warm, encouraging | Coffee, Lab, Notebook | 5A, 5B, 5D |
| Destination | Visionary, inspired | Lab, Window, Rooftop | 6A, 6B, 6C |
| Closing / CTA | Inviting, open | Lab, Coffee, Minimal | 7A, 7B, 7D |

## Color Reference for Text Overlay

| Element | Color | Hex |
|---------|-------|-----|
| Headline text | White or very light grey | `#F5F5F5` |
| Body text | Light grey | `#D0D0D0` |
| Accent / highlight words | Neon cyan | `#00E5FF` |
| Secondary accent | Neon orange | `#FF6D00` |
| Footer / subtle text | Muted purple-grey | `#9E9EB8` |
| Background fill | Deep charcoal | `#1A1A2E` |
| Brand purple | Electric purple | `#7B2FBE` |
