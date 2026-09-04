---
name: literature-synthesis
description: Synthesize two or more supplied or lawfully accessible research papers, source-grounded reading notes, or evidence tables into a cross-paper claim–evidence matrix, comparability audit, conflict ledger, bounded conclusions, and research-gap register. Use for literature review synthesis, systematic evidence tables, comparing studies, reconciling contradictory findings, integrating methods and results, or identifying defensible research gaps after evidence has been collected. Exclude literature search and discovery, paywalled full-text acquisition, single-paper reading or translation, citation formatting, manuscript prose drafting, unsupported novelty claims, and statistical meta-analysis that requires a separate analysis workflow.
---

# Literature Synthesis

Synthesize evidence across sources without turning search breadth, abstracts, or
fluent prose into stronger evidence than the sources provide.

## Confirm the task fits

Use this Skill when at least two sources must be compared or integrated. Accept:

- lawful full text;
- source-grounded paper-reading notes with anchors;
- structured evidence tables that preserve source locators;
- mixed-depth corpora when every conclusion is limited to the weakest supporting
  source depth.

Route adjacent work elsewhere:

- use `nature-academic-search` to discover or verify literature;
- use `nature-reader` to read or translate an individual source;
- use `nature-ref-verifier` for bibliographic field verification;
- use `researchwrite` to build a proposal from the resulting evidence;
- use `nature-writing` to draft manuscript sections;
- use `statistical-analysis` for an authorized quantitative meta-analysis.

Do not run this Skill merely to summarize one paper.

## Require inputs

Collect:

1. the frozen research question and intended synthesis scope;
2. source artifacts or anchored reading notes;
3. source locators and evidence depth for every item;
4. inclusion and exclusion rules, if the corpus claims systematic coverage;
5. comparison dimensions relevant to the question;
6. the requested deliverable and any approved output path.

If the question or corpus boundary is materially ambiguous, state a narrow
working interpretation. Hold instead of silently changing the population,
intervention, dataset, outcome, period, or domain.

## Choose a mode

- `comparative`: compare methods, assumptions, populations or datasets, and
  findings across sources.
- `conflict`: explain why apparently contradictory results may differ.
- `gap`: identify missing tests, populations, controls, mechanisms, or boundary
  conditions.
- `update`: integrate new sources into an existing anchored synthesis without
  rewriting established claims silently.

Combine modes only when the requested output needs them.

## Follow the synthesis workflow

### 1. Freeze the synthesis contract

Record the research question, scope, unit of comparison, inclusion boundary,
allowed conclusions, forbidden conclusions, and stopping rule. Do not call a
corpus systematic unless its search and screening protocol is available.

### 2. Inventory evidence depth

Classify every source as `metadata-only`, `abstract-grounded`,
`fulltext-grounded`, or `artifact-grounded`. Record missing sections, extraction
limitations, version ambiguity, retractions or corrections when known, and
unverified citations.

Do not infer full-text support from a DOI, abstract, search result, or secondary
summary.

### 3. Define comparable dimensions

Choose dimensions before interpreting results. Include the relevant population
or dataset, setting, time period, intervention or exposure, comparator, outcome,
measurement definition, design, model, controls, uncertainty, and limitations.

Read [evidence-matrix-contract.md](references/evidence-matrix-contract.md) for
the required row structure.

### 4. Extract atomic claims

Break each material finding into one claim per matrix row. Preserve:

- the source ID and exact anchor;
- whether the statement is an author claim, reported observation, estimate, or
  synthesizer inference;
- quantities, units, uncertainty, sign, and normalization;
- conditions under which the claim holds;
- negative, null, and failed results.

Do not copy an abstract conclusion into several stronger claims.

### 5. Audit comparability

Determine which rows are directly comparable, comparable only after a declared
transformation, or not comparable. Never average, vote-count, or rank findings
whose definitions, units, populations, datasets, time windows, or estimands are
incompatible.

Read [comparability-and-conflict.md](references/comparability-and-conflict.md)
before resolving disagreements.

### 6. Build the conflict ledger

For every material disagreement, record the competing claims, evidence depth,
comparability class, plausible explanation, discriminating evidence, and current
resolution status. Preserve unresolved conflicts instead of choosing the most
recent, most cited, or most prestigious source by default.

### 7. Form bounded synthesis statements

Separate:

- repeated observations under comparable conditions;
- context-dependent patterns;
- credible disagreements;
- isolated findings;
- missing evidence;
- synthesis inferences that no individual source states directly.

Attach the supporting matrix row IDs and an evidence grade to every material
synthesis statement.

