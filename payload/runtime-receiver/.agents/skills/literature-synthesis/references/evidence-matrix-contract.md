# Evidence matrix contract

Build one row per atomic claim. Do not place several claims with different
conditions or outcomes in one cell.

## Required fields

| Field | Requirement |
|---|---|
| `row_id` | Stable identifier used by synthesis statements and conflicts |
| `source_id` | Stable source identifier from the input inventory |
| `source_locator` | DOI, local artifact ID, stable URL, or supplied-note locator |
| `evidence_depth` | metadata-only / abstract-grounded / fulltext-grounded / artifact-grounded |
| `source_anchor` | Page, section, figure, table, paragraph, or note anchor |
| `claim_type` | author-claim / observation / estimate / synthesizer-inference |
| `claim` | One bounded proposition |
| `population_or_dataset` | Population, sample, corpus, market, material, or dataset |
| `setting_and_period` | Context, location, date range, regime, or experimental setting |
| `design_and_method` | Study design, model, intervention, exposure, or measurement method |
| `comparator` | Control, baseline, alternative, or none |
| `outcome_definition` | Exact outcome or estimand |
| `value_unit_direction` | Estimate, unit, normalization, and beneficial/adverse direction |
| `uncertainty` | Interval, standard error, sample variation, or not reported |
| `conditions` | Preconditions and boundary conditions |
| `limitations` | Source-reported and synthesis-detected limitations kept distinct |
| `verification_status` | verified / partially-verified / unverified / contradicted |

## Row rules

- Preserve original units and definitions before adding a transformed field.
- Record every transformation and its assumptions in a separate column.
- Keep a null or negative result; do not omit it because another source reports
  a positive result.
- Mark unavailable values as `not reported`, not zero or none.
- Use a synthesizer inference only when its supporting row IDs are explicit.
- Downgrade the row when the anchor cannot be reopened from the supplied
  artifact.

## Matrix integrity checks

Reject the matrix when source IDs are duplicated ambiguously, anchors point to
missing artifacts, evidence depth is inflated, units are silently mixed, or a
single row merges incompatible outcomes.
