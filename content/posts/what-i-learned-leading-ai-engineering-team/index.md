---
title: "What I learned leading an AI engineering team"
date: 2026-07-24
draft: false
description: "Stakeholder pressure, AI coding tools, and a team that still needs judgment. Lessons from building my own AI engineering team: 1:1s, ADRs, co-owned architecture, shared skills, and what code review is for now."
tags: ["AI Engineering", "AI Leadership", "Software Design", "Skills"]
categories: ["Columns"]
featureImage: "feature_ai_engineering_team_learnings.png"
featureAlt: "Abstract digital art of human silhouettes connected by luminous data streams into a shared architectural blueprint, warm oranges merging into deep teals and blues"
showReadingTime: true
icon: "flask"
---

{{< lead >}}
In a year where stakeholders want demos in three hours and tool vendors sell "10x engineers," I learned that the job is still context, judgment, and human process — just with agents amplifying whatever you already have.
{{< /lead >}}

## TL;DR

**What you will learn:**

- Why AI coding speed without engineering discipline leaves teams overwhelmed, not "10x"
- Why 1:1s, ADRs/RFCs, and co-owned architecture matter more once agents enter the loop
- How shared skills compound team knowledge — and why they cannot replace architectural decisions
- Why mechanical code review should be automated, and human review should protect intent
- The operating stack I use: judgment → ADR → review → skill

Most of 2025 and early 2026 felt like living inside someone else's pitch deck. Stakeholders wanted agents, copilots, and "AI-native delivery" on timelines that treated engineering judgment as optional. Vendors shipped coding tools that looked like magic in a conference booth. And I started hearing a question from engineers that bothered me more than the hype itself:

*Why do leaders trust the companies selling AI coding tools more than the judgment of their own teams?*

I lead AI R&D engineering teams by day. I also ship with agents in my own repos by night. Properly used, AI really does speed up development. The part people undersell is the second-order cost: the pace of code change rises faster than the team's ability to stay oriented. Without engineering discipline and human process, people do not feel "10x." They feel overwhelmed, replaceable, and quietly frustrated.

What kept my team sane was not a new framework vendor. It was a handful of practices I already half-knew, applied more deliberately once agents entered the loop.

Something usually starts as a hard call in a 1:1, gets codified into an ADR once the trade-off is settled, gets enforced while the team learns the new shape, and finally automates into a skill once the execution is mechanical. Recognizing where a discipline currently sits — and where it is heading next — is most of the operating model.

## Lesson 1: My job is context, constraints, and judgment

People do their best work with a clear vision, constrained scope, and explicit rules — and with someone watching the trajectory who will intervene before the work drifts.

That sounds obvious. Under AI hype it is not. The pressure is to remove friction, "let the agents cook," and measure output by volume of merged diffs. The opposite of what actually works.

What I have to provide as a lead:

- **Context** the agent will never have: which downstream team will break, which stakeholder promise is soft, which "temporary" design is already load-bearing
- **Constraints** that make autonomy useful: what is in scope this quarter, what is explicitly out, which interfaces are frozen
- **Judgment** when the data is incomplete: ship this, pause that, push back on the demo date

Engineers do not need me to type faster than Cursor. They need to know the frame is real, and that someone will help them stay inside it when the prompt-driven path looks easier.

## Lesson 2: 1:1s became one of the most important practices of 2026

This is the lesson I did not expect to rank this high.

Agents ship features. They do not tell you when an engineer is bored, stuck, growing into the next role, burning out, or about to quit. They do not know which conversation to have before a re-org leaks. They do not absorb hard news on behalf of a relationship.

1:1s are how I keep track of the spirit of the team. Not as psychotherapy. As a place to be transparent, listen for what is broken in the system, help people grow through setbacks, and rebuild trust when the delivery pressure gets dishonest.

Failure modes I keep correcting for:

1. **Status meetings dressed as 1:1s.** Status lives in Jira. An agent can pull it. Use the half-hour for the things only humans can do.
2. **Empathy with no movement.** People want to be heard *and* to leave with a next step. The relationship is what makes the movement possible.

The temptation right now is to outsource the 1:1 to a skill — "summarize team status, generate an agenda." Agents can help you prepare. They cannot replace the conversation. The product of a good 1:1 is not notes. It is a relationship that can carry hard news.

## Lesson 3: ADRs and RFCs are the shared brain — skills cannot replace them

