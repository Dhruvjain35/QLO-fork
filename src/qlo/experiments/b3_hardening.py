"""B3 statistical hardening of Stage 7 (delegated track, Satyabrat work allocation).

    python -m qlo.experiments.b3_hardening --workers 8                 # compute (cached) + analyse -> results/b3_hardening/
    python -m qlo.experiments.b3_hardening --fast --work-dir /tmp/b3   # reduced smoke run

Two uncertainty sources are kept SEPARATE throughout:
  SEED      (primary)   20 independent master seeds 10000..10019, each a fresh theta population and pipeline;
  THETA     (secondary) paired theta bootstrap inside the regenerated Stage 7 reference population (seed 0);
  HIERARCHICAL (optional, separately labelled) seeds resampled, then theta within each selected seed.
Stage 7 code, results and report are not modified. Per-theta caches go to --work-dir (default: external SSD).
"""

from __future__ import annotations

import argparse
import json
import pickle
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd

from qlo.hardening import bootstrap as BS
from qlo.hardening import figures as FIG
from qlo.hardening import intervals as IV
from qlo.hardening import numerics as NUM
from qlo.hardening import seed_replicates as SR
from qlo.stage6.analysis import wilson_ci
from qlo.stage6.directional import direction_probabilities
from qlo.stage7 import analysis as AN
from qlo.stage7.estimators import SCHEMES, pair
from qlo.experiments.stage7 import Stage7Config

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "b3_hardening"
STAGE7_DIR = ROOT / "results" / "stage7"
DEFAULT_WORK = Path("/Volumes/SSD Disk  1TB/qlo-b3-work")
SIGN_LAW_MEDIAN = (1.0 + 1.0 / np.sqrt(2.0)) / 2.0  # fixed Stage 7 prediction; never refitted


@dataclass(frozen=True)
class B3Config:
    seeds: tuple[int, ...] = SR.B3_SEEDS
    reference_seed: int = SR.STAGE7_SEED            # regenerated Stage 7 population (theta bootstrap reference)
    primary_n: tuple[int, ...] = SR.PRIMARY_N
    extension_n: tuple[int, ...] = SR.EXTENSION_N
    seed_samples: int = 25_000                      # theta per (seed, n), required shots
    reference_samples: int = 100_000               # = Stage 7 n_samples
    n_ge_8_secondary_fit: bool = True              # Stage 7 also reported n >= 8 slopes
    n_boot: int = 2000                              # theta bootstrap replicates
    n_boot_hier: int = 2000                         # two-level bootstrap replicates
    n_boot_seed: int = 10_000                       # bootstrap of the mean over seeds
    boot_seed: int = 2026
    fixed_n: tuple[int, ...] = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24)
    fixed_shots: tuple[int, ...] = (16, 64, 256, 1024, 4096, 16384, 65536)
    fixed_seed_samples: int = 10_000
    fixed_reference_samples: int = 20_000          # = Stage 7 paired_samples
    fixed_n_boot: int = 2000
    sign_law_n: tuple[int, ...] = (12, 14, 16, 18, 20, 22, 24)
    sign_law_deep_p_zero: float = 0.99              # predeclared deep-regime criterion: reference median LE P_zero
    mc_n: tuple[int, ...] = (8, 12, 16, 20, 24)
    mc_shots: tuple[int, ...] = (1024, 16384, 65536)
    mc_reps: int = 20_000
    vector_n: tuple[int, ...] = (4, 6, 8, 10, 12)
    vector_shots: tuple[int, ...] = (16, 64, 256, 1024, 4096)
    vector_theta: int = 400                         # per seed, = Stage 7
    vector_replicates: int = 25                     # per seed, = Stage 7
    opt_n: tuple[int, ...] = (6, 8, 10, 12)
    opt_starts_per_seed: int = 50                   # = Stage 7 opt_seeds; x 20 master seeds = 1000 paired starts per n
    opt_iters: int = 500
    opt_eta: float = 0.3                            # Stage 7 / Stage 4 value, NOT retuned
    # predeclared interval-check rule: the Stage 7 point estimate is ONE replicate (100k theta), so "inside the seed
    # interval" is judged against the seed 95% PERCENTILE interval (replicate-to-replicate spread). The stricter
    # bootstrap CI of the seed MEAN is reported alongside, and a z diagnostic rescales the seed SD to 100k theta.
    check_rule: str = "seed_percentile_interval (primary); seed-mean bootstrap CI and theta-bootstrap CI reported separately"


# =================================================================================================================
# workers (cached)
# =================================================================================================================
def _cache(work: Path, kind: str, seed: int, n=None) -> Path:
    d = work / kind
    d.mkdir(parents=True, exist_ok=True)
    return d / (f"seed{seed}.pkl" if n is None else f"seed{seed}_n{n}.npz")


def task_required(work: str, seed: int, n: int, n_samples: int) -> dict:
    path = _cache(Path(work), "required", seed, n)
    if path.exists():
        z = np.load(path)
        res = {"n": n, "seed": seed, "n_samples": int(z["vals"].shape[1]), "vals": z["vals"], "meth": z["meth"], "logA": z["logA"], "s": z["s"]}
        if res["n_samples"] == n_samples:
            return {"rows": SR.medians_and_methods(res), "check": NUM.validate_required_point(res)}
    t = time.time()
    res = SR.required_shots_per_theta(n, n_samples, seed)
    np.savez(path, vals=res["vals"], meth=res["meth"], logA=res["logA"], s=res["s"])
    return {"rows": SR.medians_and_methods(res), "check": NUM.validate_required_point(res), "seconds": time.time() - t}


def task_fixed(work: str, seed: int, n: int, shots: tuple, n_samples: int, keep: bool) -> list[dict]:
    rows_path = Path(work) / "fixed_rows" / f"seed{seed}_n{n}_N{n_samples}.pkl"
    rows_path.parent.mkdir(parents=True, exist_ok=True)
    if rows_path.exists() and (not keep or _cache(Path(work), "fixed", seed, n).exists()):
        return pickle.loads(rows_path.read_bytes())
    rows = _task_fixed(work, seed, n, shots, n_samples, keep)
    rows_path.write_bytes(pickle.dumps(rows))
    return rows


