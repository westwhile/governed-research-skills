---
name: quant-workflow-router
description: Route quantitative research, backtest, performance, data, code-review, ML-experiment, and trading-safety tasks to the smallest ordered subset of installed quant Skills. Use when a request spans two or more quant workflow stages or when the correct quant Skill is unclear. Do not use for a single clearly named Skill — a single-stage ML experiment plan or audit goes directly to quant-ml-experiment-audit — for general statistics without a market context, or for live-trading actions that lack explicit authorization.
---

# Quant Workflow Router

Select the minimum installed Skill subset needed for the current quantitative task. Return the proposed order before work begins when more than two Skills are needed.

## Available children

| Need | Skill |
|---|---|
| Inspect market or portfolio data quality | `quant-data-audit` |
| Research or validate alpha factors | `factor-research` |
| Plan or audit quantitative ML experiments | `quant-ml-experiment-audit` |
| Review quant/data/model code | `quant-code-review` |
| Audit historical strategy execution realism | `backtest-audit` |
| Analyze performance, risk, drawdown, or attribution | `performance-attribution` |
| Review anything that can place or manage orders | `trading-safety-review` |

## Routing rules

0. This Router is a control layer, not an executable child. Never include the
   Router's own name in selected Skills; expand every route to concrete installed
   children. If a required child is unavailable, report the missing dependency
   and stop instead of returning only the Router.
1. Start with `quant-data-audit` when conclusions depend on an unaccepted dataset.
2. Use `factor-research` only for factor construction or validation.
3. Use `quant-code-review` for implementation quality, leakage, alignment, and reproducibility. Keep pure implementation and code questions here.
4. Use `quant-ml-experiment-audit` to plan or audit a financial ML experiment protocol: trial families, model comparison, negative controls, ablations, search budgets, and final-holdout selection.
5. Use `backtest-audit` after signals are frozen and enter portfolio construction.
6. Use `performance-attribution` only after return/trade evidence exists.
7. Add `trading-safety-review` whenever code may place, cancel, or rebalance orders. It never authorizes a live action.
8. Route general non-market experiments to `stats-experiment-router`, not this group.

For a full research chain, use:

`quant-data-audit → factor-research → quant-code-review → backtest-audit → performance-attribution`

Add `trading-safety-review` at the end for production or broker-facing scope.

For experiment planning, use:

`quant-data-audit → factor-research (only when factors are involved) → quant-ml-experiment-audit → quant-code-review (only when implementation is needed)`

For result audit, use:

`quant-data-audit (only when data is not yet accepted) → quant-code-review → quant-ml-experiment-audit → backtest-audit → performance-attribution`

## Hard boundaries

- Do not load the whole group by default.
- Do not treat a fitted model, synthetic test, or engineering pass as accepted real-market evidence.
- Do not infer authorization to trade, connect a broker, use credentials, or write production state.
- Do not route general sample-size questions to the quant group unless a market-study context makes the quant safeguards material.

## Output

Return:

1. selected Skills in order;
2. one-line reason for each;
3. explicitly excluded adjacent Skills;
4. any authorization or data-acceptance gate that remains.
