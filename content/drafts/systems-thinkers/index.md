---
title: "Systems thinkers: how to spot them, grow them, and become one"
date: 2026-11-15
draft: true
description: "AI widened what one engineer can build. Notes on why systems thinkers matter most now, how to spot and grow them, and how to become one."
tags: ["AI Leadership", "Engineering Management", "Team Culture", "Systems Thinking"]
categories: ["Columns"]
showReadingTime: true
icon: "flask"
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

What is the most important skill for a software engineer today? A few years ago I would have said deep knowledge of one stack. I still value depth, but it is no longer enough, because AI has widened what one engineer can build.

Five years ago a backend engineer did not touch the frontend. A frontend developer did not write the Terraform for their own app: that belonged to the platform team and was usually out of reach. Today, with a coding agent, 
??for above ^^, I would say more, that you barly touch the code, you do not see the code, you start don't care about it, it is just an expression language, what matters is what to build and support oters according to our standards
the backend engineer can change a React component, and the frontend developer can write the Terraform module that deploys it. 

Elizabeth Stone, Chief Product and Technology Officer at Netflix, sees the same shift: specialists can now pick up a broader set of tools more easily than in the past [1].

So the role is changing, and two questions follow. How should engineers grow their careers when the borders of their role keep moving? And whom should companies hire, and work hard to keep, to thrive in the AI era? My answer to both: systems thinkers.


?? add links to the text, keep the references as well
I am not the only one saying it. In July, Stone told Lenny Rachitsky what Netflix needs more of: *"We need more systems thinkers in a world with AI"* [1]. In October, Yossi Matias, head of Google Research, described the colleagues he looks for: people who connect disciplines, ask the right questions and judge the trade-offs. The host summed it up in four words: *"that's a systems thinker"* [2].

?? add only recent evidences, I want it to be connected to AI era and AI coding (last 2 years), those who close work on tech projects, understand the techonolgy, understand the requirements, those are not only developers, those who understand tech and have a context
I have worked with such people on many levels: software engineers, engineering managers, , in my own software house, in startups and now in enterprise AI teams at Pearson. Their titles differed. What they shared was a starting point: the company's problem, not their own component.

In my [previous post](/posts/what-ai-quietly-broke-in-my-engineering-team/) I argued that code is no longer the bottleneck: AI made writing software cheap, so deciding what to build became almost the whole job. This post is about the people who can take the lead, who make things happen, who move the needle: how to spot them, how to grow them, and how to become one.

## What I mean by a systems thinker


?? add that AI cant replace system thinkers, It never has such a context and tast what and why to build
?? below is not right angle, with deep experties cite the podcast, those people need to build trust (by their experties) and technology understanding, but at the same time AI allows them to build broder
AI expands the range of what each of us can do, but a systems thinker still needs one expertise that goes very deep. Without it, the range is shallow: you can generate a Terraform module, but you cannot tell whether it is safe to deploy. Both talks defend depth. Netflix still needs the few people in the world who really understand video encoding or playback, and the head of Google Research says going deep *"is going to be incredibly important"* [1][2]. What Netflix sees trending down is narrow specialization without the will to look beyond it [1].

So a systems thinker is not a generalist who dabbles. It is someone with a deep craft who also knows where their work sits in the whole company, and who uses AI's wider range to build across it.

## Why they matter more now

My opinion: four things changed with AI, and each one raises the value of the person who sees the whole.

**Code is cheap, coherence is not.** When every team can build its own stack in a week, every team will. Agents write the services, but nobody writes the agreement on how those services share identity, data and on-call. The cost of building used to limit how much incoherence a company could produce. That limit is gone.

**Agents need context that lives between teams.** An agent has no hallway. It cannot ask the SRE who got burned by this pattern last year, or the security team why a data source is off limits. It gets only what we write down: good documentation, documented processes, source-of-truth data and a clear alignment on what we build and why. That is the input for our agents, and it limits the quality of what they produce. Netflix learned this from its own history. For years, local teams moved fast by building whatever stack their problem needed, off the central paved path. That stops working once agents are *"operating across multiple systems, wanting source of truth data"* [1], so Netflix now hires more people *"who can look across all the business domains"* and turn what they see into shared building blocks. The people we need are the ones who understand this and build that context, not only the features on top of it.

**When building is cheap, the question is the scarce part.** At Pearson we do applied AI science, and I see a simple pattern: the more context we get from the product owner, the better the result. A vision, a long-term roadmap and real user research let a systems thinker build something that works across domains and has value, instead of a clever prototype for one team. Google Research expects the same shift in science: with an AI collaborator that reads across fields, every researcher will work more like the head of a lab, choosing the right questions instead of doing the heavy lifting [2]. Asking the right questions comes first on its list of skills to hire for, together with spotting the opportunity, communicating and listening: *"Sometimes we call them soft skills, but they're skills"* [2].

**The hard problems sit at team boundaries, and so do other teams' goals.** In the agent systems I build, code rarely delays a launch. Other teams' rules do. At Pearson, daily Snyk security scans can block a deployment, content rules decide what an agent may show to a learner, and SRE teams need to hear about a new workload long before go-live. None of this is red tape: each rule protects another team's goal. A systems thinker knows those goals before the project starts and designs with them from day one, so the security scan is a check that passes, not a surprise a week before launch. I covered the architecture side in [If You Want to Build Agent Systems, You Need to Lose Your REST-Style Intuitions](/posts/enterprise-agents-new-systems-mindset/).

