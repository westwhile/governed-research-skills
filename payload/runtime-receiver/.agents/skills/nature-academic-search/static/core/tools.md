# MCP tools and shared modules

Multi-source literature search, citation verification, citation format conversion, and reference management.

The `scripts/format-converter.py` secure export path is Windows-only. On non-Windows platforms it must fail closed before path, network, conversion, or write operations, and any item or batch error must produce a non-zero CLI exit. This restriction does not turn unavailable MCP tools into callable capabilities.

## MCP tools

**This environment has no MCP server registered.** The inventory below is split into (a) the 16 tools bundled in this skill's optional `mcp-server/` layer — inert here, and never to be registered without separate user approval — and (b) external tool names from other MCP servers that are **not bundled**, each mapped to its no-MCP substitute in this environment. Do not attempt calls to any tool named on this page; use the mapped substitute instead.

### (a) Bundled in `mcp-server/` (inert — NOT registered in this environment)

These 16 tools exist only inside the optional MCP layer. They are listed for reference and become callable only if the user separately approves installing and registering that layer (see [routing-and-ops.md](routing-and-ops.md)).

#### Core search

| Tool | Source | Best For |
|------|--------|----------|
| `search_papers` | academic-search MCP | Default concurrent search across CrossRef, PubMed, arXiv; accepts opt-in Scopus / ScienceDirect sources |
| `get_paper_by_id` | academic-search MCP | DOI / PMID / arXiv ID details |
| `get_citation` | academic-search MCP | DOI-based formatted citation |
| `lookup_mesh` | academic-search MCP | MeSH term exploration |

#### Scopus / ScienceDirect tools

| Tool | Source | Best For |
|------|--------|----------|
| `search_scopus` | academic-search MCP | Scopus advanced document search |
| `get_scopus_abstract` | academic-search MCP | Scopus abstract and document metadata |
| `get_scopus_citation_overview` | academic-search MCP | Scopus citation overview |
| `search_scopus_authors` / `get_scopus_author` | academic-search MCP | Author profile search and retrieval |
| `search_scopus_affiliations` / `get_scopus_affiliation` | academic-search MCP | Affiliation search and retrieval |
| `search_scopus_serial_titles` / `get_scopus_serial_title` | academic-search MCP | Journal/source metadata |
| `get_scopus_plumx_metrics` | academic-search MCP | PlumX metrics |
| `search_sciencedirect` | academic-search MCP | ScienceDirect article search |
| `get_sciencedirect_article_metadata` | academic-search MCP | ScienceDirect article metadata |

### (b) External / not bundled — use the no-MCP substitute

These tool names come from other MCP servers (a "paper-search" MCP, a PubMed utilities MCP, external CrossRef / arXiv MCPs). None of them exist in this environment. Wherever a workflow or shared module names one of them, follow the substitute path below instead of attempting the tool call.

#### Extended search

| Tool (not bundled) | Source | No-MCP substitute |
|--------------------|--------|-------------------|
| `pubmed_search_articles` | external PubMed MCP | `scripts/academic_search.py` (OpenAlex discovery) or direct anonymous HTTP to NCBI E-utilities (`esearch.fcgi` + `efetch.fcgi`, `db=pubmed`) |
| `search_crossref` | external CrossRef MCP | Direct anonymous HTTP to Crossref REST: `GET https://api.crossref.org/works?query=...` |
| `search_arxiv` | external arXiv MCP | Direct anonymous HTTP to the arXiv API: `https://export.arxiv.org/api/query?search_query=...` |
| `get_paper_by_doi` | external CrossRef MCP | Direct Crossref REST: `GET https://api.crossref.org/works/{doi}` |
| `search_google_scholar` | paper-search MCP | Host agent's built-in web search (never scrape Google Scholar) |
| `search_semantic_scholar` | paper-search MCP | `scripts/academic_search.py` (OpenAlex citation graph) or host web search |
| `search_biorxiv` | paper-search MCP | `scripts/academic_search.py` (OpenAlex indexes bioRxiv) or host web search |
| `search_medrxiv` | paper-search MCP | `scripts/academic_search.py` (OpenAlex indexes medRxiv) or host web search |
| `search_webofscience` | paper-search MCP | Not available (no institutional access); use `scripts/academic_search.py` and disclose the coverage gap |
| `search_scopus` (paper-search) | paper-search MCP | Not available without Elsevier keys; use `scripts/academic_search.py` and disclose the coverage gap |

#### PubMed utilities

| Tool (not bundled) | Purpose | No-MCP substitute |
|--------------------|---------|-------------------|
| `pubmed_fetch_articles` | Full metadata by PMID | Direct NCBI E-utilities `efetch.fcgi?db=pubmed&id={pmid}&retmode=xml` |
| `pubmed_find_related` | Related article discovery | OpenAlex `related_works` (direct HTTP; resolve the work via `scripts/academic_search.py`), or NCBI `elink.fcgi` |
| `pubmed_format_citations` | APA / MLA / BibTeX / RIS formatting | `scripts/format-converter.py`, or Crossref content negotiation (`Accept: text/x-bibliography`) |
| `pubmed_convert_ids` | DOI ↔ PMID ↔ PMCID conversion | Direct NCBI ID Converter API `https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/` |
| `pubmed_lookup_mesh` | MeSH term exploration and hierarchy | Direct NCBI E-utilities on `db=mesh` (`esearch.fcgi` then `efetch.fcgi`) |
| `pubmed_lookup_citation` | Bibliographic citation → PMID lookup | Direct NCBI E-utilities `esearch.fcgi` with fielded bibliographic terms, or host web search |
| `pubmed_spell_check` | Query spelling suggestions | Direct NCBI E-utilities `espell.fcgi` |
| `pubmed_fetch_fulltext` | PMC full text (structured JATS) | Direct NCBI E-utilities `efetch.fcgi?db=pmc&id={pmcid}` (open-access PMC copies only) |
| `download_paper` | Paywalled full-text download | No legitimate substitute — do not attempt; report metadata-only, or use host web search for legal open-access copies |

## Shared modules

| Module | Purpose |
|--------|---------|
| [Dedup Engine](../../references/dedup-engine.md) | Unified deduplication (WFs 1, 2, 5a) |
| [Citation Parser](../../references/citation-parser.md) | Extract citations from documents (WF 2) |
| [Search Strategy](../../references/search-strategy.md) | Query construction, source selection, ranking |
| [RIS/BibTeX Format](../../references/ris-bibtex-format.md) | Format specifications and field mappings |
| [Format Converter](../../scripts/format-converter.py) | Multi-source .nbib/.ris/.bib downloader |
