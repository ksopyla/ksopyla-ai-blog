---
title: "Systems thinkers: how to spot them, grow them, and become one"
date: 2026-11-15
draft: true
description: "Leaders at Netflix and Google Research say systems thinkers are who they hire for now. Notes on how I spot them, how leaders can grow them, and how a software engineer can become one."
tags: ["AI Leadership", "Engineering Management", "Team Culture", "Systems Thinking"]
categories: ["Columns"]
showReadingTime: true
icon: "flask"
---

{{< lead >}}
?? What in the era of AI gen code is the most valuable in emploees - the system thinkers, why
When code got cheap, the people I least wanted to lose were not the fastest coders. 
?? they were the few who can understand the broder context, those who move the needle
They were the few who see how the whole company fits together. 
?? I dont like this, this sounds as not mine, those should support my views and observations in the main content
This year, leaders at Netflix and Google Research named the same skill as the one they now hire for.
{{< /lead >}}

## TL;DR

**What you will learn:**

- Why systems thinkers matter more once AI makes code cheap
- Seven signals I use to spot them in a company
- Four things leaders can do to grow them, and one thing that drives them away
- How a software engineer can become one, starting with the next ticket


?? Open this differently, start with: what is the most important skill for Software engeenrs, why the role os SE is evolve, thanks to AI our capacity to build has broaden, you could eaily build or change something that 5years ago was over your role (eg. backend engineer do not change things on fronted, building the terraform for frontend dev was usually out of his reach), now this changed, so how we should evolve our carrers and what people we should hire or stay in companies to thrive in AI era -> System thinkers

?? some profs from podcast
In July, Elizabeth Stone, Chief Product and Technology Officer at Netflix, told Lenny Rachitsky what Netflix is hiring more of. Her answer was not a function: *"We need more systems thinkers in a world with AI"* [1]. Three months later, Yossi Matias, who leads Google Research, told futurist Sinéad Bovell what he looks for in colleagues: people who connect disciplines, ask the right questions and judge the trade-offs. Bovell summed it up in four words: *"that's a systems thinker"* [2].

I recognized the people both of them described. I have worked with a handful of them in my own software house, in startups, and now in enterprise AI teams ??On many levels as software engineers, engineering managers, staff/principal engineers
?? this is too obious and banal
. They rarely had a special title. They were the people other teams called first.

In my [previous post](/posts/what-ai-quietly-broke-in-my-engineering-team/) I argued that code is no longer the bottleneck: AI made writing software cheap, so deciding what to build became almost the whole job. This post is about the people who ?? can take the lead, who makes things happen, who move the needle.



## What the two talks agree on
?? I don't like the title, I dont want to hava a post about the other podcast, this should be mine, with references to good and valuable sources, we can cite and take a lot from them, but it needs to be a part of my story

?? AI expands the range of our capabilities, but we need to have one experties very deep

?? In Pearson now my role has changed, from EM to more Staff engineer and from people on my team I've started expecting a more independence and self direction, I want them build things end to end, with more collaboration with others (other po and teams), this transition has started but it also need some changes of my behaviour and more trust 


?? this is valuable observation, the aligment is important, having the right context for building, good docs, good documented process those are the input for our agents, people who understand that and try to build it are the ones that we need 
Stone starts from Netflix's own history. For years, local teams moved fast by building whatever stack their business problem needed, off the central paved path. That stops working once agents are *"operating across multiple systems, wanting source of truth data"* [1]. So Netflix now hires more people *"who can look across all the business domains"* and turn what they see into shared building blocks. Her designers spend more time on design systems, so that non-designers can build products that still feel like one Netflix instead of *"shipping Frankensteins"*. Her short version: *"what got Netflix here doesn't get Netflix there."*


?? relate to my experience at Pearsone, were we do a applied AI science, the more. context from product owner (vision, long term roadmap, user reserach) the better, system thinkers could use those to build somthing across domains, that has value, asking the right questions skill is importatn
Matias comes at it from science. Research pushes people into ever narrower specialties, while in his words *"a lot of the magic happens"* when you bring people and disciplines together, *"connecting dots"* [2]. With an AI collaborator that reads across fields, he expects every researcher to work more like the head of a lab, choosing the right questions instead of doing the heavy lifting. The skills he hires for follow: asking the right questions, spotting the opportunity, communicating and listening. *"Sometimes we call them soft skills, but they're skills."* Bovell's name for such a person stuck with me: *"an organization of one"* [2].


?? who is Stone, it isn't clear, try to avoid such references to people, this makes reading hard
Both also defend depth, which keeps the idea honest. Stone still needs the few people in the world who really understand video encoding or playback, and Matias says going deep *"is going to be incredibly important"* [1][2]. What Stone sees trending down is narrow specialization without the will to look beyond it. A systems thinker is not a generalist who dabbles. It is someone with a craft who also knows where their work sits in the whole.

