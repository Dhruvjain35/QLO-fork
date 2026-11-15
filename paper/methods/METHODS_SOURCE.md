# Methods source (for the manuscript)

This document collects the methods already in the repository, so the principal track can adapt it into the
manuscript. It is not manuscript text.
- **Facts only.** It restates existing definitions and procedures, with a source for each section. It adds no
  claims and decides nothing about what the paper includes.
- **Numbers.** Configuration values, validation errors and run costs are in the generated tables in
  [`../appendix/APPENDIX_TABLES.md`](../appendix/APPENDIX_TABLES.md) (Tables A1–A5). They are not repeated here, so
  there is one source for each number.

**Where the numbers come from.**
- **Original scientific numerics:** classical simulations actually executed on Dhruv's macOS machine.
- **Cross-platform CI:** code, tests and smoke runs on GitHub-hosted Linux and Windows runners.
- **Second-machine reproduction** (principal P9): done by a co-author on Windows 11, 9 November 2026; every frozen
  experiment matched (`docs/phase8/P9_WINDOWS_REPRODUCTION.md`). Not reproduced outside the team.
- **Real quantum hardware:** not used. PennyLane `default.qubit` and `default.mixed` are classical simulators.

Source: [`docs/phase8/REPRODUCTION_STATUS.md`](../../docs/phase8/REPRODUCTION_STATUS.md).

## 1. Computational environment

- **Machine.** All committed results were produced on Dhruv's macOS machine. Stage 1 records macOS (Darwin 25.4.0,
  arm64) in `docs/stages/STAGE1_STATUS.md`. The hardware model is named only in the B1 numerics log, which refers to
  the machine's M4 performance cores (B1 log, `results/b1_entangling/numerics_log.md`). No other run records the model.
- **Software.** Python, NumPy, SciPy, pandas, Matplotlib and PennyLane. Section 16 gives versions.
- **Parallelism.** The B1 and B3 sweeps and the Stage 6/7 required-shot solves ran in parallel worker processes.
  Results do not depend on the number of workers, because every task is seeded by its own identifiers (Section 2).
- **Machine load.** The B1 and B3 runs were made while the machine was shared with other jobs. The B1 log records the
  memory and load conditions and the restarts (`results/b1_entangling/numerics_log.md`). These affect wall time only.

## 2. Random seeding and reproducibility

- **Seed derivation.** Every random quantity is derived from an explicit seed through NumPy `SeedSequence`, keyed by
  the experiment, n, the master seed and (where relevant) the stream, start or replicate.
  - Stage 4 uses `SeedSequence([4, 200, method_id, n, start_seed, replicate, config_id])` (`docs/stages/STAGE4.md` §3).
  - Stages 6 and 7 seed each per-n solve by (n, seed) (`docs/stages/STAGE6.md`, `STAGE7.md`, "Re-run").
- **Disjoint seed sets.** Seed sets are kept disjoint across tasks and checked in code
  (`qlo.hardening.seed_replicates.check_seeds`):
  - Stage 7 reference seed 0;
  - B3 seeds 10000–10019;
  - B1 and B4 seeds 11000–11009;
  - B2 replicate seeds 12000–12009.

  Table A1 lists the seeds of every experiment.
- **Frozen configurations.** B1, B2 and B4 configurations were frozen before their full runs. Each is stored as JSON
  in `docs/b{1,2,4}/B*_CONFIG.md`, and each driver refuses to run if its configuration differs.

## 3. RX-product benchmark

- **Definition.** |ψ(θ)⟩ = ⊗ⱼ RX(θⱼ)|0ⁿ⟩, with θⱼ iid U[−π, π] and target |0ⁿ⟩.
- **Fidelity and gradient.** F = ∏ⱼ cos²(θⱼ/2) and C = 1 − F. For component k: A = ∏_{j≠k} cos²(θⱼ/2), s = sin θ_k,
  F± = F(θ ± π/2 e_k) = A(1 ∓ s)/2, and g = ∂C/∂θ_k = A s/2.
- **Stage 3.** The benchmark is the global cost of Cerezo et al. (2021), with closed-form gradient variance
  (1/8)(3/8)^(n−1). The matched local cost is the control.
- **Closed forms.** Stages 3–7 use these exact closed forms. Stage 3 also checks them against PennyLane circuits
  (Table A2).

Sources: `docs/stages/STAGE3.md` ("Benchmark"), `docs/stages/STAGE7.md` §4.

## 4. Hardware-efficient ansatz (`hea_ring`, B1 family 1)

- **Layer.** Each layer applies RY(θ[l,q,0]) and then RZ(θ[l,q,1]) on every qubit, followed by CNOT(0,1),
  CNOT(1,2), …, CNOT(n−2,n−1) and CNOT(n−1,0), in that order.
- **Implementation.** The repository class is `src/qlo/circuits/hardware_efficient.py`. The B1 simulator reproduces
  its PennyLane state at machine precision.
- **Target and initialisation.** |0ⁿ⟩, θ iid U[−π, π].

