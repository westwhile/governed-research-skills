# Security Model

## Principles

- Least authority: routing does not expand permissions.
- Explicit ownership: only one implicit control router is present.
- Fail closed: missing capabilities, invalid contracts, and unsupported safe
  output paths are reported rather than bypassed.
- Byte reproducibility: every payload file is bound by size and SHA-256.
- Separation: release metadata does not contain machine-specific governance
  evidence or credentials.

## Citation-file output

The safe citation-file writer uses Windows-specific filesystem guarantees. On
non-Windows platforms the file export path fails closed before path, network,
conversion, or filesystem processing. A host must not replace it with ordinary
`open`, shell redirection, a temporary script, or an unreviewed POSIX writer.

## External services

Documentation may refer to public scholarly APIs or optional MCP integrations.
Their presence is not authorization to call them. API keys are optional runtime
inputs and must never be committed.

## Out of scope

This release does not secure an untrusted host, prove native POSIX writer safety,
authorize production trading, or validate arbitrary third-party Skills.
