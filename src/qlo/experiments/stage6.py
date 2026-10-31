"""Stage 6 driver: do the projector and parity barren plateaus fail the same way at finite shots?

    python -m qlo.experiments.stage6           # everything -> results/stage6/
    python -m qlo.experiments.stage6 --fast    # reduced sample counts (smoke run)

No optimizer is implemented. The Stage 3-5 projector code is reused unmodified.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import quad

from qlo.stage5.theory import a_k, f_plus_minus
from qlo.stage5.theory import s_k as proj_s_k
from qlo.stage5.theory import shots_for_snr as proj_shots_for_snr
from qlo.stage5.theory import snr_squared as proj_snr_squared
from qlo.stage6 import figures as FIG
from qlo.stage6.analysis import (
    BENCH_ID,
    PAIRS,
    failure_fractions,
    information_distance_table,
    information_distances,
    matched_signal_table,
    scaling_fit,
    vector_reliability,
    wilson_ci,
)
from qlo.stage6.directional import direction_probabilities, normal_approximation
from qlo.stage6.exact_distribution import (
    difference_probabilities,
    difference_probabilities_bruteforce,
    p_equal_zero_signal,
    p_equal_zero_signal_asymptotic,
)
from qlo.stage6.finite_shot import estimator_from_counts, shot_variance, shots_for_snr, snr_squared
from qlo.stage6.parity_benchmark import (
    E_LOG_ABS_COS,
    E_LOG_ABS_SIN,
    VAR_LOG_ABS_COS,
    b_k,
    cost,
    exact_gradient,
    exact_gradient_k,
    log_moments,
    mu_z,
    s_k,
    shifted_mu,
    shifted_probabilities,
    theoretical_gradient_variance,
)
from qlo.stage6.scaling import parity_required_shots, projector_required_shots

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "stage6"


@dataclass(frozen=True)
class Stage6Config:
    n_values: tuple[int, ...] = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
    n_samples: int = 100_000
    sample_seed: int = 0
    rho_targets: tuple[float, ...] = (1.0, 2.0)
    q_targets: tuple[float, ...] = (0.75, 0.90)
    failure_n: tuple[int, ...] = (4, 6, 8, 10, 12, 14, 16)
    failure_shots: tuple[int, ...] = (16, 64, 256, 1024, 4096, 16384)
    failure_samples: int = 20_000
    matched_n: tuple[int, ...] = (4, 6, 8, 10, 12, 14, 16)
    matched_samples: int = 20_000
    matched_shots: tuple[int, ...] = (64, 1024, 16384)
    info_n: tuple[int, ...] = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
    info_samples: int = 20_000
    vector_n: tuple[int, ...] = (4, 6, 8, 10, 12)
    vector_shots: tuple[int, ...] = (64, 1024, 16384)
    vector_theta: int = 300
    vector_replicates: int = 20
    mc_n: tuple[int, ...] = (4, 6, 8, 10, 12)
    mc_replicates: int = 20_000
    pl_n: tuple[int, ...] = (3, 4, 6)
    pl_shots: tuple[int, ...] = (16, 64, 256)
    pl_reps: int = 400
    retro_n: tuple[int, ...] = (6, 10)
    retro_shots: tuple[int, ...] = (64, 1024)
    retro_seeds: int = 20
    retro_iters: int = 300
    retro_eta: float = 0.3


# ------------------------------------------------------------------------------------------
def theory_validation(cfg: Stage6Config) -> dict:
    """Tasks 1, 2, 3, 4, 5, 8, 9: identities, structural-zero audit, asymptotics."""
    rng = np.random.default_rng(6)
    ident = {k: 0.0 for k in ("gradient_vs_finite_difference", "gradient_vs_sB_over_2", "mu_plus", "mu_minus",
                              "p_plus", "p_minus", "variance_formula", "snr_formula", "estimator_identity")}
    for _ in range(200):
        n = int(rng.integers(2, 9)); th = rng.uniform(-np.pi, np.pi, n); k = int(rng.integers(0, n)); M = float(rng.integers(1, 5000))
        s, B = s_k(th, k), b_k(th, k)
        h = 1e-6; e = np.zeros(n); e[k] = 1.0
        ident["gradient_vs_finite_difference"] = max(ident["gradient_vs_finite_difference"], abs(exact_gradient(th)[k] - (cost(th + h * e) - cost(th - h * e)) / (2 * h)))
        ident["gradient_vs_sB_over_2"] = max(ident["gradient_vs_sB_over_2"], abs(exact_gradient(th)[k] - exact_gradient_k(s, B)))
        ep = np.zeros(n); ep[k] = np.pi / 2
        mp, mm = shifted_mu(s, B)
        ident["mu_plus"] = max(ident["mu_plus"], abs(mu_z(th + ep) - mp))
        ident["mu_minus"] = max(ident["mu_minus"], abs(mu_z(th - ep) - mm))
        pp, pm = shifted_probabilities(s, B)
        ident["p_plus"] = max(ident["p_plus"], abs(cost(th + ep) - pp))
        ident["p_minus"] = max(ident["p_minus"], abs(cost(th - ep) - pm))
        v_generic = (pp * (1 - pp) + pm * (1 - pm)) / (4 * M)
        ident["variance_formula"] = max(ident["variance_formula"], abs(v_generic - shot_variance(s * B, M)) / max(v_generic, 1e-300))
        ident["snr_formula"] = max(ident["snr_formula"], abs(snr_squared(s * B, M) - (s * B / 2) ** 2 / v_generic) / max(snr_squared(s * B, M), 1e-300))
        kp, km = int(rng.integers(0, int(M) + 1)), int(rng.integers(0, int(M) + 1))
        ident["estimator_identity"] = max(ident["estimator_identity"], abs(estimator_from_counts(kp, km, M) - 0.5 * ((1 - km / M) - (1 - kp / M))))

    # Task 1: Var_theta[g] = 2^-(n+2)
    var_rows = []
    for n in (2, 3, 4, 6, 8):
        TH = np.random.default_rng(np.random.SeedSequence([6, 1, n])).uniform(-np.pi, np.pi, (400_000, n))
        g = 0.5 * np.sin(TH[:, 0]) * np.prod(np.cos(TH[:, 1:]), axis=1)
        # SE of the sample variance from the EXACT 4th moment: E[g^4] = (1/16) E[sin^4] E[cos^4]^(n-1) = (1/16)(3/8)^n,
        # so kurtosis = (3/2)^n; the Gaussian sqrt(2/N) rule understates the SE exponentially for this heavy-tailed g
        m4, vt = (3.0 / 8.0) ** n / 16.0, theoretical_gradient_variance(n)
        v, se = float(g.var(ddof=1)), float(np.sqrt((m4 - vt**2) / 400_000))
        var_rows.append({"n": n, "empirical_var": v, "theory_var": theoretical_gradient_variance(n),
                         "ratio": v / theoretical_gradient_variance(n), "z": (v - theoretical_gradient_variance(n)) / se,
                         "kurtosis_exact": m4 / vt**2,
                         "empirical_mean_g": float(g.mean()), "mean_z": float(g.mean() / (g.std(ddof=1) / np.sqrt(g.size)))})

    # Task 2: structural-zero audit
    struct = []
    for n in (2, 3, 4, 6, 8):
        witness_ok = True
        for k in range(n):
            th = np.zeros(n); th[k] = np.pi / 2  # g_k = (1/2) sin(pi/2) prod_{j!=k} cos 0 = 1/2 exactly
            witness_ok &= abs(exact_gradient(th)[k] - 0.5) < 1e-15
        TH = np.random.default_rng(np.random.SeedSequence([6, 2, n])).uniform(-np.pi, np.pi, (2000, n))
        G = np.stack([0.5 * s_k(TH, k) * b_k(TH, k) for k in range(n)], axis=1)
        struct.append({"n": n, "analytic_witness_all_k": bool(witness_ok), "min_over_k_of_max_abs_g": float(np.min(np.max(np.abs(G), axis=0))),
                       "n_exact_zero_entries": int(np.sum(G == 0.0)), "n_entries": int(G.size)})

    # Task 5: zero-signal central-binomial identity and 1/sqrt(pi M)
    zero_sig = []
    for M in (1, 2, 5, 10, 100, 1000, 10_000, 10**6):
        gt, eq, lt = difference_probabilities(0.5, 0.5, M)
        zero_sig.append({"M": M, "p_zero_exact": float(eq), "central_binomial": float(p_equal_zero_signal(M)),
                         "asymptotic_1_over_sqrt_pi_M": float(p_equal_zero_signal_asymptotic(M)),
                         "rel_err_vs_central_binomial": abs(float(eq) / float(p_equal_zero_signal(M)) - 1),
                         "rel_err_vs_asymptotic": abs(float(eq) / float(p_equal_zero_signal_asymptotic(M)) - 1),
                         "p_correct": float(gt), "p_wrong": float(lt), "sum": float(gt + eq + lt)})

    # Task 6: direction becomes uninformative as |g| -> 0 while P_zero stays small (parity)
    vanish = []
    for sB in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 0.0):
        pp, pm = shifted_probabilities(sB, 1.0)
        for M in (1000, 10**6):
            d = direction_probabilities(pp, pm, M)
            vanish.append({"sB": sB, "M": M, "p_correct": float(d["p_correct"]), "p_wrong": float(d["p_wrong"]),
                           "p_zero": float(d["p_zero"]), "sum": float(d["p_correct"] + d["p_wrong"] + d["p_zero"])})

    # Task 8: normal approximation error
    normal = []
    for sB in (0.5, 0.1, 0.03, 0.01):
        for M in (16, 64, 256, 1024, 10_000):
            pp, pm = shifted_probabilities(sB, 1.0)
            d = direction_probabilities(pp, pm, M)
            na_cc = normal_approximation(pp, pm, M, continuity=True)
            na = normal_approximation(pp, pm, M, continuity=False)
            normal.append({"sB": sB, "M": M, "snr": float(na["snr"]), "p_correct_exact": float(d["p_correct"]),
                           "phi_snr": float(na["p_correct_normal"]), "phi_snr_continuity": float(na_cc["p_correct_normal"]),
                           "abs_err_plain": abs(float(na["p_correct_normal"]) - float(d["p_correct"])),
                           "abs_err_continuity": abs(float(na_cc["p_correct_normal"]) - float(d["p_correct"])),
                           "p_zero": float(d["p_zero"])})

    # Task 9: log-moment constants
    e_logcos = quad(lambda t: np.log(abs(np.cos(t))), -np.pi, np.pi, limit=500, points=[-np.pi / 2, np.pi / 2])[0] / (2 * np.pi)
    e_logsin = quad(lambda t: np.log(abs(np.sin(t))), -np.pi, np.pi, limit=500, points=[0.0])[0] / (2 * np.pi)
    v_logcos = quad(lambda t: (np.log(abs(np.cos(t))) + np.log(2)) ** 2, -np.pi, np.pi, limit=500, points=[-np.pi / 2, np.pi / 2])[0] / (2 * np.pi)

    # brute-force check of the difference-of-binomials machinery
    bf = 0.0
    for _ in range(100):
        pa, pb = rng.uniform(0, 1, 2) * rng.choice([1.0, 1e-2]); M = int(rng.integers(1, 60))
        got = difference_probabilities(pa, pb, M)
        ref = difference_probabilities_bruteforce(pa, pb, M)
        bf = max(bf, max(abs(g - r) for g, r in zip(got, ref)))

    # bisection precondition: P_correct(M) non-decreasing in M (checked on a log-spaced M grid)
    mono = {}
    Mgrid = np.unique(np.round(np.logspace(0, 5, 120)))
    for bench in ("parity", "projector"):
        worst = 0.0
        for n in (4, 8, 12):
            th = np.random.default_rng(np.random.SeedSequence([6, 3, n, BENCH_ID[bench]])).uniform(-np.pi, np.pi, (40, n))
            pp, pn, _ = PAIRS[bench](th, 0)
            pc = direction_probabilities(pp[:, None], pn[:, None], Mgrid[None, :])["p_correct"]
            worst = max(worst, float(np.max(np.maximum(pc[:, :-1] - pc[:, 1:], 0.0))))
        mono[bench] = worst

    return {"identities_max_abs_or_rel_err": ident, "p_correct_max_decrease_over_M_grid": mono, "gradient_variance_check": var_rows, "structural_zero_audit": struct,
            "zero_signal_identity": zero_sig, "vanishing_signal_direction": vanish, "normal_approximation": normal,
            "E_log_abs_cos_quadrature": e_logcos, "E_log_abs_cos_theory": E_LOG_ABS_COS,
            "E_log_abs_sin_quadrature": e_logsin, "E_log_abs_sin_theory": E_LOG_ABS_SIN,
            "Var_log_abs_cos_quadrature": v_logcos, "Var_log_abs_cos_theory": VAR_LOG_ABS_COS,
            "log_moments_n8": log_moments(8), "difference_probabilities_max_err_vs_bruteforce": bf,
            "note": "Typical |g| ~ 2^-(n+1) (geometric) while RMS |g| = 2^-(n/2+1); the gap is exponential, so "
                    "median-based and variance-based statements about this benchmark are not interchangeable."}


# ------------------------------------------------------------------------------------------
def representative_thetas(n: int, bench: str, pool: int = 400) -> list[tuple[str, np.ndarray]]:
    """Predetermined: from a seeded pool, the theta whose |g_true| is nearest the pool's 25/50/75th percentile."""
    rng = np.random.default_rng(np.random.SeedSequence([6, 600, n, 1 if bench == "parity" else 2]))
    th = rng.uniform(-np.pi, np.pi, (pool, n))
    _, _, g = PAIRS[bench](th, 0)
    lg = np.log(np.abs(g))
    out = []
    for lab, p in (("lower-quartile |g|", 25), ("median |g|", 50), ("upper-quartile |g|", 75)):
        out.append((lab, th[int(np.argmin(np.abs(lg - np.percentile(lg, p))))]))
    return out


