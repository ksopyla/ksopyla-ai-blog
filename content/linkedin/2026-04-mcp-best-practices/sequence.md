---
title: "2-week LinkedIn sequence for MCP best practices article"
date: 2026-04-02
platform: linkedin
asset_type: sequence
status: draft
related_blog_post: "posts/mcp_best_practices"
---

## 2-Week Sequence

Goal: turn one article into repeated native LinkedIn touchpoints instead of a single blog announcement.

Cadence note: if one post gets unusual traction, delay the next post by 1-2 days and keep replying to comments while momentum lasts.

### Day 1
- Format: Text post
- Core angle: Contrarian thesis — tool pollution makes agents dumber
- Hook: Your 20-tool MCP server is making every agent that connects to it dumber.
- Purpose: Start debate and attract MCP builders who feel the pain of tool overload.
- CTA / question: How many tools does your MCP server expose today?
- Notes: Use `post.md`. Do not lead with the blog link. The benchmark numbers (87% → 77%, GitHub's 60-90% context reduction) carry the credibility.

### Day 3
- Format: Carousel
- Core angle: REST endpoints vs MCP capabilities — old model vs new model
- Hook: MCP Is Not Your REST API.
- Purpose: Create a saveable framework asset that people can share with their team.
- CTA / question: Which slide resonates most with what you see in your own stack?
- Notes: Use `carousel_rest_vs_capabilities.md`. Slide 1 must be visually bold and readable on mobile.

### Day 6
- Format: Text post
- Core angle: GitHub's escape hatch — even the builders say "don't load all of it"
- Hook: GitHub ships 40 MCP tools. Their own docs tell you: don't load all of them.
- Purpose: Use a trusted name (GitHub) to reinforce the thesis with concrete evidence.
- CTA / question: Have you tried the X-MCP-Tools header? What did you keep vs drop?
- Notes: Mention the 60-90% context reduction stat. Reference Block's evolution from 30+ tools to 2. Lightly link the blog post here if engagement on Day 1 and Day 3 was strong.

### Day 9
- Format: Carousel
- Core angle: Tool schema as agent prompt — names, descriptions, args, errors
- Hook: Your tool name, description, and error messages are not docs — they're prompts.
- Purpose: Shift from "how many tools" to "how good are your tool definitions." Practical and saveable.
- CTA / question: What is the worst MCP error message you have seen?
- Notes: Use `carousel_tool_schema_as_prompt.md`. The bad vs good code comparison on slide 6 is the most shareable frame.

### Day 12
- Format: Text post
- Core angle: The controversial rule — 2-4 tools max per MCP server
- Hook: A great MCP server has 2-4 tools. Controversial? Maybe. But every tool you add taxes every agent that loads you.
- Purpose: End the sequence with the strongest opinion and invite pushback from experienced builders.
- CTA / question: What is the right number of tools per MCP server? Is there a number where you draw the line?
- Notes: Mention the domain-split pattern (crypto-intelligence vs crypto-trading). This is the best place to link the full article for anyone who wants the complete argument.

## Packaging Logic

- Day 1 earns attention with tension and benchmark data.
- Day 3 turns the article into a native framework people can save and repost.
- Day 6 uses social proof (GitHub, Block) to reinforce the thesis for skeptics.
- Day 9 shifts to the practical "how to write good tools" angle — different enough to re-engage.
- Day 12 closes with the strongest opinion and invites the strongest discussion.

## Optional Variations

- If the Day 1 post performs unusually well, add a short follow-up comment with one extra insight (e.g., the Block Linear MCP story) instead of posting again too quickly.
- If the REST vs Capabilities carousel gets high saves, turn Slide 5 (the evidence slide) into a standalone image post the following week.
- If the "2-4 tools" take generates strong pushback on Day 12, turn it into a longer follow-up post with more nuance: when is it okay to have more, what about dynamic tool loading, etc.
