# Paper assets

Built only from committed results. No experiment is rerun.

| Path | What | Rebuild |
|---|---|---|
| `figures/*.pdf` | The six paper figures (vector PDF, canonical) | `python -m qlo.paper.figures` |
| `figures/png/*.png` | 200 dpi previews of the same figures | same command |
| `figures/FIGURE_SOURCES.md` | For each panel: source file, columns, filters, aggregation, CI, function | same command |
| `figures/manifest.json` | sha256 of every figure and of every source file it read, plus git commit and time | same command |
| `FIGURE_CAPTIONS_DRAFT.md` | Draft captions: what is plotted and its limits; no novelty language | by hand |
| `references.bib` | Bibliography, built from the B5 source manifest and `bib_sources.json` | `python tools/build_bib.py` |
| `BIBLIOGRAPHY_AUDIT.md` | Entry counts, versions reviewed vs cited, unresolved metadata | same command |
| `bib_sources.json` | The planned citations: identifiers and reasons only | by hand |
| `bib_verification.json` | Crossref / arXiv metadata snapshot used by the build | `python tools/fetch_bib_metadata.py` (network) |

Check the bibliography with `python tools/check_bib.py`. The tests are in `tests/test_paper_assets.py`.

PDFs are written without timestamps, so rebuilding from unchanged results gives byte-identical files in the same
environment. A different Matplotlib or font version may change the bytes but not the plotted data.
