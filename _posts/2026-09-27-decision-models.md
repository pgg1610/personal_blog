---
layout: post
title: Decision models and the return of the specialist
date: 2026-09-27
description: Type-constrained models for routing and classification feel like an ode to the pre-ChatGPT era, rebuilt on modern infrastructure.
tags: [ai]
---

Looking back, Jev might go down as one of the most successful AI launches of 2026. Jev is a new model from TypeSafe AI, released earlier this month. It is easy to dismiss as "just a classifier." Feed it text, and instead of words it returns numbers: a probability for a yes/no question, a distribution over a set of choices, or a score along a defined range. 

Think of it as the beginning of a class of specialized models that are type-constrained and built for routing and classification. In some ways it is an ode to the pre-ChatGPT era of modeling: encoder models, classification heads, structured outputs - the core basis of machine learning before chatbots (and now agents) made generation the center of everything. What is new is the packaging. These models run on good engineering infrastructure, exposed as a simple service, and they generalize well enough that you do not need a specialized fine-tuned model for each new task.

That combination is what makes it exciting. From the infrastructure and excitement around autoregressive, general-purpose LLMs, we now have the engineering discipline and the interest to treat a typed, specialized model as a product: a service with an API, a price, and a reliability story.

## How Jev works

The basic shape is simple. You compose a "state"—a string, a list of strings, or a set of name-value pairs describing anything: an article, a customer record, an incident report. You attach one or more questions to that state and send it to the API. Three question types cover most decisions:

- **Noul** questions (named after Bernoulli) pose a statement and return a number between 0 and 1—how confident the model is that the statement is true.
- **Choice** questions ask the model to pick from options you provide, and return a full probability distribution over them.
- **Score** questions let you define numeric levels with descriptions, and the model returns a score somewhere along that range.

