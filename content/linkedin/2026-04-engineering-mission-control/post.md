---
title: "Engineering Manager Mission Control with AI and MCP"
date: 2026-04-13
platform: linkedin
status: draft
content_score: 0
related_blog_post: ""
---

I wired my Cursor IDE to Jira, Confluence, GitHub, Azure, and SNYK — not to write code, but to manage my engineering teams.

Here is why.

As an engineering manager I spend most of my time gathering context. Checking sprint status across Jira boards. Reading RFCs that touch services I haven't looked at in weeks. Figuring out if a dependent team is on track by digging through their epics. Writing architecture docs that nobody updates after the first draft.

I realized I already have a tool that is great at reading, cross-referencing, and summarizing large amounts of context. I just never thought to use it for management work.

So I created a repository with markdown files describing my org — teams, projects, dependencies, APIs — and connected MCP servers to our actual systems. Atlassian MCP for Jira and Confluence. GitHub CLI for code and PRs. Azure CLI for deployments, costs, and quotas. SNYK for dependency vulnerabilities. Python with uv configured so the agent can spin up quick scripts for data analysis or generate Excel reports for stakeholders.

Then I built cursor skills — reusable instructions the agent follows consistently:
→ RFC reviewer that actually brainstorms alternatives, not just summarizes
→ Sprint health checker that flags risks I would have caught too late
→ Roadmap builder that scopes epics and checks cross-team dependencies
→ Architecture doc reviewer that generates mermaid diagrams and publishes them directly to Confluence

A few observations and wins so far:

Architecture docs that stay alive.
The agent reviews a design in GitHub, generates mermaid diagrams, and publishes them straight to Confluence with proper rendering. Our architecture docs are actually up to date now. Previously this work was my last priority, and I postponed it when I would have time. Now its much easier to keep the docs up to date. (Is not perfect, but much better than before)


Hidden dependency delay.
It caught something I would have missed entirely. A comment in one of our Jira issues mentioned another team's ticket. That ticket sat in an epic whose scope had grown and target date quietly slipped. Nothing was linked — just one buried comment. The agent traced it, checked the epic, and flagged the delay before it hit our roadmap.

Delivery blockers surfaced.
I asked it to analyze where our sprints lose time. It pulled ticket histories, compared estimates to actuals, and flagged patterns. Turns out our most common blocker was waiting for PR reviews from peer developers. We switched to an AI-assisted PR reviewer. That one honest analysis opens my eyes to the real problems we have. Previously I was operating in old mindset that this is how it should be. AI acted as challenger and gave me a new perspective.



I am not building anything revolutionary here. I just pointed the same tool everyone uses for coding at a different problem. The setup took a few days and I still working on it. This is not a quick win, but a long term investment.

The time it saves me every week is significant.

If you manage an engineering team, try connecting your project tools via MCP. Start with Jira + Confluence. You will be surprised how much context-gathering work just disappears.

#AIEngineering #AIAgents #MCP
