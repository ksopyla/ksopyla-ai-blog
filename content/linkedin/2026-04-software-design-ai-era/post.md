---
title: "Fundamentals just had their leverage multiplied"
date: 2026-04-26
platform: linkedin
status: draft
content_score: 0
related_blog_post: ""
---

AI did not flatten seniority. It steepened it.

Two Matt Pocock talks rearranged something in my head this weekend — "Software Fundamentals Matter More Than Ever" and his full AI Coding For Real Engineers workshop. If you lead AI engineers, block 90 minutes. Both linked below. Treat them as required watching for your senior IC track.

The thesis is the optimistic shift: people who invested years in DDD, deep modules (Ousterhout), SOLID, TDD, and vertical slices just had their leverage multiplied. The decades-old ideas are exactly what stops an agent from emitting spaghetti.

Three things stuck.

Ubiquitous language is no longer optional.
If your domain model lives in three shapes across product docs, Jira, and code, the agent picks whichever the prompt happened to nudge. Pocock has retired /grill-me into a /domain-model skill that pulls DDD vocabulary and ADRs into the design conversation before any code is written. Old practice, new urgency.

Deep modules outperform clever modules.
Ousterhout's "narrow interface, deep implementation" is now the difference between an agent that ships a feature and one that drowns in API surface. Wide interfaces leak intent. Deep modules concentrate it. The same property that makes a service maintainable for humans makes it tractable for an LLM.

Vertical slices and TDD keep the agent honest.
In the workshop he goes idea → /grill-me → PRD → vertical-slice issues → /tdd → "Ralph loops" running autonomously while he is AFK. The agent ships. The discipline doing the shipping is what we have always taught juniors. The loop just got faster.

The optimistic read: every habit your seniors built when "vibe coding" was unthinkable is now their highest-margin skill.

The uncomfortable read: teams that skipped fundamentals during the framework gold rush are the ones whose agents look most impressive in demos and most fragile in production.

I am not claiming Pocock's stack is the right one. There will be many shapes. But the shift has happened, and it rewards engineers who can express intent precisely and modules that hide complexity well.

The next 1:1 question is not "are you using AI?" It is: which fundamental do we tighten this quarter, knowing the agent will amplify whatever we already have?

Watch both:
- Software Fundamentals Matter More Than Ever → https://youtu.be/v4F1gFy-hqg
- AI Coding For Real Engineers (full workshop) → https://youtu.be/-QFHIoCo-Ko

Which fundamental do you wish your team had tightened a year ago?

#AIEngineering #SoftwareDesign #AILeadership
