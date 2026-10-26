"""B2 tests: destructive SWAP, Hadamard U-statistic, shot conventions, required-shot inversion (all deterministic)."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from qlo.b2 import config as CF
from qlo.b2 import destructive_swap as DS
from qlo.b2 import hadamard as HD
from qlo.b2 import hadamard_theory as HT
from qlo.b2 import required_shots as RS
from qlo.stage5.theory import log_a_k, s_k
from qlo.stage7 import analysis as AN
from qlo.stage7 import required_shots as R

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results" / "b2_estimators"


def _rand_state(rng, n):
    v = rng.normal(size=2**n) + 1j * rng.normal(size=2**n)
    return v / np.linalg.norm(v)


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_destructive_swap_expectation_variance_and_ancilla_equality(n):
    rng = np.random.default_rng(n)
    for _ in range(3):
        psi, phi = _rand_state(rng, n), _rand_state(rng, n)
        F = abs(np.vdot(phi, psi)) ** 2
        p, z = DS.destructive_swap_outcomes(psi, phi)
        ez = float(np.sum(p * z))
        assert abs(ez - F) < 1e-12                                   # 1. E[Z] = F
        assert abs(float(np.sum(p * z * z)) - ez**2 - (1 - F**2)) < 1e-12   # 2. Var Z = 1 - F^2
        assert abs(DS.destructive_swap_p_plus(psi, phi) - DS.ancilla_swap_p_plus(psi, phi)) < 1e-12   # 3.


def test_bell_pair_path_matches_full_destructive_circuit_on_product_states():
    rng = np.random.default_rng(7)
    a = [_rand_state(rng, 1) for _ in range(3)]
    b = [_rand_state(rng, 1) for _ in range(3)]
    psi, phi = np.kron(np.kron(a[0], a[1]), a[2]), np.kron(np.kron(b[0], b[1]), b[2])
    p, z = DS.destructive_swap_outcomes(psi, phi)
    prod = np.prod([DS.bell_pair_expectation(a[i], b[i]) for i in range(3)])
    assert abs(float(np.sum(p * z)) - prod) < 1e-12


@pytest.mark.parametrize("n", [1, 2, 3])
def test_hadamard_quadratures_and_fidelity(n):
    rng = np.random.default_rng(10 + n)
    params = rng.uniform(-np.pi, np.pi, (2, n, 2))
    U = HD.hea_unitary(params, n, 2)
    a = U[0, 0]
    x, y = HD.pennylane_hadamard(params, n, 2, False), HD.pennylane_hadamard(params, n, 2, True)
    assert abs(x - a.real) < 1e-12 and abs(HD.hadamard_expectation(U, False) - a.real) < 1e-12     # 4.
    assert abs(y - a.imag) < 1e-12 and abs(HD.hadamard_expectation(U, True) - a.imag) < 1e-12      # 5.
    assert abs(x * x + y * y - abs(a) ** 2) < 1e-12                                                 # 6.
    assert abs(a.imag) > 1e-3                                                                        # genuinely complex


@pytest.mark.parametrize("q", [0.0, 0.3, -0.7, 0.95])
def test_u_statistic_unbiased_and_exact_variance_by_enumeration(q):
    for M in (2, 3, 4, 5, 6):
        p = (1 + q) / 2
        vals, w = [], []
        for seq in itertools.product([1, -1], repeat=M):
            vals.append(HT.u_stat(sum(seq), M))
            w.append(np.prod([p if s == 1 else 1 - p for s in seq]))
        vals, w = np.array(vals), np.array(w)
        mean = float(np.sum(w * vals))
        assert abs(mean - q * q) < 1e-13                                           # 7./8. (same function for x and y)
        assert abs(float(np.sum(w * (vals - mean) ** 2)) - float(HT.var_u(q, M))) < 1e-13   # 9./10.


def test_hadamard_fidelity_unbiased_pmf_sums_to_one():
    for x, y in ((0.31, -0.42), (0.0, 0.0), (0.9, 0.1)):
        for M in (2, 3, 8, 64):
            f, p = HT.f_ht_pmf(x, y, M)
            assert abs(p.sum() - 1) < 1e-12                                       # 14.
            assert abs(float(np.sum(p * f)) - (x * x + y * y)) < 1e-13             # 11.
            assert abs(float(np.sum(p * f * f) - np.sum(p * f) ** 2) - float(HT.var_f_ht(x, y, M))) < 1e-13


def test_hadamard_gradient_unbiased_and_variance():
    xp, yp, xm, ym = 0.2, 0.1, 0.35, -0.2
    for M in (2, 4, 16):
        fp, pp = HT.f_ht_pmf(xp, yp, M)
        fm, pm = HT.f_ht_pmf(xm, ym, M)
        g = (fm[None, :] - fp[:, None]) / 2
        w = pp[:, None] * pm[None, :]
        gm = float(np.sum(w * g))
        assert abs(gm - ((xm**2 + ym**2) - (xp**2 + yp**2)) / 2) < 1e-13         # 12.
        assert abs(float(np.sum(w * (g - gm) ** 2)) - float(HT.var_g_ht(xp, yp, xm, ym, M))) < 1e-13   # 13.
        s = HT.gradient_sign_exact(xp, yp, xm, ym, M)
        assert abs(s["p_pos"] + s["p_zero"] + s["p_neg"] - 1) < 1e-12
        assert abs(s["p_pos"] - float(np.sum(w[g > 0]))) < 1e-12 and abs(s["p_zero"] - float(np.sum(w[g == 0]))) < 1e-12


def test_shot_accounting_factors():
    assert CF.EXECUTIONS_PER_M == {"loschmidt": 2, "swap_ancilla": 2, "swap_destructive": 2, "hadamard_u": 4}   # 15.


def test_required_m_inversion_is_minimal_and_reaches_target():
    rng = np.random.default_rng(5)
    xp, xm = rng.uniform(-0.3, 0.3, 300), rng.uniform(-0.3, 0.3, 300)
    yp, ym = rng.uniform(-0.2, 0.2, 300), rng.uniform(-0.2, 0.2, 300)
    delta = (xm**2 + ym**2) - (xp**2 + yp**2)
    for rho in (1.0, 2.0):
        M = HT.required_m_ht(xp, yp, xm, ym, delta, rho)
        snr2 = (delta / 2) ** 2 / HT.var_g_ht(xp, yp, xm, ym, M)
        assert np.all(snr2 >= rho**2 * (1 - 1e-12))                                # 16.
        lower = np.maximum(M - 1, 2)
        ok = M > 2
        assert np.all((delta[ok] / 2) ** 2 / HT.var_g_ht(xp, yp, xm, ym, lower)[ok] < rho**2)


def test_destructive_and_ancilla_required_shots_equal_and_paired():
    r = RS.required_all(10, 3000, 0, 20, 1.0)
    m = r["log10_m_internal"]
    assert np.median(np.abs(m["swap_destructive"] - m["swap_ancilla"])) < 1e-12    # 17.
    assert np.quantile(np.abs(m["swap_destructive"] - m["swap_ancilla"]), 0.99) < 1e-8
    th = AN.sample_theta(10, 3000, 0, 20)                                           # 18. same theta for all estimators
    assert np.allclose(r["theta_q"]["s"], s_k(th, 0)) and np.allclose(r["theta_q"]["logA"], log_a_k(th, 0))
    assert all(v.shape == (3000,) for v in m.values())


def test_stage7_le_swap_unchanged():
    r = RS.required_all(8, 2000, 0, 20, 1.0)                                        # 19.
    th = AN.sample_theta(8, 2000, 0, 20)
    for sc, e in (("loschmidt", "loschmidt"), ("swap", "swap_ancilla")):
        assert np.array_equal(r["log10_m_internal"][e], R.snr_shots(sc, log_a_k(th, 0), s_k(th, 0), 1.0))


def test_committed_stage7_regression_and_config_frozen():
    frozen = CF.config_json_from_markdown((ROOT / "docs" / "b2" / "B2_CONFIG.md").read_text())
    assert json.loads(frozen) == json.loads(CF.B2Config().to_json())
    p = RES / "stage7_regression.csv"
    if not p.exists():
        pytest.skip("results not generated")
    assert pd.read_csv(p).abs_diff.max() < 1e-12
