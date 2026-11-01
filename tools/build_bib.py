"""Build paper/references.bib and paper/BIBLIOGRAPHY_AUDIT.md (offline).

    python tools/build_bib.py

Field sources, in order of precedence:
  * B5-reviewed papers: results/b5_prior_work/source_manifest.json (title, venue, volume, article number, year, DOI,
    arXiv id), so the entry describes the version B5 recorded. Author name splitting (given / family) comes from the
    Crossref record of the same DOI when the author lists agree.
  * Other papers: paper/bib_verification.json (Crossref for DOIs, arXiv API for arXiv-only papers).
  * A paper/bib_sources.json "supplement" only fills or expands fields: each value must occur verbatim in the arXiv
    journal_ref, or contain the metadata record's own value (an abbreviation expanded to its full name).
Every disagreement between B5 and Crossref, and every reviewed-version / cited-version difference, is written to the
audit instead of being overwritten.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
MANIFEST = ROOT / "results" / "b5_prior_work" / "source_manifest.json"
SOURCES = PAPER / "bib_sources.json"
VERIFY = PAPER / "bib_verification.json"
BIB = PAPER / "references.bib"
AUDIT = PAPER / "BIBLIOGRAPHY_AUDIT.md"


def _clean(s: str | None) -> str | None:
    return None if s is None else " ".join(html.unescape(re.sub(r"<[^>]+>", "", s)).split())


def _norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (_clean(s) or "").lower())


def _tex(s: str) -> str:
    return s.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#").replace("_", r"\_")


def _person(full: str) -> str:
    """'Samuel J. Lomonaco, Jr.' -> 'Lomonaco, Jr., Samuel J.'; 'Andriy Miranskyy' -> 'Miranskyy, Andriy'."""
    suffix = ""
    m = re.match(r"^(.*?),\s*(Jr\.|Sr\.|III|II)$", full.strip())
    if m:
        full, suffix = m.group(1), m.group(2)
    parts = full.split()
    family, given = parts[-1], " ".join(parts[:-1])
    return f"{family}, {suffix}, {given}" if suffix else f"{family}, {given}"


def _crossref_people(rec: dict) -> list[str]:
    return [f"{a['family']}, {a['given']}" if a.get("given") else (a.get("family") or a.get("name")) for a in rec["authors"]]


def _pages(rec_page: str | None, article: str | None) -> str | None:
    if article:
        return article
    return rec_page.replace("-", "--") if rec_page else None


def build() -> tuple[list[dict], list[dict]]:
    src = json.loads(SOURCES.read_text(encoding="utf-8"))["entries"]
    b5 = {p["paper_id"]: p for p in json.loads(MANIFEST.read_text(encoding="utf-8"))["papers"]}
    ver = json.loads(VERIFY.read_text(encoding="utf-8"))
    entries, issues = [], []
    for e in src:
        key = e["key"]
        if "unresolved" in e:
            issues.append({"key": key, "kind": "unresolved", "detail": e["unresolved"]})
            continue
        p = b5.get(e.get("b5_paper_id"))
        doi = e.get("doi") or (p or {}).get("doi")
        if doi and doi.startswith("10.48550/"):
            doi_is_arxiv = True
        else:
            doi_is_arxiv = False
        ax = e.get("arxiv") or (p or {}).get("arxiv_id")
        cr = ver["crossref"].get(doi) if doi and not doi_is_arxiv else None
        dc = ver.get("datacite", {}).get(doi) if doi and not doi_is_arxiv else None
        kind_override = None
        ar = ver["arxiv"].get(ax) if ax else None
        f: dict = {}
        origin = ""
        if p is not None:                                                        # B5-reviewed: manifest is authoritative
            origin = "B5 manifest"
            f["title"] = p["title"]
            names = p["authors"]
            if cr and len(cr["authors"]) == len(names) and all(_norm(a["family"]) in _norm(n) for a, n in zip(cr["authors"], names)):
                f["author"] = _crossref_people(cr)
            else:
                f["author"] = [_person(n) for n in names]
            f["year"] = str(p["year"])
            if p.get("volume"):
                f["journal"], f["volume"], f["pages"] = p["journal"], str(p["volume"]), p.get("article_number")
            if cr:                                                               # cross-check, never overwrite
                for fld, a, b in (("title", p["title"], cr["title"]), ("journal", p.get("journal"), cr["container_title"]),
                                  ("volume", p.get("volume"), cr["volume"]), ("article number", p.get("article_number"), cr["article_number"]),
                                  ("year", str(p["year"]), str(cr["issued"][0])), ("author count", str(len(names)), str(len(cr["authors"])))):
                    if _norm(a) != _norm(b):
                        issues.append({"key": key, "kind": "B5 vs Crossref", "detail": f"{fld}: B5 '{a}' vs Crossref '{_clean(b)}' (B5 kept)"})
            rev = p.get("version_reviewed", "")
            m = re.search(r"arXiv:(\d{4}\.\d{4,5}v\d+)", rev)
            reviewed = "published version" if p.get("published_version_inspected") else (f"arXiv:{m.group(1)}" if m else "arXiv")
            if not p.get("published_version_inspected") and p.get("volume"):
                issues.append({"key": key, "kind": "version", "detail": f"cited as the published version (DOI {doi}); B5 reviewed {reviewed} only; "
                                                                        "the journal reference comes from the arXiv record (B5 manifest)"})
            elif p.get("published_version_inspected_in"):
                issues.append({"key": key, "kind": "version", "detail": f"B5 first reviewed {m.group(1) if m else 'arXiv'}; the version of record was "
                                                                        f"inspected in the {p['published_version_inspected_in']} (cited as published)"})
            f["b5reviewed"] = reviewed
        elif cr:
            origin = "Crossref"
            f["title"] = _clean(cr["title"])
            f["author"] = _crossref_people(cr)
            f["year"] = str(cr["issued"][0])
            if cr["type"] == "journal-article":
                f["journal"], f["volume"], f["pages"] = _clean(cr["container_title"]), cr["volume"], _pages(cr["page"], cr["article_number"])
            elif cr["type"] == "book-chapter" and "Symposium" in (cr["container_title"] or ""):
                f["booktitle"], f["pages"], f["publisher"] = _clean(cr["container_title"]), _pages(cr["page"], None), cr["publisher"]
            else:
                f["series"], f["pages"], f["publisher"] = _clean(cr["container_title"]), _pages(cr["page"], None), cr["publisher"]
            if ar and _norm(ar["title"]) != _norm(cr["title"]):
                issues.append({"key": key, "kind": "title differs", "detail": f"arXiv title '{ar['title']}' vs published '{_clean(cr['title'])}' (published kept)"})
        elif dc:                                                                 # DataCite (LIPIcs); fields from the record only
            origin = "DataCite"
            f["title"] = dc["title"]
            f["author"] = [f"{a['family']}, {a['given']}" for a in dc["authors"]]
            f["year"] = str(dc["year"])
            si = dc.get("series_information") or ""
            m = re.search(r"Vol\. \d+, (.*?), pages", si)
            if m:
                f["booktitle"] = m.group(1)
            f["series"], f["volume"] = si.split(",")[0], dc["container"]["volume"]
            f["pages"], f["publisher"] = f"{dc['container']['firstPage']}--{dc['container']['lastPage']}", dc["publisher"]
            kind_override = "inproceedings"
            if ar and _norm(ar["title"]) != _norm(dc["title"]):
                issues.append({"key": key, "kind": "title differs", "detail": f"arXiv title '{ar['title']}' vs published '{dc['title']}' (published kept)"})
        elif ar:
            origin = "arXiv API"
            f["title"], f["author"], f["year"] = ar["title"], [_person(n) for n in ar["authors"]], ar["published"][:4]
            issues.append({"key": key, "kind": "arXiv only", "detail": f"no published version in the arXiv record (retrieved {ver['retrieved_utc']})"})
        else:
            issues.append({"key": key, "kind": "unresolved", "detail": "no metadata record"})
            continue
        if e.get("resolved_note"):
            issues.append({"key": key, "kind": "resolved", "detail": e["resolved_note"]})
        if e.get("version_note"):
            issues.append({"key": key, "kind": "version", "detail": e["version_note"]})
        if e.get("b5_as_printed"):
            printed = e["b5_as_printed"]
            miss = [f"{k} {f[k]}" for k in ("volume", "pages") if f.get(k) and str(f[k]).split("--")[0] not in printed]
            if _norm(f["title"]) not in _norm(printed):
                miss.append("title")
            if miss:
                issues.append({"key": key, "kind": "B5 follow-up as printed", "detail": f"B5 follow-up row {e['b5_followup_row']} records the "
                               f"citation as printed by the citing paper ('{printed}'); the verified record differs in {', '.join(miss)} "
                               "(verified record used; B5 never reviewed this paper)"})
        sup = e.get("supplement")
        if sup:
            jr = (ar or {}).get("journal_ref") or ""
            for k, v in sup.items():
                if k == "source":
                    continue
                rec = f.get(k)
                assert v in jr or (rec and str(rec) in v), f"{key}: supplement {k}={v!r} is neither in the journal_ref nor an expansion of {rec!r}"
                f[k] = [_person(v)] if k == "editor" else v
        if doi and not doi_is_arxiv:
            f["doi"] = doi
        if ax:
            f["eprint"], f["archiveprefix"] = ax, "arXiv"
            if ar and ar.get("primary_category"):
                f["primaryclass"] = ar["primary_category"]
        kind = kind_override or ("article" if "journal" in f else "inproceedings" if "booktitle" in f and "series" not in f and "editor" not in f \
            else "incollection" if "booktitle" in f else "misc")
        if kind == "misc":
            f["howpublished"] = "arXiv preprint"
        entries.append({"key": key, "type": kind, "fields": f, "origin": origin, "role": e["role"], "cited_by": e["cited_by"]})
    return entries, issues


ORDER = ("author", "editor", "title", "journal", "booktitle", "series", "volume", "pages", "publisher", "year", "doi",
         "eprint", "archiveprefix", "primaryclass", "howpublished", "b5reviewed")


def to_bibtex(entries: list[dict]) -> str:
    out = ["% Generated by tools/build_bib.py from paper/bib_sources.json, the B5 source manifest and",
           "% paper/bib_verification.json. Do not edit by hand. 'b5reviewed' records the version B5 read (ignored by BibTeX).", ""]
    for e in entries:
        f = e["fields"]
        lines = [f"@{e['type']}{{{e['key']},"]
        for k in ORDER:
            if k not in f or f[k] in (None, ""):
                continue
            v = f[k]
            if k in ("author", "editor"):
                v = " and ".join(v)
            v = _tex(str(v)) if k not in ("doi", "eprint") else str(v)
            lines.append(f"  {k} = {{{{{v}}}}}," if k == "title" else f"  {k} = {{{v}}},")
        lines[-1] = lines[-1].rstrip(",")
        out += lines + ["}", ""]
    return "\n".join(out)


def audit_md(entries: list[dict], issues: list[dict]) -> str:
    pub = [e for e in entries if e["fields"].get("doi")]
    axo = [e for e in entries if not e["fields"].get("doi")]
    b5 = [e for e in entries if e["origin"] == "B5 manifest"]
    ver = json.loads(VERIFY.read_text(encoding="utf-8"))
    L = ["# Bibliography audit", "",
         f"Generated by `tools/build_bib.py`; validated by `tools/check_bib.py`. Metadata snapshot retrieved {ver['retrieved_utc']}"
         " (Crossref, DataCite and arXiv API, metadata only). This is a citation-metadata audit, not a novelty audit.", "",
         "| | count |", "|---|---|",
         f"| entries in `references.bib` | {len(entries)} |",
         f"| with a DOI (published version) | {len(pub)} |",
         f"| arXiv only | {len(axo)} |",
         f"| B5-reviewed papers (fields from the B5 manifest) | {len(b5)} |",
         f"| unresolved planned citations (not in the .bib) | {sum(i['kind'] == 'unresolved' for i in issues)} |", "",
         "## Entries", "", "| key | type | DOI | arXiv | fields from | B5 reviewed | why cited |", "|---|---|---|---|---|---|---|"]
    for e in entries:
        f = e["fields"]
        L.append(f"| `{e['key']}` | {e['type']} | {f.get('doi', '—')} | {f.get('eprint', '—')} | {e['origin']} | {f.get('b5reviewed', '—')} | {e['role']} |")
    for title, kinds in (("Unresolved metadata", ("unresolved",)), ("Resolved citations", ("resolved",)), ("Version notes (reviewed vs cited version)", ("version",)),
                         ("arXiv-only entries", ("arXiv only",)), ("Title differences (arXiv vs published)", ("title differs",)),
                         ("B5 vs Crossref discrepancies (B5 kept)", ("B5 vs Crossref",)),
                         ("B5 follow-up citations as printed vs verified record", ("B5 follow-up as printed",))):
        rows = [i for i in issues if i["kind"] in kinds]
        L += ["", f"## {title}", ""]
        L += [f"- `{i['key']}`: {i['detail']}" for i in rows] if rows else ["None."]
    L += ["", "## Not included", "",
          "B5's MEDIUM and BACKGROUND follow-up lists (`docs/b5/B5_FOLLOWUP_SOURCES.md`, M1–M6 and G6–G8) are not in the .bib;"
          " none is a planned direct citation in the principal track or the allocation. Add them to `paper/bib_sources.json` if"
          " the manuscript cites them.", "",
          "Non-ASCII author names (for example Zoë, Høyer, Gilyén) are stored as UTF-8; use biber or a UTF-8-aware BibTeX setup.", ""]
    return "\n".join(L)


def main() -> None:
    entries, issues = build()
    BIB.write_text(to_bibtex(entries), encoding="utf-8")
    AUDIT.write_text(audit_md(entries, issues), encoding="utf-8")
    print(f"{len(entries)} entries -> {BIB.relative_to(ROOT)}; {len(issues)} audit notes -> {AUDIT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