Source: `docs/b1/B1_ENTANGLING_SWEEPS.md` §6.

## 5. RX–RY CZ brickwork ansatz (`rxry_czbrick`, B1 family 2)

- **Layer.** Each layer applies RX(θ[l,q,0]) and then RY(θ[l,q,1]) on every qubit, followed by open-boundary CZ
  brickwork: CZ(0,1), CZ(2,3), … on even layers and CZ(1,2), CZ(3,4), … on odd layers.
- **Validation.** It is checked against an independent PennyLane template (`qlo.b1.audit.pl_rxry_czbrick`).

Source: `docs/b1/B1_ENTANGLING_SWEEPS.md` §7.

## 6. Fidelity objective

- **General setting.** The trial state is ρ(θ), possibly mixed, and the target is pure, |φ⟩ = V|0ⁿ⟩.
  F(θ) = ⟨φ|ρ(θ)|φ⟩ and C = 1 − F.
- **Derived quantities.** S = F₊ + F₋, Δ = F₋ − F₊, r = Δ/S and Q = F₊² + F₋².

Source: `docs/theory/A2_PROPOSITIONS.md` §0.

## 7. Parameter-shift gradients

- **Shift rule.** θ_k enters through e^{−iθ_k P/2} with P a Pauli string, so the two-term shift rule is exact:
  g = ∂C/∂θ_k = (F₋ − F₊)/2.
- **Batches.** One independent batch of M shots is taken at each shift. Stage 4 additionally takes an independent
  batch for every component k and iteration.
- **Positions.** For the entangling circuits, B1 differentiates θ[l,0,0] on qubit 0 at layer l = 0, floor(d/2) or
  d − 1 (early, middle, late). A structural-zero audit was run before the sweep.

Sources: `docs/theory/A2_PROPOSITIONS.md` §0; `docs/stages/STAGE4.md` §3; `docs/b1/B1_ENTANGLING_SWEEPS.md` §4, §8.

## 8. Loschmidt (projector) estimator

- **Readout.** Each shot is Bernoulli(F±): apply V†, then test for 0ⁿ.
- **Estimator.** K± ~ Bin(M, F±), F̂ = K/M and ĝ_LE = (K₋ − K₊)/(2M), which is unbiased.
- **Variance.** Var ĝ_LE = [F₊(1−F₊) + F₋(1−F₋)]/(4M) = (S − Q)/(4M).

Sources: `docs/stages/STAGE7.md` §5; `docs/theory/A2_PROPOSITIONS.md` §0–1.

## 9. Ancilla SWAP estimator

- **Readout.** The ancilla Z of the standard SWAP test has E Z = F, i.e. P(+1) = (1 + F)/2. The target copy is pure.
- **Estimator.** With K± counting +1 outcomes, F̂ = 2K/M − 1 and ĝ_SW = (K₋ − K₊)/M, which is unbiased.
- **Variance.** Var F̂ = (1 − F²)/M, so Var ĝ_SW = (2 − Q)/(4M).
- **Sign check.** The sign convention was checked by exact enumeration.

Sources: `docs/stages/STAGE7.md` §6; `docs/theory/A2_PROPOSITIONS.md` §0–1.

## 10. Destructive SWAP estimator

- **Readout.** Two copies, no ancilla. Each copy pair is measured in the Bell basis, and Z = ∏ᵢ(−1)^(aᵢbᵢ).
- **Equivalence.** The outcome statistics are identical to the ancilla SWAP test. B2 validates this at circuit level
  and on the Stage 7 population.
- **Circuit cost.** n CNOTs and n Hadamards, at constant depth 2 after state preparation (Table A5).

Sources: `docs/b2/B2_ADDITIONAL_ESTIMATORS.md` §5–6; `results/b2_estimators/resource_accounting.csv`.

## 11. Hadamard-test U-statistic estimator

- **Readout.** An ancilla-controlled V†U circuit measures the real and imaginary quadratures of the overlap.
- **Estimator.** The fidelity estimator is the unbiased U-statistic built from these quadratures. It is not confined
  to [0, 1] and is never clipped.
- **Variance.** [2(1−x⁴) + 4(M−2)x²(1−x²)]/[M(M−1)], plus the same term in y.
- **Cost convention.** 4M executions per gradient component (M per quadrature per shift).
- **Validation.** Unbiasedness and the variance were checked by exact enumeration up to M = 256.

Sources: `docs/b2/B2_ADDITIONAL_ESTIMATORS.md`, `docs/b2/B2_HADAMARD_DERIVATION.md`;
`results/b2_estimators/resource_accounting.csv`.

## 12. Required-shot and SNR calculation

- **SNR target.** Required shots are the smallest M with SNR = |g|/√Var ĝ ≥ ρ (ρ = 1 primary, ρ = 2 secondary).
  Directional and nonzero-probability targets are defined analogously in Stages 6 and 7.
- **Stages 6 and 7.** These solve integer budgets by exact binomial or bisection methods, using normal or closed forms
  only where validated.
