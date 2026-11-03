"""Methods and appendix tables from committed files (Phase 8 I4).

    python -m qlo.paper.methods_tables      # -> paper/appendix/*.csv, APPENDIX_TABLES.md, PROVENANCE.md

Every cell value comes from one of four places, recorded in the row's `provenance` column:
  * j(path, key...)   a value read from a committed JSON file;
  * c(path, ...)      a value computed from a committed CSV (max error, count, ...);
  * q(path, text)     a verbatim quote, checked to occur in the committed file (the cell may restate it in plain form);
  * na(reason) / NOT RECORDED   nothing applicable / nothing recorded (never an estimate).
The run fails if a file, key or quote is missing, so no row can exist without a source.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "paper" / "appendix"
NR = "NOT RECORDED"

S1, S2, S3, S4, S5, S6, S7 = (f"docs/stages/{n}.md" for n in ("STAGE1_STATUS", "STAGE2", "STAGE3", "STAGE4", "STAGE5", "STAGE6", "STAGE7"))
B1D, B1C, B1L = "docs/b1/B1_ENTANGLING_SWEEPS.md", "docs/b1/B1_CONFIG.md", "results/b1_entangling/numerics_log.md"
B2D, B2L = "docs/b2/B2_ADDITIONAL_ESTIMATORS.md", "results/b2_estimators/numerics_log.md"
B3D, B4D, B4L = "docs/b3/B3_STATISTICAL_HARDENING.md", "docs/b4/B4_NOISE_OVERLAY.md", "results/b4_noise/numerics_log.md"
A2, REPRO = "docs/theory/A2_PROPOSITIONS.md", "docs/phase8/REPRODUCTION_STATUS.md"

_cache: dict[str, str] = {}


def _text(rel: str) -> str:
    if rel not in _cache:
        p = ROOT / rel
        if not p.exists():
            raise FileNotFoundError(rel)
        _cache[rel] = p.read_text(encoding="utf-8")
    return _cache[rel]


def q(rel: str, text: str, value=None) -> tuple:
    if text not in _text(rel):
        raise ValueError(f"quote not found in {rel}: {text!r}")
    return (text if value is None else value), f'{rel}: "{text}"'


def j(rel: str, *keys) -> tuple:
    v = json.loads(_text(rel))
    for k in keys:
        v = v[k]
    return v, f"{rel}: {'.'.join(map(str, keys))}"


def c(rel: str, how: str, value) -> tuple:
    if not (ROOT / rel).exists():
        raise FileNotFoundError(rel)
    return value, f"{rel}: {how}"


def na(reason: str) -> tuple:
    return "N/A", f"not applicable: {reason}"


def nr(searched: str) -> tuple:
    return NR, f"no value in {searched}"


def csv_(rel: str) -> pd.DataFrame:
    return pd.read_csv(ROOT / rel)


def nrange(v) -> str:
    v = [int(x) for x in v]
    d = np.diff(v)
    return f"{v[0]}–{v[-1]} (step {d[0]})" if len(v) > 2 and (d == d[0]).all() else ", ".join(map(str, v))


def row(**fields) -> dict:
    out, prov = {}, []
    for k, val in fields.items():
        if isinstance(val, tuple):
            v, p = val
            out[k] = "; ".join(map(str, v)) if isinstance(v, list) else v
            prov.append(f"{k} <- {p}")
        else:
            out[k] = val
    out["provenance"] = " | ".join(prov)
    return out


def g(x: float) -> str:
    return f"{x:.3g}" if x != 0 else "0"


# =================================================================================================================
def configuration_rows() -> list[dict]:
    R = []
    c3, c4, c5, c6, c7 = (f"results/stage{n}/config.json" for n in (3, 4, 5, 6, 7))
    n3, _ = j(c3, "n_values")
    R.append(row(
        experiment="Stage 3", purpose=q(S3, "Controlled barren-plateau benchmark"),
        circuit_family=q(S3, "`V(θ) = ⊗_j RX(θ_j)`", "RX product V(θ) = ⊗_j RX(θ_j); global and local costs"),
        target=q(S3, "target `|0>^n`", "|0^n⟩"), n_range=(nrange(n3), f"{c3}: n_values"), depth=na("product circuit (one RX layer)"),
        parameter_position=na("product circuit"), theta_distribution=q(S3, "`θ_j ~ iid U[-π, π]`", "θ_j iid U[−π, π]"),
        number_of_theta=(f"{j(c3, 'n_init')[0]} per n", f"{c3}: n_init"), number_of_seeds=(f"1 (master_seed {j(c3, 'master_seed')[0]})", f"{c3}: master_seed"),
        shot_budgets=q(S3, "The Monte Carlo sweep uses the closed-form gradients", "N/A (exact closed-form gradients, no shots)"),
        gradient_component=(f"k = {j(c3, 'parameter_index')[0]}", f"{c3}: parameter_index"), optimizer_iterations=na("no optimizer"),
        fit_range=(f"log Var vs n over {j('results/stage3/global_fit.json', 'n_points')[0]} points (n = {nrange(n3)})", "results/stage3/global_fit.json: n_points, model"),
        CI_method=("exact relative SE of the sample variance per n", j("results/stage3/global_fit.json", "variance_rel_se_exact_by_n")[1]),
        config_source=c3, result_source="results/stage3/"))
    R.append(row(
        experiment="Stage 4", purpose=q(S4, "Does finite-shot stochasticity help escape a verified barren plateau?"),
        circuit_family=q(S4, "on the Stage 3 global benchmark", "RX product (Stage 3 global benchmark)"), target=q(S4, "`F = |<0^n|ψ>|² = ∏ cos²(θ_j/2)`", "|0^n⟩"),
        n_range=(nrange(j(c4, "eval_n")[0]) + " (evaluation)", f"{c4}: eval_n"), depth=na("product circuit"), parameter_position=na("product circuit"),
        theta_distribution=q(S4, "`θ_j ~ U[−π,π]`", "θ_j U[−π, π] (start points)"),
        number_of_theta=(f"evaluation start seeds {j(c4, 'evaluation_start_seeds')[0][0]}–{j(c4, 'evaluation_start_seeds')[0][1]}; tuning start seeds "
                         f"{j(c4, 'tuning_start_seeds')[0][0]}–{j(c4, 'tuning_start_seeds')[0][1]}", f"{c4}: evaluation_start_seeds, tuning_start_seeds"),
        number_of_seeds=q(S4, "A: 1 trajectory / seed; B, C, D, E and the controls: 5 replicates / seed (500 runs per cell).",
                          "100 evaluation start seeds; 1 trajectory per seed (exact GD), 5 replicates per seed otherwise"),
        shot_budgets=(", ".join(map(str, j(c4, "sgd_shots")[0])) + " shots per shifted circuit", f"{c4}: sgd_shots"),
        gradient_component=q(S4, "with an independent M-shot batch for every\n(k, ±), iteration and replicate", "all components k, an independent batch per (k, ±) and iteration"),
        optimizer_iterations=(j(c4, "n_iters")[0], f"{c4}: n_iters"), fit_range=na("optimization study, no scaling fit"),
        CI_method=q(S4, "paired by start seed, 10 000-sample bootstrap", "paired bootstrap (10,000 samples); Wilson 95% CIs for success probabilities"),
        config_source=c4, result_source="results/stage4/"))
    R.append(row(
        experiment="Stage 5", purpose=q(S5, "Finite-shot gradient dead zones on the controlled projector benchmark"),
        circuit_family=q(S5, "`|ψ(θ)> = ⊗_j RX(θ_j)|0^n>`", "RX product (projector / Loschmidt readout)"), target=q(S5, "`|ψ(θ)> = ⊗_j RX(θ_j)|0^n>`", "|0^n⟩"),
        n_range=(nrange(j(c5, "n_values")[0]), f"{c5}: n_values"), depth=na("product circuit"), parameter_position=na("product circuit"),
        theta_distribution=q(S5, "`θ_j ~ iid U[−π, π]`", "θ_j iid U[−π, π]"),
        number_of_theta=(f"{j(c5, 'n_samples')[0]} per n", f"{c5}: n_samples"), number_of_seeds=(f"1 (sample_seed {j(c5, 'sample_seed')[0]})", f"{c5}: sample_seed"),
        shot_budgets=(", ".join(map(str, j(c5, "deadzone_shots")[0])) + " (dead-zone grid)", f"{c5}: deadzone_shots"),
        gradient_component=q(S5, "For component k", "component k (A_k, s_k)"), optimizer_iterations=na("no optimizer"),
        fit_range=(f"median log10 M vs n, n = {nrange(j(c5, 'n_values')[0])}", "results/stage5/scaling_fits.json"),
        CI_method=q(S5, "exact `P₀` inside the Wilson 95 % CI", "Wilson 95% CIs (Monte Carlo validation)"), config_source=c5, result_source="results/stage5/"))
    R.append(row(
        experiment="Stage 6", purpose=q(S6, "Do all finite-shot barren plateaus fail the same way?"),
        circuit_family=q(S6, "Two analytically controlled global barren plateaus on the same circuit", "RX product; projector and global Pauli-parity costs"),
        target=na("parity cost has no target state; projector cost targets |0^n⟩ (Stage 5)"), n_range=(nrange(j(c6, "n_values")[0]), f"{c6}: n_values"),
        depth=na("product circuit"), parameter_position=na("product circuit"), theta_distribution=q(S5, "`θ_j ~ iid U[−π, π]`", "θ_j iid U[−π, π] (frozen Stage 3–5 landscape)"),
        number_of_theta=(f"{j(c6, 'n_samples')[0]} per n", f"{c6}: n_samples"), number_of_seeds=(f"1 (sample_seed {j(c6, 'sample_seed')[0]})", f"{c6}: sample_seed"),
        shot_budgets=(", ".join(map(str, j(c6, "failure_shots")[0])) + " (failure grid)", f"{c6}: failure_shots"), gradient_component=q(S5, "For component k", "component k"),
        optimizer_iterations=(f"{j(c6, 'retro_iters')[0]} (retrodiction only)", f"{c6}: retro_iters"),
        fit_range=(f"median log10 M vs n, n = {nrange(j(c6, 'n_values')[0])}", "results/stage6/scaling_fits.json"),
        CI_method=q(S6, "Raw Wilson-CI coverage", "Wilson CIs"), config_source=c6, result_source="results/stage6/"))
    R.append(row(
        experiment="Stage 7", purpose=q(S7, "Stage 7 is a replication /", "same landscape, Loschmidt vs SWAP readout (replication / specialization / extension test)"),
        circuit_family=q(S7, "`|ψ(θ)⟩ = ⊗_j RX(θ_j)|0ⁿ⟩`", "RX product"), target=q(S7, "target `|0ⁿ⟩`", "|0^n⟩"),
        n_range=(nrange(j(c7, "n_values")[0]), f"{c7}: n_values"), depth=na("product circuit"), parameter_position=na("product circuit"),
        theta_distribution=q(S7, "θ_j ~ iid U[−π, π]", "θ_j iid U[−π, π]"),
        number_of_theta=(f"{j(c7, 'n_samples')[0]} per n (required shots)", f"{c7}: n_samples"), number_of_seeds=(f"1 (seed {j(c7, 'seed')[0]})", f"{c7}: seed"),
        shot_budgets=(f"paired {j(c7, 'paired_shots')[0]}; vector {j(c7, 'vector_shots')[0]}", f"{c7}: paired_shots, vector_shots"),
        gradient_component=q(S7, "k = 0, the same θ for both schemes", "k = 0"),
        optimizer_iterations=(f"{j(c7, 'opt_iters')[0]} ({j(c7, 'opt_seeds')[0]} paired starts per variant)", f"{c7}: opt_iters, opt_seeds"),
        fit_range=("n = 2–20 (10 points); n ≥ 8 secondary", "results/stage7/scaling_fits.json: n_points, slope_n_ge_8"),
        CI_method=q(S7, "the Wilson CIs overlap", "Wilson CIs (optimization); no seed replicates (B3 adds them)"), config_source=c7, result_source="results/stage7/"))
    b1 = "results/b1_entangling/config.json"
    R.append(row(
        experiment="B1", purpose=q("src/qlo/experiments/b1_entangling.py", "an independent empirical test of the principal-track A2 scaling rule",
                                   "independent empirical test of the principal-track A2 scaling rule (entangling circuits)"),
        circuit_family=q(B1D, "| families | `rx_product` (Family 0, regression), `hea_ring` (Family 1, repo HEA), `rxry_czbrick` (Family 2, fallback) |",
                         "RX product (regression arm); HEA ring (RY, RZ, CNOT ring); RX-RY CZ brickwork"),
        target=q(B1D, "Target |0^n⟩, θ iid U[−π, π].", "|0^n⟩"),
        n_range=q(B1D, "| n grids | d2 and d4: 4–16 (even); depth = n: 4–14 (even); RX: 2–20 (even) |", "d2, d4: 4–16 (even); depth n: 4–14 (even); RX: 2–20 (even)"),
        depth=q(B1D, "| depth regimes | 2, 4, depth = n |", "2, 4, n"),
        parameter_position=q(B1D, "EARLY l = 0, MIDDLE l = floor(d/2), LATE l = d−1", "qubit 0, θ[l,0,0]; EARLY l = 0, MIDDLE l = floor(d/2), LATE l = d−1"),
        theta_distribution=q(B1D, "Target |0^n⟩, θ iid U[−π, π].", "θ iid U[−π, π]"),
        number_of_theta=(f"{j(b1, 'samples_per_cell')[0]} per (family, regime, n, seed); RX {j(b1, 'rx_samples')[0]} per (seed, n)", f"{b1}: samples_per_cell, rx_samples"),
        number_of_seeds=(f"{len(j(b1, 'seeds')[0])} ({j(b1, 'seeds')[0][0]}–{j(b1, 'seeds')[0][-1]})", f"{b1}: seeds"),
        shot_budgets=q(B1D, "continuous exact M at SNR 1", "continuous exact M at SNR = 1 (no sampled shots)"),
        gradient_component=q(B1D, "qubit 0, θ[l,0,0]", "θ[l,0,0] at the three positions"), optimizer_iterations=na("no optimizer"),
        fit_range=q(B1D, "| fit ranges | primary = full grid; secondary = n ≥ 8 |", "primary = full grid; secondary = n ≥ 8"),
        CI_method=q(B1D, "primary = bootstrap 95% CI of the seed mean", "bootstrap 95% CI of the 10-seed mean (10,000 replicates, seed 2026)"),
        config_source=B1C, result_source="results/b1_entangling/"))
    b2 = "results/b2_estimators/config.json"
    R.append(row(
        experiment="B2", purpose=q("src/qlo/experiments/b2_estimators.py", "four fidelity-gradient estimators on the frozen Stage 7 RX-product landscape"),
        circuit_family=q("src/qlo/experiments/b2_estimators.py", "spot (secondary entangling spot check)", "RX product (Stage 7 landscape); secondary HEA depth-n spot check"),
        target=q(S7, "target `|0ⁿ⟩`", "|0^n⟩"), n_range=(f"{nrange(j(b2, 'rx_n')[0])}; spot check {nrange(j(b2, 'spot_n')[0])}", f"{b2}: rx_n, spot_n"),
        depth=na("product circuit (spot check: HEA depth n)"), parameter_position=na("product circuit"), theta_distribution=q(S7, "θ_j ~ iid U[−π, π]", "θ_j iid U[−π, π] (Stage 7 streams)"),
        number_of_theta=(f"{j(b2, 'stage7_samples')[0]} (Stage 7 population); {j(b2, 'replicate_samples')[0]} per replicate seed", f"{b2}: stage7_samples, replicate_samples"),
        number_of_seeds=(f"Stage 7 seed {j(b2, 'stage7_seed')[0]} + {len(j(b2, 'replicate_seeds')[0])} replicate seeds ({j(b2, 'replicate_seeds')[0][0]}–{j(b2, 'replicate_seeds')[0][-1]})", f"{b2}: stage7_seed, replicate_seeds"),
        shot_budgets=(f"fixed budgets {j(b2, 'budgets_total_executions')[0]} total executions; required shots per θ by the frozen Stage 7 solver "
                      "(integer budgets; exact integer inversion for Hadamard)", f"{b2}: budgets_total_executions; src/qlo/b2/required_shots.py docstring"),
        gradient_component=q(S7, "k = 0, the same θ for both schemes", "k = 0"), optimizer_iterations=na("no optimizer"),
        fit_range=(", ".join(f"{a} (n {b}–{c_})" for a, b, c_ in j(b2, "fit_ranges")[0]), f"{b2}: fit_ranges"),
        CI_method=(f"95% percentile interval over {len(j(b2, 'replicate_seeds')[0])} replicate seeds; bootstrap {j(b2, 'n_boot_seed')[0]} replicates", f"{b2}: replicate_seeds, n_boot_seed"),
        config_source="docs/b2/B2_CONFIG.md", result_source="results/b2_estimators/"))
    b3 = "results/b3_hardening/config.json"
    R.append(row(
        experiment="B3", purpose=q("src/qlo/experiments/b3_hardening.py", "B3 statistical hardening of Stage 7", "statistical hardening of Stage 7 (independent seeds, intervals, n extension)"),
        circuit_family=q(B3D, "Anything beyond the RX-product circuit", "RX product (Stage 7)"), target=q(B3D, "the |0ⁿ⟩ target", "|0^n⟩"),
        n_range=(f"{nrange(j(b3, 'primary_n')[0])}; extension {', '.join(map(str, j(b3, 'extension_n')[0]))}", f"{b3}: primary_n, extension_n"),
        depth=na("product circuit"), parameter_position=na("product circuit"), theta_distribution=q(B3D, "U[−π, π] initialization", "θ_j iid U[−π, π]"),
        number_of_theta=(f"{j(b3, 'seed_samples')[0]} per (seed, n); reference {j(b3, 'reference_samples')[0]}", f"{b3}: seed_samples, reference_samples"),
        number_of_seeds=(f"{len(j(b3, 'seeds')[0])} ({j(b3, 'seeds')[0][0]}–{j(b3, 'seeds')[0][-1]}) + Stage 7 reference seed {j(b3, 'reference_seed')[0]}", f"{b3}: seeds, reference_seed"),
        shot_budgets=(f"fixed shots {j(b3, 'fixed_shots')[0]}; required shots per θ by the Stage 7 solver (reproduces Stage 7 exactly)",
                      f"{b3}: fixed_shots; results/b3_hardening/run_meta.json: stage7_reproduction.exact"),
        gradient_component=q(B3D, "component k = 0", "k = 0"),
        optimizer_iterations=(f"{j(b3, 'opt_iters')[0]} ({j(b3, 'opt_starts_per_seed')[0]} starts per seed)", f"{b3}: opt_iters, opt_starts_per_seed"),
        fit_range=("primary_2_20, n_ge_8, extended_2_24", "results/b3_hardening/run_meta.json: fit_ranges"),
        CI_method=q(B3D, "The predeclared primary criterion is the SEED 95% percentile interval", "SEED 95% percentile interval (primary); THETA bootstrap CI (secondary)"),
        config_source=b3, result_source="results/b3_hardening/"))
    b4 = "results/b4_noise/config.json"
    R.append(row(
        experiment="B4", purpose=q(B4D, "B4: depolarizing-noise overlay", "depolarizing-noise overlay on the Stage 7 RX product and the B1 cells"),
        circuit_family=q(B4D, "RX product (L = 1); all 16 B1 cells (L = 2, 4 or n)", "RX product (global and local noise); 16 B1 entangling cells (global noise)"),
        target=q(B1D, "Target |0^n⟩, θ iid U[−π, π].", "|0^n⟩"), n_range=(f"RX {nrange(j(b4, 'rx_n')[0])}; entangling cells as B1", f"{b4}: rx_n"),
        depth=q(B4D, "L = 2, 4 or n", "RX: L = 1; B1 cells: L = 2, 4 or n"), parameter_position=q(B4D, "same θ, seeds, circuits and positions", "as B1"),
        theta_distribution=q(B4D, "same θ, seeds, circuits and positions", "the B1 θ populations (reused per-θ caches)"),
        number_of_theta=(f"RX {j(b4, 'rx_samples')[0]} per (seed, n); entangling cells as B1", f"{b4}: rx_samples"),
        number_of_seeds=(f"{len(j(b4, 'seeds')[0])} ({j(b4, 'seeds')[0][0]}–{j(b4, 'seeds')[0][-1]})", f"{b4}: seeds"),
        shot_budgets=q(B1D, "continuous exact M at SNR 1", "N/A (continuous required shots at SNR 1, as B1)"), gradient_component=q(B4D, "same θ, seeds, circuits and positions", "as B1 (RX: k = 0)"),
        optimizer_iterations=na("no optimizer"),
        fit_range=(f"primary = full grid; secondary = n ≥ {j(b4, 'secondary_n_min')[0]}; {j(b4, 'window')[0]}-point local windows", f"{b4}: secondary_n_min, window"),
        CI_method=(f"bootstrap of the seed mean ({j(b4, 'n_boot_seed')[0]} replicates, seed {j(b4, 'boot_seed')[0]})", f"{b4}: n_boot_seed, boot_seed"),
        config_source="docs/b4/B4_CONFIG.md", result_source="results/b4_noise/"))
    return R


# =================================================================================================================
def validation_rows() -> list[dict]:
    R = []

    def v(check, quantity, reference, observed, tolerance, status, src, loc):
        R.append(row(check=check, quantity=quantity, reference=reference, observed_error=observed, tolerance=tolerance, status=status,
                     source_file=src, source_location=loc))

    v("analytic gradient vs autograd", "PennyLane backprop (autograd) gradient vs closed form, Stage 3 benchmark (global / local cost)", "closed form (NumPy)",
      q(S3, "| PennyLane backprop gradient vs closed form | 1.1e-19 (global), 5.6e-17 (local) |", "1.1e-19 (global), 5.6e-17 (local)"), na("not stated"), "reported", S3,
      "Closed-form validation")
    v("parameter-shift vs autograd", "PennyLane autograd vs parameter-shift gradient (HEA smoke circuits)", "parameter-shift rule",
      q(S1, "| autograd vs parameter-shift                  | 4.4e-16      |", "4.4e-16"), na("not stated"), "reported", S1, "gradient cross-check table")
    v("finite-difference cross-check", "autograd vs central finite difference (h = 1e-5)", "central finite difference",
      q(S1, "| autograd vs central finite-diff (h=1e-5)     | 6.8e-11      |", "6.8e-11"), na("not stated"), "reported", S1, "gradient cross-check table")
    v("Stage 3 closed form vs PennyLane", "PennyLane parameter-shift gradient vs closed form (global / local cost)", "closed form (NumPy)",
      q(S3, "| PennyLane parameter-shift gradient vs closed form | 1.2e-18 (global), 7.3e-17 (local) |", "1.2e-18 (global), 7.3e-17 (local)"),
      na("not stated"), "reported", S3, "Closed-form validation")
    v("Stage 3 closed form vs finite difference", "closed-form gradient vs central finite difference", "central finite difference",
      q(S3, "| closed-form gradient vs central finite difference | < 1e-8 |", "< 1e-8"), na("not stated"), "reported", S3, "Closed-form validation")
    v("projector variance Monte Carlo (Stage 5)", "empirical / analytic variance of the projector gradient", "exact binomial variance",
      q(S5, "empirical/analytic variance 0.92–1.06", "ratio 0.92–1.06 (75 cells, 20,000 replicates)"), na("sampling"), "reported", S5, "Validation summary")
    v("Stage 5 exact distribution", "exact P0 vs brute-force enumeration", "brute force",
      q(S5, "`P₀` vs brute force: 2.6e-15 (M<80), 1e-11 relative (M = 2×10⁶)", "2.6e-15 (M < 80); 1e-11 relative (M = 2e6)"), na("not stated"), "reported", S5, "Validation summary")
    v("Stage 6 exact / normal approximations", "exact difference-of-binomials code vs brute force", "brute force",
      q(S6, "matches brute force to 4.5e-14 at small M", "4.5e-14 (small M); central-binomial identity 4e-9 at M = 1e6"), na("not stated"), "reported", S6,
      "Validation summary")
    v("Stage 7 common-gradient identity", "LE and SWAP estimate the same exact gradient (n = 2–20)", "closed form",
      q(S7, "Common-gradient identity ≤ 1.7e-16 for n = 2…20", "≤ 1.7e-16"), na("not stated"), "reported", S7, "Validation summary")
    v("Stage 7 PennyLane SWAP validation", "P_zero inside the PennyLane Wilson CI (Loschmidt / SWAP)", "explicit PennyLane circuits",
      q(S7, "| P_zero in Wilson CI | 27/27 | 25/27 |", "27/27 / 25/27 cells"), na("sampling (Wilson 95% CI)"), "reported", S7, "§16")
    fk = "results/b1_entangling/fused_kernel_validation.csv"
    v("B1 fused kernel vs reference", "max |ΔF±|/S, fused vs audited per-qubit kernel (40 cells)", "audited per-qubit kernel",
      c(fk, "max(max_rel_err_Fpm_over_S)", g(csv_(fk).max_rel_err_Fpm_over_S.max())), na("not stated"), "reported", fk, "max_rel_err_Fpm_over_S")
    v("B1 gradient checks", "max agreement error |diff|/S over all audit rows (PennyLane-checked 140/140)", "PennyLane autograd and parameter shift",
      q(B1L, "max agreement error (|diff|/S) over all rows: 3.17e-13", "3.17e-13"), (f"{j('results/b1_entangling/config.json', 'audit_agreement_tol')[0]}·S", "results/b1_entangling/config.json: audit_agreement_tol"),
      "pass", B1L, "phases=audit")
    ri = "results/b1_entangling/ratio_identity_validation.csv"
    d = csv_(ri)
    v("B1 exact shot-ratio identity", f"max relative error of M_SW/M_LE = (2−Q)/(S−Q) over {int(d.n_checked.sum()):,} θ rows ({int(d.n_excluded.sum())} excluded)",
      "Proposition 1", c(ri, "max(max_rel_err), sum(n_checked), sum(n_excluded)", g(d.max_rel_err.max())),
      (j("results/b1_entangling/config.json", "identity_rel_tol")[0], "results/b1_entangling/config.json: identity_rel_tol"),
      ("pass" if bool(d.passes.all()) else "fail", f"{ri}: passes"), ri, "max_rel_err")
    ds = "results/b2_estimators/destructive_swap_validation.csv"
    v("B2 destructive vs ancilla SWAP", "max |P(+1) ancilla − destructive| (circuit level)", "ancilla SWAP / (1+F)/2",
      c(ds, "max(abs_err_ancilla_vs_destructive)", g(csv_(ds).abs_err_ancilla_vs_destructive.max())),
      (j("results/b2_estimators/config.json", "swap_equality_tol")[0], "results/b2_estimators/config.json: swap_equality_tol"), "pass", ds, "abs_err_ancilla_vs_destructive")
    hc = "results/b2_estimators/hadamard_circuit_validation.csv"
    v("B2 Hadamard circuit validation", "max error of Hadamard-test expectations vs Re/Im of the overlap (NumPy and PennyLane)", "exact overlap",
      c(hc, "max(max_abs_err)", g(csv_(hc).max_abs_err.max())), (j("results/b2_estimators/config.json", "circuit_tol")[0], "results/b2_estimators/config.json: circuit_tol"),
      "pass", hc, "max_abs_err")
    hv = "results/b2_estimators/hadamard_variance_validation.csv"
    e = csv_(hv).dropna(subset=["exact_var_err"])
    v("B2 U-statistic exact enumeration", "max |bias|, |variance error| by exact enumeration", "variance formula",
      c(hv, "max(|exact_bias|, |exact_var_err|)", g(max(e.exact_bias.abs().max(), e.exact_var_err.abs().max()))),
      (j("results/b2_estimators/config.json", "variance_tol")[0], "results/b2_estimators/config.json: variance_tol"), "pass", hv, "exact_bias, exact_var_err")
    sr = "results/b2_estimators/stage7_regression.csv"
    v("B2 Stage 7 regression", "max |median log10 M| difference vs Stage 7 (LE / SWAP, SNR 1 and 2)", "results/stage7/scaling_summary.csv",
      c(sr, "max(abs_diff)", g(csv_(sr).abs_diff.max())), ("1e-12", "src/qlo/experiments/b2_estimators.py: phase_rx STOP threshold"), "pass", sr, "abs_diff")
    rm = "results/b3_hardening/run_meta.json"
    v("B3 independent seed replication (Stage 7 reproduction)", f"max |median log10 M| difference on the regenerated Stage 7 population ({j(rm, 'stage7_reproduction', 'cells')[0]} cells)",
      "results/stage7/scaling_summary.csv", (g(j(rm, "stage7_reproduction", "max_abs_diff_median_log10M")[0]), j(rm, "stage7_reproduction", "max_abs_diff_median_log10M")[1]),
      na("exact reproduction required"), ("pass" if j(rm, "stage7_reproduction", "exact")[0] else "fail", f"{rm}: stage7_reproduction.exact"), rm, "stage7_reproduction")
    ic = "results/b3_hardening/stage7_interval_check.csv"
    icd = csv_(ic)
    icd = icd[icd.inside_seed_pct_interval.isin([True, False, "True", "False"])]
    inside = int(icd.inside_seed_pct_interval.astype(str).eq("True").sum())
    v("B3 Stage 7 slopes inside seed intervals", "Stage 7 slope estimates inside the B3 SEED 95% percentile interval", "20 independent seeds",
      c(ic, "count(inside_seed_pct_interval)", f"{inside}/{len(icd)} inside"), na("predeclared criterion"), "reported", ic, "inside_seed_pct_interval")
    vb = "results/b4_noise/validation.csv"
    v("B4 density-matrix validation", "max |noise overlay − PennyLane default.mixed| (global and local)", "density-matrix simulation",
      c(vb, "max(abs_err)", g(csv_(vb).abs_err.max())), (j("results/b4_noise/config.json", "validate_tol")[0], "results/b4_noise/config.json: validate_tol"),
      "pass", vb, "abs_err")
    rp = "results/b4_noise/regression_p0_vs_b1.csv"
    v("B4 p = 0 regression vs B1", "max |median difference| at p = 0 vs committed B1 medians", "results/b1_entangling/sample_summary.csv",
      c(rp, "max over absdiff_* columns", g(csv_(rp).filter(like="absdiff").max().max())),
      (j("results/b4_noise/config.json", "regression_tol")[0], "results/b4_noise/config.json: regression_tol"), "pass", rp, "absdiff_*")
    ri4 = "results/b4_noise/ratio_identity_validation.csv"
    d4 = csv_(ri4)
    v("B4 identity under noise", f"max relative error of the shot-ratio identity over {int(d4.n_checked.sum()):,} noisy θ rows ({int(d4.n_excluded.sum())} excluded)",
      "Proposition 1", c(ri4, "max(max_rel_err), sum(n_checked), sum(n_excluded)", g(d4.max_rel_err.max())),
      (j("results/b4_noise/config.json", "identity_rel_tol")[0], "results/b4_noise/config.json: identity_rel_tol"), "pass", ri4, "max_rel_err")
    v("CI cross-platform tests", "full pytest suite on GitHub-hosted runners (no PYTHONUTF8)", "local suite",
      q(REPRO, "| pytest | windows-latest, Python 3.13.16 | 279 passed, 1 skipped (no `PYTHONUTF8`) |", "ubuntu 3.12 / ubuntu 3.13 / windows 3.13: 279 passed, 1 skipped"),
      na("all tests must pass"), "pass", REPRO, "B. Automated cross-platform testing")
    return R


# =================================================================================================================
def regime_rows() -> list[dict]:
    R = []
    mt = csv_("results/b1_entangling/main_table.csv")
    mt = mt[mt.fit_range == "primary"]
    ent = mt[mt.family != "rx_product"]
    n1 = int(csv_("results/b1_entangling/ratio_identity_validation.csv").n_checked.sum())
    n4 = int(csv_("results/b4_noise/ratio_identity_validation.csv").n_checked.sum())
    eps = 100 * mt.eps_gap / mt.b_S
    sg = csv_("results/b3_hardening/sign_law_summary.csv")
    bs = csv_("results/b1_entangling/conditional_sign_summary.csv")
    gp = [p for p in j("results/b4_noise/config.json", "global_p")[0] if p > 0]
    lp = [p for p in j("results/b4_noise/config.json", "local_p_rx")[0] if p > 0]
    COMPUTED = ("computed from results/b1_entangling/{main_table,ratio_identity_validation,conditional_sign_summary}.csv, "
                "results/b4_noise/{ratio_identity_validation.csv,config.json}, results/b3_hardening/sign_law_summary.csv")

    def r(result, math, tested, assumptions, exclusions, *sources):
        R.append(row(result=result, mathematical_scope=math, tested_scope=tested, assumptions=assumptions, known_exclusions=exclusions,
                     source="; ".join([s[1] for s in sources] + [COMPUTED])))

    r("Exact shot-ratio identity", q(A2, "For every θ with Δ ≠ 0 and S − Q > 0:", "exact for every θ with Δ ≠ 0 and S − Q > 0; trial state may be mixed"),
      f"B1: {n1:,} θ rows (RX + {len(ent)} entangling cells); B4: {n4:,} noisy θ rows", "two-term shift rule (Pauli generator); one independent batch of M shots per shift; pure target; SNR target with continuous M",
      "SWAP with both copies noisy (estimates Tr(ρσ)) is not covered",
      q(A2, "It may be mixed, so noise is allowed."), q(B1D, "## 14. Exact ratio identity check"), q(B4D, "SWAP tests in which **both** copies are noisy"))
    r("Conditional sign law", q(A2, "(1 + |r|)/2 + O(M S)", "asymptotic: P(correct | ĝ_LE ≠ 0) = (1 + |r|)/2 + O(MS) as MS → 0"),
      f"B1: {len(bs)} exact (cell, θ, M) points at n = {', '.join(map(str, sorted(bs.n.unique())))}; B3: n = {sg.n.min()}–{sg.n.max()}, M = {sg.shots.min()}–{sg.shots.max():,}", "independent binomial counts at the two shifts", "not a finite-M equality; departures grow with M·S (n = 12, large M)",
      q(A2, "Let K± ~ Bin(M, F±) be independent"), q(B3D, "This is consistent with the law being an M·A → 0 limit."))
    r("Slope rule b_SWAP − b_LE = b_S", q(A2, "## 2. Proposition 2 (slope rule in the concentrated regime)", "asymptotic in n under (H1) shift family, (H2) S → 0, (H3) unique medians"),
      f"B1: {len(mt)} cells, n ≤ 16 (≤ 20 RX); B4 under depolarizing noise", "(H1)–(H3)",
      f"finite-n residual ε_gap of {eps.max():.2f}% to {eps.min():.2f}% of b_S in B1; not a finite-n identity",
      q(A2, "(H1) Shift family."), q(B1D, "## 17. Gap rule test (main B1 equation: b_SWAP − b_LE = b_S)"))
    r("Exponent doubling", q(A2, "If b_r = 0, the ratio equals 2.", "b_SW/b_LE = (2b_S + 2b_r)/(b_S + 2b_r); equals 2 only if b_r = 0"),
      f"B1: |b_r| ≤ {mt.b_r.abs().max():.4f} in every tested cell; ratio {mt.ratio_obs.min():.3f}–{mt.ratio_obs.max():.3f}", "Proposition 2 hypotheses; b_S > 0", "b_r > 0 gives a ratio between 1 and 2 (e.g. global depolarizing noise)",
      q(A2, "If b_r > 0, it lies strictly between 1 and 2."), q(B1D, "## 18. Exponent-doubling conditions"))
    r("RX-product 4ⁿ vs 16ⁿ", ("benchmark-specific (RX product, target |0ⁿ⟩, U[−π, π] θ, k = 0); not a universal base rate",
                               q(S7, "same-landscape gradient shot complexity (≈ 4ⁿ vs ≈ 16ⁿ, with measured exponents)")[1]),
      "Stage 7 (Table A1); B3 seeds and n extension (Table A1); B2 regression (Table A2)", "noiseless circuits; SNR ≥ 1 and sign targets",
      f"entangling circuits have other base rates (B1: b_S = {ent.b_S.min():.3f}–{ent.b_S.max():.3f})",
      q(S7, "same-landscape gradient shot complexity (≈ 4ⁿ vs ≈ 16ⁿ, with measured exponents)"), q(B3D, "Anything beyond the RX-product circuit"))
    r("B1 entangling generalization", ("tested regime only (not a theorem)", q(B1D, "## 25. What B1 supports")[1]),
      "HEA ring and RX-RY CZ brickwork, depths 2 / 4 / n, early / middle / late, n ≤ 16, 10 seeds", "noiseless; target |0ⁿ⟩; θ iid U[−π, π]",
      "other ansätze, targets, initialisations and n > 16 are untested", q(B1D, "## 25. What B1 supports"), q(B1D, "## 26. What B1 does not establish"))
    r("Hadamard U-statistic scaling", ("tested regime (RX product)", q(B2D, "Hadamard therefore combines **Loschmidt's exponent with SWAP's failure type**")[1]),
      "B2: RX product n = 2–20; HEA depth-n spot check n = 6–12", "coherent controlled-(V†U) access; 4M executions per gradient component",
      "execution counts are not hardware cost", q(B2D, "Hadamard therefore combines **Loschmidt's exponent with SWAP's failure type**"), q(B2D, "Hardware cost or wall-clock superiority of any estimator."))
    r("Destructive SWAP equivalence", ("identical outcome statistics to the ancilla SWAP test (exact model)", q(A2, "The ancilla and destructive (Bell-basis) SWAP tests have identical outcome statistics (B2 §5).")[1]),
      "B2: circuit validation; required shots on the Stage 7 population", "pure target copy; ±1 product-of-parities readout", "hardware depth/noise differences not assessed",
      q(A2, "The ancilla and destructive (Bell-basis) SWAP tests have identical outcome statistics (B2 §5)."), q(B2D, "## 6. Destructive SWAP validation"))
    r("Global depolarizing result", q(A2, "ρ' = q ρ + (1 − q) I/d,   q = (1 − p)^L.", "exact overlay F' = qF + (1 − q)/2ⁿ for global depolarizing after each layer; asymptotic exponents under (H1)"),
      f"B4: RX product (L = 1) and {len(ent)} B1 cells, p = {min(gp):g} to {max(gp):g}", "noise acts on the trial state only; the SWAP target copy and readout are ideal",
      "fixed-depth entangling cells are pre-asymptotic at n ≤ 16; other channels untested",
      q(B4D, "Noise acts on the trial state. The SWAP target copy is ideal"), q(B4D, "The asymptotic fixed-depth entangling exponents."))
    r("Local depolarizing result", q(A2, "## 7. Proposition 6 (local depolarizing on the product circuit) — prediction for B4", "exact only for the RX product circuit (state stays a product)"),
      f"B4: RX product, p = {', '.join(f'{p:g}' for p in lp)}", "single-qubit depolarizing after every rotation; ideal readout",
      "local depolarizing on entangling circuits is NOT tested (needs density-matrix simulation)", q(B4D, "Local depolarizing on entangling circuits. That needs density-matrix simulation"))
    return R


# =================================================================================================================
def reproduction_rows() -> list[dict]:
    R = []
    # Hardware model only where a committed source for that run names it (B1 log); every other run is documented as macOS only
    mac = q(REPRO, "Dhruv's macOS machine", "Dhruv's macOS machine; classical simulation")
    mac_m4 = q(B1L, "the M4's 4 performance\ncores busy", "Dhruv's macOS machine (Apple M4, named in the B1 log); classical simulation")

    def r(exp, cmd, platform, py, workers, wall, cpu, mem, cache, outdir, headline, log):
        R.append(row(experiment=exp, command=cmd, platform_actually_run=platform, python_version=py, workers=workers, wall_time=wall,
                     cpu_time=cpu, peak_memory=mem, cache_requirement=cache, output_directory=outdir, expected_headline_check=headline,
                     source_log=log, physical_hardware=("false", "all results are classical simulation (docs/phase8/REPRODUCTION_STATUS.md §D)")))

    for s, d in (("Stage 3", S3), ("Stage 4", S4), ("Stage 5", S5)):
        r(s, f"python -m qlo.experiments.{'controlled_bp' if s == 'Stage 3' else s.lower().replace(' ', '')}", mac, nr(d), nr(d), nr(d), nr(d), nr(d), na("no cache"),
          f"results/{s.lower().replace(' ', '')}/", na("see stage report"), d)
    r("Stage 6", "python -m qlo.experiments.stage6 --workers 5", mac, nr(S6), q(S6, "`python -m qlo.experiments.stage6 --workers 5`", "5"),
      q(S6, "(365 s wall, 2.2 GB peak", "365 s"), nr(S6), q(S6, "(365 s wall, 2.2 GB peak", "2.2 GB"), na("no cache"), "results/stage6/",
      na("see the Stage 6 report"), S6)
    r("Stage 7", "python -m qlo.experiments.stage7 --workers 5", mac, nr(S7), q(S7, "`python -m qlo.experiments.stage7 --workers 5`", "5"),
      q(S7, "~15–20 min on 5 cores, ≤ 2.4 GB peak", "≈15–20 min (approximate, as stated in the report; no timed log)"), nr(S7),
      q(S7, "~15–20 min on 5 cores, ≤ 2.4 GB peak", "≤ 2.4 GB (as stated)"), na("no cache"), "results/stage7/",
      (f"median-shot slopes LE {j('results/stage7/scaling_fits.json', 'fits', 'loschmidt_snr1', 'slope')[0]:.4f}, "
       f"SWAP {j('results/stage7/scaling_fits.json', 'fits', 'swap_snr1', 'slope')[0]:.4f} (SNR ≥ 1)", "results/stage7/scaling_fits.json: fits.{loschmidt,swap}_snr1.slope"), S7)
    r("B1", "python -m qlo.experiments.b1_entangling --workers 6", mac_m4, nr(B1L),
      q(B1L, "The first sweep attempt (6 workers", NR + " for the completed sweep (first attempt 6 workers, restart 4)"),
      q(B1L, "compute 5.03 CPU-h; wall 418s", "final sweep invocation 418 s (87 of 400 tasks cached from interrupted runs); audit 704 s"),
      q(B1L, "compute 5.03 CPU-h; wall 418s", "5.03 CPU-h (sweep)"), q(B1C, "≤0.65 GB resident each", "≤ 0.65 GB per worker (preflight estimate, B1_CONFIG)"),
      "per-θ caches (400 .npz files) in the work dir; required by the analyse/sign phases and by B4", "results/b1_entangling/",
      q(B1L, "analyse: identity check over 6740000 theta rows: max abs err 2.96e+02, max rel err 1.75e-11, excluded 0", "identity over 6.74 M θ rows, max rel err 1.75e-11"), B1L)
    r("B2", "python -m qlo.experiments.b2_estimators", mac, nr(B2L), na("single process"),
      q(B2L, "hadamard_u 0.6066 (34s)", "validate 5 s, rx 34 s, spot 47 s (per phase; total not logged)"), nr(B2L),
      q(B2L, "exact joint pmf at T=2048 exceeded memory", NR + " (log notes one illustration exceeded memory at T = 2048)"), na("no cache"), "results/b2_estimators/",
      q(B2L, "loschmidt 0.6059, swap_ancilla 1.2025, swap_destructive 1.2025, hadamard_u 0.6066", "slopes LE 0.6059, SWAPs 1.2025, Hadamard 0.6066"), B2L)
    r("B3", "python -m qlo.experiments.b3_hardening --workers 8", mac, nr(B3D), q(B3D, "The full computation took 3.2 h wall on 8 workers", "8"),
      q(B3D, "The full computation took 3.2 h wall on 8 workers", "3.2 h (shared machine, load 50–150); final cached analysis 1,383 s (run_meta.json)"),
      nr(B3D), nr(B3D), "per-θ caches in the work dir", "results/b3_hardening/",
      (f"Stage 7 reproduced to {g(j('results/b3_hardening/run_meta.json', 'stage7_reproduction', 'max_abs_diff_median_log10M')[0])}",
       "results/b3_hardening/run_meta.json: stage7_reproduction"), f"{B3D}; results/b3_hardening/run_meta.json")
    r("B4", "python -m qlo.experiments.b4_noise", mac, nr(B4L), na("single process"), q(B4L, "done (28s)", "30 s and 28 s (two runs)"), nr(B4L), nr(B4L),
      "the B1 per-θ caches (read-only)", "results/b4_noise/",
      q(B4L, "analyse: identity under noise over 41200000 theta rows: max rel err 1.75e-11, excluded 0", "identity over 41.2 M noisy θ rows; p = 0 reproduces B1 to 3.55e-15"), B4L)
    r("CI test suite", "python -m pytest -W error::DeprecationWarning",
      q(REPRO, "| pytest | windows-latest, Python 3.13.16 | 279 passed, 1 skipped (no `PYTHONUTF8`) |", "GitHub-hosted ubuntu-latest and windows-latest runners"),
      q(REPRO, "ubuntu-latest, Python 3.13.17", "3.12.15, 3.13.17 (ubuntu); 3.13.16 (windows)"), na("pytest default"), nr(REPRO), nr(REPRO), nr(REPRO), na("none"), na("none"),
      q(REPRO, "279 passed, 1 skipped (no `PYTHONUTF8`)", "279 passed, 1 skipped on every job"), REPRO)
    r("CI smoke runs", "python -m qlo.experiments.{b1_entangling,b2_estimators,b3_hardening,b4_noise} --fast",
      q(REPRO, "| smoke | ubuntu-latest / 3.12, ubuntu-latest / 3.13, windows-latest / 3.13 | all four `--fast` runs finished; no committed file changed |",
        "GitHub-hosted ubuntu-latest and windows-latest runners"),
      q(REPRO, "ubuntu-latest / 3.12, ubuntu-latest / 3.13, windows-latest / 3.13", "3.12 (ubuntu); 3.13 (ubuntu, windows)"), na("driver defaults"), nr(REPRO), nr(REPRO), nr(REPRO), ".qlo_cache/<experiment>_fast/",
      ".qlo_cache/<experiment>_fast/out", q(REPRO, "all four `--fast` runs finished; no committed file changed"), REPRO)
    r("Paper figures", "python -m qlo.paper.figures", nr("paper/figures/manifest.json"), nr("paper/figures/manifest.json"), na("single process"),
      nr("paper/figures/manifest.json"), nr("paper/figures/manifest.json"), nr("paper/figures/manifest.json"), na("reads committed results only"), "paper/figures/",
      q("paper/figures/FIGURE_SOURCES.md", "# Figure sources", "6 figures, 22 panels; PDFs byte-identical on rebuild"), "paper/figures/manifest.json")
    r("Bibliography check", "python tools/check_bib.py", nr("paper/BIBLIOGRAPHY_AUDIT.md"), nr("paper/BIBLIOGRAPHY_AUDIT.md"), na("single process"),
      nr("paper/BIBLIOGRAPHY_AUDIT.md"), nr("paper/BIBLIOGRAPHY_AUDIT.md"), nr("paper/BIBLIOGRAPHY_AUDIT.md"), na("offline (committed metadata snapshot)"), "paper/",
      q("paper/BIBLIOGRAPHY_AUDIT.md", "| entries in `references.bib` |", "all entries valid; B5 and A4 citations present"), "paper/BIBLIOGRAPHY_AUDIT.md")
    return R


# =================================================================================================================
def estimator_rows() -> list[dict]:
    rel, sl_rel, fx_rel = "results/b2_estimators/resource_accounting.csv", "results/b2_estimators/slope_summary.csv", "results/b2_estimators/fixed_budget_failure_modes.csv"
    ra = csv_(rel).set_index("estimator")
    sl = csv_(sl_rel)
    sl = sl[(sl.quantity == "median_log10_total_executions") & (sl.fit_range == "primary_2_20")].set_index("estimator")
    fx = csv_(fx_rel)
    fx = fx[(fx.n == 14) & (fx.total_executions == 2048)].set_index("estimator")
    labels = {"loschmidt": "Loschmidt", "swap_ancilla": "ancilla SWAP", "swap_destructive": "destructive SWAP", "hadamard_u": "Hadamard U-statistic"}
    R = []
    for est, lab in labels.items():
        a = ra.loc[est]
        ctrl = "controlled-(V†U)" if "controlled-(V" in a.needs else ("controlled-SWAPs (no controlled V†U)" if "CSWAP" in a.measures else "none")
        inv = "yes (V†)" if "V^dagger" in (a.needs + a.measures) else "no (target supplied as a second copy)"
        R.append(row(estimator=lab, measured_quantity=(a.measures, f"{rel}: measures"), qubits=(a.qubits_per_shot, f"{rel}: qubits_per_shot"),
                     copies=(int(a.state_copies_per_shot), f"{rel}: state_copies_per_shot"), controlled_unitary_requirement=(ctrl, f"{rel}: needs / measures"),
                     target_inverse_requirement=(inv, f"{rel}: needs / measures"), executions_convention=(a.executions_per_gradient, f"{rel}: executions_per_gradient"),
                     failure_behavior=(f"median P(ĝ=0) = {fx.loc[est, 'median_P_zero']:.3g}; median P(correct | ĝ≠0) = {fx.loc[est, 'median_P_correct_given_nonzero']:.3g} "
                                       "(n = 14, T = 2048 executions)", f"{fx_rel}: n = 14, total_executions = 2048"),
                     rx_exponent=(f"{sl.loc[est, 'stage7_population_slope']:.4f} decades/qubit (total executions, n = 2–20)", f"{sl_rel}: primary_2_20, median_log10_total_executions")))
    return R


# =================================================================================================================
TABLES = {"configuration_table": configuration_rows, "validation_table": validation_rows, "regime_of_validity": regime_rows,
          "reproduction_table": reproduction_rows, "estimator_resources": estimator_rows}
TITLES = {"configuration_table": "Table A1. Experiment configurations", "validation_table": "Table A2. Validation checks",
          "regime_of_validity": "Table A3. Regime of validity", "reproduction_table": "Table A4. Reproduction and compute cost",
          "estimator_resources": "Table A5. Estimator resources and access requirements"}
HEADER = """# Appendix tables

