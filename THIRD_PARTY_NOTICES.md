# Third-Party Notices

## Test data

The citation fixtures in
`payload/runtime-receiver/.agents/skills/nature-academic-search/references/`
are synthetic project-authored test data. They do not reproduce a real PubMed
record, publisher abstract, author list, affiliation, or publisher copyright
notice.

The Apache-2.0 license applies to those synthetic fixtures as part of this
repository. It does not relicense citation records or article content that a
user later retrieves from PubMed or another provider. Users remain responsible
for the rights and terms attached to retrieved material.

## Optional runtime dependencies

The following packages are named in `mcp-server/requirements.txt` but are not
vendored or redistributed in this repository:

| Package | Declared range | Upstream license |
|---|---:|---|
| `mcp` | `>=1.0.0,<2.0.0` | MIT |
| `requests` | `>=2.28.0,<3.0.0` | Apache-2.0 |
| `toml` | `>=0.10.2,<2.0.0` | MIT |
| `pybliometrics` | `>=4.4.1,<5.0.0` | MIT |

Installing those optional dependencies creates a separate environment governed
by each package and its transitive dependencies. This repository does not
bundle their source or binary distributions.

## Names and services

Names such as Nature, PubMed, Crossref, arXiv, OpenAlex, Semantic Scholar,
Scopus, ScienceDirect, OpenAI, and Codex belong to their respective owners.
Their appearance describes workflows or interoperability and does not imply
endorsement, sponsorship, or affiliation. Apache-2.0 does not grant trademark
rights beyond customary descriptive use.
