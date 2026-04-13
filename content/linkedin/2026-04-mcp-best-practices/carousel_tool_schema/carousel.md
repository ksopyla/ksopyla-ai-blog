---
title: "Your Tool Schema Is Your Agent's Prompt — carousel"
date: 2026-04-02
platform: linkedin
asset_type: carousel
status: published
related_blog_post: "posts/mcp_best_practices"
---

Angle: Practical framework for writing MCP tool definitions that actually help agents. Covers tool names, descriptions, arguments, and error messages. The key insight: these are not documentation, they are prompts. Designed as a reference people can save and revisit when building their own MCP servers.

Template: purple cover + purple slides (Torchenstein brand)


## Slide 1 — cover

Headline: Your Tool Schema Is Your Agent's Prompt


## Slide 2

Headline: Tool name: make it long and descriptive

Supporting copy: research_crypto_project tells the model the domain, action, and scope instantly. analyze or run tells it nothing. A good name sets context before the model reads the description.


## Slide 3

Headline: Description: write a mini-contract

Supporting copy: State the intent: "produce a structured intelligence report." Name the inputs that matter. Describe the return structure. If your description is vague, you lose to a competing tool with a clearer one.


## Slide 4

Headline: Arguments: be explicit, reduce decisions

Supporting copy: project → project_name → crypto_project_name. Use type hints, Literal enums, and defaults. Every ambiguity is a decision the model has to make. Fewer decisions = fewer mistakes.


## Slide 5

Headline: Error messages: give recovery paths

Supporting copy: Bad: {"error": 404}. Good: "Project 'ARBTRUM' not found — did you mean 'ARB' (Arbitrum)?" The agent sees the error and self-corrects on the next turn. Generic errors are dead ends.


## Slide 6

Headline: Bad vs Good in one glance

Supporting copy: Bad: run_analysis(payload: dict) → "Run analysis." Good: research_crypto_project(query: str) → full docstring with intent, input guidance, and return structure.


---
Companion post copy (text to accompany the carousel in LinkedIn feed):

Your MCP tool name, description, arguments, and error messages are not documentation.

They are prompts for the calling agent.

Every character competes for the model's attention and directly affects whether the agent picks your tool, passes correct parameters, and recovers from failures.

Most MCP servers fail hardest on error messages. Returning HTTP 404 or a generic exception gives the agent no signal for what to try next. It gives up or hallucinates a workaround.

Instead: "Project 'ARBTRUM' not found — did you mean 'ARB' (Arbitrum)?"

The agent self-corrects and retries without bothering the user.

The carousel breaks down the four areas where your schema matters most.

What is the worst MCP error message you have seen?

#AIEngineering #AIAgents #MCP
