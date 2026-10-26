"""B1 tests. All deterministic: fixed seeds, exact identities, committed result tables (no statistical pass/fail)."""

from __future__ import annotations

import json
import subprocess
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from qlo.b1 import audit as A
from qlo.b1 import circuits as C
from qlo.b1 import config as CF
from qlo.b1 import fits as FT
from qlo.b1 import quantities as Q
from qlo.b1 import rx_product as RX
from qlo.b1 import sign_law as SL
from qlo.circuits.hardware_efficient import HardwareEfficientAnsatz
from qlo.hardening import intervals as IV
from qlo.hardening import seed_replicates as SR
from qlo.stage5.theory import log_a_k, s_k
from qlo.stage7 import analysis as AN
from qlo.stage7 import required_shots as R
from qlo.stage7.estimators import log10_shots_for_snr

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results" / "b1_entangling"
B3 = ROOT / "results" / "b3_hardening"
BASE_COMMIT = "00c8550"   # upstream merge of the delegated track (PR #3); Stage 2-7 and B3 files byte-identical to the B1 base


def _batch(family: str, n: int, depth: int, rows: int, seed: int = 5):
    theta = np.random.default_rng(seed).uniform(-np.pi, np.pi, (rows, depth, n, 2))
    pos = sorted(set(CF.distinct_positions(depth).values()))
    F, sh = C.shifted_fidelities(theta, family, n, depth, pos)
    return theta, pos, F, sh


# 1. RX regression formulas ------------------------------------------------------------------------------------------
def test_rx_pipeline_reproduces_stage7_closed_forms():
    q = RX.rx_per_theta(8, 500, seed=123, stream=20)
    th = AN.sample_theta(8, 500, 123, 20)
    logA, s = log_a_k(th, 0), s_k(th, 0)
    for scheme, key in (("loschmidt", "log10_M_LE"), ("swap", "log10_M_SWAP")):
        assert np.allclose(q[key], log10_shots_for_snr(scheme, logA, s, 1.0), rtol=0, atol=1e-11)
        # ceil(M) can move by one integer at M >~ 1e13 from a 1e-15 difference in log10 M: compare in log10
        assert np.allclose(q[f"{key}_ceil"], R.snr_shots(scheme, logA, s, 1.0), rtol=0, atol=1e-12)
    assert np.allclose(q["S"], np.exp(logA), rtol=1e-12, atol=0)
    assert np.allclose(q["r"], s, rtol=0, atol=1e-12)


def test_ceil_convention_matches_stage7_post_processing():
    l = np.array([-3.0, -0.2, 0.0, 0.3, 2.000001, 14.9, 15.0, 40.0, np.inf])
    out = Q.ceil_convention(l)
    assert out[0] == 0.0 and out[1] == 0.0 and out[2] == 0.0
    assert out[3] == np.log10(2.0) and out[4] == np.log10(101.0)
    assert out[6] == 15.0 and out[7] == 40.0 and np.isinf(out[8])


# 2. parameter-shift gradient vs exact / autograd, for every new ansatz ---------------------------------------------
@pytest.mark.parametrize("family", C.FAMILIES)
def test_simulator_state_matches_pennylane(family):
    theta = np.random.default_rng(1).uniform(-np.pi, np.pi, (3, 3, 4, 2))
    mine = C.forward(theta, family, 4, 3)[0]
    ref = A.pl_states(theta, family, 4, 3)
    assert np.max(np.abs(mine - ref)) < 1e-12


