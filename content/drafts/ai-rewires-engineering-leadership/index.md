---
title: "What AI quietly broke in my engineering team"
date: 2026-10-12
draft: true
description: "Code got cheap, but leading an engineering team got harder. Field notes on what AI erodes in a team: the filter that forced us to choose, the ladder of experience, and the habit of asking each other for help."
tags: ["AI Leadership", "AI Engineering", "Engineering Management", "Team Culture"]
categories: ["Columns"]
showReadingTime: true
icon: "flask"
---

{{< lead >}}
AI made my team's code cheap and quietly took away three things that held the team together. Leading it is harder now than before AI. This post is about that damage.
{{< /lead >}}

## TL;DR

**What you will learn:**

- Why cheap code does not shorten the roadmap, and why deciding *why* and *what* to build got harder
- How AI flattens the ladder of expertise, threatens the standing of seniors, and lets confidence beat experience
- What a team loses when nobody needs to ask anyone: relationships, the feeling of being needed, shared ideas, and honesty about mistakes
- Four things I am trying as a lead to counter it



??STORY [DETAIL]: Put the real moment here (anonymized). Who asked, in which meeting, what did you answer, and what did you think but not say?
??improve it
Begining of the year was difficult to me, there were high expections about the metrics, the Agentic coding revolution has started and everyone expectations has skyrocket. Fairly speaking even mine, but the speed of execution didn't wanted to got 3x. I felt burn down, I thought what is wrong with my team, why we cant achive the expected 3X velocity. That my realization has started, how AI started to erode the engineering management and teams. This post will focus on the negatives, but I'm still positive on AI, we need to adapt. But without noticing it is hard to adapt. 

I keep hearing a version of the same question: *if AI writes the code in minutes, why does this still take a quarter?*

It is a fair question, and the short answer is that the code was never what took a quarter. The longer answer is this post. AI made my team's code cheap, but it also removed three things that used to do part of my job as a lead for free: the cost of building, which forced us to choose; a ladder of experience, which gave people status and identity; and the habit of asking each other for help, which held the team together. None of it shows up on a velocity chart. All of it is now my job.

My [previous post](/posts/what-i-learned-leading-ai-engineering-team/) covered the practices that keep my team sane with agents in the loop. This one is about the damage underneath, so it is one-sided on purpose.

## 1. The code was never the bottleneck

The logic from above sounds airtight: AI writes code faster, so features ship faster, so the roadmap should shrink. The first step is true. The rest does not follow, because typing code was rarely what slowed us down. **The constraint is knowing what to build.**

Fred Brooks explained why forty years ago. In *No Silver Bullet* he separated the *accidental* work of software, turning a design into code, from the *essential* work of deciding what the system should be [1]. *"The hardest single part of building a software system,"* he wrote, *"is deciding precisely what to build."* That part lives in people, not in code. *"The clients do not know what they want"* until they have tried a few versions, and every round needs a human to look, react and change their mind. That loop runs at human speed.

AI is the best weapon against accidental work we have ever had, and for much of what my team does it has pushed that work close to zero. So the essential part is now almost the whole job, and it got harder.

**The *why* got harder.** Does this product fit who we are? Pearson, where I work, is a learning company, so AI tutors make sense for us: they rest on our content, our brand and the trust that teachers and learners already give us. From a team with no learning background, the same tutor is a weekend demo. When anyone can generate a working app in a day, code stops being the moat. Fit with your mission becomes the moat, and someone has to judge it.

**The *what* got harder.** When building was expensive, cost acted as a filter: we could not build everything, so we had to choose. Now every stakeholder idea arrives with a working demo, and saying no is a pure judgment call with nothing to hide behind. DORA's 2025 research found that teams adopting AI without a strong focus on users can see their performance *drop* [2]. DORA calls it the [feature factory](https://dora.dev/capabilities/user-centric-focus/): *"high activity but low impact."*

So I no longer trust tasks closed or code shipped as a measure of my team. The value sits around the code: an architecture that survives the next three requirements; long conversations with partners who want to integrate, listening until you understand their goals well enough to write them down as requirements; and the judgment to turn three similar requests into one general capability instead of three one-offs.

Even the best change I have seen comes with a trap. Clickable HTML mocks and vibe-coded prototypes now work better as requirements than spec documents: we show one to a partner and quickly learn whether we mean the same thing. Brooks saw this coming, too [1]. But he also warned that a prototype makes *"no attempt to handle the exceptions."* A mock looks finished, so people treat it as almost done. It hides everything non-functional: system scalability, a cost per session we first have to prove against the business case, an architecture elastic enough for the next partner, backups that restore in minutes. Someone still has to negotiate those with the client and turn them into requirements.

