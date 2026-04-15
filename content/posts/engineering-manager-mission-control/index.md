---
title: "How I Built an Engineering Manager Mission Control with Cursor, MCP, and AI Skills"
date: 2026-04-14
draft: false
description: "I connected my Cursor IDE to Jira, Confluence, GitHub, Azure, and SNYK — not to write code, but to manage engineering teams. Here is the full setup, the skills I built, and what I learned after weeks of using it."
tags: ["AI Agents", "MCP", "AI Engineering", "Engineering Management"]
categories: ["AI Engineering"]
featureImage: "featured_engineering_mission_control.png"
featureAlt: "Stylized mission control cockpit with multiple glowing screens showing Jira boards, code diffs, cloud infrastructure diagrams, and security dashboards, all connected by luminous data streams through a central console"
showReadingTime: true
---

{{< lead >}}
I connected my Cursor IDE to Jira, Confluence, GitHub, Azure, and SNYK — not to write code, but to manage my engineering teams. This post documents the full setup, the skills I built, and the honest lessons from weeks of using it.
{{< /lead >}}

## TL;DR

**What you will learn from this post:**

- How to treat your management knowledge as a codebase the AI can reason about
- A concrete MCP setup for engineering management (Atlassian, GitHub CLI, Azure, SNYK)
- The "problems folder" pattern — a living structure where each management problem accumulates context over time, with a compounding effect
- Six reusable Cursor skills for RFC review, sprint health, roadmaps, architecture docs, documentation quality, and vulnerability triage
- Honest lessons: skills need 80% refinement effort, work on one problem per session to avoid "problem drift," and capturing your own thinking style is the hardest part

## The Mindset Shift

Most of my engineering management work is not engineering. It is context gathering. Figuring out sprint status, reading proposals, checking if a dependent team is on track, preparing data for a leadership conversation. I spend a lot of time in Jira, Confluence, GitHub, cloud resources (Azure, AWS) — and not much of that time feels like good use of my experience.

I have been slowly building a system that helps with this. Not a polished product, not a weekend project I can show off — just a growing set of tools and habits inside Cursor that make the repetitive parts of management faster. I started small, added one piece at a time, and iterated when things did not work.

Before I get into the setup, I want to talk about the shift that made this possible.

I have always wanted to connect all my loosely coupled data sources into one place. Before AI agents, there was no practical way to do it. Now there is.

The realization came gradually. When I started this blog, I set it up with Hugo — a static site generator where all content is written in markdown. Working with it made something click: **markdown is the current exchange format for information** (like JSON is for software development) between humans and AI. It is how agents read, how they write, and how context gets structured.

From there I started using Cursor chat to gather context from Azure documentation for architecture and design decisions. That worked well enough that I connected it to our company Confluence, where the rest of the technical context lived. This greatly sped up my RFC and design reviews — I could cross-reference Azure service documentation with our existing architecture docs in one conversation.

Then I needed to push the compiled information back into Jira epics. And while doing that, I hit a wall: the agent lacked broader company and team context. It could read individual tickets and docs, but it did not understand our team structure, our dependencies, or the history behind our decisions.

That was the moment I realized I needed one place to collect all of this context in a format the AI could actually use. What if I gave the coding agent the same depth of context about my organization that it already has about a codebase? What if I treated my management knowledge — team structures, project dependencies, architecture decisions, delivery history — as a kind of codebase that the agent could read and reason about?

That reframing opened up use cases I had not considered. The agent is fundamentally good at reading, cross-referencing, and summarizing large amounts of structured information. That happens to describe a huge chunk of what engineering managers do every day.

## The Foundation: Organizational Context in Markdown

The first step was writing down what I carry in my head. I created a private repository with markdown files describing my organization:

- **My 2 teams**: team members, skills, roles, what they are good at, who works on what, areas of ownership, reporting structure
- **Dependent teams**: who we collaborate with, our ways of working, how to report bugs or make feature requests
- **Projects**: ours and other teams' projects, project goals, roadmaps, Jira boards, Confluence spaces
- **Dependent projects**: work from other teams we rely on, their timelines and key contacts
- **OKRs and KPIs**: for the team and the whole department
- **Cloud resources**: Azure and AWS subscriptions, resources across dev, staging, and production environments
- **APIs and services**: what exists, what connects to what, which team owns each service
- **Services architecture**: key RFCs and architecture decisions, diagrams in mermaid format, how services connect, where they are deployed, dependencies, monitoring and alerting tools
- **Company services**: HR system with career framework and other shared platforms

I did not write all of this from scratch. Once I connected the MCP servers (next section), I asked the AI to generate the initial markdown files by pulling data from Jira, Confluence, and GitHub. I reviewed and corrected them, but the first draft was surprisingly close. That step alone was useful — seeing my organization described back to me by an AI that had just read our actual project data highlighted gaps I had been ignoring. Documentation that I thought existed did not. Dependencies I assumed were tracked were only in people's heads.

