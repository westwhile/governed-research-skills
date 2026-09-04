# Source routing and operations

## Source routing

See [Source Tiers & Reliability](../../references/source-tiers.md) for the complete reliability classification and fallback routing rules. The T1→T2→T3 fallback chain is the standard execution order across all workflows.

Quick guide:

| User need | Primary (T1) | Secondary (T2) | Last Resort (T3) |
|-----------|-------------|-----------------|-------------------|
| Medical / clinical | PubMed | Semantic Scholar | Google Scholar |
| Cross-disciplinary | CrossRef | Semantic Scholar | Scopus |
| Preprints / CS / physics | arXiv | bioRxiv / medRxiv | — |
| Exhaustive review | PubMed + CrossRef + arXiv | Semantic Scholar + bioRxiv/medRxiv | WoS / Scopus |
| Citation count sensitive | Semantic Scholar | CrossRef | — |
| Chinese literature | — | — | CNKI / 万方 (manual) |

## Environment setup

### API keys (this environment's profile)

In this installed profile the only identity sent is the polite-pool email, and only when the user has set it: `OPENALEX_MAILTO` / `CROSSREF_MAILTO` (scripts) or `PUBMED_EMAIL` (optional MCP layer). Do not create or request any API key.

The table below is the upstream reference for optional deployments only — none of these keys are provisioned or permitted in this profile:

| Service | Env Var | Register At | Free Tier |
|---------|---------|-------------|-----------|
| Semantic Scholar | `SEMANTIC_SCHOLAR_API_KEY` | [api.semanticscholar.org](https://api.semanticscholar.org/) | 100 req/s with key (1/s without) |
| NCBI E-utilities | `NCBI_API_KEY` | [ncbi.nlm.nih.gov/account](https://www.ncbi.nlm.nih.gov/account/) | 10 req/s with key (3/s without) |
| Elsevier / Scopus / ScienceDirect | pybliometrics config | [dev.elsevier.com](https://dev.elsevier.com/) | Depends on API entitlement |

Elsevier keys would be read from the local pybliometrics config (normally `~/.config/pybliometrics.cfg`) by the optional, inert MCP layer only; do not copy API keys anywhere, and do not create `.env` files for this skill.

### Proxy (if behind firewall, PowerShell)

```powershell
$env:http_proxy = 'http://127.0.0.1:7890'
$env:https_proxy = 'http://127.0.0.1:7890'
```

### Pre-flight check

```bash
python scripts/preflight.py
```

Run before batch operations to verify API endpoints are reachable.

### Format converter dependencies

The format converter (`scripts/format-converter.py`) uses Python stdlib only — no extra dependencies. Its secure citation-file export is Windows-only. On non-Windows platforms the CLI must fail closed before path, network, conversion, or write operations because no native writer has been verified. On Windows, run `python scripts/format-converter.py --test` to verify the conversion pipeline. Any item or batch error produces a non-zero CLI exit.

### No-MCP fallback (standalone search)

When the MCP server is not mounted (plain CLI use, skill auto-discovery, CI), the search workflow still runs via two stdlib-only scripts that hit public HTTP APIs directly — the same pattern `nature-citation/scripts/nature_citation.py` uses for CrossRef:

- **Discovery** — `scripts/academic_search.py` queries OpenAlex (free, no API key). OpenAlex indexes CrossRef, PubMed and arXiv-deposited works, so one endpoint covers journals and preprints for keyword/author search, with relevance re-ranking and author disambiguation (`--affiliation` / `--orcid` / `--list-authors`). Returns ranked JSON (title, DOI, authors, year, citations, abstract).
- **Download / convert** — `scripts/format-converter.py` turns the chosen DOIs/PMIDs/arXiv IDs into `.ris`/`.bib`/`.enw`/`.nbib` (CrossRef + PubMed + arXiv, also stdlib-only).

```powershell
# discover, then export the picks
python scripts/academic_search.py "graph neural network potentials" --limit 10 --sort cited_by_count --mailto you@example.com
# $UserApprovedCitationOutput must name an existing user-approved directory.
$outputDir = (Resolve-Path -LiteralPath $UserApprovedCitationOutput).Path
python scripts/format-converter.py --doi 10.1103/physrevlett.120.143001 --format ris --output $outputDir
```

Be polite to the OpenAlex pool: pass `--mailto` or set `OPENALEX_MAILTO` / `CROSSREF_MAILTO`. Each script reports per-source failures (HTTP 429, timeout, network) on stderr and exits non-zero, so a caller treats each source independently and continues with another tool. This fallback covers the same T1→T2→T3 sources for *discovery* via OpenAlex; the MCP path remains preferred when available (per-source tool selection, Semantic Scholar / Scopus providers).

### No-MCP execution order (this environment)

This environment has no MCP server registered. Run live retrieval in this order:

1. `scripts/academic_search.py` — OpenAlex discovery (indexes CrossRef-, PubMed- and arXiv-deposited works).
2. Direct anonymous HTTP to the public APIs — NCBI E-utilities (PubMed/MeSH), Crossref REST, arXiv API.
3. The host agent's built-in web search — identity evidence and gaps the APIs do not cover.

The bundled `mcp-server/` layer is NOT registered in this environment and must not be installed, registered, or launched without separate explicit user approval.

### MCP server runtime (optional layer — NOT registered in this environment)

The `mcp-server/` layer is optional and inert here; use it only after separate explicit user approval (see the execution order above). With approval, use uv to start the MCP server in an isolated dependency environment:

```bash
uv run --no-project --directory <mcp-server> --with "mcp>=1.0.0,<2.0.0" --with "requests>=2.28.0,<3.0.0" --with "toml>=0.10.2,<2.0.0" --with "pybliometrics>=4.4.1,<5.0.0" python academic_search_server.py
```

`search_papers` defaults to CrossRef, PubMed, and arXiv. Scopus / ScienceDirect are opt-in providers: include `scopus` / `sciencedirect` in `sources`, or call their dedicated tools. These calls use the local pybliometrics config at `~/.config/pybliometrics.cfg` and may consume Elsevier API quota.

## Error handling

- **MCP tool unavailable**: report specific failure, continue with remaining tools. If the whole MCP server is absent, switch to the No-MCP fallback (`scripts/academic_search.py` + `scripts/format-converter.py`) above.
- **No results**: broaden terms, try alternative sources, suggest user refine query.
- **Non-Windows citation-file export**: treat the platform rejection as a terminal failure; stop file export, do not retry it, and do not switch to manual file generation or another writer. At most, return citation text in chat labeled `text only; no file created`; this is not a citation-file export.
- **Windows citation-file script failure (2x)**: manual content may be written only through the converter's public `write_text_exclusive` writer and the same approved output directory. Never use an alternative write path.

## Limitations

- Google Scholar is scraped (not API-backed) — results may vary. Semantic Scholar has an official REST API but is rate-limited (1 req/s without a key, 100 req/s with one).
- Chinese literature (CNKI / 万方) not indexed by CrossRef or PubMed.
- Citation counts may be delayed (CrossRef updates monthly).