When you build capabilities other teams will integrate with, you need a shared understanding of vision and rules that survives Slack, re-orgs, and prompt drift. That is what ADRs and RFCs are for.

An ADR is dated, immutable, and explains a single decision. New decisions supersede old ones; you do not edit history. An RFC is the debate before the decision hardens. Skills tell the agent *how* to execute. ADRs tell humans and agents *why this stack and not that one*.

You cannot put the real architectural rationale in a Cursor skill and expect it to hold. Skills are for repeatable execution. They go stale when strategy moves. ADRs are for expensive-to-undo choices.

Examples that belong in an ADR or RFC on an AI engineering team:

- How we structure the agentic solution: which agent owns orchestration, which ones are specialists, where human approval sits in the loop
- How authorization works: role-based checks versus policy-based decisions, and where each is enforced
- How we migrate from an old schema to a new one: dual-write window, rollback path, who owns the cutover
- Which integration surface we expose to other teams, and what we refuse to support

Why this matters more now: when an agent proposes a "simpler" path that quietly undoes one of those decisions, the ADR is often the only thing standing between you and a bad weekend. The agent will follow the rationale if you wrote it down. It will refactor against you if you did not.

Failure modes:

1. **No ADRs.** The decision happens in Slack, or in a stakeholder meeting under pressure. The rationale evaporates. The agent and the new hire re-litigate it next quarter.
2. **ADRs that read like marketing.** "We chose X because it is a leading platform" teaches nobody. Write the trade-off you accepted, the option you rejected, and the conditions that would force a revisit — for example, "we picked policy-based auth because role explosion was already hurting us; revisit if a simpler product surface appears."
3. **Treating every implementation choice as an ADR.** Renaming a helper or swapping a library in one service is usually just a PR. Choosing the migration strategy for a shared schema that three teams depend on is an ADR. If undoing it costs a week or more of coordination, write it down.

## Lesson 4: Architecture only speeds you up if the team owns it

A well-documented, maintained architecture is the real multiplier. It is the blueprint. With a clear blueprint, less communication overhead is needed — the team can act without waiting for me to unblock every decision.

The caveat I learned the hard way: architecture you invent alone and drop on the team does not accelerate anything. It becomes another document nobody feels responsible for. The architecture has to be developed *with* the team. People need to feel it is theirs. They need to be in the decision-making process, not just the implementation lane.

The same failure shows up when an omnipotent architect designs the system for the team without involving them. On paper the diagrams look clean. In practice, the small details that person missed — the ugly edge case in production data, the downstream team's real latency budget, the auth quirk nobody put in the slide deck — are often the difference between a system that ships and one that collapses under first real traffic. Those details usually live in the heads of the people who will build and operate the thing. Leave them out of the design room and you pay for it later.

Co-design is slower at the start. Leaders often dislike that. They want results fast, and architecture work does not look like velocity on a board. My experience is the opposite on any horizon past the first MVP: time spent on a shared architecture pays off months and years later, in fewer rewrites, fewer "why did we do it this way?" debates, and a team that can move without waiting for permission.

Agents amplify this difference. An architecture the team owns becomes shared language the agent can follow. An architecture that exists only in one person's head becomes a stream of contradictory prompts.

## Lesson 5: Shared skills are how the team compounds what it learns

This is not a guide to writing skills. It is what changed when we stopped treating useful agent workflows as private tricks.

If someone finds a good pattern — an AWS debugging skill that connects logs, metrics, and recent deploys to find a root cause; a skill for integrating with an external service the same safe way every time; a PR format; a documentation generation process — they should codify it and put it in a shared repository. Then the team improves it step by step, finds new use cases, and kills the ones that go stale.

What I care about is not the skill file format. It is the effect on the team:

- Knowledge stops living in one person's chat history
- A junior engineer can run the same debugging loop a senior already refined
- Process stops being "ask the person who figured it out last month"
- When someone leaves or rotates, the hard-won workflow does not leave with them

The practical rule I use: if the team has already agreed on *what* to do, and the remaining work is making the *how* consistent, a shared skill is the right home. If the team is still arguing about *what*, that belongs in an RFC or ADR first. Skills amplify alignment. They do not create it.

