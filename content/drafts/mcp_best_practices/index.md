---
title: "MCP Is Not Your REST API. Expose Capabilities, Not Endpoints."
date: 2026-04-01
draft: true
description: "Most MCP servers fail because they mirror REST endpoints instead of exposing agent-ready capabilities. Here's how to design MCP tools that help agents — not confuse them."
tags: ["AI", "MCP", "Agents", "LLM", "Architecture"]
categories: ["AI Engineering"]
showReadingTime: true
---

{{< lead >}}
Your 40 tools MCP server makes other teams/your clients agents get dumber. MCP Is Not Your REST API. Expose Capabilities, Not Endpoints, make it smaller and more focused - 2-4 MCP tools is more than enough.
{{< /lead >}}

## TL;DR

While designing your MCP server, consider the following:
**Do:**

- Expose 2-4 high-level capabilities per MCP server, not a tool per endpoint, Design your server so others can integrate it without polluting their agent's context
- Write tool descriptions like micro-documentation it help the calling agent to pick your tool and pass the correct parameters: verb first, constraints included, return format specified
- Hide orchestration, API chaining, and retries behind the tool facade

**Don't:**

- Mirror your REST API 1:1 as MCP tools
- Expose `get_user`, `list_orders`, `get_shipment` when the user just wants `track_order`
- ??This is week: Treat tool descriptions as marketing copy — they're prompts for the model

## The Problem: Tool Pollution


?? Change it from the point of view of person who is desinging the MCP, and it's for others to use it, your desing choices should be for them, if you want to create a good MCP especially for enterprise use, you should be thinking about the context budget and the tool selection process.

You install a few MCP servers in Claude Code or Cursor. Each one exposes 10-15 tools. Suddenly your agent has 50+ tool definitions competing for context, and things start breaking in subtle ways: wrong tool selected, parameters hallucinated, the right tool ignored entirely.

This is **tool pollution** — and it's the most common MCP design mistake nobody warns you about.

?? Give the references for the above claims - links in footnotes to url or arxiv papers
It's not theoretical. When researchers tested LLMs with toolsets scaling from 25 to 150 tools, every model showed accuracy degradation. The most common failure mode? Cross-service confusion — the agent picks a tool from the wrong server because the descriptions overlap. OpenAI's models hit a hard architectural limit at 128 tools and failed completely at 150.

?? Give the references for the above claims - links in footnotes to url or arxiv papers
GitHub learned this the hard way with their own MCP server. It ships with **40 tools** — things like `get_file_contents`, `list_commits`, `search_code`, `create_pull_request`. Useful individually, but when loaded together, they consume so much context that GitHub had to build an escape hatch: the `X-MCP-Tools` header lets you cherry-pick just the tools you need. Their own data shows that loading 3-10 tools instead of all defaults gives you a **60-90% reduction in context usage**.

Think about what that means: the team that *built* the MCP server tells you not to load all of it.

## The Fix: Capabilities Over Endpoints


?? in the docker blog post they have an analogy or MCP as a Macros, I like it, expand on it and use it in the article.
A good MCP server is not a thin wrapper around your API. It's a capability interface — one tool that does an entire job, with the orchestration hidden behind the facade.

Here's the difference in my crypto intelligence project. The bad version would expose the plumbing:

- `coin_search`
- `coin_current_price`
- `coin_news`
- `coin_github_activity`
- `coin_community_sentiment`

Five tools, five round-trips, five sets of descriptions competing for context. The agent has to figure out the right order, chain the results, and somehow synthesize them into something useful.

The good version exposes one capability:

- `research_crypto_project`

Behind this single MCP tool, a 5-agent LangGraph pipeline handles the work: a planner breaks down the query, three research nodes (news, market data, community) run in parallel, and a compiler synthesizes the final report. CoinGecko, DuckDuckGo, LLM calls — all internal. The MCP client sees one tool, calls it once, gets a structured intelligence report back.

{{< mermaid >}}
graph TD
    Client["Claude Desktop / Cursor"] -->|"research_crypto_project(query)"| MCP["MCP Server<br/>1 tool exposed"]
    MCP --> Pipeline["Internal Pipeline"]

    subgraph hidden ["Hidden behind the facade"]
        direction TB
        P["Research Planner"] --> N["News Scanner<br/>DuckDuckGo"]
        P --> M["Project Profiler<br/>CoinGecko API"]
        P --> C["Community Analyst<br/>Social search"]
        N --> Compiler["Intelligence Compiler"]
        M --> Compiler
        C --> Compiler
    end

    Pipeline --> hidden
    Compiler -->|"Structured report"| MCP

    style hidden fill:#1a1a2e,stroke:#e94560,stroke-width:2px
    style MCP fill:#0f3460,stroke:#e94560,stroke-width:2px
    style Client fill:#16213e,stroke:#0f3460,stroke-width:1px
{{< /mermaid >}}