These markdown files are the AI's long-term memory. They live in the repo, get updated as things change, and give every conversation a baseline of organizational knowledge.

## The MCP Connections

The second step was wiring Cursor to the systems where the actual data lives.

**Atlassian MCP server** — connects to Jira and Confluence. This is the most heavily used connection. The agent reads tickets, checks sprint boards, queries epic status, and writes directly to Confluence. That last part matters — it can publish architecture diagrams, documentation updates, and summaries without me copy-pasting between tools.

**GitHub CLI** — I initially connected our company GitHub MCP server, but switched to the CLI instead. It turned out to be more reliable for what I needed: reading PRs, checking CI status, reviewing changes, cross-referencing issues.

**Azure CLI** — for checking resources, deployments, subscriptions, costs, and quotas. When someone proposes a new service or infrastructure change, the agent checks what we already have running, what it costs, and whether we have capacity.

**AWS Cursor plugins** — same idea, for our AWS resources.

**SNYK MCP server** — for dependency vulnerability checks across repositories. Instead of me opening the SNYK dashboard and filtering through noise, the agent checks specific projects and tells me what actually needs attention.

**Python with uv** — the repository has `uv` configured so the agent has a consistent Python environment. When it needs to do data analysis, generate an Excel report for stakeholders, or build a quick one-off tool, it just runs Python. No environment setup needed.

The combination of these connections matters more than any single one. The most unexpectedly powerful setup: linking GitHub and Confluence through the agent. It reviews a design in a GitHub PR, generates mermaid architecture diagrams, and publishes them to Confluence with the mermaid plugin rendering them properly. Our architecture documentation is actually up to date for the first time. I could never maintain that manually.

## The Problems Folder

This was not planned. It emerged from how I naturally work.

I created a `problems/` folder in the repository. Each management problem gets its own subfolder with a markdown file describing the problem, the relevant context, any constraints, and what a good outcome looks like. As I work on a problem, I add more data — links to tickets, notes from conversations, decisions made, results of previous analysis.

The key discipline: deal with one problem at a time and give it as much context as possible.

Here are some of the problems I have worked on. I am sharing these because I think the specific use cases are more useful than a generic description of the system.

**Promotion readiness.** Our HR has a career framework with specific criteria for each level. I built a problem template where I feed in a team member's recent work, and the agent maps it against the framework. It does not decide — but it gives me a structured draft instead of me spending an evening scrolling through six months of Jira tickets trying to remember what someone worked on.

**Delivery speed assessment.** I asked the agent to analyze our sprint data — velocity trends, committed vs completed points, patterns over recent months. Raw velocity numbers are misleading on their own, so the problem file includes context for anomalies: someone was on leave, a ticket was blocked waiting on another team for a week, a wrong initial assignment required reshuffling. The agent factors these in, and the output is something I can bring to a leadership discussion without spending half a day preparing it first.

**Delivery blockers.** I asked the agent to look at where our sprints lose the most time. It pulled ticket histories, compared estimates to actuals, and flagged repeating patterns. The biggest finding: our most common blocker was not external dependencies or unclear requirements. It was PRs sitting in peer review queues. We switched to an AI-assisted PR reviewer after that analysis. That one insight made the entire setup worth the effort.

**Architecture feasibility.** When the team proposes a new approach, I used to rely on my own knowledge of our infrastructure. Now the agent pulls documentation from AWS and Azure, checks what services we already run, looks at comparable architectures in our setup, and gives me a faster feasibility picture. I still make the call, but with better data.

**Estimation validation.** This matters especially for infrastructure work. I am not a DevOps expert. When the team estimates two weeks for a deployment pipeline change, I used to either trust it or challenge it on gut feeling. Now the agent compares the proposed work against previous similar tickets and our current infrastructure. It gives me concrete questions: "the last time we set up a similar pipeline it took 8 story points across 3 sprints, and we already have X and Y configured in Azure — is this estimate accounting for that?" I am not overriding anyone. I am asking better questions.

Over time, something interesting happened. As the problems folder grew, each new problem became easier to work on. Not because the model improved, but because the accumulated context from previous problems kept being relevant. A delivery speed analysis is more useful when the agent already knows about last sprint's blockers. An architecture review is sharper when it has seen three prior reviews in the same domain. There is a real compounding effect.

## The Skills

After a few weeks of repeating the same kinds of requests — review this RFC, check sprint health, help me scope this epic — I started turning the patterns into Cursor skills. A skill is a reusable set of instructions the agent follows consistently.

**RFC Reviewer.** Reads a proposal, evaluates the approach, identifies trade-offs the author might have missed, brainstorms alternative solutions. It does not just summarize — it challenges. Gives me a structured starting point for the review conversation.

**Sprint Health Checker.** Pulls current sprint data from Jira — tickets, status, assignees, blockers — and produces a health summary. Flags risks: tickets that have not moved, blocked items, scope changes mid-sprint.

