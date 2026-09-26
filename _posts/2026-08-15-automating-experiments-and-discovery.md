---
layout: post
title: Automating the experiment is not the same as automating discovery
date: 2026-08-15
description: The hard part of laboratory automation often lives between the instruments.
tags: [automation]
---

A laboratory can contain a lot of automation without being an automated laboratory.

A liquid handler moves precise volumes. A plate reader measures a signal. An incubator maintains conditions. Each instrument can perform its own task well, while the experiment still depends on a person carrying material, translating instructions, and deciding what happens next.

That distinction is easy to miss when looking at an impressive machine. The unit of work we care about is not the instrument's operation. It is the experiment, and eventually the decision that experiment informs.

These notes began while reading [Owl Posting's discussion of laboratory robotics](https://www.owlposting.com/p/heuristics-for-lab-robotics-and-where). Its discussion of specialized instruments and robotic arms is a useful starting point for thinking about where automation helps—and where the work remains.

## The work between the boxes

Consider a simple screening workflow: dispense compounds, add cells, incubate, add a detection reagent, and read the resulting signal. There are several machines involved, but also questions that belong to no single machine.

Which plate is this? Has it spent the right amount of time in the incubator? Is the next instrument available? Did a transfer fail? Does the result justify repeating the experiment or changing it?

Connecting instruments with a robotic arm and scheduling software can address some of these handoffs. It does not automatically answer the scientific questions. Moving a plate correctly and choosing a useful experiment are different achievements.

## Possible is not the same as worthwhile

An experiment can be technically automatable without being worth automating.

The setup cost includes more than programming a motion. Someone has to translate the protocol, validate the implementation, handle exceptions, and maintain it. A repeated workflow can repay that investment. An exploratory protocol that changes every few runs may not.

Suppose configuring a workflow takes 40 hours at an illustrative cost of $100 per hour. That is $4,000 before the first useful run. Spread over 50 runs, setup alone costs $80 per run; over 1,000 runs, it costs $4. This is not a complete economic model, but it explains why repetition matters.

Research complicates the calculation because changing the procedure is often the point. A perfectly optimized workflow for yesterday's question can be the wrong tool for today's.

## Three places to reduce the effort

I find it useful to separate three layers:

- **Translation:** turning scientific intent into an executable protocol. This includes units, materials, instrument capabilities, and explicit assumptions.
- **Hardware:** making physical operations reliable and connecting them without fragile handoffs.
- **Intelligence:** choosing actions, interpreting results, recognizing uncertainty, and escalating when the system cannot safely proceed.

A language model may help with translation, but a plausible protocol is not a validated protocol. A better robot may help with execution, but it cannot rescue an experiment whose readout does not answer the question. A planning system needs both dependable tools and meaningful feedback.

## Start with the friction

Rather than asking how much of a laboratory can be automated, I would start with a smaller question: which recurring handoff consumes the most effort or introduces the most uncertainty?

It might be moving samples. It might be reconciling identifiers, preparing instrument instructions, or noticing that a run has failed before wasting another day.

Reducing that friction can make a scientist more effective without pretending to automate scientific judgment. Automating an experiment is valuable. Making it easier to run the next *useful* experiment is the larger goal.

---

*Adapted for the blog on September 26, 2026, from a note created on August 15, 2026. The date above preserves the original note's creation date.*
