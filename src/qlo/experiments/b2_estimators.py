"""B2: four fidelity-gradient estimators on the frozen Stage 7 RX-product landscape.

    python -m qlo.experiments.b2_estimators                 # all phases -> results/b2_estimators/

Phases (in order; each STOPs on failure): validate (destructive SWAP + Hadamard circuits, Hadamard variance;
Case C / D gates) -> rx (four-estimator required shots on the Stage 7 population, Stage 7 regression, replicate seeds,
slopes) -> fixed (fixed-budget failure modes) -> spot (secondary entangling spot check) -> figures.
The configuration is qlo.b2.config.B2Config, frozen in docs/b2/B2_CONFIG.md (checked at start).
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from qlo.b2 import analysis as AZ
from qlo.b2 import config as CF
from qlo.b2 import figures as FG
from qlo.b2 import required_shots as RS
from qlo.b2 import resources as RES
from qlo.stage6.analysis import linear_fit

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results" / "b2_estimators"
STAGE7 = ROOT / "results" / "stage7"
LOG2, LOG4 = float(np.log10(2.0)), float(np.log10(4.0))


class Stop(SystemExit):
    """A predeclared STOP condition (Case C / D or a failed regression)."""


def log(msg: str) -> None:
    print(msg, flush=True)
    with open(OUT / "numerics_log.md", "a") as f:
        f.write(msg + "\n")


def summarize(x, n_boot: int, seed: int) -> dict:
    """Seed mean, SD, 95% percentile interval of the values and percentile-bootstrap CI of the mean (B3 definitions)."""
    x = np.asarray(x, dtype=np.float64)
    rng = np.random.default_rng(np.random.SeedSequence([3, 0xB3, int(seed)]))
    means = x[rng.integers(0, x.size, (n_boot, x.size))].mean(axis=1)
    return {"n_seeds": int(x.size), "mean": float(x.mean()), "sd": float(x.std(ddof=1)),
            "pct_lo": float(np.percentile(x, 2.5)), "pct_hi": float(np.percentile(x, 97.5)),
            "boot_lo": float(np.percentile(means, 2.5)), "boot_hi": float(np.percentile(means, 97.5))}


# =================================================================================================================
def phase_validate(cfg) -> None:
    t = time.time()
    ds = AZ.destructive_swap_validation(cfg)
    ds.to_csv(OUT / "destructive_swap_validation.csv", index=False)
    hc = AZ.hadamard_circuit_validation()
    hc.to_csv(OUT / "hadamard_circuit_validation.csv", index=False)
    hv, pmf = AZ.hadamard_variance_validation(cfg)
    hv.to_csv(OUT / "hadamard_variance_validation.csv", index=False)
    pmf.to_csv(OUT / "hadamard_exact_smallM.csv", index=False)
    e_ds = float(ds[["abs_err_ancilla", "abs_err_destructive", "abs_err_ancilla_vs_destructive"]].max().max())
    zmax = float(ds[["dswap_mean_z", "ancilla_mean_z", "two_sample_z"]].abs().max().max())
    log(f"validate: destructive/ancilla SWAP circuits max |P(+1) - (1+F)/2| = {e_ds:.2e}; finite-shot max |z| = {zmax:.2f} "
        f"({len(ds)} cells); var x M rel err max {float((ds.dswap_sample_var_x_M / ds.model_var_x_M - 1).abs().max()):.3f}")
    if e_ds > cfg.swap_equality_tol:
        raise Stop("STOP (CASE C): destructive SWAP circuit disagrees with the ancilla SWAP / (1+F)/2 model")
    e_h = float(hc[["max_abs_err", "abs_err_x2_plus_y2_vs_F"]].max().max())
    log(f"validate: Hadamard circuits (numpy + PennyLane qml.ctrl, complex overlaps) max error = {e_h:.2e}")
    if e_h > cfg.circuit_tol:
        raise Stop("STOP: Hadamard-test circuit expectations disagree with Re/Im of the overlap")
    ex = hv.dropna(subset=["exact_var_err"])
    e_v = float(max(ex.exact_var_err.abs().max(), ex.exact_bias.abs().max(), (ex.exact_pmf_sum - 1).abs().max()))
    gr = hv.dropna(subset=["exact_grad_var"])
    e_g = float(max(gr.exact_grad_bias.abs().max(), (gr.exact_grad_var - gr.grad_var_formula).abs().max()))
    log(f"validate: Hadamard U-statistic exact (M <= {cfg.hadamard_exact_validation_max_m}) max |bias|,|var err|,|pmf-1| = {e_v:.2e}; "
        f"gradient exact bias/var err = {e_g:.2e}; MC max |mean z| = {hv.mc_mean_z.abs().max():.2f}, "
        f"max |var rel err| = {hv.mc_var_rel_err.abs().max():.4f} ({time.time() - t:.0f}s)")
    if e_v > cfg.variance_tol or e_g > cfg.variance_tol:
        raise Stop("STOP (CASE D): Hadamard variance / unbiasedness fails exact enumeration")


# =================================================================================================================
def _medians(n_values, seed, n_samples, cfg, rho):
    rows, keep = [], {}
    for n in n_values:
        r = RS.required_all(n, n_samples, seed, cfg.req_stream, rho)
        q = r["theta_q"]
        for est, lm in r["log10_m_internal"].items():
            tot = lm + np.log10(CF.EXECUTIONS_PER_M[est])
            rows.append({"seed": seed, "n": n, "rho": rho, "estimator": est, "n_samples": n_samples,
                         "median_log10_M_internal": float(np.median(lm)), "median_log10_total_executions": float(np.median(tot)),
                         "q25_log10_total": float(np.percentile(tot, 25)), "q75_log10_total": float(np.percentile(tot, 75)),
                         "nonfinite": int(np.sum(~np.isfinite(lm)))})
        keep[n] = r
    return pd.DataFrame(rows), keep


def _fit(df, value, cfg):
    out = []
    for (seed, rho, est), g in df.groupby(["seed", "rho", "estimator"], sort=False):
        for name, lo, hi in cfg.fit_ranges:
            d = g[(g.n >= lo) & (g.n <= hi)].sort_values("n")
            f = linear_fit(d.n.values, d[value].values)
            resid = d[value].values - (f["intercept"] + f["slope"] * d.n.values)
            out.append({"seed": seed, "rho": rho, "estimator": est, "fit_range": name, "quantity": value, **f,
                        "residuals": " ".join(f"{v:.5f}" for v in resid)})
    return pd.DataFrame(out)


def phase_rx(cfg) -> None:
    t = time.time()
    med_rows, fits, per_theta = [], [], []
    for rho in (cfg.rho_primary, cfg.rho_secondary):
        med, keep = _medians(cfg.rx_n, cfg.stage7_seed, cfg.stage7_samples, cfg, rho)
        med_rows.append(med)
        if rho == cfg.rho_primary:
            for n, r in keep.items():                      # compact per-theta subsample for figures (2000 theta per n)
                q, m = r["theta_q"], r["log10_m_internal"]
                sub = slice(0, 2000)
                per_theta.append(pd.DataFrame({"n": n, "log10_S": np.log10(q["F_plus"][sub] + q["F_minus"][sub]), "s": q["s"][sub],
                                               **{f"log10_total_{e}": (m[e][sub] + np.log10(CF.EXECUTIONS_PER_M[e])) for e in m}}))
            # destructive vs ancilla SWAP per-theta agreement (control)
            ctrl = []
            for n, r in keep.items():
                m = r["log10_m_internal"]
                d = np.abs(m["swap_destructive"] - m["swap_ancilla"])
                ctrl.append({"n": n, "median_abs_dlog10": float(np.median(d)), "q999_abs_dlog10": float(np.quantile(d, 0.999)),
                             "max_abs_dlog10": float(d.max()), "frac_exactly_equal": float(np.mean(d == 0)),
                             "median_diff": float(np.median(m["swap_destructive"]) - np.median(m["swap_ancilla"]))})
            pd.DataFrame(ctrl).to_csv(OUT / "swap_destructive_vs_ancilla_rx.csv", index=False)
    med = pd.concat(med_rows, ignore_index=True)
    # Stage 7 regression: LE / SWAP SNR medians on the same population must reproduce Stage 7 exactly
    st7 = pd.read_csv(STAGE7 / "scaling_summary.csv")
    reg = []
    for sc, est in (("loschmidt", "loschmidt"), ("swap", "swap_ancilla")):
        for tag, rho in (("snr1", 1.0), ("snr2", 2.0)):
            for n in cfg.rx_n:
                a = st7[(st7.n == n) & (st7.scheme == sc)][f"{tag}_log10M_median"].iloc[0]
                b = med[(med.n == n) & (med.estimator == est) & (med.rho == rho)].median_log10_M_internal.iloc[0]
                reg.append({"scheme": sc, "target": tag, "n": n, "stage7": a, "b2": b, "abs_diff": abs(a - b)})
    reg = pd.DataFrame(reg)
    reg.to_csv(OUT / "stage7_regression.csv", index=False)
    log(f"rx: Stage 7 LE/SWAP median regression max |diff| = {reg.abs_diff.max():.2e} over {len(reg)} cells")
    if reg.abs_diff.max() > 1e-12:
        raise Stop("STOP: B2 does not reproduce the frozen Stage 7 LE/SWAP medians")
    # replicate seeds (slope uncertainty)
    rep = pd.concat([_medians(cfg.rx_n, sd, cfg.replicate_samples, cfg, cfg.rho_primary)[0] for sd in cfg.replicate_seeds], ignore_index=True)
    allmed = pd.concat([med, rep], ignore_index=True)
    allmed.to_csv(OUT / "required_shots_rx.csv", index=False)
    f_tot = _fit(allmed, "median_log10_total_executions", cfg)
    f_int = _fit(allmed, "median_log10_M_internal", cfg)
    fits = pd.concat([f_tot, f_int], ignore_index=True)
    fits.to_csv(OUT / "seed_slopes.csv", index=False)
    rows = []
    for (est, rng_name, quantity), g in fits[fits.rho == cfg.rho_primary].groupby(["estimator", "fit_range", "quantity"], sort=False):
        st = g[g.seed == cfg.stage7_seed].iloc[0]
        rp = g[g.seed != cfg.stage7_seed]
        rows.append({"estimator": est, "fit_range": rng_name, "quantity": quantity, "stage7_population_slope": st.slope,
                     "stage7_population_intercept": st.intercept, "stage7_population_r2": st.r2, "stage7_population_residuals": st.residuals,
                     **{f"replicate_{k}": v for k, v in summarize(rp.slope.values, cfg.n_boot_seed, cfg.boot_seed).items()}})
    summ = pd.DataFrame(rows)
    summ.to_csv(OUT / "slope_summary.csv", index=False)
    pd.concat(per_theta).to_csv(OUT / "required_shots_rx_theta_subsample.csv.gz", index=False)
    d = summ[(summ.fit_range == "primary_2_20") & (summ.quantity == "median_log10_total_executions")].set_index("estimator")
    log("rx: slopes of median log10 total executions (Stage 7 population, n = 2..20): " +
        ", ".join(f"{e} {d.loc[e, 'stage7_population_slope']:.4f}" for e in cfg.estimators) + f" ({time.time() - t:.0f}s)")
    sw = summ[summ.estimator.isin(["swap_ancilla", "swap_destructive"])].pivot_table(index=["fit_range", "quantity"], columns="estimator",
                                                                                     values="stage7_population_slope")
    dmax = float((sw.swap_ancilla - sw.swap_destructive).abs().max())
    log(f"rx: ancilla vs destructive SWAP slope difference max {dmax:.2e}")
    if dmax > 1e-6:
        raise Stop("STOP (CASE C): ancilla and destructive SWAP slopes differ")


def phase_fixed(cfg) -> None:
    t = time.time()
    fb = AZ.fixed_budget(cfg)
    fb.to_csv(OUT / "fixed_budget_failure_modes.csv", index=False)
    AZ.hadamard_distribution_examples(cfg).to_csv(OUT / "hadamard_distribution_examples.csv", index=False)
    log(f"fixed: {len(fb)} (n, budget, estimator) cells ({time.time() - t:.0f}s)")


def phase_spot(cfg) -> None:
    t = time.time()
    sp = AZ.entangling_spotcheck(cfg)
    sp.to_csv(OUT / "entangling_spotcheck.csv", index=False)
    fits = []
    for est, g in sp.groupby("estimator", sort=False):
        f = linear_fit(g.n.values, g.median_log10_total_executions.values)
        fits.append({"estimator": est, "slope": f["slope"], "r2": f["r2"]})
    pd.DataFrame(fits).to_csv(OUT / "entangling_spotcheck_slopes.csv", index=False)
    log("spot: SECONDARY ENTANGLING SPOT CHECK slopes (HEA depth n, EARLY, n 6..12): " +
        ", ".join(f"{r['estimator']} {r['slope']:.4f}" for r in fits) + f" ({time.time() - t:.0f}s)")


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--phase", choices=("validate", "rx", "fixed", "spot", "figures", "all"), default="all")
    a = p.parse_args(argv)
    cfg = CF.B2Config()
    frozen = CF.config_json_from_markdown((ROOT / "docs" / "b2" / "B2_CONFIG.md").read_text())
    if json.loads(frozen) != json.loads(cfg.to_json()):
        raise Stop("STOP: B2Config differs from docs/b2/B2_CONFIG.md")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "figures").mkdir(exist_ok=True)
    (OUT / "config.json").write_text(json.dumps({**json.loads(cfg.to_json()), "config_sha256": cfg.sha256(),
                                                 "executions_per_M": CF.EXECUTIONS_PER_M}, indent=2))
    RES.resource_table().to_csv(OUT / "resource_accounting.csv", index=False)
    log(f"\n## run {time.strftime('%Y-%m-%d %H:%M:%S %Z')} phase={a.phase} config sha256={cfg.sha256()}")
    phases = ("validate", "rx", "fixed", "spot", "figures") if a.phase == "all" else (a.phase,)
    if "validate" in phases:
        phase_validate(cfg)
    if "rx" in phases:
        phase_rx(cfg)
    if "fixed" in phases:
        phase_fixed(cfg)
    if "spot" in phases:
        phase_spot(cfg)
    if "figures" in phases:
        FG.all_figures(OUT, cfg)


if __name__ == "__main__":
    main()
