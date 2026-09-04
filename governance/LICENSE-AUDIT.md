# License and Third-Party Content Audit

Audit date: 2026-09-04

Release: `v1.0.1`

Scope: every Git-tracked repository file, including the 110-file runtime
receiver

## Outcome

The repository is technically ready to be distributed under Apache License
2.0, subject to the ownership assumption below. The real PubMed record bundled
in `v1.0.0` has been removed from the `v1.0.1` tree and replaced with synthetic
project-authored fixtures in NBIB, RIS, and BibTeX formats.

The root `LICENSE` is an unmodified copy of the Apache License 2.0 text from
<https://www.apache.org/licenses/LICENSE-2.0.txt>. The root `NOTICE` identifies
the project and copyright holder. The repository can remain private while its
contents are licensed under Apache-2.0; repository visibility is a separate
administrative choice.

## Why the PubMed fixture changed

The `v1.0.0` fixture reproduced a real MEDLINE/PubMed export, including a long
publisher-supplied abstract and an explicit publisher copyright notice. NCBI
states that NLM does not claim copyright in PubMed abstracts and that journal
publishers or authors may hold those rights. The three corresponding files were
therefore replaced rather than relicensed:

- `pubmed-synthetic-record.nbib` — authored synthetic source record;
- `pubmed-synthetic-record.ris` — deterministic conversion of that source;
- `pubmed-synthetic-record.bib` — deterministic conversion of that source.

The fixture deliberately uses fictional people, institutions, journal names,
identifier values, findings, and provenance labels. Short real identifiers in
documentation and connectivity examples are retained as factual interface
examples; no abstract or article text accompanies them.

## Repository scan

The audit checked:

- copyright, license, attribution, and “all rights reserved” markers;
- abstract-bearing NBIB, RIS, and BibTeX records;
- dependency and package manifests;
- generated files, caches, logs, local paths, credentials, and binary payloads;
- references to external publishers, services, trademarks, DOIs, and PubMed
  identifiers;
- the staged diff against immutable `v1.0.0`.

No other publisher abstract, full article, downloaded paper, third-party source
distribution, vendored package, image, audio, font, or binary asset was found.
Documentation that mentions copyright is project-authored policy text. Service
and publisher names are used descriptively and are addressed in
`THIRD_PARTY_NOTICES.md`.

## Dependencies

The only dependency manifest declares four optional Python packages. None is
vendored. PyPI project metadata identifies `mcp`, `toml`, and `pybliometrics`
as MIT-licensed and `requests` as Apache-2.0. Their licenses and transitive
dependency obligations apply when a user installs them; they are not part of
this source distribution.

## License application

- Project-authored code, documentation, schemas, and synthetic fixtures in
  `v1.0.1` are offered under Apache-2.0.
- The complete unmodified license text is present at repository root.
- A root `NOTICE` is included and must be preserved as required by the license.
- `THIRD_PARTY_NOTICES.md` distinguishes project material, unbundled optional
  dependencies, retrieved user data, and nominative trademark references.
- Existing `v1.0.0` remains immutable and retains the license terms committed
  in that tag; this patch does not retroactively rewrite it.

## Ownership assumption and limits

This audit verifies repository contents and recorded provenance; it cannot
independently prove chain of title. Licensing under Apache-2.0 assumes that the
repository owner is authorized to license the project-authored code and
documentation. No conclusion is made about content users may later retrieve
from external services. This document is an engineering audit, not legal
advice; obtain qualified legal advice if ownership or redistribution rights are
uncertain.

## Official references

- Apache License 2.0: <https://www.apache.org/licenses/LICENSE-2.0.txt>
- Apache licensing FAQ: <https://www.apache.org/foundation/license-faq.html>
- NCBI website and data policies: <https://www.ncbi.nlm.nih.gov/home/about/policies/>
- GitHub repository licensing guidance:
  <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository>
- PyPI package metadata: <https://pypi.org/project/mcp/>,
  <https://pypi.org/project/requests/>, <https://pypi.org/project/toml/>, and
  <https://pypi.org/project/pybliometrics/>