@pytest.mark.parametrize("family", C.FAMILIES)
def test_parameter_shift_gradient_matches_autograd_and_analytic(family):
    n, depth = 4, 3
    theta = np.random.default_rng(2).uniform(-np.pi, np.pi, (3, depth, n, 2))
    positions = [(l, 0, j) for l in range(depth) for j in (0, 1)]
    _, sh = C.shifted_fidelities(theta, family, n, depth, positions)
    G = A.pl_cost_gradients(theta, family, n, depth)
    for p in positions:
        g_ps = Q.per_theta(sh[p]["F_plus"], sh[p]["F_minus"])["g"]
        assert np.allclose(g_ps, G[:, p[0], p[1], p[2]], rtol=0, atol=1e-12)
        assert np.allclose(g_ps, C.analytic_cost_gradient(theta, family, n, depth, p), rtol=0, atol=1e-12)
        tp, tm = theta.copy(), theta.copy()
        tp[:, p[0], p[1], p[2]] += np.pi / 2
        tm[:, p[0], p[1], p[2]] -= np.pi / 2
        assert np.allclose(sh[p]["F_plus"], C.fidelity(tp, family, n, depth), rtol=0, atol=1e-13)
        assert np.allclose(sh[p]["F_minus"], C.fidelity(tm, family, n, depth), rtol=0, atol=1e-13)


@pytest.mark.parametrize("family", C.FAMILIES)
def test_fused_kernel_matches_per_qubit_reference(family):
    """The production path fuses up to 4 neighbouring rotations into one matrix; fuse=1 is the audited reference."""
    for n, depth in ((5, 3), (9, 2), (6, 6)):
        theta = np.random.default_rng(9).uniform(-np.pi, np.pi, (4, depth, n, 2))
        pos = set(CF.distinct_positions(depth).values()) | {(depth - 1, 0, 1)}
        F1, s1 = C.shifted_fidelities(theta, family, n, depth, pos, fuse=1)
        F4, s4 = C.shifted_fidelities(theta, family, n, depth, pos, fuse=4)
        assert np.allclose(F1, F4, rtol=1e-12, atol=1e-16)
        for p in pos:
            assert np.allclose(s1[p]["F_plus"], s4[p]["F_plus"], rtol=1e-12, atol=1e-16)
            assert np.allclose(s1[p]["F_minus"], s4[p]["F_minus"], rtol=1e-12, atol=1e-16)
        assert np.max(np.abs(C.forward(theta, family, n, depth, fuse=1)[0] - C.forward(theta, family, n, depth)[0])) < 1e-13


def test_repo_hea_entangler_and_brickwork_layout():
    for n in (2, 3, 4, 7):
        assert C.ring_pairs(n) == HardwareEfficientAnsatz(n, 1, "ring").entangling_pairs()
    assert C.brick_pairs(5, 0) == [(0, 1), (2, 3)] and C.brick_pairs(5, 1) == [(1, 2), (3, 4)]
    assert C.brick_pairs(6, 2) == [(0, 1), (2, 3), (4, 5)] and C.brick_pairs(6, 3) == [(1, 2), (3, 4)]
    assert C.AXES == {"hea_ring": ("Y", "Z"), "rxry_czbrick": ("X", "Y")}


# 3-5. ranges of F_+-, S, r ----------------------------------------------------------------------------------------
@pytest.mark.parametrize("family", C.FAMILIES)
def test_fidelities_sum_and_relative_gradient_in_range(family):
    _, pos, F, sh = _batch(family, 6, 4, 300)
    assert np.all((F >= 0) & (F <= 1 + 1e-12))
    for p in pos:
        q = Q.per_theta(sh[p]["F_plus"], sh[p]["F_minus"])
        assert np.all((q["F_plus"] >= 0) & (q["F_plus"] <= 1 + 1e-12))
        assert np.all((q["F_minus"] >= 0) & (q["F_minus"] <= 1 + 1e-12))
        assert np.all((q["S"] >= 0) & (q["S"] <= 2 + 1e-12))
        valid = q["S"] > 0
        assert np.all(np.abs(q["r"][valid]) <= 1 + 1e-12)
        assert np.allclose(sh[p]["F_bracket"], F, rtol=0, atol=1e-13)