def monte_carlo_validation(cfg: Stage6Config) -> pd.DataFrame:
    rows = []
    for bench in ("parity", "projector"):
        for n in cfg.mc_n:
            for li, (lab, th) in enumerate(representative_thetas(n, bench)):
                pp, pn, g = (float(x) for x in PAIRS[bench](th, 0))
                snr_ref = abs(pp - pn) / np.sqrt((pp * (1 - pp) + pn * (1 - pn)))  # per-shot; times sqrt(M) below
                for M in (16, 256, 4096):
                    rng = np.random.default_rng(np.random.SeedSequence([6, 700, n, li, M, 1 if bench == "parity" else 2]))
                    kp = rng.binomial(M, pp, cfg.mc_replicates)
                    km = rng.binomial(M, pn, cfg.mc_replicates)
                    ghat = (kp - km) / (2.0 * M)
                    d = direction_probabilities(pp, pn, float(M))
                    sgn = np.sign(g)
                    n_zero = int(np.sum(ghat == 0))
                    n_corr = int(np.sum(np.sign(ghat) == sgn)) if sgn != 0 else 0
                    n_wrong = int(np.sum((np.sign(ghat) == -sgn) & (ghat != 0))) if sgn != 0 else 0
                    lo_z, hi_z = wilson_ci(n_zero, cfg.mc_replicates)
                    lo_c, hi_c = wilson_ci(n_corr, cfg.mc_replicates)
                    var_analytic = (pp * (1 - pp) + pn * (1 - pn)) / (4.0 * M)
                    rows.append({"benchmark": bench, "n": n, "label": lab, "log10_abs_g": float(np.log10(abs(g))), "shots": M,
                                 "replicates": cfg.mc_replicates, "p_pos": pp, "p_neg": pn, "g_exact": g,
                                 "p_zero_empirical": n_zero / cfg.mc_replicates, "p_zero_exact": float(d["p_zero"]),
                                 "p_zero_ci_low": lo_z, "p_zero_ci_high": hi_z, "p_zero_in_ci": bool(lo_z <= float(d["p_zero"]) <= hi_z),
                                 "p_correct_empirical": n_corr / cfg.mc_replicates, "p_correct_exact": float(d["p_correct"]),
                                 "p_correct_ci_low": lo_c, "p_correct_ci_high": hi_c, "p_correct_in_ci": bool(lo_c <= float(d["p_correct"]) <= hi_c),
                                 "p_wrong_empirical": n_wrong / cfg.mc_replicates, "p_wrong_exact": float(d["p_wrong"]),
                                 "mean_empirical": float(ghat.mean()), "z_mean": float((ghat.mean() - g) / (ghat.std(ddof=1) / np.sqrt(ghat.size))) if ghat.std(ddof=1) > 0 else 0.0,
                                 "var_empirical": float(ghat.var(ddof=1)), "var_analytic": float(var_analytic),
                                 "var_ratio": float(ghat.var(ddof=1) / var_analytic) if var_analytic > 0 else float("nan"),
                                 "snr_analytic": float(snr_ref * np.sqrt(M)),
                                 # with < 30 expected nonzero draws the sample variance / normal z of the mean are not
                                 # meaningful (the estimator is almost always exactly 0); judge those cells by counts only
                                 "expected_nonzero_draws": float(cfg.mc_replicates * (1 - float(d["p_zero"]))),
                                 "moment_check_meaningful": bool(cfg.mc_replicates * (1 - float(d["p_zero"])) >= 30)})
    return pd.DataFrame(rows)


