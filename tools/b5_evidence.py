"""B5 prior-work evidence files: parse the ledger and matrix, build results/b5_prior_work/evidence.csv, and check
quotes and locators against the local (git-ignored) source copies.

    python tools/b5_evidence.py                    # rewrite evidence.csv from docs/b5/B5_EVIDENCE_LEDGER.md
    python tools/b5_evidence.py --check            # only verify that evidence.csv matches the ledger
    python tools/b5_evidence.py --verify-sources   # check quotes / equation / figure numbers against local texts

The ledger is the single source of truth; the CSV is generated from it so the two cannot drift.
No scientific code is involved.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B5_DIR = ROOT / "docs" / "b5"
LEDGER = B5_DIR / "B5_EVIDENCE_LEDGER.md"
MATRIX = B5_DIR / "B5_PRIOR_WORK_MATRIX.md"
CSV_PATH = ROOT / "results" / "b5_prior_work" / "evidence.csv"
MANIFEST = ROOT / "results" / "b5_prior_work" / "source_manifest.json"

# Classification vocabulary. The follow-up audit uses exactly these four labels.
CLASSIFICATIONS = ("EXPLICIT", "PARTIAL / IMPLIED", "RELATED BUT DIFFERENT", "NOT LOCATED")
# Label of the initial B5 round (commit dfd2c6b), kept unchanged on the papers A/B entries that carry it.
# It is the B5-round equivalent of RELATED BUT DIFFERENT; no entry was relabelled.
LEGACY = ("PARTIAL / RELATED",)
ALLOWED = CLASSIFICATIONS + LEGACY
LEGACY_PAPERS = ("A", "B")
FORBIDDEN_LABEL_WORDS = ("NOVEL", "NEW", "FIRST")

PAPERS = {"A": ("thanasilp2024", "Exponential concentration in quantum kernel methods", 2024),
          "B": ("aghaeisaem2026", "Pitfalls when tackling the exponential concentration of parameterized quantum models", 2026),
          "C": ("arrasmith2021", "Effect of barren plateaus on gradient-free optimization", 2021),
          "D": ("teo2023", "Optimized numerical gradient and Hessian estimation for variational quantum algorithms", 2023),
          "E": ("gentinetta2024", "The complexity of quantum support vector machines", 2024),
          "F": ("mari2021", "Estimating the gradient and higher-order derivatives on quantum hardware", 2021),
          "G": ("miranskyy2025", "The Cost of Certainty: Shot Budgets in Quantum Program Testing", 2025),
          "H": ("zhan2025", "Experimental benchmarking of quantum state overlap estimation strategies with photonic systems",
                2025)}
MATRIX_PAPERS = tuple(PAPERS)                  # every paper has a column (part 1: A-E, part 2: F-H)
HEADER_PAPERS = {"Thanasilp 2024": "A", "Aghaei Saem 2026": "B", "Arrasmith 2021": "C", "Teo 2023": "D",
                 "Gentinetta 2024": "E", "Mari 2021": "F", "Miranskyy 2025": "G", "Zhan 2025": "H"}
FIELDS = ("Paper", "Candidate", "Matrix rows", "Claim category", "Classification", "Section", "Subsection", "Equation",
          "Figure", "Appendix", "Page", "Source version", "Source URL", "Short quote", "Source statement (paraphrase)",
          "Mathematical expression", "Assumptions", "Scope", "Relation to Stage 7", "Does NOT establish")
CSV_COLUMNS = ("evidence_id", "paper_id", "paper_title", "year", "candidate_id", "matrix_rows", "claim_category",
               "classification", "section", "subsection", "equation", "figure", "appendix", "page", "short_quote",
               "paraphrase", "assumptions", "scope", "relation_to_stage7", "does_not_establish", "source_version",
               "source_url")
EMPTY = {"", "—", "-"}
ID_RE = r"[A-H]-[A-Za-z0-9]+"

# Local text extractions of the reviewed versions (git-ignored; checks run only where present).
SOURCE_TEXTS = {
    "A": ("research_sources/b5/thanasilp2024_natcommun_raw.txt", "research_sources/b5/thanasilp2024_natcommun.txt",
          "research_sources/b5/SI_raw.txt", "research_sources/b5/thanasilp2024_SI.txt"),
    "B": ("research_sources/b5/aghaeisaem_arxiv_2507.22054v2.txt", "research_sources/b5/src_v2/main.tex",
          "research_sources/b5_followup/version_gap/aghaeisaem2026_qst_vor_raw.txt"),
    "C": ("research_sources/b5_followup/arrasmith2021_quantum_raw.txt",
          "research_sources/b5_followup/arrasmith2021_quantum.txt"),
    "D": ("research_sources/b5_followup/teo_arxiv_2206.12643v3_raw.txt",
          "research_sources/b5_followup/teo_arxiv_2206.12643v3.txt"),
    "E": ("research_sources/b5_followup/gentinetta2024_quantum_raw.txt",
          "research_sources/b5_followup/gentinetta2024_quantum.txt"),
    "F": ("research_sources/b5_closure/mari_arxiv_2008.06517v2_raw.txt",
          "research_sources/b5_closure/mari_arxiv_2008.06517v2.txt",
          "research_sources/b5_closure/mari_arxiv_2008.06517v2_tex/main.tex"),
    "G": ("research_sources/b5_closure/miranskyy_arxiv_2510.22418v1_raw.txt",
          "research_sources/b5_closure/miranskyy_arxiv_2510.22418v1.txt"),
    "H": ("research_sources/b5_closure/zhan2025_lsa_raw.txt", "research_sources/b5_closure/zhan2025_lsa.txt",
          "research_sources/b5_closure/zhan2025_lsa_SI_raw.txt", "research_sources/b5_closure/zhan2025_lsa_SI.txt"),
}
_PDF_GLYPHS = str.maketrans({"ð": "(", "Þ": ")", "¼": "="})
_SUP = str.maketrans({"ⁿ": "n", "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff",
                      "ﬃ": "ffi", "ﬄ": "ffl"})


def parse_ledger(path: Path = LEDGER) -> dict[str, dict]:
    text = path.read_text(encoding="utf-8")
    entries: dict[str, dict] = {}
    parts = re.split(r'<a id="(' + ID_RE + r')"></a>', text)
    for eid, body in zip(parts[1::2], parts[2::2]):
        if eid in entries:
            raise ValueError(f"duplicate ledger id {eid}")
        head = re.search(r"^###\s+(.+)$", body, re.M)
        rec = {"id": eid, "title": head.group(1).strip() if head else ""}
        for name in FIELDS:
            m = re.search(r"^- \*\*" + re.escape(name) + r":\*\*\s*(.*)$", body, re.M)
            rec[name] = m.group(1).strip() if m else None
        entries[eid] = rec
    return entries


def matrix_rows_of(rec: dict) -> list[str]:
    raw = rec.get("Matrix rows") or ""
    return [] if raw.strip() in EMPTY else [r.strip() for r in raw.split(",") if r.strip()]


def candidates_of(rec: dict) -> list[str]:
    return [c for c in re.split(r"[;,\s]+", rec.get("Candidate") or "") if c]


def parse_matrix(path: Path = MATRIX) -> list[dict]:
    """Rows of the matrix tables, merged by row number: claim(s), notes and per-paper (label, [linked ids], cell).

    The matrix is split into several tables (part 1: papers A-E; part 2: papers F-H). Each table starts with a header
    row "| # | Candidate / claim | <paper column titles> | Notes |"; paper columns are identified by HEADER_PAPERS."""
    rows: dict[str, dict] = {}
    order: list[str] = []
    cols: list | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\|\s*#\s*\|", line):
            header = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            cols = [HEADER_PAPERS.get(h, "notes" if h == "Notes" else None) for h in header]
            continue
        if cols is None or not re.match(r"^\|\s*\d+[ab]?\s*\|", line):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        num = cells[0]
        if num not in rows:
            rows[num] = {"row": num, "claim": cells[1], "claims": [], "notes": []}
            order.append(num)
        out = rows[num]
        out["claims"].append(cells[1])
        for key, cell in zip(cols, cells):
            if key == "notes":
                out["notes"].append(cell)
            elif key in PAPERS:
                label = next((lab for lab in sorted(ALLOWED, key=len, reverse=True) if cell.startswith(lab)), None)
                out[key] = (label, re.findall(r"\[(" + ID_RE + r")\]\(B5_EVIDENCE_LEDGER\.md#\1\)", cell), cell)
    return [rows[k] for k in order]


def ledger_to_rows(entries: dict[str, dict]) -> list[dict]:
    rows = []
    for eid, r in entries.items():
        pid, title, year = PAPERS[r["Paper"]]
        rows.append({"evidence_id": eid, "paper_id": pid, "paper_title": title, "year": year,
                     "candidate_id": r["Candidate"], "matrix_rows": r["Matrix rows"], "claim_category": r["Claim category"],
                     "classification": r["Classification"], "section": r["Section"], "subsection": r["Subsection"],
                     "equation": r["Equation"], "figure": r["Figure"], "appendix": r["Appendix"], "page": r["Page"],
                     "short_quote": r["Short quote"], "paraphrase": r["Source statement (paraphrase)"],
                     "assumptions": r["Assumptions"], "scope": r["Scope"], "relation_to_stage7": r["Relation to Stage 7"],
                     "does_not_establish": r["Does NOT establish"], "source_version": r["Source version"],
                     "source_url": r["Source URL"]})
    return rows


def write_csv(rows: list[dict], path: Path = CSV_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_COLUMNS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)


def read_csv(path: Path = CSV_PATH) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------------------------------------------
# Source checks (quotes, equation and figure numbers) against the local text extractions.

def alnum(s: str) -> str:
    """Lower-case letters and digits only: robust to line breaks, hyphenation and PDF math spacing."""
    return re.sub(r"[^0-9a-z]", "", s.translate(_SUP).lower())


def source_text(paper: str, root: Path = ROOT) -> str | None:
    """Concatenated local extractions for a paper, or None if no local copy is present."""
    parts = [(root / p).read_text(encoding="utf-8", errors="replace") for p in SOURCE_TEXTS.get(paper, ())
             if (root / p).exists()]
    # Springer Nature PDFs extract "(" ")" "=" as "ð" "Þ" "¼"; map them back so equation labels can be matched.
    return "\n".join(parts).translate(_PDF_GLYPHS) if parts else None


def quote_of(rec: dict) -> str | None:
    """The quoted text of the Short quote field (inside the first pair of double quotes), or None."""
    raw = rec.get("Short quote") or ""
    if raw.strip() in EMPTY:
        return None
    m = re.search(r"[\"“](.+?)[\"”]", raw)
    return m.group(1) if m else raw.strip()


def equation_tokens(field: str | None) -> list[str]:
    """Equation labels such as 13, C1, B14 in an Equation field (range end points included)."""
    if not field or field.strip() in EMPTY:
        return []
    return re.findall(r"\(([A-DS]?\d{1,3})\)", field)


def figure_tokens(field: str | None) -> list[str]:
    if not field or field.strip() in EMPTY:
        return []
    return re.findall(r"\bFig\.\s*(\d+)", field)


def table_tokens(field: str | None) -> list[str]:
    if not field or field.strip() in EMPTY:
        return []
    return re.findall(r"\bTab\.\s*([IVX]+)", field)


def verify_sources(entries: dict[str, dict], papers=tuple(PAPERS), root: Path = ROOT) -> tuple[list[str], list[str]]:
    """Return (failures, skipped_papers). Quotes are checked for every paper with a local copy; equation, figure and
    table numbers are checked for the given papers (all papers by default)."""
    failures, skipped = [], []
    texts = {p: source_text(p, root) for p in PAPERS}
    for p, t in texts.items():
        if t is None:
            skipped.append(p)
    norm = {p: alnum(t) for p, t in texts.items() if t is not None}
    flat = {p: re.sub(r"\s+", " ", t) for p, t in texts.items() if t is not None}
    for eid, r in entries.items():
        p = r["Paper"]
        if p not in norm:
            continue
        q = quote_of(r)
        if q is not None:
            if len(q.split()) > 15:
                failures.append(f"{eid}: quote longer than 15 words")
            if alnum(q) not in norm[p]:
                failures.append(f"{eid}: quote not found in the local {p} text: {q!r}")
        if p not in papers:
            continue
        for tok in equation_tokens(r["Equation"]) + equation_tokens(r["Appendix"]):
            if not re.search(r"\(\s*" + re.escape(tok) + r"\s*\)", flat[p]):
                failures.append(f"{eid}: equation ({tok}) not found in the local {p} text")
        for tok in figure_tokens(r["Figure"]):
            if not re.search(r"(fig\.|figure)\s*" + tok + r"\b", flat[p], re.I):
                failures.append(f"{eid}: figure {tok} not found in the local {p} text")
        for tok in table_tokens(r["Figure"]) + table_tokens(r["Appendix"]):
            if not re.search(r"TABLE\s+" + tok + r"\b", flat[p]):
                failures.append(f"{eid}: table {tok} not found in the local {p} text")
    return failures, skipped


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--verify-sources", action="store_true")
    a = ap.parse_args(argv)
    entries = parse_ledger()
    if a.verify_sources:
        failures, skipped = verify_sources(entries)
        for f in failures:
            print("FAIL", f)
        if skipped:
            print("no local copy (skipped):", ", ".join(skipped))
        print("source checks passed" if not failures else f"{len(failures)} source check failure(s)")
        return 0 if not failures else 1
    rows = ledger_to_rows(entries)
    if a.check:
        on_disk = read_csv()
        same = [{k: str(v) for k, v in r.items()} for r in rows] == on_disk
        print("evidence.csv matches ledger" if same else "evidence.csv is STALE")
        return 0 if same else 1
    write_csv(rows)
    print(f"wrote {len(rows)} rows -> {CSV_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
