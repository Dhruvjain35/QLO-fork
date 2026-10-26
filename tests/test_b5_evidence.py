"""B5 prior-work evidence files: structural consistency checks (no scientific numerics)."""

import csv
import hashlib
import importlib.util
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
B5 = ROOT / "docs" / "b5"


def doc(name: str) -> Path:
    """B5 reports live in docs/b5/; result files keep their repo-root path."""
    return ROOT / name if name.startswith("results/") else B5 / name
_spec = importlib.util.spec_from_file_location("b5_evidence", ROOT / "tools" / "b5_evidence.py")
E = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(E)

B5_DOCS = ("B5_PRIOR_WORK_EXTRACTION.md", "B5_PRIOR_WORK_MATRIX.md", "B5_EVIDENCE_LEDGER.md", "B5_MATH_COMPARISON.md",
           "B5_FOLLOWUP_SOURCES.md", "B5_POTENTIAL_ISSUES.md")
FOLLOWUP_DOCS = ("B5_FOLLOWUP_AUDIT.md", "B5_TEO_DEEP_AUDIT.md", "B5_ARRASMITH_AUDIT.md", "B5_GENTINETTA_AUDIT.md",
                 "B5_STATISTIC_COMPARISON.md", "B5_SHOT_CONVENTIONS.md", "B5_VERSION_GAP.md")
CLOSURE_DOCS = ("B5_CLOSURE_AUDIT.md", "B5_MARI_AUDIT.md", "B5_CLOSURE_SEARCH.md", "B5_PRINCIPAL_LINE_CHECK.md")
# Entries for papers A/B written after the initial round (matrix rows 29-33) use the four-label vocabulary only.
FOLLOWUP_AB_IDS = {"A-NL29", "A-NL30", "B-17", "B-NL30", "A-19", "A-NL33", "B-18", "B-NL33"}
FINAL_LINE = "This remains an evidence extraction for A1 and does not make the novelty decision."


@pytest.fixture(scope="module")
def ledger():
    return E.parse_ledger()


@pytest.fixture(scope="module")
def matrix():
    return E.parse_matrix()


def test_ledger_entries_complete(ledger):
    assert len(ledger) > 0
    for eid, r in ledger.items():
        assert all(r[f] is not None for f in E.FIELDS), eid
        assert r["Paper"] in E.PAPERS and eid.startswith(r["Paper"] + "-"), eid             # every row has a paper id
        assert r["Classification"] in E.ALLOWED, (eid, r["Classification"])
        if r["Classification"] in E.LEGACY:
            assert r["Paper"] in E.LEGACY_PAPERS and eid not in FOLLOWUP_AB_IDS, eid           # legacy label: A/B only
        locator = [r[k] for k in ("Section", "Subsection", "Equation", "Figure", "Appendix", "Page")]
        assert any(v not in E.EMPTY for v in locator), eid                                   # every row has a location
        assert r["Source version"] not in E.EMPTY and r["Source URL"].startswith("https://"), eid
        if r["Paper"] == "B":                                                                # never pretend B = published
            assert "arXiv:2507.22054v2" in r["Source version"], eid
        if r["Paper"] == "D":                                                                # Teo reviewed as arXiv v3
            assert "arXiv:2206.12643v3" in r["Source version"], eid
            assert "not inspected" in r["Source version"], eid
        if r["Paper"] == "F":                                                                # Mari reviewed as arXiv v2
            assert "arXiv:2008.06517v2" in r["Source version"], eid
            assert "not inspected" in r["Source version"], eid
        if r["Paper"] == "G":                                                                # preprint only
            assert "arXiv:2510.22418v1" in r["Source version"], eid
        if r["Paper"] == "H":                                                                # published version + SI
            assert "Light Sci. Appl. 14, 83" in r["Source version"], eid
        if r["Classification"] == "NOT LOCATED":
            assert "Not located in the reviewed version" in r["Source statement (paraphrase)"], eid
            assert "searches for:" in r["Source statement (paraphrase)"], eid


def test_followup_entries_use_four_label_vocabulary_with_exact_locators(ledger):
    followup = {e: r for e, r in ledger.items() if r["Paper"] not in E.LEGACY_PAPERS or e in FOLLOWUP_AB_IDS}
    assert {r["Paper"] for r in followup.values()} == set(E.PAPERS)
    for eid, r in followup.items():
        assert r["Classification"] in E.CLASSIFICATIONS, (eid, r["Classification"])
        if r["Classification"] != "NOT LOCATED":                                             # exact location required
            assert r["Page"] not in E.EMPTY, eid
            assert re.search(r"\d", r["Page"]), eid
            assert any(r[k] not in E.EMPTY for k in ("Equation", "Figure", "Appendix", "Subsection", "Section")), eid
    assert set(E.CLASSIFICATIONS) == {r["Classification"] for r in followup.values()}       # all four labels in use


