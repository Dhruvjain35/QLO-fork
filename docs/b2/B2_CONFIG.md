# B2 frozen design: four fidelity-gradient estimators

This document freezes the B2 design **before the full sweep**. It is committed first as "b2: freeze four-estimator
comparison design". Before the freeze, three things were checked on small validation inputs:

- the Hadamard variance formula, by exhaustive enumeration;
- the explicit SWAP circuits;
- the explicit Hadamard circuits.

No RX-product required-shot or slope number had been computed. The JSON block at the end is
`qlo.b2.config.B2Config().to_json()`, and the driver refuses to run unless the two match.

## 1. Common objective (frozen Stage 7)

- **Landscape:** |ψ(θ)⟩ = ⊗_j RX(θ_j)|0ⁿ⟩, target |0ⁿ⟩, F = |⟨0ⁿ|ψ(θ)⟩|², C = 1 − F.
- **Shifted component:** k = 0, with F± = F(θ ± π/2 e_k), Δ = F₋ − F₊ and g = Δ/2.
- **Primary θ population:** exactly the Stage 7 required-shots population, `qlo.stage7.analysis.sample_theta(n,
  100000, seed=0, stream=20)`, for n = 2, 4, …, 20.
- **Pairing:** all four estimators use the same θ, the same F± and the same exact g.
- **Slope uncertainty:** 10 replicate seeds, 12000–12009, × 25,000 θ on the same stream. These are disjoint from
  Stage 7, B3 and B1.

## 2. The four estimators

M is shots **per shift** for estimators 1–3. For the Hadamard test it is shots **per quadrature per shift**.

| # | estimator | single shot | fidelity estimate | Var(F̂) | gradient | executions per gradient component |
|---|---|---|---|---|---|---|
| 1 | Loschmidt / projector (Stage 7, unchanged) | Bernoulli(F) | K/M | F(1−F)/M | (F̂₋−F̂₊)/2 | 2M |
| 2 | ancilla SWAP (Stage 7, unchanged) | Z ∈ {±1}, P(+1) = (1+F)/2 | mean Z | (1−F²)/M | (F̂₋−F̂₊)/2 | 2M |
| 3 | destructive SWAP (Bell-basis) | Z = ∏(−1)^{aᵢbᵢ}, P(+1) = (1+F)/2 | mean Z | (1−F²)/M | (F̂₋−F̂₊)/2 | 2M |
| 4 | Hadamard U-statistic | X, Y ∈ {±1}, E = Re a, Im a | U_x + U_y | Var U_x + Var U_y (B2_HADAMARD_DERIVATION §4) | (F̂₋−F̂₊)/2 | 4M |

- **Estimator 3** is simulated as an explicit 2n-qubit circuit: CNOT(Aᵢ→Bᵢ), then H(Aᵢ), then measure every
  qubit. Z is −1 for each singlet pair (1, 1).
  - Its per-shot probability on the RX sweep is computed from explicit 2-qubit Bell-circuit probabilities on each
    qubit pair, which is valid because the states are product states. Ancilla-SWAP formulas are never called for it.
  - Any statistical disagreement between estimators 2 and 3 is a **bug** (Case C), not a finding.
- **Estimator 4** is the primary Hadamard fidelity estimator.
  - It uses the unbiased U-statistic, never the plug-in x̄² + ȳ², and is never clipped.
  - Both quadratures are always measured, even though y = 0 on the RX product.

## 3. Required shots (exact, SNR ρ = 1 primary, ρ = 2 secondary)

| estimator | rule | source |
|---|---|---|
| LE and ancilla SWAP | M = max(⌈M_cont⌉, 1) | the Stage 7 functions (`qlo.stage7.required_shots.snr_shots`) |
| destructive SWAP | the same integer rule, applied to its own ±1 model: M = ⌈ρ²(2 − e₊² − e₋²)/(e₋ − e₊)²⌉ with e± = E[Z±] | explicit Bell-pair probabilities |
| Hadamard | smallest integer M ≥ 2 meeting the exact variance | `required_m_ht` (exact integer inversion) |

**Resource unit (primary):** total circuit executions per gradient component, i.e. 2M or 4M. The internal M is
always reported alongside.

**Fits:** median_θ log10(total executions) against n, OLS, on the ranges `primary_2_20` and `n_ge_8`. Seed
replicate intervals use the B3 `summarize` utility (10,000 bootstrap replicates, seed 2026). Each fit is called an
"RX-product benchmark scaling", not a universal exponent.

## 4. Validation (before any slope; tolerances)

- **Destructive SWAP:**
  - Analytic: E[Z] = F and Var Z = 1 − F² (derivation in the report).
  - Exact circuit: for n = 1..4 random pure pairs, the explicit destructive and ancilla circuits must give
    P(+1) = (1+F)/2 with |error| ≤ 1e-12.
  - Finite shots: at M ∈ {64, 256, 1024}, full 2n-bit records sampled from the circuit distribution; the sample
    mean, variance and pmf are compared with the Bernoulli model, and the finite-shot difference against the
    ancilla circuit is reported.
