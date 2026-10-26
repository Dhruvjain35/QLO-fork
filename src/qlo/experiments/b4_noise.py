"""B4: depolarizing-noise overlay on the Stage 7 RX product and every B1 entangling cell.

    python -m qlo.experiments.b4_noise                    # all phases -> results/b4_noise/
    python -m qlo.experiments.b4_noise --b1-work DIR      # B1 per-theta caches (default: external SSD)

Phases: validate (density-matrix checks) -> rx (global + local noise on the RX product) -> ent (global noise on the
B1 cells, from the B1 per-theta F_pm caches) -> analyse (p = 0 regression vs B1, identity, fits, predictions,
transition profile) -> figures. The configuration is frozen in docs/b4/B4_CONFIG.md (checked at start).
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from qlo.b1 import config as B1CF
from qlo.b1 import fits as FT
from qlo.b1 import quantities as Q
from qlo.b4 import config as CF
from qlo.b4 import noise as N
from qlo.hardening import intervals as IV
from qlo.stage6.analysis import linear_fit

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results" / "b4_noise"
B1_RESULTS = ROOT / "results" / "b1_entangling"
DEFAULT_B1_WORK = Path("/Volumes/SSD Disk  1TB/qlo-b1-work")
LOG2 = float(np.log10(2.0))
KEYS = ["model", "p", "family", "regime", "position"]


class Stop(SystemExit):
    """A predeclared STOP condition (failed validation or regression)."""


def log(msg: str) -> None:
    print(msg, flush=True)
    with open(OUT / "numerics_log.md", "a") as f:
        f.write(msg + "\n")


def layers(family: str, regime: str, n: int) -> int:
    return 1 if family == "rx_product" else B1CF.depth_of(regime, n)


def _rows(q: dict, meta: dict, cfg) -> tuple[dict, dict]:
    return {**meta, **Q.cell_diagnostics(q)}, {**meta, **Q.identity_check(q)}


# =================================================================================================================
def phase_validate(cfg) -> None:
    rng = np.random.default_rng(np.random.SeedSequence([0xB4, 1]))
    rows = []
    for n in cfg.validate_n:
        for p in cfg.global_p[1:]:
            for _ in range(cfg.validate_theta):
                th = rng.uniform(-np.pi, np.pi, n)
                F = float(np.prod(np.cos(th / 2) ** 2))
                pred = N.global_overlay(F, F, n, N.global_q(p, 1))[0]
                rows.append({"check": "global_rx", "n": n, "p": p, "density_matrix": N.dm_rx_global(th, p), "overlay": float(pred)})
                par = rng.uniform(-np.pi, np.pi, (2, n, 2))
                pred = N.global_overlay(N.pure_hea_fidelity(par), 0.0, n, N.global_q(p, 2))[0]
                rows.append({"check": "global_hea_depth2", "n": n, "p": p, "density_matrix": N.dm_hea_global(par, p), "overlay": float(pred)})
    for n in cfg.validate_local_n:
        for p in cfg.local_p_rx[1:]:
            for _ in range(cfg.validate_theta):
                th = rng.uniform(-np.pi, np.pi, (1, n))
                fp, fm = N.rx_local(th, p)
                for sh, val in ((np.pi / 2, fp[0]), (-np.pi / 2, fm[0])):
                    t = th[0].copy()
                    t[0] += sh
                    rows.append({"check": "local_rx_shifted", "n": n, "p": p, "density_matrix": N.dm_rx_local(t, p), "overlay": float(val)})
    df = pd.DataFrame(rows)
    df["abs_err"] = (df.density_matrix - df.overlay).abs()
    df.to_csv(OUT / "validation.csv", index=False)
    log(f"validate: {len(df)} density-matrix checks, max |error| = {df.abs_err.max():.2e} "
        f"(global {df[df.check != 'local_rx_shifted'].abs_err.max():.2e}, local {df[df.check == 'local_rx_shifted'].abs_err.max():.2e})")
    if df.abs_err.max() > cfg.validate_tol:
        raise Stop("STOP: noise overlay disagrees with density-matrix simulation")


# =================================================================================================================
def phase_rx(cfg) -> tuple[list, list]:
    med, ident = [], []
    for sd in cfg.seeds:
        for n in cfg.rx_n:
            th, fp0, fm0 = N.rx_noiseless(n, cfg.rx_samples, sd, cfg.rx_stream)
            for p in cfg.global_p:
                qq = N.global_q(p, 1)
                fp, fm = N.global_overlay(fp0, fm0, n, qq)
                q = Q.per_theta(fp, fm, cfg.rho, delta=N.global_delta(fp0, fm0, qq) if p > 0 else None)
                a, b = _rows(q, {"model": "global", "p": p, "family": "rx_product", "regime": "product", "position": "k=0", "n": n, "seed": sd}, cfg)
                med.append(a), ident.append(b)
            for p in cfg.local_p_rx[1:]:
                fp, fm, dl = N.rx_local(th, p, with_delta=True)
                q = Q.per_theta(fp, fm, cfg.rho, delta=dl)
                a, b = _rows(q, {"model": "local", "p": p, "family": "rx_product", "regime": "product", "position": "k=0", "n": n, "seed": sd}, cfg)
                med.append(a), ident.append(b)
    log(f"rx: {len(med)} (model, p, n, seed) cells")
    return med, ident


def phase_ent(cfg, b1_work: Path) -> tuple[list, list]:
    from qlo.experiments.b1_entangling import load_cell

    b1 = B1CF.B1Config()
    med, ident = [], []
    for fam in b1.families:
        for reg in b1.regimes:
            for n in b1.n_grid(reg):
                L = B1CF.depth_of(reg, n)
                for sd in b1.seeds:
                    cell = load_cell(b1_work, fam, reg, n, sd)
                    for label in cell["positions"]:
                        fp0, fm0 = cell[f"{label}_F_plus"], cell[f"{label}_F_minus"]
                        for p in cfg.global_p:
                            qq = N.global_q(p, L)
                            fp, fm = N.global_overlay(fp0, fm0, n, qq)
                            q = Q.per_theta(fp, fm, cfg.rho, delta=N.global_delta(fp0, fm0, qq) if p > 0 else None)
                            a, b = _rows(q, {"model": "global", "p": p, "family": fam, "regime": reg, "position": label, "n": n, "seed": sd}, cfg)
                            med.append(a), ident.append(b)
    log(f"ent: {len(med)} (p, cell, n, seed) rows from {b1_work}")
    return med, ident


# =================================================================================================================
def _ranges(cfg, family, regime):
    grid = cfg.rx_n if family == "rx_product" else B1CF.B1Config().n_grid(regime)
    return {"primary": tuple(grid), "secondary_n_ge_8": tuple(n for n in grid if n >= cfg.secondary_n_min)}


def regression_vs_b1(med: pd.DataFrame, cfg) -> pd.DataFrame:
    b1 = pd.read_csv(B1_RESULTS / "sample_summary.csv")
    zero = med[(med.model == "global") & (med.p == 0.0)]
    cols = ["median_log10_S", "median_log10_abs_r", "median_log10_M_LE", "median_log10_M_SWAP"]
    m = zero.merge(b1, on=["family", "regime", "position", "n", "seed"], suffixes=("", "_b1"))
    out = pd.DataFrame({"family": m.family, "regime": m.regime, "position": m.position, "n": m.n, "seed": m.seed,
                        **{f"absdiff_{c}": (m[c] - m[f"{c}_b1"]).abs() for c in cols}})
    return out


def predictions(summ: pd.DataFrame, cfg) -> pd.DataFrame:
    """Asymptotic Proposition 5 / 6 exponents from the measured noiseless slopes of the same cell and range."""
    rows = []
    base = summ[summ.p == 0.0]
    for (model, p, fam, reg, pos, rname), g in summ.groupby(["model", "p", "family", "regime", "position", "fit_range"], sort=False):
        b0 = base[(base.family == fam) & (base.regime == reg) & (base.position == pos) & (base.fit_range == rname)].set_index("metric")["mean"]
        bS0, br0 = float(b0["b_S"]), float(b0["b_r"])
        if p == 0.0:
            pS, pr = bS0, br0
        elif model == "local":
            a, b = 1 - p, p / 2
            pS, pr = float(-(2 / np.log(10)) * np.log((np.sqrt(a + b) + np.sqrt(b)) / 2)), 0.0
        else:
            excess = max(bS0 - LOG2, 0.0)
            pS = LOG2 if bS0 >= LOG2 else bS0
            pr = br0 + excess + (-np.log10(1 - p) if reg == "dn" else 0.0)
        meas = g.set_index("metric")["mean"]
        r = {"model": model, "p": p, "family": fam, "regime": reg, "position": pos, "fit_range": rname,
             "noiseless_b_S": bS0, "noiseless_b_r": br0, "asym_b_S": pS, "asym_b_r": pr, "asym_b_LE": pS + 2 * pr,
             "asym_b_SWAP": 2 * pS + 2 * pr, "asym_ratio": (2 * pS + 2 * pr) / (pS + 2 * pr)}
        for m in ("b_S", "b_r", "b_LE", "b_SWAP", "ratio_obs", "eps_gap", "eps_LE", "eps_SWAP"):
            r[f"measured_{m}"] = float(meas[m])
        for m in ("b_S", "b_r"):
            span = r[f"asym_{m}"] - r[f"noiseless_{m}"]
            r[f"fraction_toward_asymptote_{m}"] = (r[f"measured_{m}"] - r[f"noiseless_{m}"]) / span if abs(span) > 1e-3 else np.nan
        rows.append(r)
    return pd.DataFrame(rows)


def window_slopes(med: pd.DataFrame, cfg) -> pd.DataFrame:
    """Local slopes on sliding windows of `window` consecutive n (seed-mean medians): the transition profile."""
    rows = []
    cols = {"b_S": ("median_log10_S", -1), "b_r": ("median_log10_abs_r", -1), "b_LE": ("median_log10_M_LE", 1), "b_SWAP": ("median_log10_M_SWAP", 1)}
    for key, g in med.groupby(KEYS, sort=False):
        m = g.groupby("n")[[c for c, _ in cols.values()]].mean().sort_index()
        ns = m.index.values
        for i in range(len(ns) - cfg.window + 1):
            sl = slice(i, i + cfg.window)
            r = dict(zip(KEYS, key), n_mid=float(ns[sl].mean()), n_lo=int(ns[sl][0]), n_hi=int(ns[sl][-1]))
            for name, (c, sign) in cols.items():
                r[name] = sign * linear_fit(ns[sl].astype(float), m[c].values[sl])["slope"]
            r["ratio"] = r["b_SWAP"] / r["b_LE"]
            rows.append(r)
    return pd.DataFrame(rows)


def crossover(med: pd.DataFrame, cfg) -> pd.DataFrame:
    """n where q * median S_noiseless(n) equals the floor 2(1 - q)/2^n (global model), log-linear interpolation."""
    rows = []
    zero = med[(med.model == "global") & (med.p == 0.0)]
    for (fam, reg, pos), g in zero.groupby(["family", "regime", "position"], sort=False):
        ms = g.groupby("n").median_log10_S.mean().sort_index()
        for p in cfg.global_p[1:]:
            ns = ms.index.values
            d = np.array([np.log10(N.global_q(p, layers(fam, reg, n))) + ms.loc[n] - np.log10(2 * (1 - N.global_q(p, layers(fam, reg, n))) / 2.0**n) for n in ns])
            idx = np.where(np.diff(np.sign(d)) != 0)[0]
            if len(idx):
                i = idx[0]
                nstar = ns[i] + (ns[i + 1] - ns[i]) * d[i] / (d[i] - d[i + 1])
                note = "inside range"
            else:
                nstar, note = np.nan, ("signal dominates throughout" if d[-1] > 0 else "floor dominates throughout")
            rows.append({"family": fam, "regime": reg, "position": pos, "p": p, "n_star": nstar, "note": note})
    return pd.DataFrame(rows)


def phase_analyse(cfg, med_rows, ident_rows) -> None:
    from qlo.b4 import figures as FG

    med = pd.DataFrame(med_rows)
    med.to_csv(OUT / "sample_summary.csv", index=False)
    iv = pd.DataFrame(ident_rows)
    agg = iv.groupby(["model", "p", "family"]).agg(n_checked=("n_checked", "sum"), n_excluded=("n_excluded", "sum"),
                                                     max_rel_err=("max_rel_err", "max")).reset_index()
    agg.to_csv(OUT / "ratio_identity_validation.csv", index=False)
    log(f"analyse: identity under noise over {int(agg.n_checked.sum())} theta rows: max rel err {agg.max_rel_err.max():.2e}, "
        f"excluded {int(agg.n_excluded.sum())}")
    if agg.max_rel_err.max() > cfg.identity_rel_tol:
        raise Stop("STOP: shot-ratio identity violated under noise")
    reg = regression_vs_b1(med, cfg)
    reg.to_csv(OUT / "regression_p0_vs_b1.csv", index=False)
    rmax = float(reg.filter(like="absdiff").max().max())
    log(f"analyse: p = 0 reproduces B1 medians on {len(reg)} (cell, n, seed) rows, max |diff| = {rmax:.2e}")
    if not len(reg) or rmax > cfg.regression_tol:
        raise Stop("STOP: p = 0 does not reproduce B1")
    fits = FT.seed_fits(med, lambda key: _ranges(cfg, key[2], key[3]), group_keys=tuple(KEYS))
    fits.to_csv(OUT / "seed_slopes.csv", index=False)
    rows = []
    for key, g in fits.groupby(KEYS + ["fit_range"], sort=False):
        g = g.sort_values("seed")
        for m in FT.METRICS:
            rows.append({**dict(zip(KEYS + ["fit_range"], key)), "metric": m, **IV.summarize(g[m].values, cfg.n_boot_seed, cfg.boot_seed)})
    summ = pd.DataFrame(rows)
    summ.to_csv(OUT / "slope_summary.csv", index=False)
    pr = predictions(summ, cfg)
    pr.to_csv(OUT / "predictions_vs_measured.csv", index=False)
    window_slopes(med, cfg).to_csv(OUT / "window_slopes.csv", index=False)
    crossover(med, cfg).to_csv(OUT / "crossover.csv", index=False)
    log(f"analyse: {len(fits)} seed fits, {len(pr)} (model, p, cell, range) rows")
    FG.all_figures(OUT, cfg)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--b1-work", type=Path, default=DEFAULT_B1_WORK)
    ap.add_argument("--skip-validate", action="store_true")
    a = ap.parse_args(argv)
    cfg = CF.B4Config()
    if json.loads(CF.config_json_from_markdown((ROOT / "docs" / "b4" / "B4_CONFIG.md").read_text())) != json.loads(cfg.to_json()):
        raise Stop("STOP: B4Config differs from docs/b4/B4_CONFIG.md")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "figures").mkdir(exist_ok=True)
    (OUT / "config.json").write_text(json.dumps({**json.loads(cfg.to_json()), "config_sha256": cfg.sha256()}, indent=2))
    log(f"\n## run {time.strftime('%Y-%m-%d %H:%M:%S %Z')} config sha256={cfg.sha256()}")
    t = time.time()
    if not a.skip_validate:
        phase_validate(cfg)
    m1, i1 = phase_rx(cfg)
    m2, i2 = phase_ent(cfg, a.b1_work)
    phase_analyse(cfg, m1 + m2, i1 + i2)
    log(f"done ({time.time() - t:.0f}s)")


if __name__ == "__main__":
    main()