I wrote earlier about building an [engineering-manager mission control](/posts/engineering-manager-mission-control/) with Cursor skills and MCP. The same lesson applies at team scale: skills compound only when they are shared, reviewed, and pruned — not when each engineer keeps a private stash of prompts that never meet.

Public references like [Matt Pocock's skills repo](https://github.com/mattpocock/skills) are useful as examples of execution patterns. Steal shapes, not cargo cult. The value is your team's version of the same idea.

## Lesson 6: Code review cannot carry the architecture anymore

My opinion has shifted here.

In the past, code review was where the team learned the architecture, enforced practices, and caught bugs early. That still matters — but the volume and shape of AI-generated diffs changed the economics. Reviewing every line of agent-produced code the old way is close to impossible if the team is actually using the tools.

My current take: a large part of mechanical review can and should be automated — lint, tests, security scanners, style, known smells, maybe even an agent doing a first pass against the ADR set. What humans should still do is the expensive check: does this diff express *intent* the rest of the team will recognize a year from now?

The reviewer's remaining questions:

- Did the agent invent a new noun for something we already named?
- Did a deep module grow a wide, leaky interface?
- Is there an edge case from a customer escalation or a downstream contract that no prompt contained?
- Is this PR smuggling a decision that should have been an ADR?

If two reviewers are debating an architectural fork in PR comments, pause the PR and write the ADR.

This is why lessons 3 and 4 matter more than they used to. When code review can no longer be the primary teaching surface for architecture, RFCs, ADRs, and a co-owned blueprint have to carry that load upstream. Otherwise the team reviews forever and still drifts.

## Where the disciplines live

These lessons sit on a simple stack. Frequency drops as human judgment rises:

```
                  Frequency       Judgment
Skills        ▇▇▇▇▇▇▇▇         ▁▁
ADRs / RFCs   ▇▇▇▇             ▇▇▇▇▇▇
Code review   ▇▇▇▇▇            ▇▇▇▇▇
1:1s          ▇▇               ▇▇▇▇▇▇▇▇
```

Putting a discipline in the wrong layer is how it goes stale. Strategy in a skill. Architecture only in PR comments. Team health only in Slack reactions.

The useful direction of travel is still:

> judgment → architecture → enforcement → automation
>
> 1:1 → ADR / RFC → code review → skill

## What changes when this works

The payoff I care about is not a prettier process diagram. It is what happens to the team:

- They start acting as one brain, not a collection of individuals with incompatible private models of the system
- Willingness to help each other goes up, because the vision and rules are shared instead of negotiated per ticket
- Cooperation moves up a level: people seek each other out as sparring partners to challenge assumptions before the code hardens
- The team handles complex problems and delivery pressure better, because the hard decisions already have a place to live
- And selfishly, this helps me too: I trust their judgment more, and I can delegate with more confidence

Agents amplify whatever model you already have. Clear fundamentals make you faster. Fuzzy fundamentals make the fuzziness ship.

## Limits

This is what worked on my teams. It is one shape, not the shape.

A two-person team does not need ADRs as a separate layer; the shared head and the codebase are enough. A regulated organization may need audit trails, model cards, and compliance docs this framing collapses into ADRs. A research-heavy team may put more weight on experiment logs than on product RFCs.

I am writing from product and applied AI engineering, not from safety-critical systems. Treat the stack as a diagnostic, not a checklist.

The interesting question is not whether this exact split survives the next tooling wave. It is whether your team has *any* explicit answer to: where does our engineering discipline live now that agents read the repo too?

## Takeaway

AI did not make engineering leadership easier. It made the cost of weak leadership visible faster.

If your team feels overwhelmed while the demos look impressive, the missing piece is probably not another coding tool. It is a shared brain: hard calls that leave the 1:1 and become decisions, decisions that leave Slack and become ADRs, architecture the team actually owns, and skills that turn one person's win into the team's default.

Build that, and the agents make you faster. Skip it, and they only help you ship confusion at higher velocity.

## References

1. Pocock, M. (2026). [**skills**](https://github.com/mattpocock/skills). GitHub repository — composable agent skills for engineering workflows.
2. Sopyla, K. (Apr 2026). [**How I Built an Engineering Manager Mission Control with Cursor, MCP, and AI Skills**](https://ai.ksopyla.com/posts/engineering-manager-mission-control/). ai.ksopyla.com.
3. Ousterhout, J. (2018). *A Philosophy of Software Design*. Yaknyam Press.
