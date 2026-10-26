# Stage 3 — Controlled barren-plateau benchmark (Cerezo et al. 2021)

**Purpose.** Show that the pipeline can distinguish genuine exponential gradient
concentration from polynomial gradient shrinkage on a benchmark with *exactly
known* variance scaling, without relying on structurally-zero gradients. No QLO,
no shot noise, no claims beyond the benchmark.

## Benchmark
- State `|0>^n`, circuit `V(θ) = ⊗_j RX(θ_j)`, `p = n`, `θ_j ~ iid U[-π, π]`, target `|0>^n`.
- Global cost `C_G = 1 − |<0^n|ψ>|² = 1 − ∏_j cos²(θ_j/2)`;
  `∂C_G/∂θ_k = ½ sin θ_k ∏_{j≠k} cos²(θ_j/2)`; `E=0`; **`Var_θ = (1/8)(3/8)^(n−1)`** (exponential).
- Local cost `C_L = 1 − (1/n)Σ_j P(q_j=0) = 1 − (1/n)Σ_j cos²(θ_j/2)`;
  `∂C_L/∂θ_k = sin θ_k/(2n)`; `E=0`; **`Var_θ = 1/(8n²)`** (polynomial).
- Implementation: `src/qlo/benchmarks/cerezo2021.py` — closed forms in pure NumPy
  (external reference), and the PennyLane circuit on analytic `default.qubit`
  (`Projector` observables, backprop and parameter-shift, parameter broadcasting).
- Experiment: `src/qlo/experiments/controlled_bp.py` → `results/stage3/`
  (primary, N=10 000 per n, `master_seed=3`, k=0) and `results/stage3_n1e6/`
  (supplemental, N=10⁶, closed-form only).

The Monte Carlo sweep uses the closed-form gradients. **This is exact arithmetic
on a validated formula, not hardware execution and not statevector simulation.**

## Closed-form validation (tests, n ∈ {2,3,4,6} × 3 seeds × 2 costs)
| comparison | max abs error |
|---|---|
| PennyLane cost vs closed form | 0.0 (bit-identical) |
| PennyLane backprop gradient vs closed form | 1.1e-19 (global), 5.6e-17 (local) |
| PennyLane parameter-shift gradient vs closed form | 1.2e-18 (global), 7.3e-17 (local) |
| broadcast parameter-shift (batched) vs closed form | 2.5e-16 |
| closed-form gradient vs central finite difference | < 1e-8 |
Theoretical variances and 4th moments are independently reproduced by `scipy` quadrature in tests.

## Primary result — N = 10 000 per n, k = 0 (`results/stage3/controlled_bp_summary.csv`)

### Global cost (exponential positive control)
| n | Var_emp | Var_theory | ratio | predicted rel. SE of Var_emp | z (exact) | factorized ratio† |
|---|---|---|---|---|---|---|
| 2 | 4.619e-2 | 4.688e-2 | 0.985 | 0.014 | −1.05 | 0.990 |
| 4 | 6.625e-3 | 6.592e-3 | 1.005 | 0.032 | 0.16 | 1.008 |
| 6 | 9.664e-4 | 9.270e-4 | 1.043 | 0.064 | 0.67 | 1.008 |
| 8 | 1.514e-4 | 1.304e-4 | 1.162 | 0.125 | 1.29 | 1.016 |
| 10 | 1.608e-5 | 1.833e-5 | 0.877 | 0.244 | −0.50 | 1.010 |
| 12 | 1.578e-6 | 2.578e-6 | 0.612 | 0.475 | −0.82 | 1.009 |
| 14 | 2.311e-7 | 3.625e-7 | 0.638 | 0.923 | −0.39 | 0.975 |
| 16 | 1.209e-7 | 5.098e-8 | 2.372 | 1.795 | 0.76 | 1.004 |
| 18 | 2.856e-10 | 7.169e-9 | 0.040 | 3.49 | −0.28 | 0.950 |
| 20 | 1.670e-10 | 1.008e-9 | 0.166 | 6.79 | −0.12 | 1.078 |
| 22 | 5.204e-12 | 1.418e-10 | 0.037 | 13.2 | −0.07 | 1.005 |
| 24 | 7.732e-13 | 1.994e-11 | 0.039 | 25.7 | −0.04 | 1.099 |