- **B1 and B4.** These use the continuous exact M at the SNR target. B1 applies the Stage 7 ceil convention only for
  its comparison with B3.
- **B2.** B2 uses the frozen Stage 7 functions with the Stage 7 integer-budget convention for Loschmidt and ancilla
  SWAP, and exact integer inversion for the Hadamard estimator (`src/qlo/b2/required_shots.py`).
- **Statistic.** The median of log₁₀ M over θ is fitted against n by least squares. Slopes are reported in decades
  per qubit.

Sources: `docs/stages/STAGE6.md`, `docs/stages/STAGE7.md` §12; `docs/theory/A2_PROPOSITIONS.md` §0;
`docs/b1/B1_ENTANGLING_SWEEPS.md` §4; `src/qlo/b2/required_shots.py`.

## 13. Statistical hardening and confidence intervals

Two uncertainty sources are kept separate in B3 (`docs/b3/B3_STATISTICAL_HARDENING.md`):
- **SEED (primary).** 20 independent master seeds, each a fresh θ population. The predeclared primary criterion is
  the SEED 95% percentile interval.
- **THETA (secondary).** A paired θ bootstrap inside the regenerated Stage 7 population.

Other tasks:
- **B1 and B4.** The bootstrap 95% CI of the 10-seed mean, using B3's `summarize` with 10,000 replicates and seed
  2026.
- **B2.** 95% percentile intervals over 10 replicate seeds.
- **Probabilities in Stages 4–7.** Wilson 95% intervals.

Table A1 lists the CI method of every experiment.

## 14. B1 entangling sweeps

- **Design.** Two entangling families (Sections 4–5) and the RX-product regression arm, at depths 2, 4 and n.
  Early, middle and late parameter positions. 10 seeds of 4,000 θ per (family, regime, n, seed). Grids in Table A1.
- **Quantities.** The slopes b_S, b_r, b_LE and b_SWAP of the median log₁₀ quantities against n.
- **Tests.** The exact shot-ratio identity per θ, and the slope rule b_SWAP − b_LE = b_S per cell, with predeclared
  acceptance rules.
- **Freeze.** The configuration was frozen at commit 735a8df before any full-run output existed. The B1 log
  timestamps the post-freeze implementation changes, a faster simulator kernel validated against the audited one.

Sources: `docs/b1/B1_CONFIG.md`; `docs/b1/B1_ENTANGLING_SWEEPS.md` §4–8, §14–17.

## 15. B4 noise models

- **Global depolarizing.** Applied after each of L layers: ρ ↦ (1 − p)ρ + p I/2ⁿ. It commutes with unitaries, so
  F' = qF + (1 − q)/2ⁿ and Δ' = qΔ with q = (1 − p)^L.
  - This is applied exactly to the B1 per-θ caches and the Stage 7 θ stream.
  - Δ' is computed as qΔ to avoid cancellation.
- **Local depolarizing.** Single-qubit depolarizing with probability p after every rotation, on the product circuit
  only. The state stays a product, giving F±' in closed form (Proposition 6).
- **Readout model.** Noise acts on the trial state only. The SWAP target copy is ideal.
- **Validation.** Both models are checked against PennyLane `default.mixed` density-matrix simulation. This is a
  classical simulator, not hardware.

Sources: `docs/b4/B4_NOISE_OVERLAY.md` §2–3; `docs/theory/A2_PROPOSITIONS.md` §6–7.

## 16. Software and versions

- **Pinned.** PennyLane is pinned to 0.45.1 in `pyproject.toml`. NumPy, SciPy, pandas and Matplotlib are not pinned.
- **Recorded.** The versions recorded at Stage 2 are Python 3.12.13, PennyLane 0.45.1, NumPy 2.5.3, pandas 3.0.6,
  Matplotlib 3.11.2 and pytest 9.1.1 (`docs/stages/STAGE2.md`).
- **Not recorded.** Per-run interpreter and library versions for the later stages and the B tasks were not logged
  (Table A4, "NOT RECORDED").
- **CI.** CI installs current releases of the unpinned packages on Python 3.12 and 3.13.

## 17. Reproducibility

- **Drivers.** Every experiment has one driver, `python -m qlo.experiments.<name>`, writing to `results/<name>/`.
  Table A4 lists the command, the recorded wall time, CPU time and memory, the cache requirements and a headline
  check.
- **Caches.** Per-θ caches go to `--work-dir`, else `$QLO_WORK_DIR`, else `.qlo_cache/` (Phase 8 I2).
- **Smoke modes.** The `--fast` modes run reduced, unfrozen configurations into `.qlo_cache/` and never touch
  `results/`.
- **Paper assets.** The figures and these tables are regenerated from committed results by
  `python -m qlo.paper.figures` and `python -m qlo.paper.methods_tables`.
- **Status.** Every frozen experiment was reproduced on a second machine (P9, Windows 11, by a co-author). No
  reproduction outside the team and no hardware validation yet (`docs/phase8/REPRODUCTION_STATUS.md`).