All questions attached to a state are evaluated in parallel, so asking ten questions costs about the same latency as asking one. Pricing is per input token only—the output is free—and the first model costs $0.042 per million input tokens, cheaper than GPT-5 Nano. Simon Willison has a [good write-up of the API and its design](https://simonwillison.net/2026/Sep/21/jev/); his experiment with search reranking (BM25 to fetch candidates, Jev to rescore them) is a nice example of the shape of task these models fit.

The [jaggedness documentation](https://docs.typesafe.ai/model-jaggedness/jev-1.13) for Jev 1.13 notes weaknesses with numbers, dates, and adversarial content. These are not models for open-ended reasoning. They are models for decisions.

## Working with decision models

Sean Goedecke has been writing a thoughtful series on System One models, and his notes on programming with them are the most useful thing I have read on the subject. Two ideas in particular have shaped how I think these models will be used.

The first is what he calls **setting tiered goals**. In his Doom-playing experiment, feeding raw game states and choices straight to the model did not work well: a single forward pass is enough time to react, but not enough to derive a short-term plan. The model simply held down the shoot button. The fix was to periodically ask the model to pick a short-term goal—"collect armor," "kill enemies"—and then include that goal in the fast inner-loop prompt. Stacked at different time scales, this looks a lot like the goal hierarchies familiar from game and robotics AI: a slow loop for strategy, a faster loop for tactics, and a tight inner loop for actions. It is reasoning reframed as layered decisions rather than generated text.

The second is **tournament sampling**. When the number of options is large—his example is a Wikipedia page with over a thousand links—a single choice question falls apart (Jev caps at 255 choices, and accuracy degrades well before that). Instead of scoring options absolutely, present them in batches of a hundred, keep the winners, and run another round. Relative judgments are much easier for these models than absolute ratings, and in his hands the tournament found the ideal three-link path. The same pattern would work for prioritizing a long queue of samples or narrowing a large set of candidate routes.

There is a deeper observation in another of his posts: a well-prompted System One model can **distill itself into a cheaper replacement**. Because the model must be prompted for a specific task, every successful deployment quietly assembles a labeled dataset—inputs in, decisions out. Once the prompt is stable and the logs are collected, a small dedicated classifier can be trained on exactly that data, at lower cost and latency. It is a refreshingly practical view of generalization: the general model earns its place by making the first version cheap, and gracefully works itself out of a job if the task proves permanent.

## Why this matters for agents and laboratories

For agentic systems, this is a natural fit. Most of the steps in an agent workflow are not open-ended generation; they are routing and triage. Which tool should handle this? Is this result good enough to accept? Should this failure be retried or escalated? Those are classification questions, and a fast, cheap, calibrated model is a better tool for them than a large generative one. It would work well as a model router or an agent router, deciding which specialist to call before spending tokens on the expensive one.

The same logic applies in the laboratory. A lot of scientific work is quietly classification: sorting objects, triaging requests, routing paperwork. A model like this could quickly classify samples or instruments in a lab, or route forms in a health and safety evaluation (HSE) context—deciding which hazard category an incident belongs to, or which review path a request should take. These are exactly the kind of high-volume, low-glamour decisions where a typed output with a confidence score is more useful than a paragraph of fluent text.

A recent paper shows how well this "first opinion" idea holds up under scrutiny. In [*Jev-as-a-Judge: Accept When Confident, Escalate When Unsure*](https://arxiv.org/abs/2609.26550), Li and colleagues at Carnegie Mellon ran Jev as a cheap evaluator against sixteen generative and reward-model judges, with blinded human adjudication. On ordinary preference and evidence-grounded factuality, it lands within three percentage points of a state-of-the-art LLM judge at 0.36% of the fee. The interesting part is where the gaps concentrate: derivation-checking and elaborately written wrong answers—and, on several benchmarks, Jev's disadvantage clusters in its own low-confidence decisions. So they gate on the confidence score: accept the cheap verdict when it is confident, escalate the rest to the stronger judge. On held-out preference pairs, the cascade keeps about 99% of the strong judge's accuracy at roughly 57% of its cost. The threshold has to be validated for each workload (confidence is a useful ranking signal, not a certificate of correctness), but the shape of the result is compelling. A cheap first opinion works—if you know when to get a second one. This is also close to how I would want triage working in a laboratory or an HSE process: the fast model handles the routine, and anything it is unsure about goes to a person or a stronger system with the context attached.

## The specialist returns

For a few years, the field converged on one answer for everything: a large, general, autoregressive model. The pendulum is now swinging back toward specialization, but with better tools. Where the pre-ChatGPT era gave us a fragmented landscape of single-purpose models, each brittle and each requiring its own pipeline, this generation of decision models is general enough to skip per-task fine-tuning while still returning typed, constrained outputs.

If this holds, specialized typed models become a new kind of infrastructure: cheap services you call to make a decision, sitting between raw data and the larger reasoning systems that act on it. Not a replacement for LLMs, but a complement—a fast, well-engineered first opinion.

One footnote worth adding, from Nandakishor Mukkunnoth of ConvAI Innovations, who wrote a candid account of [building a System 1 decision model a year before Jev](https://laya.convaiinnovations.com/). His [SalesRLAgent paper on arXiv](https://arxiv.org/abs/2503.23303) (March 2025) used reinforcement learning over sequence representations to output calibrated conversion probabilities in sales conversations, and a [second paper](https://arxiv.org/abs/2510.01237) formalized schema-based decisions trained the same way. Frustrated by the launch coverage, he built [Laya](https://github.com/NandhaKishorM/laya): open-weight bidirectional-encoder decision models—three checkpoints, 100+ languages, the same choice/score/noul primitives, 33 milliseconds on a single GPU, Apache 2.0. His post is equal parts memoir and technical tour, and it includes an honest limitations section: choice questions degrade beyond about twenty options, and the confidence scores need a fitted calibration temperature to become trustworthy. The pre-history matters. The idea did not arrive fully formed this month; it arrived when the engineering around it caught up.

It is fun to watch an old idea come back around, dressed in better engineering.

<img class="img-fluid rounded z-depth-1" src="{{ site.baseurl }}/assets/img/jev-raschka.png" width="1000" data-zoomable loading="lazy">

<div class="caption">
Sebastian Raschka on Jev: easy to dismiss as "just a classifier," but its generalization is the breakthrough. Source: <a href="https://sebastianraschka.com/blog/2026/jev-classification-generalization.html">Sebastian Raschka, "Jev and Generalization" (Sep 20, 2026)</a>.
</div>

<div class="references">

<h2>Further reading</h2>

<h3>Writing</h3>

<ul>
<li>
<a href="https://sebastianraschka.com/blog/2026/jev-classification-generalization.html">Jev and Generalization</a><span class="ref-meta"> &mdash; Sebastian Raschka, September 2026</span>
<span class="ref-gloss">Easy to dismiss as "just a classifier." The generalization is the real breakthrough.</span>
</li>
<li>
<a href="https://simonwillison.net/2026/Sep/21/jev/">Jev introduces a new shape of LLM &mdash; System One, aka Decision Models</a><span class="ref-meta"> &mdash; Simon Willison, September 2026</span>
<span class="ref-gloss">The API, the pricing, and a search-reranking experiment.</span>
</li>
<li>
<a href="https://www.seangoedecke.com/jev-means-structured-output-is-interesting-again/">Jev means structured output is interesting again</a><span class="ref-meta"> &mdash; Sean Goedecke, September 2026</span>
<span class="ref-gloss">Fast typed decisions as a new computational primitive.</span>
</li>
<li>
<a href="https://www.seangoedecke.com/two-techniques-for-working-with-system-one-models/">Two techniques for working with System One models</a><span class="ref-meta"> &mdash; Sean Goedecke, September 2026</span>
<span class="ref-gloss">Tiered goals and tournament sampling &mdash; the source of the middle section above.</span>
</li>
<li>
<a href="https://www.seangoedecke.com/system-one-models-can-train-their-own-replacements/">System One models can train their own replacements</a><span class="ref-meta"> &mdash; Sean Goedecke, September 2026</span>
<span class="ref-gloss">Every deployment quietly collects the data for its cheaper successor.</span>
</li>
<li>
<a href="https://laya.convaiinnovations.com/">Building a System 1 decision model before Jev</a><span class="ref-meta"> &mdash; Nandakishor Mukkunnoth, ConvAI Innovations</span>
<span class="ref-gloss">A candid account of arriving at the idea early, and building it in the open.</span>
</li>
</ul>

<h3>Research</h3>

<ul>
<li>
<a href="https://arxiv.org/abs/2609.26550">Jev-as-a-Judge: Accept When Confident, Escalate When Unsure</a><span class="ref-meta"> &mdash; Li, Miao, Krishnan &amp; Padman, arXiv, September 2026</span>
<span class="ref-gloss">A confidence-gated cascade keeps 99% of a strong judge's accuracy at a fraction of the fee.</span>
</li>
<li>
<a href="https://arxiv.org/abs/2503.23303">SalesRLAgent: Real-Time Sales Conversion Prediction with Reinforcement Learning</a><span class="ref-meta"> &mdash; Nandakishor Mukkunnoth, arXiv, March 2025</span>
<span class="ref-gloss">An early System 1 decision model.</span>
</li>
<li>
<a href="https://arxiv.org/abs/2510.01237">Confidence-Aware Routing for Large Language Model Reliability Enhancement</a><span class="ref-meta"> &mdash; Nandakishor Mukkunnoth, arXiv, September 2025</span>
<span class="ref-gloss">A formalization of schema-based decisions trained with reinforcement learning.</span>
</li>
</ul>

<h3>Watching</h3>

<ul>
<li>
<a href="https://www.youtube.com/watch?v=FQNftquDDaI">Trying Jev: the new style of AI</a><span class="ref-meta"> &mdash; ThePrimeagen</span>
</li>
<li>
<a href="https://www.youtube.com/watch?v=vj7hysh0mOI">Jev explained in 7 minutes</a><span class="ref-meta"> &mdash; Caleb writes Codes</span>
</li>
<li>
<a href="https://www.youtube.com/watch?v=TbkUKCm3CHQ">An ex-OpenAI researcher just deleted language from the LLM</a><span class="ref-meta"> &mdash; FireShip</span>
</li>
</ul>

<h3>Open source</h3>

<ul>
<li>
<a href="https://github.com/NandhaKishorM/laya">Laya</a><span class="ref-meta"> &mdash; ConvAI Innovations</span>
<span class="ref-gloss">Open-weight decision models: three checkpoints, 100+ languages, 33 ms per pass, Apache 2.0.</span>
</li>
<li>
<a href="https://github.com/Contrastive-LM/CLM">Contrastive Language Models</a><span class="ref-meta"> &mdash; CLM-8B</span>
<span class="ref-gloss">Trained contrastively on states and actions; on par with Jev at up to 9&times; lower latency.</span>
</li>
<li>
<a href="https://x.com/george_onx/status/2103189119891624205">GLiNER2.5-Decide</a><span class="ref-meta"> &mdash; George Maloney and collaborators</span>
<span class="ref-gloss">Decisions that also extract evidence and structured records.</span>
</li>
</ul>

</div>
