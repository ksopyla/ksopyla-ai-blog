---
title: "Systems thinkers: how to spot them, grow them, and become one"
date: 2026-11-17
draft: false
description: "AI widened what one engineer can build. Notes on why systems thinkers matter most now, how to spot and grow them, and how to become one."
tags: ["AI Leadership", "Engineering Management", "Team Culture", "Systems Thinking"]
categories: ["Columns"]
showReadingTime: true
icon: "flask"
featureImage: "feature_systems_thinkers.jpg"
featureAlt: "Abstract digital painting: a lone figure on a glowing cliff looks over floating islands of light in many colours, each a separate city, joined by fine golden threads that only the figure can see as one system"
---

{{< lead >}}
In the era of AI-generated code, the most valuable people on my teams are not the fastest coders.
They are the systems thinkers: the few who understand the broader context and move the needle.
{{< /lead >}}

## TL;DR

**What you will learn:**

- Why AI's wider range makes systems thinkers the people to hire and keep
- Six signals I use to spot them
- Four things leaders can do to grow them, and one thing that drives them away
- Three habits that help a software engineer become one

## What changed for software engineers

What is the most important skill for a software engineer today? A few years ago I would have said deep knowledge of one stack. I still value depth, but it is no longer enough, because AI has widened what one engineer can build.

Five years ago a backend engineer did not touch the frontend. A frontend developer did not write the Terraform for their own app: that belonged to the platform team and was usually out of reach. Today, with a coding agent, the backend engineer can change a React component, and the frontend developer can write the Terraform module that deploys it.

On many days I barely touch the code. I do not read most of what the agent writes, and I care less and less about it, because code is becoming just an expression language. What matters is what we build, and whether it supports other teams and follows our standards. Elizabeth Stone, Chief Product and Technology Officer at Netflix, sees a similar shift: specialists can now pick up a broader set of tools more easily than in the past [1].

So the role is changing, and two questions follow. How should engineers grow their careers when the borders of their role keep moving? And whom should companies hire, and work hard to keep, to thrive in the AI era? My answer to both: systems thinkers.

