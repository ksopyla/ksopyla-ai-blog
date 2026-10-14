---
title: "What AI quietly broke in my engineering team"
date: 2026-10-13
draft: false
description: "Code got cheap, but leading an engineering team got harder. Field notes on what AI erodes in a team: the filter that forced us to choose, the ladder of experience, and the habit of asking each other for help."
tags: ["AI Leadership", "AI Engineering", "Engineering Management", "Team Culture"]
categories: ["Columns"]
showReadingTime: true
icon: "flask"
featureImage: "feature_ai_quietly_broke_engineering_teams.jpg"
featureAlt: "Abstract digital painting: glowing human silhouettes linked by warm orange threads of light drift apart into isolated figures lit by cool blue light, with a fading ladder of light between them"
---

{{< lead >}}
AI made my team's code cheap and quietly took away three things that held the team together. Leading it is harder now than before AI. This post is about that damage.
{{< /lead >}}

## TL;DR

**What you will learn:**

- Why cheap code does not shorten the roadmap, and why deciding *why* and *what* to build got harder
- How AI flattens the ladder of expertise, threatens the standing of seniors, and lets confidence beat experience
- What a team loses when nobody needs to ask anyone: relationships, communities, collective creativity, and honesty about mistakes
- Four things I am trying as a lead to counter it

Prefer to watch? Here is the one-minute version:

{{< youtube-short id="BQU01JP1X1E" title="3 things AI quietly eroded in my engineering team" >}}

The beginning of this year was hard for me. The agentic coding revolution had started, and expectations went through the roof: everyone's, and to be fair, mine too. The metrics did not follow. However hard we pushed, our speed of execution would not triple. I felt burned out, and I kept asking myself what was wrong with my team. Why could we not reach the 3x velocity everyone expected?

Around me, the same question came back in many versions: *if AI writes the code in minutes, why does this still take a quarter?* Trying to answer it changed how I see my job. The code was never what took a quarter. AI made it cheap, but it also removed three things that used to do part of my job as a lead for free:

- 💸 **The cost of building**, which forced us to choose.
- 🪜 **A ladder of experience**, which gave people status and identity.
- 🙋 **The habit of asking each other for help**, which held the team together.

None of it shows up on a velocity chart. All of it is now my job.

This post covers only the damage, so it is one-sided on purpose. I am still positive about AI and believe we have to adapt, but it is hard to adapt to something you have not noticed. The practices that keep my team sane with agents are in my [previous post](/posts/what-i-learned-leading-ai-engineering-team/).

## 💸 Code is no longer the bottleneck {#code-is-no-longer-the-bottleneck}

The logic behind that question sounds airtight: AI writes code faster, so features ship faster, so the roadmap should shrink. Only the first step is true: typing code was rarely what slowed us down. **The constraint is knowing what to build.**

Fred Brooks explained why forty years ago. In *No Silver Bullet* he separated the *accidental* work of software, turning a design into code, from the *essential* work of deciding what the system should be [1]. *"The hardest single part of building a software system is deciding precisely what to build."* Clients learn what they want by trying versions, and every round needs a human to look, react and change their mind, at human speed.

AI has pushed the accidental part of my team's work close to zero, so the essential part is now almost the whole job. And it got harder.

**The *why* got harder.** Does this product fit who we are? Pearson, where I work, is a learning company, so AI tutors make sense for us: they rest on our content, our brand and the trust teachers and learners already give us. From a team with no learning background, the same tutor is a weekend demo. When anyone can generate a working app in a day, code stops being the moat. Fit with your mission becomes the moat, and someone has to judge it.

**The *what* got harder.** When building was expensive, cost acted as a filter: we could not build everything, so we had to choose. Now every stakeholder idea arrives with a working demo, and saying no is a pure judgment call with nothing to hide behind. DORA's 2025 research found that teams adopting AI without a strong focus on users can see their performance *drop* [2], and calls it the [feature factory](https://dora.dev/capabilities/user-centric-focus/): *"high activity but low impact."*

### Prototypes hide the hard parts

Even the best change hides a trap. Clickable mocks and vibe-coded prototypes now work better as requirements than spec documents: we show one to a partner and quickly learn whether we mean the same thing. But Brooks also warned that a prototype makes *"no attempt to handle the exceptions"* [1]. A mock looks finished, so people treat it as almost done, while it hides everything non-functional: scalability, a cost per session that must fit the business case, an architecture elastic enough for the next partner, backups that restore in minutes.