def pennylane_validation(cfg: Stage6Config) -> pd.DataFrame:
    import pennylane as qml

    rows = []
    for n in cfg.pl_n:
        for li, (lab, th) in enumerate(representative_thetas(n, "parity")):
            s, B = float(s_k(th, 0)), float(b_k(th, 0))
            pp, pm = (float(x) for x in shifted_probabilities(s, B))
            g = 0.5 * s * B
            for M in cfg.pl_shots:
                dev = qml.device("default.qubit", wires=n, seed=np.random.default_rng(np.random.SeedSequence([6, 800, n, li, M])))
                obs = qml.prod(*[qml.PauliZ(j) for j in range(n)])

                @qml.set_shots(shots=M)
                @qml.qnode(dev, diff_method=None)
                def parity_expval(t):
                    for j in range(n):
                        qml.RX(t[j], wires=j)
                    return qml.expval(obs)

                e = np.zeros(n); e[0] = np.pi / 2
                g_pl = np.array([0.5 * ((1 - float(parity_expval(th + e))) / 2 - (1 - float(parity_expval(th - e))) / 2) for _ in range(cfg.pl_reps)])
                rng = np.random.default_rng(np.random.SeedSequence([6, 801, n, li, M]))
                g_bi = (rng.binomial(M, pp, cfg.pl_reps) - rng.binomial(M, pm, cfg.pl_reps)) / (2.0 * M)
                d = direction_probabilities(pp, pm, float(M))
                zpl = int(np.sum(g_pl == 0)); cpl = int(np.sum(np.sign(g_pl) == np.sign(g)))
                lo_z, hi_z = wilson_ci(zpl, cfg.pl_reps); lo_c, hi_c = wilson_ci(cpl, cfg.pl_reps)
                se = np.sqrt(g_pl.var(ddof=1) / cfg.pl_reps + g_bi.var(ddof=1) / cfg.pl_reps)
                var_analytic = float(shot_variance(s * B, M))
                rows.append({"n": n, "label": lab, "shots": M, "reps": cfg.pl_reps, "g_exact": g, "p_plus": pp, "p_minus": pm,
                             "mean_pennylane": float(g_pl.mean()), "mean_binomial": float(g_bi.mean()),
                             "z_mean_pl_vs_binomial": float((g_pl.mean() - g_bi.mean()) / se) if se > 0 else 0.0,
                             "z_mean_pl_vs_exact": float((g_pl.mean() - g) / (g_pl.std(ddof=1) / np.sqrt(cfg.pl_reps))) if g_pl.std(ddof=1) > 0 else 0.0,
                             "var_pennylane": float(g_pl.var(ddof=1)), "var_binomial": float(g_bi.var(ddof=1)), "var_analytic": var_analytic,
                             "var_ratio_pl_over_analytic": float(g_pl.var(ddof=1) / var_analytic) if var_analytic > 0 else float("nan"),
                             "p_zero_pennylane": zpl / cfg.pl_reps, "p_zero_binomial": float(np.mean(g_bi == 0)), "p_zero_exact": float(d["p_zero"]),
                             "p_zero_in_pl_ci": bool(lo_z <= float(d["p_zero"]) <= hi_z),
                             "p_correct_pennylane": cpl / cfg.pl_reps, "p_correct_exact": float(d["p_correct"]),
                             "p_correct_in_pl_ci": bool(lo_c <= float(d["p_correct"]) <= hi_c),
                             "support_lattice_ok": bool(np.allclose(g_pl * 2 * M, np.round(g_pl * 2 * M)))})
    return pd.DataFrame(rows)