def test_classification_labels_never_claim_novelty(ledger, matrix):
    for word in E.FORBIDDEN_LABEL_WORDS:
        for lab in E.ALLOWED:
            assert not re.search(r"\b" + word + r"\b", lab)
        for eid, r in ledger.items():
            assert not re.search(r"\b" + word + r"\b", r["Classification"]), eid
        for row in matrix:
            for p in E.MATRIX_PAPERS:
                assert not re.search(r"\b" + word + r"\b", row[p][0] or ""), (row["row"], p)


def test_matrix_cells_link_to_matching_ledger_entries(matrix, ledger):
    required = {str(i) for i in range(1, 34) if i != 14} | {"14a", "14b"}
    assert required <= {row["row"] for row in matrix}
    for row in matrix:
        assert len(set(row["claims"])) == 1, (row["row"], "claim text differs between matrix parts")
        for paper in E.MATRIX_PAPERS:
            label, ids, cell = row[paper]
            assert label in E.ALLOWED, (row["row"], paper, cell)
            if paper not in E.LEGACY_PAPERS or row["row"] in ("29", "30", "31", "32", "33"):
                assert label in E.CLASSIFICATIONS, (row["row"], paper, label)
            assert ids, (row["row"], paper, "cell has no ledger reference")
            for i in ids:
                assert i in ledger, (row["row"], i)
                assert ledger[i]["Paper"] == paper, (row["row"], i)
                assert ledger[i]["Classification"] == label, (row["row"], i, ledger[i]["Classification"], label)
                assert row["row"] in E.matrix_rows_of(ledger[i]), (row["row"], i)


def test_every_ledger_matrix_row_is_linked_back(matrix, ledger):
    linked = {(row["row"], i) for row in matrix for p in E.MATRIX_PAPERS for i in row[p][1]}
    for eid, r in ledger.items():
        for rr in E.matrix_rows_of(r):
            assert (rr, eid) in linked, (eid, rr)


def test_each_candidate_has_an_evidence_trail(ledger):
    for cand in ("C1", "C2", "C3", "C4", "C5"):
        hits = [e for e, r in ledger.items() if cand in E.candidates_of(r)]
        assert {ledger[h]["Paper"] for h in hits} == set(E.PAPERS), cand                      # >= 1 entry per paper


def test_csv_matches_ledger(ledger):
    rows = E.read_csv()
    assert tuple(rows[0].keys()) == E.CSV_COLUMNS
    assert [{k: str(v) for k, v in r.items()} for r in E.ledger_to_rows(ledger)] == rows
    for r in rows:
        assert r["paper_id"] in {v[0] for v in E.PAPERS.values()}
        assert r["classification"] in E.ALLOWED


def test_manifest_complete_and_hashes_match():
    man = json.loads(E.MANIFEST.read_text(encoding="utf-8"))
    assert {p["paper_id"] for p in man["papers"]} == {v[0] for v in E.PAPERS.values()}
    for p in man["papers"]:
        for key in ("title", "authors", "journal", "year", "doi", "arxiv_id", "version_reviewed", "publication_date",
                    "review_completed", "files"):
            assert p.get(key) not in (None, "", []), (p["paper_id"], key)
        assert isinstance(p.get("published_version_inspected"), bool), p["paper_id"]
        for f in p["files"]:
            assert f["download_source"].startswith("https://") and len(f["sha256"]) == 64
            assert f["local_filename"].startswith("research_sources/")
            local = ROOT / f["local_filename"]
            if local.exists():                    # local copies are git-ignored; check only where present
                assert hashlib.sha256(local.read_bytes()).hexdigest() == f["sha256"], f["local_filename"]
    by_id = {p["paper_id"]: p for p in man["papers"]}
    for pid in ("arrasmith2021", "teo2023", "gentinetta2024", "mari2021", "miranskyy2025", "zhan2025"):
        for key in ("arxiv_versions_cross_checked", "supplement_reviewed", "review_scope"):
            assert by_id[pid].get(key), (pid, key)
    assert by_id["teo2023"]["published_version_inspected"] is False       # APS version of record not inspected
    assert by_id["mari2021"]["published_version_inspected"] is False      # APS version of record not inspected
    assert "arXiv:2008.06517v2" in by_id["mari2021"]["version_reviewed"]
    assert by_id["zhan2025"]["published_version_inspected"] is True       # LSA version of record + published SI
    assert any("Supplementary Information" in f["role"] for f in by_id["zhan2025"]["files"])
    assert "arXiv:2206.12643v3" in by_id["teo2023"]["version_reviewed"]
    b = by_id["aghaeisaem2026"]
    assert b["published_version_inspected"] is True                       # follow-up: version of record retrieved
    assert any("version-of-record" in f["role"] for f in b["files"])
    assert b["version_of_record"]["journal_dates"]["accepted"] == "2025-11-20"