??STORY [DETAIL]: An anonymized moment when a partner saw a mock and said "great, so it's almost ready?" What did the NFR conversation look like afterwards? - remove it, it make the blog too long

?? good one, keep
Cheap prototypes also create more decisions, not fewer. When the team can build three variants in a day, someone has to pick one, align the stakeholders and say no to the other two. That load lands on product managers and leads, and it does not scale with tokens. **AI moved the bottleneck from the people who build to the people who decide**. If they were already the constraint, faster engineering only makes their queue longer.

??STORY [TENSION]: Your Pearson example (anonymized): a feature built in days that waited weeks for a decision, or was built and then dropped. How long did it wait, and what did it cost? - 

## 2. The ladder of expertise is flattening

?? I've change it review and improve the language, I've changed the examles based on our converstaional capabity: refactor to have a more decompose system (conversation, feedback, memory), cutting the latency
Before AI, my teams had a hierarchy nobody wrote down. It was not the org chart. It was built from expertise and natural inclinations: the one who loved squeezing a query from minutes to milliseconds, the one who cut the latency by 100ms by reorganizing the go-routines, the one who could keep all the dependiencies in their head and refactor the main sevice in a week. Those inclinations were noticed and appreciated, and that gave people worth and a safe place in the team.

Juniors learned by osmosis: reading good review comments on other people's PRs, overhearing the performance debbugging sessions. Then they climbed themselves: a hard problem, a struggle, a fix of their own or a question to someone who had been there. Every climb left knowledge, confidence and an identity: *I am the person who can handle this.*

AI compresses that ladder. In field experiments with nearly 5,000 developers, the less experienced adopted AI more and gained more [3]. In customer support, the most experienced agents got only *"small gains in speed and small declines in quality"* [4]. Good news for juniors. For seniors, something quieter.


?? please find a good way of transistion from my observation to the paragraphs with some evidence, now it looks distict, like written by AI, I would like users see that I have try to understand this phenomen and do a reserach on this topic, that confirms my observation
Part of a senior's standing rested on knowledge that is now one prompt away. Social psychologists French and Raven called this *expert power*: influence that comes from knowing more [5]. AI devalues the cheap half of expert power (recall of syntax, APIs, tricks) and leaves the expensive half: judgment about trade-offs, context and consequences.

For the people who were role models and figures of authority, this is an identity story, not a productivity story. Research on "AI identity threat" at work names loss of status among its central predictors [6], and a three-wave study of 381 employees found that AI adoption lowered psychological safety, which in turn raised depression [7]. When the person everyone used to ask stops being asked, they lose more than a task. They lose part of the reason they felt safe in the team.

?? remove the story
??STORY [DETAIL]: One anonymized person from your team who used to be "the one you ask". What changed for them, and how did you notice? - 


My opinion: people whose expertise rested on recall of syntax, algorithmic knowledge or understanding the maths will lose ground. People who communicate, take responsibility, push change through and think holistically will win. I used to think the hard part for seniors was becoming full-time reviewers of AI diffs. That frustration was temporary. Agents review agents now, and most of us stopped reading the generated code. The harder part is relearning the soft skills the old ladder never asked for.

?? leaders like to hear the confident people that do not consider all the potential pitfalls, so I see that less experience often got more voice, but then seniors needs to repair the damage, extend this
Then there is confidence. With AI, less experienced engineers *feel* much more capable, and they sound it. 
?? find a way to transist from above paragraph to this, it is too sharp transistion
In one study, AI raised scores on reasoning tasks by about 3 points while people overestimated their performance by about 4, and those who knew AI best judged themselves worst [8]. Confidence also sells: overconfident people gain status, because others read their confidence as competence [9]. Some senior leaders like that confidence and believe it, and the AI behind it sounds just as sure of itself.
?? good pargraph, merge better with the above two
Really experienced engineers are mostly humble. They know there is always something the team forgot, did not notice, or that someone did not say out loud. So they hedge, and they watch the room listen to the person who does not. I understand their frustration. A flattened ladder where everyone feels senior is not the same as a team where everyone is senior.

To be fair, the old ladder was not always fair. Tenure is not wisdom, and some "experts" hoarded knowledge to stay indispensable. I do not miss that. The goal is not to restore the old ladder but to build a new one on judgment instead of recall.

## 3. Nobody needs to ask anymore


?? the same opening, to schematic and repetition, start differently, start on the other side, start with psychology, what it gives to us
Before AI, nobody on my team was self-sufficient. One person was the SQL master. Another could write a Python one-liner for anything. Another could fix your broken deployment pipeline in ten minutes. You had to walk over, or ping them on Slack, and ask. Now the query, the one-liner and the Terraform fix come from an assistant. It is faster. It is also lonelier.

