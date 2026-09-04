# Workflow 5: Reference Management

**Purpose:** Manage and enrich reference collections.

**Uses:** [Dedup Engine](../dedup-engine.md) — for 5a (related papers overlap).

When a step invokes `scripts/format-converter.py`, its secure export path is Windows-only. On non-Windows platforms it must fail closed before path, network, conversion, or write operations, and any item or batch error must produce a non-zero CLI exit.

## 5a. Find Related Papers

1. Fetch source paper metadata via direct NCBI E-utilities `efetch.fcgi?db=pubmed` — `pubmed_fetch_articles` is NOT bundled in this environment (see [MCP tools and shared modules](../../static/core/tools.md) part (b)).
2. Discover related articles via OpenAlex `related_works` (direct HTTP; resolve the work via `scripts/academic_search.py`) or NCBI `elink.fcgi` — `pubmed_find_related` is NOT bundled.
3. Filter by relevance, date, or journal.
4. Deduplicate against source using [Dedup Engine](../dedup-engine.md).
5. Present with context notes.

## 5b. BibTeX Generation

1. DOI → direct Crossref REST `GET /works/{doi}` (not `search_crossref`) → format as BibTeX.
2. PMID → direct NCBI E-utilities `efetch.fcgi?db=pubmed` (not `pubmed_fetch_articles`) → format as BibTeX.
3. Batch: process multiple IDs via `scripts/format-converter.py`; require an exact user-approved existing absolute output directory and pass it with `--output`.
4. Clean: deduplicate by citation key, sort, validate required fields.
   See [BibTeX Format](../ris-bibtex-format.md#bibtex-format) for field requirements.

## 5c. ID Conversion

1. Accept DOI, PMID, or PMCID (up to 50).
2. Convert via the direct NCBI ID Converter API (`https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/`) — `pubmed_convert_ids` is NOT bundled.
3. Fetch metadata for newly resolved IDs via direct NCBI E-utilities `efetch.fcgi?db=pubmed`.

## 5d. Citation Formatting

1. Accept PMIDs.
2. Use `scripts/format-converter.py` (or Crossref content negotiation) for APA / MLA / BibTeX / RIS output — `pubmed_format_citations` is NOT bundled. For the script, pass an exact user-approved existing absolute output directory with `--output`.

## 5e. Full-Text Access

1. Direct NCBI E-utilities `efetch.fcgi?db=pmc&id={pmcid}` for articles with open-access PMC copies (structured JATS) — `pubmed_fetch_fulltext` is NOT bundled.
2. Paywalled articles: no `download_paper` tool exists here — do not attempt downloads; report metadata-only, or use the host's built-in web search for legal open-access copies.
3. Report: structured text / PDF-as-text / metadata-only.
