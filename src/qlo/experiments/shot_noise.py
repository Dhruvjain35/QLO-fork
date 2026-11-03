"""Stage 2: finite-shot gradient-noise characterization at a single theta.

Validates the estimator model  g_hat(theta) = g_exact(theta) + xi_shot(theta)
for the finite-shot parameter-shift estimator (``qlo.gradients.finite_shot``)
against the analytic reference (``qlo.gradients.exact``) and the analytic
±1-observable variance formula (``qlo.analysis.shot_theory``), for the GLOBAL
Pauli-Z product cost only.

Parts
-----
A. single-point study: for selected flat indices k and shot counts M, draw
   ``replicates`` independent g_hat_k, summarize xi = g_hat_k - g_exact_k.
B. 1/M scaling: log-log fit of empirical Var(xi) vs M per k.
C. covariance pilot: full-gradient replicates -> p x p empirical Cov(xi).
D. figures.

Outputs (predictably named, under ``--out-dir``, default ``results/stage2``):
    config.json
    shot_noise_raw.csv           one row per (k, M, replicate)
    shot_noise_summary.csv       one row per (k, M)
    shot_noise_scaling.csv       one row per k
    covariance/cov_M{M}.csv      p x p matrices
    covariance_summary.csv       one row per M
    figures/variance_vs_shots.png, scaled_variance.png, bias_vs_shots.png

This characterizes ESTIMATOR NOISE ONLY. It says nothing about barren-plateau
escape, useful exploration, FDT, or QLO.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from qlo.analysis.shot_theory import theoretical_parameter_shift_variance
from qlo.analysis.statistics import fit_loglog_slope, summarize_shot_noise
from qlo.circuits.hardware_efficient import HardwareEfficientAnsatz
from qlo.gradients.exact import gradient_autograd
from qlo.gradients.finite_shot import FiniteShotParameterShift
from qlo.utils.indexing import flat_to_multi
from qlo.utils.seeding import make_rng

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "stage2"
SLOPE_SANITY = (-1.30, -0.70)  # sanity band for ~200 replicates, NOT a proof criterion


@dataclass(frozen=True)
class ShotNoiseConfig:
    n_qubits: int = 3
    depth: int = 2
    entangler: str = "ring"
    cost: str = "global"
    theta_seed: int = 7
    master_seed: int = 2025
    shots: tuple[int, ...] = (64, 128, 256, 512, 1024, 2048)
    replicates: int = 200
    k_indices: tuple[int, ...] | None = None  # None -> (first, middle, last)
    cov_shots: tuple[int, ...] = (128, 512, 2048)
    cov_replicates: int = 100

    def __post_init__(self) -> None:
        if self.cost != "global":
            raise ValueError("Stage 2 quantitative validation is defined for cost='global' only")
        if self.replicates < 2 or self.cov_replicates < 2:
            raise ValueError("replicates must be >= 2")

    def resolved_k(self, p: int) -> tuple[int, ...]:
        if self.k_indices is not None:
            return tuple(int(k) for k in self.k_indices)
        return (0, p // 2, p - 1)


# ----- part A + B ------------------------------------------------------------------
def run_single_point(cfg: ShotNoiseConfig) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
    ansatz = HardwareEfficientAnsatz(cfg.n_qubits, cfg.depth, cfg.entangler)
    theta = ansatz.init_params(make_rng(cfg.theta_seed))
    g_exact = gradient_autograd(ansatz, cfg.cost, theta).ravel()  # offline reference only
    ks = cfg.resolved_k(ansatz.n_params)

    raw_rows, summary_rows = [], []
    for k in ks:
        multi = flat_to_multi(k, ansatz.param_shape)
        for M in cfg.shots:
            # one independent, reproducible stream per (k, M), derived from the master seed
            est = FiniteShotParameterShift(ansatz, cfg.cost, M, master_seed=[cfg.master_seed, k, M])
            g_hat = est.replicate_component(theta, k, cfg.replicates)
            var_th = theoretical_parameter_shift_variance(ansatz, theta, k, M, cfg.cost)
            for r, gh in enumerate(g_hat):
                raw_rows.append({"k": k, "layer": multi[0], "qubit": multi[1], "rot": multi[2], "shots": M,
                                 "replicate": r, "g_hat": gh, "g_exact": g_exact[k], "xi": gh - g_exact[k]})
            summary_rows.append({"k": k, "layer": multi[0], "qubit": multi[1], "rot": multi[2],
                                 **summarize_shot_noise(g_hat, g_exact[k], M, var_th)})
    raw, summary = pd.DataFrame(raw_rows), pd.DataFrame(summary_rows)

    scaling_rows = []
    for k in ks:
        s = summary[summary.k == k].sort_values("shots")
        fit = fit_loglog_slope(s.shots.to_numpy(), s.var_xi_emp.to_numpy())
        mv = s.M_times_var_emp.to_numpy()
        scaling_rows.append({"k": k, **fit,
                             "M_var_min": float(mv.min()), "M_var_max": float(mv.max()),
                             "M_var_mean": float(mv.mean()), "M_var_theory": float(s.M_times_var_theory.iloc[0]),
                             "slope_in_sanity_band": bool(SLOPE_SANITY[0] < fit["slope"] < SLOPE_SANITY[1])})
    return raw, summary, pd.DataFrame(scaling_rows), theta, g_exact


# ----- part C ------------------------------------------------------------------------
def run_covariance_pilot(cfg: ShotNoiseConfig, theta: np.ndarray, g_exact: np.ndarray, out_dir: Path) -> pd.DataFrame:
    ansatz = HardwareEfficientAnsatz(cfg.n_qubits, cfg.depth, cfg.entangler)
    cov_dir = out_dir / "covariance"
    cov_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for M in cfg.cov_shots:
        est = FiniteShotParameterShift(ansatz, cfg.cost, M, master_seed=[cfg.master_seed, 99_991, M])
        xi = est.replicate_gradient(theta, cfg.cov_replicates) - g_exact[None, :]
        cov = np.cov(xi, rowvar=False, ddof=1)
        pd.DataFrame(cov).to_csv(cov_dir / f"cov_M{M}.csv", index=False, header=False)
        off = cov[~np.eye(cov.shape[0], dtype=bool)]
        diag_theory = np.array([theoretical_parameter_shift_variance(ansatz, theta, k, M, cfg.cost) for k in range(ansatz.n_params)])
        rows.append({"shots": M, "replicates": cfg.cov_replicates, "p": ansatz.n_params,
                     "trace_cov": float(np.trace(cov)), "trace_cov_theory": float(diag_theory.sum()),
                     "frobenius_norm": float(np.linalg.norm(cov)),
                     "max_abs_offdiag": float(np.max(np.abs(off))), "mean_abs_offdiag": float(np.mean(np.abs(off))),
                     "trace_M_cov": float(M * np.trace(cov)), "trace_M_cov_theory": float(M * diag_theory.sum()),
                     "max_abs_offdiag_over_mean_diag": float(np.max(np.abs(off)) / np.mean(np.diag(cov)))})
    return pd.DataFrame(rows)


# ----- part D ------------------------------------------------------------------------
def make_figures(cfg: ShotNoiseConfig, summary: pd.DataFrame, fig_dir: Path) -> list[Path]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig_dir.mkdir(parents=True, exist_ok=True)
    cfg_txt = (f"n={cfg.n_qubits}, depth={cfg.depth}, {cfg.entangler}, cost={cfg.cost}, "
               f"theta_seed={cfg.theta_seed}, {cfg.replicates} replicates per point")
    ks = sorted(summary.k.unique())
    markers = ["o", "s", "^", "D", "v"]
    paths = []

    # 1. variance vs shots (log-log) with theory
    fig, ax = plt.subplots(figsize=(6, 4.5))
    for i, k in enumerate(ks):
        s = summary[summary.k == k].sort_values("shots")
        ax.loglog(s.shots, s.var_xi_emp, marker=markers[i % 5], linestyle="-", label=f"empirical, k={k}")
        ax.loglog(s.shots, s.var_xi_theory, linestyle="--", color="gray", alpha=0.8,
                  label="theory (2−C₊²−C₋²)/(4M)" if i == 0 else None)
    ax.set_xlabel("shots per circuit evaluation, M")
    ax.set_ylabel("Var(ξ_k)  (ddof=1)")
    ax.set_title("Finite-shot parameter-shift gradient variance vs M\n" + cfg_txt, fontsize=9)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    p = fig_dir / "variance_vs_shots.png"; fig.tight_layout(); fig.savefig(p, dpi=150); plt.close(fig); paths.append(p)

    # 2. scaled variance M*Var
    fig, ax = plt.subplots(figsize=(6, 4.5))
    for i, k in enumerate(ks):
        s = summary[summary.k == k].sort_values("shots")
        ax.semilogx(s.shots, s.M_times_var_emp, marker=markers[i % 5], linestyle="-", label=f"M·Var_emp, k={k}")
        ax.axhline(s.M_times_var_theory.iloc[0], linestyle="--", color="gray", alpha=0.8,
                   label="M·Var_theory (per k)" if i == 0 else None)
    ax.set_xlabel("shots per circuit evaluation, M")
    ax.set_ylabel("M · Var(ξ_k)")
    ax.set_title("Scaled variance (should be flat if Var ∝ 1/M)\n" + cfg_txt, fontsize=9)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    p = fig_dir / "scaled_variance.png"; fig.tight_layout(); fig.savefig(p, dpi=150); plt.close(fig); paths.append(p)

    # 3. bias with 95% CI
    fig, ax = plt.subplots(figsize=(6, 4.5))
    for i, k in enumerate(ks):
        s = summary[summary.k == k].sort_values("shots")
        err = np.vstack([s.mean_xi - s.ci95_low, s.ci95_high - s.mean_xi])
        ax.errorbar(s.shots * (1 + 0.06 * (i - len(ks) / 2)), s.mean_xi, yerr=err, marker=markers[i % 5],
                    linestyle="none", capsize=3, label=f"mean ξ ± 95% CI, k={k}")
    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_xscale("log")
    ax.set_xlabel("shots per circuit evaluation, M")
    ax.set_ylabel("mean ξ_k = mean(ĝ_k) − g_k")
    ax.set_title("Empirical bias of finite-shot estimator\n" + cfg_txt, fontsize=9)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    p = fig_dir / "bias_vs_shots.png"; fig.tight_layout(); fig.savefig(p, dpi=150); plt.close(fig); paths.append(p)
    return paths


# ----- driver -------------------------------------------------------------------------
def run_stage2(cfg: ShotNoiseConfig, out_dir: Path = RESULTS_DIR, figures: bool = True) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    raw, summary, scaling, theta, g_exact = run_single_point(cfg)
    cov_summary = run_covariance_pilot(cfg, theta, g_exact, out_dir)

    (out_dir / "config.json").write_text(json.dumps(asdict(cfg), indent=2), encoding="utf-8")
    raw.to_csv(out_dir / "shot_noise_raw.csv", index=False)
    summary.to_csv(out_dir / "shot_noise_summary.csv", index=False)
    scaling.to_csv(out_dir / "shot_noise_scaling.csv", index=False)
    cov_summary.to_csv(out_dir / "covariance_summary.csv", index=False)
    np.savetxt(out_dir / "theta.csv", theta.ravel(), delimiter=",")
    np.savetxt(out_dir / "g_exact.csv", g_exact, delimiter=",")
    figs = make_figures(cfg, summary, out_dir / "figures") if figures else []
    return {"raw": raw, "summary": summary, "scaling": scaling, "covariance": cov_summary,
            "theta": theta, "g_exact": g_exact, "figures": figs, "out_dir": out_dir}


def _parse(argv=None) -> tuple[ShotNoiseConfig, Path]:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--n-qubits", type=int, default=3)
    p.add_argument("--depth", type=int, default=2)
    p.add_argument("--entangler", choices=("ring", "chain"), default="ring")
    p.add_argument("--theta-seed", type=int, default=7)
    p.add_argument("--master-seed", type=int, default=2025)
    p.add_argument("--shots", type=int, nargs="+", default=[64, 128, 256, 512, 1024, 2048])
    p.add_argument("--replicates", type=int, default=200)
    p.add_argument("--k", type=int, nargs="+", default=None, help="flat parameter indices (default first/middle/last)")
    p.add_argument("--cov-shots", type=int, nargs="+", default=[128, 512, 2048])
    p.add_argument("--cov-replicates", type=int, default=100)
    p.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    a = p.parse_args(argv)
    cfg = ShotNoiseConfig(n_qubits=a.n_qubits, depth=a.depth, entangler=a.entangler, theta_seed=a.theta_seed,
                          master_seed=a.master_seed, shots=tuple(a.shots), replicates=a.replicates,
                          k_indices=tuple(a.k) if a.k else None, cov_shots=tuple(a.cov_shots),
                          cov_replicates=a.cov_replicates)
    return cfg, a.out_dir


def main(argv=None) -> dict:
    cfg, out_dir = _parse(argv)
    res = run_stage2(cfg, out_dir)
    cols = ["k", "shots", "g_exact", "mean_xi", "se_mean_xi", "z_mean_xi", "var_xi_emp", "var_xi_theory",
            "var_ratio_emp_over_theory", "M_times_var_emp", "M_times_var_theory"]
    with pd.option_context("display.width", 220, "display.max_columns", 40, "display.float_format", "{:.5g}".format):
        print(f"config: {cfg}\n")
        print("summary per (k, M):")
        print(res["summary"][cols].to_string(index=False))
        print("\n1/M scaling per k:")
        print(res["scaling"].to_string(index=False))
        print("\ncovariance pilot per M:")
        print(res["covariance"].to_string(index=False))
    print(f"\nwrote outputs to {res['out_dir']}")
    for f in res["figures"]:
        print(f"  figure: {f} ({f.stat().st_size} bytes)")
    return res


if __name__ == "__main__":
    main()
