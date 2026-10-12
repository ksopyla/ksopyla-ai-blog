---
title: "AI did not make my team faster. It rewired it."
date: 2026-10-12
draft: true
description: "Leadership expects AI to speed up delivery. What I see instead: the bottleneck moved to decisions, the expertise ladder flattened, and engineers stopped asking each other for help. Field notes plus the research behind them."
tags: ["AI Leadership", "AI Engineering", "Engineering Management", "Team Culture"]
categories: ["Columns"]
showReadingTime: true
icon: "flask"
---

{{< lead >}}
Senior leadership sees AI write code in minutes and asks why the roadmap is not twice as fast. My team sees something different: the code got cheap, and three things that held the team together got quietly expensive.
{{< /lead >}}

## TL;DR

**What you will learn:**

- Why AI speeds up the feedback loop but not the decision about *what* to build, and why that is where delivery time actually goes
- How AI flattens the experience-based hierarchy in a team, and why that is harder on seniors than on juniors
- Why "I don't need to ask anyone anymore" is a hidden cost for team trust, backed by research on help-seeking and transactive memory
- Two less obvious effects: the broken apprenticeship pipeline and the collapse of output as a signal of skill
- Five things I am trying as a lead to counter this

In my [previous post](/posts/what-i-learned-leading-ai-engineering-team/) I wrote about the practices that kept my team sane once agents entered the loop. This one is about the forces underneath: what AI changes in the *structure* of an engineering team, beyond the tooling. Some of it is good. Some of it is destructive if nobody notices. These are my observations, tested against the research I could find.

<!-- TODO(Krzysztof): add a short personal opening scene — e.g. the meeting where someone said "AI can build it in a week, why is this a quarter?" -->

## 1. The code was never the bottleneck

The expectation from above is simple: AI writes code faster, so features ship faster, so the roadmap should compress. The first half is true. The rest does not follow.

In modern product engineering, typing code was rarely the constraint. The constraint is knowing what to build. A well-defined roadmap for the next three months is close to impossible to have, and that is not a planning failure. It is the nature of the work. We run in sprints whose goals should be defined by user value: something a user can do, try, and react to. AI can shorten the path from idea to a clickable thing in front of a user. It cannot shorten the time it takes users to change their behavior, stakeholders to agree on what "done" means, or the team to learn which feature sticks.

Fred Brooks called this forty years ago. In *No Silver Bullet* he split software difficulty into *accidental* complexity (the friction of tools and languages) and *essential* complexity (deciding what the system should do) [1]. AI is the best attack on accidental complexity we have ever had. It barely touches the essential part.

The data matches this. Faros AI analysed telemetry from more than 10,000 developers across 1,255 teams. On teams with high AI adoption, developers completed 21% more tasks and merged 98% more PRs, but PR review time went up 91% and average PR size grew 154%. Their summary: *"Any correlation between AI adoption and key performance metrics evaporates at the company level"* [2]. Downstream bottlenecks ate the gains. That is Theory of Constraints in a sentence: speeding up a station that is not the bottleneck only builds a bigger pile in front of the one that is.

The DORA 2025 report frames it as amplification: *"AI's primary role in software development is that of an amplifier. It magnifies the strengths of high-performing organisations and the dysfunctions of struggling ones"* [3]. In DORA 2024, a 25% increase in AI adoption was associated with a 1.5% *drop* in delivery throughput and a 7.2% drop in delivery stability [4]. These are correlations, not causal effects, but they point the same way.

And then there is perception. In METR's randomized trial, 16 experienced open-source developers expected AI to make them 24% faster. With AI they took 19% longer. Afterwards they still believed they had been about 20% faster [5]. The authors call it a snapshot of early-2025 tools, and the tools have improved since. My point is not that AI makes developers slower. It is that *felt* speed and *measured* speed can diverge, and leadership expectations are usually built on the felt one.

**The less obvious consequence:** cheap prototypes create more decisions, not fewer. When a team can produce three working variants in a day, someone has to choose between them, align stakeholders, and say no to two. That load lands on product managers and leads, and it does not scale with tokens. In my experience, AI moves the bottleneck from engineers to the people who decide. If those people are already the constraint, faster engineering makes their queue longer.

<!-- TODO(Krzysztof): concrete example from Pearson (anonymized) — a feature built quickly that sat waiting for a decision, or was built and then dropped after user feedback. -->

## 2. The ladder of expertise is flattening

