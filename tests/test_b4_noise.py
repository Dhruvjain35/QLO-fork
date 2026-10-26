"""B4 tests: noise overlays against density-matrix simulation, closed forms, predictions, frozen config."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy.integrate import quad

from qlo.b1 import quantities as Q
from qlo.b4 import config as CF
from qlo.b4 import noise as N
from qlo.experiments import b4_noise as D
from qlo.stage5.theory import f_plus_minus, log_a_k, s_k

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results" / "b4_noise"


@pytest.mark.parametrize("p", [1e-3, 0.3])
def test_global_overlay_matches_density_matrix(p):
    rng = np.random.default_rng(1)
    for n in (2, 3):
        th = rng.uniform(-np.pi, np.pi, n)
        F = float(np.prod(np.cos(th / 2) ** 2))
        assert abs(N.dm_rx_global(th, p) - N.global_overlay(F, F, n, N.global_q(p, 1))[0]) < 1e-12
        par = rng.uniform(-np.pi, np.pi, (2, n, 2))
        assert abs(N.dm_hea_global(par, p) - N.global_overlay(N.pure_hea_fidelity(par), 0.0, n, N.global_q(p, 2))[0]) < 1e-12


@pytest.mark.parametrize("p", [1e-3, 0.3])
def test_local_formula_matches_density_matrix(p):
    th = np.random.default_rng(2).uniform(-np.pi, np.pi, (1, 3))
    fp, fm = N.rx_local(th, p)
    for sh, val in ((np.pi / 2, fp[0]), (-np.pi / 2, fm[0])):
        t = th[0].copy()
        t[0] += sh
        assert abs(N.dm_rx_local(t, p) - val) < 1e-12


def test_noiseless_limits_reproduce_stage7_closed_form():
    th = np.random.default_rng(3).uniform(-np.pi, np.pi, (200, 6))
    A, s = np.exp(log_a_k(th, 0)), s_k(th, 0)
    fp0, fm0 = f_plus_minus(A, s)
    gp, gm = N.global_overlay(fp0, fm0, 6, N.global_q(0.0, 4))
    assert np.array_equal(gp, fp0) and np.array_equal(gm, fm0)
    lp, lm = N.rx_local(th, 0.0)
    assert np.allclose(lp, fp0, rtol=1e-12) and np.allclose(lm, fm0, rtol=1e-12)


def test_global_overlay_algebra_and_identity_under_noise():
    rng = np.random.default_rng(4)
    fp, fm = rng.uniform(0, 1e-3, 1000), rng.uniform(0, 1e-3, 1000)
    q = N.global_q(0.05, 3)
    assert q == pytest.approx(0.95**3)
    a, b = N.global_overlay(fp, fm, 10, q)
    assert np.allclose(b - a, q * (fm - fp)) and np.allclose(a + b, q * (fp + fm) + 2 * (1 - q) / 2**10)
    chk = Q.identity_check(Q.per_theta(a, b))
    assert chk["n_excluded"] == 0 and chk["max_rel_err"] < 1e-12


def test_local_relative_gradient_is_noise_scaled_sine():
    th = np.random.default_rng(5).uniform(-np.pi, np.pi, (500, 8))
    for p in (1e-3, 0.1):
        fp, fm = N.rx_local(th, p)
        assert np.allclose((fm - fp) / (fm + fp), (1 - p) * np.sin(th[:, 0]), atol=1e-12)


@pytest.mark.parametrize("p", [1e-3, 1e-2, 0.1, 0.5])
def test_local_bS_closed_form(p):
    a, b = 1 - p, p / 2
    num = quad(lambda t: np.log(a * np.cos(t / 2) ** 2 + b) / (2 * np.pi), -np.pi, np.pi, limit=400)[0]
    assert num == pytest.approx(2 * np.log((np.sqrt(a + b) + np.sqrt(b)) / 2), rel=1e-12)


def test_predictions_rx_global_asymptotes():
    cfg = CF.B4Config()
    rows = []
    for p in (0.0, 1e-3):
        for m, v in (("b_S", np.log10(4)), ("b_r", 0.0), ("b_LE", 0.6), ("b_SWAP", 1.2), ("ratio_obs", 2.0),
                     ("eps_gap", 0.0), ("eps_LE", 0.0), ("eps_SWAP", 0.0)):
            rows.append({"model": "global", "p": p, "family": "rx_product", "regime": "product", "position": "k=0",
                         "fit_range": "primary", "metric": m, "mean": v})
    pr = D.predictions(pd.DataFrame(rows), cfg).set_index("p")
    r = pr.loc[1e-3]
    assert r.asym_b_S == pytest.approx(np.log10(2)) and r.asym_b_r == pytest.approx(np.log10(2))
    assert r.asym_b_LE == pytest.approx(np.log10(8)) and r.asym_b_SWAP == pytest.approx(np.log10(16))
    assert r.asym_ratio == pytest.approx(4 / 3)


def test_config_frozen():
    frozen = CF.config_json_from_markdown((ROOT / "docs" / "b4" / "B4_CONFIG.md").read_text())
    assert json.loads(frozen) == json.loads(CF.B4Config().to_json())


def test_committed_results_regression_and_identity():
    if not (RES / "regression_p0_vs_b1.csv").exists():
        pytest.skip("results not generated")
    reg = pd.read_csv(RES / "regression_p0_vs_b1.csv")
    assert len(reg) > 0 and reg.filter(like="absdiff").max().max() < 1e-12
    assert pd.read_csv(RES / "ratio_identity_validation.csv").max_rel_err.max() < 1e-10
    assert pd.read_csv(RES / "validation.csv").abs_err.max() < 1e-12


def test_per_theta_accepts_exact_delta_and_rejects_inconsistent_one():
    fp0, fm0 = np.array([1e-30, 2e-12]), np.array([3e-30, 5e-12])
    q = 0.9
    fp, fm = N.global_overlay(fp0, fm0, 20, q)
    out = Q.per_theta(fp, fm, delta=N.global_delta(fp0, fm0, q))
    assert out["delta"][0] == pytest.approx(q * 2e-30) and not out["flag_delta_zero"].any()
    with pytest.raises(ValueError):
        Q.per_theta(fp, fm, delta=np.array([1.0, 1.0]))