Cheap prototypes also create more decisions, not fewer. When the team can build three variants in a day, someone has to pick one, align the stakeholders and say no to the other two. That load lands on product managers and leads, and it does not scale with tokens. Faster engineering only makes their queue longer.

> **AI moved the bottleneck from the people who build to the people who decide.**

## 🪜 The ladder of expertise is flattening {#the-ladder-of-expertise-is-flattening}

Before AI, my teams had a hierarchy nobody wrote down. It was not the org chart. It grew from expertise and natural inclinations: the engineer who loved squeezing a query from minutes down to milliseconds, the one who cut 100 ms of latency by reorganizing the goroutines, the one who kept every dependency in their head and in a week split our main conversational service into conversation, feedback and memory parts. Those inclinations were noticed and appreciated, and that gave people worth and a safe place in the team.

Juniors learned by osmosis: reading good review comments on other people's PRs, overhearing performance debugging sessions. Then they climbed themselves: a hard problem, a struggle, a fix of their own or a question to someone who had been there. Every climb left knowledge, confidence and an identity: *I am the person who can handle this.*

### Who gains, who loses

AI compresses that ladder. I watched the distance between junior and senior output shrink in my own team and wondered whether it was just us, so I went looking for research. The pattern was the same in very different places.

In field experiments with nearly 5,000 developers at Microsoft, Accenture and a Fortune 100 company, the less experienced adopted AI more and gained more [3]. In customer support, the newest agents improved the most, while the most experienced got only *"small gains in speed and small declines in quality"* [4]. Good news for juniors. What it meant for seniors, the productivity papers did not explain. Social psychology did.

In 1959, John French and Bertram Raven described *expert power*: influence that comes from knowing more [5]. Part of a senior's standing rested on knowledge that is now one prompt away. AI devalues the cheap half of expert power (recall of syntax, APIs, tricks) and leaves the expensive half: judgment about trade-offs, context and consequences.

For people who were role models, this is an identity story, not a productivity story. Researchers call it *AI identity threat* and count loss of status among its central predictors [6]. In a study of 381 employees, AI adoption lowered psychological safety and, through it, raised depression [7]. When the person everyone used to ask stops being asked, they lose part of the reason they felt safe in the team.

My opinion: people whose expertise rested on recall of syntax, algorithmic knowledge or understanding the maths will lose ground. People who communicate, take responsibility, push change through and think holistically will win. I used to think the hard part for seniors was becoming full-time reviewers of AI diffs. That frustration was temporary: agents review agents now, and most of us stopped reading the generated code. The harder part is relearning the soft skills the old ladder never asked for.

### When confidence beats experience

Being heard is one of those skills, and the flattened ladder made it harder. With AI, less experienced engineers *feel* much more capable, and they sound it. The feeling runs ahead of the skill: in one study, AI raised scores on reasoning tasks by about 3 points, while people overestimated their performance by about 4, and those who knew AI best judged themselves worst [8].

Confidence also sells. Overconfident people gain status, because others read confidence as competence [9]. I see it in meetings: many leaders prefer a confident plan to a careful one, and the AI behind the plan sounds just as sure of itself. So less experience often gets more voice. The bill comes when the plan meets production, with edge cases nobody considered and costs nobody calculated. Usually, the seniors repair the damage.

Really experienced engineers are mostly humble. They know the team always forgot something, or someone left something unsaid. So they hedge, watch the room listen to the person who does not, and later get the call when it breaks.

> **A flattened ladder where everyone feels senior is not the same as a team where everyone is senior.**

## 🙋 Nobody needs to ask anymore {#nobody-needs-to-ask-anymore}

Asking a colleague for help looks like a small cost: you interrupt someone and admit you do not know. Psychology suggests it gives both sides more than it takes. Roy Baumeister and Mark Leary argued that the need to belong is a fundamental human motivation, met through frequent, positive contact with people who care about us [10].

At work, much of that contact came from small requests. The one who asked got an answer and a reason to talk. The one who helped felt needed, and not only figuratively: in a brain-imaging study, giving to a cause activated the same reward system as receiving money [11].

For most of my career, nobody on my team was self-sufficient. One person was the SQL master, another could write a Python one-liner for anything, another could fix your broken deployment pipeline in ten minutes. You had to walk over, or ping them on Slack, and ask.

Now the query, the one-liner and the Terraform fix come from an assistant. It is faster. It is also lonelier, and not only in my team. Among about 187,000 GitHub developers, Copilot shifted work away from collaboration and toward working alone [12], and across four countries, employees who worked more with AI reported more loneliness [13].