def _task_fixed(work: str, seed: int, n: int, shots: tuple, n_samples: int, keep: bool) -> list[dict]:
    path = _cache(Path(work), "fixed", seed, n)
    if path.exists() and np.load(path)["s"].size == n_samples:
        z = np.load(path)
        r = {"loschmidt": z["loschmidt"], "swap": z["swap"], "loschmidt_float_tie": z["loschmidt_float_tie"], "swap_float_tie": z["swap_float_tie"],
             "loschmidt_cond_accurate": z["loschmidt_cond_accurate"], "s": z["s"], "logA": z["logA"]}
    else:
        r = SR.fixed_shot_per_theta(n, shots, n_samples, seed)
        if keep:   # per-theta arrays are kept only for the reference population (theta bootstrap)
            np.savez(path, **{k: r[k] for k in ("loschmidt", "swap", "loschmidt_float_tie", "swap_float_tie", "loschmidt_cond_accurate", "s", "logA")})
    rows = []
    pred = (1.0 + np.abs(r["s"])) / 2.0
    for j, M in enumerate(shots):
        row = {"seed": seed, "n": n, "shots": int(M), "n_samples": n_samples}
        for sc in SCHEMES:
            for k, key in enumerate(SR.FIXED_KEYS):
                v = r[sc][j, k]
                row[f"{sc}_median_{key}"] = SR.finite_median(v)
                row[f"{sc}_nan_{key}"] = int(np.sum(~np.isfinite(v)))
            row[f"{sc}_frac_float_tie"] = float(np.mean(r[f"{sc}_float_tie"][j]))
        acc = r["loschmidt_cond_accurate"][j]
        row["loschmidt_median_cond_accurate"] = SR.finite_median(acc)
        row["loschmidt_nan_cond_accurate"] = int(np.sum(~np.isfinite(acc)))
        d_st7 = r["loschmidt"][j, 2] - acc
        row["cond_stage7_minus_accurate_max_abs"] = float(np.nanmax(np.abs(d_st7))) if np.isfinite(d_st7).any() else float("nan")
        row["cond_stage7_minus_accurate_frac_gt_1e-3"] = float(np.mean(np.abs(d_st7[np.isfinite(d_st7)]) > 1e-3)) if np.isfinite(d_st7).any() else float("nan")
        disc = acc - pred
        f = np.isfinite(disc)
        row["sign_law_median_predicted_sample"] = float(np.median(pred))
        row.update({"sign_law_disc_median": float(np.median(disc[f])), "sign_law_disc_q05": float(np.percentile(disc[f], 5)),
                    "sign_law_disc_q95": float(np.percentile(disc[f], 95)), "sign_law_disc_max_abs": float(np.max(np.abs(disc[f])))})
        rows.append(row)
    return rows


def task_vector(work: str, seed: int, cfg: B3Config) -> pd.DataFrame:
    path = _cache(Path(work), "vector", seed)
    if path.exists():
        return pickle.loads(path.read_bytes())
    df = AN.vector_reliability(cfg.vector_n, cfg.vector_shots, cfg.vector_theta, cfg.vector_replicates, seed)
    df["seed"] = seed
    path.write_bytes(pickle.dumps(df))
    return df


def task_opt(work: str, seed: int, cfg: B3Config) -> pd.DataFrame:
    path = _cache(Path(work), "opt", seed)
    if path.exists():
        return pickle.loads(path.read_bytes())
    runs, _ = AN.optimization_diagnostic(cfg.opt_n, list(Stage7Config().opt_variants), cfg.opt_starts_per_seed, cfg.opt_iters, cfg.opt_eta, seed)
    runs["master_seed"] = seed
    path.write_bytes(pickle.dumps(runs))
    return runs


def load_required(work: Path, seed: int, n: int) -> np.ndarray:
    return np.load(_cache(work, "required", seed, n))["vals"]


# =================================================================================================================
# analysis
# =================================================================================================================
FIT_RANGES = {"primary_2_20": lambda n: 2 <= n <= 20, "n_ge_8": lambda n: 8 <= n <= 20}


def fit_rows(med: pd.DataFrame, ranges: dict) -> pd.DataFrame:
    rows = []
    for (seed, sc, tag), g in med.groupby(["seed", "scheme", "target"], sort=False):
        for rname, sel in ranges.items():
            d = g[g.n.map(sel)].sort_values("n")
            f = SR.fit_series(d.n.values, d.median_log10M.values)
            rows.append({"seed": seed, "scheme": sc, "target": tag, "fit_range": rname, **f,
                         "n_samples_per_n": int(d.n_samples.iloc[0]),
                         **{f"mean_{c}": float(d[c].mean()) for c in d.columns if c.startswith("frac_")},
                         "unsolved_total": int(d.unsolved.sum())})
    return pd.DataFrame(rows)


def seed_summary(fits: pd.DataFrame, cfg: B3Config) -> pd.DataFrame:
    rows = []
    sub = fits[fits.seed.isin(cfg.seeds)]
    for (rname, sc, tag), g in sub.groupby(["fit_range", "scheme", "target"], sort=False):
        g = g.sort_values("seed")
        rows.append({"fit_range": rname, "metric": f"slope_{sc}_{tag}", "scheme": sc, "target": tag, "source": "SEED",
                     **IV.summarize(g.slope.values, cfg.n_boot_seed, cfg.boot_seed),
                     "mean_r2": float(g.r2.mean()), "min_r2": float(g.r2.min()), "mean_ols_se_diagnostic": float(g.ols_slope_se_diagnostic.mean())})
    for rname in sub.fit_range.unique():
        for tag, _, _ in SR.TARGETS:
            if tag.startswith("nz"):
                continue
            a = sub[(sub.fit_range == rname) & (sub.scheme == "loschmidt") & (sub.target == tag)].sort_values("seed")
            b = sub[(sub.fit_range == rname) & (sub.scheme == "swap") & (sub.target == tag)].sort_values("seed")
            assert list(a.seed) == list(b.seed)
            gap = IV.paired_gap(a.slope.values, b.slope.values)
            rows.append({"fit_range": rname, "metric": f"gap_swap_minus_le_{tag}", "scheme": "paired", "target": tag, "source": "SEED (paired by seed)",
                         **IV.summarize(gap, cfg.n_boot_seed, cfg.boot_seed)})
    return pd.DataFrame(rows)