I am not the only one saying it. In July, Stone [told Lenny Rachitsky](https://www.youtube.com/watch?v=t0GiTyz4syY) what Netflix needs more of: *"We need more systems thinkers in a world with AI"* [1]. In October, Yossi Matias, head of Google Research, [described the colleagues he looks for](https://www.youtube.com/watch?v=FlOufV3hZFo): people who connect disciplines, ask the right questions and judge the trade-offs. The host summed it up: *"that's a systems thinker"* [2].

I see the same people in my AI teams at Pearson, most clearly in the last two years, since AI coding became part of daily work. They are not only developers: some are engineering managers or product owners. What they share is that they work close to the tech project and understand both the technology and the requirements. They have the context, and they start from the company's problem, not from their own component.

In my [previous post](/posts/what-ai-quietly-broke-in-my-engineering-team/) I argued that with cheap code, deciding what to build is almost the whole job. This post is about the people who can take the lead, who make things happen, who move the needle: how to spot them, grow them, and become one.

## What I mean by a systems thinker

{{< alert "lightbulb" >}}
**AI cannot replace systems thinkers.** An agent never has their context, and it has no taste for what to build and why. It can build almost anything you describe, but someone still has to know what is worth describing.
{{< /alert >}}

Systems thinkers still need deep expertise, but its job has changed. Depth is how they earn trust: people follow the person who connects the dots only if they trust that person in at least one area.

Depth is also how they see the problem. Deep knowledge of one area, whether technology, finance or the methodology of learning, comes only from spending real time on hard problems in it. That time is what lets them decompose a new problem and connect the components at a deeper level. An agent gives you a plausible design in seconds. Someone who has lived with the domain can tell which part of it will hurt in a year.

The Netflix talk draws this line for engineers: you may write less code, but you still need to understand how systems work, or you cannot judge what the agents built or fix it when it breaks [1]. The head of Google Research agrees that going deep *"is going to be incredibly important"* [2].

So a systems thinker is not someone who knows a little about everything. They know one area deeply, they see how their work fits into the company, and they use AI to build beyond their own area.

## Why they matter more now

Three things changed with AI, and each one raises the value of the person who sees the whole.

**Code is cheap, coherence is not.** When every team can build its own stack in a week, every team will. Agents write the services, but nobody writes the agreement on how those services share identity, data and on-call. Picture three teams that each build an agent over the same course content, each with its own retrieval, access rules and logging. Each demo works. Together they are three bills, three security reviews, and a learner who gets different answers from the same company. Netflix sees the same risk in design, which is why its designers now build design systems instead of *"shipping Frankensteins"* [1]. The cost of building used to limit how much incoherence a company could produce. That limit is gone. Now the limit is a person who notices the second copy before it gets built.

**Agents build only as well as the context we give them.** An agent has no hallway. It cannot ask the product owner where the roadmap goes next year. It knows only what we write down, and the context it needs goes far beyond team boundaries: business goals, user needs, company strategy and roadmaps. Some of today's small components will become the foundation of a larger picture, and only someone who knows that picture builds them that way. At Pearson we do applied AI science, and the pattern is simple: the more context we get from the product owner, from the vision to the roadmap and user research, the better the result. Good context becomes more valuable every month, and so does good documentation written for agents, not for humans. Netflix hires more people *"who can look across all the business domains"* for the same reason [1]. With the context in place, the scarce skill is asking the right question: Google Research expects every researcher to work more like the head of a lab, while AI does the heavy lifting [2].

**The hard problems sit at team boundaries.** In the agent systems I build, code rarely delays a launch. Other teams' rules do: daily Snyk security scans can block a deployment, and content rules decide what an agent may show to a learner. Each rule protects another team's goal. A systems thinker knows these limits before the project starts, because they have hit most of them before. They know the company policies, remember what blocked the last launch, and design with all of it from day one. I covered the architecture side in [an earlier post on agent systems](/posts/enterprise-agents-new-systems-mindset/).

## How I spot a systems thinker

The first five signals show in how people work. The last one is a result you can see from the outside, which makes it the easiest place to start.

1. **They understand the broader scope of the company.** They can explain what value the company creates and who the customer is, and they know how their work fits with other teams. Ask them why their team exists and you get a business answer, not a list of components.

2. **They build with other teams' goals in mind.** They connect the dots between roadmaps: the assessment team will need this same capability next quarter, so if we build it as a shared MCP tool instead of inside our agent, both teams win. That is how they influence priorities they do not own.

3. **They turn recurring arguments into written agreements.** When the same debate comes back for the third time, they write the RFC, collect feedback and leave behind an agreement everyone can point to. Those documents become the context our agents work from.

4. **They have a plan ahead.** Leadership priorities change, and their plan changes with them, but they always have one. My test: if I left them alone for six months, would they know what to build? With a systems thinker, the answer is yes.

5. **They keep asking why.** Why did we build this? Why this way? Why now? It can feel like friction, but the work gets better because they insist. Google Research puts asking the right questions first, because *"you need to understand what matters"* [2].

6. **Other teams already know them.** Because they always build for the whole system, over the years they have worked with many teams: developers, subject-matter experts, tech leads and product owners. They remember the decision and the trade-off from last year that everyone else has forgotten. Ask whom people call first when something crosses team lines, and you will hear the same few names.

## How leaders can grow them

This part is personal. My title at Pearson did not change, but this year I noticed my role drifting from engineering manager toward staff engineer. Before, I mostly managed and led. Now I take part in RFCs and design discussions, and I have started to build more things myself, with AI. With that drift, I started expecting more from the people on my team: more independence and self-direction, building things end to end, and working directly with other product owners and teams instead of through me. The transition has started, but it also needs changes in my own behavior and more trust from my side.

Systems thinkers are partly found and partly made. Four things help them grow.

**Give them a north star.** A vision and a roadmap are worth more to them than a detailed backlog. Once they understand where the company wants to be in two years, they build the missing pieces around it, often before anyone asks.

**Give them fast validation loops.** They build fast with agents, but they need someone to check the direction with: a customer, a product manager, an expert. Without that loop, a systems thinker can design a beautiful platform for a problem nobody has.

**Give them space.** Fewer meetings, more focus time. This is hard, because everyone wants them in their meeting, but if they spend the week in alignment calls, nobody thinks about where the system should go.

**Give them a talented team.** They want peers who think in a similar way and challenge them. In my experience they lose motivation faster around mediocrity than around hard problems. Netflix calls talent density *"the non-negotiable"*, because without it you cannot trust decisions made deep in the organization [1].

What drives them away is answering every failure with a new process. Netflix found that each time it added process to hard problems like planning or leveling, *"we spent more time without getting better outcomes"* [1]. Systems thinkers feel this first, because a new gate replaces exactly the judgment they bring.

## How an engineer becomes one

If you are an engineer who wants to reach the next level, this is a practice, not a personality type. Three habits matter most.

**Step out one click.** The most practical tip from Netflix: *"Each problem you're trying to solve, step out one click"*, and ask what you assume about the broader space [1]. Say you get a ticket to add an MCP tool that reads customer data. One click out: who else needs this data? Who owns it? What will security ask? Does a shared tool exist? Then build, and don't stay in the questioning state.

**Build relationships on purpose.** Spend more time with product and business people, and with those who understand user needs: they know why a feature matters before anyone writes a ticket. Then find the people who already think in systems, the ones who build templates and processes and try to protect them. Each of them becomes a shortcut to seeing a problem, or an opportunity, early.

**Always carry a why and a plan.** For everything you build, be able to say in one sentence why it matters to a customer or the business, and keep a written plan for your area for the next six months. In [*The Staff Engineer's Path*](https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/), Tanya Reilly turns this big-picture thinking into three maps: where you are, what the terrain around you looks like, and where the organization is heading [3].

### The traits underneath

| Trait | How it shows up |
|---|---|
| Curiosity | Asks why before how, reads beyond their own domain |
| Judgment | Weighs cost, risk and ethics, not only technical trade-offs [2] |
| Communication and listening | Explains their area to the CISO and to a content creator, and listens to both [2] |
| Selflessness | Optimizes for the organization, not their own team's metric [1] |
| Ownership | Stays responsible for the result, even when an agent wrote the code [1] |

## Takeaway

If you lead a team, find out whom other teams call first, and give that person a north star, a short feedback loop, focus time and strong peers. If you are an engineer, take your next ticket and step out one click before you start.

Going too far in the other direction isn't good either: a team made only of systems thinkers, asking why and writing RFCs, ships nothing. What matters most is that these people deliver results.

## References

1. Stone, E. and Rachitsky, L. (Jul 2026). [**Why Netflix is betting on systems thinkers—not specialists—in the AI era**](https://www.youtube.com/watch?v=t0GiTyz4syY). Lenny's Podcast. [Episode transcript](https://www.lennysnewsletter.com/p/netflix-cpto-on-ai-and-the-future)
2. Matias, Y. and Bovell, S. (Oct 2026). [**The Kind of Thinker Who Will Thrive in the AI Era**](https://www.youtube.com/watch?v=FlOufV3hZFo). I've Got Questions with Sinéad Bovell.
3. Reilly, T. (Sep 2022). [**The Staff Engineer's Path: A Guide for Individual Contributors Navigating Growth and Change**](https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/). O'Reilly Media.

*Quotes from [1] and [2] come from the YouTube captions and may differ slightly from the published transcripts. The Google Research episode [2] is sponsored by Google Research.*
