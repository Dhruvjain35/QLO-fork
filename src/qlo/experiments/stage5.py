"""Stage 5 driver: exact finite-shot gradient dead-zone characterization (no optimizer).

    python -m qlo.experiments.stage5            # everything -> results/stage5/
    python -m qlo.experiments.stage5 --fast     # reduced sample counts for a smoke run
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import quad

from qlo.stage4.seeds import EVALUATION_START_SEEDS, initial_theta
from qlo.stage5 import figures as FIG
from qlo.stage5.analysis import scaling_fit, wilson_ci
from qlo.stage5.global_deadzone import deadzone_fraction, required_shots_distribution, stage4_prediction
from qlo.stage5.local_resolvability import local_required_shots_distribution
from qlo.stage5.sampling import sample_theta
from qlo.stage5.theory import (
    E_LOG_COS2_HALF,
    a_k,
    f_plus_minus,
    local_p_plus_minus,
    local_snr_squared,
    local_variance,
    p_both_zero,
    p_zero_exact,
    p_zero_poisson_limit,
    p_zero_rare_event,
    s_k,
    shot_variance,
    shots_for_nonzero_exact,
    shots_for_nonzero_rare_event,
    snr_squared,
)

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "stage5"
LN10 = np.log(10.0)


@dataclass(frozen=True)
class Stage5Config:
    n_values: tuple[int, ...] = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
    n_samples: int = 100_000
    sample_seed: int = 0
    q_targets: tuple[float, ...] = (0.5, 0.9)
    rho_targets: tuple[float, ...] = (1.0, 2.0)
    q_targets_representative: tuple[float, ...] = (0.5, 0.9, 0.95, 0.99)
    rho_targets_representative: tuple[float, ...] = (0.5, 1.0, 2.0, 5.0)
    deadzone_n: tuple[int, ...] = (4, 6, 8, 10, 12, 14, 16)
    deadzone_shots: tuple[int, ...] = (16, 64, 256, 1024, 4096, 16384)
    deadzone_samples: int = 100_000
    deadzone_full_samples: int = 5_000
    mc_n: tuple[int, ...] = (4, 6, 8, 10, 12)
    mc_replicates: int = 20_000
    pl_n: tuple[int, ...] = (3, 4, 6)
    pl_shots: tuple[int, ...] = (16, 64, 256)
    pl_reps: int = 400
    stage4_shots: tuple[int, ...] = (16, 64, 256, 1024)
    stage4_iters: int = 2000


# ------------------------------------------------------------------------------------------
def theory_validation(cfg: Stage5Config) -> dict:
    e_logc2 = quad(lambda t: np.log(np.cos(t / 2) ** 2), -np.pi, np.pi, limit=200)[0] / (2 * np.pi)
    e_c2 = quad(lambda t: np.cos(t / 2) ** 2, -np.pi, np.pi)[0] / (2 * np.pi)
    v_logc2 = quad(lambda t: (np.log(np.cos(t / 2) ** 2) - e_logc2) ** 2, -np.pi, np.pi, limit=200)[0] / (2 * np.pi)
    rng = np.random.default_rng(5)
    ident = {"max_abs_err_F_plus": 0.0, "max_abs_err_F_minus": 0.0, "max_abs_err_sum_A": 0.0, "max_abs_err_gradient": 0.0,
             "max_abs_err_F2_sum": 0.0, "max_abs_err_variance_simplification": 0.0, "max_abs_err_snr_formula": 0.0,
             "max_abs_err_local_variance": 0.0, "max_abs_err_local_snr": 0.0}
    from qlo.stage4.landscape import exact_gradient, shifted_fidelities

    for _ in range(200):
        n = int(rng.integers(2, 9)); th = rng.uniform(-np.pi, np.pi, n); k = int(rng.integers(0, n)); M = float(rng.integers(1, 5000))
        A, s = a_k(th, k), s_k(th, k)
        fp, fm = shifted_fidelities(th)
        ident["max_abs_err_F_plus"] = max(ident["max_abs_err_F_plus"], abs(fp[k] - A * (1 - s) / 2))
        ident["max_abs_err_F_minus"] = max(ident["max_abs_err_F_minus"], abs(fm[k] - A * (1 + s) / 2))
        ident["max_abs_err_sum_A"] = max(ident["max_abs_err_sum_A"], abs(fp[k] + fm[k] - A))
        ident["max_abs_err_gradient"] = max(ident["max_abs_err_gradient"], abs(exact_gradient(th)[k] - A * s / 2))
        ident["max_abs_err_F2_sum"] = max(ident["max_abs_err_F2_sum"], abs(fp[k] ** 2 + fm[k] ** 2 - A**2 * (1 + s**2) / 2))
        v_old = (fp[k] * (1 - fp[k]) + fm[k] * (1 - fm[k])) / (4 * M)
        ident["max_abs_err_variance_simplification"] = max(ident["max_abs_err_variance_simplification"], abs(v_old - shot_variance(A, s, M)) / v_old)
        ident["max_abs_err_snr_formula"] = max(ident["max_abs_err_snr_formula"], abs((A * s / 2) ** 2 / v_old - snr_squared(A, s, M)) / max((A * s / 2) ** 2 / v_old, 1e-300))
        pp, pm = local_p_plus_minus(s)
        vl = (pp * (1 - pp) + pm * (1 - pm)) / (4 * M * n**2)
        ident["max_abs_err_local_variance"] = max(ident["max_abs_err_local_variance"], abs(vl - local_variance(s, M, n)) / vl)
        ident["max_abs_err_local_snr"] = max(ident["max_abs_err_local_snr"], abs((s / (2 * n)) ** 2 / vl - local_snr_squared(s, M)) / max((s / (2 * n)) ** 2 / vl, 1e-300))
    # Poisson-limit / rare-event accuracy map
    acc = []
    for A in (1.0, 0.3, 0.1, 0.03, 0.01, 1e-3, 1e-4, 1e-6):
        for s in (0.0, 0.5, 0.9, 0.99):
            for x in (0.1, 0.5, 1.0, 2.0, 5.0, 10.0):
                M = max(x / A, 1.0)
                fp, fm = f_plus_minus(A, s)
                ex = float(p_zero_exact(fp, fm, M))
                acc.append({"A": A, "s": s, "MA": x, "M": M, "p_zero_exact": ex, "abs_err_poisson": abs(float(p_zero_poisson_limit(A, s, M)) - ex),
                            "abs_err_rare_event": abs(float(p_zero_rare_event(A, M)) - ex), "gap_bound": ex - float(p_both_zero(fp, fm, M))})
    acc = pd.DataFrame(acc)
    accsum = acc.groupby("A").agg(max_abs_err_poisson=("abs_err_poisson", "max"), max_abs_err_rare_event=("abs_err_rare_event", "max"), max_gap_to_both_zero_bound=("gap_bound", "max")).reset_index()
    return {"E_log_cos2_half_quadrature": e_logc2, "E_log_cos2_half_theory": E_LOG_COS2_HALF, "abs_err": abs(e_logc2 - E_LOG_COS2_HALF),
            "E_cos2_half_quadrature": e_c2, "Var_log_cos2_half_quadrature": v_logc2, "Var_log_cos2_half_theory": float(np.pi**2 / 3),
            "identities_max_abs_err": ident, "approximation_accuracy_by_A": accsum.to_dict("records"),
            "approximation_note": "Poisson limit exp(-MA) I0(MA|cos|) error is O(A); rare-event exp(-MA) additionally ignores equal non-zero counts and is poor when |sin theta_k| is small."}


# ------------------------------------------------------------------------------------------
def representative_thetas(n: int, pool: int = 400) -> list[tuple[str, np.ndarray]]:
    """Predetermined: from a seeded pool, the theta whose log A_0 is nearest the pool's 25/50/75th percentile."""
    th = sample_theta(n, pool, seed=777)
    la = np.log(a_k(th, 0))
    out = []
    for lab, p in (("lower-quartile A", 25), ("typical A", 50), ("upper-quartile A", 75)):
        out.append((lab, th[int(np.argmin(np.abs(la - np.percentile(la, p))))]))
    return out