?? write more about the eroding the devs communities, which I really like and enjoy to be part of, I like being a part of stackoverflow, I remember my first badges and that I helped others, I've rememver when my universtity we try to solve some algorithim puzzels as a group, it was fun and each of us was responsible for part of the sollution, I remember being a part of local tech meetups and presenting my solution, taking with other like-minded people, belonging to the tribe, I remeber the ML Conferences where you can listen and collaborate with others, now it is different, is less technical, more
?? change this below
It happened outside our teams first. By May 2025, Stack Overflow was getting about as few new questions per month as in 2009, the year it launched [10]. For many of us those forums were the first place of like-minded people: a first answer, a first upvote, a first chance to help a stranger. Local meetups feel thinner to me too. The loss is not only professional: in studies across four countries, employees who worked more with AI reported more loneliness, which was linked to insomnia and drinking after work [11].
?? too much data, and feels not human, 
Inside teams, a study of about 187,000 GitHub developers found that Copilot shifts work away from collaboration and toward working alone [12]. We rarely talk about what that takes from the person who used to help. Helping feels good, and not only figuratively: in a brain-imaging study, giving to a cause activated the same reward system as receiving money [13]. Every "can you look at this?" was a small dose of being needed. When nobody asks, the helpers lose it, and with it part of the feeling that they matter.

?? building connections, good
Those requests were also the doorway to everything else. While fixing someone's query, you noticed the tennis racket behind them and asked about it, or about the kids, the hobbies, the weekend. That is how colleagues became people to each other. Benjamin Franklin famously won over a hostile fellow legislator by asking to borrow a rare book, and a 1969 experiment confirmed the effect: we like people more after doing them a favor [14]. Asking the SQL master for help was never only a cost to them. It was an investment in the relationship.

?? hudge one, for companies, extend it, separate subsection, collective creativity - this come from interaction with others, AI agents will tell you what it is known, they drift to know things - check one of my linkedin post about how agents drift to default, the real innovation cames from interaction and experimentations
The team's thinking pays a price, too. Psychologist Daniel Wegner called it *transactive memory*: a team stores knowledge not in each head but in the shared map of who knows what [15]. When nobody asks anyone, the map decays. The team still has experts. It just stops knowing who they are.

And ideas need collisions. In professional service firms, Hargadon and Bechky found that moments of collective creativity grew out of four behaviors, and the first two were asking for help and giving it [16]. A colleague's question often leads to a better idea than the original problem. AI pushes the other way: in one writing experiment, stories built on AI ideas were rated more creative one by one, but they were more alike [17]. Each person gets better. The group gets more uniform.

The cost I worry about most is honesty. An assistant never judges you, and that is part of its appeal: asking a peer means admitting you do not know. When Amy Edmondson studied hospital units in the 1990s, the better-led units recorded *more* medication errors, not fewer. Her explanation was that people there felt safe enough to report them [18]. That is the team I want: people who say "I don't know" and "I made a mistake" early, so we fix the real problem instead of discovering it a week later. Every question that goes to a chatbot instead of a colleague is one less chance to practice that honesty, and it is the same honesty people need to deliver bad news or challenge a design.


## What I am trying as a lead

These are experiments, not a framework.

?? I've changed the frist point - 
1. **Measure value, not velocity.** 

?? this is valid, but needs different explanation, rewrite it
1. **Measure decision time** - I try to show stakeholders how long work waits for a decision versus how long it takes to build, and what changed for users after it shipped. When building takes days and waiting takes weeks, the "why isn't AI making this faster?" conversation changes.
2. **Reward the people who challenge the solution.** Seniority now shows in who says "this will not scale", "the partner never asked for that" or "we are building the wrong thing". That is where I want to give credit, in design reviews, ADRs and trade-off calls.
4. **Watch who takes the blame.** When something breaks, who says "that was me"? I treat it as one of the strongest positive signals a team can give. If nobody ever does, the team is weak, however good the velocity chart looks.

3. **Share AI setups, not prompts.** Short demos of how each person actually works with AI, shared skills (more in [the previous post](/posts/what-i-learned-leading-ai-engineering-team/)), and open sessions where the team trades ideas. Knowledge flows between people again instead of disappearing into private chats.

??STORY [VOICE]: Which of these have you actually tried, and what happened? Cut the ones that are still pure intent.
some of them are my observations and intuitions, I stil struggle to show the decistion time and value - this is not simple to convince, we all are learning together (I mean I, other Enginering mangesr, tech and prodcut team and our stakeholders). I'm glad that I work with such open minded people, but this takes time. 