def optimization_retrodiction(cfg: Stage6Config) -> pd.DataFrame:
    """Task 17 - small diagnostic only (NOT an optimizer study): identical fixed-eta GD update on both
    benchmarks, predetermined seeds, no tuning. Records how often the step is exactly zero versus
    non-zero but poorly aligned with the exact gradient. ``shots = 0`` rows are the EXACT-gradient
    control (same eta, same start points): it separates landscape effects (parity has 2^(n-1) global
    minima, theta_j in {0, pi} with an even number of pi's; the projector has one) from measurement effects."""
    rows = []
    for bench in ("parity", "projector"):
        fn = PAIRS[bench]
        for n in cfg.retro_n:
            for M in (0, *cfg.retro_shots):
                for seed in range(cfg.retro_seeds):
                    # start point depends on (n, seed, benchmark) only, so every M (and the exact control) starts from
                    # the SAME theta_0 and comparisons are paired; the shot-noise stream additionally depends on M
                    th = np.random.default_rng(np.random.SeedSequence([6, 900, n, seed, BENCH_ID[bench]])).uniform(-np.pi, np.pi, n)
                    rng = np.random.default_rng(np.random.SeedSequence([6, 901, n, M, seed, BENCH_ID[bench]]))
                    n_zero_steps = n_neg_dot = n_pos_dot = 0
                    cos_sum, cos_count = 0.0, 0
                    c0 = float(cost(th)) if bench == "parity" else float(1 - np.prod(np.cos(th / 2) ** 2))
                    for _ in range(cfg.retro_iters):
                        pp = np.empty(n); pn = np.empty(n); G = np.empty(n)
                        for k in range(n):
                            pp[k], pn[k], G[k] = (float(x) for x in fn(th, k))  # 1-D theta -> 0-d outputs
                        ghat = G.copy() if M == 0 else (rng.binomial(M, pp) - rng.binomial(M, pn)) / (2.0 * M)
                        hn, gn = np.linalg.norm(ghat), np.linalg.norm(G)
                        if hn == 0:
                            n_zero_steps += 1
                        else:
                            dot = float(ghat @ G)
                            n_pos_dot += dot > 0
                            n_neg_dot += dot <= 0
                            if gn > 0:
                                cos_sum += dot / (hn * gn); cos_count += 1
                        th = (th - cfg.retro_eta * ghat + np.pi) % (2 * np.pi) - np.pi
                    c1 = float(cost(th)) if bench == "parity" else float(1 - np.prod(np.cos(th / 2) ** 2))
                    rows.append({"benchmark": bench, "n": n, "shots": M, "seed": seed, "iters": cfg.retro_iters, "eta": cfg.retro_eta,
                                 "frac_zero_steps": n_zero_steps / cfg.retro_iters,
                                 "frac_nonzero_descent": n_pos_dot / cfg.retro_iters,
                                 "frac_nonzero_ascent_or_orthogonal": n_neg_dot / cfg.retro_iters,
                                 "mean_cos_nonzero": cos_sum / cos_count if cos_count else float("nan"),
                                 "cost_start": c0, "cost_end": c1, "cost_change": c1 - c0})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------
