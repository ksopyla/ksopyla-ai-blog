---
title: "My exam could be passed without reading: testing the test"
date: 2026-10-11
platform: linkedin
status: draft
content_score: 4.4
related_blog_post: "https://ai.ksopyla.com/projects/cogito-capability-datasets/"
visual: "Optional. A simple before/after table or chart: shortcut score per task in v0 (lookup 98%, latest 100%, count 51%) vs v2 (all at the guessing rate). Or no image: the post is short and the numbers carry it."
link_strategy: "No link in the post. After the first hour, add the project page as a comment, or reply with it to anyone who asks: https://ai.ksopyla.com/projects/cogito-capability-datasets/ (the Hugging Face collection is linked from there)."
audience: "Research peers, potential hires, Pearson leaders and colleagues who read silently. Goal: steady expert presence in evaluation and reasoning, framed as an evening hobby, no bragging."
---

The first version of my exam could be passed without reading the facts.

In the evenings I train small language models from scratch and build the exams that check whether they actually use what they read thousands of tokens earlier.

Before testing any model, I tested the exam itself with simple cheating strategies. No model at all. Version 0 failed:

→ "Where does Lumo live?" Copy the only place name in the text: 98%
→ "Where does Lumo live now?" Take the last place of whoever moves most: 100%
→ "How many visits?" Count everyone's visits, not Lumo's: 51%

A model could look smart without reading a single fact.

Version 2 closes all five shortcuts. Every question now has a guessing rate below 10%, and every item has a twin with the evidence removed. If a model still answers the twin, it found a shortcut, not the fact.

First result: a 30M model copies a sign almost perfectly (95%) but still can't find where someone lives. Now that gap means something.

The datasets are open on Hugging Face as Cogito Capability Checks.

How do you check that your evals measure what you think they measure?

#AIResearch #MachineLearning #Evaluation