def monte_carlo_validation(cfg: Stage5Config) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, rep_rows = [], []
    for n in cfg.mc_n:
        for li, (lab, th) in enumerate(representative_thetas(n)):
            A, s = float(a_k(th, 0)), float(s_k(th, 0))
            fp, fm = f_plus_minus(A, s)
            M_star = float(shots_for_nonzero_exact(np.array([fp]), np.array([fm]), 0.5)[0][0])
            Ms = sorted({max(1, int(round(M_star * f))) for f in (1 / 8, 1 / 2, 1, 2, 8)})
            for M in Ms:
                rng = np.random.default_rng(np.random.SeedSequence([5, 300, n, li, M]))
                kp = rng.binomial(M, fp, cfg.mc_replicates); km = rng.binomial(M, fm, cfg.mc_replicates)
                g = (km - kp) / (2.0 * M)
                zero = float(np.mean(g == 0)); lo, hi = wilson_ci(int(np.sum(g == 0)), g.size)
                ex = float(p_zero_exact(fp, fm, float(M)))
                snr_emp = abs(A * s / 2) / g.std(ddof=1) if g.std(ddof=1) > 0 else float("inf")
                rows.append({"n": n, "label": lab, "log10A": np.log10(A), "s": s, "shots": M, "M_star_nonzero0.5": M_star, "replicates": cfg.mc_replicates,
                             "p_zero_empirical": zero, "p_zero_ci_low": lo, "p_zero_ci_high": hi, "p_zero_exact": ex,
                             "exact_in_ci": bool(lo <= ex <= hi), "p_both_zero": float(p_both_zero(fp, fm, M)),
                             "p_zero_rare_event": float(p_zero_rare_event(A, M)), "p_zero_poisson": float(p_zero_poisson_limit(A, s, M)),
                             "mean_g_hat": float(g.mean()), "g_exact": A * s / 2, "z_mean": (g.mean() - A * s / 2) / (g.std(ddof=1) / np.sqrt(g.size)) if g.std(ddof=1) > 0 else 0.0,
                             "var_empirical": float(g.var(ddof=1)), "var_analytic": float(shot_variance(A, s, M)),
                             "snr_empirical": snr_emp, "snr_analytic": float(np.sqrt(snr_squared(A, s, M)))})
            # dense curve for the figure (exact + approximations), and the q-target comparison (Task 3)
            for M in np.unique(np.round(np.logspace(0, np.log10(max(M_star * 64, 100)), 40))):
                rep_rows.append({"n": n, "label": lab, "log10A": np.log10(A), "s": s, "shots": float(M),
                                 "p_zero_exact": float(p_zero_exact(fp, fm, float(M))), "p_both_zero": float(p_both_zero(fp, fm, M)),
                                 "p_zero_rare_event": float(p_zero_rare_event(A, M)), "p_zero_poisson": float(p_zero_poisson_limit(A, s, M))})
    mc = pd.DataFrame(rows)
    return mc, pd.DataFrame(rep_rows)


