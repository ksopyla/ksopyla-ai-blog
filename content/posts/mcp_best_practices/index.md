---
title: "MCP Is Not Your REST API. Expose Capabilities, Not Endpoints."
date: 2026-04-01
draft: false
description: "Most MCP servers fail because they mirror REST endpoints instead of exposing agent-ready capabilities. Here's how to design MCP tools that help agents — not confuse them."
tags: ["AI", "MCP", "Agents", "LLM", "Architecture"]
categories: ["AI Engineering"]
featureImage: "feature_mcp_capabilities_not_endpoints.png"
featureAlt: "Abstract digital art showing a chaotic cluster of tools converging into a single clean stream of light, representing tool pollution vs focused capabilities"
showReadingTime: true
---

{{< lead >}}
Your 20-tool MCP server is making every agent that connects to it dumber. Design fewer, smarter tools — 2-4 capabilities is more than enough.
{{< /lead >}}

## TL;DR

**Do:**

- Expose 2-4 high-level capabilities per MCP server — design for the teams who will integrate your server, not just for yourself
- Hide orchestration, API chaining, and retries behind the tool facade — think of MCP tools as macros, not endpoints
- Write tool descriptions as micro-documentation for the calling agent: verb first, constraints included, return format specified

**Don't:**

- Mirror your REST API 1:1 as MCP tools — `get_user`, `list_orders`, `get_shipment` should be one `track_order` tool
- Dump 30+ tools into a single server — you're taxing every agent that loads you
- Return HTTP status codes or generic exceptions — return messages that help the agent reason about what went wrong and retry with better parameters

## The Problem: Tool Pollution

If you're building an MCP server, especially for enterprise use, you need to think about what happens on the other side. Your consumers connect your server alongside 3-5 others. Each tool definition you expose competes for context in their agent's prompt. Every overlapping description increases the chance of mis-selection. Your design choices are not just about your server — they shape the quality of every agent that integrates with you.

This is **tool pollution**: too many tools, too much overlap, degraded tool selection, and wasted context budget. It's the most common MCP design mistake, and it's measurable.