# 6-8. identity, positivity, edge cases ------------------------------------------------------------------------------
def test_exact_shot_ratio_identity_sample_by_sample():
    rng = np.random.default_rng(3)
    fp = np.concatenate([rng.uniform(0, 1, 2000), 10.0 ** rng.uniform(-30, -1, 2000), 1 - 10.0 ** rng.uniform(-8, -1, 500)])
    fm = np.concatenate([rng.uniform(0, 1, 2000), 10.0 ** rng.uniform(-30, -1, 2000), rng.uniform(0, 1, 500)])
    q = Q.per_theta(fp, fm)
    chk = Q.identity_check(q)
    assert chk["n_excluded"] == 0 and chk["max_rel_err"] < 1e-12
    S, Qv = fp + fm, fp**2 + fm**2
    assert np.allclose(q["var_le_prefactor"], (S - Qv) / 4) and np.allclose(q["var_swap_prefactor"], (2 - Qv) / 4)


def test_shot_requirements_positive_where_defined_and_edge_cases_flagged():
    rng = np.random.default_rng(4)
    q = Q.per_theta(rng.uniform(0, 0.5, 1000), rng.uniform(0, 0.5, 1000), rho=2.0)
    ok = ~q["flag_delta_zero"]
    assert np.all(np.isfinite(q["log10_M_LE"][ok])) and np.all(10.0 ** q["log10_M_LE"][ok] > 0)
    assert np.all(np.isfinite(q["log10_M_SWAP"][ok])) and np.all(10.0 ** q["log10_M_SWAP"][ok] > 0)
    e = Q.per_theta(np.array([0.0, 0.3, 1.0, 1e-300]), np.array([0.0, 0.3, 0.0, 2e-300]))
    assert e["flag_S_zero"].tolist() == [True, False, False, False] and np.isnan(e["r"][0])
    assert e["flag_delta_zero"].tolist() == [True, True, False, False]
    assert np.isinf(e["log10_M_LE"][1]) and np.isinf(e["log10_M_SWAP"][1]) and e["log10_abs_r"][1] == -np.inf
    assert e["flag_var_le_zero"][2] and e["log10_M_LE"][2] == -np.inf          # deterministic LE outcomes: M_LE = 0
    assert e["flag_underflow"].tolist() == [False, False, False, True]
    chk = Q.identity_check(e)
    assert chk["n_excluded"] == 3 and chk["n_checked"] == 1
    d = Q.cell_diagnostics(e)
    assert d["n_S_zero"] == 1 and d["n_delta_zero"] == 2 and d["n_nan_log10_abs_r"] == 1


# 9. paired LE / SWAP ----------------------------------------------------------------------------------------------------
def test_le_and_swap_are_formed_from_the_same_rows():
    rng = np.random.default_rng(6)
    fp, fm = rng.uniform(0, 0.2, 500), rng.uniform(0, 0.2, 500)
    q = Q.per_theta(fp, fm)
    assert np.allclose(q["log10_R"], q["log10_R_identity"], rtol=0, atol=1e-12)
    perm = rng.permutation(500)
    q2 = Q.per_theta(fp[perm], fm[perm])
    assert np.allclose(q2["log10_M_SWAP"], q["log10_M_SWAP"][perm]) and np.allclose(q2["log10_M_LE"], q["log10_M_LE"][perm])
    with pytest.raises(ValueError):
        Q.per_theta(fp, fm[:-1])


# 10. seed reproducibility -----------------------------------------------------------------------------------------------
def test_theta_streams_reproducible_and_independent():
    a = CF.sample_theta("hea_ring", "d4", 6, 11_000, 50)
    assert np.array_equal(a, CF.sample_theta("hea_ring", "d4", 6, 11_000, 50))
    assert a.shape == (50, 4, 6, 2) and np.all(np.abs(a) <= np.pi)
    assert not np.allclose(a, CF.sample_theta("hea_ring", "d4", 6, 11_001, 50))
    assert not np.allclose(a, CF.sample_theta("rxry_czbrick", "d4", 6, 11_000, 50))
    assert not np.allclose(a[:, :4], CF.sample_theta("hea_ring", "dn", 6, 11_000, 50)[:, :4])
    assert not np.allclose(a, CF.audit_theta("hea_ring", "d4", 6, 50))
    assert np.array_equal(CF.sample_theta("hea_ring", "d4", 6, 11_000, 80)[:50], a)   # prefix-stable
    cfg = CF.B1Config()
    assert set(cfg.seeds).isdisjoint(SR.B3_SEEDS) and SR.STAGE7_SEED not in cfg.seeds and len(set(cfg.seeds)) == 10


