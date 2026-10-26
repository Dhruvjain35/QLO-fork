"""Stage 7 driver: same fidelity landscape, Loschmidt (projector) vs SWAP-test finite-shot gradients.

    python -m qlo.experiments.stage7 --workers 5    # everything -> results/stage7/
    python -m qlo.experiments.stage7 --fast         # reduced sample counts (smoke run)

No optimizer is implemented (Task 17 is a fixed-eta diagnostic). Stage 3-6 code is reused unmodified.
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binom, norm

from qlo.stage5.theory import a_k, f_plus_minus, log_a_k, s_k
from qlo.stage6.analysis import linear_fit, wilson_ci
from qlo.stage6.directional import direction_probabilities, shots_for_direction_exact
from qlo.stage6.exact_distribution import (
    difference_probabilities,
    difference_probabilities_bruteforce,
    p_equal_zero_signal,
    p_equal_zero_signal_asymptotic,
)
from qlo.stage7 import analysis as AN
from qlo.stage7 import estimators as E
from qlo.stage7 import figures as FIG
from qlo.stage7 import required_shots as R
from qlo.stage7.pennylane_check import make_loschmidt, make_swap, swap_expval

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "stage7"
REF_SLOPE = {"log10_4": float(np.log10(4.0)), "log10_16": float(np.log10(16.0))}


@dataclass(frozen=True)
class Stage7Config:
    n_values: tuple[int, ...] = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
    n_samples: int = 100_000
    seed: int = 0
    paired_n: tuple[int, ...] = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
    paired_samples: int = 20_000
    paired_shots: tuple[int, ...] = (64, 1024, 16384)
    vector_n: tuple[int, ...] = (4, 6, 8, 10, 12)
    vector_shots: tuple[int, ...] = (16, 64, 256, 1024, 4096)
    vector_theta: int = 400
    vector_replicates: int = 25
    info_samples: int = 20_000
    replication_shots: tuple[int, ...] = (64, 1024, 16384)
    replication_samples: int = 20_000
    pl_n: tuple[int, ...] = (2, 3, 4)
    pl_shots: tuple[int, ...] = (32, 128, 512)
    pl_reps: int = 300
    opt_n: tuple[int, ...] = (6, 8, 10, 12)
    opt_seeds: int = 50
    opt_iters: int = 500
    # predeclared, NOT tuned here: the finite-shot learning rate selected by the Stage 4 protocol on this same
    # benchmark (A' / B in docs/stages/STAGE4.md), used unchanged for every variant including exact GD
    opt_eta: float = 0.3
    opt_variants: tuple = (("exact", None, 0), ("LE M=64", "loschmidt", 64), ("SWAP M=64", "swap", 64),
                           ("SWAP M=32 (state-copy matched to LE M=64)", "swap", 32),
                           ("LE M=1024", "loschmidt", 1024), ("SWAP M=1024", "swap", 1024),
                           ("SWAP M=512 (state-copy matched to LE M=1024)", "swap", 512),
                           # random-walk controls: SWAP shot noise with the gradient signal removed (q_+ = q_- = 1/2)
                           ("SWAP-noise random walk M=64", "swap_null", 64), ("SWAP-noise random walk M=1024", "swap_null", 1024))


# ------------------------------------------------------------------------------------------------
def theory_validation(cfg: Stage7Config) -> dict:
    rng = np.random.default_rng(7)
    err = {k: 0.0 for k in ("F_plus_direct", "F_minus_direct", "gradient_vs_fd", "gradient_A_s_over_2", "F2_sum_identity",
                            "le_counts_vs_simplified", "swap_counts_vs_simplified", "le_var_closed_vs_generic",
                            "swap_var_closed_vs_generic", "le_snr_vs_g2_over_var", "swap_snr_vs_g2_over_var",
                            "swap_fhat_var_vs_4q1q", "implied_g_identical")}
    Fz = lambda t: float(np.prod(np.cos(t / 2.0) ** 2))
    for _ in range(300):
        n = int(rng.integers(2, 9)); th = rng.uniform(-np.pi, np.pi, n); k = int(rng.integers(0, n)); M = float(rng.integers(1, 4000))
        A, s = float(a_k(th, k)), float(s_k(th, k))
        fp, fm = (float(x) for x in f_plus_minus(A, s))
        e = np.zeros(n); e[k] = np.pi / 2
        err["F_plus_direct"] = max(err["F_plus_direct"], abs(Fz(th + e) - fp))
        err["F_minus_direct"] = max(err["F_minus_direct"], abs(Fz(th - e) - fm))
        h = np.zeros(n); h[k] = 1e-6
        err["gradient_vs_fd"] = max(err["gradient_vs_fd"], abs(-(Fz(th + h) - Fz(th - h)) / 2e-6 - A * s / 2))
        err["gradient_A_s_over_2"] = max(err["gradient_A_s_over_2"], abs(0.5 * ((1 - fp) - (1 - fm)) - A * s / 2))
        err["F2_sum_identity"] = max(err["F2_sum_identity"], abs(fp**2 + fm**2 - A**2 * (1 + s**2) / 2))
        kp, km = rng.integers(0, int(M) + 1, 2)
        for sc in E.SCHEMES:
            key = "le" if sc == "loschmidt" else "swap"
            err[f"{key}_counts_vs_simplified"] = max(err[f"{key}_counts_vs_simplified"],
                                                    abs(float(E.gradient_from_counts(sc, kp, km, M) - E.gradient_from_counts_simplified(sc, kp, km, M))))
            vc, vg = float(E.gradient_variance(sc, A, s, M)), float(E.gradient_variance_generic(sc, A, s, M))
            err[f"{key}_var_closed_vs_generic"] = max(err[f"{key}_var_closed_vs_generic"], abs(vc - vg) / max(vg, 1e-300))
            snr2 = float(E.snr_squared(sc, A, s, M))
            if snr2 > 0:
                err[f"{key}_snr_vs_g2_over_var"] = max(err[f"{key}_snr_vs_g2_over_var"], abs(snr2 - (A * s / 2) ** 2 / vc) / snr2)
            p_pos, p_neg, c = E.pair(sc, A, s)
            err["implied_g_identical"] = max(err["implied_g_identical"], abs(float(c * (p_pos - p_neg)) - A * s / 2))
        q = (1 + fp) / 2
        err["swap_fhat_var_vs_4q1q"] = max(err["swap_fhat_var_vs_4q1q"], abs(float(E.fidelity_estimate_variance("swap", fp, M)) - 4 * q * (1 - q) / M))

    # exact enumeration: unbiasedness and variance for both schemes
    enum = []
    for (A, s, M) in ((0.8, 0.3, 7), (0.05, -0.7, 12), (0.5, 0.0, 9), (1e-3, 0.9, 25)):
        for sc in E.SCHEMES:
            pp, pm = E.outcome_probabilities(sc, A, s)
            r = np.arange(M + 1)
            W = binom.pmf(r, M, pp)[:, None] * binom.pmf(r, M, pm)[None, :]
            G = E.gradient_from_counts(sc, r[:, None], r[None, :], M)
            mean = float(np.sum(W * G)); var = float(np.sum(W * G * G)) - mean**2
            enum.append({"scheme": sc, "A": A, "s": s, "M": M, "mean": mean, "g": A * s / 2, "abs_bias": abs(mean - A * s / 2),
                         "var": var, "var_closed": float(E.gradient_variance(sc, A, s, M)),
                         "rel_var_err": abs(var - float(E.gradient_variance(sc, A, s, M))) / float(E.gradient_variance(sc, A, s, M))})

    # SNR deep-plateau approximations (A -> 0)
    deep = []
    for A in (1e-2, 1e-4, 1e-8):
        s, M = 0.6, 1000.0
        deep.append({"A": A, "le_snr2_over_MAs2": float(E.snr_squared("loschmidt", A, s, M) / (M * A * s**2)),
                     "swap_snr2_over_MA2s2_half": float(E.snr_squared("swap", A, s, M) / (M * A**2 * s**2 / 2)),
                     "snr2_ratio_swap_over_le": float(E.snr_squared("swap", A, s, M) / E.snr_squared("loschmidt", A, s, M))})

    # deep-limit zero probabilities: SWAP -> central binomial; Loschmidt -> 1
    zero = []
    for M in (1, 10, 100, 1000, 10_000, 100_000):
        pp, pm, _ = E.pair("swap", 1e-12, 0.5)
        _, eq_sw, _ = difference_probabilities(pp, pm, M)
        pp, pm, _ = E.pair("loschmidt", 1e-8, 0.5)
        _, eq_le, _ = difference_probabilities(pp, pm, M)
        zero.append({"M": M, "swap_p_zero_A1e-12": float(eq_sw), "central_binomial": float(p_equal_zero_signal(M)),
                     "one_over_sqrt_pi_M": float(p_equal_zero_signal_asymptotic(M)),
                     "swap_rel_err_vs_central_binomial": abs(float(eq_sw) / float(p_equal_zero_signal(M)) - 1),
                     "loschmidt_p_zero_A1e-8": float(eq_le)})

    # brute force of the exact difference distribution on SWAP-like probabilities
    bf = 0.0
    for _ in range(80):
        A, s, M = rng.uniform(0, 1), rng.uniform(-1, 1), int(rng.integers(1, 70))
        for sc in E.SCHEMES:
            pp, pm, _ = E.pair(sc, A, s)
            got = difference_probabilities(pp, pm, M); ref = difference_probabilities_bruteforce(float(pp), float(pm), M)
            bf = max(bf, max(abs(float(a) - b) for a, b in zip(got, ref)))

    # P_correct + P_wrong + P_zero, Loschmidt conditional sign quality, SWAP normal approximation
    cond, normal = [], []
    for A in (1e-2, 1e-4, 1e-6):
        for M in (1e2, 1e4, 1e6, 1e8):
            pp, pm, _ = E.pair("loschmidt", A, 0.5)
            d = direction_probabilities(pp, pm, M)
            nz = 1 - float(d["p_zero"])
            cond.append({"A": A, "s": 0.5, "M": M, "p_zero": float(d["p_zero"]), "p_correct": float(d["p_correct"]),
                         "p_wrong": float(d["p_wrong"]), "p_correct_given_nonzero": float(d["p_correct"]) / nz if nz > 0 else float("nan"),
                         "sum": float(d["p_correct"] + d["p_wrong"] + d["p_zero"])})
    for A in (0.5, 0.1, 0.02):
        for M in (16, 256, 4096, 65536):
            s = 0.6
            pp, pm, _ = E.pair("swap", A, s)
            d = direction_probabilities(pp, pm, M)
            snr = float(np.sqrt(E.snr_squared("swap", A, s, M)))
            mean = M * A * s / 2; sd = np.sqrt(M * (pp * (1 - pp) + pm * (1 - pm)))
            normal.append({"A": A, "s": s, "M": M, "snr": snr, "p_correct_exact": float(d["p_correct"]), "phi_snr": float(norm.cdf(snr)),
                           "phi_continuity": float(norm.cdf((mean - 0.5) / sd)),
                           "abs_err_plain": abs(float(norm.cdf(snr)) - float(d["p_correct"])),
                           "abs_err_continuity": abs(float(norm.cdf((mean - 0.5) / sd)) - float(d["p_correct"]))})

    # integer-M monotonicity (bisection preconditions): P_correct non-decreasing, P_zero non-increasing
    mono = {}
    Mg = np.unique(np.round(np.logspace(0, 4, 160)))
    for sc in E.SCHEMES:
        worst_c = worst_z = 0.0
        for n in (4, 8, 12):
            th = AN.sample_theta(n, 40, 0, 5)
            A, s = np.exp(log_a_k(th, 0)), s_k(th, 0)
            pp, pn, _ = E.pair(sc, A, s)
            d = direction_probabilities(pp[:, None], pn[:, None], Mg[None, :])
            worst_c = max(worst_c, float(np.max(np.maximum(d["p_correct"][:, :-1] - d["p_correct"][:, 1:], 0.0))))
            worst_z = max(worst_z, float(np.max(np.maximum(d["p_zero"][:, 1:] - d["p_zero"][:, :-1], 0.0))))
        mono[sc] = {"max_decrease_p_correct": worst_c, "max_increase_p_zero": worst_z}

    # SWAP normal-cc inversion vs exact integer inversion at the handover (~1e3..1e4 shots)
    A = np.full(400, 0.02); s = np.random.default_rng(3).uniform(0.15, 1.0, 400)
    v = (2 - A**2 * (1 + s**2) / 2) / 4
    handover = {}
    for q in (0.75, 0.90):
        ln = R.log10_normal_cc_direction(np.log(A * s / 2), v, q)
        pp, pn, _ = E.pair("swap", A, s)
        me, ok = shots_for_direction_exact(pp, pn, q, lo_log10=ln - 1, hi_log10=ln + 1)
        handover[str(q)] = {"log10M_range": [float(ln.min()), float(ln.max())], "all_reached": bool(ok.all()),
                            "max_abs_log10_err": float(np.max(np.abs(np.log10(me) - ln)))}

    return {"identities_max_err": err, "exact_enumeration": enum, "snr_deep_limit": deep, "deep_limit_zero_probability": zero,
            "difference_distribution_max_err_vs_bruteforce": bf, "loschmidt_conditional_sign": cond, "swap_normal_approximation": normal,
            "integer_M_monotonicity": mono, "swap_normal_cc_inversion_handover": handover,
            "resource_accounting_example_n8_M1024": [E.resource_accounting(sc, 8, 1024) for sc in E.SCHEMES]}


# ------------------------------------------------------------------------------------------------
def pennylane_validation(cfg: Stage7Config) -> pd.DataFrame:
    rows = []
    for n in cfg.pl_n:
        pool = AN.sample_theta(n, 400, 0, 80)
        lg = np.log(np.abs(a_k(pool, 0) * s_k(pool, 0)) / 2)
        picks = [("lower-quartile |g|", pool[np.argmin(np.abs(lg - np.percentile(lg, 25)))]),
                 ("median |g|", pool[np.argmin(np.abs(lg - np.percentile(lg, 50)))]),
                 ("upper-quartile |g|", pool[np.argmin(np.abs(lg - np.percentile(lg, 75)))])]
        for li, (lab, th) in enumerate(picks):
            A, s = float(a_k(th, 0)), float(s_k(th, 0))
            g = A * s / 2
            e = np.zeros(n); e[0] = np.pi / 2
            for M in cfg.pl_shots:
                for si, sc in enumerate(E.SCHEMES):
                    maker = make_loschmidt if sc == "loschmidt" else make_swap
                    counter = maker(n, M, np.random.default_rng(np.random.SeedSequence([7, 800, n, li, M, si])))
                    kp = np.array([counter(th + e) for _ in range(cfg.pl_reps)])
                    km = np.array([counter(th - e) for _ in range(cfg.pl_reps)])
                    gpl = E.gradient_from_counts(sc, kp, km, M)
                    fhat = E.fidelity_estimate(sc, kp, M)
                    pp, pm = E.outcome_probabilities(sc, A, s)
                    rng = np.random.default_rng(np.random.SeedSequence([7, 801, n, li, M, si]))
                    gbi = E.gradient_from_counts(sc, rng.binomial(M, pp, cfg.pl_reps), rng.binomial(M, pm, cfg.pl_reps), M)
                    p_pos, p_neg, _ = E.pair(sc, A, s)
                    d = direction_probabilities(p_pos, p_neg, float(M))
                    var_a = float(E.gradient_variance(sc, A, s, M))
                    F_plus = float(f_plus_minus(A, s)[0])
                    zc, cc = int(np.sum(gpl == 0)), int(np.sum(np.sign(gpl) == np.sign(g)))
                    lz, hz = wilson_ci(zc, cfg.pl_reps); lc, hc = wilson_ci(cc, cfg.pl_reps)
                    se = np.sqrt(gpl.var(ddof=1) / cfg.pl_reps + gbi.var(ddof=1) / cfg.pl_reps)
                    rows.append({"n": n, "label": lab, "shots": M, "scheme": sc, "reps": cfg.pl_reps, "F_plus": F_plus, "g_exact": g,
                                 "fhat_plus_mean": float(fhat.mean()), "fhat_plus_z": float((fhat.mean() - F_plus) / np.sqrt(float(E.fidelity_estimate_variance(sc, F_plus, M)) / cfg.pl_reps)) if F_plus < 1 else 0.0,
                                 "fhat_plus_var_ratio": float(fhat.var(ddof=1) / float(E.fidelity_estimate_variance(sc, F_plus, M))) if float(E.fidelity_estimate_variance(sc, F_plus, M)) > 0 else float("nan"),
                                 "grad_mean_pl": float(gpl.mean()), "grad_mean_binomial": float(gbi.mean()),
                                 "grad_z_pl_vs_exact": float((gpl.mean() - g) / np.sqrt(var_a / cfg.pl_reps)),
                                 "grad_z_pl_vs_binomial": float((gpl.mean() - gbi.mean()) / se) if se > 0 else 0.0,
                                 "grad_var_ratio_pl": float(gpl.var(ddof=1) / var_a), "grad_var_ratio_binomial": float(gbi.var(ddof=1) / var_a),
                                 "p_zero_pl": zc / cfg.pl_reps, "p_zero_exact": float(d["p_zero"]), "p_zero_in_ci": bool(lz <= float(d["p_zero"]) <= hz),
                                 "p_correct_pl": cc / cfg.pl_reps, "p_correct_exact": float(d["p_correct"]), "p_correct_in_ci": bool(lc <= float(d["p_correct"]) <= hc),
                                 "swap_expval_minus_F": abs(swap_expval(n, th + e) - F_plus) if sc == "swap" else float("nan")})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------
def fit_table(summary: pd.DataFrame) -> dict:
    fits = {}
    for sc in E.SCHEMES:
        s = summary[summary.scheme == sc].sort_values("n")
        for tag, _, _ in AN.TARGETS:
            col = f"{tag}_log10M_median"
            d = s.dropna(subset=[col])
            f = linear_fit(d.n, d[col])
            ref_key = "log10_4" if (sc == "loschmidt" or tag.startswith("nz")) else "log10_16"
            ref = None if (sc == "swap" and tag.startswith("nz")) else REF_SLOPE[ref_key]
            f.update({"scheme": sc, "target": tag, "reference": ref_key if ref is not None else "none (SWAP P_nonzero is ~M-only in the deep regime)",
                      "reference_slope": ref, "abs_err_vs_reference": abs(f["slope"] - ref) if ref is not None else None})
            # the deep regime only (n >= 8), where the asymptotic references apply
            dd = d[d.n >= 8]
            if len(dd) >= 3:
                fd = linear_fit(dd.n, dd[col])
                f.update({"slope_n_ge_8": fd["slope"], "r2_n_ge_8": fd["r2"]})
            fits[f"{sc}_{tag}"] = f
    return fits


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    p.add_argument("--fast", action="store_true")
    p.add_argument("--workers", type=int, default=5, help="processes for the per-n required-shot solves (results do not depend on it)")
    a = p.parse_args(argv)
    cfg = Stage7Config()
    if a.fast:
        cfg = Stage7Config(n_samples=3000, paired_samples=2000, vector_theta=60, vector_replicates=5, info_samples=2000,
                           replication_samples=2000, pl_reps=60, opt_seeds=8, opt_iters=120)
    out = a.out_dir; out.mkdir(parents=True, exist_ok=True)
    fig = out / "figures"; fig.mkdir(exist_ok=True)
    (out / "config.json").write_text(json.dumps(asdict(cfg), indent=2, default=str))
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60); pd.set_option("display.float_format", "{:.4g}".format)

    tv = theory_validation(cfg)
    tv["common_landscape"] = [AN.common_landscape_check(n, 20_000, cfg.seed) for n in cfg.n_values]
    (out / "theory_validation.json").write_text(json.dumps(tv, indent=2, default=float))
    print("== theory validation ==")
    print(json.dumps({k: tv[k] for k in ("identities_max_err", "difference_distribution_max_err_vs_bruteforce", "integer_M_monotonicity",
                                         "swap_normal_cc_inversion_handover")}, indent=1, default=float))
    for key in ("exact_enumeration", "snr_deep_limit", "deep_limit_zero_probability", "loschmidt_conditional_sign", "swap_normal_approximation", "common_landscape"):
        print(f"-- {key}\n", pd.DataFrame(tv[key]).to_string(index=False))

    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futs = [pool.submit(AN.required_shots_for_n, n, cfg.n_samples, cfg.seed) for n in cfg.n_values]
        res = []
        for n, f in zip(cfg.n_values, futs):
            res.append(f.result()); print(f"n={n} required shots done", flush=True)
    summary = pd.DataFrame([r for x in res for r in x["rows"]])
    paired_req = pd.DataFrame([x["paired"] for x in res])
    samples = pd.concat([x["samples"] for x in res], ignore_index=True)
    summary.to_csv(out / "scaling_summary.csv", index=False)
    samples.to_csv(out / "paired_required_shots_subsample.csv.gz", index=False)
    fits = fit_table(summary)
    (out / "scaling_fits.json").write_text(json.dumps({"fits": fits, "note": "median log10 M = a + b n; slopes not forced"}, indent=2, default=float))
    cols = ["n", "scheme", "log10_abs_g_median"] + [f"{t}_log10M_median" for t, _, _ in AN.TARGETS]
    print("== required shots (median log10 M) ==\n", summary[cols].to_string(index=False))
    print("== methods ==\n", summary[["n", "scheme"] + [c for c in summary.columns if "_frac_" in c and not c.endswith("closed_form")]].to_string(index=False))
    print("== scaling fits ==")
    for k, f in fits.items():
        print(f"  {k:22s} slope={f['slope']:.4f} ref={f['reference_slope']} R2={f['r2']:.5f} maxres={f['max_abs_residual']:.3f} slope(n>=8)={f.get('slope_n_ge_8', float('nan')):.4f}")

    pf = AN.paired_fixed_shots(cfg.paired_n, cfg.paired_shots, cfg.paired_samples, cfg.seed)
    paired = pf.merge(paired_req, on="n", how="left", suffixes=("", "_req"))
    paired.to_csv(out / "paired_estimator_comparison.csv", index=False)
    print("== paired fixed-M ==\n", pf[["n", "shots", "loschmidt_median_p_zero", "swap_median_p_zero", "loschmidt_median_p_correct", "swap_median_p_correct",
                                        "loschmidt_median_p_correct_given_nonzero", "swap_median_p_correct_given_nonzero", "paired_median_log10_snr_swap_over_le",
                                        "swap_frac_float_tie"]].to_string(index=False))
    print("== paired required shots: median log10(M_swap / M_le) ==\n",
          paired_req[["n"] + [f"{t}_log10_swap_over_le_median" for t, _, _ in AN.TARGETS] + [f"{t}_frac_swap_needs_more" for t, _, _ in AN.TARGETS]].to_string(index=False))

    vr = AN.vector_reliability(cfg.vector_n, cfg.vector_shots, cfg.vector_theta, cfg.vector_replicates, cfg.seed)
    vr.to_csv(out / "vector_reliability.csv", index=False)
    print("== vector reliability ==\n", vr[["n", "shots", "scheme", "p_vector_zero", "median_cos", "median_cos_given_nonzero", "p_dot_gt_0",
                                            "median_log10_norm_ratio", "mean_frac_components_zero", "mean_frac_component_signs_correct"]].to_string(index=False))

    info = AN.information_distance_table(cfg.n_values, cfg.info_samples, cfg.seed)
    info.to_csv(out / "information_distance.csv", index=False)
    print("== information distances ==\n", info[["n", "scheme", "median_log10_tv", "median_log10_hellinger2", "median_log10_kl", "median_log10_bhattacharyya"]].to_string(index=False))

    rep = AN.prior_work_replication(cfg.n_values, cfg.replication_shots, cfg.replication_samples, cfg.seed)
    rep.to_csv(out / "prior_work_replication.csv", index=False)
    print("== prior-work replication (fidelity level) ==\n", rep.to_string(index=False))

    pl = pennylane_validation(cfg)
    pl.to_csv(out / "pennylane_validation.csv", index=False)
    print("== PennyLane ==\n", pl[["n", "label", "shots", "scheme", "fhat_plus_z", "fhat_plus_var_ratio", "grad_z_pl_vs_exact", "grad_z_pl_vs_binomial",
                                   "grad_var_ratio_pl", "p_zero_pl", "p_zero_exact", "p_correct_pl", "p_correct_exact", "p_zero_in_ci", "p_correct_in_ci"]].to_string(index=False))

    runs, curves = AN.optimization_diagnostic(cfg.opt_n, list(cfg.opt_variants), cfg.opt_seeds, cfg.opt_iters, cfg.opt_eta, cfg.seed)
    runs.to_csv(out / "optimization_diagnostic.csv", index=False)
    curves.to_csv(out / "optimization_curves.csv", index=False)
    osum = AN.summarize_optimization(runs)
    osum.to_csv(out / "optimization_summary.csv", index=False)
    print("== optimization diagnostic ==\n", osum.drop(columns=["scheme"]).to_string(index=False))

    figs = [FIG.fig_same_landscape(fig / "same_landscape_two_estimators.png"),
            FIG.fig_zero_probability(pf, fig / "zero_probability.png"),
            FIG.fig_directional(pf, fig / "directional_correctness.png"),
            FIG.fig_required(summary, ("snr1", "snr2"), fig / "required_shots_snr.png", "component SNR ≥ ρ"),
            FIG.fig_required(summary, ("dir0.75", "dir0.9", "nz0.9"), fig / "required_shots_direction.png", "sign reliability / non-zero estimate"),
            FIG.fig_scaling(summary, fits, fig / "shot_scaling_comparison.png"),
            FIG.fig_vector(vr, fig / "vector_alignment.png"),
            FIG.fig_trajectories(curves, fig / "trajectory_comparison.png"),
            FIG.fig_information(info, fig / "information_distance.png")]
    for f in figs:
        print(f"figure: {f} ({f.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