def boot_slopes(meds: np.ndarray, n_values, ranges: dict) -> dict:
    """meds (B, S, len(n)) -> {range: (B, S) slopes}."""
    out = {}
    n_values = np.asarray(n_values)
    for rname, sel in ranges.items():
        m = np.array([sel(int(n)) for n in n_values])
        out[rname] = IV.ols_slopes(n_values[m], meds[:, :, m])[0]
    return out


def boot_table(slopes: dict, kind: str, point: dict | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    long, summ = [], []
    for rname, S in slopes.items():
        cols = {}
        for i, (sc, tag) in enumerate(SR.SERIES):
            cols[f"slope_{sc}_{tag}"] = S[:, i]
        for tag, _, _ in SR.TARGETS:
            if not tag.startswith("nz"):
                cols[f"gap_swap_minus_le_{tag}"] = S[:, SR.SERIES.index(("swap", tag))] - S[:, SR.SERIES.index(("loschmidt", tag))]
        df = pd.DataFrame(cols)
        df.insert(0, "replicate", np.arange(len(df)))
        df.insert(0, "fit_range", rname)
        df.insert(0, "kind", kind)
        long.append(df)
        for k, v in cols.items():
            lo, hi = IV.percentile_interval(v)
            summ.append({"kind": kind, "fit_range": rname, "metric": k, "point_estimate": (point or {}).get((rname, k), np.nan),
                         "boot_median": float(np.median(v)), "pct_lo": lo, "pct_hi": hi, "boot_se": float(np.std(v, ddof=1)), "replicates": int(v.size)})
    return pd.concat(long, ignore_index=True), pd.DataFrame(summ)


def stage7_point_estimates() -> dict:
    fits = json.loads((STAGE7_DIR / "scaling_fits.json").read_text())["fits"]
    out = {}
    for k, f in fits.items():
        sc, tag = k.split("_", 1)
        out[("primary_2_20", f"slope_{sc}_{tag}")] = f["slope"]
        if f.get("slope_n_ge_8") is not None:
            out[("n_ge_8", f"slope_{sc}_{tag}")] = f["slope_n_ge_8"]
    for rname in ("primary_2_20", "n_ge_8"):
        for tag in ("snr1", "snr2", "dir0.75", "dir0.9"):
            a, b = out.get((rname, f"slope_loschmidt_{tag}")), out.get((rname, f"slope_swap_{tag}"))
            if a is not None and b is not None:
                out[(rname, f"gap_swap_minus_le_{tag}")] = b - a
    return out


def interval_check(st7: dict, seed_sum: pd.DataFrame, theta_sum: pd.DataFrame, fits: pd.DataFrame, cfg: B3Config) -> pd.DataFrame:
    rows = []
    for (rname, metric), v in st7.items():
        if metric == "slope_swap_nz0.9" and rname != "primary_2_20":
            continue   # flat (~1e-17) by construction for n >= 8: SWAP P_nonzero depends on M only; no reference
        s = seed_sum[(seed_sum.fit_range == rname) & (seed_sum.metric == metric)]
        t = theta_sum[(theta_sum.fit_range == rname) & (theta_sum.metric == metric)]
        if s.empty or t.empty:
            continue
        s, t = s.iloc[0], t.iloc[0]
        sd_100k = s["sd"] * np.sqrt(cfg.seed_samples / cfg.reference_samples)   # slope SD rescaled to Stage 7's 100k theta
        rows.append({"fit_range": rname, "metric": metric, "stage7_estimate": v,
                     "seed_pct_lo": s.pct_lo, "seed_pct_hi": s.pct_hi, "inside_seed_pct_interval": bool(s.pct_lo <= v <= s.pct_hi),
                     "seed_mean": s["mean"], "seed_mean_ci_lo": s.boot_lo, "seed_mean_ci_hi": s.boot_hi,
                     "inside_seed_mean_ci": bool(s.boot_lo <= v <= s.boot_hi),
                     "z_vs_seed_mean_sd_rescaled_to_100k_DIAGNOSTIC": float((v - s["mean"]) / np.sqrt(sd_100k**2 + s.boot_se**2)),
                     "theta_lo": t.pct_lo, "theta_hi": t.pct_hi, "inside_theta_ci": bool(t.pct_lo <= v <= t.pct_hi),
                     "theta_reference_is_stage7_population": True})
    df = pd.DataFrame(rows)
    # headline ranges (docs/stages/STAGE7.md / handoff): LE 0.600-0.607 over the 5 LE targets, SWAP 1.197-1.203 over 4 SWAP targets
    for sc, tags, label in (("loschmidt", ("snr1", "snr2", "dir0.75", "dir0.9", "nz0.9"), "LE headline range 0.600-0.607"),
                            ("swap", ("snr1", "snr2", "dir0.75", "dir0.9"), "SWAP headline range 1.197-1.203")):
        d = df[(df.fit_range == "primary_2_20") & df.metric.isin([f"slope_{sc}_{t}" for t in tags])]
        rows.append({"fit_range": "primary_2_20", "metric": label, "stage7_estimate": f"{d.stage7_estimate.min():.4f}-{d.stage7_estimate.max():.4f}",
                     "seed_pct_lo": d.seed_pct_lo.min(), "seed_pct_hi": d.seed_pct_hi.max(),
                     "inside_seed_pct_interval": bool(d.inside_seed_pct_interval.all()),
                     "seed_mean": np.nan, "seed_mean_ci_lo": d.seed_mean_ci_lo.min(), "seed_mean_ci_hi": d.seed_mean_ci_hi.max(),
                     "inside_seed_mean_ci": bool(d.inside_seed_mean_ci.all()),
                     "theta_lo": d.theta_lo.min(), "theta_hi": d.theta_hi.max(), "inside_theta_ci": bool(d.inside_theta_ci.all()),
                     "theta_reference_is_stage7_population": True,
                     "note": "envelope over targets; inside_* = every target inside its own interval"})
    return pd.DataFrame(rows)


def fixed_summary(seed_rows: pd.DataFrame, ref_rows: pd.DataFrame, ref_boot: dict, cfg: B3Config) -> pd.DataFrame:
    st7 = pd.read_csv(STAGE7_DIR / "paired_estimator_comparison.csv")
    rows = []
    quantities = [(sc, key) for sc in SCHEMES for key in SR.FIXED_KEYS] + [("loschmidt", "cond_accurate")]
    for (n, M), g in seed_rows.groupby(["n", "shots"]):
        ref = ref_rows[(ref_rows.n == n) & (ref_rows.shots == M)].iloc[0]
        for sc, key in quantities:
            col = f"{sc}_median_{key}"
            b = ref_boot[(n, M)][col]
            lo, hi = IV.percentile_interval(b)
            ss = IV.summarize(g.sort_values("seed")[col].values, cfg.n_boot_seed, cfg.boot_seed)
            s7 = st7[(st7.n == n) & (st7.shots == M)]
            rows.append({"n": n, "shots": M, "scheme": sc, "quantity": key, "reference_median": ref[col],
                         "THETA_lo": lo, "THETA_hi": hi, "THETA_se": float(np.std(b, ddof=1)),
                         "SEED_mean": ss["mean"], "SEED_median": ss["median"], "SEED_pct_lo": ss["pct_lo"], "SEED_pct_hi": ss["pct_hi"],
                         "SEED_mean_ci_lo": ss["boot_lo"], "SEED_mean_ci_hi": ss["boot_hi"],
                         "stage7_value": float(s7[col].iloc[0]) if (not s7.empty and col in s7) else np.nan,
                         "reference_nan_rows": int(ref.get(f"{sc}_nan_{key}", 0)) if key != "cond_accurate" else int(ref["loschmidt_nan_cond_accurate"]),
                         "reference_frac_float_tie": ref[f"{sc}_frac_float_tie"], "seed_max_frac_float_tie": float(g[f"{sc}_frac_float_tie"].max())})
    return pd.DataFrame(rows)


def mc_validation(cfg: B3Config, ref_seed: int) -> pd.DataFrame:
    """Finite-shot Monte Carlo of the exact probabilities at the extended M / n (binomial draws, Wilson CIs).
    This uncertainty is about the MC replicate count only and is never mixed with theta or seed intervals."""
    rows = []
    for n in cfg.mc_n:
        th = AN.sample_theta(n, 400, ref_seed, 95)
        from qlo.stage5.theory import log_a_k, s_k
        logA, s = log_a_k(th, 0), s_k(th, 0)
        i = int(np.argmin(np.abs(logA - np.median(logA))))   # median-A theta
        A, sv = float(np.exp(logA[i])), float(s[i])
        for M in cfg.mc_shots:
            for si, sc in enumerate(SCHEMES):
                p_pos, p_neg, _ = pair(sc, A, sv)
                ex = direction_probabilities(p_pos, p_neg, float(M))
                rng = np.random.default_rng(np.random.SeedSequence([0xB3, 95, n, M, si]))
                D = rng.binomial(M, p_pos, cfg.mc_reps) - rng.binomial(M, p_neg, cfg.mc_reps)
                kz, kc = int(np.sum(D == 0)), int(np.sum(np.sign(D) == np.sign(p_pos - p_neg)))
                lz, hz = wilson_ci(kz, cfg.mc_reps)
                lc, hc = wilson_ci(kc, cfg.mc_reps)
                rows.append({"n": n, "shots": M, "scheme": sc, "A": A, "s": sv, "reps": cfg.mc_reps,
                             "p_zero_exact": float(ex["p_zero"]), "p_zero_mc": kz / cfg.mc_reps, "p_zero_wilson_lo": lz, "p_zero_wilson_hi": hz,
                             "p_zero_in_wilson": bool(lz <= float(ex["p_zero"]) <= hz),
                             "p_correct_exact": float(ex["p_correct"]), "p_correct_mc": kc / cfg.mc_reps, "p_correct_wilson_lo": lc,
                             "p_correct_wilson_hi": hc, "p_correct_in_wilson": bool(lc <= float(ex["p_correct"]) <= hc),
                             "float_tie": bool(p_pos == p_neg)})
    return pd.DataFrame(rows)


VEC_METRICS = ("p_vector_zero", "median_cos", "median_cos_given_nonzero", "p_dot_gt_0", "mean_frac_component_signs_correct",
               "median_log10_norm_ratio", "mean_frac_components_zero")


def vector_summary(vec: pd.DataFrame, cfg: B3Config) -> pd.DataFrame:
    st7 = pd.read_csv(STAGE7_DIR / "vector_reliability.csv")
    rows = []
    for (n, M, sc), g in vec.groupby(["n", "shots", "scheme"]):
        s7 = st7[(st7.n == n) & (st7.shots == M) & (st7.scheme == sc)]
        for m in VEC_METRICS:
            ss = IV.summarize(g.sort_values("seed")[m].values, cfg.n_boot_seed, cfg.boot_seed)
            v7 = float(s7[m].iloc[0]) if not s7.empty else np.nan
            rows.append({"n": n, "shots": M, "scheme": sc, "metric": m, "source": "SEED (theta and shot noise both fresh per seed)",
                         **ss, "stage7_value": v7, "stage7_inside_seed_pct": bool(ss["pct_lo"] <= v7 <= ss["pct_hi"]) if np.isfinite(v7) else None})
    return pd.DataFrame(rows)


RW_COMPARISONS = (("SWAP M=64", "SWAP-noise random walk M=64"), ("SWAP M=1024", "SWAP-noise random walk M=1024"),
                  ("SWAP M=64", "exact"), ("SWAP M=1024", "exact"), ("LE M=64", "exact"), ("LE M=1024", "exact"),
                  ("SWAP-noise random walk M=64", "exact"), ("SWAP-noise random walk M=1024", "exact"))


def _pair_stats(x: pd.DataFrame, y: pd.DataFrame) -> dict:
    x, y = x.set_index("seed"), y.set_index("seed")
    assert np.allclose(x.F0.values, y.F0.values, rtol=0, atol=0), "paired arms must start from identical theta"
    lx, ly = np.log10(np.maximum(x.F_final, 1e-300)), np.log10(np.maximum(y.F_final, 1e-300))
    return {"median_dlog10_F_final": float(np.median(lx - ly)), "mean_dlog10_F_final": float(np.mean(lx - ly)),
            "median_dlog10_gain_best": float(np.median(x.log10_gain_best - y.log10_gain_best)),
            "p_x_final_better": float(np.mean(x.F_final > y.F_final + 1e-9)), "p_x_final_worse": float(np.mean(x.F_final < y.F_final - 1e-9)),
            "p_x_gain_best_higher": float(np.mean(x.log10_gain_best > y.log10_gain_best + 1e-12)),
            "dP_F_final_ge_0.5": float(np.mean(x.F_final >= 0.5) - np.mean(y.F_final >= 0.5))}


def random_walk_summary(runs: pd.DataFrame, cfg: B3Config) -> pd.DataFrame:
    rows = []
    for n in cfg.opt_n:
        r = runs[runs.n == n]
        # per-variant direction / alignment statistics
        for v, g in r.groupby("variant", sort=False):
            per_seed = g.groupby("master_seed").agg(mean_frac_wrong=("frac_wrong_iters", "mean"), mean_frac_zero=("frac_zero_iters", "mean"),
                                                    mean_cos=("mean_cos_nonzero", "mean"), p_final_ge_half=("F_final", lambda f: float(np.mean(f >= 0.5))),
                                                    median_log10_gain_best=("log10_gain_best", "median"))
            for m in per_seed.columns:
                rows.append({"n": n, "comparison": v, "metric": m, "source": "SEED", **IV.summarize(per_seed[m].values, cfg.n_boot_seed, cfg.boot_seed)})
        # paired comparisons: identical theta0 per (master seed, start) in every arm (asserted)
        for xv, yv in RW_COMPARISONS:
            per = []
            for ms in cfg.seeds:
                x, y = r[(r.variant == xv) & (r.master_seed == ms)], r[(r.variant == yv) & (r.master_seed == ms)]
                per.append(_pair_stats(x, y))
            per = pd.DataFrame(per)
            pooled_x, pooled_y = r[r.variant == xv].sort_values(["master_seed", "seed"]), r[r.variant == yv].sort_values(["master_seed", "seed"])
            assert np.array_equal(pooled_x.F0.values, pooled_y.F0.values)
            lx, ly = np.log10(np.maximum(pooled_x.F_final.values, 1e-300)), np.log10(np.maximum(pooled_y.F_final.values, 1e-300))
            dl = lx - ly
            better = (pooled_x.F_final.values > pooled_y.F_final.values + 1e-9).astype(float)
            rng = np.random.default_rng(np.random.SeedSequence([0xB3, 70, n, RW_COMPARISONS.index((xv, yv))]))
            idx = rng.integers(0, dl.size, (cfg.n_boot, dl.size))
            for m in per.columns:
                rows.append({"n": n, "comparison": f"{xv} vs {yv}", "metric": m, "source": "SEED", **IV.summarize(per[m].values, cfg.n_boot_seed, cfg.boot_seed)})
            for m, vals, stat in (("median_dlog10_F_final", dl, np.median), ("p_x_final_better", better, np.mean)):
                b = np.array([stat(vals[i]) for i in idx])
                lo, hi = IV.percentile_interval(b)
                rows.append({"n": n, "comparison": f"{xv} vs {yv}", "metric": m, "source": "START-BOOTSTRAP (pooled paired starts)",
                             "n_units": int(dl.size), "mean": float(stat(vals)), "pct_lo": lo, "pct_hi": hi, "boot_se": float(b.std(ddof=1))})
    return pd.DataFrame(rows)


def random_walk_stratified(runs: pd.DataFrame, cfg: B3Config, n_values=(10, 12)) -> pd.DataFrame:
    """POST-HOC diagnostic (added after the pooled SWAP-vs-random-walk difference was seen; not a predeclared test).
    Strata of the starting fidelity F0 over all paired starts: below median, median..90th percentile, top 10%.
    Intervals: START-BOOTSTRAP (2000 resamples of starts within the stratum)."""
    rows = []
    for n in n_values:
        r = runs[runs.n == n]
        ex = r[r.variant == "exact"].sort_values(["master_seed", "seed"])
        lab = np.digitize(ex.F0.values, np.quantile(ex.F0, [0.5, 0.9]))
        for M in (64, 1024):
            arms = {"exact": ex, "SWAP": r[r.variant == f"SWAP M={M}"].sort_values(["master_seed", "seed"]),
                    "random walk": r[r.variant == f"SWAP-noise random walk M={M}"].sort_values(["master_seed", "seed"])}
            for d in arms.values():
                assert np.array_equal(d.F0.values, ex.F0.values), "paired arms must start from identical theta"
            for k, name in enumerate(("F0 < median", "median <= F0 < q90", "F0 >= q90")):
                m = lab == k
                rng = np.random.default_rng(np.random.SeedSequence([0xB3, 71, n, M, k]))
                idx = rng.integers(0, int(m.sum()), (cfg.n_boot, int(m.sum())))
                for arm, d in arms.items():
                    row = {"n": n, "shots": M, "stratum": name, "starts": int(m.sum()), "arm": arm,
                           "median_log10_F0": float(np.median(np.log10(d.F0.values[m])))}
                    for key, v in (("p_F_final_ge_0.5", (d.F_final.values[m] >= 0.5).astype(float)), ("mean_cos", d.mean_cos_nonzero.values[m]),
                                   ("frac_wrong", d.frac_wrong_iters.values[m])):
                        lo, hi = IV.percentile_interval(v[idx].mean(axis=1))
                        row.update({key: float(v.mean()), f"{key}_lo": lo, f"{key}_hi": hi})
                    rows.append(row)
    return pd.DataFrame(rows)


def nonmonotone_rows(checks: pd.DataFrame, work: Path) -> pd.DataFrame:
    """For every (seed, n) whose LE inversion check failed: scan ALL exact LE direction rows for P_correct(M(1-1e-5)) >= q,
    and measure the overshoot of the returned M against the first budget meeting q on a 3000-point grid in [0.97M, M]."""
    rows = []
    for _, b in checks[~checks.accepted].iterrows():
        z = np.load(_cache(work, "required", int(b.seed), int(b.n)))
        A, s = np.exp(z["logA"]), z["s"]
        for tag, q in (("dir0.75", 0.75), ("dir0.9", 0.90)):
            i = SR.SERIES.index(("loschmidt", tag))
            ex = np.flatnonzero(z["meth"][i] == 1)
            M = np.round(np.power(10.0, z["vals"][i][ex]))
            pp, pn, _ = pair("loschmidt", A[ex], s[ex])
            below = direction_probabilities(pp, pn, np.floor(M * (1 - NUM.INV_REL_TOL)))["p_correct"]
            for j in np.flatnonzero((below >= q) & (M > 2)):
                grid = np.unique(np.round(np.linspace(M[j] * 0.97, M[j], 3000)))
                pc = direction_probabilities(pp[j], pn[j], grid)["p_correct"]
                rows.append({"n": int(b.n), "seed": int(b.seed), "target": tag, "exact_rows_in_point": int(ex.size), "M_returned": float(M[j]),
                             "log10_overshoot_vs_first_grid_M": float(np.log10(M[j] / grid[np.argmax(pc >= q)])),
                             "max_nonmonotone_drop_in_P": float(np.max(np.maximum(pc[:-1] - pc[1:], 0.0))),
                             "M_times_A": float(M[j] * A[ex][j]), "abs_s": float(abs(s[ex][j]))})
    return pd.DataFrame(rows)


def interval_diagnostics(cfg: B3Config) -> dict:
    """(1) Calibration: probability that ONE fresh exchangeable replicate falls outside the 2.5-97.5% percentile interval
    of len(seeds) others (Monte Carlo, normal draws; the result is distribution-free for continuous data).
    (2) Where the Stage 7 vector-reliability theta draw (seed 0, 400 theta) ranks among the B3 seeds in mean log F."""
    rng = np.random.default_rng(np.random.SeedSequence([0xB3, 80]))
    k = len(cfg.seeds)
    x = rng.normal(size=(200_000, k + 1))
    lo, hi = np.percentile(x[:, :k], [2.5, 97.5], axis=1)
    miss = float(np.mean((x[:, k] < lo) | (x[:, k] > hi)))
    rank = {}
    for n in cfg.vector_n:
        f = lambda sd: float(np.mean(np.sum(np.log(np.cos(AN.sample_theta(n, cfg.vector_theta, sd, 60) / 2.0) ** 2), axis=1)))
        v0, vs = f(SR.STAGE7_SEED), np.array([f(sd) for sd in cfg.seeds])
        rank[str(n)] = {"stage7_mean_logF": v0, "seed_min": float(vs.min()), "seed_max": float(vs.max()), "rank_of_stage7_among_all": int((vs < v0).sum()) + 1,
                        "out_of": int(len(vs) + 1)}
    return {"percentile_interval_miss_rate_for_one_fresh_replicate": miss, "n_seeds": k, "stage7_vector_theta_rank": rank}


# =================================================================================================================
def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--fast", action="store_true")
    p.add_argument("--skip-hierarchical", action="store_true")
    a = p.parse_args(argv)
    cfg = B3Config()
    if a.fast:
        cfg = replace(cfg, seeds=SR.B3_SEEDS[:4], seed_samples=800, reference_samples=1500, n_boot=60, n_boot_hier=40, n_boot_seed=500,
                      fixed_seed_samples=300, fixed_reference_samples=600, fixed_n_boot=60, mc_reps=2000, vector_theta=40,
                      vector_replicates=4, opt_starts_per_seed=6, opt_iters=60)
    SR.check_seeds(cfg.seeds)
    out, work = a.out_dir, a.work_dir
    out.mkdir(parents=True, exist_ok=True)
    (out / "figures").mkdir(exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    (out / "config.json").write_text(json.dumps({**asdict(cfg), "work_dir": str(work), "stage7_seed_excluded": SR.STAGE7_SEED,
                                                 "theta_streams": {"required_shots": SR.REQ_STREAM, "fixed_shots": SR.FIXED_STREAM},
                                                 "sign_law_fixed_prediction": SIGN_LAW_MEDIAN, "baseline_commit": "ba51866"}, indent=2, default=str))
    all_n = tuple(cfg.primary_n) + tuple(cfg.extension_n)
    t0 = time.time()

    # ---- 1. compute (parallel, cached) -------------------------------------------------------------------------
    jobs = [(cfg.reference_seed, n, cfg.reference_samples) for n in all_n] + [(sd, n, cfg.seed_samples) for sd in cfg.seeds for n in all_n]
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        fr = {pool.submit(task_required, str(work), sd, n, N): (sd, n) for sd, n, N in jobs}
        ff = {pool.submit(task_fixed, str(work), sd, n, cfg.fixed_shots, cfg.fixed_reference_samples if sd == cfg.reference_seed else cfg.fixed_seed_samples,
                          sd == cfg.reference_seed): (sd, n)
              for sd in (cfg.reference_seed,) + tuple(cfg.seeds) for n in cfg.fixed_n}
        fv = {pool.submit(task_vector, str(work), sd, cfg): sd for sd in cfg.seeds}
        fo = {pool.submit(task_opt, str(work), sd, cfg): sd for sd in cfg.seeds}
        req = []
        for i, f in enumerate(fr):
            req.append(f.result())
            if (i + 1) % 12 == 0:
                print(f"required shots: {i + 1}/{len(fr)} ({time.time() - t0:.0f}s)", flush=True)
        fixed_rows = [r for f in ff for r in f.result()]
        vec = pd.concat([f.result() for f in fv], ignore_index=True)
        runs = pd.concat([f.result() for f in fo], ignore_index=True)
    print(f"compute done ({time.time() - t0:.0f}s)", flush=True)

    med = pd.DataFrame([r for x in req for r in x["rows"]])
    checks = pd.DataFrame([x["check"] for x in req])
    med.to_csv(out / "seed_medians.csv", index=False)

    # ---- 2. Stage 7 reproduction on the regenerated reference population ------------------------------------------
    st7_sum = pd.read_csv(STAGE7_DIR / "scaling_summary.csv")
    rep = []
    for _, r in med[med.seed == cfg.reference_seed].iterrows():
        s = st7_sum[(st7_sum.n == r.n) & (st7_sum.scheme == r.scheme)]
        if not s.empty:
            rep.append({"n": r.n, "scheme": r.scheme, "target": r.target, "b3": r.median_log10M,
                        "stage7": float(s[f"{r.target}_log10M_median"].iloc[0])})
    rep = pd.DataFrame(rep)
    rep["abs_diff"] = (rep.b3 - rep.stage7).abs()
    reproduction = {"max_abs_diff_median_log10M": float(rep.abs_diff.max()), "cells": int(len(rep)),
                    "exact": bool(rep.abs_diff.max() <= 1e-12) if not a.fast else None}

    # ---- 3. n extension acceptance ------------------------------------------------------------------------------------
    handover = NUM.swap_normal_handover_check()
    ext_ok = {}
    for n in cfg.extension_n:
        c = checks[checks.n == n]
        ext_ok[n] = bool(c.accepted.all() and handover["passed"])
    checks.to_csv(out / "numerical_checks.csv", index=False)
    accepted_ext = tuple(n for n in cfg.extension_n if ext_ok[n])
    ranges = dict(FIT_RANGES)
    if accepted_ext:
        ranges["extended_2_" + str(max(accepted_ext))] = lambda n, _acc=accepted_ext: 2 <= n <= 20 or n in _acc
    (out / "numerical_extension.json").write_text(json.dumps({"swap_normal_handover": handover, "extension_accepted": {str(k): v for k, v in ext_ok.items()},
                                                             "primary_fit_range": "2..20 (unchanged, Stage 7 range)",
                                                             "per_point_failures": checks[~checks.accepted].to_dict("records")}, indent=2, default=float))

    # ---- 4. seed-level fits and summaries ---------------------------------------------------------------------------
    fits = fit_rows(med, ranges)
    fits[fits.seed.isin(cfg.seeds)].to_csv(out / "seed_slopes.csv", index=False)
    ssum = seed_summary(fits, cfg)
    ssum.to_csv(out / "seed_summary.csv", index=False)

    # ---- 5. theta bootstrap (reference) and two-level bootstrap --------------------------------------------------------
    ref_pop = {n: load_required(work, cfg.reference_seed, n) for n in all_n}
    fit_n = [n for n in all_n if any(sel(n) for sel in ranges.values())]
    meds = BS.theta_bootstrap(ref_pop, fit_n, cfg.n_boot, cfg.boot_seed)
    ref_fit = fits[fits.seed == cfg.reference_seed]
    point = {(r.fit_range, f"slope_{r.scheme}_{r.target}"): r.slope for r in ref_fit.itertuples()}
    for rname in ranges:
        for tag, _, _ in SR.TARGETS:
            if not tag.startswith("nz"):
                point[(rname, f"gap_swap_minus_le_{tag}")] = point[(rname, f"slope_swap_{tag}")] - point[(rname, f"slope_loschmidt_{tag}")]
    tlong, tsum = boot_table(boot_slopes(meds, fit_n, ranges), "THETA-BOOTSTRAP (reference = regenerated Stage 7 population)", point)
    longs, sums = [tlong], [tsum]
    print(f"theta bootstrap done ({time.time() - t0:.0f}s)", flush=True)
    if not a.skip_hierarchical:
        hpath = work / f"hierarchical_B{cfg.n_boot_hier}_S{len(cfg.seeds)}_N{cfg.seed_samples}_seed{cfg.boot_seed}.npy"
        if hpath.exists():
            H = np.load(hpath)
        else:
            pops = {sd: {n: load_required(work, sd, n) for n in cfg.primary_n} for sd in cfg.seeds}
            H = BS.hierarchical_bootstrap(pops, cfg.seeds, cfg.primary_n, cfg.n_boot_hier, cfg.boot_seed)
            np.save(hpath, H)
            del pops
        hlong, hsum = boot_table({"primary_2_20": H}, "HIERARCHICAL (seeds, then theta within seed; mean slope over seeds)")
        longs.append(hlong); sums.append(hsum)
        print(f"hierarchical bootstrap done ({time.time() - t0:.0f}s)", flush=True)
    pd.concat(longs, ignore_index=True).to_csv(out / "theta_bootstrap_slopes.csv.gz", index=False, float_format="%.6g")
    bsum = pd.concat(sums, ignore_index=True)
    bsum.to_csv(out / "bootstrap_summary.csv", index=False)
    theta_sum = tsum

    # ---- 6. Stage 7 interval check --------------------------------------------------------------------------------------
    chk = interval_check(stage7_point_estimates(), ssum, theta_sum, fits, cfg)
    chk.to_csv(out / "stage7_interval_check.csv", index=False)

    # ---- 7. fixed-shot probabilities and sign law ----------------------------------------------------------------------
    fx = pd.DataFrame(fixed_rows)
    fx.to_csv(out / "fixed_shot_per_seed.csv", index=False)
    ref_fx = fx[fx.seed == cfg.reference_seed]
    seed_fx = fx[fx.seed.isin(cfg.seeds)]
    ref_boot = {}
    for n in cfg.fixed_n:
        z = np.load(_cache(work, "fixed", cfg.reference_seed, n))
        for j, M in enumerate(cfg.fixed_shots):
            arrs = {f"{sc}_median_{key}": z[sc][j, k][None, :] for sc in SCHEMES for k, key in enumerate(SR.FIXED_KEYS)}
            arrs["loschmidt_median_cond_accurate"] = z["loschmidt_cond_accurate"][j][None, :]
            b = BS.bootstrap_fixed_medians(arrs, cfg.fixed_n_boot, cfg.boot_seed + 1000 * n + j)
            ref_boot[(n, M)] = {k: v[:, 0] for k, v in b.items()}
    fsum = fixed_summary(seed_fx, ref_fx, ref_boot, cfg)
    fsum.to_csv(out / "fixed_shot_summary.csv", index=False)
    mc = mc_validation(cfg, cfg.reference_seed)
    mc.to_csv(out / "mc_validation.csv", index=False)

    sl = []
    for n in cfg.sign_law_n:
        for M in cfg.fixed_shots:
            r = ref_fx[(ref_fx.n == n) & (ref_fx.shots == M)].iloc[0]
            g = seed_fx[(seed_fx.n == n) & (seed_fx.shots == M)].sort_values("seed")
            ss = IV.summarize(g.loschmidt_median_cond_accurate.values, cfg.n_boot_seed, cfg.boot_seed)
            tb = ref_boot[(n, M)]["loschmidt_median_cond_accurate"]
            tlo, thi = IV.percentile_interval(tb)
            deep = bool(r.loschmidt_median_p_zero >= cfg.sign_law_deep_p_zero)
            sl.append({"n": n, "shots": M, "reference_median_le_p_zero": r.loschmidt_median_p_zero, "deep_regime": deep,
                       "prediction_fixed": SIGN_LAW_MEDIAN, "reference_sample_median_of_prediction": r.sign_law_median_predicted_sample,
                       "reference_observed_median_accurate": r.loschmidt_median_cond_accurate,
                       "reference_observed_median_stage7_method": r.loschmidt_median_p_correct_given_nonzero,
                       "reference_stage7_method_nan_rows": int(r.loschmidt_nan_p_correct_given_nonzero),
                       "reference_stage7_method_max_abs_err": r["cond_stage7_minus_accurate_max_abs"],
                       "reference_stage7_method_frac_err_gt_1e-3": r["cond_stage7_minus_accurate_frac_gt_1e-3"],
                       "THETA_lo": tlo, "THETA_hi": thi, "prediction_inside_THETA": bool(tlo <= SIGN_LAW_MEDIAN <= thi),
                       "SEED_mean": ss["mean"], "SEED_sd": ss["sd"], "SEED_pct_lo": ss["pct_lo"], "SEED_pct_hi": ss["pct_hi"],
                       "SEED_mean_ci_lo": ss["boot_lo"], "SEED_mean_ci_hi": ss["boot_hi"],
                       "prediction_inside_SEED_pct": bool(ss["pct_lo"] <= SIGN_LAW_MEDIAN <= ss["pct_hi"]),
                       "prediction_inside_SEED_mean_ci": bool(ss["boot_lo"] <= SIGN_LAW_MEDIAN <= ss["boot_hi"]),
                       "per_theta_disc_median": r.sign_law_disc_median, "per_theta_disc_q05": r.sign_law_disc_q05,
                       "per_theta_disc_q95": r.sign_law_disc_q95, "per_theta_disc_max_abs": r.sign_law_disc_max_abs,
                       "seed_max_per_theta_disc_max_abs": float(g.sign_law_disc_max_abs.max())})
    sl = pd.DataFrame(sl)
    sl.to_csv(out / "sign_law_summary.csv", index=False)

    # ---- 8. vectors, random walk ----------------------------------------------------------------------------------------
    vec.to_csv(out / "vector_per_seed.csv", index=False)
    vsum = vector_summary(vec, cfg)
    vsum.to_csv(out / "vector_summary.csv", index=False)
    rw = random_walk_summary(runs, cfg)
    rw.to_csv(out / "random_walk_summary.csv", index=False)
    random_walk_stratified(runs, cfg).to_csv(out / "random_walk_stratified_posthoc.csv", index=False)
    nonmonotone_rows(checks, work).to_csv(out / "numerical_nonmonotone_rows.csv", index=False)
    (out / "interval_diagnostics.json").write_text(json.dumps(interval_diagnostics(cfg), indent=2))

    (out / "run_meta.json").write_text(json.dumps({"stage7_reproduction": reproduction, "extension_accepted": {str(k): v for k, v in ext_ok.items()},
                                                   "fit_ranges": list(ranges), "wall_seconds": time.time() - t0}, indent=2, default=float))

    # ---- 9. figures ----------------------------------------------------------------------------------------------------
    fig = out / "figures"
    for f in (FIG.slope_seed_distribution(fits[fits.seed.isin(cfg.seeds)], fig / "slope_seed_distribution.png"),
              FIG.slope_confidence_intervals(chk, fig / "slope_confidence_intervals.png"),
              FIG.exponent_gap(fits[fits.seed.isin(cfg.seeds)], ssum, tsum, stage7_point_estimates(), fig / "exponent_gap.png"),
              FIG.required_shots_with_intervals(med, cfg.seeds, cfg.reference_seed, meds, fit_n, fig / "required_shots_with_intervals.png"),
              FIG.zero_probability_with_intervals(fsum, fig / "zero_probability_with_intervals.png"),
              FIG.directional_correctness_with_intervals(fsum, fig / "directional_correctness_with_intervals.png"),
              FIG.vector_alignment_with_intervals(vsum, fig / "vector_alignment_with_intervals.png"),
              FIG.conditional_sign_validation(sl, fig / "conditional_sign_validation.png")):
        print("figure:", f)

    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.float_format", "{:.5g}".format)
    print("== Stage 7 reproduction ==", reproduction)
    print("== extension ==", ext_ok)
    print("== seed summary ==\n", ssum[["fit_range", "metric", "mean", "sd", "median", "pct_lo", "pct_hi", "boot_lo", "boot_hi"]].to_string(index=False))
    print("== bootstrap summary ==\n", bsum[["kind", "fit_range", "metric", "point_estimate", "boot_median", "pct_lo", "pct_hi", "boot_se"]].to_string(index=False))
    print("== Stage 7 interval check ==\n", chk.to_string(index=False))
    print(f"total {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