## Why they matter more now

My opinion: three things changed with AI, and each raises the value of the person who sees the whole.

?? this is good one, I like it
**Code is cheap, coherence is not.** When every team can build its own stack in a week, every team will. Agents write the services, but nobody writes the agreement on how those services share identity, data and on-call. The cost of building used to limit how much incoherence a company could produce. That limit is gone.

?? good, make sure that we do not duplicate ideas, maybe the note that I have written few lines above should go here
**Agents need context that lives between teams.** An agent has no hallway. It cannot ask the SRE who got burned by this pattern last year, or the security team why a data source is off limits. Stone's warning that a company of thousands *"can no longer rely on tribal knowledge"* applies twice to agents [1]. The context has to be written down as paved paths, source-of-truth data and guardrails, and systems thinkers are the people who know it well enough to write it.

?? this is acctually true, we have daily snyc scans which can block the deployment, but I try to write it from different angle, one of the examples is to 
**In enterprise AI, the hard problems sit at team boundaries.** In the agent systems I build, code rarely delays a launch. A security review nobody planned for does, or a content rule nobody asked about, or an SRE team that hears about a new workload a week before go-live. I covered the architecture side in [If You Want to Build Agent Systems, You Need to Lose Your REST-Style Intuitions](/posts/enterprise-agents-new-systems-mindset/). The human side is a person who knew all those teams before the project started.


??there are a few my personal takes above, 
> **TODO (Krzysztof):** one short, anonymized story of a systems thinker you worked with. What did they spot early, whom did they talk to, and what would have happened without them?



## How I spot a systems thinker

?? I don't like this, change it
None of these signals is a title, and I have seen them in junior engineers too.


?? rephrase based on my additons
1. **They understand the broader scope of the company.** They can explain what the company value is, try to understand who is the customer and they seek the value, how what they are building fit for other teams. Ask why their team exists and you get a business answer, not a list of components.

?? this is good, but rather a observed results, this could help you spot them
2. **They have relationships across many teams.** They always try to buld system, so over the years they have help and reach other dev teams, SME's, tech leaders, product owners other product teams. Thanks to this their context is much broder, the keep everything in their minds

?? I'm not sure to which point it should goes, but the have a good memory, they remember decisions and tradeoffs from last year

?? this is not about the collisions and problems but rather aligning with the goals of others
3. **They connect the dots and raise issues before they become problems.** They are the ones who can mentions that this feature could be requred by other team, if we build it in such a way we could alos help them, they could influecne the prorities. They can identified the potential problems in the future and call it out out loud 

??
4. **They push for shared agreements.** They write the RFC, collect feedback from other engineering teams, and turn a recurring argument into an agreement everyone can point to. Netflix calls the ideal *"highly aligned but loosely coupled"* [1]. Systems thinkers do most of the aligning.

?? the point is good, but the example is week, 
5. **They understand other teams' priorities.** They know the platform team is measured on stability and the product team on a launch date, and they find a sequence that protects both, even when the goals conflict in time. A Netflix engineering principle Stone quotes names the instinct: *"do the thing that is right for the broader organization instead of just what's right for you locally"* [1].

6. **They have a plan ahead.** Leadership priorities change, and their plan changes with them, but they always have one. My test: if I left them alone for six months, would they know what to build? With a systems thinker, the answer is yes.

7. **They keep asking why.** Why did we build this? Why this way? Why now? It can feel like friction, but they need a valuable why before they build, and the work gets better because they insist. Matias puts asking the right questions first, because *"you need to understand what matters"* [2].

## How leaders can grow them

Systems thinkers are partly found and partly made. Four things have worked for me.

**Give them a north star.** A vision and a long-term roadmap are worth more to them than a detailed backlog. Once they understand where the company wants to be in two years, they build the missing pieces around it, often before anyone asks.

**Give them fast validation loops.** They build fast, especially with agents, but they need someone to check the direction with: a customer, a product manager, a subject-matter expert. Without that loop, a systems thinker can design a beautiful platform for a problem nobody has.

**Give them space.** Fewer meetings, more focus time. This is hard, because they are exactly the people everyone wants in their meeting. If they spend the week in alignment calls, nobody is left to think about where the system should go.

**Give them a talented team.** They want peers who think in a similar way and challenge them. In my experience they lose motivation faster around mediocrity than around hard problems. Stone calls talent density *"the non-negotiable"*, because without it you cannot trust decisions made deep in the organization [1].

What drives them away is answering every failure with a new process. Stone says that each time Netflix added process to hard problems like planning or leveling, *"we spent more time without getting better outcomes"* [1]. My opinion: systems thinkers feel this first, because a new gate replaces exactly the judgment they bring.