def representative_targets(cfg: Stage5Config) -> pd.DataFrame:
    rows = []
    for n in cfg.mc_n:
        for lab, th in representative_thetas(n):
            A, s = float(a_k(th, 0)), float(s_k(th, 0))
            fp, fm = f_plus_minus(A, s)
            for q in cfg.q_targets_representative:
                Mx = float(shots_for_nonzero_exact(np.array([fp]), np.array([fm]), q)[0][0])
                Mr = float(shots_for_nonzero_rare_event(A, q))
                rows.append({"n": n, "label": lab, "log10A": np.log10(A), "s": s, "target": f"P_nonzero>={q}", "M_exact": Mx, "M_rare_event_approx": Mr,
                             "ratio_approx_over_exact": Mr / Mx, "abs_log10_err": abs(np.log10(Mr / Mx))})
            for rho in cfg.rho_targets_representative:
                from qlo.stage5.theory import shots_for_snr

                rows.append({"n": n, "label": lab, "log10A": np.log10(A), "s": s, "target": f"SNR>={rho}", "M_exact": float(np.ceil(shots_for_snr(A, s, rho))),
                             "M_rare_event_approx": float("nan"), "ratio_approx_over_exact": float("nan"), "abs_log10_err": float("nan")})
    return pd.DataFrame(rows)


