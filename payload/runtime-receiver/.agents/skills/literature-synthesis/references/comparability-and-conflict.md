# Comparability and conflict rules

## Classify comparability

Assign one class before integrating two claims:

- `direct`: definitions, conditions, outcome, scale, and estimand align.
- `transformable`: a declared, defensible transformation can align them.
- `contextual-only`: comparison is qualitative because important contexts differ.
- `incompatible`: the claims answer materially different questions.
- `unknown`: required fields or source depth are missing.

Never treat `contextual-only`, `incompatible`, or `unknown` rows as numerical
replicates.

## Check common incompatibilities

Inspect:

- population, sample, organism, asset universe, dataset, or material;
- experimental setting, market regime, geography, and time period;
- exposure, intervention, comparator, baseline, and control;
- outcome definition, label horizon, unit, normalization, and direction;
- design, identification assumption, preprocessing, model, and estimator;
- follow-up length, censoring, missingness, exclusions, and reporting threshold;
- uncertainty measure, multiplicity, selection, and publication status.

## Classify conflict causes

Use one or more labels:

- `definition-conflict`;
- `population-or-dataset-shift`;
- `design-or-identification-difference`;
- `measurement-difference`;
- `temporal-or-regime-difference`;
- `model-or-analysis-choice`;
- `effect-direction-or-magnitude`;
- `reporting-or-selection-bias`;
- `source-or-artifact-integrity`;
- `unresolved`.

## Build a conflict ledger

For each conflict, record:

```text
conflict_id:
claim_row_ids:
comparability_class:
conflict_labels:
shared_conditions:
material_differences:
plausible_explanations:
discriminating_evidence_needed:
resolution_status:
allowed_conclusion:
forbidden_conclusion:
```

Use `resolved-by-scope`, `resolved-by-quality`, `credible-heterogeneity`, or
`unresolved` as the resolution status. Do not use prestige, citation count,
recency, or majority vote as a resolution rule.

## Avoid false consensus

- Count independent evidence streams, not repeated publications from the same
  data or cohort.
- Separate replication from reanalysis.
- Identify shared datasets, code, assumptions, or research groups when known.
- Preserve a high-quality contrary result even when it is numerically outvoted.
- State when apparent agreement comes from compatible wording but different
  estimands.
