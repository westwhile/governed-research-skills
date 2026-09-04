# Changelog

All notable changes to Governed Research Skills are documented here.

## [1.0.1] - 2026-09-04

### Changed

- Replaced the real PubMed/MEDLINE test record and its generated RIS and BibTeX
  forms with an explicitly synthetic, internally consistent fixture.
- Renamed the three fixture files from `pubmed-28344011.*` to
  `pubmed-synthetic-record.*` so their provenance is unambiguous.
- Adopted the Apache License, Version 2.0, and added a project `NOTICE` file.
- Added a repository-wide license and third-party-content audit.

### Validation

- Confirmed that the synthetic NBIB source converts byte-for-byte to the
  committed RIS and BibTeX fixtures using the bundled converter.
- Rebuilt the 110-file payload manifest and normalized payload digest.
- Re-ran both independent payload verifiers and all nine Skill validators.

### Compatibility

- No Skill instructions, routing rules, executable code, schemas, or runtime
  contracts changed.
- The seven model-session results from `v1.0.0` were not rerun and are recorded
  as inherited evidence, not as a fresh `v1.0.1` execution.

## [1.0.0] - 2026-09-04

### Added

- First independently reviewed stable runtime baseline.
- Sole implicit `research-workflow-router` with explicit domain delegation.
- Nine bundled Skill and Router components.
- Frozen 110-file runtime receiver and reproducible payload manifest.
- Deterministic verification tools for Python and PowerShell.
- Passing P00, D01, C13, L01, C03, C04, and C05 runtime contracts with zero retries.

### Security and governance

- Strict raw-response validation in the frozen acceptance chain.
- Fail-closed routing and capability boundaries.
- Windows-exclusive safe citation-file output; non-Windows output fails closed.
- Sanitized release metadata derived from the sealed R79 governance baseline.

### Known limitations

- Optional delegated specialist Skills are not all bundled.
- No Manager, Default, or Kimi integration is included.
- The private baseline has not yet completed a public-license review.
