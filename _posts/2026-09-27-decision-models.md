---
layout: post
title: Decision models and the return of the specialist
date: 2026-09-27
description: Type-constrained models for routing and classification feel like an ode to the pre-ChatGPT era, rebuilt on modern infrastructure.
tags: [ai]
---

Looking back Jev might go as one of the most successful AI launches of 2026. It is a new model TypeSafe AI released earlier this month, is easy to dismiss as "just a classifier." Feed it text, and instead of words it returns numbers: a probability for a yes/no question, a distribution over a set of choices, or a score along a defined range. 

Think of it as the beginning of a class of specialized models that are type-constrained and built for routing and classification. In some ways it is an ode to the pre-ChatGPT era of modeling: encoder models, classification heads, structured outputs - the core basis of machine learning before chatbots (and now agents) made generation the center of everything. What is new is the packaging. These models run on good engineering infrastructure, exposed as a simple service, and they generalize well enough that you do not need a specialized fine-tuned model for each new task.

That combination is what makes it exciting. From the infrastructure and excitement around autoregressive, general-purpose LLMs, we now have the engineering discipline and the interest to treat a typed, specialized model as a product: a service with an API, a price, and a reliability story.

## How Jev works

The basic shape is simple. You compose a "state"—a string, a list of strings, or a set of name-value pairs describing anything: an article, a customer record, an incident report. You attach one or more questions to that state and send it to the API. Three question types cover most decisions:

- **Noul** questions (named after Bernoulli) pose a statement and return a number between 0 and 1—how confident the model is that the statement is true.
- **Choice** questions ask the model to pick from options you provide, and return a full probability distribution over them.
- **Score** questions let you define numeric levels with descriptions, and the model returns a score somewhere along that range.

All questions attached to a state are evaluated in parallel, so asking ten questions costs about the same latency as asking one. Pricing is per input token only—the output is free—and the first model costs $0.042 per million input tokens, cheaper than GPT-5 Nano. Simon Willison has a [good write-up of the API and its design](https://simonwillison.net/2026/Sep/21/jev/); his experiment with search reranking (BM25 to fetch candidates, Jev to rescore them) is a nice example of the shape of task these models fit.

The [jaggedness documentation](https://docs.typesafe.ai/model-jaggedness/jev-1.13) for Jev 1.13 notes weaknesses with numbers, dates, and adversarial content. These are not models for open-ended reasoning. They are models for decisions.

## Why this matters for agents and laboratories

For agentic systems, this is a natural fit. Most of the steps in an agent workflow are not open-ended generation; they are routing and triage. Which tool should handle this? Is this result good enough to accept? Should this failure be retried or escalated? Those are classification questions, and a fast, cheap, calibrated model is a better tool for them than a large generative one. It would work well as a model router or an agent router, deciding which specialist to call before spending tokens on the expensive one.

The same logic applies in the laboratory. A lot of scientific work is quietly classification: sorting objects, triaging requests, routing paperwork. A model like this could quickly classify samples or instruments in a lab, or route forms in a health and safety evaluation (HSE) context—deciding which hazard category an incident belongs to, or which review path a request should take. These are exactly the kind of high-volume, low-glamour decisions where a typed output with a confidence score is more useful than a paragraph of fluent text.

## The specialist returns

For a few years, the field converged on one answer for everything: a large, general, autoregressive model. The pendulum is now swinging back toward specialization, but with better tools. Where the pre-ChatGPT era gave us a fragmented landscape of single-purpose models, each brittle and each requiring its own pipeline, this generation of decision models is general enough to skip per-task fine-tuning while still returning typed, constrained outputs.

If this holds, specialized typed models become a new kind of infrastructure: cheap services you call to make a decision, sitting between raw data and the larger reasoning systems that act on it. Not a replacement for LLMs, but a complement—a fast, well-engineered first opinion.

It is fun to watch an old idea come back around, dressed in better engineering.

<img class="img-fluid rounded z-depth-1" src="{{ site.baseurl }}/assets/img/jev-raschka.png" width="1000" data-zoomable loading="lazy">

<div class="caption">
Sebastian Raschka on Jev: easy to dismiss as "just a classifier," but its generalization is the breakthrough. Source: <a href="https://sebastianraschka.com/blog/2026/jev-classification-generalization.html">Sebastian Raschka, "Jev and Generalization" (Sep 20, 2026)</a>.
</div>

---

*Further watching and reading: [Sebastian Raschka on Jev and generalization](https://sebastianraschka.com/blog/2026/jev-classification-generalization.html), [ThePrimeagen trying Jev](https://www.youtube.com/watch?v=FQNftquDDaI), [Caleb writes Codes explaining Jev in 7 minutes](https://www.youtube.com/watch?v=vj7hysh0mOI), [FireShip on the model that removed language](https://www.youtube.com/watch?v=TbkUKCm3CHQ). Open-source cousins worth knowing: [Laya](https://github.com/NandhaKishorM/laya), [Contrastive Language Models](https://github.com/Contrastive-LM/CLM), and [GLiNER2.5-Decide](https://x.com/george_onx/status/2103189119891624205).*
