"""Committed result files used by the paper figures, with the columns each figure needs.

Every figure reads its data through ``table()`` / ``doc()``, which check that the file and the required columns
exist and record the file for the manifest. No scientific value is typed into the plotting code.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]

TABLES = {
    "stage7_scaling": ("results/stage7/scaling_summary.csv",
                       ["n", "scheme", "snr1_log10M_median", "snr1_log10M_q25", "snr1_log10M_q75"]),
    "b3_stage7_intervals": ("results/b3_hardening/stage7_interval_check.csv",
                            ["fit_range", "metric", "stage7_estimate", "seed_pct_lo", "seed_pct_hi", "theta_lo", "theta_hi"]),
    "b3_sign_law": ("results/b3_hardening/sign_law_summary.csv",
                    ["n", "shots", "deep_regime", "prediction_fixed", "reference_sample_median_of_prediction",
                     "reference_observed_median_accurate", "SEED_pct_lo", "SEED_pct_hi"]),
    "b1_sign": ("results/b1_entangling/conditional_sign_summary.csv",
                ["family", "regime", "position", "n", "M", "M_times_S", "abs_r", "p_correct_given_nonzero", "predicted", "error"]),
    "b1_main": ("results/b1_entangling/main_table.csv",
                ["family", "regime", "position", "fit_range", "n_seeds"] +
                [f"{m}{s}" for m in ("b_S", "b_r", "gap_obs", "eps_gap", "ratio_obs", "ratio_pred") for s in ("", "_ci_lo", "_ci_hi")]),
    "b2_required": ("results/b2_estimators/required_shots_rx.csv",
                    ["seed", "n", "rho", "estimator", "n_samples", "median_log10_total_executions", "q25_log10_total", "q75_log10_total"]),
    "b2_slopes": ("results/b2_estimators/slope_summary.csv",
                  ["estimator", "fit_range", "quantity", "stage7_population_slope", "replicate_pct_lo", "replicate_pct_hi", "replicate_n_seeds"]),
    "b2_fixed": ("results/b2_estimators/fixed_budget_failure_modes.csv",
                 ["n", "total_executions", "estimator", "M_internal", "method", "median_P_zero", "median_P_correct",
                  "median_P_correct_given_nonzero"]),
    "b4_window": ("results/b4_noise/window_slopes.csv", ["model", "p", "family", "n_mid", "n_lo", "n_hi", "b_LE", "b_SWAP"]),
    "b4_pred": ("results/b4_noise/predictions_vs_measured.csv",
                ["model", "p", "family", "regime", "position", "fit_range", "measured_b_S", "measured_ratio_obs", "asym_ratio"]),
    "b4_crossover": ("results/b4_noise/crossover.csv", ["family", "regime", "position", "p", "n_star", "note"]),
}
DOCS = {
    "stage7_fits": "results/stage7/scaling_fits.json",
    "b4_config": "results/b4_noise/config.json",
    "stage7_config": "results/stage7/config.json",
}

USED: dict[str, str] = {}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _record(rel: str) -> Path:
    p = ROOT / rel
    if not p.exists():
        raise FileNotFoundError(f"paper figures need the committed file {rel}")
    USED[rel] = sha256(p)
    return p


def table(name: str) -> pd.DataFrame:
    rel, cols = TABLES[name]
    df = pd.read_csv(_record(rel))
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise KeyError(f"{rel} lacks columns {missing}")
    return df


def doc(name: str) -> dict:
    return json.loads(_record(DOCS[name]).read_text(encoding="utf-8"))
