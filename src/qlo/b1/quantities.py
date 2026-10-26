"""Per-theta B1 quantities from ONE pair (F_plus, F_minus). LE and SWAP are always formed from the same arrays.

    S = F_+ + F_-      Delta = F_- - F_+      r = Delta / S (S > 0)      g = Delta / 2 = dC/dtheta_k,  C = 1 - F
    Q = F_+^2 + F_-^2
    Loschmidt per-shot variances  v_LE   = F_+(1 - F_+) + F_-(1 - F_-)          (= S - Q;  Var_LE   = v_LE / 4M)
    SWAP per-shot variances       v_SWAP = 4[q_+(1 - q_+) + q_-(1 - q_-)],  q = (1 + F)/2   (= 2 - Q;  Var_SWAP = v_SWAP / 4M)
    M_LE   = rho^2 v_LE   / Delta^2        M_SWAP = rho^2 v_SWAP / Delta^2      (continuous; SNR = rho)
    R = M_SWAP / M_LE (from the two M's)   R_identity = (2 - Q) / (S - Q) (from S and Q directly)

Everything that is reported on a log scale is computed in log space. Edge cases are kept as rows and flagged:
    S = 0           r undefined (NaN), M infinite                    -> flag_S_zero
    Delta = 0       log10|r| = -inf, M_LE = M_SWAP = +inf             -> flag_delta_zero
    v_LE = 0        zero Loschmidt variance (F_+-, in {0, 1}): M_LE = 0 -> flag_var_le_zero
    underflow       S < 1e-280                                       -> flag_underflow
Nothing is dropped here; medians downstream run over all rows (+-inf are valid order statistics) and count NaN.
"""

from __future__ import annotations

import numpy as np

UNDERFLOW_S = 1e-280
LOG10_KEYS = ("log10_S", "log10_abs_r", "log10_M_LE", "log10_M_SWAP")


def per_theta(F_plus, F_minus, rho: float = 1.0, delta=None) -> dict:
    """``delta`` (optional): F_minus - F_plus computed exactly by the caller. Needed when both fidelities sit on a large
    common offset (e.g. a depolarizing floor) and their float difference would cancel; must agree with F_- - F_+ to
    rounding of the offset."""
    fp = np.asarray(F_plus, dtype=np.float64)
    fm = np.asarray(F_minus, dtype=np.float64)
    if fp.shape != fm.shape:
        raise ValueError("F_plus and F_minus must be paired row by row")
    S = fp + fm
    if delta is None:
        delta = fm - fp
    else:
        delta = np.asarray(delta, dtype=np.float64)
        if delta.shape != fp.shape or not np.all(np.abs(delta - (fm - fp)) <= 1e-12 * np.maximum(S, 1e-300)):
            raise ValueError("delta must equal F_minus - F_plus up to rounding")
    Q = fp**2 + fm**2
    v_le = fp * (1.0 - fp) + fm * (1.0 - fm)
    qp, qm = (1.0 + fp) / 2.0, (1.0 + fm) / 2.0
    v_sw = 4.0 * (qp * (1.0 - qp) + qm * (1.0 - qm))
    lr = 2.0 * np.log10(rho)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.where(S > 0, delta / S, np.nan)
        log10_abs_delta = np.log10(np.abs(delta))
        out = {
            "F_plus": fp, "F_minus": fm, "S": S, "delta": delta, "r": r, "g": delta / 2.0, "Q": Q,
            "var_le_prefactor": (S - Q) / 4.0, "var_swap_prefactor": (2.0 - Q) / 4.0,
            "log10_S": np.log10(S), "log10_abs_r": np.log10(np.abs(r)),
            "log10_M_LE": lr + np.log10(v_le) - 2.0 * log10_abs_delta,
            "log10_M_SWAP": lr + np.log10(v_sw) - 2.0 * log10_abs_delta,
            "log10_R_identity": np.log10(2.0 - Q) - np.log10(S - Q),
        }
    with np.errstate(invalid="ignore"):        # inf - inf (Delta = 0) -> NaN, flagged below and excluded by identity_check
        out["log10_R"] = out["log10_M_SWAP"] - out["log10_M_LE"]
    out["flag_S_zero"] = S == 0
    out["flag_delta_zero"] = delta == 0
    out["flag_var_le_zero"] = v_le == 0
    out["flag_underflow"] = (S > 0) & (S < UNDERFLOW_S)
    return out


