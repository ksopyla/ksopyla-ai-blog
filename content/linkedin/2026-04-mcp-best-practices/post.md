---
title: "Your 20-tool MCP server is making agents dumber"
date: 2026-04-02
platform: linkedin
status: draft
content_score: 0
related_blog_post: "posts/mcp_best_practices"
---

Your 20-tool MCP server is making every agent that connects to it dumber.

I used to think more tools meant more capability.
Then I saw the benchmarks.

A study tested 6 LLMs across toolsets from 25 to 150 tools. Every model degraded. GPT-4o dropped from 82% to 73%. Grok dropped to a coin-flip 50% when prompts were ambiguous at 100 tools.

The failure mode? Cross-service confusion. The agent picks datadog_get_alerts when it should pick grafana_get_alerts because the descriptions look alike.

GitHub ran into this with their own MCP server. It ships with 40 tools. Their escape hatch? A header that lets you cherry-pick only what you need. Their own data: loading 3-10 tools instead of all 40 gives 60-90% reduction in context window usage.

The team that built the server is telling you: don't load all of it.

I followed the same principle in my agent-patterns-lab. Instead of exposing five endpoint-shaped tools (coin_search, coin_price, coin_news, coin_github, coin_sentiment), I exposed one: research_crypto_project. Behind it, a 5-agent LangGraph pipeline does all the work. The MCP client sees one tool, calls it once, gets a structured report back.

The mental model shift:
→ Stop mirroring REST endpoints as MCP tools
→ Think of MCP tools as macros, not endpoints
→ Chain operations behind the facade
→ A great MCP server has 2-4 tools, max

If you need more surface, split by domain. Two servers, two trust boundaries, four focused capabilities.

How many tools does your MCP server expose today?

#AIEngineering #AIAgents #MCP
