"""Phase 8 (Shravan section 8 item 2): every number in the B1-B4 results draft traces to a committed file."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "paper" / "drafts" / "results_b1_b4.tex"
LEDGER = ROOT / "paper" / "drafts" / "results_b1_b4_numbers.csv"
# decimals (0.376, 1.75) and comma-grouped counts (6,740,000); bare small integers are structure (n, depth, seeds)
NUMBER = re.compile(r"(?<![\w.])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\w.,])\d+\.\d+")


def _ledger() -> list[dict]:
    with open(LEDGER, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _draft_numbers() -> set[str]:
    text = "\n".join(l for l in DRAFT.read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("%"))
    text = re.sub(r"\\(?:label|ref)\{[^}]*\}", "", text)
    return set(NUMBER.findall(text))


def test_every_number_in_the_draft_has_a_source():
    missing = _draft_numbers() - {r["token"] for r in _ledger()}
    assert not missing, f"numbers without a ledger row: {sorted(missing)}"


def test_ledger_has_no_stale_rows():
    stale = {r["token"] for r in _ledger()} - _draft_numbers()
    assert not stale, f"ledger rows for numbers no longer in the draft: {sorted(stale)}"


def test_text_sources_contain_the_quoted_number():
    for r in (r for r in _ledger() if r["kind"] == "text"):
        src = (ROOT / r["source"]).read_text(encoding="utf-8").replace("\r\n", "\n")
        assert r["locator"] in src, (r["token"], r["source"], r["locator"])
        assert r["token"] in r["locator"], (r["token"], r["locator"])


def test_csv_sources_reproduce_the_number():
    for r in (r for r in _ledger() if r["kind"] == "csv"):
        query, column, agg, digits = r["locator"].split("|")
        rows = pd.read_csv(ROOT / r["source"]).query(query)[column]
        assert len(rows) and (agg != "value" or len(rows) == 1), (r["token"], r["locator"], len(rows))
        v = {"min": rows.min(), "max": rows.max(), "value": rows.iloc[0]}[agg]
        assert f"{v:.{int(digits)}f}" == r["token"], (r["token"], r["locator"], v)
