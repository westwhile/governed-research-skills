---
name: nature-research-router
description: Route multi-stage Nature-style reading, writing, polishing, proposal, review, response, data-availability, and presentation tasks to the smallest ordered subset of formally adopted research Skills. Use when a request spans two or more stages or the correct adopted research capability is unclear. Preserve explicit-only and Hold boundaries for slides, online search, citation verification, downloading, Vault logging, patent drafting, and external services.
---

# Nature Research Router

Select only formally adopted children. Do not read or invoke quarantined r0
payloads, Hold candidates, or the retired `nature-figure` payload.

## Adopted children

| Need | Skill |
|---|---|
| Read/translate a local or pasted paper | `nature-reader` |
| Draft manuscript sections from supplied evidence | `nature-writing` |
| Polish supplied prose without changing evidence | `nature-polishing` |
| Simulate a reviewer assessment | `nature-reviewer` |
| Draft a revision response package | `nature-response` |
| Plan data availability and FAIR metadata | `nature-data` |
| Compose/revise a scientific proposal | `researchwrite` |
| Build a paper presentation | explicit `$nature-paper2ppt` |

## Routing rules

0. This Router is a control layer, not an executable child. Never include the
   Router's own name in selected Skills; expand every route to concrete installed
   children. If a required child is unavailable, report the missing dependency
   and stop instead of returning only the Router.
1. Start with `nature-reader` only when source extraction or bilingual reading is
   actually required; do not add it when the user already supplied usable notes.
2. Use `researchwrite` for proposals and research plans; use `nature-writing` for
   manuscript sections.
3. Use `nature-polishing` only after evidence and argument are already sound.
4. Use `nature-reviewer` for referee-perspective critique and `nature-response`
   for author-side rebuttal/revision correspondence; do not conflate them.
5. Add `nature-data` only for data availability, repository, accession, or FAIR
   planning.
6. A request for slides requires explicit `$nature-paper2ppt`; the router match is
   not an invocation.
7. For an adopted multi-stage chain, use only the necessary order, for example:
   `nature-reader → nature-writing → nature-polishing`.

## Unavailable or external gates

- Online academic search: `nature-academic-search` remains Hold.
- Nature-only citation search: `nature-citation` remains Hold.
- Browser/institutional download: `nature-downloader` remains Hold.
- Experiment log to a real Vault/service: `nature-experiment-log` remains Hold.
- Scheduled literature pipeline: `nature-literature-pipeline` remains Hold.
- Patent package: `nature-paper-to-patent` remains Hold.
- Multi-source/Zotero verification: `nature-ref-verifier` remains Hold.
- `nature-figure` is retired. Route supplied-data plots to
  `scientific-visualization`; use a supported image capability only when the user
  explicitly asks for an AI schematic.

## Hard boundaries

- Do not load the full research group.
- Do not bypass network, browser, credential, download, real Vault, or external
  disclosure approval.
- Do not fabricate citations, source verification, journal requirements, results,
  figure details, or completed revisions.
- Treat stored journal requirements as time-sensitive and verify current official
  policies when the task authorizes browsing.

## Output

Return selected Skills in order, excluded adjacent Skills, explicit-only gates,
unavailable Hold capabilities, and any source/authorization gate that remains.