def ceil_convention(log10_M) -> np.ndarray:
    """Stage 7 integer-budget convention (``qlo.stage7.required_shots.snr_shots``): log10 max(ceil(M), 1) for
    log10 M < 15, else max(log10 M, 0). Used ONLY to compare the RX arm with the B3 intervals."""
    l = np.asarray(log10_M, dtype=np.float64)
    small = l < 15.0
    out = np.maximum(l, 0.0)
    out[small] = np.log10(np.maximum(np.ceil(np.power(10.0, l[small])), 1.0))
    return out


def identity_check(q: dict) -> dict:
    """Sample-by-sample M_SWAP / M_LE vs (2 - Q)/(S - Q) on every non-degenerate row."""
    ok = (~q["flag_S_zero"]) & (~q["flag_delta_zero"]) & (~q["flag_var_le_zero"]) & np.isfinite(q["log10_R"]) \
        & np.isfinite(q["log10_R_identity"])
    R = np.power(10.0, q["log10_R"][ok])
    Rid = np.power(10.0, q["log10_R_identity"][ok])
    abs_err = np.abs(R - Rid)
    return {"n_rows": int(q["S"].size), "n_checked": int(ok.sum()), "n_excluded": int((~ok).sum()),
            "max_abs_err": float(abs_err.max()) if ok.any() else float("nan"),
            "max_rel_err": float((abs_err / Rid).max()) if ok.any() else float("nan"),
            "max_abs_log10_err": float(np.abs(q["log10_R"][ok] - q["log10_R_identity"][ok]).max()) if ok.any() else float("nan")}


def median_with_count(x) -> tuple[float, int]:
    """Median over every non-NaN row (+-inf included as order statistics) and the number of NaN rows."""
    x = np.asarray(x, dtype=np.float64)
    nan = np.isnan(x)
    return (float(np.median(x[~nan])) if (~nan).any() else float("nan")), int(nan.sum())


def cell_diagnostics(q: dict, zero_tol_r: float = 1e-10) -> dict:
    """Section 18 (fidelity) and 19 (relative gradient) diagnostics plus the per-cell medians that are fitted."""
    fp, fm, S = q["F_plus"], q["F_minus"], q["S"]
    ls = q["log10_S"]
    abs_r = np.abs(q["r"])
    lr = q["log10_abs_r"]
    fin_ls = ls[np.isfinite(ls)]
    fin_lr = lr[np.isfinite(lr)]
    d = {"n_rows": int(S.size),
         "n_S_zero": int(q["flag_S_zero"].sum()), "n_delta_zero": int(q["flag_delta_zero"].sum()),
         "n_var_le_zero": int(q["flag_var_le_zero"].sum()), "n_underflow": int(q["flag_underflow"].sum()),
         "n_r_numerically_zero": int(np.sum(abs_r <= zero_tol_r)),
         "n_nonfinite_log10_M_LE": int(np.sum(~np.isfinite(q["log10_M_LE"]))),
         "n_nonfinite_log10_M_SWAP": int(np.sum(~np.isfinite(q["log10_M_SWAP"]))),
         "mean_F_plus": float(fp.mean()), "mean_F_minus": float(fm.mean()),
         "median_F_plus": float(np.median(fp)), "median_F_minus": float(np.median(fm)),
         "mean_S": float(S.mean()), "median_S": float(np.median(S)),
         "mean_log10_S": float(fin_ls.mean()) if fin_ls.size else float("nan"),
         "geometric_mean_S": float(10.0 ** fin_ls.mean()) if fin_ls.size else float("nan"),
         "iqr_log10_S": float(np.subtract(*np.percentile(fin_ls, [75, 25]))) if fin_ls.size else float("nan"),
         "median_abs_r": float(np.nanmedian(abs_r)), "mean_abs_r": float(np.nanmean(abs_r)),
         "iqr_log10_abs_r": float(np.subtract(*np.percentile(fin_lr, [75, 25]))) if fin_lr.size else float("nan"),
         "frac_abs_r_lt_1e-1": float(np.nanmean(abs_r < 1e-1)), "frac_abs_r_lt_1e-2": float(np.nanmean(abs_r < 1e-2)),
         "frac_abs_r_lt_1e-3": float(np.nanmean(abs_r < 1e-3)),
         "median_log10_R": median_with_count(q["log10_R"])[0],
         "median_log10_R_times_S": median_with_count(q["log10_R"] + ls)[0]}      # -> log10 2 when S << 1
    for k in LOG10_KEYS:
        d[f"median_{k}"], d[f"n_nan_{k}"] = median_with_count(q[k])
    return d
