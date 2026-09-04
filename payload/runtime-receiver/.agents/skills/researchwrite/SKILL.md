---
name: researchwrite
description: Proposal-first scientific writing pipeline for composing, revising, or rebuilding research proposals and research-plan sections from user-supplied evidence. Use when the user asks for a scientific proposal, research plan, argument map, evidence table, section contract, supervisor-facing revision, or evidence-before-prose academic drafting. Do not use for general manuscript polishing when nature-polishing is sufficient, for reviewer reports handled by nature-reviewer, or for unsupported literature retrieval.
---

# ResearchWrite

Build scientific proposals from an auditable evidence and argument structure. The
installed profile is self-contained and Markdown-first; it does not depend on the
missing private references or the legacy DOCX exporter from the old source tree.

## Choose a mode

- `compose`: turn supplied evidence, notes, constraints, and hypotheses into a new proposal.
- `revise`: diagnose and revise an existing draft without silently changing supported claims.
- `hybrid`: preserve usable text while rebuilding weak evidence and argument layers.

State the selected mode and deliverable scope before drafting. Use
`templates/00_scope.md` when the request leaves material constraints unspecified.

## Required workflow

1. Inventory the supplied sources, results, constraints, and terminology. Record
   source-bounded facts in `templates/01_research_canon.md`.
2. Build `templates/02_evidence_table.md`. Classify every important claim as
   `evidence-backed`, `plausible-inference`, `hypothesis`, or `unsupported`.
3. Build the scientific tension, central question, thesis, supporting arguments,
   limitations, and alternatives with `templates/03_argument_map.md`.
4. Define each requested section's purpose, inputs, allowed claims, forbidden
   claims, required evidence, and validation checks with
   `templates/04_section_contracts.md`.
5. Draft only after steps 1–4 are coherent. Keep terminology aligned with
   `templates/05_style_guide.md`.
6. Run the four-layer QA contract in `references/qa-contract.md`; record material
   defects and remaining gaps in `templates/quality-check.md`.
7. For another revision round, use `templates/revision_brief.md` and change only
   the issues that failed the gate.

Read `references/workflow.md` for mode-specific details and output organization.

## Evidence rules

- Never invent sources, references, results, effect sizes, feasibility evidence,
  preliminary data, supervisor requirements, or completed work.
- Keep fact, interpretation, hypothesis, proposed method, and expected outcome
  visibly distinct.
- Downgrade or remove a claim when its support is weaker than its wording.
- Mark missing support as `[EVIDENCE NEEDED]`; do not hide the gap with fluent prose.
- Do not turn a proposed validation step into a claimed result.

## Output contract

Return the requested proposal text plus the minimum useful audit artifacts. For a
substantial compose or hybrid task, this normally means:

- `research_canon.md`
- `evidence_table.md`
- `argument_map.md`
- `section_contracts.md`
- `proposal.md`
- `quality-check.md`

Write files only to an exact user-approved path. Markdown is the authoritative
output. If the user asks for DOCX, use the runtime's supported document workflow
and render the final DOCX before claiming visual acceptance. If that capability is
not present, return Markdown and disclose the unperformed export gate.

## Local governance boundary

Read `references/runtime-boundary.md` before use. The adopted profile was accepted
offline with synthetic or user-supplied inputs; external retrieval, real Vault
access, unapproved writes, and invented evidence remain prohibited.