† benchmark-specific diagnostic estimator, see "Anomaly 1".

### Local cost (polynomial trainable control)
| n | Var_emp | Var_theory | ratio | predicted rel. SE | z (exact) |
|---|---|---|---|---|---|
| 2 | 3.118e-2 | 3.125e-2 | 0.998 | 0.0071 | −0.30 |
| 4 | 7.849e-3 | 7.812e-3 | 1.005 | 0.0071 | 0.67 |
| 6 | 3.499e-3 | 3.472e-3 | 1.008 | 0.0071 | 1.09 |
| 8 | 1.938e-3 | 1.953e-3 | 0.992 | 0.0071 | −1.11 |
| 10 | 1.245e-3 | 1.250e-3 | 0.996 | 0.0071 | −0.57 |
| 12 | 8.660e-4 | 8.681e-4 | 0.998 | 0.0071 | −0.34 |
| 14 | 6.358e-4 | 6.378e-4 | 0.997 | 0.0071 | −0.43 |
| 16 | 4.854e-4 | 4.883e-4 | 0.994 | 0.0071 | −0.82 |
| 18 | 3.874e-4 | 3.858e-4 | 1.004 | 0.0071 | 0.60 |
| 20 | 3.121e-4 | 3.125e-4 | 0.999 | 0.0071 | −0.19 |
| 22 | 2.605e-4 | 2.583e-4 | 1.009 | 0.0071 | 1.21 |
| 24 | 2.162e-4 | 2.170e-4 | 0.996 | 0.0071 | −0.56 |

### Fits (`global_fit.json`, `local_fit.json`, `model_comparison.json`)
| fit | slope | theory | abs err | R² |
|---|---|---|---|---|
| global semi-log, all 12 n (as specified) | −1.142 | log(3/8) = −0.9808 | 0.161 | 0.986 |
| global semi-log, resolved range n ≤ 12 (a-priori criterion: predicted rel. SE < 0.5) | −1.019 | −0.9808 | 0.038 | 0.998 |
| global semi-log, factorized diagnostic estimator, all n | −0.979 | −0.9808 | 0.002 | 0.99997 |
| local log-log, all 12 n | −2.0003 | −2 | 0.0003 | 0.99999 |

Model comparison (12 points, n = 2…24; AIC = N ln(RSS/N) + 2K):
- global: exponential R² 0.986 / RSS 10.3 / AIC 2.2 vs power-law R² 0.847 / RSS 115 / AIC 31.2 → **exponential** (ΔAIC 29)
- local: power-law R² 0.99999 / RSS 3e-4 / AIC −122 vs exponential R² 0.895 / RSS 2.6 / AIC −14 → **power-law** (ΔAIC 108)

Means: 1 of 24 (n, cost) cells has |z_mean| > 1.96 (n=14 local, z = 2.12); all consistent with E = 0.

Symmetry (other k at n ∈ {4,12,24}, `symmetry_check.csv`): 24 cells, max |z_exact| = 3.0
(n=4 global k=2, ratio 0.905), max |z_mean| = 2.65. Re-checked over 20 seeds × 8 cells at n=4:
z-scores have mean −0.13, sd 1.07 — no bias; the 3.0 is chance.

## Supplemental — N = 10⁶ per n (`results/stage3_n1e6/`)
| fit | slope | abs err | R² |
|---|---|---|---|
| global semi-log, all 12 n | −0.9882 | 0.0073 | 0.9992 |
| global semi-log, resolved range (now n ≤ 18) | −0.9867 | 0.0059 | 0.9995 |
| local log-log, all 12 n | −1.9999 | 0.0001 | 1.0000 |

Global ratios at N=10⁶: 1.000, 1.000, 0.995, 1.003, 0.973, 0.919, 0.844, 1.249, 0.787, 0.552, 1.126, 0.948
(n = 2…24); all |z_exact| ≤ 1.7. ΔAIC(power − exp) = 59 for global, ΔAIC(exp − power) = 162 for local.

## PennyLane cross-check (`pennylane_crosscheck.csv`, n ∈ {2,4,6,8,10}, fresh θ)
Two simulator-based estimates of `Var_θ[∂C/∂θ_0]`: (a) `qml.grad` backprop on 1 000 θ,
(b) broadcast two-term parameter shift on 10 000 θ (pure circuit arithmetic).