?? I don't know if this section is needed, when someone read all the above he/she should know what to do, maybe we could shrink it to 3 most important
## How an engineer becomes one

If you are a software engineer who wants to reach the next level, this is a practice, not a personality type. AI makes it easier: Stone notes that specialists can now pick up a broader set of tools more easily than in the past [1].

**Step out one click.** Stone's trick is the most practical advice in either talk: *"Each problem you're trying to solve, step out one click"*, and ask what you assume about the broader space [1]. Say you get a ticket to add an MCP tool that reads customer data. One click out: who else needs this data? Who owns it? What will security ask? Does a shared tool already exist? Then build. Stone warns against staying in the questioning state, and her second tip goes with it: do your job in a way that helps your manager do theirs, because your manager's seat shows the whole.

**Collect relationships on purpose.** Do not wait for an incident to meet the SRE team or the security office. Join a cross-team review, help with a migration, ask the content team how they actually use your feature. Each of those people becomes a shortcut that later lets you see a problem early.

> **TODO (Krzysztof):** how did you build your own cross-team relationships? One concrete habit would make this paragraph yours.

**Write things down.** Turn what you learn into RFCs and ADRs other teams can comment on, as I described in [What I learned leading an AI engineering team](/posts/what-i-learned-leading-ai-engineering-team/). Writing is how a systems thinker scales beyond their own calendar, and today it is also how agents get the context.

**Keep one deep craft.** People trust your dot-connecting only if they trust you in at least one area. Stone draws the line for engineers: you may write fewer lines of code, but you still need to understand how code and systems work, or you cannot tell whether what the agents built is good, or fix it when it breaks [1].

**Always carry a why and a plan.** For everything you build, be able to say in one sentence why it matters to a customer or the business, and keep a written plan for your area for the next six months. Tanya Reilly calls this big-picture thinking, and in *The Staff Engineer's Path* she turns it into three maps: where you are in the organization, what the terrain around you looks like, and where the organization is heading [3].

### The traits underneath

??this is really good summary
| Trait | How it shows up |
|---|---|
| Curiosity | Asks why before how, reads beyond their own domain |
| Judgment | Weighs cost, risk and ethics, not only technical trade-offs [2] |
| Communication and listening | Explains their area to the CISO and to a content creator, and listens to both [2] |
| Comfort with ambiguity | Keeps a plan while priorities change around it [1] |
| Selflessness | Optimizes for the organization, not their own team's metric [1] |
| Ownership | Stays responsible for the result, even when an agent wrote the code [1] |


?? I don't want to spent to much space for that, add this to takeaway, as a brief comment, Going too far in the other direction isn't good; what matters most is that these people deliver results.
## Limits and counterpoints

**A team of only systems thinkers ships RFCs, not products.** You still need people who go deep and stay there. My best teams had both kinds.

**Questioning can become a hiding place.** Asking why is valuable until it becomes the reason nothing ships. One click out, not ten.

**Their work is easy to miss.** Tanya Reilly calls much of it glue work: onboarding people, noticing what got dropped, keeping everyone going roughly the same direction. Managed deliberately, she says, it builds technical leadership, but *"left unconscious, it can be career limiting"* [4]. If your promotion process counts only code, you will push your systems thinkers out of engineering.

**They can become the bottleneck.** When one person is the hallway for the whole company, they burn out and everything waits for them. A good systems thinker works to make themselves less necessary by writing agreements down and building paved paths.

**The evidence is thin.** Netflix and Google have thousands of engineers, and in a ten-person startup most people think in systems by necessity. My own sample is a handful of people I have worked with, so treat the seven signals as my opinion, not a validated model.

## Takeaway

If you lead a team, find out whom other teams call first, and give that person a north star, a short feedback loop, focus time and strong peers. If you are an engineer, take your next ticket and step out one click before you start.

## References

1. Stone, E. and Rachitsky, L. (Jul 2026). [**Why Netflix is betting on systems thinkers—not specialists—in the AI era**](https://www.youtube.com/watch?v=t0GiTyz4syY). Lenny's Podcast. [Episode transcript](https://www.lennysnewsletter.com/p/netflix-cpto-on-ai-and-the-future)
2. Matias, Y. and Bovell, S. (Oct 2026). [**The Kind of Thinker Who Will Thrive in the AI Era**](https://www.youtube.com/watch?v=FlOufV3hZFo). I've Got Questions with Sinéad Bovell.
3. Reilly, T. (Sep 2022). [**The Staff Engineer's Path: A Guide for Individual Contributors Navigating Growth and Change**](https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/). O'Reilly Media.
4. Reilly, T. (2018). [**Being Glue**](https://www.noidea.dog/glue). Talk and annotated slides, No Idea Blog.

*Quotes from [1] and [2] come from the YouTube captions and may differ slightly from the published transcripts. The Google Research episode [2] is sponsored by Google Research.*
