# Workflow 1: Multi-Source Literature Search

**Purpose:** Search multiple academic databases in parallel, deduplicate, merge, and rank results.

**Prerequisites:** No MCP server is registered in this environment. Execute every search through the no-MCP substitutes mapped in [MCP tools and shared modules](../../static/core/tools.md) part (b): `scripts/academic_search.py` (OpenAlex discovery), direct anonymous HTTP to Crossref REST / NCBI E-utilities / arXiv API, and the host's built-in web search.

**Uses:** [Dedup Engine](../dedup-engine.md) — deduplication and merge preference logic.

## Procedure

1. **Analyze topic** — identify domain, consult [source routing](../search-strategy.md#source-selection).
2. **Select sources by tier** — follow [Source Tiers](../source-tiers.md). Always try T1 first; escalate to T2 only if T1 insufficient; use T3 as last resort with explicit user warning.
3. **Search in parallel** — query all relevant sources simultaneously via the no-MCP substitutes (the MCP tool names below are NOT bundled here; do not call them):
   - Biomedical → direct NCBI E-utilities HTTP (`esearch.fcgi` + `efetch.fcgi`, `db=pubmed`) or `scripts/academic_search.py` — not `pubmed_search_articles`
   - Cross-disciplinary → direct Crossref REST HTTP (`GET /works?query=...`) — not `search_crossref`
   - Preprints → direct arXiv API HTTP (`export.arxiv.org/api/query`); bioRxiv / medRxiv via OpenAlex or host web search — not `search_arxiv` / `search_biorxiv` / `search_medrxiv`
   - Exhaustive → add `scripts/academic_search.py` (OpenAlex) and the host's built-in web search — `search_semantic_scholar` / `search_webofscience` / `search_scopus` are not available here
4. **Deduplicate** — apply [Dedup Engine](../dedup-engine.md) to merged result list.
5. **Merge and rank** — sort by relevance, date, or citation count per user preference. See [Result Ranking](../search-strategy.md#result-ranking).
6. **Present results** — unified table with source labels, metadata, and abstract snippets.

## Output Format

```
**Title**: [Paper Title]
**Authors**: [Author list]
**Journal**: [Journal name]
**Year**: [Year]  |  **DOI**: [DOI]  |  **PMID**: [PMID]
**Citations**: [count if available]
**Abstract**: [First 200 characters...]
```

## Error Modes

- **MCP tool unavailable:** report specific failure, continue with remaining tools.
- **No results:** broaden terms per [Query Construction](../search-strategy.md#query-construction), try alternative sources, suggest user refine query.
- **All sources empty:** suggest MeSH strategy (Workflow 3) or manual query refinement.