Those requests were also the doorway to everything else. While fixing someone's query, you noticed the tennis racket behind them and asked about it, or about the kids. That is how colleagues became people to each other. Benjamin Franklin famously won over a hostile fellow legislator by asking to borrow a rare book, and a 1969 experiment confirmed the effect: we like people more after doing them a favor [14]. Asking the SQL master for help was never only a cost to them. It was an investment in the relationship.

### Communities are thinning

The same is happening outside our teams, and this part I take personally. Developer communities shaped me. I remember my first Stack Overflow badges and the quiet pride of helping a stranger. At university, a few of us solved algorithmic puzzles together, each owning a piece of the solution, and it was fun. Later I presented my solutions at local tech meetups and stayed long after the talks with people who cared about the same things. At ML conferences you could listen, ask and start a collaboration in the corridor. It was a tribe, and I belonged to it.

By May 2025, Stack Overflow was getting about as few new questions per month as in 2009, its first full year online [15]. Meetups and conferences feel different to me now, less technical. The questions that used to bring strangers together go to a chat window, and nobody earns a badge for answering them.

### Collective creativity

For a company, this may be the most expensive loss, because nobody sees it until a new idea is needed.

Psychologist Daniel Wegner called it *transactive memory*: a team stores knowledge not in each head but in the shared map of who knows what [16]. When nobody asks anyone, the map decays. The team still has experts. It just stops knowing who they are.

New ideas need that map, because they come from collisions. Andrew Hargadon and Beth Bechky found that collective creativity in professional service firms grew out of four kinds of interaction, and the first two were asking for help and giving it [17]. A colleague's question often turns your problem into a better one.

An assistant pushes the other way: it answers with what is already known. I saw it in my own research: agents pulled an unusual idea back toward the ordinary, one reasonable decision at a time, and nothing failed along the way ([I wrote about it here](/posts/auto-research-and-human-ideas/)). In a writing experiment, stories built on AI ideas were rated more creative one by one, but they were more alike [18]. Each person gets better. The group gets more uniform.

My opinion: this is a strategic risk few companies see yet. If every engineer asks the same few models, every team gets similar answers, and so do your competitors. What sets a company apart comes from people who know different things colliding over a real problem, trying, failing and trying again, together.

> **A hundred engineers in private chats with the same model are not a hundred perspectives. They may be closer to one.**

### Honesty about mistakes

The cost I worry about most as a lead is honesty. An assistant never judges you, and that is part of its appeal: asking a peer means admitting you do not know. When Amy Edmondson studied hospital units in the 1990s, the better-led units recorded *more* medication errors, not fewer, because people there felt safe enough to report them [19].

That is the team I want: people who say "I don't know" and "I made a mistake" early, so we fix the real problem instead of discovering it a week later. Every question that goes to a chatbot instead of a colleague is one less chance to practice that honesty, the same honesty it takes to deliver bad news or challenge a design.

## 🧪 What I am trying as a lead {#what-i-am-trying-as-a-lead}

These are experiments and intuitions, not a framework. Some I already practice; others I am still learning, together with other engineering managers, our tech and product teams, and our stakeholders. I am glad I work with open-minded people, but none of this changes in one quarter.

1. **Measure value, not velocity.** Velocity shows how busy we are, not whether it mattered. So I try to show stakeholders what changed for users, and how long work waited for a decision compared with how long it took to build. When building takes days and deciding takes weeks, "why isn't AI making us faster?" becomes a question about how we decide. This is the one I struggle with most: neither is easy to measure or to sell.
2. **Reward the people who challenge the solution.** Seniority now shows in who says "this will not scale", "the partner never asked for that" or "we are building the wrong thing". That is where I want to give credit: in design reviews, ADRs and trade-off calls.
3. **Watch who takes the blame.** When something breaks, who says "that was me"? I treat it as one of the strongest positive signals a team can give. If nobody ever does, the team is weak, however good the velocity chart looks.
4. **Share AI setups, not prompts.** Short demos of how each person works with AI, shared skills (more in [the previous post](/posts/what-i-learned-leading-ai-engineering-team/)), and open sessions where the team trades ideas. Knowledge flows between people again instead of disappearing into private chats.

## 🎯 Takeaway {#takeaway}

At the beginning of the year I asked what was wrong with my team. It was the wrong question. The better one was what AI had quietly taken from it: the cost that forced us to choose, the ladder that gave people standing, and the questions that held us together. They used to do part of a lead's job for free. Now they have to be built on purpose. If your velocity chart went up this year, ask what it cost: who stopped being asked, who stopped asking, and who still admits a mistake out loud.

