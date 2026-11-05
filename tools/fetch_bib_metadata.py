"""Refresh paper/bib_verification.json: Crossref, DataCite and arXiv records for every identifier in paper/bib_sources.json.

    python tools/fetch_bib_metadata.py          # network; writes paper/bib_verification.json

Metadata only (titles, authors, venue, volume, pages, dates, identifiers). The snapshot is committed so that
tools/build_bib.py and tools/check_bib.py run offline. Nothing scientific is read from these records.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "paper" / "bib_sources.json"
MANIFEST = ROOT / "results" / "b5_prior_work" / "source_manifest.json"
OUT = ROOT / "paper" / "bib_verification.json"
UA = {"User-Agent": "qlo-research bibliography check (https://github.com/Satyabrat2005/QLO---Quantum-Langevin-Optimisation)"}
ATOM = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}


def _get(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def crossref(doi: str) -> dict:
    m = json.loads(_get("https://api.crossref.org/works/" + urllib.parse.quote(doi)).decode("utf-8"))["message"]
    return {"doi": m.get("DOI"), "type": m.get("type"), "title": (m.get("title") or [None])[0],
            "container_title": (m.get("container-title") or [None])[0], "volume": m.get("volume"),
            "article_number": m.get("article-number"), "page": m.get("page"),
            "issued": m.get("issued", {}).get("date-parts", [[None]])[0],
            "authors": [{"given": a.get("given"), "family": a.get("family"), "name": a.get("name")} for a in m.get("author", [])],
            "editors": [{"given": a.get("given"), "family": a.get("family")} for a in m.get("editor", [])],
            "publisher": m.get("publisher"), "url": "https://api.crossref.org/works/" + doi}


DATACITE_PREFIXES = ("10.4230/",)          # LIPIcs (Dagstuhl) registers its DOIs with DataCite, not Crossref


def datacite(doi: str) -> dict:
    a = json.loads(_get("https://api.datacite.org/dois/" + urllib.parse.quote(doi)).decode("utf-8"))["data"]["attributes"]
    c = a.get("container") or {}
    return {"doi": a.get("doi"), "type": (a.get("types") or {}).get("bibtex"), "title": a["titles"][0]["title"],
            "authors": [{"given": x.get("givenName"), "family": x.get("familyName"), "name": x.get("name")} for x in a.get("creators", [])],
            "year": a.get("publicationYear"), "publisher": a.get("publisher"),
            "series_information": next((d["description"] for d in a.get("descriptions", []) if d.get("descriptionType") == "SeriesInformation"), None),
            "container": {k: c.get(k) for k in ("title", "volume", "firstPage", "lastPage", "identifier")},
            "related": [r["relatedIdentifier"] for r in a.get("relatedIdentifiers", []) if r.get("relationType") == "IsVersionOf"],
            "url": "https://api.datacite.org/dois/" + doi}


def arxiv(ids: list[str]) -> dict:
    xml = _get("https://export.arxiv.org/api/query?max_results=100&id_list=" + ",".join(ids)).decode("utf-8")
    out = {}
    for e in ET.fromstring(xml).findall("a:entry", ATOM):
        full = e.find("a:id", ATOM).text.split("/abs/")[-1]
        base = full.rsplit("v", 1)[0]
        cat = e.find("x:primary_category", ATOM)
        jr, doi = e.find("x:journal_ref", ATOM), e.find("x:doi", ATOM)
        out[base] = {"id": base, "latest_version": full, "title": " ".join(e.find("a:title", ATOM).text.split()),
                     "authors": [a.find("a:name", ATOM).text for a in e.findall("a:author", ATOM)],
                     "published": e.find("a:published", ATOM).text[:10], "updated": e.find("a:updated", ATOM).text[:10],
                     "primary_category": cat.get("term") if cat is not None else None,
                     "journal_ref": jr.text if jr is not None else None, "doi": doi.text if doi is not None else None,
                     "url": "https://arxiv.org/abs/" + base}
    return out


def main() -> None:
    src = json.loads(SOURCES.read_text(encoding="utf-8"))["entries"]
    b5 = {p["paper_id"]: p for p in json.loads(MANIFEST.read_text(encoding="utf-8"))["papers"]}
    dois, ids = [], []
    for e in src:
        p = b5.get(e.get("b5_paper_id"), {})
        doi, ax = e.get("doi") or p.get("doi"), e.get("arxiv") or p.get("arxiv_id")
        if doi and not doi.startswith("10.48550/"):
            dois.append(doi)
        if ax:
            ids.append(ax)
    rec = {"retrieved_utc": time.strftime("%Y-%m-%d", time.gmtime()), "crossref": {}, "datacite": {}, "arxiv": arxiv(sorted(set(ids)))}
    for d in sorted(set(dois)):
        if d.startswith(DATACITE_PREFIXES):
            rec["datacite"][d] = datacite(d)
        else:
            rec["crossref"][d] = crossref(d)
        time.sleep(0.2)
    missing = sorted(set(ids) - set(rec["arxiv"]))
    if missing:
        raise SystemExit(f"arXiv records not returned for {missing}")
    OUT.write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(rec['crossref'])} Crossref, {len(rec['datacite'])} DataCite and {len(rec['arxiv'])} arXiv records -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
