# B4 frozen design: depolarizing-noise overlay

This was committed before any B4 number was computed. The predictions under test are Propositions 5 and 6 in
[`docs/theory/A2_PROPOSITIONS.md`](../theory/A2_PROPOSITIONS.md), committed with this file. The JSON block at the end
is `qlo.b4.config.B4Config().to_json()`, and the driver refuses to run unless the two match.

## Question

Does the measurement-cost picture survive depolarizing noise? Specifically:
1. Does the exact shot-ratio identity still hold?
2. Does the general slope rule b_SW − b_LE = b_S still hold?
3. Does exponent doubling, which needs b_r = 0, survive, and does the answer depend on the noise model?

## Noise models

| model | channel | effect on the shifted fidelities (exact) | applied to |
|---|---|---|---|
| global depolarizing | ρ ↦ (1−p)ρ + p I/2ⁿ after each of L layers, i.e. q = (1−p)^L | F±' = q F± + (1−q)/2ⁿ | RX product (L = 1) and every B1 entangling cell (L = depth: 2, 4 or n) |
| local depolarizing | ρ_j ↦ (1−p)ρ_j + p I/2 on every qubit after its rotation | F±' = ∏_{j≠k} f_j · [(1−p)(1∓s)/2 + p/2], f_j = (1−p)cos²(θ_j/2) + p/2 | RX product (stays a product state, so this is exact) |

**Global depolarizing.** Because the channel commutes with unitaries, the noisy shifted fidelities are an exact
function of the noiseless ones. B4 therefore reuses B1's per-θ F± caches: the same θ, seeds, circuits and positions,
with no re-simulation.

**Readout.** In both readouts, noise acts on the trial state only. The SWAP target copy is the ideal |0ⁿ⟩, so both
readouts estimate the same F±', exactly as in Stage 7. A SWAP test between two noisy copies estimates Tr(ρσ), a
different quantity, and is out of scope.

## Grid

| item | value |
|---|---|
| global depolarizing p | 0, 10⁻⁴, 10⁻³, 10⁻², 10⁻¹; p = 0 is the regression control and must reproduce B1 |
| local depolarizing p (RX only) | 0, 10⁻³, 10⁻², 10⁻¹ |
| RX product | n = 2..20; 10 seeds (11000–11009) × 25,000 θ; Stage 7 stream 20 (the B1 RX arm's θ) |
| entangling cells | all 16 B1 cells (HEA and RX–RY + CZ; depths 2, 4, n; EARLY / MIDDLE / LATE); B1 grids; 10 seeds × 4,000 θ |
| shots | continuous exact M at SNR ρ = 1 (Proposition 1) |
| fits | median-over-θ OLS slopes per seed, as in B1; ranges are the full grid and n ≥ 8; local 3-point slope windows for the transition profile |
| intervals | 10 seeds, B3 `summarize` (10,000 bootstrap replicates, seed 2026) |

## Validation (before any slope)

- Global overlay against explicit density-matrix simulation for n = 2, 3 (PennyLane `default.mixed` with a
  global-depolarizing Kraus channel after every layer). This covers the RX product and the repo HEA at depth 2.
- Local formula against `default.mixed` with single-qubit `DepolarizingChannel` for n = 2, 3, 4. PennyLane's
  convention is p_PL = 3p/4.
- Tolerance 10⁻¹² on F±.
- At p = 0, the per-cell medians must equal B1's committed `sample_summary.csv` to 10⁻¹².
- The identity check under noise must pass at 10⁻¹⁰.

## Predictions (Proposition 5 and 6; asymptotic, not assumed reached at n ≤ 20)

- **Global, RX product.** b_S' → log₁₀ 2, b_r' → log₁₀ 2, b_LE' → log₁₀ 8, b_SW' → log₁₀ 16, ratio → 4/3.
  The crossover n* is where q·median S ≈ 2(1−q)/2ⁿ.
- **Global, fixed depth.** b_S' → log₁₀ 2 and b_r' → b_S + b_r − log₁₀ 2.
- **Global, depth n.** b_S' → log₁₀ 2 and b_r' → b_S + b_r − log₁₀ 2 − log₁₀(1−p).
- **Local, RX product.** b_r' = 0, b_S'(p) = −(2/ln 10) ln[(√(1−p/2) + √(p/2))/2], and the ratio stays 2.
- **Every model.** Proposition 1 holds exactly, and the general slope rule holds wherever (H1) holds.

## Machine-readable configuration

sha256: `77e9e93a7e21d5ef1b9ad8015caa03b6a77af7b89ed0f69c8c7e8c3cc746ce38`

<!-- B4-CONFIG-JSON-BEGIN -->
```json
{
  "boot_seed": 2026,
  "global_p": [
    0.0,
    0.0001,
    0.001,
    0.01,
    0.1
  ],
  "identity_rel_tol": 1e-10,
  "local_p_rx": [
    0.0,
    0.001,
    0.01,
    0.1
  ],
  "n_boot_seed": 10000,
  "regression_tol": 1e-12,
  "rho": 1.0,
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
  "rx_samples": 25000,
  "rx_stream": 20,
  "secondary_n_min": 8,
  "seeds": [
    11000,
    11001,
    11002,
    11003,
    11004,
    11005,
    11006,
    11007,
    11008,
    11009
  ],
  "validate_local_n": [
    2,
    3,
    4
  ],
  "validate_n": [
    2,
    3
  ],
  "validate_theta": 6,
  "validate_tol": 1e-12,
  "window": 3
}
```
<!-- B4-CONFIG-JSON-END -->