Before AI, a team had a natural hierarchy that nobody wrote down. It was not the org chart. It was built from experience: the person who had debugged the payment service at 3 a.m. twice, the one who knew why the schema looked weird, the one whose code review comments you learned to fear. Juniors climbed that ladder by accumulating knowledge, and the climb itself gave people confidence and identity.

AI compresses that gradient. The best evidence comes from outside software but the pattern is consistent:

- In a study of 5,179 customer support agents, AI assistance raised resolved issues per hour by 14% on average and by 34% for novice and low-skilled workers, with minimal gains for the most experienced [6]. The published version describes the AI as spreading top performers' best practices to everyone else, with the most skilled seeing *"small gains in speed and small declines in quality"* [7].
- In the BCG experiment with 758 consultants, below-average performers improved by 43% and above-average performers by 17% on tasks inside the AI's capability frontier [8].
- In three field experiments with 4,867 developers at Microsoft, Accenture and a Fortune 100 company, AI raised completed tasks by about 26%, and less experienced developers adopted more and gained more [9].

On paper, that is great news: juniors get productive faster. In a team, it does something subtle to the seniors. Part of their status rested on knowledge that is now one prompt away. In the classic French and Raven taxonomy of social power, this is *expert power*: influence that comes from knowing more [10]. AI devalues the cheap half of expert power (recall of syntax, APIs, tricks) and leaves the expensive half (judgment about trade-offs, context, consequences).

My opinion: this is why some experienced engineers are quietly losing confidence. Not because they got worse, but because the visible markers of their expertise stopped being rare. And the role they are being pushed into, reviewing a growing stream of AI-generated diffs, is the least rewarding version of seniority. CodeRabbit's analysis of 470 open-source PRs found 1.7× more issues in AI-co-authored PRs than in human-only ones, including 75% more logic errors [11]. Seniors catch those. Nobody gives them credit for it.

There is also a calibration problem on the other side. Fernandes et al. found that AI raised participants' scores on reasoning tasks by about 3 points, while participants overestimated their performance by about 4. The usual Dunning-Kruger pattern disappeared: *everyone* overestimated, and higher AI literacy came with worse self-assessment [12]. A flattened ladder where everyone feels senior is not the same as a team where everyone is senior.

**Counterpoint I take seriously:** the old hierarchy was not always fair. Tenure is not wisdom. Some "experts" were gatekeepers who hoarded knowledge to stay indispensable, and AI removes their leverage. That part I do not miss. The goal is not to restore the old ladder. It is to build a new one on judgment instead of recall.

## 3. Nobody needs to ask anymore

Before AI, nobody on a team was self-sufficient. One person was the SQL master. Another could write a Python one-liner for anything. Another knew the cloud deployment well enough to fix your broken pipeline in ten minutes. You had to walk over (or ping on Slack) and ask.

Those small requests did more than unblock work. They built the team.

Now an engineer can get the SQL query, the one-liner, and the Terraform fix from an assistant without talking to anyone. It is faster. It is also lonelier, and it removes the micro-interactions that make a group of individuals into a team.

There is evidence that this is happening at scale:

- **Public help-seeking dropped.** After ChatGPT's release, posting on Stack Overflow fell by about 25% relative to comparable sites within six months, and the drop was not limited to low-quality questions [13].
- **Work becomes less collaborative.** A natural experiment on about 187,000 GitHub developers found that Copilot shifts work towards core coding and away from project management and collaboration, toward more autonomous work [14].
- **AI interaction correlates with loneliness.** In four studies across four countries (N=794), employees who interacted more with AI systems reported a stronger need for affiliation, which led to more helping of coworkers, but also more loneliness, which was linked to insomnia and after-work drinking [15]. The data is partly self-reported, so I would not say "AI causes loneliness", but the direction is uncomfortable.

Why does a lost question matter? Three lines of research explain it:

1. **Help-seeking creates collective creativity.** Hargadon and Bechky studied professional service firms and found that "moments of collective creativity" were triggered by four behaviors, and the first two were *help seeking* and *help giving* [16]. The question is often the start of a better idea than the original problem.
2. **Asking for help builds liking.** The Ben Franklin effect: people who did someone a favor liked that person more afterwards [17]. Asking the SQL master for help was not only a cost to them. It was an investment in the relationship.
3. **Teams think through "who knows what".** Wegner called it transactive memory: a team stores knowledge not in each head but in the shared map of who to ask [18]. Lewis showed that the strength of this system (specialization, credibility, coordination) predicts team performance [19]. When nobody asks anyone, the map decays. The team still has experts. It just stops knowing who they are.

