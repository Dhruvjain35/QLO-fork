# Stage 2 — Finite-shot gradient-noise characterization

**Scope.** Stage 2 validates the estimator model

    g_hat(θ) = g_exact(θ) + ξ_shot(θ)

for the finite-shot parameter-shift estimator implemented in
`src/qlo/gradients/finite_shot.py`, at a single fixed θ, for the GLOBAL Pauli
cost `Z_0 Z_1 Z_2` only. **It characterizes estimator noise and nothing else.**

## Environment
Python 3.12.13 · PennyLane 0.45.1 · NumPy 2.5.3 · pandas 3.0.6 · matplotlib 3.11.2 · pytest 9.1.1.
Finite-shot execution uses `default.qubit` with an explicit `seed=` Generator per
evaluation and the `qml.set_shots` transform (device-level `shots=` is deprecated
in 0.45.1 and is not used).

## Estimator
For flat index `k` and `M` shots per circuit evaluation

    ĝ_k = ½ [ Ĉ(θ + π/2 e_k) − Ĉ(θ − π/2 e_k) ]

Each `Ĉ` is the mean of `M` single-shot outcomes. Every circuit evaluation
(+ shift, − shift, every replicate, every k) spawns its own child of one
`numpy.random.SeedSequence(master_seed)` and gets a fresh `default.qubit`
device seeded from it — independent streams, fully reproducible from the master
seed, spawn keys recorded for audit. The estimator module does not import the
analytic reference (checked by AST in tests); `g_exact` is only used offline.

## Theory (global ±1 observable only)
Single-shot outcomes are ±1, so `Var(Ĉ) = (1 − C²)/M` and, with independent ± evaluations,

    Var(ĝ_k) = [2 − C₊² − C₋²] / (4M),   C± = exact expectation at θ ± π/2 e_k .

`qlo.analysis.shot_theory` implements this and **rejects** any cost other than
`"global"` (the local cost's single-shot value is a mean of n ±1's whose variance
depends on Z_iZ_j correlations; the formula does not transfer).

## Configuration
`n=3, depth=2, ring, cost=global, theta_seed=7 → p=12`, `master_seed=2025`,
`M ∈ {64,128,256,512,1024,2048}`, 200 replicates per (k,M).
Default k = first/middle/last = (0, 6, 11) → `results/stage2/`.
Supplemental k = (2, 3, 8), the three largest-|g| components → `results/stage2_nonzero_k/`
(see *Anomalies* for why this run was added).
Covariance pilot: `M ∈ {128,512,2048}`, 100 full-gradient replicates.

## Results — single point (per k, M)

Default run, `results/stage2/shot_noise_summary.csv`:

| k | M | g_exact | mean ξ | Var_emp | Var_theory | emp/theory | z(mean ξ) |
|---|---|---|---|---|---|---|---|
| 0 | 64 | 0.0331 | 0.00140 | 8.685e-3 | 7.730e-3 | 1.124 | 0.21 |
| 0 | 128 | 0.0331 | 0.00608 | 3.982e-3 | 3.865e-3 | 1.030 | 1.36 |
| 0 | 256 | 0.0331 | 0.00298 | 2.075e-3 | 1.932e-3 | 1.074 | 0.92 |
| 0 | 512 | 0.0331 | −0.00179 | 1.088e-3 | 9.662e-4 | 1.126 | −0.77 |
| 0 | 1024 | 0.0331 | −0.00034 | 5.098e-4 | 4.831e-4 | 1.055 | −0.21 |
| 0 | 2048 | 0.0331 | −0.00043 | 2.548e-4 | 2.416e-4 | 1.055 | −0.38 |
| 6 | 64 | 0 (structural) | −0.00422 | 7.309e-3 | 7.679e-3 | 0.952 | −0.70 |
| 6 | 128 | 0 | 0.00535 | 4.119e-3 | 3.840e-3 | 1.073 | 1.18 |
| 6 | 256 | 0 | −0.00346 | 1.625e-3 | 1.920e-3 | 0.847 | −1.21 |
| 6 | 512 | 0 | 0.00012 | 1.010e-3 | 9.599e-4 | 1.052 | 0.05 |
| 6 | 1024 | 0 | 0.00294 | 4.506e-4 | 4.799e-4 | 0.939 | 1.96 |
| 6 | 2048 | 0 | −0.00126 | 2.505e-4 | 2.400e-4 | 1.044 | −1.13 |
| 11 | 64 | 0 (structural) | −0.01141 | 8.020e-3 | 7.679e-3 | 1.044 | −1.80 |
| 11 | 128 | 0 | −0.00137 | 3.593e-3 | 3.840e-3 | 0.936 | −0.32 |
| 11 | 256 | 0 | −0.00271 | 2.070e-3 | 1.920e-3 | 1.078 | −0.84 |
| 11 | 512 | 0 | −0.00104 | 9.095e-4 | 9.599e-4 | 0.947 | −0.49 |
| 11 | 1024 | 0 | −0.00208 | 4.847e-4 | 4.799e-4 | 1.010 | −1.34 |
| 11 | 2048 | 0 | −0.00004 | 2.734e-4 | 2.400e-4 | 1.139 | −0.03 |

