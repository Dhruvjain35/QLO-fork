"""Phase 8 I3 / I5: paper figures from committed results and the bibliography. No pixel tests."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from qlo.paper import figures as FG
from qlo.paper import sources as S

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_bib as BB  # noqa: E402
import check_bib as CB  # noqa: E402

EXPECTED = ["fig1_same_landscape", "fig2_conditional_sign_law", "fig3_b1_scaling_rule", "fig4_four_estimators", "fig5_noise",
            "fig6_empirical_estimator_comparison"]


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# sources ----------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("name", sorted(S.TABLES))
def test_source_files_and_columns_exist(name):
    df = S.table(name)                       # raises if the file or a required column is missing
    assert len(df) > 0


def test_no_nan_dropped_without_a_declared_rule():
    cx = S.table("b4_crossover")
    assert (cx.n_star.isna() == (cx.note != "inside range")).all()          # NaN only where no crossover is in range (declared)
    assert (S.table("b1_sign").error > 0).all()                              # Figure 2b log axis drops nothing
    for name, cols in (("stage7_scaling", ["snr1_log10M_median", "snr1_log10M_q25", "snr1_log10M_q75"]),
                       ("b1_main", ["b_S", "gap_obs", "eps_gap", "b_r", "ratio_obs", "ratio_pred"]),
                       ("b2_required", ["median_log10_total_executions", "q25_log10_total", "q75_log10_total"]),
                       ("b2_fixed", ["median_P_zero", "median_P_correct", "median_P_correct_given_nonzero"]),
                       ("b4_window", ["b_LE", "b_SWAP"]), ("b4_pred", ["measured_b_S", "measured_ratio_obs", "asym_ratio"]),
                       ("b3_sign_law", ["reference_observed_median_accurate", "SEED_pct_lo", "SEED_pct_hi"])):
        assert np.isfinite(S.table(name)[cols].to_numpy(dtype=float)).all(), name


# the numbers the figures are meant to show ----------------------------------------------------------------------------
def test_stage7_slopes_and_b3_intervals_are_consistent():
    fits = S.doc("stage7_fits")["fits"]
    iv = S.table("b3_stage7_intervals").set_index(["fit_range", "metric"])
    for sc in ("loschmidt", "swap"):
        for t in ("snr1", "snr2", "dir0.75", "dir0.9"):
            assert float(iv.loc[("primary_2_20", f"slope_{sc}_{t}"), "stage7_estimate"]) == pytest.approx(fits[f"{sc}_{t}"]["slope"], abs=1e-12)
    assert fits["loschmidt_snr1"]["slope"] == pytest.approx(0.6059, abs=5e-5)
    assert fits["swap_snr1"]["slope"] == pytest.approx(1.2025, abs=5e-5)


def test_corrected_sign_law_number_is_used():
    lo, hi = FG.stage7_sign_range(S.table("b3_sign_law"), S.doc("stage7_config")["paired_shots"])
    assert (round(lo, 4), round(hi, 4)) == (0.8527, 0.8530)
    assert hi < 0.8533                                                       # the superseded Stage 7 value is not used
    assert "0.8533" not in (ROOT / "paper" / "FIGURE_CAPTIONS_DRAFT.md").read_text(encoding="utf-8")


def test_b1_gap_data_match_the_committed_table():
    m = S.table("b1_main")
    assert np.allclose(m.eps_gap, m.gap_obs - m.b_S, atol=1e-10)
    p = m[m.fit_range == "primary"]
    assert len(p) == 17 and (p.n_seeds == 10).all()
    assert (p.b_r.abs() < 3e-3).all() and ((100 * p.eps_gap / p.b_S).between(-1.3, -0.4)).all()


def test_b2_slopes_match_the_committed_result():
    s = S.table("b2_slopes")
    s = s[(s.quantity == "median_log10_total_executions") & (s.fit_range == "primary_2_20")].set_index("estimator").stage7_population_slope
    assert round(s.loschmidt, 4) == 0.6059 and round(s.swap_ancilla, 4) == 1.2025 and round(s.hadamard_u, 4) == 0.6066
    assert s.swap_destructive == pytest.approx(s.swap_ancilla, abs=1e-12)


def test_b4_noise_values_match_the_committed_result():
    pr = S.table("b4_pred")
    loc = pr[(pr.model == "local") & (pr.family == "rx_product") & (pr.fit_range == "secondary_n_ge_8")]
    assert np.allclose(loc.measured_b_S, FG._prop6_bS(loc.p.to_numpy()), atol=1e-3)
    g = pr[(pr.model == "global") & (pr.family == "rx_product") & (pr.fit_range == "secondary_n_ge_8") & (pr.p == 0.1)]
    assert float(g.measured_ratio_obs.iloc[0]) == pytest.approx(4 / 3, abs=0.02)
    cx = S.table("b4_crossover")
    r = cx[cx.family == "rx_product"].sort_values("p").n_star.round(1).tolist()
    assert r == [15.4, 12.1, 8.7, 5.2]


def test_prop6_closed_form_noiseless_limit():
    # Proposition 6 at p = 0 is log10 4, the noiseless RX-product b_S
    assert FG._prop6_bS(np.array([0.0]))[0] == pytest.approx(np.log10(4.0), abs=1e-15)


# builder ----------------------------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("figs")
    return out, FG.build(out, png=False)


def test_builder_writes_every_pdf_with_sources_and_manifest(built):
    out, man = built
    assert [f["name"] for f in man["figures"]] == EXPECTED
    for name in EXPECTED:
        pdf = out / f"{name}.pdf"
        assert pdf.exists() and pdf.read_bytes()[:5] == b"%PDF-"
    srcmd = (out / "FIGURE_SOURCES.md").read_text(encoding="utf-8")
    panels = [(p["figure"], p["panel"]) for p in FG.PANELS]
    assert len(panels) == len(set(panels)) == 22
    for fig, letter in panels:
        assert f"## Figure {fig}{letter.upper()}" in srcmd
    for p in FG.PANELS:
        for k in ("source", "columns", "filters", "aggregation", "ci", "function", "output"):
            assert p.get(k), (p["figure"], p["panel"], k)
    for f in man["figures"]:
        assert f["sources"], f["name"]
        for s in f["sources"]:
            assert _sha(ROOT / s["path"]) == s["sha256"]


def test_pdfs_are_deterministic_and_timestamp_free(built, tmp_path):
    out, man = built
    again = FG.build(tmp_path, png=False)
    a = {f["name"]: f["files"][0]["sha256"] for f in man["figures"]}
    b = {f["name"]: f["files"][0]["sha256"] for f in again["figures"]}
    assert a == b
    assert b"/CreationDate" not in (out / f"{EXPECTED[0]}.pdf").read_bytes()


def test_committed_figure_folder_is_complete():
    figs = ROOT / "paper" / "figures"
    man = json.loads((figs / "manifest.json").read_text(encoding="utf-8"))
    assert [f["name"] for f in man["figures"]] == EXPECTED
    for f in man["figures"]:
        for s in f["sources"]:                                               # committed figures were built from today's results
            assert _sha(ROOT / s["path"]) == s["sha256"], s["path"]
        for x in f["files"]:
            assert (figs / x["filename"]).exists()
    assert (figs / "FIGURE_SOURCES.md").exists()


# bibliography -----------------------------------------------------------------------------------------------------------
def test_bibliography_validates():
    assert CB.main() == 0


def test_bib_checks_reject_bad_identifiers():
    assert CB.DOI_RE.match("10.1103/PhysRevA.107.042421") and not CB.DOI_RE.match("doi:10.1103/x") and not CB.DOI_RE.match("10.1/x")
    assert CB.ARXIV_RE.match("2507.22054") and CB.ARXIV_RE.match("quant-ph/0005055")
    assert not CB.ARXIV_RE.match("2507.22054v2") and not CB.ARXIV_RE.match("arXiv:2507.22054")
    dup = "@article{a,\n  author = {X, Y},\n  title = {{T}},\n  year = {2020}\n}\n\n@article{a,\n  author = {X, Y},\n  title = {{T}},\n  year = {2020}\n}\n"
    keys = [e["key"] for e in CB.parse_bib(dup)]
    assert keys == ["a", "a"]


def test_bib_uses_b5_reviewed_versions_and_flags_unresolved():
    entries = {e["key"]: e for e in CB.parse_bib(BB.BIB.read_text(encoding="utf-8"))}
    manifest = {p["paper_id"]: p for p in json.loads(BB.MANIFEST.read_text(encoding="utf-8"))["papers"]}
    for pid, p in manifest.items():
        f = entries[pid]["fields"]
        assert BB._norm(f["title"]) == BB._norm(p["title"]) and f["year"] == str(p["year"])
        if p.get("volume"):
            assert f["volume"] == str(p["volume"]) and f["doi"] == p["doi"]
        assert f["b5reviewed"]
    assert entries["teo2023"]["fields"]["b5reviewed"] == "arXiv:2206.12643v3"
    assert entries["kaminishi2026"]["fields"]["doi"] == "10.1038/s41598-026-40123-3"
    audit = (ROOT / "paper" / "BIBLIOGRAPHY_AUDIT.md").read_text(encoding="utf-8")
    assert "wangfang2025" in audit and "wangfang2025" not in entries
    assert re.search(r"\| entries in `references.bib` \| 23 \|", audit)