**The less obvious angle:** an assistant is attractive partly because it never judges you. Asking a peer means admitting you do not know something. If engineers on my team prefer a chatbot for *every* question, I read that as a signal about psychological safety, not just tooling. Edmondson's research showed that teams learn when people feel safe to admit gaps [20]. AI gives people an escape from that discomfort, and the team loses the practice of being vulnerable with each other. That practice is what lets people deliver bad news or challenge a design when it matters.

## 4. Two effects nobody puts on the slide

### The apprenticeship pipeline is breaking

Seniors became seniors by struggling with problems, asking the person next to them, and getting their code torn apart in review. If juniors delegate the struggle and do not ask anyone, both learning channels close at once.

Anthropic ran a randomized trial with 52 mostly junior engineers learning an unfamiliar async library. The AI-assisted group scored 17% lower on a follow-up quiz (50% vs 67%), with the largest gap on debugging questions, and the time saved was not statistically significant [21]. At the same time, Stanford's analysis of ADP payroll data found a 16% relative employment decline for 22–25-year-olds in the most AI-exposed occupations, while experienced workers stayed stable [22].

Put together: fewer juniors are hired, and those who are hired learn less by default. In five years, where do the seniors who can review AI output come from?

### Output stopped being a signal of skill

As a lead, I used to read a lot from a PR: how someone structured the change, what tests they wrote, what they missed. Now a clean PR can come from someone who understands the system deeply or from someone who prompted well and did not read the result. HBR and BetterUp coined the term *workslop* for AI output that "masquerades as good work, but lacks the substance to meaningfully advance a given task", and 40% of surveyed US employees had received some in the previous month [23]. Every piece of workslop moves effort from the sender to the reviewer and quietly erodes trust between them.

This makes hiring, performance reviews, and promotion decisions harder. The artifact no longer tells you who did the thinking.

## What I am trying as a lead

These are experiments, not a framework. Some will fail.

1. **Measure decision lead time, not PR count.** I try to show stakeholders how long work waits for a decision versus how long it takes to build. When the build part shrinks to days and the waiting part stays at weeks, the conversation about "why is this not faster with AI" changes.
2. **Redefine seniority around judgment.** Seniors should be visible in design reviews, ADRs, and trade-off calls, not only as the last line of defense in code review. Credit the catches.
3. **Bring back deliberate help-seeking.** Pairing sessions, "show your prompt and what it got wrong" demos, and shared skills (see [the previous post](/posts/what-i-learned-leading-ai-engineering-team/)) make knowledge flow between people again instead of through private chats.
4. **Protect the struggle for juniors.** Explain-before-merge: the author walks through an AI-generated change in their own words. It is slow. It is also the cheapest way I know to check that understanding exists behind the diff.
5. **Treat "I never ask anyone" as a signal.** In 1:1s I ask who people learned something from this week. If the answer is always "Claude", that is a conversation about team safety, not productivity.

<!-- TODO(Krzysztof): which of these have you actually tried, and what happened? Cut the ones that are pure intent. -->

## Limits and counterpoints

- Most of the research above is from 2023–2025 tools. Agents in late 2026 are more capable, and some productivity findings (METR especially) may not hold today.
- Several numbers come from vendor reports (Faros, CodeRabbit) or self-reported surveys. They show direction, not precise effect sizes.
- AI also *creates* collaboration in some teams: shared skills, prompt reviews, joint agent debugging. The loss of peer help is a default, not a law.
- Remote work already eroded many of the hallway interactions I describe. AI may be accelerating a trend rather than starting it.
- I lead applied AI teams in a large enterprise. A five-person startup or a research lab will feel these forces differently.

## Takeaway

AI does not destroy engineering leadership. It removes the accidental structure that used to do part of a leader's job for free: the bottleneck that hid in coding, the ladder that formed from experience, the trust that formed from asking for help. Those now have to be built on purpose.

## References

<!-- TODO: verify each figure against the primary source before publishing; several primary sites were unreachable during research and numbers were cross-checked via multiple secondary sources. Fetch exact titles where marked. -->