# 11. structural-zero audit behaviour --------------------------------------------------------------------------------------
def test_structural_audit_flags_the_control_and_passes_valid_positions():
    cfg = replace(CF.B1Config(), audit_samples=40)
    rows = pd.DataFrame(A.audit_cell("hea_ring", "d2", 4, cfg))
    assert rows.agreement_ok.all() and rows.pennylane_checked.all()
    ctrl = rows[rows.position == "CONTROL_FINAL_RZ"].iloc[0]
    assert ctrl.classification == "STRUCTURAL" and ctrl.zero_fraction == 1.0 and ctrl.gate == "RZ"
    pre = rows[rows.role == "predeclared"]
    assert (pre.classification == "VALID").all()
    assert pre.set_index("position").loc["MIDDLE", "same_parameter_as"] == "LATE"


def test_classification_thresholds_and_fallback_rule():
    cfg = CF.B1Config()
    assert A.classify(1.0, 0.0, cfg) == "STRUCTURAL"
    assert A.classify(0.5, 1.0, cfg) == "DEGENERATE" and A.classify(0.0, 0.0, cfg) == "DEGENERATE"
    assert A.classify(0.0, 0.1, cfg) == "VALID" and A.classify(0.01, 0.1, cfg) == "VALID"
    assert A.fallback_candidates((2, 0, 0), 3) == [(1, 2, 0), (1, 1, 0), (1, 0, 0), (0, 2, 0), (0, 1, 0), (0, 0, 0)]
    assert A.fallback_candidates((1, 2, 1), 3)[:3] == [(1, 1, 1), (1, 0, 1), (0, 2, 1)]
    theta = CF.audit_theta("hea_ring", "d4", 4, 30)
    fb = A.fallback(theta, "hea_ring", 4, 4, (3, 0, 1), replace(cfg, audit_samples=30))
    assert fb["classification"] == "VALID" and fb["position"][2] == 1 and fb["position"] in A.fallback_candidates((3, 0, 1), 4)


def test_position_rules():
    assert CF.distinct_positions(2) == {"EARLY": (0, 0, 0), "LATE": (1, 0, 0)}
    assert CF.distinct_positions(4) == {"EARLY": (0, 0, 0), "MIDDLE": (2, 0, 0), "LATE": (3, 0, 0)}
    assert CF.position_map(7)["MIDDLE"] == (3, 0, 0) and CF.depth_of("dn", 12) == 12
    assert CF.control_positions("hea_ring", 4) == {"CONTROL_FINAL_RZ": (3, 0, 1)} and CF.control_positions("rxry_czbrick", 4) == {}


# 12-14. slope conventions, residuals, predicted ratio ------------------------------------------------------------------------
def _synthetic_medians(n_values, bS, br, bLE, bSW):
    n = np.asarray(n_values, dtype=float)
    return pd.DataFrame({"n": n_values, "n_rows": 100, "median_log10_S": 0.3 - bS * n, "median_log10_abs_r": -0.2 - br * n,
                         "median_log10_M_LE": 1.0 + bLE * n, "median_log10_M_SWAP": 2.0 + bSW * n})


def test_slope_sign_convention():
    f = FT.seed_fit(_synthetic_medians((4, 6, 8, 10), 0.5, 0.1, 0.7, 1.2), (4, 6, 8, 10))
    assert f["b_S"] == pytest.approx(0.5) and f["b_r"] == pytest.approx(0.1)
    assert f["b_LE"] == pytest.approx(0.7) and f["b_SWAP"] == pytest.approx(1.2)
    assert f["a_S"] == pytest.approx(0.3) and f["a_r"] == pytest.approx(-0.2)
    assert f["eps_LE"] == pytest.approx(0.0, abs=1e-12) and f["eps_SWAP"] == pytest.approx(0.0, abs=1e-12)
    assert f["eps_gap"] == pytest.approx(0.0, abs=1e-12) and f["r2_S"] == pytest.approx(1.0)
    with pytest.raises(ValueError):
        FT.fit_series([4, 6, 8], [0.1, np.nan, 0.3])