- **Hadamard circuits:** n = 1..4 random complex HEA circuits; numpy and PennyLane `qml.ctrl` expectations against
  Re a and Im a, and x² + y² against F, all to 1e-12.
- **Hadamard estimator:**
  - Exact enumeration (M ≤ 256) of the mean, variance, support, P(F̂ < 0) and P(F̂ > 1) against the formulas, to
    1e-12.
  - Seeded Monte Carlo with 200,000 replicates at M ∈ {2, 3, 4, 8, 16, 64, 256}, reported as z-scores.
- **Gradient:** the exact small-M difference distribution gives the mean (unbiased) and the variance formula.
- **Rule:** if the Hadamard variance fails these checks, that is **Case D: STOP before fitting slopes.**

## 5. Fixed-budget failure modes

- **Budgets:** total executions T ∈ {32, 128, 512, 2048, 8192, 32768}.
  - For LE, ancilla SWAP and destructive SWAP: M = T/2.
  - For Hadamard: M = T/4.
- **Cells:** n ∈ {6, 10, 14, 18}.
- **θ:** the Stage 7 fixed-shot population (seed 0, stream 30). LE and both SWAPs use the first 2,000 θ with exact
  binomial differences (Stage 6/B3 functions). Hadamard uses the first 300 of the same θ, with exact lattice
  enumeration for M ≤ 512 and seeded Monte Carlo (20,000 replicates, seed 2027) above that.
- **Metrics:** P(ĝ = 0), P(correct), P(wrong), P(correct | ĝ ≠ 0), SNR, and gradient MSE (= Var for all four,
  since all are unbiased).

## 6. Secondary entangling spot check (only after the RX analysis)

- Repo-layout HEA (RY, RZ + CNOT ring), depth = n, n ∈ {6, 8, 10, 12}.
- EARLY parameter: RY on qubit 0, layer 0.
- 2,000 θ, seed 13000.
- Complex shifted amplitudes a± from an explicit statevector; all four estimators' required executions computed
  exactly.
- Labelled SECONDARY ENTANGLING SPOT CHECK. It is not a sweep.

## 7. Predeclared outcomes

| case | meaning |
|---|---|
| A | destructive SWAP = ancilla SWAP, and Hadamard has a distinct third scaling or failure mode |
| B | destructive SWAP = ancilla SWAP, and Hadamard collapses onto the Loschmidt exponent (derivation §6 predicts this; the sweep tests it) |
| C | destructive SWAP ≠ ancilla SWAP: a bug, never a finding |
| D | the Hadamard variance fails simulation: STOP before slopes |
| E | the Hadamard inversion is unstable at deep n: report only the trustworthy range |

## 8. Machine-readable configuration

sha256: `9dc965c2ede0a00145b75827382fd47333de4b6b11d17f5749cf3e4e0c58cf4a`

<!-- B2-CONFIG-JSON-BEGIN -->
```json
{
  "boot_seed": 2026,
  "budgets_total_executions": [
    32,
    128,
    512,
    2048,
    8192,
    32768
  ],
  "circuit_tol": 1e-12,
  "estimators": [
    "loschmidt",
    "swap_ancilla",
    "swap_destructive",
    "hadamard_u"
  ],
  "fit_ranges": [
    [
      "primary_2_20",
      2,
      20
    ],
    [
      "n_ge_8",
      8,
      20
    ]
  ],
  "fixed_n": [
    6,
    10,
    14,
    18
  ],
  "fixed_samples": 2000,
  "fixed_samples_hadamard": 300,
  "fixed_stream": 30,
  "hadamard_exact_max_m": 512,
  "hadamard_exact_validation_max_m": 256,
  "hadamard_mc_reps": 20000,
  "hadamard_validation_m": [
    2,
    3,
    4,
    8,
    16,
    64,
    256
  ],
  "mc_seed": 2027,
  "n_boot_seed": 10000,
  "replicate_samples": 25000,
  "replicate_seeds": [
    12000,
    12001,
    12002,
    12003,
    12004,
    12005,
    12006,
    12007,
    12008,
    12009
  ],
  "req_stream": 20,
  "rho_primary": 1.0,
  "rho_secondary": 2.0,
  "rx_n": [
    2,
    4,
    6,
    8,
    10,
    12,
    14,
    16,
    18,
    20
  ],
  "spot_n": [
    6,
    8,
    10,
    12
  ],
  "spot_samples": 2000,
  "spot_seed": 13000,
  "stage7_samples": 100000,
  "stage7_seed": 0,
  "swap_equality_tol": 1e-12,
  "validation_mc_reps": 200000,
  "validation_shots": [
    64,
    256,
    1024
  ],
  "variance_tol": 1e-12
}
```
<!-- B2-CONFIG-JSON-END -->
