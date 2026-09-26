---
layout: post
title: An impressive agent is not necessarily a reliable one
date: 2024-12-23
description: A successful demonstration tells us what an agent can do, not how much we can depend on it.
tags: [ai, agents]
---

Watching an AI agent choose tools and finish a complicated task can be impressive. It is tempting to move directly from “it did that” to “we can give it this job.”

Those are different claims.

A demonstration establishes that a system can succeed under some conditions. Depending on it requires understanding how often it succeeds, how it fails, and whether we can recognize those failures before acting on its output.

For scientific work, that distinction matters more than how convincingly the system narrates its progress.

## How agentic does the task need to be?

I find it more useful to ask how much discretion a workflow needs than whether something deserves the label “agent.”

Some tasks have a known sequence: retrieve data, validate a schema, run an analysis, and produce a report. Others require deciding which source to consult or which calculation to perform next. The second kind benefits from flexibility, but flexibility also creates more ways to go wrong.

[Anthropic's distinction between workflows and agents](https://www.anthropic.com/research/building-effective-agents) is useful here. A predefined workflow and a model-directed process solve different problems. More autonomy is not automatically an improvement.

The goal should be enough discretion to handle the task—not the greatest possible amount of discretion.

## A scientific answer is more than a fluent response

Imagine asking an agent whether a compound has evidence of activity against a target. It searches the literature, selects a paper, extracts a number, and writes a summary.

The response may look excellent while answering the wrong question. Perhaps the number belongs to a related compound. Perhaps it is a binding measurement presented as functional activity. Perhaps the assay used a different species or experimental system.

No single spectacular failure is necessary. A small mismatch at each step can produce a confident conclusion that the evidence does not support.

This is why evaluating only the final paragraph is insufficient. We need to inspect the connection between the question, the source, the tool output, and the claim.

## What I would test before depending on it

**Repeatability.** Try the same task more than once and vary its wording. The prose need not be identical, but the important facts and conclusions should remain defensible.

**Tool selection.** Check whether the system chooses an appropriate tool, supplies valid inputs, and understands what its output means. More available tools are not necessarily better if their purposes overlap or their interfaces are unclear.

**Evidence.** Ask whether the answer can be traced to an actual source or calculation. A citation is useful only if it supports the claim attached to it.

**Failure recovery.** Introduce an unavailable service, an empty result, or malformed data. Does the agent retry appropriately, stop, or quietly invent a substitute?

**Boundaries.** Give it a task it should not complete autonomously. Can it recognize that it needs clarification, permission, or a human decision?

**Effort.** Count the time spent reviewing and correcting the result, not just the time the agent spent generating it.

## Reliability belongs to the whole system

A capable model is only part of the answer. Typed inputs, validation rules, limited permissions, useful logs, and clear stopping conditions can matter as much as another improvement in model performance.

The [Coscientist study](https://www.nature.com/articles/s41586-023-06792-0) is a useful example of language models working with tools in chemical research. Such demonstrations expand our sense of what is possible. They should also motivate the next question: what evidence would justify trusting a particular system in a particular workflow?

That evidence will look different for drafting a literature summary and controlling a physical experiment.

I do not need an agent to appear autonomous. I need to know what I can reasonably hand over to it, what still needs inspection, and what happens when it reaches its limits. A system that makes those boundaries clear may be less dazzling in a demo—and considerably more useful at work.

---

*Adapted for the blog on September 26, 2026, from an evolving note created on December 23, 2024. The date above preserves the original note's creation date, not the completion date of this essay.*
