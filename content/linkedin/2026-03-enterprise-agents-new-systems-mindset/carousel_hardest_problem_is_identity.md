---
title: "The hardest agent problem is not reasoning — it is authorization"
date: 2026-03-22
platform: linkedin
asset_type: carousel
status: draft
related_blog_post: "posts/enterprise-agents-new-systems-mindset"
---

Angle: Everyone obsesses over reasoning, planning, and tool use. The real enterprise blocker is identity and authorization — a boring problem that nobody has solved for dynamic agents. Controversial because it says the "sexy" problems are not the hard ones.

Template: purple cover + purple slides (Torchenstein brand)

## Slide 1 — cover

Headline: The hardest agent problem is not

Highlighted keyword: reasoning

Designer note: White bold headline "The hardest agent problem is not" with "reasoning" in yellow highlight, crossed out or styled as the wrong answer. Cover template.

## Slide 2

Headline: Everyone is optimizing for smarter agents.

Supporting copy: Better planning. Stronger reasoning. More tools. Fancier orchestration graphs.

Designer note: Yellow text. This is the "what everyone focuses on" slide.

## Slide 3

Headline: Meanwhile, nobody has solved this:

Supporting copy: Who is the agent acting for?
What scopes were delegated?
Which tools can it call transitively?
What data can cross tenant boundaries?
Who is accountable when it acts wrong?

Designer note: White text, question format. This is the "uncomfortable gap" slide — hit hard.

## Slide 4

Headline: Classic RBAC was built for humans and fixed services.

Supporting copy: Agents break every assumption:
- created dynamically
- responsibilities shift via prompt changes
- same agent, different delegations
- permissions valid yesterday, unsafe today

Designer note: Yellow headline, white bullets. The "why old tools don't work" slide.

## Slide 5

Headline: Start with one question before your next agent deployment.

Supporting copy: "If this agent acts under a different delegation tomorrow, do our permissions still hold?" If you can't answer that, your agent system is fragile — no matter how smart the model.

Designer note: Yellow headline, white copy. Actionable first step.

## Slide 6

Headline: The control plane matters more than the model.

Supporting copy: Identity. Delegation chains. Budget enforcement. Audit trails. Without these, agent autonomy is a liability, not a feature.

Designer note: Yellow headline. Vision / destination slide.

## Slide 7

Headline: How are you handling agent authorization today?

Supporting copy: Static roles? Per-request tokens? Nothing yet? That answer probably matters more than which base model you picked.

Designer note: White headline, yellow highlight on "Nothing yet?" — closing CTA.

---
Companion post copy (text to accompany the carousel in LinkedIn feed):

The biggest enterprise agent problem is not reasoning.
It is authorization.

I keep seeing teams invest months into better planning, smarter tool use, fancier orchestration graphs.

Then they hit a wall nobody was thinking about:
→ Who is this agent acting for right now?
→ What scopes were actually delegated?
→ What happens when a prompt change shifts the agent's effective role?
→ Who is accountable when it does something wrong?

Classic RBAC was designed for humans and fixed services. Agents break every assumption. They are created dynamically. Their responsibilities change through prompts. The same agent can act under different delegations in the same hour.

The hard truth: without an explicit control plane for identity, delegation, and auditability, the rest of your agent architecture is fragile. No matter how strong the model.

How are you handling agent authorization in your stack today?

#AIEngineering #AIAgents #MultiAgentSystems