## References

1. Brooks, F. P. (Apr 1987). [**No Silver Bullet: Essence and Accidents of Software Engineering**](https://doi.org/10.1109/MC.1987.1663532). IEEE Computer 20(4).
2. DORA / Google Cloud (Sep 2025). [**State of AI-assisted Software Development**](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/). Google.
3. Cui, Z. K. et al. (2025). [**The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers**](https://doi.org/10.1287/mnsc.2025.00535). Management Science.
4. Brynjolfsson, E., Li, D., Raymond, L. (2025). [**Generative AI at Work**](https://doi.org/10.1093/qje/qjae044). Quarterly Journal of Economics 140(2).
5. French, J. R. P., Raven, B. (1959). **The Bases of Social Power**. In Cartwright, D. (ed.), *Studies in Social Power*, pp. 150–167. University of Michigan.
6. Mirbabaie, M. et al. (Mar 2022). [**The rise of artificial intelligence – understanding the AI identity threat at the workplace**](https://doi.org/10.1007/s12525-021-00496-x). Electronic Markets 32(1).
7. Kim, B.-J., Kim, M.-J., Lee, J. (2025). [**The dark side of artificial intelligence adoption: linking artificial intelligence adoption to employee depression via psychological safety and ethical leadership**](https://doi.org/10.1057/s41599-025-05040-2). Humanities and Social Sciences Communications 12.
8. Fernandes, D. et al. (2026). [**AI Makes You Smarter But None the Wiser: The Disconnect Between Performance and Metacognition**](https://arxiv.org/abs/2409.16708). Computers in Human Behavior 175. arXiv:2409.16708
9. Anderson, C. et al. (2012). [**A status-enhancement account of overconfidence**](https://doi.org/10.1037/a0029395). Journal of Personality and Social Psychology 103(4).
10. Baumeister, R. F., Leary, M. R. (1995). [**The Need to Belong: Desire for Interpersonal Attachments as a Fundamental Human Motivation**](https://doi.org/10.1037/0033-2909.117.3.497). Psychological Bulletin 117(3).
11. Moll, J. et al. (Oct 2006). [**Human fronto-mesolimbic networks guide decisions about charitable donation**](https://doi.org/10.1073/pnas.0604475103). PNAS 103(42).
12. Hoffmann, M. et al. (2024). [**Generative AI and the Nature of Work**](https://www.hbs.edu/faculty/Pages/item.aspx?num=66044). Harvard Business School Working Paper 25-021.
13. Tang, P. M. et al. (2023). [**No Person Is an Island: Unpacking the Work and After-Work Consequences of Interacting With Artificial Intelligence**](https://doi.org/10.1037/apl0001103). Journal of Applied Psychology 108(11).
14. Jecker, J., Landy, D. (1969). [**Liking a Person as a Function of Doing Him a Favour**](https://doi.org/10.1177/001872676902200407). Human Relations 22(4).
15. Orosz, G. (May 2025). [**Stack overflow is almost dead**](https://blog.pragmaticengineer.com/stack-overflow-is-almost-dead/). The Pragmatic Engineer.
16. Wegner, D. M. (1987). [**Transactive Memory: A Contemporary Analysis of the Group Mind**](https://doi.org/10.1007/978-1-4612-4634-3_9). In Mullen, B., Goethals, G. (eds.), *Theories of Group Behavior*. Springer.
17. Hargadon, A., Bechky, B. (2006). [**When Collections of Creatives Become Creative Collectives: A Field Study of Problem Solving at Work**](https://ideas.repec.org/a/inm/ororsc/v17y2006i4p484-500.html). Organization Science 17(4).
18. Doshi, A. R., Hauser, O. P. (Jul 2024). [**Generative AI enhances individual creativity but reduces the collective diversity of novel content**](https://doi.org/10.1126/sciadv.adn5290). Science Advances 10(28).
19. Edmondson, A. C. (1996). [**Learning from Mistakes Is Easier Said Than Done: Group and Organizational Influences on the Detection and Correction of Human Error**](https://doi.org/10.1177/0021886396321001). Journal of Applied Behavioral Science 32(1).

*DORA findings are correlational. The identity-threat, psychological-safety and loneliness studies rely on self-reported surveys. The Stack Overflow figure comes from public question counts, not a peer-reviewed study.*
