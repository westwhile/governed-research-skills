# Workflow 3: MeSH Search Strategy

**Purpose:** Build precise PubMed queries from MeSH terms.

## Procedure

1. Explore MeSH terms related to the topic via direct NCBI E-utilities on `db=mesh` (`esearch.fcgi` then `efetch.fcgi`) — `pubmed_lookup_mesh` is NOT bundled in this environment (see [MCP tools and shared modules](../../static/core/tools.md) part (b)).
2. Show term hierarchy (broader / narrower / related).
3. Construct Boolean query: MeSH terms + keywords.
   See [Query Construction](../search-strategy.md#query-construction) for templates.
4. Optionally spell-check the query via direct NCBI E-utilities `espell.fcgi` — `pubmed_spell_check` is NOT bundled.
5. Execute via direct NCBI E-utilities (`esearch.fcgi` + `efetch.fcgi`, `db=pubmed`) — `pubmed_search_articles` is NOT bundled.

## Output

Final PubMed query string, result count, and top results.
