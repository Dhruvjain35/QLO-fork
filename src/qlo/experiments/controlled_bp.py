"""Stage 3: controlled barren-plateau benchmark (Cerezo et al. 2021, RX-product circuit).

Primary statistic:  Var_theta[dC/dtheta_0]  (ddof=1) over theta ~ U[-pi,pi]^n,
for the global cost (theory (1/8)(3/8)^(n-1), exponential) and the matched
local cost (theory 1/(8n^2), polynomial).

The large sweep uses the CLOSED-FORM gradients (exact arithmetic; validated
against the PennyLane circuit in tests and in the cross-check below). It is NOT
quantum-hardware execution and not even statevector simulation.

Outputs (under ``--out-dir``, default ``results/stage3``):
    config.json
    controlled_bp_summary.csv     one row per (n, cost) — primary result
    symmetry_check.csv            other k at selected n
    pennylane_crosscheck.csv      simulator-based Var_theta[dC/dtheta_0] at small n
    numerical_stability.csv       NaN/Inf/underflow / log-domain diagnostics per n
    global_fit.json, local_fit.json, model_comparison.json
    figures/*.png
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from qlo.analysis.statistics import Z_95
from qlo.benchmarks.cerezo2021 import (
    COST_NAMES,
    THEORETICAL_GLOBAL_SEMILOG_SLOPE,
    THEORETICAL_LOCAL_LOGLOG_SLOPE,
    Cerezo2021Circuit,
    closed_form_global_gradient_component_logdomain,
    closed_form_gradient_component,
    factorized_global_second_moment_estimate,
    sample_params,
    theoretical_variance,
    theoretical_variance_estimator_rel_se,
)
from qlo.utils.seeding import make_rng

RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "stage3"


@dataclass(frozen=True)
class ControlledBPConfig:
    n_values: tuple[int, ...] = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24)
    n_init: int = 10_000
    master_seed: int = 3
    parameter_index: int = 0
    symmetry_n: tuple[int, ...] = (4, 12, 24)
    symmetry_n_init: int = 10_000
    pennylane_n: tuple[int, ...] = (2, 4, 6, 8, 10)
    pennylane_n_init_grad: int = 1_000       # qml.grad (backprop) per-sample gradients
    pennylane_n_init_batched: int = 10_000   # broadcast parameter-shift, simulator arithmetic only
    save_raw: bool = False
    # a-priori resolvability criterion for the "resolved-range" fit: predicted relative SE of the
    # sample variance (exact 4th-moment formula) must be below this
    resolved_rel_se_max: float = 0.5

    def __post_init__(self) -> None:
        if self.n_init < 3 or self.parameter_index < 0:
            raise ValueError("n_init must be >= 3 and parameter_index >= 0")
        if any(n <= self.parameter_index for n in self.n_values):
            raise ValueError("parameter_index must be < every n")


# ----- statistics ---------------------------------------------------------------------
def gradient_component_stats(g: np.ndarray, var_theory: float, rel_se_exact: float | None = None) -> dict[str, float]:
    """Summary of one gradient component across theta samples. Variance uses ddof=1.

    ``variance_se_sample`` is the plug-in SE of the sample variance, sqrt((m4 - s^4 (N-3)/(N-1)) / N),
    using the SAMPLE 4th moment — unreliable when the tail is under-sampled. ``variance_rel_se_exact``
    (if given) is the same quantity from the EXACT 4th moment; ``variance_z_exact`` uses it.
    """
    g = np.asarray(g, dtype=np.float64)
    N = g.size
    mean = float(np.mean(g))
    var = float(np.var(g, ddof=1))
    std = float(np.sqrt(var))
    se = std / np.sqrt(N)
    m4 = float(np.mean((g - mean) ** 4))
    var_se = float(np.sqrt(max(m4 - var**2 * (N - 3) / (N - 1), 0.0) / N))
    return {
        "n_initializations": int(N),
        "mean_gradient": mean,
        "mean_abs_gradient": float(np.mean(np.abs(g))),
        "median_abs_gradient": float(np.median(np.abs(g))),
        "rms_gradient": float(np.sqrt(np.mean(g**2))),
        "std_gradient": std,
        "empirical_variance": var,
        "theoretical_variance": float(var_theory),
        "variance_ratio": var / var_theory if var_theory > 0 else float("nan"),
        "variance_se_sample": var_se,
        "variance_z_sample": (var - var_theory) / var_se if var_se > 0 else float("nan"),
        "variance_rel_se_exact": float(rel_se_exact) if rel_se_exact is not None else float("nan"),
        "variance_z_exact": (var / var_theory - 1.0) / rel_se_exact if rel_se_exact else float("nan"),
        "standard_error_mean": float(se),
        "z_mean": mean / se if se > 0 else 0.0,
        "ci95_low": mean - Z_95 * se,
        "ci95_high": mean + Z_95 * se,
        "n_exact_zero": int(np.sum(g == 0.0)),
        "min_abs_nonzero": float(np.min(np.abs(g[g != 0.0]))) if np.any(g != 0.0) else float("nan"),
        "max_abs": float(np.max(np.abs(g))),
        "all_finite": bool(np.all(np.isfinite(g))),
    }


def _linear_fit(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    b, a = np.polyfit(x, y, 1)
    pred = a + b * x
    rss = float(np.sum((y - pred) ** 2))
    tss = float(np.sum((y - y.mean()) ** 2))
    N = x.size
    # Gaussian least-squares AIC up to an additive constant common to both models: N ln(RSS/N) + 2K, K=2
    aic = N * np.log(rss / N) + 2 * 2 if rss > 0 else -np.inf
    return {"slope": float(b), "intercept": float(a), "r2": 1.0 - rss / tss, "rss": rss, "aic": float(aic), "n_points": int(N)}


def fit_models(n: np.ndarray, var: np.ndarray) -> dict[str, dict[str, float]]:
    """Fit exponential (log Var ~ n) and power-law (log Var ~ log n) models."""
    n, lv = np.asarray(n, dtype=np.float64), np.log(np.asarray(var, dtype=np.float64))
    return {"exponential": _linear_fit(n, lv), "power_law": _linear_fit(np.log(n), lv)}


# ----- experiment parts -------------------------------------------------------------------
def run_sweep(cfg: ControlledBPConfig, out_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    k = cfg.parameter_index
    rows, stab = [], []
    raw_dir = out_dir / "raw"
    for n in cfg.n_values:
        Theta = sample_params(n, make_rng([cfg.master_seed, n]), cfg.n_init)
        if cfg.save_raw:
            raw_dir.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(raw_dir / f"theta_n{n}.npz", theta=Theta)
        for cost in COST_NAMES:
            g = closed_form_gradient_component(cost, Theta, k)
            vt = theoretical_variance(cost, n)
            row = {"n": n, "cost_type": cost, "parameter_index": k,
                   **gradient_component_stats(g, vt, theoretical_variance_estimator_rel_se(cost, n, cfg.n_init))}
            if cost == "global":  # benchmark-specific diagnostic, see factorized_global_second_moment_estimate
                f = factorized_global_second_moment_estimate(Theta, k)
                row.update({"factorized_second_moment": f, "factorized_ratio": f / vt})
            else:
                row.update({"factorized_second_moment": float("nan"), "factorized_ratio": float("nan")})
            rows.append(row)
        # numerical stability diagnostics (global product of cos^2 terms)
        g = closed_form_gradient_component("global", Theta, k)
        sign, log_abs = closed_form_global_gradient_component_logdomain(Theta, k)
        nz = g != 0.0
        rel = np.abs(sign[nz] * np.exp(log_abs[nz]) - g[nz]) / np.abs(g[nz])
        stab.append({"n": n, "theoretical_variance_global": theoretical_variance("global", n),
                     "any_nan": bool(np.isnan(g).any()), "any_inf": bool(np.isinf(g).any()),
                     "n_exact_zero": int((~nz).sum()), "min_abs_nonzero": float(np.min(np.abs(g[nz]))),
                     "max_abs": float(np.max(np.abs(g))), "min_log10_abs": float(np.min(log_abs[nz]) / np.log(10)),
                     "max_rel_diff_logdomain_vs_direct": float(rel.max()),
                     "float64_tiny": float(np.finfo(np.float64).tiny)})
    return pd.DataFrame(rows), pd.DataFrame(stab)


def run_symmetry_check(cfg: ControlledBPConfig) -> pd.DataFrame:
    rows = []
    for n in cfg.symmetry_n:
        Theta = sample_params(n, make_rng([cfg.master_seed, 7_777, n]), cfg.symmetry_n_init)
        ks = sorted({0, 1, n // 2, n - 1})
        for cost in COST_NAMES:
            vt = theoretical_variance(cost, n)
            for kk in ks:
                s = gradient_component_stats(closed_form_gradient_component(cost, Theta, kk), vt,
                                             theoretical_variance_estimator_rel_se(cost, n, cfg.symmetry_n_init))
                rows.append({"n": n, "cost_type": cost, "parameter_index": kk, "empirical_variance": s["empirical_variance"],
                             "theoretical_variance": vt, "variance_ratio": s["variance_ratio"],
                             "variance_rel_se_exact": s["variance_rel_se_exact"], "variance_z_exact": s["variance_z_exact"],
                             "z_mean": s["z_mean"]})
    return pd.DataFrame(rows)


def run_pennylane_crosscheck(cfg: ControlledBPConfig, summary: pd.DataFrame) -> pd.DataFrame:
    """Simulator-based Var_theta[dC/dtheta_k] at small n, two ways, on fresh theta samples."""
    k = cfg.parameter_index
    rows = []
    for n in cfg.pennylane_n:
        circ = Cerezo2021Circuit(n)
        rng = make_rng([cfg.master_seed, 4_242, n])
        # (a) per-sample qml.grad (backprop) on the actual circuit
        Theta_a = sample_params(n, rng, cfg.pennylane_n_init_grad)
        # (b) broadcast two-term parameter shift, simulator arithmetic only
        Theta_b = sample_params(n, rng, cfg.pennylane_n_init_batched)
        for cost in COST_NAMES:
            vt = theoretical_variance(cost, n)
            g_a = np.array([circ.gradient(cost, th)[k] for th in Theta_a])
            g_b = circ.gradient_component_parameter_shift_batched(cost, Theta_b, k)
            cf_a = closed_form_gradient_component(cost, Theta_a, k)
            cf_b = closed_form_gradient_component(cost, Theta_b, k)
            sa = gradient_component_stats(g_a, vt, theoretical_variance_estimator_rel_se(cost, n, cfg.pennylane_n_init_grad))
            sb = gradient_component_stats(g_b, vt, theoretical_variance_estimator_rel_se(cost, n, cfg.pennylane_n_init_batched))
            mc = summary[(summary.n == n) & (summary.cost_type == cost)].iloc[0]
            rows.append({"n": n, "cost_type": cost, "parameter_index": k,
                         "pl_grad_n_init": sa["n_initializations"], "pl_grad_variance": sa["empirical_variance"],
                         "pl_grad_ratio": sa["variance_ratio"], "pl_grad_rel_se_exact": sa["variance_rel_se_exact"], "pl_grad_z_mean": sa["z_mean"],
                         "pl_grad_max_abs_diff_vs_closed_form": float(np.max(np.abs(g_a - cf_a))),
                         "pl_ps_n_init": sb["n_initializations"], "pl_ps_variance": sb["empirical_variance"],
                         "pl_ps_ratio": sb["variance_ratio"], "pl_ps_rel_se_exact": sb["variance_rel_se_exact"], "pl_ps_z_mean": sb["z_mean"],
                         "pl_ps_max_abs_diff_vs_closed_form": float(np.max(np.abs(g_b - cf_b))),
                         "closed_form_mc_variance": mc["empirical_variance"], "closed_form_mc_ratio": mc["variance_ratio"],
                         "theoretical_variance": vt})
    return pd.DataFrame(rows)


def make_figures(cfg: ControlledBPConfig, summary: pd.DataFrame, fig_dir: Path) -> list[Path]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig_dir.mkdir(parents=True, exist_ok=True)
    cap = f"RX-product benchmark (Cerezo 2021), θ~U[-π,π]^n, k={cfg.parameter_index}, {cfg.n_init} inits/n, closed-form gradients"
    G = summary[summary.cost_type == "global"].sort_values("n")
    L = summary[summary.cost_type == "local"].sort_values("n")
    nn = np.linspace(G.n.min(), G.n.max(), 200)
    paths = []

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.semilogy(G.n, G.empirical_variance, "o", label="empirical Var_θ[∂C_G/∂θ₀] (ddof=1, generic sample variance)")
    ax.semilogy(G.n, G.factorized_second_moment, "x", color="C2", label="factorized estimator (benchmark-specific diagnostic)")
    ax.semilogy(nn, (1 / 8) * (3 / 8) ** (nn - 1), "--", color="gray", label="theory (1/8)(3/8)^(n−1)")
    ax.set_xlabel("n (qubits = parameters)"); ax.set_ylabel("Var_θ[∂C_G/∂θ₀]")
    ax.set_title("Global cost: gradient variance vs n\n" + cap, fontsize=8); ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8)
    p = fig_dir / "global_variance_scaling.png"; fig.tight_layout(); fig.savefig(p, dpi=150); plt.close(fig); paths.append(p)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.loglog(L.n, L.empirical_variance, "s", label="empirical Var_θ[∂C_L/∂θ₀] (ddof=1)")
    ax.loglog(nn, 1 / (8 * nn**2), "--", color="gray", label="theory 1/(8n²)")
    ax.set_xlabel("n (qubits = parameters)"); ax.set_ylabel("Var_θ[∂C_L/∂θ₀]")
    ax.set_title("Local cost: gradient variance vs n\n" + cap, fontsize=8); ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8)
    p = fig_dir / "local_variance_scaling.png"; fig.tight_layout(); fig.savefig(p, dpi=150); plt.close(fig); paths.append(p)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.semilogy(G.n, G.empirical_variance, "o", label="global, empirical")
    ax.semilogy(nn, (1 / 8) * (3 / 8) ** (nn - 1), "--", color="C0", alpha=0.7, label="global, theory")
    ax.semilogy(L.n, L.empirical_variance, "s", label="local, empirical")
    ax.semilogy(nn, 1 / (8 * nn**2), "--", color="C1", alpha=0.7, label="local, theory")
    ax.set_xlabel("n"); ax.set_ylabel("Var_θ[∂C/∂θ₀]")
    ax.set_title("Global (exponential) vs local (polynomial) gradient variance\n" + cap, fontsize=8)
    ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8)
    p = fig_dir / "global_vs_local.png"; fig.tight_layout(); fig.savefig(p, dpi=150); plt.close(fig); paths.append(p)

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, D, name in ((axes[0], G, "global"), (axes[1], L, "local")):
        ax.errorbar(D.n, D.mean_gradient, yerr=np.vstack([D.mean_gradient - D.ci95_low, D.ci95_high - D.mean_gradient]),
                    fmt="o", capsize=3, label="mean ∂C/∂θ₀ ± 95% CI")
        ax.axhline(0, color="black", linewidth=1); ax.set_xlabel("n"); ax.set_ylabel("mean gradient"); ax.set_title(name, fontsize=9)
        ax.grid(True, alpha=0.3); ax.legend(fontsize=8)
    fig.suptitle("Empirical mean gradient (should be 0)\n" + cap, fontsize=8)
    p = fig_dir / "mean_gradient.png"; fig.tight_layout(); fig.savefig(p, dpi=150); plt.close(fig); paths.append(p)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    for D, name, m in ((G, "global", "o"), (L, "local", "s")):
        ax.errorbar(D.n, D.variance_ratio, yerr=Z_95 * D.variance_rel_se_exact, fmt=m, capsize=3, label=f"{name} sample variance (±1.96 × exact predicted rel. SE)")
    ax.plot(G.n, G.factorized_ratio, "x", color="C2", markersize=10, markeredgewidth=2, zorder=5, label="global, factorized estimator (diagnostic)")
    ax.axhline(1, color="black", linewidth=1); ax.set_xlabel("n"); ax.set_ylabel("empirical / theoretical variance")
    ax.set_yscale("log")
    ax.set_title("Variance ratio vs n\n" + cap, fontsize=8); ax.grid(True, alpha=0.3); ax.legend(fontsize=8)
    p = fig_dir / "relative_error.png"; fig.tight_layout(); fig.savefig(p, dpi=150); plt.close(fig); paths.append(p)
    return paths


# ----- driver -------------------------------------------------------------------------
def run_stage3(cfg: ControlledBPConfig, out_dir: Path = RESULTS_DIR, figures: bool = True, pennylane: bool = True) -> dict:
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    summary, stability = run_sweep(cfg, out_dir)
    symmetry = run_symmetry_check(cfg)
    G = summary[summary.cost_type == "global"].sort_values("n")
    L = summary[summary.cost_type == "local"].sort_values("n")
    gm, lm = fit_models(G.n.to_numpy(), G.empirical_variance.to_numpy()), fit_models(L.n.to_numpy(), L.empirical_variance.to_numpy())
    Gr = G[G.variance_rel_se_exact < cfg.resolved_rel_se_max]
    gr = _linear_fit(Gr.n.to_numpy(dtype=float), np.log(Gr.empirical_variance.to_numpy())) if len(Gr) >= 3 else None
    gf = _linear_fit(G.n.to_numpy(dtype=float), np.log(G.factorized_second_moment.to_numpy()))
    global_fit = {"model": "log Var = intercept + slope * n", **gm["exponential"],
                  "theoretical_slope": THEORETICAL_GLOBAL_SEMILOG_SLOPE,
                  "abs_slope_error": abs(gm["exponential"]["slope"] - THEORETICAL_GLOBAL_SEMILOG_SLOPE),
                  "theoretical_intercept": float(np.log(1 / 8) - np.log(3 / 8)),
                  "variance_ratio_by_n": dict(zip(G.n.astype(int).astype(str), G.variance_ratio.round(4))),
                  "variance_rel_se_exact_by_n": dict(zip(G.n.astype(int).astype(str), G.variance_rel_se_exact.round(3))),
                  "fit_resolved_range": None if gr is None else {
                      "criterion": f"exact predicted rel SE of sample variance < {cfg.resolved_rel_se_max}",
                      "n_values": [int(x) for x in Gr.n], **gr,
                      "abs_slope_error": abs(gr["slope"] - THEORETICAL_GLOBAL_SEMILOG_SLOPE)},
                  "fit_factorized_estimator": {"note": "benchmark-specific product-structure estimator; diagnostic only",
                                               **gf, "abs_slope_error": abs(gf["slope"] - THEORETICAL_GLOBAL_SEMILOG_SLOPE),
                                               "ratio_by_n": dict(zip(G.n.astype(int).astype(str), G.factorized_ratio.round(4)))}}
    local_fit = {"model": "log Var = intercept + slope * log n", **lm["power_law"],
                 "theoretical_slope": THEORETICAL_LOCAL_LOGLOG_SLOPE,
                 "abs_slope_error": abs(lm["power_law"]["slope"] - THEORETICAL_LOCAL_LOGLOG_SLOPE),
                 "theoretical_intercept": float(np.log(1 / 8)),
                 "variance_ratio_by_n": dict(zip(L.n.astype(int).astype(str), L.variance_ratio.round(4))),
                 "variance_rel_se_exact_by_n": dict(zip(L.n.astype(int).astype(str), L.variance_rel_se_exact.round(3)))}
    model_cmp = {
        "global": {**gm, "delta_aic_power_minus_exp": gm["power_law"]["aic"] - gm["exponential"]["aic"],
                   "preferred": "exponential" if gm["exponential"]["aic"] < gm["power_law"]["aic"] else "power_law"},
        "local": {**lm, "delta_aic_exp_minus_power": lm["exponential"]["aic"] - lm["power_law"]["aic"],
                  "preferred": "power_law" if lm["power_law"]["aic"] < lm["exponential"]["aic"] else "exponential"},
        "note": "AIC = N ln(RSS/N) + 2K (K=2), additive constant dropped; 12 points over n=2..24. "
                "Exact theoretical formulas are the primary validation, not this comparison.",
    }
    crosscheck = run_pennylane_crosscheck(cfg, summary) if pennylane else pd.DataFrame()

    (out_dir / "config.json").write_text(json.dumps(asdict(cfg), indent=2), encoding="utf-8")
    summary.to_csv(out_dir / "controlled_bp_summary.csv", index=False)
    symmetry.to_csv(out_dir / "symmetry_check.csv", index=False)
    stability.to_csv(out_dir / "numerical_stability.csv", index=False)
    crosscheck.to_csv(out_dir / "pennylane_crosscheck.csv", index=False)
    for name, obj in (("global_fit.json", global_fit), ("local_fit.json", local_fit), ("model_comparison.json", model_cmp)):
        (out_dir / name).write_text(json.dumps(obj, indent=2, default=float), encoding="utf-8")
    figs = make_figures(cfg, summary, out_dir / "figures") if figures else []
    return {"summary": summary, "symmetry": symmetry, "stability": stability, "crosscheck": crosscheck,
            "global_fit": global_fit, "local_fit": local_fit, "model_comparison": model_cmp, "figures": figs, "out_dir": out_dir}


def _parse(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--n-values", type=int, nargs="+", default=list(ControlledBPConfig.n_values))
    p.add_argument("--n-init", type=int, default=ControlledBPConfig.n_init)
    p.add_argument("--master-seed", type=int, default=ControlledBPConfig.master_seed)
    p.add_argument("--k", type=int, default=0)
    p.add_argument("--pennylane-n", type=int, nargs="+", default=list(ControlledBPConfig.pennylane_n))
    p.add_argument("--pennylane-n-init-grad", type=int, default=ControlledBPConfig.pennylane_n_init_grad)
    p.add_argument("--pennylane-n-init-batched", type=int, default=ControlledBPConfig.pennylane_n_init_batched)
    p.add_argument("--no-pennylane", action="store_true")
    p.add_argument("--save-raw", action="store_true")
    p.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    a = p.parse_args(argv)
    cfg = ControlledBPConfig(n_values=tuple(a.n_values), n_init=a.n_init, master_seed=a.master_seed, parameter_index=a.k,
                             pennylane_n=tuple(a.pennylane_n), pennylane_n_init_grad=a.pennylane_n_init_grad,
                             pennylane_n_init_batched=a.pennylane_n_init_batched, save_raw=a.save_raw)
    return cfg, a.out_dir, not a.no_pennylane


def main(argv=None) -> dict:
    cfg, out_dir, pl = _parse(argv)
    res = run_stage3(cfg, out_dir, pennylane=pl)
    cols = ["n", "cost_type", "mean_gradient", "standard_error_mean", "z_mean", "empirical_variance", "theoretical_variance", "variance_ratio", "variance_rel_se_exact", "variance_z_exact", "factorized_ratio", "n_exact_zero"]
    with pd.option_context("display.width", 220, "display.max_columns", 40, "display.float_format", "{:.5g}".format):
        print(f"config: {cfg}\n\nsummary:"); print(res["summary"][cols].to_string(index=False))
        skip = ("variance_ratio_by_n", "variance_rel_se_exact_by_n", "ratio_by_n")
        print("\nglobal fit:", json.dumps({k: v for k, v in res["global_fit"].items() if k not in skip}, indent=1, default=float))
        print("local fit: ", json.dumps({k: v for k, v in res["local_fit"].items() if k not in skip}, indent=1, default=float))
        print("\nmodel comparison:"); print(json.dumps(res["model_comparison"], indent=1, default=float))
        print("\nsymmetry check:"); print(res["symmetry"].to_string(index=False))
        print("\nnumerical stability:"); print(res["stability"].to_string(index=False))
        if len(res["crosscheck"]):
            print("\npennylane cross-check:"); print(res["crosscheck"].to_string(index=False))
    print(f"\nwrote {res['out_dir']}")
    for f in res["figures"]:
        print(f"  figure: {f.name} ({f.stat().st_size} bytes)")
    return res


if __name__ == "__main__":
    main()