def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    p.add_argument("--fast", action="store_true")
    p.add_argument("--workers", type=int, default=5, help="processes for the required-shot solves (results do not depend on it)")
    a = p.parse_args(argv)
    cfg = (Stage6Config(n_samples=5000, failure_samples=2000, matched_samples=2000, info_samples=2000,
                        vector_theta=60, vector_replicates=5, mc_replicates=3000, pl_reps=100,
                        retro_seeds=4, retro_iters=60) if a.fast else Stage6Config())
    out = a.out_dir; out.mkdir(parents=True, exist_ok=True)
    fig = out / "figures"; fig.mkdir(exist_ok=True)
    (out / "config.json").write_text(json.dumps(asdict(cfg), indent=2), encoding="utf-8")
    pd.set_option("display.width", 260); pd.set_option("display.max_columns", 80); pd.set_option("display.float_format", "{:.4g}".format)

    tv = theory_validation(cfg)
    (out / "parity_theory_validation.json").write_text(json.dumps(tv, indent=2, default=float), encoding="utf-8")
    print("== parity theory validation ==")
    print(json.dumps({k: v for k, v in tv.items() if not isinstance(v, list)}, indent=1, default=float))
    print(pd.DataFrame(tv["gradient_variance_check"]).to_string(index=False))
    print(pd.DataFrame(tv["structural_zero_audit"]).to_string(index=False))
    print(pd.DataFrame(tv["zero_signal_identity"]).to_string(index=False))
    print(pd.DataFrame(tv["vanishing_signal_direction"]).to_string(index=False))
    print(pd.DataFrame(tv["normal_approximation"]).to_string(index=False))

    # per-(benchmark, n) solves are independent and seeded by (n, seed), so running them in worker
    # processes changes wall time only, not results
    jobs = [(fn, n) for n in cfg.n_values for fn in (parity_required_shots, projector_required_shots)]
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futs = [pool.submit(fn, n, cfg.n_samples, cfg.sample_seed, cfg.rho_targets, cfg.q_targets) for fn, n in jobs]
        rows = []
        for (fn, n), f in zip(jobs, futs):
            rows.append(f.result())
            print(f"n={n} {rows[-1]['benchmark']} scaling done", flush=True)
    summary = pd.DataFrame(rows)
    cols = ["n", "benchmark", "log10_abs_g_median", "snr1_log10M_median", "snr2_log10M_median", "dir0.75_log10M_median", "dir0.9_log10M_median"]
    print("== required shots (median log10 M) ==\n", summary[[c for c in cols if c in summary]].to_string(index=False))
    summary[summary.benchmark == "parity"].to_csv(out / "parity_scaling_summary.csv", index=False)
    summary.to_csv(out / "projector_parity_comparison.csv", index=False)

    fits = {}
    for bench in ("parity", "projector"):
        s = summary[summary.benchmark == bench].sort_values("n")
        for tag in ("snr1", "snr2", "dir0.75", "dir0.9"):
            col = f"{tag}_log10M_median"
            d = s.dropna(subset=[col]) if col in s else s.iloc[0:0]
            if len(d) >= 3:
                fits[f"{bench}_{tag}"] = scaling_fit(d.n, d[col], f"{bench}_{tag}")
    (out / "scaling_fits.json").write_text(json.dumps({"fits": fits, "note": "median log10 M = a + b n; reference slopes log10 4 = 0.602, log10 2 = 0.301"}, indent=2, default=float), encoding="utf-8")
    print("== scaling fits ==")
    for k, f in fits.items():
        print(f"  {k:20s} slope={f['slope']:.4f} R2={f['r2']:.5f} closer_to={f['closer_to']} (n_points={f['n_points']})")

    ff = failure_fractions(cfg.failure_n, cfg.failure_shots, cfg.failure_samples, cfg.sample_seed)
    ff.to_csv(out / "failure_fraction.csv", index=False)
    print("== failure fractions: frac P_zero >= 0.9 ==\n", ff.pivot_table(index=["benchmark", "n"], columns="shots", values="frac_p_zero_ge").to_string())
    print("== failure fractions: frac P_correct <= 0.60 ==\n", ff.pivot_table(index=["benchmark", "n"], columns="shots", values="frac_p_correct_le").to_string())

    ms = matched_signal_table(cfg.matched_n, cfg.matched_samples, cfg.matched_shots, cfg.sample_seed)
    ms.to_csv(out / "matched_signal_analysis.csv", index=False)
    print("== matched-signal analysis (M = %d) ==" % cfg.matched_shots[len(cfg.matched_shots) // 2])
    M0 = cfg.matched_shots[len(cfg.matched_shots) // 2]
    print(ms[ms.shots == M0].pivot_table(index="log10_abs_g_mid", columns="benchmark", values=["mean_p_zero", "mean_p_correct", "mean_p_pos"]).to_string())

    info = information_distance_table(cfg.info_n, cfg.info_samples, cfg.sample_seed)
    info.to_csv(out / "information_distance.csv", index=False)
    print("== information distances ==\n", info[["benchmark", "n", "median_abs_g", "median_tv", "median_hellinger2", "median_chi2_mid", "median_shots_1_over_hellinger2", "median_shots_1_over_tv2"]].to_string(index=False))

    vr = vector_reliability(cfg.vector_n, cfg.vector_shots, cfg.vector_theta, cfg.vector_replicates, cfg.sample_seed)
    vr.to_csv(out / "vector_reliability.csv", index=False)
    print("== vector reliability ==\n", vr[["benchmark", "n", "shots", "p_vector_zero", "median_cos", "p_dot_gt_0", "median_cos_given_nonzero", "p_dot_gt_0_given_nonzero"]].to_string(index=False))

    mc = monte_carlo_validation(cfg)
    mc.to_csv(out / "direction_probability_validation.csv", index=False)
    print("== Monte Carlo validation ==")
    print(f"  cells={len(mc)} p_zero in CI: {mc.p_zero_in_ci.sum()}/{len(mc)}; p_correct in CI: {mc.p_correct_in_ci.sum()}/{len(mc)}; "
          f"moment-meaningful cells={int(mc.moment_check_meaningful.sum())}: "
          f"max|z_mean|={mc[mc.moment_check_meaningful].z_mean.abs().max():.2f}, "
          f"var ratio [{mc[mc.moment_check_meaningful].var_ratio.min():.3f},{mc[mc.moment_check_meaningful].var_ratio.max():.3f}]")

    pl = pennylane_validation(cfg)
    pl.to_csv(out / "pennylane_validation.csv", index=False)
    print("== PennyLane validation ==\n", pl[["n", "label", "shots", "mean_pennylane", "mean_binomial", "z_mean_pl_vs_binomial", "var_ratio_pl_over_analytic", "p_zero_pennylane", "p_zero_exact", "p_correct_pennylane", "p_correct_exact", "p_zero_in_pl_ci", "p_correct_in_pl_ci"]].to_string(index=False))

    retro = optimization_retrodiction(cfg)
    retro.to_csv(out / "optimization_retrodiction.csv", index=False)
    print("== optimization retrodiction (diagnostic) ==\n",
          retro.groupby(["benchmark", "n", "shots"]).agg(frac_zero=("frac_zero_steps", "mean"), frac_descent=("frac_nonzero_descent", "mean"),
                                                          mean_cos=("mean_cos_nonzero", "mean"), cost_change=("cost_change", "mean")).to_string())

    figs = [FIG.fig_two_failure_modes(ff, fig / "two_failure_modes.png", 1024),
            FIG.fig_zero_probability_comparison(ff, fig / "zero_probability_comparison.png"),
            FIG.fig_directional_correctness(ff, fig / "directional_correctness.png"),
            FIG.fig_shots_for_direction(summary, fig / "shots_for_direction_vs_n.png", fits),
            FIG.fig_snr_shot_scaling(summary, fig / "snr_shot_scaling.png", fits),
            FIG.fig_matched_gradient(ms, fig / "matched_gradient_distribution.png"),
            FIG.fig_vector_alignment(vr, fig / "vector_alignment.png"),
            FIG.fig_mechanism_map(ff, fig / "mechanism_map.png")]
    for f in figs:
        print(f"figure: {f} ({f.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