| n | cost | (a) ratio [pred. rel SE] | (b) ratio [pred. rel SE] | closed-form MC ratio | max\|PL − closed form\| same θ |
|---|---|---|---|---|---|
| 2 | global | 1.008 [0.04] | 1.031 [0.014] | 0.985 | 2.5e-16 |
| 4 | global | 1.040 [0.10] | 1.080 [0.032] | 1.005 | 2.4e-16 |
| 6 | global | 0.743 [0.20] | 1.123 [0.064] | 1.043 | 1.5e-16 |
| 8 | global | 0.787 [0.40] | 0.818 [0.125] | 1.162 | 1.4e-16 |
| 10 | global | 0.714 [0.77] | 0.874 [0.244] | 0.877 | 8.3e-17 |
| 2–10 | local | 0.971–1.015 [0.022] | 0.996–1.011 [0.007] | 0.992–1.008 | ≤ 3.1e-16 |

Every PennyLane gradient equals the closed form on identical θ to ≤ 3e-16, and the
simulator-based variances agree with theory within their predicted sampling error.
A bug in the closed-form pipeline would have shown up here; none did.

## Structural-zero audit
Closed form: `∂C_G/∂θ_k = ½ sin θ_k ∏_{j≠k} cos²(θ_j/2)` and `∂C_L/∂θ_k = sin θ_k/(2n)`
are non-trivial functions of θ for every k (each equals ½, resp. 1/(2n), at
θ = (π/2)e_k — an exact witness checked in tests for both closed form and PennyLane,
n ∈ {2,3,4,6,8}). Numerically, over 200 random θ every component has max|g_k| > 1e-3,
for both costs. Over the whole sweep (12 n × 10 000 θ) the count of exactly-zero
`∂C_G/∂θ_0` values is **0**. Individual gradients can be tiny at particular θ
(median |∂C_G/∂θ_0| at n=24 is 9e-15) — that is concentration, not structure.

**Distinction.** *Structural zero*: `∂C/∂θ_k ≡ 0 for all θ` because of gate/observable
commutation (the Stage 1 HEA case, below). *Gradient concentration*: `∂C/∂θ_k` is a
non-trivial function whose distribution over random θ shrinks with n (this benchmark's
global cost, exponentially). Only the second is a barren plateau.

## Numerical stability (`numerical_stability.csv`)
No NaN, no Inf, no exact zeros at any n. Smallest theoretical variance encountered:
1.99e-11 (n=24). Smallest |∂C_G/∂θ_0| observed: 2.9e-34 (N=10⁴), 4.6e-41 (N=10⁶) — far above
float64 tiny (2.2e-308). Log-domain evaluation `log|g| = log½ + log|sin θ_k| + Σ log cos²(θ_j/2)`
agrees with direct evaluation to relative 2e-14 at every n. Float64 is adequate; the estimand was not changed.

## Anomaly 1 (substantive): the generic sample variance is exponentially hard to estimate for the global cost
`∂C_G/∂θ_0` is a product of n−1 iid `cos²` factors, so its 4th moment grows relative to
its variance²: **`E[g⁴]/Var² = (3/2)(35/18)^(n−1)`** (exact; `theoretical_fourth_moment`,
verified by quadrature). The relative SE of the N-sample variance is `√((E[g⁴]/Var² − 1)/N)`:
at N = 10 000 this is 0.014 (n=2), 0.47 (n=12), 1.8 (n=16), **25.7 (n=24)**. The N=10⁴
result therefore *cannot* resolve the variance for n ≳ 14 — the sample is dominated by
whether a few rare near-`|0>` initializations were drawn — and the observed ratios
(2.4, 0.04, 0.17, 0.04, 0.04) are all within ~1 predicted σ of 1. The local cost has
constant `E[g⁴]/Var² = 3/2`, which is why it is resolved perfectly at every n.

Consequences and what was done:
- The specified N=10⁴, all-n semi-log fit (slope −1.14, err 0.16) is contaminated by
  unresolved points. Reported as-is, plus an a-priori "resolved range" fit (criterion:
  predicted rel. SE < 0.5, from the exact formula, not from looking at the data):
  n ≤ 12, slope −1.019 (err 0.038), R² 0.998.