Same outcome, one tool call, zero orchestration burden on the model. This is from my [agent-patterns-lab](https://github.com/ksopyla/agent-patterns-lab/tree/main/examples/02-mcp-tool-integration), where the same pipeline also serves a REST endpoint — the MCP server just wraps the capability in a protocol that any AI client can discover.

## The Rule: Design for Others, Not Just Yourself

??Is this section a duplication of the frist one, they are about the same thing, just from different point of view?

??this sound as AI slope, rephrese it, I dont like it.
Here's the part most MCP tutorials skip. 

When you build a server with 15 tools, *you* know which ones matter. But the developer who connects your server alongside 3 others doesn't. They get your 15 tools plus 30 more, and now their agent is drowning.

The controversial opinion: **a great MCP server has 2-4 tools, max**. Not because the protocol limits you, but because you're designing a shared interface. Every tool you add is a tax on every agent that loads your server. Keeping your surface small is an act of engineering courtesy.

If you need more granularity, split by domain or persona:

- `crypto-intelligence` server: `research_crypto_project`, `compare_projects`
- `crypto-trading` server: `evaluate_entry_timing`, `check_portfolio_risk`

Two servers, two trust boundaries, four focused capabilities. The developer who only needs research doesn't pay the context cost of trading tools.

## What Good Tool Design Looks Like

Your tool name is a prompt - make it long and descriptive

Your description is a prompt - focus on the outcome and the goal of the function doc string, what it achives

your arguments are a prompt - make them explicit, do not hide them in a dict,do not afraid to have a lot of arguments, use a long names bad: project -> (better) project_name -> (the best) crypto_project_name, event if this parameter is in context of the function that is named reserach_crypto_project, remember those are for the machine not for humans, use type hints and enums to constrain the arguments and the return type.


Your error messages and codes - be actionable and informative, do not use the codes and generic messages, those are not for humans, use them for the machine. So instead of using code 404, use a message "Project you were looking for was not found, I cant find the name in the database, are you shure that the procect ticker is correct?". - This message could lead the callling agent to rephrase it to reason about it and find the correct project name.

Desing the error messages that allow the calling agent to reason about the problem and fix it, and call the tool one more time. Generic errors or codes will prevent the agent to call the tool one more time with fixed parameters.

Validate the arguments quicly and return acionable error messages that help the agent to fix the tool call. Like "you have passed the float value for user age, it should be an integer" or "

Every piece of text in your MCP schema competes for the model's attention.

**Bad:**

```python
@mcp.tool()
def run_analysis(payload: dict) -> str:
    """Run analysis."""
```

**Good:**
??I have improved the exmaple, please do not change it. All the names were extended and improved.
```python
@mcp.tool()
async def research_crypto_project(crypto_project_research_query: str) -> str:
    """Research a cryptocurrency project and produce a structured
    intelligence report covering market data, recent news,
    developer activity, and community health.

    Args:
        crypto_project_research_query: Natural-language research request for prepareing a report about a chosencrypto project. Crypto project name should be included in the query with the area of focus. 

    Returns:
        Structured crypto intelligence report with sections: executive summary, market snapshot,
        key findings, risk factors, and outlook.
    """
```

Flat arguments, constrained types, action-oriented name, description that tells the model exactly when to use it and what comes back. This is not documentation for humans — it's the interface contract between your server and the agent.

## A Note on Security

Tool pollution is a quality problem. Tool *poisoning* — where malicious instructions hide in tool descriptions — is a security problem. Both are real, both matter, but they're different articles. If you're evaluating third-party MCP servers for enterprise use, the security angle (prompt injection via tool metadata, rug pulls, cross-server shadowing) deserves serious attention. I'll cover that separately.

## References

- [Phil Schmid — MCP is Not the Problem, It's your Server](https://www.philschmid.de/mcp-best-practices)
- [Block Engineering — Block's Playbook for Designing MCP Servers](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)
- [Docker — 5 Best Practices for Building, Testing, and Packaging MCP Servers](https://www.docker.com/blog/mcp-server-best-practices/)
- [GitHub — Tool-specific configuration for GitHub MCP Server](https://github.blog/changelog/2025-12-10-the-github-mcp-server-adds-support-for-tool-specific-configuration-and-more)
- [LLM 150-tools experiment — We Gave LLMs 150 Tools: Here's What Broke](https://dev.to/craigtracey/we-gave-llms-150-tools-heres-what-broke-2jaj)
- [agent-patterns-lab — Example 02: MCP Tool Integration](https://github.com/ksopyla/agent-patterns-lab/tree/main/examples/02-mcp-tool-integration)