A [benchmark testing 6 LLMs across toolsets from 25 to 150 tools](https://dev.to/craigtracey/we-gave-llms-150-tools-heres-what-broke-2jaj) found that every model showed accuracy degradation as tools increased. Grok 4.1 Fast dropped from 86.7% to 76.7%. GPT-4o fell from 81.7% to 73.3% — and both OpenAI models hit a hard API limit at 128 tools, failing completely at 150. The most common failure mode was cross-service confusion: the agent picks `datadog_get_alerts` when it should pick `grafana_get_alerts` because the descriptions look alike. It gets worse with ambiguous prompts — Grok 4 dropped to a coin-flip 50% accuracy at 100 tools when the user didn't name the service explicitly.

GitHub ran into this with their own MCP server. It ships with [40 tools](https://hub.docker.com/mcp/server/github-official/tools) — `get_file_contents`, `list_commits`, `search_code`, `create_pull_request`, and 36 more. Useful individually, but loaded together they consume so much context that GitHub had to build an escape hatch: the [`X-MCP-Tools` header](https://github.blog/changelog/2025-12-10-the-github-mcp-server-adds-support-for-tool-specific-configuration-and-more) lets you cherry-pick only the tools you need. Their own data shows that loading 3-10 tools instead of all defaults gives **60-90% reduction in context window usage**. The team that built the server is telling you: don't load all of it.

## The Fix: Think Macros, Not Endpoints

The [Docker team](https://www.docker.com/blog/mcp-server-best-practices/) has a useful analogy from their experience building over 100 MCP servers for the Docker MCP Catalog: think of MCP tools like **macros**. Instead of requiring the agent to call multiple tools in sequence, create a single tool that chains multiple endpoint calls behind the scenes. The user says "fetch my invoices" and the agent calls one tool — not three.

This is fundamentally different from REST API design. [Phil Schmid puts it sharply](https://www.philschmid.de/mcp-best-practices): REST principles — composability, discoverability, small endpoints developers combine — work for human developers who read docs once, write a script, debug it, and ship. They don't work for agents. For an agent, discovery is expensive (the schema is in every request), composability means slow multi-step tool chains, and flexibility leads to hallucination. A good REST API is not a good MCP server.

His order tracking example makes it concrete. A bad MCP server exposes `get_user_by_email()`, `list_orders(user_id)`, and `get_order_status(order_id)` — three tools, three round-trips, all intermediate results stored in conversation history. A good MCP server exposes `track_latest_order(email)` — one tool that calls all three internally and returns "Order #12345 shipped via FedEx, arriving Thursday."

I followed the same principle in my [agents patterns lab](https://github.com/ksopyla/agent-patterns-lab/tree/main/examples/02-mcp-tool-integration) where we build set of examples on crypto intelligence project idea. The bad version would expose five endpoint-shaped tools: `coin_search`, `coin_current_price`, `coin_news`, `coin_github_activity`, `coin_community_sentiment`. Five round-trips, five sets of descriptions fighting for context, and the agent has to figure out the chaining order.

The good version exposes one capability: `research_crypto_project`. Behind it, a 5-agent LangGraph pipeline does the work — a planner decomposes the query, three research nodes (news via DuckDuckGo, market data via CoinGecko, community sentiment via social search) run in parallel, and a compiler synthesizes the final report. The MCP client sees one tool, calls it once, gets a structured intelligence report back.

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

This is from my [agent-patterns-lab](https://github.com/ksopyla/agent-patterns-lab/tree/main/examples/02-mcp-tool-integration), where the same pipeline also serves a REST endpoint. The MCP server just wraps the capability in a protocol any AI client can discover. CoinGecko, DuckDuckGo, LLM calls — all internal implementation details, invisible to the caller.

Block saw the same evolution across their 60+ MCP servers. Their [Linear MCP went through three versions](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers): v1 had 30+ tools mirroring GraphQL queries — asking "what issues is bob working on" required 4-6 chained tool calls. v2 consolidated read-only tools into grouped functions like `get_issue_info(issue_id, info_category)`. v3 collapsed everything into two tools: `execute_readonly_query` and `execute_mutation_query`, taking raw GraphQL. What originally took 4+ tool calls became one.

My controversial take: **a great MCP server has 2-4 tools, max**. Not because the protocol limits you, but because every tool you add taxes every agent that loads your server. If you need more surface, split by domain:

- `crypto-intelligence` server: `research_crypto_project`, `compare_projects`
- `crypto-trading` server: `evaluate_entry_timing`, `check_portfolio_risk`

Two servers, two trust boundaries, four focused capabilities. The team that only needs research doesn't pay the context cost of trading tools.

## Your Tool Schema Is Your Agent's Prompt

Your tool name, description, argument names, and error messages are not documentation — they're prompts for the calling agent. Every character competes for the model's attention and directly affects whether the agent picks your tool, passes correct parameters, and recovers from failures.

**Tool name** — make it long and descriptive. A good name sets the context for the entire interaction before the model even reads the description. `research_crypto_project` immediately signals the domain (crypto), the action (research), and the scope (project-level). Compare that with `analyze` or `run` — the model has no context to decide if your tool fits the user's request.

**Description** — focus on what the tool achieves, when to use it, and what the output looks like. Treat the docstring as a mini-contract: state the intent ("produce a structured intelligence report"), name the inputs that matter ("crypto project name should be included in the query"), and describe the return structure ("sections: executive summary, market snapshot, key findings, risk factors, and outlook"). The model uses this text to decide whether to call your tool at all — if the description is vague, you lose to a competing tool with a clearer one.

**Arguments** — make them explicit. Don't hide them in a `dict`. Use long, unambiguous names even if they feel redundant: `project` → `project_name` → `crypto_project_name`. Use type hints, `Literal` enums, and defaults to constrain choices and reduce the decisions the model has to make.

**Error messages** — this is where most MCP servers fail hardest. [Docker's team](https://www.docker.com/blog/mcp-server-best-practices/) puts it well: the agent, not the user, is calling your tool. If you return HTTP 404 or a generic Python exception, the agent has no signal for what to try next and will likely give up or hallucinate a workaround. A good error message gives the agent a concrete recovery path — enough information to fix the parameters and call the tool again.

Instead of a status code, return actionable text:

- "Project not found. The ticker 'ARBTRUM' doesn't match any known project — did you mean 'ARB' (Arbitrum)?"
- "Date range too broad. Maximum span is 90 days. You requested 2024-01-01 to 2025-06-15 (531 days). Try narrowing to a single quarter."
- "Invalid argument type: `user_age` received float 25.5 but expects int. Round to nearest integer and retry."
- "API rate limit exceeded. CoinGecko free tier allows 30 requests/minute. Wait 45 seconds before retrying."

Each of these tells the agent exactly what went wrong and how to fix it. The agent can self-correct and retry without asking the user. Generic errors like `{"error": 404}` or `Exception: request failed` are dead ends — the agent has nothing to reason about.

Validate arguments early and fail fast. Don't let bad input travel through three internal API calls before returning an unhelpful stack trace. Check types, ranges, and required fields at the tool boundary and return a clear message immediately. [Phil Schmid frames it as a rule](https://www.philschmid.de/mcp-best-practices): "Error messages are context too. The agent sees the error as an observation and uses your instruction to self-correct in the next turn."

Block's Goose file-reading tool is a good example of this in practice — when a file exceeds 400KB, instead of silently truncating, it raises a [specific tool error](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers): "File is too large (412KB). Maximum is 400KB. Use shell commands like `head`, `tail`, or `sed -n` to read a subset." The agent recovers and uses a different approach.

**Bad:**

```python
@mcp.tool()
def run_analysis(payload: dict) -> str:
    """Run analysis."""
```

**Good:**

```python
@mcp.tool()
async def research_crypto_project(crypto_project_research_query: str) -> str:
    """Research a cryptocurrency project and produce a structured
    intelligence report covering market data, recent news,
    developer activity, and community health.

    Args:
        crypto_project_research_query: Natural-language research request
            for preparing a report about a chosen crypto project.
            Crypto project name should be included in the query
            with the area of focus.

    Returns:
        Structured crypto intelligence report with sections:
        executive summary, market snapshot, key findings,
        risk factors, and outlook.
    """
```

## A Note on Security

Tool pollution is a quality problem. Tool *poisoning* — where malicious instructions hide in tool descriptions to manipulate agent behavior — is a security problem. Both are real, both matter, but they're different articles. If you're evaluating third-party MCP servers for enterprise use, the security angle (prompt injection via tool metadata, rug pulls, cross-server shadowing) deserves serious attention. I'll cover that separately.

## References

- [Phil Schmid — MCP is Not the Problem, It's your Server](https://www.philschmid.de/mcp-best-practices)
- [Block Engineering — Block's Playbook for Designing MCP Servers](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)
- [Docker — 5 Best Practices for Building, Testing, and Packaging MCP Servers](https://www.docker.com/blog/mcp-server-best-practices/)
- [GitHub — Tool-specific configuration for GitHub MCP Server](https://github.blog/changelog/2025-12-10-the-github-mcp-server-adds-support-for-tool-specific-configuration-and-more)
- [Boundary — We Gave LLMs 150 Tools: Here's What Broke](https://dev.to/craigtracey/we-gave-llms-150-tools-heres-what-broke-2jaj)
- [agent-patterns-lab — Example 02: MCP Tool Integration](https://github.com/ksopyla/agent-patterns-lab/tree/main/examples/02-mcp-tool-integration)
