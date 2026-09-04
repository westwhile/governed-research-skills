---
name: stats-experiment-router
description: Route study-planning, randomization, power, statistical-analysis, model-diagnostics, and scientific-figure tasks to the smallest ordered subset of installed statistics and experiment Skills. Use when a request spans two or more stages or the correct statistics capability is unclear. Do not use for a single clearly named Skill, for quantitative market workflows, or to turn exploratory analysis into causal evidence.
---

# Stats & Experiment Router

Choose the minimum specialist set and distinguish planning before data collection
from analysis after data collection.

## Available children

| Need | Skill |
|---|---|
| Design, randomize, block, or lay out a study before data collection | `experimental-design` |
| Compute a priori sample size, power, MDE, or power curves | `statistical-power` |
| Select tests, check assumptions, estimate effects, and report results | `statistical-analysis` |
| Implement OLS/GLM/mixed/time-series models with detailed diagnostics | `statsmodels` |
| Build or audit publication-ready scientific figures | `scientific-visualization` |

## Routing rules

0. This Router is a control layer, not an executable child. Never include the
   Router's own name in selected Skills; expand every route to concrete installed
   children. If a required child is unavailable, report the missing dependency
   and stop instead of returning only the Router.
1. For a new study, use `experimental-design` before `statistical-power`; power
   assumptions depend on the actual unit, allocation, clustering, and design.
2. For collected data, start with `statistical-analysis` when test/model selection
   is unclear.
3. Add `statsmodels` only when a specific model implementation, coefficient table,
   residual diagnostic, or rigorous inference workflow is needed.
4. Add `scientific-visualization` only when a figure is requested or graphical
   diagnostics materially support the analysis.
5. Route market data, factors, backtests, performance attribution, and trading code
   to `quant-workflow-router`, not this group.

Typical chains:

- `experimental-design → statistical-power`
- `statistical-analysis → statsmodels → scientific-visualization`

## Hard boundaries

- Do not load the entire group.
- Do not treat repeated measurements as independent replicates.
- Do not present synthetic tests as real study evidence.
- Separate assumptions, estimates, statistical significance, practical meaning,
  and causal identification.
- Do not write data or reports unless the user requested an exact output path.

## Output

Return selected Skills in order, one-line reasons, excluded adjacent Skills, and
remaining design/data/assumption gates.