Supplemental run, `results/stage2_nonzero_k/shot_noise_summary.csv`:

| k | M | g_exact | mean ξ | Var_emp | Var_theory | emp/theory | z(mean ξ) |
|---|---|---|---|---|---|---|---|
| 2 | 64 | −0.1874 | 0.00029 | 6.062e-3 | 7.538e-3 | 0.804 | 0.05 |
| 2 | 128 | −0.1874 | −0.00271 | 3.983e-3 | 3.769e-3 | 1.057 | −0.61 |
| 2 | 256 | −0.1874 | −0.00295 | 1.957e-3 | 1.885e-3 | 1.039 | −0.94 |
| 2 | 512 | −0.1874 | 0.00093 | 1.041e-3 | 9.423e-4 | 1.105 | 0.41 |
| 2 | 1024 | −0.1874 | −0.00285 | 5.050e-4 | 4.711e-4 | 1.072 | −1.79 |
| 2 | 2048 | −0.1874 | 0.00128 | 2.463e-4 | 2.356e-4 | 1.045 | 1.16 |
| 3 | 64 | 0.6213 | 0.00173 | 4.439e-3 | 4.788e-3 | 0.927 | 0.37 |
| 3 | 128 | 0.6213 | 0.00439 | 2.167e-3 | 2.394e-3 | 0.905 | 1.33 |
| 3 | 256 | 0.6213 | 0.00034 | 1.350e-3 | 1.197e-3 | 1.128 | 0.13 |
| 3 | 512 | 0.6213 | −0.00138 | 6.380e-4 | 5.985e-4 | 1.066 | −0.77 |
| 3 | 1024 | 0.6213 | 0.00152 | 3.024e-4 | 2.993e-4 | 1.010 | 1.24 |
| 3 | 2048 | 0.6213 | 0.00003 | 1.612e-4 | 1.496e-4 | 1.078 | 0.04 |
| 8 | 64 | −0.0789 | −0.00696 | 8.190e-3 | 7.764e-3 | 1.055 | −1.09 |
| 8 | 128 | −0.0789 | −0.00286 | 3.617e-3 | 3.882e-3 | 0.932 | −0.67 |
| 8 | 256 | −0.0789 | 0.00282 | 1.668e-3 | 1.941e-3 | 0.859 | 0.98 |
| 8 | 512 | −0.0789 | 0.00092 | 9.327e-4 | 9.705e-4 | 0.961 | 0.42 |
| 8 | 1024 | −0.0789 | 0.00112 | 4.976e-4 | 4.852e-4 | 1.026 | 0.71 |
| 8 | 2048 | −0.0789 | −0.00081 | 2.261e-4 | 2.426e-4 | 0.932 | −0.77 |

Pooled over all 36 cells: **emp/theory ratio mean 1.015 (SE 0.014), SD 0.084**
(the expected sampling SD of a variance ratio at 200 replicates is ≈ √(2/199) ≈ 0.10);
**0/36 cells have |z| > 1.96** (≈1.8 expected under H₀); Σz² = 32.0 on 36 dof
(p ≈ 0.66); all 36 95% CIs for E[ξ] contain 0.

## Results — 1/M scaling (`shot_noise_scaling.csv`)

| run | k | slope b | R² | M·Var_emp range | M·Var_theory |
|---|---|---|---|---|---|
| default | 0 | −1.008 | 0.9993 | 0.510 – 0.557 | 0.495 |
| default | 6 | −0.989 | 0.9951 | 0.416 – 0.527 | 0.491 |
| default | 11 | −0.978 | 0.9969 | 0.460 – 0.560 | 0.491 |
| suppl. | 2 | −0.942 | 0.9948 | 0.388 – 0.533 | 0.482 |
| suppl. | 3 | −0.958 | 0.9970 | 0.277 – 0.346 | 0.306 |
| suppl. | 8 | −1.009 | 0.9969 | 0.427 – 0.524 | 0.497 |

All six slopes lie inside the (−1.30, −0.70) sanity band and within ~0.06 of −1.
The k=3 row is the informative one: its theoretical `M·Var` is 0.306 rather than
≈0.49 because |C±| is large there, and the empirical `M·Var` (0.277–0.346) follows
it — i.e. the formula's dependence on C± is reproduced, not just the 1/M shape.

## Results — covariance pilot (`covariance_summary.csv`, matrices in `covariance/`)

| M | trace Cov | trace Cov (theory, Σ_k Var_k) | trace(M·Cov) | ‖Cov‖_F | max \|offdiag\| | mean \|offdiag\| | max\|offdiag\| / mean diag |
|---|---|---|---|---|---|---|---|
| 128 | 4.260e-2 | 4.471e-2 | 5.45 | 1.34e-2 | 9.90e-4 | 3.48e-4 | 0.28 |
| 512 | 1.120e-2 | 1.118e-2 | 5.73 | 3.44e-3 | 2.14e-4 | 7.42e-5 | 0.23 |
| 2048 | 2.720e-3 | 2.794e-3 | 5.57 | 8.33e-4 | 4.81e-5 | 1.79e-5 | 0.21 |

