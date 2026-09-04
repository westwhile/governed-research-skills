# Contributing

Stable tags are immutable. Changes should be proposed on a branch and released
under a new semantic version; never rewrite an existing release tag.

## Requirements

1. Keep runtime behavior and documentation consistent.
2. Do not commit credentials, local absolute paths, raw private model sessions,
   downloaded copyrighted papers, caches, virtual environments, or governance
   backups.
3. Preserve explicit permission boundaries and fail-closed behavior.
4. Add tests for routing, validation, and security-sensitive changes.
5. Run both payload verifiers before requesting review.
6. Update the payload manifest and release metadata only in a new version.

## Versioning

- Patch: documentation or compatible defect fixes.
- Minor: backward-compatible Skill or contract additions.
- Major: changes to routing ownership, contract schemas, permission semantics,
  or other incompatible behavior.

Every stable release should use a new annotated tag and retain an immutable
payload digest.
