"""Exact finite-shot theory of the Hadamard-test fidelity estimator (derivation: docs/b2/B2_HADAMARD_DERIVATION.md).

Overlap a = <phi|psi> = x + i y. One quadrature batch: M iid outcomes X_i in {+1, -1}, E[X_i] = q (q = x or y),
S = sum_i X_i = 2K - M with K ~ Bin(M, (1 + q)/2).

    U(S, M) = (S^2 - M) / [M (M - 1)]                    unbiased for q^2   (M >= 2)
    Var U   = [2 (1 - q^4) + 4 (M - 2) q^2 (1 - q^2)] / [M (M - 1)]
    F_hat   = U_x + U_y   (independent batches)         unbiased for F = x^2 + y^2
    g_hat   = (F_hat(-) - F_hat(+)) / 2   (independent shifted batches), Var g = [Var F(+) + Var F(-)] / 4
M is the number of shots PER QUADRATURE PER SHIFT; one gradient component costs 4M circuit executions.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import binom


def u_stat(S, M):
    S, M = np.asarray(S, dtype=np.float64), np.asarray(M, dtype=np.float64)
    return (S**2 - M) / (M * (M - 1.0))


def var_u(q, M):
    q2, M = np.asarray(q, dtype=np.float64) ** 2, np.asarray(M, dtype=np.float64)
    return (2.0 * (1.0 - q2**2) + 4.0 * (M - 2.0) * q2 * (1.0 - q2)) / (M * (M - 1.0))


def var_f_ht(x, y, M):
    return var_u(x, M) + var_u(y, M)


def var_g_ht(xp, yp, xm, ym, M):
    return (var_f_ht(xp, yp, M) + var_f_ht(xm, ym, M)) / 4.0


def _var_g_coeffs(xp, yp, xm, ym):
    """4 M (M - 1) Var g = A + B (M - 2) with A = 2 sum(1 - q^4), B = 4 sum q^2 (1 - q^2) over the 4 quadratures."""
    qs = [np.asarray(v, dtype=np.float64) ** 2 for v in (xp, yp, xm, ym)]
    A = 2.0 * sum(1.0 - q2**2 for q2 in qs)
    B = 4.0 * sum(q2 * (1.0 - q2) for q2 in qs)
    return A, B


def required_m_ht(xp, yp, xm, ym, delta, rho: float = 1.0) -> np.ndarray:
    """Smallest integer M >= 2 with SNR = |g| / sqrt(Var g) >= rho, g = delta / 2 (exact integer inversion).

    Var g(M) is decreasing in M, so the condition is c M (M - 1) - B M - (A - 2B) >= 0 with c = 4 g^2 / rho^2; the
    closed-form root is rounded up and then corrected by direct evaluation of the exact variance."""
    A, B = _var_g_coeffs(xp, yp, xm, ym)
    g2 = (np.asarray(delta, dtype=np.float64) / 2.0) ** 2
    c = 4.0 * g2 / rho**2
    with np.errstate(divide="ignore", invalid="ignore"):
        b = c + B
        root = (b + np.sqrt(b * b + 4.0 * c * (A - 2.0 * B))) / (2.0 * c)
    M = np.where(c > 0, np.maximum(2.0, np.ceil(root)), np.inf)
    target = g2 / rho**2
    fin = np.isfinite(M)
    for _ in range(3):                                   # integer correction (both directions)
        too_small = fin & (var_g_ht(xp, yp, xm, ym, M) > target)
        M = np.where(too_small, M + 1.0, M)
        can_lower = fin & (M > 2) & (var_g_ht(xp, yp, xm, ym, np.maximum(M - 1.0, 2.0)) <= target)
        M = np.where(can_lower, M - 1.0, M)
    return M


# ---- exact small-M distributions ------------------------------------------------------------------------------
def s_pmf(q: float, M: int) -> tuple[np.ndarray, np.ndarray]:
    """Support and pmf of S = 2K - M, K ~ Bin(M, (1 + q)/2)."""
    k = np.arange(M + 1)
    return 2 * k - M, binom.pmf(k, M, (1.0 + q) / 2.0)


def _square_pmf(q: float, M: int) -> tuple[np.ndarray, np.ndarray]:
    """Distinct values of S^2 (S = 2K - M) and their probabilities."""
    s, p = s_pmf(q, M)
    sq = s.astype(np.int64) ** 2
    vals, inv = np.unique(sq, return_inverse=True)
    return vals, np.bincount(inv, weights=p)


def t_pmf(x: float, y: float, M: int) -> tuple[np.ndarray, np.ndarray]:
    """Exact pmf of T = S_x^2 + S_y^2 (sparse: only reachable lattice points); F_hat = (T - 2M) / [M (M - 1)]."""
    vx, px = _square_pmf(x, M)
    vy, py = _square_pmf(y, M)
    t = (vx[:, None] + vy[None, :]).ravel()
    w = (px[:, None] * py[None, :]).ravel()
    vals, inv = np.unique(t, return_inverse=True)
    return vals, np.bincount(inv, weights=w)


def f_ht_pmf(x: float, y: float, M: int) -> tuple[np.ndarray, np.ndarray]:
    t, p = t_pmf(x, y, M)
    return (t - 2.0 * M) / (M * (M - 1.0)), p


def gradient_sign_exact(xp, yp, xm, ym, M: int) -> dict:
    """Exact P(g_hat > 0), P(g_hat = 0), P(g_hat < 0) for g_hat = (F_hat(-) - F_hat(+))/2, i.e. sign(T(-) - T(+))."""
    tp, pp = t_pmf(xp, yp, M)
    tm, pm = t_pmf(xm, ym, M)
    cdf_p = np.cumsum(pp)
    idx = np.searchsorted(tp, tm, side="left")          # number of T(+) values strictly below t(-)
    below = np.where(idx > 0, cdf_p[np.maximum(idx - 1, 0)], 0.0)
    eq_idx = np.searchsorted(tp, tm, side="left")
    hit = (eq_idx < tp.size) & (tp[np.minimum(eq_idx, tp.size - 1)] == tm)
    equal = np.where(hit, pp[np.minimum(eq_idx, tp.size - 1)], 0.0)
    p_pos = float(np.sum(pm * below))
    p_zero = float(np.sum(pm * equal))
    return {"p_pos": p_pos, "p_zero": p_zero, "p_neg": max(0.0, 1.0 - p_pos - p_zero)}


def sample_f_ht(rng, x, y, M: int, size) -> np.ndarray:
    """Monte Carlo draws of F_hat_HT from the binomial outcome counts (no analytic shortcut)."""
    Kx = rng.binomial(M, (1.0 + np.asarray(x)) / 2.0, size=size)
    Ky = rng.binomial(M, (1.0 + np.asarray(y)) / 2.0, size=size)
    return u_stat(2 * Kx - M, M) + u_stat(2 * Ky - M, M)
