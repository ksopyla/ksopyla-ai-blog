---
title: "Your Tool Schema Is Your Agent's Prompt — companion post"
date: 2026-04-06
platform: linkedin
status: published
content_score: 0
related_blog_post: "posts/mcp_best_practices"
related_carousel: "carousel_tool_schema_as_prompt.pdf"
---

If your MCP server returns {"error": 404}, your agent is already lost. It has nothing to reason about and nowhere to go.

Now compare this:

"Cannot estimate delivery time — shipment #AWB-8842 is stuck in customs clearance since Apr 2. Use get_shipment_events(tracking_id='AWB-8842') to check the latest customs status, or call estimate_delivery(tracking_id, from_stage='customs') to get an adjusted ETA."

The agent reads that, calls get_shipment_events, sees the customs hold, recalculates with the right parameters, and gives the user an updated ETA. No hallucination. One error message turned a dead end into a self-correcting loop.

This is the part most MCP builders miss. Your tool name, description, arguments, and errors are not documentation. They are prompts. The agent reads every character and uses it to decide whether to call your tool, what parameters to pass, and how to recover when things break.

The same principle runs through the entire schema:

→ Tool name: track_shipment_status beats search — the model knows the domain before it reads the description
→ Description: write a mini-contract — intent, inputs, and return structure in one paragraph
→ Arguments: tracking_id beats query: dict — every ambiguity is a decision the model can get wrong
→ Errors: return recovery paths, not status codes — tell the agent what to try next

I put together a visual breakdown of these four areas (carousel attached 👇).


#AIEngineering #AIAgents #MCP
