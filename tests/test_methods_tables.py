"""Phase 8 I4: methods and appendix tables are generated from committed files, with provenance for every cell."""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

import pandas as pd
import pytest

from qlo.paper import methods_tables as MT

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "paper" / "appendix"
NAMES = list(MT.TABLES)
QUOTE = re.compile(r'([\w./{},-]+\.(?:md|py|json|csv)): "(.*?)"(?= \| |$|; )', re.S)


def _rows(name: str) -> list[dict]:
    with open(APP / f"{name}.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("appendix")
    return out, MT.build(out)


def test_generated_files_match_committed_files_and_are_deterministic(built, tmp_path):
    out, _ = built
    MT.build(tmp_path)
    for f in [f"{n}.csv" for n in NAMES] + ["APPENDIX_TABLES.md", "PROVENANCE.md"]:
        assert (out / f).read_bytes() == (tmp_path / f).read_bytes(), f        # deterministic
        assert (out / f).read_bytes() == (APP / f).read_bytes(), f"{f} is stale; rerun python -m qlo.paper.methods_tables"


def test_markdown_renders_the_csv_rows():
    md = (APP / "APPENDIX_TABLES.md").read_text(encoding="utf-8")
    for name in NAMES:
        rows = _rows(name)
        assert f"Source CSV: `{name}.csv`." in md
        for r in rows:
            first = list(r.values())[0]
            assert f"| {MT._md_cell(first)} |" in md


def test_every_row_has_provenance_and_every_quote_exists():
    for name in NAMES:
        for r in _rows(name):
            assert r["provenance"].strip(), (name, list(r.values())[0])
            for path, quote in QUOTE.findall(r["provenance"]):
                assert quote in (ROOT / path).read_text(encoding="utf-8"), (name, path, quote)


def test_configuration_and_validation_sources_exist():
    for r in _rows("configuration_table"):
        assert (ROOT / r["config_source"]).exists() and (ROOT / r["result_source"]).exists(), r["experiment"]
    assert [r["experiment"] for r in _rows("configuration_table")] == ["Stage 3", "Stage 4", "Stage 5", "Stage 6", "Stage 7", "B1", "B2", "B3", "B4"]
    for r in _rows("validation_table"):
        assert (ROOT / r["source_file"]).exists(), r["check"]
        assert r["observed_error"] not in ("", "N/A"), r["check"]                 # a check with no number is not listed
    for name in NAMES:
        for r in _rows(name):
            for p in re.findall(r"<- ((?:docs|results|src|paper)/[\w./-]+?)(?=[:;\s]|$)", r["provenance"]):
                assert (ROOT / p).exists(), (name, p)


def test_no_invented_runtime_values():
    for r in _rows("reproduction_table"):
        for f in ("wall_time", "cpu_time", "peak_memory", "workers", "python_version"):
            v = r[f]
            if v in (MT.NR, "N/A") or v.startswith(MT.NR):
                continue
            entry = [p for p in r["provenance"].split(" | ") if p.startswith(f"{f} <- ")]
            assert entry, (r["experiment"], f)
            assert ': "' in entry[0] or ".json:" in entry[0], (r["experiment"], f, entry)   # quoted from a committed log/report or read from JSON


def test_no_physical_hardware_and_platform_wording():
    rows = _rows("reproduction_table")
    assert {r["physical_hardware"] for r in rows} == {"false"}
    for r in rows:
        p = r["platform_actually_run"].lower()
        assert "qpu" not in p and "quantum hardware" not in p
        if r["experiment"] in {"Stage 3", "Stage 4", "Stage 5", "Stage 6", "Stage 7", "B1", "B2", "B3", "B4"}:
            assert "classical simulation" in p and "macos" in p
    for f in ("APPENDIX_TABLES.md",):
        t = (APP / f).read_text(encoding="utf-8")
        assert "Real quantum hardware: not used" in t
    m = (ROOT / "paper" / "methods" / "METHODS_SOURCE.md").read_text(encoding="utf-8")
    assert "Real quantum hardware:** not used" in m and "Independent full reproduction** (principal P9, Tiers 2 and 3): not yet done" in m


def test_hardware_model_only_where_its_source_names_it():
    model = re.compile(r"\bM[1-9]\b|Apple|Intel|Ryzen|Xeon")
    for r in _rows("reproduction_table"):
        if model.search(r["platform_actually_run"]):
            entry = [p for p in r["provenance"].split(" | ") if p.startswith("platform_actually_run <- ")][0]
            quote = QUOTE.findall(entry)
            assert quote and model.search(quote[0][1]), (r["experiment"], entry)       # the quoted source itself names the model
    assert [r["experiment"] for r in _rows("reproduction_table") if model.search(r["platform_actually_run"])] == ["B1"]
    for f in (APP / "APPENDIX_TABLES.md", ROOT / "paper" / "methods" / "METHODS_SOURCE.md"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if model.search(line) and not line.startswith("|"):
                assert "B1" in line, (f.name, line)                                    # prose mentions are attributed to the B1 log


def test_estimator_rows_match_b2():
    ra = pd.read_csv(ROOT / "results" / "b2_estimators" / "resource_accounting.csv").set_index("estimator")
    sl = pd.read_csv(ROOT / "results" / "b2_estimators" / "slope_summary.csv")
    sl = sl[(sl.quantity == "median_log10_total_executions") & (sl.fit_range == "primary_2_20")].set_index("estimator")
    rows = {r["estimator"]: r for r in _rows("estimator_resources")}
    for est, lab in (("loschmidt", "Loschmidt"), ("swap_ancilla", "ancilla SWAP"), ("swap_destructive", "destructive SWAP"), ("hadamard_u", "Hadamard U-statistic")):
        r = rows[lab]
        assert r["qubits"] == ra.loc[est, "qubits_per_shot"] and int(r["copies"]) == int(ra.loc[est, "state_copies_per_shot"])
        assert r["executions_convention"] == ra.loc[est, "executions_per_gradient"]
        assert r["rx_exponent"].startswith(f"{sl.loc[est, 'stage7_population_slope']:.4f}")
    assert rows["Hadamard U-statistic"]["controlled_unitary_requirement"] == "controlled-(V†U)"
    assert rows["Loschmidt"]["target_inverse_requirement"].startswith("yes")
    assert "not hardware cost" in (APP / "APPENDIX_TABLES.md").read_text(encoding="utf-8")


def test_regime_table_does_not_overclaim():
    rows = {r["result"]: r for r in _rows("regime_of_validity")}
    loc = rows["Local depolarizing result"]
    assert "only for the RX product" in loc["mathematical_scope"] and "NOT tested" in loc["known_exclusions"]
    assert "entangling" in loc["known_exclusions"]
    assert "benchmark-specific" in rows["RX-product 4ⁿ vs 16ⁿ"]["mathematical_scope"]
    assert "b_r = 0" in rows["Exponent doubling"]["mathematical_scope"]
    assert "MS → 0" in rows["Conditional sign law"]["mathematical_scope"]
    assert "ideal" in rows["Global depolarizing result"]["assumptions"]
    assert "not a theorem" in rows["B1 entangling generalization"]["mathematical_scope"]


def test_scientific_results_unchanged():
    try:
        ok = subprocess.run(["git", "cat-file", "-e", "eaf0728^{commit}"], cwd=ROOT, capture_output=True).returncode == 0
        r = subprocess.run(["git", "diff", "--quiet", "eaf0728", "--", "results", "principal"], cwd=ROOT, capture_output=True)
    except OSError:
        pytest.skip("git not available")
    if not ok or r.returncode not in (0, 1):
        pytest.skip("baseline commit not available")
    assert r.returncode == 0
