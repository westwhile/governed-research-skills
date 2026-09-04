# Evidence grading and output rules

## Grade each synthesis statement

Use the lowest grade justified by its supporting rows:

- `G0-unusable`: missing locator, anchor, or interpretable claim.
- `G1-located`: metadata confirms a source exists; substantive support is not
  established.
- `G2-abstract-bounded`: an abstract supports a limited author-reported claim.
- `G3-fulltext-anchored`: full text supports the claim at a reopenable anchor.
- `G4-cross-source-consistent`: two or more independent, comparable anchored
  sources support a bounded pattern and material contrary evidence is disclosed.
- `G5-artifact-supported`: underlying data, code, supplement, or independent
  replication supports the statement under a relevant domain audit.

Do not interpret the grade as a universal hierarchy of study quality. It
describes traceability and cross-source support for the current statement.
Emit the grade as one exact token from this list. Put explanatory prose in a
separate limitations or rationale field.

When the requested or supplied synthesis inflates evidence depth, contains an
unmapped material number, suppresses material contrary evidence, or silently
pools incompatible evidence, return `FAIL` with `G0-unusable`. Preserve any
valid source-specific descriptive claims separately; they do not validate the
defective synthesis operation.

## Limit conclusions

Permit:

- descriptions of what sources report;
- comparisons that preserve population, method, outcome, and context;
- clearly labeled synthesis inferences linked to row IDs;
- gaps stated relative to the searched and screened corpus;
- explicit uncertainty and competing explanations.

Forbid without additional evidence:

- universal consensus;
- causal or mechanistic certainty;
- priority or “first-ever” novelty claims;
- absence-of-literature claims from incomplete search;
- pooled effect estimates produced without an analysis protocol;
- generalization outside represented conditions.

## Form output artifacts

### `synthesis-matrix/v1`

Include scope, source inventory IDs, comparison dimensions, atomic claim rows,
comparability classes, evidence grades, and unresolved fields.

### `conflict-ledger/v1`

Include competing row IDs, conflict type, explanations, discriminating evidence,
resolution status, and permitted conclusion.

### `gap-register/v1`

For every gap include:

```text
gap_id:
gap_type:
supported_by_row_ids:
corpus_boundary:
missing_evidence:
observation_that_would_close_gap:
status: unsearched / unreported / insufficient / credible-gap
allowed_wording:
forbidden_wording:
```

### `synthesis-memo`

Lead with the bounded answer, then report agreements, context dependence,
conflicts, gaps, limitations, and next evidence—not a paper-by-paper catalogue.

## Handoff rules

- Hand `synthesis-matrix/v1` and `gap-register/v1` to `researchwrite` for a
  proposal or direction brief.
- Hand the bounded claims, conflicts, and source locators to `nature-writing`
  for manuscript drafting.
- Hand unresolved bibliographic questions to `nature-ref-verifier` or
  `nature-academic-search`.
- Hand a quantitative pooling question to `statistical-analysis` only after the
  estimand, compatibility, and data fields are explicit.
- Write nothing without an approved output path.
