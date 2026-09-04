# Research artifact handoff contract

Use a small manifest or bounded artifact at each stage boundary. Do not require
every stage to receive the full conversation or source corpus.

## Common envelope

Every handoff must provide:

- `artifact_type` and `contract_version`;
- `research_question` and `scope`;
- `created_from` source locators or predecessor artifact IDs;
- `evidence_level` and `verification_status`;
- `allowed_claims` and `forbidden_claims`;
- `unresolved_gaps`;
- `authorization_gates`;
- `recommended_next_skill` or `recommended_delegate_router`;
- `output_locator` only when a write was authorized.

Keep source text outside the envelope when a path, DOI, stable resource ID,
manifest, hash, or bounded excerpt is enough. Never place credentials in an
artifact.

## Artifact types

### `direction-brief/v1`

Record the problem, motivation, candidate questions, decision criteria,
available evidence, excluded directions, feasibility constraints, and what
would change the direction decision. Label unsupported directions as
hypotheses.

### `search-corpus-manifest/v1`

Record the frozen search question, databases or sources, query strings, search
dates, inclusion/exclusion rules, deduplication identity, retrieved records, and
coverage limits. A search result is metadata evidence, not proof that full text
was reviewed.

### `fulltext-manifest/v1`

Record each lawful source artifact, version, access route, file or stable
locator, content hash when local, extraction status, missing pages, and rights
or access limitation. Do not represent abstract-only access as full text.

### `paper-reading-note/v1`

Record source anchors, research question, methods, data, assumptions, principal
claims, quantitative results, limitations, contradictions, figures/tables, and
reader uncertainty. Separate author claims from reader inference.

### `synthesis-matrix/v1`

Record comparable claims, evidence, methods, populations or datasets,
agreements, conflicts, missing controls, and unresolved gaps across papers.
Preserve negative and contradictory evidence. Select `literature-synthesis`
only when it is installed; this schema alone does not execute synthesis.

### `conflict-ledger/v1`

Record competing synthesis row IDs, comparability class, material differences,
conflict labels, plausible explanations, discriminating evidence, resolution
status, and the strongest currently allowed conclusion.

### `gap-register/v1`

Record the gap type, supporting synthesis rows, corpus boundary, missing
evidence, observation that would close the gap, and whether the item is
unsearched, unreported, insufficient, or a credible bounded gap.

### `innovation-ledger/v1`

Record candidate hypotheses, attack routes, assumptions, predicted
observations, attempted steps, failures, counterevidence, stop conditions, and
next decisions. Do not upgrade a route idea into a finding.

### `knowledge-packet/v1`

Record reusable concepts, source locators, confidence, prerequisites,
relationships, open questions, review date, and destination proposal. Writing
the packet into a knowledge base requires separate authorization.

### `manuscript-package/v1`

Record section goals, supported claims, figures/tables, citations, terminology,
limitations, journal constraints, and unresolved evidence gaps. Keep drafting,
polishing, citation verification, reviewer simulation, and response work as
distinct operations.

### `research-governance-receipt/v1`

Record the frozen task, code/data/source versions, run/evidence manifests,
claims, failures, limitations, privacy/export decision, reusable-pattern
eligibility, and deferred actions. A receipt does not authorize Pattern
publication, Skill creation, installation, or promotion.

## Evidence levels

Use only levels justified by the active domain contract. At minimum distinguish:

- `unverified-input`;
- `source-located`;
- `source-read`;
- `engineering-verified`;
- `domain-evaluation-eligible`;
- `domain-supported`;
- `externally-validated`.

Do not convert a lower level into a higher one merely because a later stage
completed successfully.

## Invalid handoffs

Reject or hold a handoff when:

- the source locator or predecessor artifact is missing;
- a full-text claim relies only on metadata or an abstract;
- claims cannot be mapped to supporting evidence;
- the next stage requires authorization that is absent;
- an output path is invented rather than supplied or approved;
- a development repository is named as an installed Skill;
- synthetic, sample, or engineering evidence is presented as a real research
  finding.