**Roadmap Builder.** Helps me scope epics: estimate complexity, break down work, check the status of teams we depend on. When building a quarterly roadmap, I feed it proposed epics and it cross-references our dependency map.

**Architecture Doc Reviewer.** Reviews architecture documents, assesses design decisions, generates mermaid diagrams, and publishes results to Confluence. This is the skill that bridges GitHub and Confluence.

**Documentation Quality Checker.** Points at our Confluence spaces and assesses what is outdated, missing, or inconsistent with the current codebase. The first time I ran this, the gap between what we thought was documented and what actually was documented was larger than expected.

**Dependency Vulnerability Checker.** Pulls SNYK data for specific projects and gives me a prioritized list. Does the triage that I used to do manually in the SNYK dashboard.

## What I Learned

I want to be honest about what worked, what did not, and what surprised me.

**Context collection was the easy part.** Connecting the MCP servers and generating the initial markdown files took a few days. The AI did most of the pulling from Jira, Confluence, and GitHub. I just reviewed and corrected. If you are hesitant about the setup effort, this is probably smaller than you think.

**Skills do not work out of the box.** This is the part most people will underestimate. The first version of every skill produced mediocre results. The RFC reviewer was too generic and not aligned with my way of thinking. The sprint checker initially focused only on metrics and story points — I do not personally find that useful — and missed the more important information buried in ticket comments and discussions. It took several rounds of refining instructions, adding examples of good output, and handling edge cases. Building a skill is maybe 20% of the work. Getting it reliable is the other 80%.

**Keep rules files simple and scoped.** Each skill works better with a few (1–3) small rules files, 20–50 lines max, where one of them describes the repository structure with a short explanation of what the agent will find there.

**Work on one problem at a time.** Do not pollute the context. In one chat window, work with one problem only. It is tempting to ask follow-up questions about something else, but I have noticed that leads to "problem drift" — the agent starts mixing context from different problems and the output quality drops. Having everything in markdown files helps here: I can start a new session with fresh context without explaining too much from scratch. This turned out to be a huge win and time saver.

**The compounding effect is real.** The more problems I solve with this system, the more useful the system becomes. Each problem adds context that makes the next related problem easier. This was the biggest positive surprise.

**Capturing your own thinking is the hardest part.** I can describe my org structure. I can describe the problems I face. But describing *how I think* — the way I evaluate trade-offs, the questions I ask during architecture reviews, my communication style, how I write feedback on PRs — that is genuinely difficult. It is the most ambitious part of this system and the one that is furthest from done. That is why I created two meta-skills to help with it.

**You need a self-improvement loop and a meta-learning skill.** The self-improvement skill reads my current chat sessions — the ones where I give the agent feedback, correct its output, add more specific instructions. It extracts my thinking patterns and communication style, then uses those to refine the skill I was using. Over time, each skill gets closer to how I would actually do the work myself.

Separately, I use a meta-learning skill that reviews how all skills relate to each other — checking for overlaps, contradictions, and unclear boundaries. Each skill should have a well-defined scope and responsibility. I noticed, for example, that my software architecture skill overlapped with a software development best practices skill. Agents would load context from both and hit contradicting information. The meta-learning skill caught that and suggested how to separate them cleanly.

## What This Does Not Do

This does not replace management judgment. It does not make decisions for me. It does not handle the human parts — reading a room, knowing when a team needs a push versus space, having the difficult performance conversation. Those stay entirely human and I do not think that should change.

It also does not work without effort. If you expect to install some MCP servers and get a working management copilot tomorrow, you will be disappointed. The setup took days, the refinement took weeks, and the skills are still not finished.

What it actually does: it compresses the context-gathering phase of management. Previously I had to collect context and keep it all in my head before making a decision. Now the agent does the collecting and I focus on the deciding. That makes it much easier to look at the same information from different angles — different perspectives, different priorities, different stakeholders. I understand problems better now because I actually have the full picture. Before this setup, I rarely had enough time to collect everything, so many of my decisions were more gut feeling than data-driven. I did not always realize that at the time.

## Where to Start

If any of this sounds useful, my suggestion is to start small.

1. **One markdown file.** Write down what you carry in your head about your team and projects. Do not try to document everything. Start with the basics.
2. **One MCP connection.** Atlassian MCP for Jira and Confluence gives the most immediate value. Sprint tracking, documentation, project data — all from one connection.
3. **One repeating task as a skill.** Sprint health checks are a good first candidate. The input is structured, the output is clear, and you can validate the results quickly.
4. **One problem in a folder.** Pick a real management problem you are dealing with this week. Give it context. See what happens.

The system is not revolutionary. It is just using a familiar tool for a different purpose. But if you are an engineering manager spending hours each week on context gathering, it might be worth trying. The worst case is that you end up with a well-documented understanding of your own organization — and that has value on its own.
