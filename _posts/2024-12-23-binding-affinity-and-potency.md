---
layout: post
title: Binding tightly is not the same as working well
date: 2024-12-23
description: Why binding affinity, assay potency, and therapeutic benefit answer different questions.
tags: [science]
---

A molecule binds tightly to a protein. Does that make it a good drug?

Not by itself. It may not change the protein's function in the way we want. It may not reach the relevant tissue. It may affect other targets, or require an exposure that cannot be achieved safely.

Even before we get to those questions, two numbers used to describe a molecule's activity—Kd and IC50—need to be kept distinct. They are often discussed together, but they do not measure the same thing.

## Affinity: how strongly does it bind?

The equilibrium dissociation constant, **Kd**, describes binding affinity. For a simple one-to-one interaction at equilibrium, a lower Kd means stronger binding under the specified experimental conditions.

In that simple model, when the *free* ligand concentration equals Kd, half the target binding sites are occupied. “Free” matters: the concentration added to an experiment is not always the concentration available to bind the target.

Kd can be determined using methods such as surface plasmon resonance or isothermal titration calorimetry. For an appropriate simple kinetic model, it is also the ratio of the dissociation rate constant to the association rate constant: **Kd = koff / kon**.

Affinity is therefore not a complete description of binding behavior. Two molecules can have the same Kd and different association and dissociation rates. Nor is Kd independent of experimental conditions: temperature, buffer, and the state of the target can matter.

## Potency: how much is needed to change the measured response?

**IC50** is the concentration that produces 50% inhibition in a specified assay, relative to that assay's reference response.

It is a measure of potency in that experimental system. The readout might be enzyme activity, a cellular response, or a competitive binding signal. The assay must be described for the number to be interpretable.

A lower IC50 means less compound was needed to reach that inhibition level *in those conditions*. It does not automatically mean the compound will work at a lower dose in a patient.

Substrate concentration, incubation time, target abundance, cell permeability, and the signaling system can all affect an observed IC50. This is why comparing values from different assays without their context can be misleading.

## Related, but not interchangeable

Consider a hypothetical compound that binds a purified protein with a Kd of 10 nanomolar. In a cellular assay, it might require a much higher concentration to produce the desired response because little compound reaches the intracellular target.

The binding measurement is not necessarily wrong, and neither is the cellular result. They answer different questions.

There are relationships between binding and inhibition parameters under particular assumptions. For example, the Cheng–Prusoff relationship connects IC50 and Ki for simple competitive enzyme inhibition using the substrate concentration and Km. That is not a universal conversion from any IC50 to a Kd.

A useful habit is to ask three questions whenever a potency value appears:

- What was measured?
- Under what conditions?
- What conclusion does that measurement actually support?

## Neither number is therapeutic benefit

Potency is also different from the maximum effect a compound can produce. A molecule can be potent without producing the response we ultimately need.

Therapeutic benefit adds further requirements: sufficient exposure at the right site, an appropriate duration of action, selectivity, tolerability, and a biological mechanism that actually changes the disease.

This is especially important when building models from assay data. Treating every reported “activity” number as an interchangeable label strips away the context needed to interpret it. A prediction can look precise while its target variable is poorly defined.

The aim is not to dismiss affinity or potency. Both are valuable. It is to avoid asking either number to answer a question it was not designed to answer.

## Further reading

These notes began with [Félix Torres-Hubiche's discussion of IC50 and Kd](https://www.linkedin.com/pulse/drug-discovery-biophysics-perspective-ic50-kd-f%C3%A9lix-torres-hubiche-wgxre/). For more technical background, see the [British Journal of Pharmacology article linked in the original notes](https://doi.org/10.1111/j.1476-5381.2010.01127.x).

---

*Adapted for the blog on September 26, 2026, from a note created on December 23, 2024. The date above preserves the original note's creation date.*