- Supplemental N=10⁶ run: resolved range extends to n ≤ 18 as predicted; all-n slope
  −0.988 (err 0.007).
- `factorized_global_second_moment_estimate`: same estimand, different estimator, using
  this benchmark's product structure (`E[g²] = ¼E[sin²]∏E[cos⁴]`, product of per-factor
  sample means, relative error ~√(0.94n/N)). It tracks theory at every n (ratios 0.95–1.10
  at N=10⁴; slope −0.979, err 0.002). **It is a diagnostic only — a generic circuit has
  no such factorization** — and is not the pipeline's BP statistic.
- The engineering decision was to report the primary N=10⁴ result unchanged and add
  these diagnostics; whether a different primary estimator or sample size should be
  adopted is a scientific choice left to the project lead.

This is itself relevant to the project: **measuring** `Var_θ[∂C]` deep in a barren
plateau by generic Monte Carlo over initializations needs a sample size that grows
exponentially in n, for the same reason the plateau exists.

## Success criteria (Task 14)
| | criterion | status |
|---|---|---|
| A | PennyLane cost/gradient = closed form | **pass** (≤ 1e-16) |
| B | global Var_emp tracks (1/8)(3/8)^(n−1) | **pass within predicted MC error at all n**; resolved (rel. SE < 0.5) for n ≤ 12 at N=10⁴, n ≤ 18 at N=10⁶; factorized diagnostic at all n |
| C | global semi-log slope ≈ log(3/8) | all-n N=10⁴: err 0.16 (contaminated, see Anomaly 1); resolved range: err 0.038; N=10⁶: err 0.007 |
| D | local Var_emp tracks 1/(8n²) | **pass** (ratios 0.992–1.009, all \|z\| < 1.3) |
| E | local log-log slope ≈ −2 | **pass** (−2.0003) |
| F | means compatible with 0 | **pass** (1/24 cells beyond 1.96σ) |
| G | no structural-zero artifact | **pass** (audit above) |
| H | all prior tests pass | **pass** (115/115) |

## WHAT THIS STAGE ESTABLISHES
- The pipeline reproduces a known controlled barren plateau: for this circuit and
  initialization distribution the global cost's gradient variance decays as
  (1/8)(3/8)^(n−1), exponentially in n.
- The matched local cost's gradient variance decays polynomially, as 1/(8n²).
- The numerical implementation (NumPy closed forms and the PennyLane circuit) agrees
  with the exact formulas, including 4th moments.
- The pipeline distinguishes exponential from polynomial scaling by model comparison
  (ΔAIC 29 and 108 in the correct directions at N=10⁴; 59 and 162 at N=10⁶).
- Exact sampling-error prediction for the variance estimator, and the finding that the
  generic estimator's cost grows exponentially in n for the global cost.

## WHAT IT CANNOT ESTABLISH
- That every global cost, or every VQA, has a barren plateau.
- That the Stage 1 hardware-efficient ansatz has a barren plateau (it has structural
  zeros, see below, and was not benchmarked here).
- Anything about shot noise, Langevin dynamics, QLO, escape from a plateau, FDT,
  polynomial escape time, or quantum advantage.

## Secondary note — the Stage 1 hardware-efficient ansatz (Task 15)
Stage 2 found that for the HEA (`RY·RZ` layers + CNOT ring, global cost `Z⊗…⊗Z`) some
parameters have `∂C/∂θ ≡ 0` for all θ. Cause: in the Heisenberg picture the observable is
pushed back through the last CNOT ring, `CNOT: Z_t → Z_c Z_t`, so `Z^{⊗n}` becomes a
Z-product on a *subset* of qubits (a single `Z_1` for n=3); every last-layer `RZ` commutes
with any Z-product (identically zero gradient), and every last-layer `RY` on a qubit *not*
in that subset also has zero gradient. For n=3, depth=2 that is 6 of 12 parameters
(k = 1, 6, 7, 9, 10, 11). These are exact zeros from commutation, not concentration, and
a `Var_θ` averaged over k would be diluted by them — which is why the HEA is not the Stage 3
benchmark. It was not modified.