def test_quotes_and_locators_match_local_sources(ledger):
    if all(E.source_text(p) is None for p in E.PAPERS):
        pytest.skip("no local source copies (research_sources/ is git-ignored)")
    failures, _ = E.verify_sources(ledger)
    assert not failures, failures


def test_followup_documents_present_and_structured():
    for name in FOLLOWUP_DOCS:
        assert doc(name).exists(), name
    audit = (B5 / "B5_FOLLOWUP_AUDIT.md").read_text(encoding="utf-8")
    assert audit.rstrip().splitlines()[-1] == FINAL_LINE
    assert len(re.findall(r"^## \d+\. ", audit, re.M)) == 20
    teo = (B5 / "B5_TEO_DEEP_AUDIT.md").read_text(encoding="utf-8")
    titles = ("Setup", "Estimators", "Error metric", "Shot convention", "BP scaling assumptions",
              "Main theorems/formulas", "Critical copy-number result", "Relation to Stage 5", "Relation to Stage 7",
              "What overlaps explicitly", "What is only implied", "What is different", "What is not located")
    for i, t in enumerate(titles, 1):
        assert re.search(r"^## " + str(i) + r"\. " + re.escape(t) + r"\s*$", teo, re.M), t
    stat = (B5 / "B5_STATISTIC_COMPARISON.md").read_text(encoding="utf-8")
    header = ("Paper", "Result", "Random variable", "Statistic used", "Scaling variable", "Shot convention",
              "Circuit ensemble", "Parameter ensemble", "Measurement scheme", "Comparable to Stage 7?", "Reason")
    assert "| " + " | ".join(header) + " |" in stat
    shots = (B5 / "B5_SHOT_CONVENTIONS.md").read_text(encoding="utf-8")
    for paper in ("Stage 7", "Thanasilp", "Aghaei Saem", "Arrasmith", "Teo", "Gentinetta"):
        assert paper in shots, paper
    gap = (B5 / "B5_VERSION_GAP.md").read_text(encoding="utf-8")
    for needle in ("2025-11-20", "2026-01-30", "2026-06-04", "B-09a", "B-10a"):
        assert needle in gap, needle
    math = (B5 / "B5_MATH_COMPARISON.md").read_text(encoding="utf-8")
    assert re.search(r"^## \d+\. Comparison with Teo 2023", math, re.M)


def test_closure_documents_and_search_record():
    for name in CLOSURE_DOCS:
        assert doc(name).exists(), name
    audit = (B5 / "B5_CLOSURE_AUDIT.md").read_text(encoding="utf-8")
    assert audit.rstrip().splitlines()[-1] == FINAL_LINE
    check = (B5 / "B5_PRINCIPAL_LINE_CHECK.md").read_text(encoding="utf-8")
    assert {f"L{i}" for i in range(1, 31)} <= set(re.findall(r"^\| (L\d+) \|", check, re.M))
    math = (B5 / "B5_MATH_COMPARISON.md").read_text(encoding="utf-8")
    assert re.search(r"^## 9\. ", math, re.M)
    with (ROOT / "results" / "b5_prior_work" / "closure_search_screen.csv").open(encoding="utf-8") as fh:
        screen = list(csv.DictReader(fh))
    assert len(screen) > 1000 and {"id", "title", "queries", "decision", "reason"} <= set(screen[0])
    included = {r["decision"] for r in screen if r["decision"].startswith("included")}
    assert included == {"included (paper F)", "included (paper G)", "included (paper H)"}
    queries = json.loads((ROOT / "results" / "b5_prior_work" / "closure_search_queries.json").read_text(encoding="utf-8"))
    assert queries["unique_records_screened"] == len(screen) and queries["queries"]
    assert (ROOT / "tools" / "b5_closure_search.py").exists()


def test_no_novelty_classification_or_language():
    for name in B5_DOCS + FOLLOWUP_DOCS + CLOSURE_DOCS + ("results/b5_prior_work/evidence.csv",):
        text = doc(name).read_text(encoding="utf-8")
        assert "NOVEL" not in text.replace("NOVELTY", ""), name
        assert not re.search(r"\bnovel\b", text, re.I), name


def test_research_sources_are_git_ignored():
    assert "research_sources/" in (ROOT / ".gitignore").read_text(encoding="utf-8")
