"""Section 21: comparison with the principal A2 numerics. Run LAST, after every B1 number has been written.

The rule was timestamped in numerics_log.md before any A2 number was read:
  * corresponding cells only: same family, same depth rule, same parameter (A2 shifted the first rotation on qubit 0
    of the repo HEA = B1 hea_ring EARLY);
  * B1 slopes are refitted on A2's n range from B1's own per-seed medians (B1 has even n only, A2 also used odd n);
  * agreement = the A2 value lies inside B1's 10-seed 95% percentile interval (A2 is one replicate of 4,000 theta per n,
    the same per-seed size as B1). The B1 bootstrap CI of the seed mean is shown alongside.
A2 values are read from principal/a2_numerics/general_scaling_results.json (its own fits); nothing from A2 enters any
other B1 table.
"""

from __future__ import annotations

import json

import pandas as pd

from qlo.b1 import config as CF
from qlo.b1 import fits as FT
from qlo.hardening import intervals as IV

# A2 key -> (B1 family, B1 regime, B1 position, A2 description)
CELLS = {"rx_product": ("rx_product", "product", "k=0", "RX product (A2 regression arm)"),
         "hea_shallow": ("hea_ring", "d2", "EARLY", "HEA depth 2, first rotation on qubit 0"),
         "hea_deep": ("hea_ring", "dn", "EARLY", "HEA depth n, first rotation on qubit 0")}
A2_SLOPES = {"b_S": ("med_log10_S", -1.0), "b_r": ("med_log10_rel", -1.0), "b_LE": ("med_log10_M_LE", 1.0), "b_SWAP": ("med_log10_M_SW", 1.0)}


def b1_on_range(med: pd.DataFrame, family: str, regime: str, position: str, n_range, cfg: CF.B1Config) -> dict:
    sub = med[(med.family == family) & (med.regime == regime) & (med.position == position)]
    fits = pd.DataFrame([FT.seed_fit(g, n_range) for _, g in sub.groupby("seed", sort=True)])
    return {m: IV.summarize(fits[m].values, cfg.n_boot_seed, cfg.boot_seed) for m in ("b_S", "b_r", "b_LE", "b_SWAP", "gap_obs", "ratio_obs")}


def phase_a2(cfg: CF.B1Config, out, root, log) -> pd.DataFrame:
    a2 = json.loads((root / "principal" / "a2_numerics" / "general_scaling_results.json").read_text(encoding="utf-8"))
    med = pd.read_csv(out / "sample_summary.csv")
    rows = []
    for key, (fam, reg, pos, desc) in CELLS.items():
        block = a2[key]
        a2_n = [r["n"] for r in block["rows"] if r["n"] >= block["fit_from_n"]]
        b1_grid = set(med[(med.family == fam) & (med.regime == reg)].n)
        n_range = tuple(sorted(n for n in a2_n if n in b1_grid))
        s = b1_on_range(med, fam, reg, pos, n_range, cfg)
        f = block["fits"]
        a2v = {m: sign * f[col]["slope"] for m, (col, sign) in A2_SLOPES.items()}
        a2v["gap_obs"] = a2v["b_SWAP"] - a2v["b_LE"]
        a2v["ratio_obs"] = f["slope_ratio_SW_over_LE"]
        for m, v in a2v.items():
            b = s[m]
            rows.append({"family": fam, "depth": {"product": "-", "d2": "2", "dn": "n"}[reg], "parameter": pos, "a2_cell": desc,
                         "a2_n_fit": f"{min(a2_n)}-{max(a2_n)} (all n)", "b1_n_fit": f"{min(n_range)}-{max(n_range)} (even n)",
                         "metric": m, "a2": v, "b1_mean": b["mean"], "b1_pct_lo": b["pct_lo"], "b1_pct_hi": b["pct_hi"],
                         "b1_boot_lo": b["boot_lo"], "b1_boot_hi": b["boot_hi"], "a2_minus_b1_mean": v - b["mean"],
                         "agreement": bool(b["pct_lo"] <= v <= b["pct_hi"])})
    df = pd.DataFrame(rows)
    df.to_csv(out / "a2_comparison.csv", index=False)
    log(f"a2: {len(df)} comparisons over {len(CELLS)} corresponding cells; A2 inside B1 seed 95% interval: {int(df.agreement.sum())}/{len(df)}; "
        f"max |A2 - B1 mean| = {df.a2_minus_b1_mean.abs().max():.4f}")
    return df