def pennylane_validation(cfg: Stage5Config) -> pd.DataFrame:
    import pennylane as qml

    rows = []
    for n in cfg.pl_n:
        for lab, th in representative_thetas(n):
            A, s = float(a_k(th, 0)), float(s_k(th, 0))
            fp, fm = f_plus_minus(A, s)
            for M in cfg.pl_shots:
                dev = qml.device("default.qubit", wires=n, seed=np.random.default_rng(np.random.SeedSequence([5, 400, n, M])))

                @qml.set_shots(shots=M)
                @qml.qnode(dev, diff_method=None)
                def fid(t):
                    for j in range(n):
                        qml.RX(t[j], wires=j)
                    return qml.expval(qml.Projector(np.zeros(n, dtype=int), wires=range(n)))

                e0 = np.zeros(n); e0[0] = np.pi / 2
                g_pl = np.array([0.5 * ((1 - float(fid(th + e0))) - (1 - float(fid(th - e0)))) for _ in range(cfg.pl_reps)])
                rng = np.random.default_rng(np.random.SeedSequence([5, 401, n, M]))
                g_bi = (rng.binomial(M, fm, cfg.pl_reps) - rng.binomial(M, fp, cfg.pl_reps)) / (2.0 * M)
                zpl, zbi = int(np.sum(g_pl == 0)), int(np.sum(g_bi == 0))
                lo, hi = wilson_ci(zpl, cfg.pl_reps)
                ex = float(p_zero_exact(fp, fm, float(M)))
                se = np.sqrt(g_pl.var(ddof=1) / cfg.pl_reps + g_bi.var(ddof=1) / cfg.pl_reps)
                rows.append({"n": n, "label": lab, "log10A": np.log10(A), "s": s, "shots": M, "reps": cfg.pl_reps,
                             "p_zero_pennylane": zpl / cfg.pl_reps, "p_zero_pl_ci_low": lo, "p_zero_pl_ci_high": hi, "p_zero_binomial": zbi / cfg.pl_reps,
                             "p_zero_exact": ex, "exact_in_pl_ci": bool(lo <= ex <= hi),
                             "mean_pennylane": g_pl.mean(), "mean_binomial": g_bi.mean(), "g_exact": A * s / 2,
                             "z_mean_pl_vs_binomial": (g_pl.mean() - g_bi.mean()) / se if se > 0 else 0.0,
                             "var_pennylane": g_pl.var(ddof=1), "var_binomial": g_bi.var(ddof=1), "var_analytic": float(shot_variance(A, s, M)),
                             "var_ratio_pl_over_analytic": g_pl.var(ddof=1) / shot_variance(A, s, M) if shot_variance(A, s, M) > 0 else float("nan")})
    return pd.DataFrame(rows)