## How I spot a systems thinker

These are the signals I look for. The first five show in how people work. The last one is a result you can see from the outside, which makes it the easiest place to start.

1. **They understand the broader scope of the company.** They can explain what value the company creates and who the customer is, and they go looking for that value themselves. They know how what they build fits with the work of other teams. Ask them why their team exists and you get a business answer, not a list of components.

2. **They build with other teams' goals in mind.** They connect the dots between roadmaps. They are the ones who say: the assessment team will need this same capability next quarter, so if we build it as a shared MCP tool instead of inside our agent, both teams win. That is how they influence priorities they do not own. A Netflix engineering principle names the instinct: *"do the thing that is right for the broader organization instead of just what's right for you locally"* [1].

3. **They turn recurring arguments into written agreements.** When the same debate comes back for the third time, they write the RFC, collect feedback from the other teams and leave behind an agreement everyone can point to. Netflix calls the ideal *"highly aligned but loosely coupled"* [1]. Systems thinkers do most of the aligning, and their documents become the context our agents work from.

4. **They have a plan ahead.** Leadership priorities change, and their plan changes with them, but they always have one. My test: if I left them alone for six months, would they know what to build? With a systems thinker, the answer is yes.

5. **They keep asking why.** Why did we build this? Why this way? Why now? It can feel like friction, but they need a valuable why before they build, and the work gets better because they insist. Google Research puts asking the right questions first, because *"you need to understand what matters"* [2].

6. **Other teams already know them.** Because they always try to build the whole system, over the years they have helped and reached out to other dev teams, subject-matter experts, tech leads, product owners and other product teams. Their context is much broader than their own backlog, and they keep it in their heads: they remember the decision and the trade-off from last year that everyone else has forgotten. Ask whom people call first when something crosses team lines, and you will hear the same few names.

## How leaders can grow them

?? I dont change the role, but I rather observed that my role drifted more toward staff eng, I stared to build more things with AI, where previously I mostly manage and take part in RFC and discussions

This part is personal. This year my role at Pearson moved from engineering manager toward something closer to a staff engineer. With it, I started expecting more from the people on my team: more independence and self-direction, building things end to end, and working directly with other product owners and teams instead of through me. The transition has started, but it also needs changes in my own behavior and more trust from my side.

Systems thinkers are partly found and partly made. Four things help them grow.

**Give them a north star.** A vision and a long-term roadmap are worth more to them than a detailed backlog. Once they understand where the company wants to be in two years, they build the missing pieces around it, often before anyone asks.

**Give them fast validation loops.** They build fast, especially with agents, but they need someone to check the direction with: a customer, a product manager, a subject-matter expert. Without that loop, a systems thinker can design a beautiful platform for a problem nobody has.

**Give them space.** Fewer meetings, more focus time. This is hard, because they are exactly the people everyone wants in their meeting. If they spend the week in alignment calls, nobody is left to think about where the system should go.

**Give them a talented team.** They want peers who think in a similar way and challenge them. In my experience they lose motivation faster around mediocrity than around hard problems. Netflix calls talent density *"the non-negotiable"*, because without it you cannot trust decisions made deep in the organization [1].

What drives them away is answering every failure with a new process. Netflix found that each time it added process to hard problems like planning or leveling, *"we spent more time without getting better outcomes"* [1]. My opinion: systems thinkers feel this first, because a new gate replaces exactly the judgment they bring.

## How an engineer becomes one

If you are a software engineer who wants to reach the next level, this is a practice, not a personality type. Three habits matter most.

**Step out one click.** The most practical advice from the Netflix talk: *"Each problem you're trying to solve, step out one click"*, and ask what you assume about the broader space [1]. Say you get a ticket to add an MCP tool that reads customer data. One click out: who else needs this data? Who owns it? What will security ask? Does a shared tool already exist? Then build. The same talk warns against staying in the questioning state, and adds a second tip: do your job in a way that helps your manager do theirs, because your manager's seat shows more of the whole.

?? those are not good example, I would say rather more connect with product and busisnes people, more with those who understand user needs, more with those who think in systems, build templates, processes and try to protect them
**Build relationships on purpose.** Do not wait for an incident to meet the SRE team or the security office. Join a cross-team review, help with a migration, ask the content team how they actually use your feature. Each of those people becomes a shortcut that later lets you see a problem, or an opportunity, early.

**Always carry a why and a plan.** For everything you build, be able to say in one sentence why it matters to a customer or the business, and keep a written plan for your area for the next six months. Tanya Reilly calls this big-picture thinking, and in *The Staff Engineer's Path* she turns it into three maps: where you are in the organization, what the terrain around you looks like, and where the organization is heading [3].

### The traits underneath

| Trait | How it shows up |
|---|---|
| Curiosity | Asks why before how, reads beyond their own domain |
| Judgment | Weighs cost, risk and ethics, not only technical trade-offs [2] |
| Communication and listening | Explains their area to the CISO and to a content creator, and listens to both [2] |
| Comfort with ambiguity | Keeps a plan while priorities change around it [1] |
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