Generated by `python -m qlo.paper.methods_tables` from committed files; the CSVs next to this file are the
machine-readable versions, and [`PROVENANCE.md`](PROVENANCE.md) gives the source of every cell. Values marked
NOT RECORDED were not logged; they are never estimated.

**Where the numbers come from.** Original scientific numerics: classical simulations actually executed on Dhruv's
macOS machine (the hardware model is recorded only in the B1 log, as an Apple M4). Cross-platform CI: code, tests and `--fast` smoke runs on GitHub-hosted Linux and Windows
runners. Independent full reproduction (principal P9, Tiers 2 and 3): not yet done. Real quantum hardware: not used;
PennyLane `default.qubit` / `default.mixed` are classical simulators.
"""


def _csv(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def _md_cell(x) -> str:
    return str(x).replace("|", "\\|").replace("\n", " ")


def markdown(tables: dict[str, list[dict]]) -> str:
    L = [HEADER]
    for name, rows in tables.items():
        cols = [k for k in rows[0] if k != "provenance"]
        L += [f"## {TITLES[name]}", "", f"Source CSV: `{name}.csv`.", "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        L += ["| " + " | ".join(_md_cell(r[k]) for k in cols) + " |" for r in rows]
        L.append("")
    if any("hardware cost" in r.get("known_exclusions", "") for r in tables["regime_of_validity"]):
        L += ["Execution counts in Tables A4 and A5 are not hardware cost: qubit number, depth, ancillas and copies differ.", ""]
    return "\n".join(L)


def provenance_md(tables: dict[str, list[dict]]) -> str:
    L = ["# Provenance", "", "Source of every cell in the appendix tables (generated with them). Format: `field <- file: key, computation or \"quote\"`.", ""]
    for name, rows in tables.items():
        L += [f"## {TITLES[name]} (`{name}.csv`)", ""]
        key = list(rows[0])[0]
        for r in rows:
            L.append(f"- **{r[key]}**")
            L += [f"  - {p.strip()}" for p in r["provenance"].split(" | ") if p.strip()]
        L.append("")
    return "\n".join(L)


def build(out: Path = OUT) -> dict[str, list[dict]]:
    _cache.clear()
    tables = {name: fn() for name, fn in TABLES.items()}
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        (out / f"{name}.csv").write_text(_csv(rows), encoding="utf-8", newline="\n")
    (out / "APPENDIX_TABLES.md").write_text(markdown(tables), encoding="utf-8", newline="\n")
    (out / "PROVENANCE.md").write_text(provenance_md(tables), encoding="utf-8", newline="\n")
    return tables


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", type=Path, default=OUT)
    a = ap.parse_args(argv)
    t = build(a.out_dir)
    print(", ".join(f"{k}: {len(v)} rows" for k, v in t.items()) + f" -> {a.out_dir}")


if __name__ == "__main__":
    main()