def test_eps_gap_calculation():
    rng = np.random.default_rng(7)
    for bS, br, bLE, bSW in rng.uniform(0.01, 2.0, (50, 4)):
        r = FT.prediction_residuals(bS, br, bLE, bSW)
        assert r["eps_gap"] == pytest.approx((bSW - bLE) - bS)
        assert r["eps_gap"] == pytest.approx(r["eps_SWAP"] - r["eps_LE"])
        assert r["eps_LE"] == pytest.approx(bLE - bS - 2 * br) and r["eps_SWAP"] == pytest.approx(bSW - 2 * bS - 2 * br)


def test_predicted_ratio_formula():
    assert FT.predicted_ratio(1.0, 0.0) == pytest.approx(2.0)
    assert FT.predicted_ratio(0.6, 0.0) == pytest.approx(2.0)
    assert FT.predicted_ratio(1.0, 0.5) == pytest.approx(1.5)
    assert FT.predicted_ratio(0.6, 0.15) == pytest.approx(1.5 / 0.9)
    r = FT.prediction_residuals(0.6, 0.15, 0.9, 1.5)
    assert r["ratio_obs"] == pytest.approx(1.5 / 0.9) and r["ratio_diff"] == pytest.approx(0.0, abs=1e-12)


# 15. B3 interval utilities ------------------------------------------------------------------------------------------------
def test_b3_interval_utilities_used_with_b3_settings():
    cfg = CF.B1Config()
    b3 = json.loads((B3 / "config.json").read_text())
    assert (cfg.n_boot_seed, cfg.boot_seed) == (b3["n_boot_seed"], b3["boot_seed"])
    rng = np.random.default_rng(8)
    rows = [{"family": "f", "regime": "d2", "position": "EARLY", "fit_range": "primary", "seed": s, "n_min": 4, "n_max": 16,
             **{m: v for m, v in zip(FT.METRICS, rng.normal(size=len(FT.METRICS)))}} for s in range(10)]
    fits = pd.DataFrame(rows)
    summ = FT.summarize_metrics(fits, cfg)
    for m in FT.METRICS:
        got = summ[summ.metric == m].iloc[0]
        ref = IV.summarize(fits.sort_values("seed")[m].values, cfg.n_boot_seed, cfg.boot_seed)
        for k in ("mean", "sd", "pct_lo", "pct_hi", "boot_lo", "boot_hi"):
            assert got[k] == ref[k]
    s = summ[summ.metric == "eps_gap"].iloc[0]
    assert FT.ci_contains(s, 0.0) == (s.boot_lo <= 0 <= s.boot_hi)


def test_sign_law_rows_exact_at_one_shot():
    fp, fm = np.array([1e-4, 3e-5, 2e-6]), np.array([4e-5, 1e-4, 5e-6])
    rows = SL.sign_law_rows(fp, fm, (0.5,), (1,), {"family": "x"})
    r = rows[0]
    i = r["theta_row"]
    p_pos, p_neg = fm[i], fp[i]                                  # LE: K_pos is the minus-shift count
    gt, lt = p_pos * (1 - p_neg), p_neg * (1 - p_pos)
    expect = (gt if p_pos > p_neg else lt) / (gt + lt)
    assert r["p_correct_given_nonzero"] == pytest.approx(expect, rel=1e-12)
    assert r["predicted"] == pytest.approx((1 + abs(fm[i] - fp[i]) / (fm[i] + fp[i])) / 2)


# 16. RX regression inside the hardened B3 acceptance range (committed results) ------------------------------------------------
def _need(path: Path) -> Path:
    if not path.exists():
        pytest.skip(f"{path.name} not generated yet")
    return path