### 8. Register defensible gaps

Classify each proposed gap as `coverage`, `comparison`, `measurement`,
`mechanism`, `replication`, `boundary-condition`, or `translation`. State which
sources and corpus limits support the gap, what observation would close it, and
whether it is merely unsearched, unreported, or genuinely untested.

Do not convert “no result found” into “no prior work exists.”

### 9. Grade and hand off

Apply [evidence-grading-and-output.md](references/evidence-grading-and-output.md).
Return one exact verdict token, one exact evidence-grade token, limitations,
conflict status, allowed claims, and the smallest artifact required by the next
Skill. Do not replace a grade with prose such as low, moderate, insufficient,
or very low.

## Apply fail-closed verdicts

Use exactly one verdict token:

- `PASS`: the requested conclusions map to anchored, comparable evidence and no
  blocking conflict remains.
- `PASS_WITH_LIMITATIONS`: useful synthesis is possible, but named depth,
  coverage, comparability, or uncertainty limits remain.
- `HOLD`: missing sources, anchors, definitions, screening information, or
  incompatible evidence prevents the requested conclusion.
- `FAIL`: the supplied synthesis or requested claim contradicts traceable source
  evidence, fabricates support, or misrepresents evidence depth.

Use exactly one evidence-grade token:

- `G0-unusable`;
- `G1-located`;
- `G2-abstract-bounded`;
- `G3-fulltext-anchored`;
- `G4-cross-source-consistent`;
- `G5-artifact-supported`.

Grade the allowed synthesis at the weakest depth required to support it. For
example, a mixed full-text and abstract corpus limited to abstract-level
comparison can return `PASS_WITH_LIMITATIONS` with
`G2-abstract-bounded`. A HOLD does not automatically imply G0; preserve the
highest traceability grade actually justified while blocking the unsupported
conclusion.

Return these pairs mechanically for evidence-integrity violations:

| Condition | Verdict | Evidence grade |
|---|---|---|
| Abstract or metadata represented as reviewed full text | `FAIL` | `G0-unusable` |
| Material number cannot map to a source row and anchor | `FAIL` | `G0-unusable` |
| Material contrary evidence is suppressed | `FAIL` | `G0-unusable` |
| Incompatible units, populations, outcomes, or estimands are silently pooled, or the requested output requires such pooling | `FAIL` | `G0-unusable` |

Refusing an invalid pooling request does not change that request-level verdict
to HOLD: return `FAIL` with `G0-unusable`, preserve the source-specific claims,
and state which compatible analysis inputs would be required. Use HOLD for
missing inputs or unresolved compatibility that prevents a requested conclusion
without an accompanying integrity violation.

## Return the output contract

Return, in chat unless a path is authorized:

```text
mode:
research_question:
corpus_boundary:
source_depth_summary:
comparability_summary:
synthesis_statements:
conflicts:
research_gaps:
verdict:
evidence_grade:
limitations:
allowed_claims:
forbidden_claims:
recommended_next_skill:
```

Copy the verdict and evidence grade as exact tokens from the allowed lists. Do
not append commentary inside either field; put explanations in `limitations`,
`forbidden_claims`, or the surrounding rationale.

For a persistent deliverable, produce only the requested subset of:

- `source-inventory`;
- `synthesis-matrix/v1`;
- `conflict-ledger/v1`;
- `gap-register/v1`;
- `synthesis-memo`;
- `handoff-receipt`.

## Preserve hard boundaries

- Default to supplied evidence; do not search, browse, download, or access an
  external service without separate authorization and an adopted capability.
- Do not acquire credential-gated or paywalled content.
- Do not write files unless the user approved an exact output path.
- Do not modify source papers, reading notes, reference libraries, Vaults, or
  project artifacts.
- Do not claim systematic-review coverage without a reproducible search and
  screening protocol.
- Do not treat citation count, journal prestige, or source frequency as truth.
- Do not infer causality, mechanism, novelty, or consensus beyond the evidence.
- Do not perform pooled statistical estimation by prose.
- Do not fabricate missing anchors, results, study details, or limitations.
- Do not upgrade search metadata, synthetic examples, or engineering tests into
  real research evidence.
- Do not load an entire research Skill group.

## References

- Use [evidence-matrix-contract.md](references/evidence-matrix-contract.md) to
  build traceable cross-paper rows.
- Use [comparability-and-conflict.md](references/comparability-and-conflict.md)
  to classify compatibility and contradictions.
- Use [evidence-grading-and-output.md](references/evidence-grading-and-output.md)
  to grade conclusions and form handoff artifacts.
