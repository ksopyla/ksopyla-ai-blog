---
title: "MCP Is Not Your REST API — carousel"
date: 2026-04-02
platform: linkedin
asset_type: carousel
status: published
related_blog_post: "posts/mcp_best_practices"
---

Angle: The strongest framework from the article. Contrasts the old REST-endpoint-per-tool model with the new capability-as-macro model. Uses benchmark data and real examples (GitHub, Block, Docker) as evidence. Designed to be saveable and shareable.

Template: purple cover + purple slides (Torchenstein brand)


## Slide 1 — cover

Headline: MCP Is Not Your REST API


## Slide 2

Headline: The problem: Tool Pollution

Supporting copy: Every tool you expose competes for context in the agent's prompt. Benchmarks show accuracy drops from 87% to 77% as tools grow from 25 to 150. More tools = dumber agents.


## Slide 3

Headline: The old model: 1 endpoint = 1 tool

Supporting copy: get_user, list_orders, get_shipment — three tools, three round-trips. The agent figures out chaining. This is REST thinking applied to MCP. It does not work.


## Slide 4

Headline: The better model: 1 capability = 1 tool

Supporting copy: track_latest_order(email) — one call. User lookup, order fetch, status check all happen behind the facade. Think macros, not endpoints.


## Slide 5

Headline: The evidence

Supporting copy: GitHub's 40-tool server needed an escape hatch (60-90% context reduction when trimmed). Block collapsed 30+ tools into 2. Docker recommends "macros" after building 100+ servers.


## Slide 6

Headline: The rule: 2-4 tools per server

Supporting copy: If you need more surface, split by domain. crypto-intelligence: research, compare. crypto-trading: timing, risk. Two servers, two trust boundaries, four focused capabilities.


## Slide 7

Headline: How many tools does your MCP server expose?

Supporting copy: The answer matters more than which model you picked.


---
Companion post copy (text to accompany the carousel in LinkedIn feed):

If you still design MCP servers like REST APIs, you are optimizing the wrong abstraction.

I see this pattern constantly: teams take their existing API, wrap each endpoint as an MCP tool, and wonder why agents struggle.

The problem is tool pollution. Every tool definition competes for context in the agent's prompt. Every overlapping description increases the chance of mis-selection.

The fix is simple but uncomfortable: think macros, not endpoints.

One tool. Multiple internal API calls. Structured result.

GitHub, Block, and Docker all learned this the hard way. The carousel breaks down the shift.

Which slide resonates most with what you see in your own stack?

#AIEngineering #AIAgents #MCP