def test_rx_regression_inside_b3_intervals():
    reg = pd.read_csv(_need(RES / "rx_regression.csv"))
    prim = reg[reg.role == "PRIMARY"]
    assert set(prim.metric) == {"b_LE_ceil", "b_SWAP_ceil", "gap_ceil", "b_S", "b_r"}
    assert prim.b1_mean_inside_b3_pct.all()
    pub = pd.read_csv(B3 / "seed_summary.csv")
    for m, b3m in (("b_LE_ceil", "slope_loschmidt_snr1"), ("b_SWAP_ceil", "slope_swap_snr1"), ("gap_ceil", "gap_swap_minus_le_snr1")):
        row = prim[prim.metric == m].iloc[0]
        ref = pub[(pub.fit_range == "primary_2_20") & (pub.metric == b3m)].iloc[0]
        # both values are read back from CSV; float parsing can differ in the last ulp between pandas versions
        assert row.b3_pct_lo == pytest.approx(ref.pct_lo, rel=1e-12) and row.b3_pct_hi == pytest.approx(ref.pct_hi, rel=1e-12)


def test_committed_rx_medians_reproduce_from_code():
    med = pd.read_csv(_need(RES / "sample_summary.csv"))
    cfg = CF.B1Config()
    row, _ = RX.rx_cell_row(10, cfg.rx_samples, cfg.seeds[0], cfg.rx_stream, 0, cfg.rho, cfg.audit_zero_tol_r)
    c = med[(med.family == "rx_product") & (med.n == 10) & (med.seed == cfg.seeds[0])].iloc[0]
    for k in ("median_log10_S", "median_log10_abs_r", "median_log10_M_LE", "median_log10_M_SWAP", "median_log10_M_LE_ceil"):
        assert c[k] == pytest.approx(row[k], rel=0, abs=1e-12)


# 17. no Stage 1-7 / B3 regression -------------------------------------------------------------------------------------------
def test_b3_populations_regenerate_exactly():
    med = RX.b3_regenerated_medians([10_000], SR.PRIMARY_N, 25_000)
    sl = RX.b3_regenerated_slopes(med, {"primary_2_20": SR.PRIMARY_N})
    pub = pd.read_csv(B3 / "seed_slopes.csv")
    for sc, col in (("loschmidt", "slope_loschmidt_snr1"), ("swap", "slope_swap_snr1")):
        ref = pub[(pub.seed == 10_000) & (pub.scheme == sc) & (pub.target == "snr1") & (pub.fit_range == "primary_2_20")].slope.iloc[0]
        assert sl[col].iloc[0] == pytest.approx(ref, rel=0, abs=1e-12)


def test_historical_files_untouched_since_b1_base():
    """Stage 2-7 reports, their results, B3 results and the Stage 5-7 / B3 code are byte-identical to the B1 base.

    The stage reports moved to docs/stages/ (pure renames), so they are compared blob to blob. principal/ is not
    checked: it is the principal track's living document and changes legitimately."""
    dirs = ["results/stage2", "results/stage3", "results/stage4", "results/stage5", "results/stage6", "results/stage7",
            "results/b3_hardening", "src/qlo/stage5", "src/qlo/stage6", "src/qlo/stage7", "src/qlo/hardening"]
    try:
        r = subprocess.run(["git", "diff", "--quiet", BASE_COMMIT, "--", *dirs], cwd=ROOT, capture_output=True)
        base_ok = subprocess.run(["git", "cat-file", "-e", f"{BASE_COMMIT}^{{commit}}"], cwd=ROOT, capture_output=True).returncode == 0
    except OSError:
        pytest.skip("git not available")
    if not base_ok or r.returncode not in (0, 1):
        pytest.skip("base commit not available in this clone")
    assert r.returncode == 0
    for k in range(2, 8):
        old = subprocess.run(["git", "rev-parse", f"{BASE_COMMIT}:STAGE{k}.md"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        new = subprocess.run(["git", "hash-object", f"docs/stages/STAGE{k}.md"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        assert old and old == new, f"STAGE{k}.md changed"


def test_config_is_frozen_in_b1_config_md():
    frozen = CF.config_json_from_markdown((ROOT / "docs" / "b1" / "B1_CONFIG.md").read_text())
    assert json.loads(frozen) == json.loads(CF.B1Config().to_json())
