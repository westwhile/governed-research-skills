# Workflow 4: Citation File Management

**Purpose:** Download and convert citation files.

**Uses:** `scripts/format-converter.py` — multi-source downloader (PubMed/CrossRef/arXiv) with .nbib/.ris/.bib output.

**Platform and exit contract:** secure citation-file export is Windows-only. On non-Windows platforms the converter must fail closed before path, network, conversion, or write operations. Any item or batch error produces a non-zero CLI exit; never treat partial output as a successful batch.

## Procedure

1. **Identify papers** — by PMID, DOI, arXiv ID, or search query.
2. **Resolve the approved output directory.** The caller must set `$UserApprovedCitationOutput` to an existing directory the user explicitly approved. Resolve it before invoking the converter:
   ```powershell
   $outputDir = (Resolve-Path -LiteralPath $UserApprovedCitationOutput).Path
   ```
3. **Download** via format-converter and pass the resolved path on every export:
   ```powershell
   # PubMed
   python scripts/format-converter.py --pmid 28344011 --format nbib --output $outputDir

   # CrossRef
   python scripts/format-converter.py --doi 10.1038/nature14539 --format ris --output $outputDir

   # arXiv
   python scripts/format-converter.py --arxiv 1706.03762 --format bib --output $outputDir

   # Batch from file
   python scripts/format-converter.py --input refs.txt --format ris --output $outputDir
   ```
4. **Convert format** as needed: `.nbib` (MEDLINE), `.ris` (EndNote/Zotero), `.bib` (BibTeX/LaTeX).
   Format specifications: [RIS and BibTeX Format](../ris-bibtex-format.md).
5. Write only inside `$outputDir`. The converter rejects a missing, relative, or nonexistent output directory and never creates one.
6. Verify output count matches input.

## refs.txt Format

```
PMID:28344011
DOI:10.1038/nature14539
ARXIV:1706.03762
QUERY:TB-Profiler AND Bioinformatics[Journal]
AUTHOR:Dheda TITLE:drug-resistant tuberculosis
# Lines starting with # are comments
```

## Error Modes

- **Non-Windows citation-file export:** treat the platform rejection as a terminal failure; stop file export, do not retry it, and do not switch to manual file generation or another writer. At most, return citation text in chat labeled `text only; no file created`; this is not a citation-file export.
- **Windows script failure (2x):** manual `.ris`/`.bib` content may be written only through the converter's public `write_text_exclusive` writer and the same approved output directory. Never use an alternative write path.
- **Missing, relative, or nonexistent output directory:** stop without retrieval or writes; obtain an exact approved existing directory.
- **DOI not found in CrossRef:** suggest verifying DOI spelling, trying PMID instead.
- **arXiv ID not found:** check for version suffix (v1, v2), try without it.