trace(M·Cov) is stable (5.45–5.73 vs theory 5.72) → the p-dimensional noise
scales as 1/M in aggregate.

**Off-diagonals are near zero by construction.** In this implementation every
gradient component draws its own independent ± circuit samples, so
`Cov(ξ_j, ξ_k)` for j≠k has expectation exactly 0 and the observed values
(≤ 0.28 × mean diagonal, at 100 replicates) are sampling noise. This must NOT be
read as a property of quantum shot-noise gradients in general: an estimator that
reuses one sample set across components (e.g. simultaneous / shared-sample
strategies) would have non-trivial off-diagonal structure. The pilot only checks
that the implementation and the 1/M scaling of the full covariance behave.

## Task 1 — barren-plateau statistic
`qlo.analysis.bp_variance` implements `Var_θ[∂C/∂θ_k]` per k across independent
initializations (ddof=1), with a separate second-step summary across k. The
Stage 1 within-gradient statistic is renamed `within_gradient_entry_var` and
documented as not a BP diagnostic. No BP scaling experiment was run.

## Task 10 — sanity checks (all encoded as tests in `tests/test_finite_shot.py`)
- **A** no randomness reuse: 72 evaluations in a 3-replicate full gradient → 72 distinct spawn keys; repeated same-circuit estimates differ.
- **B/D** finite-shot really uses M shots: every M-shot estimate lies on the lattice `{−1, −1+2/M, …, 1}` for M ∈ {1,3,5,8}, while the exact value is off-lattice (a `shots=None` fallback would fail this); `set_shots(37)` returns exactly 37 samples.
- **C** analytic reference shares no randomness: exact gradient bit-identical before/after finite-shot runs and global-NumPy reseeding; `make_cost` contains no shots argument other than `shots=None`.
- **E** indexing: `flat_to_multi`/`shifted_params` agree with `np.unravel_index`; with M=4096 each `ĝ_k` lands within 5σ of `g_exact[k]` for k ∈ {0,5,11}.
- **F** ±1 outcomes: `qml.sample(Z⊗Z⊗Z)` returns only {−1,+1}.
- Also: estimator module has no import of the analytic module (AST check) and still runs with every analytic function monkey-patched to raise.

## ESTABLISHED by this implementation (for this ansatz, θ, and global cost)
- The finite-shot parameter-shift estimator is reproducible from one master seed, with independent randomness per evaluation.
- **E[ξ_shot] is consistent with 0**: 36/36 CIs contain 0; Σz² = 32.0 / 36 dof.
- **Var[ξ_shot] ∝ 1/M** empirically: fitted slopes −0.94 … −1.01, R² ≥ 0.995; `M·Var` flat within sampling error.
- **The analytic ±1-observable variance `[2 − C₊² − C₋²]/(4M)` predicts the empirical variance**: pooled ratio 1.015 ± 0.014, including its C±-dependence (k=3).
- Aggregate covariance scales as 1/M (trace(M·Cov) ≈ 5.6 vs 5.72 theory).

## NOT ESTABLISHED (and not claimed)
- Any fluctuation–dissipation relation for shot noise.
- That shot noise provides *useful* exploration.
- Barren-plateau existence for this ansatz, or escape from one.
- QLO superiority, polynomial escape time, or quantum advantage.
- Anything about the local cost's shot-noise variance (formula not derived/validated for it).
- Anything about θ-dependence of Σ(θ): a single θ was studied.
- Anything about off-diagonal covariance structure of shot-noise gradients in general (see pilot caveat).

## Anomalies / observations
1. **Structurally zero gradients.** For this ansatz with the global cost, the
   last-layer RZ parameters and (for n=3) the last-layer RY on qubits 0 and 2
   have identically zero gradient at every θ: pushing `Z⊗Z⊗Z` back through the
   ring CNOTs gives a single `Z_1`, and RZ commutes with Z. For n=3, depth=2 this
   is 6 of 12 parameters (k = 1, 6, 7, 9, 10, 11; verified numerically at 8 random
   θ, and similar patterns at n=4,5,6). The brief's "middle/last" picks (k=6, 11)
   are both such components. That does not invalidate the ξ characterization at
   those k (the noise is nonzero and g=0 is a clean unbiasedness test), but it is
   why the supplemental run on k=(2,3,8) was added. **Any future barren-plateau
   study with this ansatz+cost must account for this — the "global" cost is
   effectively a single-qubit Z at the last layer, and averaging Var_θ over all k
   would be diluted by identically-zero components.** This is a structural
   observation, not a claim about barren plateaus.
2. One cell (k=6, M=1024) has z = 1.96 — exactly the number expected once in ~20 cells.
3. The observed SD of the variance ratio (0.084) is slightly below the normal-theory
   value 0.10; ξ is a bounded difference of binomial means (kurtosis < 3), so this
   is expected, not a sign of correlated replicates.
4. The covariance pilot output is identical in the two runs (same master seed; k selection does not enter it).
