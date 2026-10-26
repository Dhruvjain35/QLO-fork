"""B1: entangling-ansatz sweeps, an independent empirical test of the principal-track A2 scaling rule.

    python -m qlo.experiments.b1_entangling --workers 6                         # all phases -> results/b1_entangling/
    python -m qlo.experiments.b1_entangling --phase analyse --workers 6         # one phase (caches are reused)
    python -m qlo.experiments.b1_entangling --smoke --out-dir D --work-dir W    # tiny pipeline test, no config check

Phases, in order; each STOPs the run on failure:
    audit    structural-zero audit of every predeclared position (+ a positive control), gradient cross-checks
    rx       Family 0 regression arm (exact Stage 7 RX product) against the B3 hardened intervals
    sweep    entangling families x depth regimes x n x master seeds -> per-theta F_+- caches (external SSD)
    analyse  per-theta quantities, identity check, per-seed fits, residuals, intervals, classes, tables, figures
    sign     conditional sign-law spot check
    a2       comparison with the principal A2 numerics (run last, after every B1 number has been written)
The configuration is ``qlo.b1.config.B1Config``; the run refuses to start unless it equals the JSON block that is
frozen in docs/b1/B1_CONFIG.md.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from qlo.b1 import audit as A
from qlo.b1 import circuits as C
from qlo.b1 import config as CF
from qlo.b1 import fits as FT
from qlo.b1 import quantities as Q
from qlo.b1 import rx_product as RX
from qlo.b1 import sign_law as SL
from qlo.hardening import intervals as IV
from qlo.hardening import seed_replicates as SR

ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = ROOT / "results" / "b1_entangling"
CONFIG_MD = ROOT / "docs" / "b1" / "B1_CONFIG.md"
B3_DIR = ROOT / "results" / "b3_hardening"
DEFAULT_WORK = Path("/Volumes/SSD Disk  1TB/qlo-b1-work")
B3_RANGE = {"primary": "primary_2_20", "secondary_n_ge_8": "n_ge_8"}
B3_METRIC = {"b_LE_ceil": "slope_loschmidt_snr1", "b_SWAP_ceil": "slope_swap_snr1", "gap_ceil": "gap_swap_minus_le_snr1"}
PHASES = ("audit", "rx", "sweep", "analyse", "sign", "a2")


class Stop(SystemExit):
    """A predeclared STOP condition (implementation error or failed regression)."""


class Log:
    def __init__(self, path: Path):
        self.path = path

    def __call__(self, msg: str) -> None:
        print(msg, flush=True)
        with open(self.path, "a") as f:
            f.write(msg + "\n")


def check_frozen(cfg: CF.B1Config) -> str:
    frozen = CF.config_json_from_markdown(CONFIG_MD.read_text())
    if json.loads(frozen) != json.loads(cfg.to_json()):
        raise Stop("STOP: B1Config differs from the JSON frozen in docs/b1/B1_CONFIG.md")
    return cfg.sha256()


def git_head() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def smoke_config() -> CF.B1Config:
    return replace(CF.B1Config(), seeds=(11_000, 11_001, 11_002), n_grid_d2=(4, 6, 8), n_grid_d4=(4, 6, 8), n_grid_dn=(4, 6, 8),
                   samples_per_cell=300, audit_samples=24, rx_n=(2, 4, 6, 8, 10), rx_samples=3_000, b3_seeds=(10_000, 10_001, 10_002),
                   n_boot_seed=500, theta_boot_reps=100, sign_n=8, sign_shots=(1, 16, 256, 4096))


def _pool(workers: int) -> ProcessPoolExecutor:
    for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        os.environ.setdefault(k, "1")
    return ProcessPoolExecutor(max_workers=workers)


# =================================================================================================================
# phase 1: structural-zero audit
# =================================================================================================================
def task_audit(family: str, regime: str, n: int, cfg: CF.B1Config) -> list[dict]:
    t = time.time()
    rows = A.audit_cell(family, regime, n, cfg)
    for r in rows:
        r["seconds"] = time.time() - t
    return rows


def resolve_positions(audit: pd.DataFrame, cfg: CF.B1Config, log: Log) -> tuple[dict, pd.DataFrame]:
    """{(family, regime, n): {label: position}} for the sweep, applying the predeclared fallback rule if needed."""
    chosen, fb_rows = {}, []
    for (fam, reg, n), g in audit[audit.role == "predeclared"].groupby(["family", "regime", "n"], sort=False):
        depth = CF.depth_of(reg, n)
        pos = {}
        for label, p in CF.distinct_positions(depth).items():
            r = g[g.position == label].iloc[0]
            if r.classification == "VALID":
                pos[label] = p
                continue
            theta = CF.audit_theta(fam, reg, n, cfg.audit_samples)
            fb = A.fallback(theta, fam, n, depth, p, cfg)
            fb_rows.append({"family": fam, "regime": reg, "n": n, "position": label, "original": str(p), "original_class": r.classification,
                            "fallback": str(fb["position"]), "fallback_class": fb["classification"],
                            "reason": f"original position {r.classification} in the audit (zero fraction {r.zero_fraction:.3g})"})
            log(f"  fallback: {fam} {reg} n={n} {label} {p} -> {fb['position']} ({fb['classification']})")
            if fb["position"] is not None:
                pos[label] = fb["position"]
        chosen[(fam, reg, int(n))] = pos
    return chosen, pd.DataFrame(fb_rows, columns=["family", "regime", "n", "position", "original", "original_class", "fallback",
                                                  "fallback_class", "reason"])


def phase_audit(cfg, out: Path, work: Path, workers: int, log: Log) -> dict:
    t0 = time.time()
    jobs = [(f, r, n) for f in cfg.families for r in cfg.regimes for n in cfg.n_grid(r)]
    jobs.sort(key=lambda j: -(j[2] * 100 + CF.depth_of(j[1], j[2])))
    with _pool(workers) as pool:
        futs = [pool.submit(task_audit, f, r, n, cfg) for f, r, n in jobs]
        rows = [row for fu in futs for row in fu.result()]
    audit = pd.DataFrame(rows).sort_values(["family", "regime", "n", "layer", "rotation_index"], kind="stable")
    audit.to_csv(out / "structural_zero_audit.csv", index=False)
    log(f"audit: {len(jobs)} (family, regime, n) cells, {len(audit)} position rows, {time.time() - t0:.0f}s")
    bad = audit[~audit.agreement_ok]
    if len(bad):
        log(bad.to_string())
        raise Stop("STOP: gradient / fidelity cross-checks disagree in the structural-zero audit (implementation error)")
    log(f"  max agreement error (|diff|/S) over all rows: {audit.max_agreement_err.max():.2e}; PennyLane-checked rows: "
        f"{int(audit.pennylane_checked.sum())}/{len(audit)}")
    ctrl = audit[audit.role == "control"]
    if len(ctrl) and not (ctrl.classification == "STRUCTURAL").all():
        raise Stop("STOP: the positive control (final-layer RZ of the repo HEA) was not classified STRUCTURAL")
    log(f"  positive control CONTROL_FINAL_RZ: {ctrl.classification.value_counts().to_dict()}")
    pre = audit[audit.role == "predeclared"]
    log(f"  predeclared positions: {pre.classification.value_counts().to_dict()}")
    chosen, fb = resolve_positions(audit, cfg, log)
    fb.to_csv(out / "position_fallbacks.csv", index=False)
    (work / "positions.json").write_text(json.dumps({f"{k[0]}|{k[1]}|{k[2]}": {l: list(p) for l, p in v.items()} for k, v in chosen.items()}, indent=1))
    return chosen


def load_positions(work: Path) -> dict:
    raw = json.loads((work / "positions.json").read_text())
    return {(k.split("|")[0], k.split("|")[1], int(k.split("|")[2])): {l: tuple(p) for l, p in v.items()} for k, v in raw.items()}


# =================================================================================================================
# phase 2: RX product regression arm (Family 0)
# =================================================================================================================
def task_rx(n: int, seed: int, cfg: CF.B1Config) -> tuple[dict, dict]:
    return RX.rx_cell_row(n, cfg.rx_samples, seed, cfg.rx_stream, cfg.rx_component, cfg.rho, cfg.audit_zero_tol_r)


def rx_ranges(cfg) -> dict:
    return cfg.fit_ranges(cfg.rx_n)


def rx_ceil_fits(med: pd.DataFrame, cfg) -> pd.DataFrame:
    rows = []
    for seed, g in med.groupby("seed", sort=True):
        for rname, n_range in rx_ranges(cfg).items():
            d = g.set_index("n").loc[list(n_range)]
            le = SR.fit_series(d.index.values, d.median_log10_M_LE_ceil.values)
            sw = SR.fit_series(d.index.values, d.median_log10_M_SWAP_ceil.values)
            rows.append({"seed": int(seed), "fit_range": rname, "b_LE_ceil": le["slope"], "b_SWAP_ceil": sw["slope"],
                         "gap_ceil": sw["slope"] - le["slope"]})
    return pd.DataFrame(rows)


def phase_rx(cfg, out: Path, work: Path, workers: int, log: Log, smoke: bool) -> None:
    t0 = time.time()
    # --- B3 populations regenerated: reproduce B3's published per-seed slopes, then derive b_S / b_r intervals -------
    b3_cfg = json.loads((B3_DIR / "config.json").read_text())
    b3_n = tuple(int(n) for n in b3_cfg["primary_n"])                  # B3's own grid and sample size, whatever cfg.rx_n is
    b3_ranges = {B3_RANGE[k]: v for k, v in cfg.fit_ranges(b3_n).items()}
    regen_med = RX.b3_regenerated_medians(cfg.b3_seeds, b3_n, int(b3_cfg["seed_samples"]))
    regen = RX.b3_regenerated_slopes(regen_med, b3_ranges)
    pub = pd.read_csv(B3_DIR / "seed_slopes.csv")
    pub = pub[(pub.target == "snr1") & pub.seed.isin(cfg.b3_seeds)]
    chk = []
    for _, r in regen.iterrows():
        for sc, col in (("loschmidt", "slope_loschmidt_snr1"), ("swap", "slope_swap_snr1")):
            p = pub[(pub.seed == r.seed) & (pub.scheme == sc) & (pub.fit_range == r.fit_range)]
            if len(p):
                chk.append({"seed": r.seed, "fit_range": r.fit_range, "metric": col, "b3_published": float(p.slope.iloc[0]),
                            "regenerated": float(r[col]), "abs_diff": abs(float(p.slope.iloc[0]) - float(r[col]))})
    chk = pd.DataFrame(chk)
    chk.to_csv(out / "b3_regeneration_check.csv", index=False)
    max_diff = float(chk.abs_diff.max())
    log(f"rx: B3 populations regenerated ({len(cfg.b3_seeds)} seeds x {len(b3_n)} n x {b3_cfg['seed_samples']} theta); max |slope diff| vs "
        f"B3 seed_slopes.csv = {max_diff:.2e} over {len(chk)} values")
    if not max_diff <= cfg.b3_regeneration_tol:
        raise Stop("STOP: regenerated B3 populations do not reproduce B3's published per-seed slopes")
    b3_pub = pd.read_csv(B3_DIR / "seed_summary.csv")
    b3_boot = (int(b3_cfg["n_boot_seed"]), int(b3_cfg["boot_seed"]))     # B3's own interval settings
    b3_int = {}
    for b1_range, b3_range in B3_RANGE.items():
        for m, b3m in B3_METRIC.items():
            s = b3_pub[(b3_pub.fit_range == b3_range) & (b3_pub.metric == b3m)].iloc[0]
            b3_int[(b1_range, m)] = {"source": "B3 results/b3_hardening/seed_summary.csv", **{k: float(s[k]) for k in
                                     ("mean", "sd", "pct_lo", "pct_hi", "boot_lo", "boot_hi")}}
        g = regen[regen.fit_range == b3_range].sort_values("seed")
        for m in ("b_S", "b_r"):
            s = IV.summarize(g[m].values, *b3_boot)
            b3_int[(b1_range, m)] = {"source": "B3 theta populations regenerated by B1 (B3 seeds, 25000 theta, stream 20)",
                                     **{k: s[k] for k in ("mean", "sd", "pct_lo", "pct_hi", "boot_lo", "boot_hi")}}
        s = IV.summarize(g.slope_loschmidt_snr1.values, *b3_boot)
        pubm = b3_int[(b1_range, "b_LE_ceil")]
        log(f"  {b3_range}: regenerated LE summary mean {s['mean']:.10f} vs published {pubm['mean']:.10f}; "
            f"pct [{s['pct_lo']:.7f}, {s['pct_hi']:.7f}] vs [{pubm['pct_lo']:.7f}, {pubm['pct_hi']:.7f}]")
    # --- B1 RX arm ---------------------------------------------------------------------------------------------------
    with _pool(workers) as pool:
        futs = [pool.submit(task_rx, n, sd, cfg) for sd in cfg.seeds for n in cfg.rx_n]
        res = [f.result() for f in futs]
    med = pd.DataFrame([r[0] for r in res])
    ident = pd.DataFrame([r[1] for r in res])
    med.to_csv(work / "rx_sample_summary.csv", index=False)
    ident.to_csv(work / "rx_identity.csv", index=False)
    ceil_fits = rx_ceil_fits(med, cfg)
    cont = FT.seed_fits(med, lambda key: rx_ranges(cfg))
    both = ceil_fits.merge(cont[["seed", "fit_range", "b_S", "b_r"]], on=["seed", "fit_range"])
    both.to_csv(work / "rx_regression_seed_slopes.csv", index=False)
    rows = []
    sanity = {"b_S": (np.log10(4.0), cfg.rx_sanity_tol_bS_bLE_br), "b_r": (0.0, cfg.rx_sanity_tol_bS_bLE_br),
              "b_LE_ceil": (np.log10(4.0), cfg.rx_sanity_tol_bS_bLE_br), "b_SWAP_ceil": (np.log10(16.0), cfg.rx_sanity_tol_bSWAP)}
    for b1_range in B3_RANGE:
        g = both[both.fit_range == b1_range].sort_values("seed")
        for m in ("b_LE_ceil", "b_SWAP_ceil", "gap_ceil", "b_S", "b_r"):
            s = IV.summarize(g[m].values, cfg.n_boot_seed, cfg.boot_seed)
            b3 = b3_int[(b1_range, m)]
            inside = b3["pct_lo"] <= s["mean"] <= b3["pct_hi"]
            overlap = not (s["boot_hi"] < b3["boot_lo"] or b3["boot_hi"] < s["boot_lo"])
            ref = sanity.get(m)
            rows.append({"fit_range": b1_range, "b3_fit_range": B3_RANGE[b1_range], "metric": m, "role": "PRIMARY" if b1_range == "primary" else "secondary",
                         "b1_n_seeds": s["n_units"], "b1_mean": s["mean"], "b1_sd": s["sd"], "b1_pct_lo": s["pct_lo"], "b1_pct_hi": s["pct_hi"],
                         "b1_boot_lo": s["boot_lo"], "b1_boot_hi": s["boot_hi"],
                         "b3_source": b3["source"], "b3_mean": b3["mean"], "b3_pct_lo": b3["pct_lo"], "b3_pct_hi": b3["pct_hi"],
                         "b3_boot_lo": b3["boot_lo"], "b3_boot_hi": b3["boot_hi"],
                         "b1_mean_inside_b3_pct": bool(inside), "boot_cis_overlap": bool(overlap),
                         "b1_seeds_inside_b3_pct": int(np.sum((g[m].values >= b3["pct_lo"]) & (g[m].values <= b3["pct_hi"]))),
                         "sanity_reference": ref[0] if ref else float("nan"), "sanity_tol": ref[1] if ref else float("nan"),
                         "sanity_ok": bool(abs(s["mean"] - ref[0]) <= ref[1]) if ref else None})
    reg = pd.DataFrame(rows)
    reg.to_csv(out / "rx_regression.csv", index=False)
    prim = reg[reg.role == "PRIMARY"]
    log(f"rx: B1 arm {len(cfg.seeds)} seeds x {len(cfg.rx_n)} n x {cfg.rx_samples} theta ({time.time() - t0:.0f}s)")
    for _, r in reg.iterrows():
        log(f"  [{r.role}] {r.fit_range:17s} {r.metric:11s} B1 mean {r.b1_mean:+.6f} (boot {r.b1_boot_lo:+.6f}..{r.b1_boot_hi:+.6f})"
            f"  B3 pct {r.b3_pct_lo:+.6f}..{r.b3_pct_hi:+.6f}  inside={r.b1_mean_inside_b3_pct} overlap={r.boot_cis_overlap}")
    imax = ident.max_rel_err.max()
    log(f"  RX identity check: max rel err {imax:.2e}, excluded rows {int(ident.n_excluded.sum())}")
    if not prim.b1_mean_inside_b3_pct.all():
        if smoke:
            log("  (smoke run: regression failure tolerated)")
        else:
            raise Stop("STOP (CASE E): the RX-product regression arm is outside the B3 hardened intervals")
    if not imax <= cfg.identity_rel_tol:
        raise Stop("STOP: exact shot-ratio identity violated on the RX arm (implementation error)")


# =================================================================================================================
# phase 3: entangling sweeps
# =================================================================================================================
def cache_path(work: Path, family: str, regime: str, n: int, seed: int) -> Path:
    return work / "sweep" / f"{family}_{regime}_n{n}_seed{seed}.npz"


def task_sweep(work: str, family: str, regime: str, n: int, seed: int, positions: dict, cfg: CF.B1Config) -> dict:
    path = cache_path(Path(work), family, regime, n, seed)
    labels = sorted(positions)
    if path.exists():
        z = np.load(path)
        if int(z["n_samples"]) == cfg.samples_per_cell and all(f"{l}_F_plus" in z for l in labels):
            return {"family": family, "regime": regime, "n": n, "seed": seed, "cached": True, "seconds": float(z["seconds"]),
                    "max_bracket_vs_forward": float(z["max_bracket_vs_forward"])}
    t = time.time()
    depth = CF.depth_of(regime, n)
    theta = CF.sample_theta(family, regime, n, seed, cfg.samples_per_cell)
    N = theta.shape[0]
    on_q0 = {l: p for l, p in positions.items() if p[1] == 0}
    other = {l: p for l, p in positions.items() if p[1] != 0}
    arr = {f"{l}_{k}": np.empty(N) for l in labels for k in ("F_plus", "F_minus")}
    F0 = np.empty(N)
    cons = 0.0
    step = C.batch_rows(n)
    for a in range(0, N, step):
        sl = slice(a, min(a + step, N))
        th = theta[sl]
        F, sh = C.shifted_fidelities(th, family, n, depth, set(on_q0.values()))
        F0[sl] = F
        for l, p in on_q0.items():
            arr[f"{l}_F_plus"][sl], arr[f"{l}_F_minus"][sl] = sh[p]["F_plus"], sh[p]["F_minus"]
            S = np.maximum(sh[p]["F_plus"] + sh[p]["F_minus"], 1e-300)
            cons = max(cons, float(np.max(np.abs(sh[p]["F_bracket"] - F) / S)))
        for l, p in other.items():
            for sign, key in ((1.0, "F_plus"), (-1.0, "F_minus")):
                ts = th.copy()
                ts[:, p[0], p[1], p[2]] += sign * np.pi / 2
                arr[f"{l}_{key}"][sl] = C.fidelity(ts, family, n, depth)
    seconds = time.time() - t
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp.npz")
    np.savez(tmp, n_samples=N, F=F0, seconds=seconds, max_bracket_vs_forward=cons,
             positions=json.dumps({l: list(p) for l, p in positions.items()}), **arr)
    tmp.rename(path)
    return {"family": family, "regime": regime, "n": n, "seed": seed, "cached": False, "seconds": seconds, "max_bracket_vs_forward": cons}


def phase_sweep(cfg, out: Path, work: Path, workers: int, log: Log) -> None:
    t0 = time.time()
    positions = load_positions(work)
    jobs = [(f, r, n, sd) for f in cfg.families for r in cfg.regimes for n in cfg.n_grid(r) for sd in cfg.seeds]
    cost = lambda j: (2.0 ** j[2]) * CF.depth_of(j[1], j[2]) * j[2]
    jobs.sort(key=cost, reverse=True)
    rows = []
    with _pool(workers) as pool:
        futs = [pool.submit(task_sweep, str(work), f, r, n, sd, positions[(f, r, n)], cfg) for f, r, n, sd in jobs]
        for i, fu in enumerate(futs):
            rows.append(fu.result())
            if (i + 1) % 20 == 0 or i + 1 == len(futs):
                print(f"sweep {i + 1}/{len(futs)} ({time.time() - t0:.0f}s)", flush=True)
    t = pd.DataFrame(rows)
    t.to_csv(work / "sweep_tasks.csv", index=False)
    log(f"sweep: {len(jobs)} tasks ({int((~t.cached).sum())} computed, {int(t.cached.sum())} cached); compute {t.seconds.sum() / 3600:.2f} "
        f"CPU-h; wall {time.time() - t0:.0f}s; max |F(theta) from brackets - forward| / S = {t.max_bracket_vs_forward.max():.2e}")


# =================================================================================================================
# phase 4: analysis
# =================================================================================================================
def load_cell(work: Path, family: str, regime: str, n: int, seed: int) -> dict:
    z = np.load(cache_path(work, family, regime, n, seed))
    pos = {l: tuple(p) for l, p in json.loads(str(z["positions"])).items()}
    return {"positions": pos, **{k: z[k] for k in z.files if k.endswith(("_F_plus", "_F_minus"))}}


def entangling_tables(cfg, work: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """(sample_summary rows per seed, identity rows, pooled-over-seeds diagnostics) for every (family, regime, n, position)."""
    rows, ident, pooled = [], [], []
    for fam in cfg.families:
        for reg in cfg.regimes:
            for n in cfg.n_grid(reg):
                depth = CF.depth_of(reg, n)
                acc = {}
                for sd in cfg.seeds:
                    cell = load_cell(work, fam, reg, n, sd)
                    for label, p in cell["positions"].items():
                        q = Q.per_theta(cell[f"{label}_F_plus"], cell[f"{label}_F_minus"], cfg.rho)
                        meta = {"family": fam, "regime": reg, "depth": depth, "position": label, "layer": p[0], "qubit": p[1],
                                "gate": f"R{C.AXES[fam][p[2]]}", "n": n, "seed": sd}
                        rows.append({**meta, **Q.cell_diagnostics(q, cfg.audit_zero_tol_r)})
                        ident.append({**meta, **Q.identity_check(q)})
                        a = acc.setdefault(label, {"meta": meta, "fp": [], "fm": []})
                        a["fp"].append(cell[f"{label}_F_plus"])
                        a["fm"].append(cell[f"{label}_F_minus"])
                for label, a in acc.items():
                    q = Q.per_theta(np.concatenate(a["fp"]), np.concatenate(a["fm"]), cfg.rho)
                    meta = {k: v for k, v in a["meta"].items() if k != "seed"}
                    pooled.append({**meta, "seeds_pooled": len(a["fp"]), **Q.cell_diagnostics(q, cfg.audit_zero_tol_r)})
    return pd.DataFrame(rows), pd.DataFrame(ident), pd.DataFrame(pooled)


def ranges_for(cfg):
    def f(key):
        fam, reg = key[0], key[1]
        return cfg.fit_ranges(cfg.rx_n if fam == "rx_product" else cfg.n_grid(reg))
    return f


def build_main_table(med: pd.DataFrame, fits: pd.DataFrame, summ: pd.DataFrame, cfg) -> pd.DataFrame:
    rows = []
    for key, g in fits.groupby(FT.CELL_KEYS, sort=False):
        fam, reg, pos, rname = key
        s = {m: summ[(summ.family == fam) & (summ.regime == reg) & (summ.position == pos) & (summ.fit_range == rname) & (summ.metric == m)].iloc[0]
             for m in FT.METRICS}
        n_range = ranges_for(cfg)((fam, reg))[rname]
        conc = FT.concentration(med[(med.family == fam) & (med.regime == reg) & (med.position == pos)], g, s["b_S"], n_range, cfg)
        out = FT.cell_outcome(s, conc["concentration"])
        dbl = FT.doubling(s, cfg)
        row = {"family": fam, "regime": reg, "position": pos, "fit_range": rname, "n_fit_range": f"{min(n_range)}-{max(n_range)}",
               "n_points": len(n_range), "n_seeds": int(s["b_S"]["n_units"])}
        for m in ("b_S", "b_r", "b_LE", "b_SWAP", "gap_obs", "eps_LE", "eps_SWAP", "eps_gap", "ratio_obs", "ratio_pred", "ratio_diff"):
            row[m] = s[m]["mean"]
            row[f"{m}_ci_lo"], row[f"{m}_ci_hi"] = s[m]["boot_lo"], s[m]["boot_hi"]
            row[f"{m}_pct_lo"], row[f"{m}_pct_hi"] = s[m]["pct_lo"], s[m]["pct_hi"]
        row["gap_pred"] = row["b_S"]
        row["eps_gap_equivalent_within_margin"] = FT.equivalence(s["eps_gap"], cfg.equivalence_margin)
        row["eps_LE_equivalent_within_margin"] = FT.equivalence(s["eps_LE"], cfg.equivalence_margin)
        row["eps_SWAP_equivalent_within_margin"] = FT.equivalence(s["eps_SWAP"], cfg.equivalence_margin)
        row.update({k: v for k, v in conc.items()})
        row.update(out)
        row.update(dbl)
        rows.append(row)
    return pd.DataFrame(rows)


def residual_table(summ: pd.DataFrame, main: pd.DataFrame, cfg) -> pd.DataFrame:
    r = summ[summ.metric.isin(["eps_LE", "eps_SWAP", "eps_gap"])].copy()
    r["boot_ci_contains_0"] = (r.boot_lo <= 0) & (r.boot_hi >= 0)
    r["pct_interval_contains_0"] = (r.pct_lo <= 0) & (r.pct_hi >= 0)
    r["equivalent_within_margin"] = (r.boot_lo >= -cfg.equivalence_margin) & (r.boot_hi <= cfg.equivalence_margin)
    r["iqr"] = r.q75 - r.q25
    bs = summ[summ.metric == "b_S"].set_index(FT.CELL_KEYS)["mean"]
    r["b_S_mean"] = [bs.loc[tuple(k)] for k in r[FT.CELL_KEYS].values]
    r["effect_rel_to_b_S"] = r["mean"] / r["b_S_mean"]
    conc = main.set_index(FT.CELL_KEYS)["concentration"]
    r["concentration"] = [conc.loc[tuple(k)] for k in r[FT.CELL_KEYS].values]
    return r


def position_table(fits: pd.DataFrame, summ: pd.DataFrame, main: pd.DataFrame, cfg) -> pd.DataFrame:
    """b_r by position, paired (same theta, same seed) position differences, and the section-22 outcome per cell."""
    rows = []
    ent = fits[fits.family != "rx_product"]
    for (fam, reg, rname), g in ent.groupby(["family", "regime", "fit_range"], sort=False):
        pos_labels = [p for p in CF.POSITIONS if p in set(g.position)]
        m = main[(main.family == fam) & (main.regime == reg) & (main.fit_range == rname)].set_index("position")
        early = g[g.position == "EARLY"].sort_values("seed")
        for p in pos_labels:
            gp = g[g.position == p].sort_values("seed")
            sb = IV.summarize(gp.b_r.values, cfg.n_boot_seed, cfg.boot_seed)
            d = IV.summarize(IV.paired_gap(early.b_r.values, gp.b_r.values), cfg.n_boot_seed, cfg.boot_seed) if p != "EARLY" else None
            approx0 = FT.ci_contains(sb) and abs(sb["mean"]) <= cfg.br_small_fraction * m.loc[p, "b_S"]
            rows.append({"family": fam, "regime": reg, "fit_range": rname, "position": p, "layer_rule": {"EARLY": "0", "MIDDLE": "floor(d/2)", "LATE": "d-1"}[p],
                         "b_r_mean": sb["mean"], "b_r_ci_lo": sb["boot_lo"], "b_r_ci_hi": sb["boot_hi"], "b_r_pct_lo": sb["pct_lo"], "b_r_pct_hi": sb["pct_hi"],
                         "b_S_mean": m.loc[p, "b_S"], "b_r_over_b_S": sb["mean"] / m.loc[p, "b_S"], "b_r_approximately_zero": bool(approx0),
                         "b_r_minus_EARLY_mean": d["mean"] if d else 0.0, "b_r_minus_EARLY_ci_lo": d["boot_lo"] if d else float("nan"),
                         "b_r_minus_EARLY_ci_hi": d["boot_hi"] if d else float("nan"),
                         "eps_gap_mean": m.loc[p, "eps_gap"], "eps_gap_ci_lo": m.loc[p, "eps_gap_ci_lo"], "eps_gap_ci_hi": m.loc[p, "eps_gap_ci_hi"],
                         "eps_gap_ci_contains_0": bool(m.loc[p, "gap_ci_contains_0"]),
                         "rule_check": m.loc[p, "rule_check"], "concentration": m.loc[p, "concentration"],
                         "ratio_obs": m.loc[p, "ratio_obs"], "ratio_pred": m.loc[p, "ratio_pred"],
                         "doubling_test_eligible": bool(m.loc[p, "doubling_test_eligible"]), "ratio_consistent_with_2": m.loc[p, "ratio_consistent_with_2"],
                         "depth2_note": "MIDDLE coincides with LATE (floor(2/2) = 1 = d - 1)" if reg == "d2" and p == "LATE" else ""})
        sub = [r for r in rows if r["family"] == fam and r["regime"] == reg and r["fit_range"] == rname]
        all0 = all(r["b_r_approximately_zero"] for r in sub)
        rule_holds = all(r["eps_gap_ci_contains_0"] for r in sub)
        if not rule_holds:
            outcome = "C (slope rule fails beyond uncertainty at some position)"
        elif all0:
            outcome = "A (b_r approximately zero at every tested position)"
        else:
            outcome = "B (b_r not approximately zero at some position; general rule holds, doubling does not)"
        for r in sub:
            r["section22_outcome"] = outcome
    return pd.DataFrame(rows)


def theta_bootstrap(cfg, work: Path, seed_fits_df: pd.DataFrame) -> pd.DataFrame:
    """Secondary: theta bootstrap inside ONE master seed, for every family and position of one regime."""
    rows = []
    reg = cfg.theta_boot_regime
    sd = cfg.seeds[cfg.theta_boot_seed_index]
    n_range = np.array(cfg.n_grid(reg), dtype=float)
    keys = ("log10_S", "log10_abs_r", "log10_M_LE", "log10_M_SWAP")
    for fam in cfg.families:
        cells = {n: load_cell(work, fam, reg, n, sd) for n in cfg.n_grid(reg)}
        for label in cells[cfg.n_grid(reg)[0]]["positions"]:
            rng = np.random.default_rng(np.random.SeedSequence([CF.B1_TAG, 0xB007, CF.FAMILY_CODE[fam], CF.REGIME_CODE[reg], sd]))
            meds = np.empty((cfg.theta_boot_reps, len(n_range), len(keys)))
            for i, n in enumerate(cfg.n_grid(reg)):
                q = Q.per_theta(cells[n][f"{label}_F_plus"], cells[n][f"{label}_F_minus"], cfg.rho)
                N = q["S"].size
                idx = rng.integers(0, N, (cfg.theta_boot_reps, N))
                for k, key in enumerate(keys):
                    meds[:, i, k] = np.median(q[key][idx], axis=1)
            sl = {key: IV.ols_slopes(n_range, meds[:, :, k])[0] for k, key in enumerate(keys)}
            b = {"b_S": -sl["log10_S"], "b_r": -sl["log10_abs_r"], "b_LE": sl["log10_M_LE"], "b_SWAP": sl["log10_M_SWAP"]}
            res = FT.prediction_residuals(b["b_S"], b["b_r"], b["b_LE"], b["b_SWAP"])
            b.update({k: res[k] for k in ("eps_LE", "eps_SWAP", "eps_gap")})
            sf = seed_fits_df[(seed_fits_df.family == fam) & (seed_fits_df.regime == reg) & (seed_fits_df.position == label)
                              & (seed_fits_df.fit_range == "primary")]
            for m, v in b.items():
                lo, hi = IV.percentile_interval(v)
                slo, shi = IV.percentile_interval(sf[m].values)
                rows.append({"family": fam, "regime": reg, "position": label, "seed": sd, "fit_range": "primary", "metric": m,
                             "theta_boot_reps": cfg.theta_boot_reps, "theta_boot_mean": float(np.mean(v)), "theta_boot_sd": float(np.std(v, ddof=1)),
                             "theta_boot_lo": lo, "theta_boot_hi": hi, "seed_sd": float(sf[m].std(ddof=1)), "seed_pct_lo": slo, "seed_pct_hi": shi,
                             "point_this_seed": float(sf[sf.seed == sd][m].iloc[0])})
    return pd.DataFrame(rows)


def posthoc_gap_decomposition(med: pd.DataFrame, cfg) -> pd.DataFrame:
    """POST-HOC (added after the results, labelled as such). eps_gap splits exactly into
        A = slope(median log10 R) - b_S          (O(S) term: median log10 R = log10 2 - median log10 S + O(S), exactly by
                                                   monotonicity, so A -> 0 as S -> 0)
        D = slope(median log10 M_SWAP - median log10 M_LE - median log10 R)   (non-additivity of medians)
    with eps_gap = A + D per seed."""
    m = med.assign(defect=med.median_log10_M_SWAP - med.median_log10_M_LE - med.median_log10_R)
    rows = []
    for (fam, reg, pos), g in m.groupby(["family", "regime", "position"], sort=False):
        for rname, n_range in ranges_for(cfg)((fam, reg)).items():
            per = []
            for _, gs in g.groupby("seed", sort=True):
                d = gs.set_index("n").loc[list(n_range)]
                x = d.index.values.astype(float)
                bS = -FT.linear_fit(x, d.median_log10_S.values)["slope"]
                A = FT.linear_fit(x, d.median_log10_R.values)["slope"] - bS
                D = FT.linear_fit(x, d.defect.values)["slope"]
                per.append((A, D, A + D))
            per = np.array(per)
            for k, name in enumerate(("A_medlogR_slope_minus_bS", "D_median_nonadditivity_slope", "A_plus_D_equals_eps_gap")):
                s = IV.summarize(per[:, k], cfg.n_boot_seed, cfg.boot_seed)
                rows.append({"family": fam, "regime": reg, "position": pos, "fit_range": rname, "component": name,
                             **{k2: s[k2] for k2 in ("mean", "sd", "pct_lo", "pct_hi", "boot_lo", "boot_hi")}})
    return pd.DataFrame(rows)


def phase_analyse(cfg, out: Path, work: Path, log: Log) -> None:
    from qlo.b1 import figures as FG

    t0 = time.time()
    ent, ident, pooled = entangling_tables(cfg, work)
    pooled.to_csv(out / "cell_diagnostics_pooled.csv", index=False)
    rx_med = pd.read_csv(work / "rx_sample_summary.csv")
    rx_ident = pd.read_csv(work / "rx_identity.csv")
    med = pd.concat([rx_med, ent], ignore_index=True)       # RX-only columns (B3 ceil convention) are empty for entangling rows
    med.to_csv(out / "sample_summary.csv", index=False)
    # ---- identity check (implementation STOP) ----
    ident_all = pd.concat([rx_ident, ident], ignore_index=True)
    iv = ident_all.groupby(["family", "regime", "position", "n"], sort=False).agg(
        n_rows=("n_rows", "sum"), n_checked=("n_checked", "sum"), n_excluded=("n_excluded", "sum"), max_abs_err=("max_abs_err", "max"),
        max_rel_err=("max_rel_err", "max"), max_abs_log10_err=("max_abs_log10_err", "max")).reset_index()
    iv["passes"] = iv.max_rel_err <= cfg.identity_rel_tol
    iv.to_csv(out / "ratio_identity_validation.csv", index=False)
    log(f"analyse: identity check over {int(iv.n_checked.sum())} theta rows: max abs err {iv.max_abs_err.max():.2e}, max rel err "
        f"{iv.max_rel_err.max():.2e}, excluded {int(iv.n_excluded.sum())}")
    if not iv.passes.all():
        raise Stop("STOP: exact shot-ratio identity violated (implementation error)")
    nan_cols = [c for c in med.columns if c.startswith("n_nan_")]
    n_nan = int(med[nan_cols].to_numpy().sum())
    flags = {c: int(med[c].sum()) for c in ("n_S_zero", "n_delta_zero", "n_var_le_zero", "n_underflow", "n_r_numerically_zero",
                                             "n_nonfinite_log10_M_LE", "n_nonfinite_log10_M_SWAP") if c in med}
    log(f"  degenerate-row counts over all cells: {flags}; NaN rows in fitted medians: {n_nan}")
    # ---- fits ----
    fits = FT.seed_fits(med, ranges_for(cfg))
    fits.to_csv(out / "seed_slopes.csv", index=False)
    summ = FT.summarize_metrics(fits, cfg)
    summ.to_csv(out / "slope_summary.csv", index=False)
    main = build_main_table(med, fits, summ, cfg)
    main.to_csv(out / "main_table.csv", index=False)
    residual_table(summ, main, cfg).to_csv(out / "prediction_residuals.csv", index=False)
    pos = position_table(fits, summ, main, cfg)
    pos.to_csv(out / "parameter_position_summary.csv", index=False)
    posthoc_gap_decomposition(med, cfg).to_csv(out / "posthoc_gap_decomposition.csv", index=False)
    tb = theta_bootstrap(cfg, work, fits)
    tb.to_csv(out / "theta_bootstrap_subset.csv", index=False)
    log(f"analyse: {len(fits)} seed fits, {len(main)} cells x ranges ({time.time() - t0:.0f}s)")
    figs = out / "figures"
    figs.mkdir(exist_ok=True)
    FG.all_figures(med, fits, main, pos, iv, figs)


# =================================================================================================================
# phase 5: conditional sign-law spot check
# =================================================================================================================
def phase_sign(cfg, out: Path, work: Path, log: Log) -> None:
    from qlo.b1 import figures as FG

    rows = []
    sd = cfg.seeds[cfg.sign_seed_index]
    for fam in cfg.families:
        for reg in cfg.regimes:
            cell = load_cell(work, fam, reg, cfg.sign_n, sd)
            for label in cell["positions"]:
                meta = {"family": fam, "regime": reg, "depth": CF.depth_of(reg, cfg.sign_n), "position": label, "n": cfg.sign_n, "seed": sd}
                rows += SL.sign_law_rows(cell[f"{label}_F_plus"], cell[f"{label}_F_minus"], cfg.sign_S_quantiles, cfg.sign_shots, meta)
    df = pd.DataFrame(rows)
    df.to_csv(out / "conditional_sign_summary.csv", index=False)
    small = df[df.M_times_S <= 1e-2]
    log(f"sign: {len(df)} (cell, theta, M) rows; max |error| where M S <= 1e-2: {small.error.abs().max():.2e} "
        f"({len(small)} rows); max |error| overall {df.error.abs().max():.2e}")
    FG.conditional_sign_error(df, out / "figures" / "conditional_sign_error_vs_MS.png")


# =================================================================================================================
def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    p.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--phase", choices=PHASES + ("all",), default="all")
    p.add_argument("--smoke", action="store_true")
    a = p.parse_args(argv)
    cfg = smoke_config() if a.smoke else CF.B1Config()
    SR.check_seeds(cfg.seeds, forbidden=(SR.STAGE7_SEED,) + SR.B3_SEEDS)
    out, work = a.out_dir, a.work_dir
    out.mkdir(parents=True, exist_ok=True)
    (out / "figures").mkdir(exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    log = Log(out / "numerics_log.md")
    sha = "smoke (not frozen)" if a.smoke else check_frozen(cfg)
    phases = PHASES if a.phase == "all" else (a.phase,)
    log(f"\n## run {time.strftime('%Y-%m-%d %H:%M:%S %Z')}  phases={','.join(phases)}  git HEAD={git_head()}  config sha256={sha}")
    (out / "config.json").write_text(json.dumps({**cfg.to_dict(), "config_sha256": sha, "work_dir": str(work),
                                                 "frozen_config_document": "B1_CONFIG.md", "git_head_at_run": git_head(),
                                                 "family_labels": C.FAMILY_LABEL, "rotation_axes": {k: list(v) for k, v in C.AXES.items()},
                                                 "position_rule": "qubit 0, rotation theta[l, 0, 0]; EARLY l = 0, MIDDLE l = floor(d/2), LATE l = d - 1"},
                                                indent=2))
    if "audit" in phases:
        phase_audit(cfg, out, work, a.workers, log)
    if "rx" in phases:
        phase_rx(cfg, out, work, a.workers, log, a.smoke)
    if "sweep" in phases:
        phase_sweep(cfg, out, work, a.workers, log)
    if "analyse" in phases:
        phase_analyse(cfg, out, work, log)
    if "sign" in phases:
        phase_sign(cfg, out, work, log)
    if "a2" in phases:
        from qlo.b1 import a2_compare as A2

        A2.phase_a2(cfg, out, ROOT, log)


if __name__ == "__main__":
    main()
