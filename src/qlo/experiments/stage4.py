"""Stage 4 driver: does finite-shot stochasticity help escape the verified global barren plateau?

Sub-commands (all outputs under ``results/stage4/``):

    crosscheck   PennyLane finite-shot projector parameter-shift vs the Binomial simulator
    analyze      recompute evaluation_summary.csv / paired_comparisons.json from saved evaluation_runs.csv
    snr          initial signal-to-noise characterization over Stage-3-distributed theta
    tune         hyperparameter screen on TUNING start seeds 0-39 (n = 6, 8, 10)
    evaluate     held-out evaluation on start seeds 1000-1099 (n = 6, 8, 10, 12) with frozen hyperparameters
    figures      regenerate figures from saved CSVs
    all          crosscheck -> snr -> tune -> evaluate -> figures

Falsification-first: the primary outcome is whether finite-shot SGD (B) beats exact GD (A)
and whether it is distinguishable from covariance-matched Gaussian noise (C). See docs/stages/STAGE4.md.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from qlo.stage4.analysis import paired_bootstrap, per_seed_mean, summarize_group
from qlo.stage4.landscape import cos2_half, exact_gradient, fidelity, shifted_fidelities
from qlo.stage4.methods import METHODS, make_method
from qlo.stage4.seeds import EVALUATION_START_SEEDS, REPRESENTATIVE_START_SEEDS, TUNING_START_SEEDS, initial_theta, noise_seed
from qlo.stage4.shots import BinomialProjectorShots, conditional_shot_variance
from qlo.stage4.trajectory import run_trajectory

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "stage4"


@dataclass(frozen=True)
class Stage4Config:
    n_iters: int = 2000
    # cross-check
    crosscheck_n: tuple[int, ...] = (3, 4, 6)
    crosscheck_shots: tuple[int, ...] = (64, 256, 1024)
    crosscheck_theta_seeds: tuple[int, ...] = (11, 12)
    crosscheck_theta_scales: tuple[float, ...] = (1.0, 0.4)  # 1.0 = Stage-3-distributed (deep plateau); 0.4 = moderate F
    crosscheck_reps: int = 400
    # SNR
    snr_n: tuple[int, ...] = (4, 6, 8, 10, 12)
    snr_shots: tuple[int, ...] = (16, 64, 256, 1024)
    snr_samples: int = 5000
    snr_eta_ref: float = 0.1
    # tuning grids (fixed by protocol)
    tune_n: tuple[int, ...] = (6, 8, 10)
    gd_etas: tuple[float, ...] = (0.01, 0.03, 0.1, 0.3, 1.0)
    sgd_etas: tuple[float, ...] = (0.01, 0.03, 0.1, 0.3)
    sgd_shots: tuple[int, ...] = (16, 64, 256, 1024)
    langevin_etas: tuple[float, ...] = (0.03, 0.1, 0.3)
    langevin_sigmas: tuple[float, ...] = (0.01, 0.03, 0.1, 0.3)
    tune_replicates: int = 1
    # evaluation
    eval_n: tuple[int, ...] = (6, 8, 10, 12)
    eval_replicates: int = 5
    workers: int = max(1, (os.cpu_count() or 2) - 1)


# ------------------------------------------------------------------------------------------
# Task 3: PennyLane vs Binomial cross-check
# ------------------------------------------------------------------------------------------
def _pennylane_shot_cost(n: int, shots: int, seed):
    import pennylane as qml

    dev = qml.device("default.qubit", wires=n, seed=np.random.default_rng(seed))

    @qml.set_shots(shots=shots)
    @qml.qnode(dev, diff_method=None)
    def fid(t):
        for j in range(n):
            qml.RX(t[j], wires=j)
        return qml.expval(qml.Projector(np.zeros(n, dtype=int), wires=range(n)))

    return lambda t: 1.0 - float(fid(t))


def run_crosscheck(cfg: Stage4Config) -> pd.DataFrame:
    rows = []
    def _z(a, b):
        return float(a / b) if b > 0 else float("nan")

    for n in cfg.crosscheck_n:
        for ts, scale in itertools.product(cfg.crosscheck_theta_seeds, cfg.crosscheck_theta_scales):
            theta = scale * initial_theta(ts, n)
            g_exact = exact_gradient(theta)
            for M in cfg.crosscheck_shots:
                pl_cost = _pennylane_shot_cost(n, M, np.random.SeedSequence([4, 300, n, ts, int(scale * 100), M]))
                binom = BinomialProjectorShots(n, M, np.random.SeedSequence([4, 301, n, ts, int(scale * 100), M]))
                for k in (0, n - 1):
                    e_k = np.zeros(n); e_k[k] = np.pi / 2
                    pl = np.array([0.5 * (pl_cost(theta + e_k) - pl_cost(theta - e_k)) for _ in range(cfg.crosscheck_reps)])
                    bi = np.array([0.5 * (binom.cost_estimate(theta + e_k) - binom.cost_estimate(theta - e_k)) for _ in range(cfg.crosscheck_reps)])
                    v_th = conditional_shot_variance(theta, M)[k]
                    se_pl, se_bi = pl.std(ddof=1) / np.sqrt(pl.size), bi.std(ddof=1) / np.sqrt(bi.size)
                    R = cfg.crosscheck_reps
                    vp, vb = pl.var(ddof=1), bi.var(ddof=1)
                    rows.append({"n": n, "theta_seed": ts, "theta_scale": scale, "F_theta": float(fidelity(theta)), "shots": M, "k": k, "reps": R,
                                 "g_exact": g_exact[k], "mean_pennylane": pl.mean(), "mean_binomial": bi.mean(),
                                 "z_mean_pl_vs_binomial": _z(pl.mean() - bi.mean(), np.sqrt(se_pl**2 + se_bi**2)),
                                 "z_mean_pl_vs_exact": _z(pl.mean() - g_exact[k], se_pl), "z_mean_binomial_vs_exact": _z(bi.mean() - g_exact[k], se_bi),
                                 "var_pennylane": vp, "var_binomial": vb, "var_theory": v_th,
                                 "var_ratio_pl_over_binomial": _z(vp, vb), "var_ratio_pl_over_theory": _z(vp, v_th), "var_ratio_binomial_over_theory": _z(vb, v_th),
                                 "approx_sd_of_var_ratio": np.sqrt(4.0 / (R - 1)), "degenerate_all_zero": bool(vp == 0 and vb == 0)})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------
# Task 7: SNR characterization
# ------------------------------------------------------------------------------------------
def _batched_others(Theta: np.ndarray) -> np.ndarray:
    c2 = cos2_half(Theta)
    N, n = c2.shape
    prefix = np.ones((N, n + 1)); suffix = np.ones((N, n + 1))
    prefix[:, 1:] = np.cumprod(c2, axis=1)
    suffix[:, :-1] = np.cumprod(c2[:, ::-1], axis=1)[:, ::-1]
    return prefix[:, :n] * suffix[:, 1:]


def run_snr(cfg: Stage4Config) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for n in cfg.snr_n:
        Theta = np.random.default_rng(np.random.SeedSequence([4, 400, n])).uniform(-np.pi, np.pi, (cfg.snr_samples, n))
        oth = _batched_others(Theta)
        g = 0.5 * np.sin(Theta) * oth
        gnorm = np.linalg.norm(g, axis=1)
        fp = np.clip(np.cos((Theta + np.pi / 2) / 2) ** 2 * oth, 0, 1)
        fm = np.clip(np.cos((Theta - np.pi / 2) / 2) ** 2 * oth, 0, 1)
        var_unit = (fp * (1 - fp) + fm * (1 - fm)) / 4.0  # per-component variance at M=1
        F = np.prod(cos2_half(Theta), axis=1)
        for M in cfg.snr_shots:
            tr = var_unit.sum(axis=1) / M
            nsr = np.sqrt(tr) / gnorm
            q = lambda x, p: float(np.percentile(x, p))
            rows.append({"n": n, "shots": M, "samples": cfg.snr_samples, "eta_ref": cfg.snr_eta_ref,
                         "F_median": q(F, 50), "gnorm_median": q(gnorm, 50), "gnorm_q25": q(gnorm, 25), "gnorm_q75": q(gnorm, 75),
                         "trace_sigma_median": q(tr, 50), "rms_noise_per_component_median": q(np.sqrt(tr / n), 50),
                         "nsr_median": q(nsr, 50), "nsr_q05": q(nsr, 5), "nsr_q25": q(nsr, 25), "nsr_q75": q(nsr, 75), "nsr_q95": q(nsr, 95),
                         "frac_nsr_gt_1": float(np.mean(nsr > 1)),
                         "det_step_norm_median": cfg.snr_eta_ref * q(gnorm, 50), "stoch_step_norm_median": cfg.snr_eta_ref * q(np.sqrt(tr), 50)})
    snr = pd.DataFrame(rows)
    scal = []
    for M in cfg.snr_shots:
        s = snr[snr.shots == M].sort_values("n")
        for col in ("gnorm_median", "trace_sigma_median", "nsr_median"):
            b, a = np.polyfit(s.n, np.log(s[col]), 1)
            scal.append({"shots": M, "quantity": col, "slope_dlog_dn": float(b), "factor_per_qubit": float(np.exp(b)), "intercept": float(a)})
    return snr, pd.DataFrame(scal)


# ------------------------------------------------------------------------------------------
# Trajectory jobs (Tasks 8-14)
# ------------------------------------------------------------------------------------------
def _job(args: tuple) -> dict:
    method, n, hp, start_seed, replicate, config_id, n_iters, record_full = args
    theta0 = initial_theta(start_seed, n)
    seed = None if method == "exact_gd" else noise_seed(method, n, start_seed, replicate, config_id)
    m = make_method(method, n, hp, seed)
    r = run_trajectory(m, theta0, n_iters, offline=True, record_full=record_full)
    row = {k: v for k, v in r.items() if k not in ("theta_final", "resources_final", "trajectory_F", "trajectory_gnorm")}
    row.update({"n": n, "start_seed": start_seed, "replicate": replicate, "config_id": config_id,
                "eta": hp.get("eta"), "shots": hp.get("shots"), "sigma_step": hp.get("sigma_step"),
                "total_circuit_evaluations": r["resources_final"]["circuit_evaluations"],
                "total_shots": r["resources_final"]["shots"], "total_oracle_calls": r["resources_final"]["oracle_gradient_calls"]})
    if record_full:
        row["_traj_F"] = r["trajectory_F"]; row["_traj_g"] = r["trajectory_gnorm"]
    return row


def _run_jobs(jobs: list, workers: int) -> list[dict]:
    if workers <= 1:
        return [_job(j) for j in jobs]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(_job, jobs, chunksize=8))


def _config_id(method: str, hp: dict) -> int:
    key = f"{method}|{hp.get('eta')}|{hp.get('shots')}|{hp.get('sigma_step')}"
    return int(sum((i + 1) * ord(c) for i, c in enumerate(key)) % 1_000_003)  # deterministic, unlike hash()


def run_tuning(cfg: Stage4Config) -> pd.DataFrame:
    jobs = []
    grid = ([("exact_gd", {"eta": e}) for e in cfg.gd_etas]
            + [("shot_sgd", {"eta": e, "shots": M}) for e in cfg.sgd_etas for M in cfg.sgd_shots]
            + [("constant_langevin", {"eta": e, "sigma_step": s}) for e in cfg.langevin_etas for s in cfg.langevin_sigmas])
    for method, hp in grid:
        reps = 1 if method == "exact_gd" else cfg.tune_replicates
        for n, s, r in itertools.product(cfg.tune_n, TUNING_START_SEEDS, range(reps)):
            jobs.append((method, n, hp, s, r, _config_id(method, hp), cfg.n_iters, False))
    rows = _run_jobs(jobs, cfg.workers)
    df = pd.DataFrame(rows)
    df["seed_set"] = "tuning"
    return df


def select_hyperparameters(tuning: pd.DataFrame, cfg: Stage4Config) -> dict:
    """PREDECLARED rule: (1) highest median log10(F_best/F0) over all tuning starts and n;
    (2) tie-break higher success rate F_best >= 0.1; (3) shot_sgd only: fewer total shots; (4) smaller eta."""
    out = {}
    for method in ("exact_gd", "shot_sgd", "constant_langevin"):
        t = tuning[tuning.method == method]
        keys = ["eta"] + (["shots"] if method == "shot_sgd" else []) + (["sigma_step"] if method == "constant_langevin" else [])
        agg = t.groupby(keys).agg(median_gain=("log10_gain_best", "median"), success_rate_F0p1=("F_best", lambda x: float(np.mean(x >= 0.1))),
                                  n_runs=("F_best", "size"), total_shots_per_run=("total_shots", "mean")).reset_index()
        agg["median_gain_r"] = agg.median_gain.round(10)
        sort_cols = ["median_gain_r", "success_rate_F0p1"] + (["total_shots_per_run"] if method == "shot_sgd" else []) + ["eta"]
        asc = [False, False] + ([True] if method == "shot_sgd" else []) + [True]
        agg = agg.sort_values(sort_cols, ascending=asc).reset_index(drop=True)
        best = agg.iloc[0]
        hp = {"eta": float(best.eta)}
        if method == "shot_sgd": hp["shots"] = int(best.shots)
        if method == "constant_langevin": hp["sigma_step"] = float(best.sigma_step)
        out[method] = {"hyperparameters": hp, "median_log10_gain_best": float(best.median_gain),
                       "success_rate_F_best_ge_0.1": float(best.success_rate_F0p1), "n_tuning_runs": int(best.n_runs),
                       "ranking_top5": agg.drop(columns=["median_gain_r"]).head(5).to_dict("records")}
    out["matched_gaussian"] = {"hyperparameters": dict(out["shot_sgd"]["hyperparameters"]), "note": "not tuned: inherits shot_sgd eta and M by protocol"}
    out["noise_only"] = {"hyperparameters": dict(out["shot_sgd"]["hyperparameters"]), "note": "diagnostic: inherits shot_sgd eta and M"}
    out["selection_rule"] = ("1) highest median log10(F_best/F0) pooled over tuning starts 0-39 and n in {6,8,10}; "
                             "2) tie: higher rate of F_best >= 0.1; 3) shot_sgd: fewer total shots; 4) smaller eta. Evaluation seeds never used.")
    return out


def run_evaluation(cfg: Stage4Config, selected: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    hp_gd = selected["exact_gd"]["hyperparameters"]
    hp_sgd = selected["shot_sgd"]["hyperparameters"]
    hp_lg = selected["constant_langevin"]["hyperparameters"]
    hp_gd_matched = {"eta": hp_sgd["eta"]}                              # secondary control: exact GD at shot-SGD's eta
    hp_diffusion = {"eta": 0.0, "sigma_step": hp_lg["sigma_step"]}       # secondary control: pure diffusion, no gradient
    jobs = []
    for n in cfg.eval_n:
        for s in EVALUATION_START_SEEDS:
            rec = s in REPRESENTATIVE_START_SEEDS
            jobs.append(("exact_gd", n, hp_gd, s, 0, _config_id("exact_gd", hp_gd), cfg.n_iters, rec))
            if hp_gd_matched["eta"] != hp_gd["eta"]:
                jobs.append(("exact_gd", n, hp_gd_matched, s, 0, _config_id("exact_gd", hp_gd_matched), cfg.n_iters, False))
            for r in range(cfg.eval_replicates):
                jobs.append(("constant_langevin", n, hp_lg, s, r, _config_id("constant_langevin", hp_lg), cfg.n_iters, rec and r == 0))
                jobs.append(("constant_langevin", n, hp_diffusion, s, r, _config_id("constant_langevin", hp_diffusion), cfg.n_iters, False))
                for M in cfg.sgd_shots:  # selected M is primary; other M feed the shot-budget trade-off
                    hp = {"eta": hp_sgd["eta"], "shots": M}
                    prim = M == hp_sgd["shots"]
                    for method in ("shot_sgd", "matched_gaussian", "noise_only"):
                        jobs.append((method, n, hp, s, r, _config_id(method, hp), cfg.n_iters, rec and r == 0 and prim))
    rows = _run_jobs(jobs, cfg.workers)
    traj_rows = []
    for row in rows:
        if "_traj_F" in row:
            F, G = row.pop("_traj_F"), row.pop("_traj_g")
            for it, (f, g) in enumerate(zip(F, G)):
                traj_rows.append({"n": row["n"], "method": row["method"], "start_seed": row["start_seed"], "shots": row["shots"], "iter": it, "F": f, "gnorm": g})
    df = pd.DataFrame(rows)
    df["seed_set"] = "evaluation"
    is_primary_gd = (df.method == "exact_gd") & (df.eta == hp_gd["eta"])
    is_primary_lg = (df.method == "constant_langevin") & (df.eta == hp_lg["eta"])
    df["primary"] = is_primary_gd | is_primary_lg | (df.method.isin(["shot_sgd", "matched_gaussian", "noise_only"]) & (df.shots == hp_sgd["shots"]))
    df["role"] = np.where(df.primary, "primary",
                          np.where((df.method == "exact_gd"), "control_exact_gd_matched_eta",
                                   np.where((df.method == "constant_langevin"), "control_pure_diffusion", "shot_budget_sweep")))
    return df, pd.DataFrame(traj_rows)


def _hit_prob_per_seed(df: pd.DataFrame, target: float = 0.1) -> pd.Series:
    """Per start seed: fraction of replicates that reached the fixed target (eligible runs only; ineligible -> nan)."""
    d = df[df[f"eligible_F{target}"]]
    return d.groupby("start_seed")[f"hit_F{target}"].apply(lambda x: float(x.notna().mean()))


def analyze_evaluation(runs: pd.DataFrame, selected: dict) -> tuple[pd.DataFrame, dict]:
    prim = runs[runs.primary]
    summ = []
    for (n, method, eta, M, sig), d in runs.groupby(["n", "method", "eta", "shots", "sigma_step"], dropna=False):
        summ.append({"n": n, "method": method, "eta": eta, "shots": M, "sigma_step": sig, "primary": bool(d.primary.iloc[0]),
                     "role": d.role.iloc[0], **summarize_group(d)})
    summary = pd.DataFrame(summ)
    paired = {}
    for n in sorted(prim.n.unique()):
        p = prim[prim.n == n]
        A = per_seed_mean(p[p.method == "exact_gd"]); B = per_seed_mean(p[p.method == "shot_sgd"])
        C = per_seed_mean(p[p.method == "matched_gaussian"]); D = per_seed_mean(p[p.method == "constant_langevin"]); E = per_seed_mean(p[p.method == "noise_only"])
        idx = A.index
        rn = runs[(runs.n == n)]
        A_eta = per_seed_mean(rn[rn.role == "control_exact_gd_matched_eta"]) if (rn.role == "control_exact_gd_matched_eta").any() else A
        Diff = per_seed_mean(rn[rn.role == "control_pure_diffusion"])
        # B vs C also paired at the (seed, replicate) level (same replicate id, independent noise streams)
        Bb = p[p.method == "shot_sgd"].set_index(["start_seed", "replicate"])["log10_gain_best"]
        Cc = p[p.method == "matched_gaussian"].set_index(["start_seed", "replicate"])["log10_gain_best"]
        j = Bb.index.intersection(Cc.index)
        hp_ = {name: _hit_prob_per_seed(p[p.method == name]) for name in ("exact_gd", "shot_sgd", "matched_gaussian", "constant_langevin")}
        hp_["exact_gd_matched_eta"] = _hit_prob_per_seed(rn[rn.role == "control_exact_gd_matched_eta"]) if (rn.role == "control_exact_gd_matched_eta").any() else hp_["exact_gd"]
        hidx = hp_["exact_gd"].index.intersection(hp_["shot_sgd"].index)
        paired[str(n)] = {
            "success_F0.1_B_minus_A": paired_bootstrap(hp_["shot_sgd"].loc[hidx].to_numpy(), hp_["exact_gd"].loc[hidx].to_numpy(), seed=n + 10),
            "success_F0.1_B_minus_A_matched_eta": paired_bootstrap(hp_["shot_sgd"].loc[hidx].to_numpy(), hp_["exact_gd_matched_eta"].loc[hidx].to_numpy(), seed=n + 11),
            "success_F0.1_B_minus_C": paired_bootstrap(hp_["shot_sgd"].loc[hidx].to_numpy(), hp_["matched_gaussian"].loc[hidx].to_numpy(), seed=n + 12),
            "success_F0.1_D_minus_A": paired_bootstrap(hp_["constant_langevin"].loc[hidx].to_numpy(), hp_["exact_gd"].loc[hidx].to_numpy(), seed=n + 13),
            "B_minus_A_log10_gain_best": paired_bootstrap(B.loc[idx].to_numpy(), A.loc[idx].to_numpy(), seed=n),
            "B_minus_C_log10_gain_best_per_seed": paired_bootstrap(B.loc[idx].to_numpy(), C.loc[idx].to_numpy(), seed=n + 1),
            "B_minus_C_log10_gain_best_per_seed_replicate": paired_bootstrap(Bb.loc[j].to_numpy(), Cc.loc[j].to_numpy(), seed=n + 2),
            "B_minus_A_matched_eta_log10_gain_best": paired_bootstrap(B.loc[idx].to_numpy(), A_eta.loc[idx].to_numpy(), seed=n + 6),
            "D_minus_A_log10_gain_best": paired_bootstrap(D.loc[idx].to_numpy(), A.loc[idx].to_numpy(), seed=n + 3),
            "D_minus_pure_diffusion_log10_gain_best": paired_bootstrap(D.loc[idx].to_numpy(), Diff.loc[idx].to_numpy(), seed=n + 7),
            "D_minus_pure_diffusion_log10_gain_final": paired_bootstrap(per_seed_mean(p[p.method == "constant_langevin"], "log10_gain_final").loc[idx].to_numpy(),
                                                                          per_seed_mean(rn[rn.role == "control_pure_diffusion"], "log10_gain_final").loc[idx].to_numpy(), seed=n + 8),
            "E_minus_A_log10_gain_best": paired_bootstrap(E.loc[idx].to_numpy(), A.loc[idx].to_numpy(), seed=n + 4),
            "B_minus_A_log10_gain_final": paired_bootstrap(per_seed_mean(p[p.method == "shot_sgd"], "log10_gain_final").loc[idx].to_numpy(),
                                                            per_seed_mean(p[p.method == "exact_gd"], "log10_gain_final").loc[idx].to_numpy(), seed=n + 5),
        }
    return summary, paired


# ------------------------------------------------------------------------------------------
def make_all_figures(out: Path, cfg: Stage4Config, selected: dict) -> list[Path]:
    from qlo.stage4 import figures as F

    fig = out / "figures"; fig.mkdir(parents=True, exist_ok=True)
    snr = pd.read_csv(out / "snr_summary.csv")
    runs = pd.read_csv(out / "evaluation_runs.csv.gz")
    summary = pd.read_csv(out / "evaluation_summary.csv")
    traj = pd.read_csv(out / "representative_trajectories.csv.gz")
    prim = runs[runs.primary]
    hp = {m: selected[m]["hyperparameters"] for m in ("exact_gd", "shot_sgd", "constant_langevin")}
    return [F.fig_snr(snr, fig / "initial_snr_vs_n.png"),
            F.fig_trajectories(traj, fig / "fidelity_trajectories.png", hp),
            F.fig_gain(prim, fig / "best_fidelity_gain.png"),
            F.fig_target_success(summary[summary.primary], fig / "target_success.png"),
            F.fig_shot_cost(prim, fig / "shot_cost_to_target.png"),
            F.fig_shot_budget(runs, fig / "shot_budget_tradeoff.png", cfg.n_iters)]


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("stage", choices=("crosscheck", "snr", "tune", "evaluate", "analyze", "figures", "all"))
    p.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    p.add_argument("--workers", type=int, default=None)
    p.add_argument("--n-iters", type=int, default=2000)
    a = p.parse_args(argv)
    cfg = Stage4Config(n_iters=a.n_iters, **({"workers": a.workers} if a.workers else {}))
    out = a.out_dir; out.mkdir(parents=True, exist_ok=True)
    (out / "config.json").write_text(json.dumps({**asdict(cfg), "tuning_start_seeds": [TUNING_START_SEEDS[0], TUNING_START_SEEDS[-1]],
                                                  "evaluation_start_seeds": [EVALUATION_START_SEEDS[0], EVALUATION_START_SEEDS[-1]],
                                                  "representative_start_seeds": list(REPRESENTATIVE_START_SEEDS)}, indent=2))
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60); pd.set_option("display.float_format", "{:.4g}".format)
    if a.stage in ("crosscheck", "all"):
        cc = run_crosscheck(cfg); cc.to_csv(out / "crosscheck_pennylane_vs_binomial.csv", index=False)
        print("== cross-check ==\n", cc[["n", "theta_seed", "theta_scale", "F_theta", "shots", "k", "g_exact", "mean_pennylane", "mean_binomial", "z_mean_pl_vs_binomial", "var_ratio_pl_over_binomial", "var_ratio_pl_over_theory", "var_ratio_binomial_over_theory", "degenerate_all_zero"]].to_string(index=False))
    if a.stage in ("snr", "all"):
        snr, scal = run_snr(cfg); snr.to_csv(out / "snr_summary.csv", index=False); scal.to_csv(out / "snr_scaling.csv", index=False)
        print("== SNR ==\n", snr[["n", "shots", "F_median", "gnorm_median", "trace_sigma_median", "nsr_median", "nsr_q25", "nsr_q75", "frac_nsr_gt_1", "det_step_norm_median", "stoch_step_norm_median"]].to_string(index=False))
        print(scal.to_string(index=False))
    if a.stage in ("tune", "all"):
        tuning = run_tuning(cfg); tuning.to_csv(out / "tuning_results.csv", index=False)
        selected = select_hyperparameters(tuning, cfg)
        (out / "selected_hyperparameters.json").write_text(json.dumps(selected, indent=2, default=float))
        print("== selected hyperparameters ==\n", json.dumps({k: v for k, v in selected.items() if k != "selection_rule"}, indent=1, default=float))
    if a.stage in ("evaluate", "all"):
        selected = json.loads((out / "selected_hyperparameters.json").read_text())
        runs, traj = run_evaluation(cfg, selected)
        runs.to_csv(out / "evaluation_runs.csv.gz", index=False); traj.to_csv(out / "representative_trajectories.csv.gz", index=False)
    if a.stage in ("evaluate", "analyze", "all"):
        selected = json.loads((out / "selected_hyperparameters.json").read_text())
        runs = pd.read_csv(out / "evaluation_runs.csv.gz")
        summary, paired = analyze_evaluation(runs, selected)
        summary.to_csv(out / "evaluation_summary.csv", index=False)
        (out / "paired_comparisons.json").write_text(json.dumps(paired, indent=2, default=float))
        cols = ["n", "method", "role", "eta", "shots", "sigma_step", "n_runs", "median_log10_gain_best", "iqr_low_gain_best", "iqr_high_gain_best", "median_log10_gain_final", "p_hit_F0.01", "p_hit_F0.1", "p_hit_F0.5", "p_10xF0", "p_100xF0", "median_iter_to_F0.1"]
        print("== evaluation summary (primary + controls) ==\n", summary[summary.role != "shot_budget_sweep"][cols].to_string(index=False))
        print("== shot-budget sweep (shot_sgd, all M) ==\n", summary[(summary.method == "shot_sgd")][["n", "shots", "median_log10_gain_best", "median_log10_gain_final", "p_hit_F0.1", "median_shots_to_F0.1", "median_shots_to_F0.01"]].to_string(index=False))
        print("== paired comparisons ==\n", json.dumps(paired, indent=1, default=float))
    if a.stage in ("figures", "all"):
        selected = json.loads((out / "selected_hyperparameters.json").read_text())
        for f in make_all_figures(out, cfg, selected):
            print(f"figure: {f} ({f.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
