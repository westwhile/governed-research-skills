# Security Policy

## Supported versions

Only the latest tagged stable release is supported.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting feature for this repository. Do
not disclose credentials, private datasets, unpublished manuscripts, local
filesystem paths, or exploit details in a public issue.

Include:

- the affected release and component;
- a minimal reproduction that contains no sensitive data;
- expected and observed behavior;
- the impact and any known containment measures.

## Security boundaries

- Installing a Skill does not grant permission to use external tools, browse,
  download content, write arbitrary files, or modify system configuration.
- API credentials must be provided through the user's own protected runtime;
  never commit them to this repository.
- Citation-file output is Windows-only in this baseline and must fail closed on
  non-Windows platforms.
- Live-trading actions, Manager updates, Default activation, and Kimi
  integration are outside this release.
