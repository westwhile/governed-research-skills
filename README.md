# Governed Research Skills

> Auditable research workflows for AI agents.

[![Verify payload](https://github.com/westwhile/governed-research-skills/actions/workflows/verify.yml/badge.svg)](https://github.com/westwhile/governed-research-skills/actions/workflows/verify.yml)

Governed Research Skills is a versioned runtime bundle for structured
AI-assisted research. It combines an explicit control router with specialist
skills for literature synthesis, academic search, paper reading, research
writing, and domain delegation.

The project emphasizes:

- deterministic routing contracts;
- explicit ownership and delegation boundaries;
- fail-closed behavior when a required capability is absent;
- byte-reproducible release payloads;
- offline validation where possible;
- evidence-based governance and independent review.

[中文说明](README.zh-CN.md)

## Stable baseline

The first stable release is `v1.0.0`.

| Property | Value |
|---|---|
| Payload | `payload/runtime-receiver` |
| Files | 110 |
| Normalized SHA-256 | `5fe9a8a3e56398debdb2b4ed2799541954b4a10bb8e3e704f044c998ed8cf4a2` |
| Deployed Router SHA-256 | `6f8691c439657bf587ba2b20c61a00e935010927b739e3ec0f97c087aa9d2e3c` |
| Governance baseline | R79, sealed 2026-09-04 |
| Runtime contracts | P00, D01, C13, L01, C03, C04, C05: PASS; retries: 0 |

The normalized digest covers only the 110 files under
`payload/runtime-receiver`. Repository documentation and release metadata are
outside that payload boundary.

## Included components

| Component | Role |
|---|---|
| `research-workflow-router` | Sole implicit control router for research, quantitative, and statistics requests |
| `nature-research-router` | Explicit router for multi-stage Nature-style research workflows |
| `quant-workflow-router` | Explicit router for quantitative research workflows |
| `stats-experiment-router` | Explicit router for study design and statistical workflows |
| `literature-synthesis` | Cross-paper evidence synthesis from supplied or lawfully accessible sources |
| `nature-academic-search` | Academic search, citation verification, and citation-file management |
| `nature-literature-pipeline` | Explicit-only literature monitoring workflow contract |
| `nature-reader` | Source-grounded, figure-aware bilingual paper reading |
| `researchwrite` | Proposal-first scientific writing from supplied evidence |

Some routers describe optional specialist skills that are not vendored in this
baseline. A missing specialist is not permission to improvise its behavior: the
runtime must disclose the missing capability or fail closed.

## Verify the payload

Python 3.10 or later:

```bash
python tools/verify_payload.py
```

PowerShell 7:

```powershell
pwsh -NoProfile -File tools/verify-payload.ps1
```

Both commands verify the file set, byte sizes, individual SHA-256 values, and
the normalized payload digest against `governance/PAYLOAD-MANIFEST.csv` and
`governance/RELEASE.json`.

## Installation

The release payload is laid out as an isolated receiver. Install only the Skill
directories you intend to use:

```text
payload/runtime-receiver/.agents/skills/<skill-name>
```

Copy those directories into the target agent's Skill root. Do **not** install
`payload/runtime-receiver/AGENTS.md` as a global configuration file: it is the
frozen, read-only evaluation envelope used to reproduce the release contracts.

Review every Skill's permissions and dependencies before enabling it. This
repository does not automatically install dependencies, register MCP servers,
enable network access, update a Skill Manager, or change a system default.

## Platform boundary

Most content is platform-neutral Markdown and Python. The controlled citation
file writer in `nature-academic-search` is Windows-only and fails closed on
non-Windows systems. A failed export must not be replaced with an uncontrolled
filesystem write.

## Security and privacy

- No credentials are included.
- External network and tool access are not granted by this repository.
- Treat downloaded papers, API responses, and user data according to their
  licenses and privacy requirements.
- Report security issues using [SECURITY.md](SECURITY.md).

## Non-goals

This project does not:

- provide investment or trading advice;
- guarantee scientific correctness, novelty, or publication outcomes;
- claim that every optional delegated specialist is bundled;
- enable a system-wide default agent;
- apply Manager or Kimi configuration automatically;
- claim affiliation with OpenAI, Nature Portfolio, AAAS, Cell Press, or any
  other publisher or platform.

## Governance

The public-facing release metadata is intentionally sanitized. Internal
governance directories, local absolute paths, raw model responses, rollback
backups, and machine-specific boundary reports are not published. See
[`governance/RELEASE.json`](governance/RELEASE.json) for the bounded release
attestation.

## License

No open-source license is granted for `v1.0.0`. The repository is initially
published as a private, all-rights-reserved baseline pending a separate
licensing and third-party fixture review. See [LICENSE](LICENSE) and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