??remove the limits section, this could be a part of comments
## Limits

- Remote work had already removed many of the hallway moments I describe. AI may be speeding up that trend rather than starting it.
- I lead applied AI teams in a large enterprise. A five-person startup or a research lab will feel these forces differently.


## Takeaway

AI did not make leading a team easier. It took away the structure that used to do part of the job for free: the cost that forced us to choose, the ladder that gave people standing, and the questions that held us together. Those now have to be built on purpose. If your velocity chart went up this year, ask what it cost: who stopped being asked, who stopped asking, and who still admits a mistake out loud.



## References

1. Brooks, F. P. (Apr 1987). [**No Silver Bullet: Essence and Accidents of Software Engineering**](https://doi.org/10.1109/MC.1987.1663532). IEEE Computer 20(4).
2. DORA / Google Cloud (Sep 2025). [**State of AI-assisted Software Development**](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/). Google.
3. Cui, Z. K. et al. (2025). [**The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers**](https://papers.ssrn.com/abstract=4945566). Management Science.
4. Brynjolfsson, E., Li, D., Raymond, L. (2025). [**Generative AI at Work**](https://doi.org/10.1093/qje/qjae044). Quarterly Journal of Economics 140(2).
5. French, J. R. P., Raven, B. (1959). **The Bases of Social Power**. In Cartwright, D. (ed.), *Studies in Social Power*, pp. 150–167. University of Michigan.
6. Mirbabaie, M. et al. (Mar 2022). [**The rise of artificial intelligence – understanding the AI identity threat at the workplace**](https://doi.org/10.1007/s12525-021-00496-x). Electronic Markets 32(1).
7. Kim, B.-J., Kim, M.-J., Lee, J. (2025). [**The dark side of artificial intelligence adoption: linking artificial intelligence adoption to employee depression via psychological safety and ethical leadership**](https://doi.org/10.1057/s41599-025-05040-2). Humanities and Social Sciences Communications 12.
8. Fernandes, D. et al. (2026). [**AI Makes You Smarter But None the Wiser: The Disconnect Between Performance and Metacognition**](https://arxiv.org/abs/2409.16708). Computers in Human Behavior 175. arXiv:2409.16708
9. Anderson, C. et al. (2012). [**A status-enhancement account of overconfidence**](https://doi.org/10.1037/a0029395). Journal of Personality and Social Psychology 103(4).
10. Orosz, G. (May 2025). [**Stack overflow is almost dead**](https://blog.pragmaticengineer.com/stack-overflow-is-almost-dead/). The Pragmatic Engineer.
11. Tang, P. M. et al. (2023). [**No Person Is an Island: Unpacking the Work and After-Work Consequences of Interacting With Artificial Intelligence**](https://doi.org/10.1037/apl0001103). Journal of Applied Psychology 108(11).
12. Hoffmann, M. et al. (2024). [**Generative AI and the Nature of Work**](https://www.hbs.edu/faculty/Pages/item.aspx?num=66044). Harvard Business School Working Paper 25-021.
13. Moll, J. et al. (Oct 2006). [**Human fronto-mesolimbic networks guide decisions about charitable donation**](https://doi.org/10.1073/pnas.0604475103). PNAS 103(42).
14. Jecker, J., Landy, D. (1969). [**Liking a Person as a Function of Doing Him a Favour**](https://doi.org/10.1177/001872676902200407). Human Relations 22(4).
15. Wegner, D. M. (1987). [**Transactive Memory: A Contemporary Analysis of the Group Mind**](https://doi.org/10.1007/978-1-4612-4634-3_9). In Mullen, B., Goethals, G. (eds.), *Theories of Group Behavior*. Springer.
16. Hargadon, A., Bechky, B. (2006). [**When Collections of Creatives Become Creative Collectives: A Field Study of Problem Solving at Work**](https://ideas.repec.org/a/inm/ororsc/v17y2006i4p484-500.html). Organization Science 17(4).
17. Doshi, A. R., Hauser, O. P. (Jul 2024). [**Generative AI enhances individual creativity but reduces the collective diversity of novel content**](https://doi.org/10.1126/sciadv.adn5290). Science Advances 10(28).
18. Edmondson, A. C. (1996). [**Learning from Mistakes Is Easier Said Than Done: Group and Organizational Influences on the Detection and Correction of Human Error**](https://doi.org/10.1177/0021886396321001). Journal of Applied Behavioral Science 32(1).

*DORA findings are correlational. The identity-threat, psychological-safety and loneliness studies rely on self-reported surveys. The Stack Overflow figure comes from public question counts, not a peer-reviewed study.*