def stage4_connection(cfg: Stage5Config, stage4_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    theta0 = np.stack([initial_theta(sd, 12) for sd in EVALUATION_START_SEEDS])
    pred = stage4_prediction(theta0, cfg.stage4_shots, cfg.stage4_iters)
    emp_rows = []
    runs_path = stage4_dir / "evaluation_runs.csv.gz"
    if runs_path.exists():
        r = pd.read_csv(runs_path)
        b = r[(r.method == "shot_sgd") & (r.n == 12)].copy()
        # "never moved": g_hat = 0 at every iteration => theta unchanged up to the 1e-16 rounding of the angle wrap.
        # Any single non-zero update moves theta by >= eta/(2M) >= 1.5e-4 rad and F by >> 1e-9 in log10, so a 1e-9
        # tolerance separates the two cases unambiguously.
        b["never_moved"] = (b.log10_gain_best.abs() < 1e-9) & (b.log10_gain_final.abs() < 1e-9)
        seed_to_index = {sd: i for i, sd in enumerate(EVALUATION_START_SEEDS)}
        b["theta_index"] = b.start_seed.map(seed_to_index)
        for M in cfg.stage4_shots:
            d = b[b.shots == M]
            never = int(d.never_moved.sum())
            lo, hi = wilson_ci(never, len(d))
            pm = pred[pred.shots == M].set_index("theta_index").p_stuck_all_iters
            # paired at the same theta0: expected count = sum over runs of P_stuck(theta0); variance = sum p(1-p)
            p_run = d.theta_index.map(pm).to_numpy()
            exp_count, var_count = float(p_run.sum()), float(np.sum(p_run * (1 - p_run)))
            per_seed = d.groupby("theta_index").never_moved.sum()
            emp_rows.append({"shots": M, "n_runs": len(d), "empirical_never_moved": never, "empirical_frac_never_moved": never / len(d), "ci_low": lo, "ci_high": hi,
                             "predicted_frac_never_moved": float(pm.mean()), "predicted_count_paired": exp_count, "predicted_count_sd_paired": float(np.sqrt(var_count)),
                             "z_paired": (never - exp_count) / np.sqrt(var_count) if var_count > 0 else float("nan"),
                             "n_seeds_pred_gt_0.5": int((pm > 0.5).sum()), "n_seeds_obs_majority_stuck": int((per_seed >= 3).sum()),
                             "n_seeds_disagree": int(((pm > 0.5) != (per_seed.reindex(pm.index).fillna(0) >= 3)).sum()),
                             "predicted_full_zero_one_iteration": float(pred[pred.shots == M].p_full_zero.mean())})
    emp = pd.DataFrame(emp_rows)
    # distribution of component P_zero over random theta at n=12
    th = sample_theta(12, 20_000, seed=4)
    fp, fm = f_plus_minus(a_k(th, 0), s_k(th, 0))
    dist = pd.concat([pd.DataFrame({"shots": M, "p_zero": p_zero_exact(fp, fm, float(M))}) for M in cfg.stage4_shots], ignore_index=True)
    return pred, emp, dist


# ------------------------------------------------------------------------------------------
def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    p.add_argument("--fast", action="store_true")
    a = p.parse_args(argv)
    cfg = Stage5Config(n_samples=5000, deadzone_samples=5000, deadzone_full_samples=500, mc_replicates=4000, pl_reps=100) if a.fast else Stage5Config()
    out = a.out_dir; out.mkdir(parents=True, exist_ok=True); fig = out / "figures"; fig.mkdir(exist_ok=True)
    (out / "config.json").write_text(json.dumps(asdict(cfg), indent=2), encoding="utf-8")
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60); pd.set_option("display.float_format", "{:.4g}".format)

    tv = theory_validation(cfg)
    (out / "theory_validation.json").write_text(json.dumps(tv, indent=2, default=float), encoding="utf-8")
    print("== theory validation ==\n", json.dumps({k: v for k, v in tv.items() if k != "approximation_accuracy_by_A"}, indent=1, default=float))
    print(pd.DataFrame(tv["approximation_accuracy_by_A"]).to_string(index=False))

    rows = []
    for n in cfg.n_values:
        row, _ = required_shots_distribution(n, cfg.n_samples, cfg.sample_seed, cfg.q_targets, cfg.rho_targets)
        rows.append(row); print(f"n={n} done")
    summ = pd.DataFrame(rows); summ.to_csv(out / "shot_scaling_summary.csv", index=False)
    cols = ["n", "empirical_mean_logA", "theory_mean_logA", "empirical_mean_A", "theory_mean_A", "nonzero0.5_log10M_median", "nonzero0.9_log10M_median", "snr1_log10M_median", "snr2_log10M_median", "nonzero0.9_median_abs_log10_err_rare_event", "nonzero0.9_max_abs_log10_err_poisson"]
    print("== global shot scaling ==\n", summ[cols].to_string(index=False))

    fits = {tag: scaling_fit(summ.n, summ[f"{tag}_log10M_median"], tag) for tag in ("nonzero0.5", "nonzero0.9", "snr1", "snr2")}
    fits_q = {f"{tag}_{stat}": scaling_fit(summ.n, summ[f"{tag}_log10M_{stat}"], f"{tag}_{stat}") for tag in ("nonzero0.9", "snr2") for stat in ("q25", "q75", "q90", "geomean")}
    lrows = [local_required_shots_distribution(n, cfg.n_samples, cfg.sample_seed, cfg.q_targets, cfg.rho_targets) for n in cfg.n_values]
    loc = pd.DataFrame(lrows); loc.to_csv(out / "local_control_summary.csv", index=False)
    lfits = {tag: scaling_fit(loc.n, loc[f"{tag}_log10M_median"], f"local_{tag}") for tag in ("nonzero0.5", "nonzero0.9", "snr1", "snr2")}
    (out / "scaling_fits.json").write_text(json.dumps({"global_median": fits, "global_other_statistics": fits_q, "local_median": lfits,
                                                       "note": "median log10 M = a + b n over n in n_values; reference slopes log10 4 = 0.602 (log-typical A = 4^-(n-1)) and log10 2 = 0.301 (arithmetic-mean A = 2^-(n-1))"}, indent=2, default=float), encoding="utf-8")
    print("== scaling fits (global median) ==")
    for k, f in fits.items(): print(f"  {k:12s} slope={f['slope']:.4f} (log10 4={f['theory_slope_log10_4']:.4f}, log10 2={f['theory_slope_log10_2']:.4f}) R2={f['r2']:.5f} closer_to={f['closer_to']}")
    print("== local control ==\n", loc[["n", "nonzero0.5_log10M_median", "nonzero0.9_log10M_median", "snr1_log10M_median", "snr2_log10M_median", "p_zero_median_M16", "p_zero_median_M1024"]].to_string(index=False))
    for k, f in lfits.items(): print(f"  local {k:12s} slope={f['slope']:+.5f} R2={f['r2']:.3f}")

    dz = pd.DataFrame([r for n in cfg.deadzone_n for r in deadzone_fraction(n, cfg.deadzone_samples, cfg.sample_seed, cfg.deadzone_shots, full_gradient_samples=cfg.deadzone_full_samples)])
    dz.to_csv(out / "deadzone_fraction.csv", index=False)
    print("== dead-zone fraction (component k=0, q=0.9) ==\n", dz.pivot(index="n", columns="shots", values="deadzone_frac_q0.9").to_string())
    print("== full-gradient dead-zone fraction (q=0.9) ==\n", dz.pivot(index="n", columns="shots", values="full_deadzone_frac_q0.9").to_string())

    mc, rep = monte_carlo_validation(cfg); mc.to_csv(out / "monte_carlo_validation.csv", index=False); rep.to_csv(out / "representative_curves.csv", index=False)
    print("== Monte Carlo validation ==\n", mc[["n", "label", "log10A", "s", "shots", "p_zero_empirical", "p_zero_exact", "exact_in_ci", "p_both_zero", "p_zero_rare_event", "p_zero_poisson", "z_mean", "var_empirical", "var_analytic", "snr_empirical", "snr_analytic"]].to_string(index=False))
    rt = representative_targets(cfg); rt.to_csv(out / "representative_targets.csv", index=False)
    print("== rare-event M approximation vs exact (representative theta) ==\n", rt[rt.target.str.startswith("P_nonzero")].groupby(["n", "target"]).agg(ratio_min=("ratio_approx_over_exact", "min"), ratio_max=("ratio_approx_over_exact", "max")).to_string())

    pl = pennylane_validation(cfg); pl.to_csv(out / "pennylane_validation.csv", index=False)
    print("== PennyLane validation ==\n", pl[["n", "label", "log10A", "shots", "p_zero_pennylane", "p_zero_binomial", "p_zero_exact", "exact_in_pl_ci", "z_mean_pl_vs_binomial", "var_pennylane", "var_binomial", "var_analytic"]].to_string(index=False))

    pred, emp, dist = stage4_connection(cfg, out.parent / "stage4")
    pred.to_csv(out / "stage4_prediction.csv", index=False); emp.to_csv(out / "stage4_prediction_summary.csv", index=False)
    print("== Stage 4 retrodiction (n=12) ==\n", emp.to_string(index=False))
    print(dist.groupby("shots").p_zero.describe(percentiles=[0.1, 0.5, 0.9]).to_string())

    figs = [FIG.fig_zero_probability_vs_shots(rep[rep.label == "typical A"], fig / "zero_probability_vs_shots.png", mc),
            FIG.fig_shots_vs_n(summ, fig / "shots_for_nonzero_vs_n.png", [("nonzero0.5", "P(ĝ≠0) ≥ 0.5"), ("nonzero0.9", "P(ĝ≠0) ≥ 0.9")], "Global projector: shots for a non-zero estimator vs n (exact integer solve per θ)", fits),
            FIG.fig_shots_vs_n(summ, fig / "shots_for_snr_vs_n.png", [("snr1", "SNR ≥ 1"), ("snr2", "SNR ≥ 2")], "Global projector: shots for component SNR vs n (closed form)", fits),
            FIG.fig_global_vs_local(summ, loc, fig / "global_vs_local_resolution.png"),
            FIG.fig_deadzone_fraction(dz, fig / "deadzone_fraction.png"),
            FIG.fig_stage4_prediction(pred, emp, dist, fig / "stage4_quantization_prediction.png"),
            FIG.fig_a_distribution(summ, fig / "A_distribution.png")]
    for f in figs:
        print(f"figure: {f} ({f.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