1. Brooks, F. P. (Apr 1987). **No Silver Bullet: Essence and Accidents of Software Engineering**. IEEE Computer 20(4). <!-- TODO: add link -->
2. Faros AI (Jul 2025). [**The AI Productivity Paradox Research Report**](https://www.faros.ai/blog/ai-software-engineering). Faros AI. <!-- TODO: confirm exact title -->
3. DORA / Google Cloud (Sep 2025). [**State of AI-assisted Software Development**](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/). Google.
4. DORA / Google Cloud (Oct 2024). [**Accelerate State of DevOps Report 2024**](https://dora.dev/research/2024/). Google.
5. Becker, J. et al. (Jul 2025). [**Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity**](https://arxiv.org/abs/2507.09089). METR. arXiv:2507.09089
6. Brynjolfsson, E., Li, D., Raymond, L. (Apr 2023). [**Generative AI at Work**](https://www.nber.org/papers/w31161). NBER Working Paper 31161.
7. Brynjolfsson, E., Li, D., Raymond, L. (2025). [**Generative AI at Work**](https://doi.org/10.1093/qje/qjae044). Quarterly Journal of Economics 140(2).
8. Dell'Acqua, F. et al. (Sep 2023). [**Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects of AI on Knowledge Worker Productivity and Quality**](https://papers.ssrn.com/abstract=4573321). Harvard Business School Working Paper 24-013.
9. Cui, Z. K. et al. (2025). [**The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers**](https://papers.ssrn.com/abstract=4945566). Management Science.
10. French, J. R. P., Raven, B. (1959). **The Bases of Social Power**. In Cartwright, D. (ed.), *Studies in Social Power*. <!-- TODO: cited from memory, verify -->
11. CodeRabbit (Dec 2025). [**State of AI vs Human Code Generation Report**](https://coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report). CodeRabbit.
12. Fernandes, D. et al. (2026). [**AI Makes You Smarter But None the Wiser: The Disconnect Between Performance and Metacognition**](https://arxiv.org/abs/2409.16708). Computers in Human Behavior 175. arXiv:2409.16708
13. del Rio-Chanona, R. M., Laurentsyeva, N., Wachs, J. (Sep 2024). [**Large language models reduce public knowledge sharing on online Q&A platforms**](https://academic.oup.com/pnasnexus/article/3/9/pgae400/7754871). PNAS Nexus 3(9).
14. Hoffmann, M. et al. (2024). [**Generative AI and the Nature of Work**](https://www.hbs.edu/faculty/Pages/item.aspx?num=66044). Harvard Business School Working Paper 25-021.
15. Tang, P. M. et al. (2023). [**No Person Is an Island: Unpacking the Work and After-Work Consequences of Interacting With Artificial Intelligence**](https://doi.org/10.1037/apl0001103). Journal of Applied Psychology 108(11).
16. Hargadon, A., Bechky, B. (2006). [**When Collections of Creatives Become Creative Collectives: A Field Study of Problem Solving at Work**](https://ideas.repec.org/a/inm/ororsc/v17y2006i4p484-500.html). Organization Science 17(4).
17. Jecker, J., Landy, D. (1969). **Liking a Person as a Function of Doing Him a Favour**. Human Relations 22(4).
18. Wegner, D. M. (1987). **Transactive Memory: A Contemporary Analysis of the Group Mind**. In Mullen, B., Goethals, G. (eds.), *Theories of Group Behavior*. <!-- TODO: cited from memory, verify -->
19. Lewis, K. (2003). **Measuring Transactive Memory Systems in the Field: Scale Development and Validation**. Journal of Applied Psychology 88(4).
20. Edmondson, A. (1999). **Psychological Safety and Learning Behavior in Work Teams**. Administrative Science Quarterly 44(2). <!-- TODO: cited from memory, verify -->
21. Shen, J., Tamkin, A. (Jan 2026). [**How AI assistance impacts the formation of coding skills**](https://www.anthropic.com/research/AI-assistance-coding-skills). Anthropic. arXiv:2601.20245
22. Brynjolfsson, E., Chandar, B., Chen, R. (Nov 2025). [**Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence**](https://digitaleconomy.stanford.edu/app/uploads/2025/11/CanariesintheCoalMine_Nov25.pdf). Stanford Digital Economy Lab.
23. Niederhoffer, K. et al. (Sep 2025). [**AI-Generated "Workslop" Is Destroying Productivity**](https://hbr.org/2025/09/ai-generated-workslop-is-destroying-productivity). Harvard Business Review.

*Faros AI and CodeRabbit figures are vendor-reported. DORA findings are correlational. METR and Anthropic studies are small-sample RCTs.*
