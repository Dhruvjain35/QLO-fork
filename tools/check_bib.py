"""Validate paper/references.bib (offline).

    python tools/check_bib.py       # exit status 1 on any failure

Checks: unique keys; author, title and year present; a DOI or an arXiv id on every entry; DOI and arXiv-id format;
no duplicate DOI, arXiv id or title; every B5-reviewed paper present; every citation in the principal track's A4
related-work paragraphs present; the committed .bib and audit equal a fresh tools/build_bib.py build.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_bib as BB  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DOI_RE = re.compile(r"^10\.\d{4,9}/[^\s{}]+$")
ARXIV_RE = re.compile(r"^(\d{4}\.\d{4,5}|[a-z\-]+(\.[A-Z]{2})?/\d{7})$")       # no version suffix
CITE_RE = re.compile(r"\[([A-Z][^\[\]]*?\d{4})\]|([A-Z][\w\- ]+?) et al\. \[(\d{4})\]")


def parse_bib(text: str) -> list[dict]:
    out = []
    for m in re.finditer(r"@(\w+)\{([^,\s]+),\n(.*?)\n\}", text, re.S):
        fields = {k.lower(): v for k, v in re.findall(r"^\s+(\w+) = \{(.*)\},?$", m.group(3), re.M)}
        out.append({"type": m.group(1), "key": m.group(2), "fields": {k: v.strip("{}") for k, v in fields.items()}})
    return out


def a4_citations() -> list[tuple[str, str]]:
    text = (ROOT / "principal" / "QLO_Principal_Track.md").read_text(encoding="utf-8")
    sec = text.split("## 5. A4 positioning", 1)[1].split("\n## ", 1)[0]
    cites = []
    for m in CITE_RE.finditer(sec):
        if m.group(1):
            for part in m.group(1).split(";"):
                mm = re.match(r"\s*([A-Z][\w\- ]+?)(?: et al\.)? (\d{4})\s*$", part)
                if mm:
                    cites.append((mm.group(1).strip(), mm.group(2)))
        else:
            cites.append((m.group(2).strip(), m.group(3)))
    return sorted(set(cites))


def first_family(author: str) -> str:
    return author.split(" and ")[0].split(",")[0].strip()


def main() -> int:
    errors: list[str] = []
    bib_text = BB.BIB.read_text(encoding="utf-8")
    entries = parse_bib(bib_text)
    keys = [e["key"] for e in entries]
    if len(keys) != len(set(keys)):
        errors.append(f"duplicate keys: {sorted(k for k in set(keys) if keys.count(k) > 1)}")
    seen_doi, seen_ax, seen_title = {}, {}, {}
    for e in entries:
        f, k = e["fields"], e["key"]
        for req in ("author", "title", "year"):
            if not f.get(req):
                errors.append(f"{k}: missing {req}")
        if not re.fullmatch(r"\d{4}", f.get("year", "")):
            errors.append(f"{k}: bad year {f.get('year')!r}")
        if not (f.get("doi") or f.get("eprint")):
            errors.append(f"{k}: neither DOI nor arXiv id")
        if f.get("doi"):
            if not DOI_RE.match(f["doi"]):
                errors.append(f"{k}: malformed DOI {f['doi']!r}")
            seen_doi.setdefault(f["doi"].lower(), []).append(k)
        if f.get("eprint"):
            if not ARXIV_RE.match(f["eprint"]) or f.get("archiveprefix") != "arXiv":
                errors.append(f"{k}: malformed arXiv id {f['eprint']!r} (expected no version suffix and archiveprefix arXiv)")
            seen_ax.setdefault(f["eprint"], []).append(k)
        if e["type"] == "article" and not (f.get("journal") and f.get("volume") and f.get("pages")):
            errors.append(f"{k}: article without journal, volume and pages/article number")
        seen_title.setdefault(BB._norm(f.get("title")), []).append(k)
    for what, d in (("DOI", seen_doi), ("arXiv id", seen_ax), ("title", seen_title)):
        for v, ks in d.items():
            if len(ks) > 1:
                errors.append(f"duplicate {what} {v!r}: {ks}")

    b5 = json.loads(BB.MANIFEST.read_text(encoding="utf-8"))["papers"]
    for p in b5:
        hit = [e["key"] for e in entries if (p.get("doi") and e["fields"].get("doi", "").lower() == p["doi"].lower())
               or (p.get("arxiv_id") and e["fields"].get("eprint") == p["arxiv_id"])]
        if not hit:
            errors.append(f"B5-reviewed paper {p['paper_id']} missing from the .bib")

    a4 = a4_citations()
    for fam, yr in a4:
        hit = [e["key"] for e in entries if BB._norm(first_family(e["fields"]["author"])) == BB._norm(fam)
               and (e["fields"]["year"] == yr or e["fields"].get("eprint", "").startswith(yr[2:]))]
        if not hit:
            errors.append(f"principal A4 citation '{fam} {yr}' has no .bib entry")

    fresh_entries, issues = BB.build()
    if BB.to_bibtex(fresh_entries) != bib_text:
        errors.append("references.bib differs from a fresh tools/build_bib.py build")
    if BB.audit_md(fresh_entries, issues) != BB.AUDIT.read_text(encoding="utf-8"):
        errors.append("BIBLIOGRAPHY_AUDIT.md differs from a fresh tools/build_bib.py build")

    unresolved = [i["key"] for i in issues if i["kind"] == "unresolved"]
    print(f"{len(entries)} entries; {len(seen_doi)} DOIs; {len(seen_ax)} arXiv ids; {len(b5)} B5 papers present; "
          f"{len(a4)} A4 citations matched; unresolved planned citations: {unresolved or 'none'}")
    for e in errors:
        print("FAIL:", e)
    print("OK" if not errors else f"{len(errors)} failure(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
