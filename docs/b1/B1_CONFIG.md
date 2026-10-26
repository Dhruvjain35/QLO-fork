# B1 frozen configuration: entangling-ansatz sweeps

This file freezes the B1 configuration **before the full sweep was run**. It is committed on
`dhruv/b1-entangling-sweeps` ahead of any full-run output, so the commit timestamp is the registration time.
Before freezing, the only computations were (i) a runtime/memory preflight that timed the simulator on the
largest cells and printed no slopes, and (ii) a smoke run of the pipeline on a reduced configuration (3 seeds,
n ≤ 8, 300 θ). That run was used only to check plumbing, the gradient cross-checks and the identity check. Its
slopes were not inspected.

The machine-readable block at the end is `qlo.b1.config.B1Config().to_json()`. The driver
(`python -m qlo.experiments.b1_entangling`) refuses to run unless the two match exactly. Any later change to
this file is visible in git history and must be logged in `results/b1_entangling/numerics_log.md` with a reason.

The A2 numerics in `principal/a2_numerics/` and the A2 table in `principal/QLO_Principal_Track.md` §3 were
**not read** before this freeze. B1 reads them only in its last phase (`a2`), after every B1 number has been
written.

## 1. What is tested

The prediction is the principal-track A2 concentrated-regime slope rule, using the derivation in principal §3
(not the §6 bullet, which has a sign typo):

    median_theta log10 S      = a_S  - b_S  n
    median_theta log10 |r|    = a_r  - b_r  n
    median_theta log10 M_LE   = a_LE + b_LE n
    median_theta log10 M_SWAP = a_SW + b_SWAP n
    prediction:  b_LE = b_S + 2 b_r,   b_SWAP = 2 b_S + 2 b_r,   b_SWAP - b_LE = b_S   (main equation)

Here S = F₊ + F₋, Δ = F₋ − F₊, r = Δ/S and g = Δ/2 = ∂C/∂θ_k with C = 1 − F. The shot requirements are
M_LE = ρ²[F₊(1−F₊)+F₋(1−F₋)]/Δ² and M_SWAP = ρ²[2−F₊²−F₋²]/Δ², with ρ = 1. The exact identity is
M_SWAP/M_LE = (2−Q)/(S−Q), Q = F₊²+F₋². No slope value is hard-coded or tuned anywhere.

## 2. Circuit families (target |0^n⟩, θ iid U[−π, π], F = |⟨0^n|U(θ)|0^n⟩|²)

| id | definition | source |
|---|---|---|
| `rx_product` (Family 0) | F = ∏_j cos²(θ_j/2), shifted component k = 0 | exact Stage 7 benchmark (`qlo.stage5.theory`, `qlo.stage7.analysis.sample_theta`, stream 20) |
| `hea_ring` (Family 1) | per layer: RY(θ[l,q,0]) RZ(θ[l,q,1]) on every qubit, then CNOT(0,1), CNOT(1,2), …, CNOT(n−2,n−1), CNOT(n−1,0) | the repo `HardwareEfficientAnsatz(n, depth, "ring")` (`src/qlo/circuits/hardware_efficient.py`) |
| `rxry_czbrick` (Family 2) | per layer: RX(θ[l,q,0]) RY(θ[l,q,1]) on every qubit, then open-boundary CZ brickwork: even l CZ(0,1), CZ(2,3), …; odd l CZ(1,2), CZ(3,4), … | B1 fallback family ("RX–RY + CZ brickwork") |

No second or "algebra-controlled" ansatz is defined in the repo or in the principal work, so Family 2 is the
spec's named fallback and nothing else. It differs from Family 1 in its rotation set (RX, RY instead of RY,
RZ), its entangler (diagonal CZ instead of CNOT), its topology (open nearest-neighbour brickwork instead of a
sequential ring) and its light cone.

Simulation uses a batched numpy statevector (`qlo.b1.circuits`, complex128, PennyLane wire order). It is
checked against PennyLane states and PennyLane autograd on the repo class, and against an independent
PennyLane template for Family 2.

## 3. Depth regimes and n ranges (frozen)

| regime | depth | n grid (both entangling families) |
|---|---|---|
| `d2` | 2 | 4, 6, 8, 10, 12, 14, 16 |
| `d4` | 4 | 4, 6, 8, 10, 12, 14, 16 |
| `dn` | n | 4, 6, 8, 10, 12, 14 |
| RX product | — | 2, 4, …, 20 (the Stage 7 / B3 range) |

Why depth = n stops at n = 14: one cell at (n = 16, depth 16) costs about 4 × 16/14 ≈ 4.6 times the
n = 14, depth 14 cell, which is ≈25 CPU-min per family per 40,000 θ, so about 2 CPU-h per family. The spec allows
stopping at 14. Every n listed is fitted; none is removed after results are seen.

**Runtime/memory preflight** (single process, machine under other load; ms per θ for all three positions,
from one forward and one backward pass):

| cell | ms/θ | CPU-min for 10 × 4,000 θ |
|---|---|---|
| hea_ring n16 d2 | 23.4 | 15.6 |
| hea_ring n16 d4 | 48.5 | 32.3 |
| rxry_czbrick n16 d2 | 19.0 | 12.7 |
| rxry_czbrick n16 d4 | 42.4 | 28.3 |
| hea_ring n14 d14 | 37.1 | 24.8 |
| rxry_czbrick n14 d14 | 39.7 | 26.4 |
| hea_ring n12 d12 | 6.3 | 4.2 |
| hea_ring n14 d4 | 11.2 | 7.4 |

The total is ≈3 CPU-h, run on 6 worker processes with ≤0.65 GB resident each. Per-θ caches (F₊ and F₋ per
position, about 0.2 MB per cell) go to `/Volumes/SSD Disk  1TB/qlo-b1-work`. Statevectors are never saved.

## 4. Parameter positions (predeclared)

All positions act on qubit 0 and use the first rotation of the layer, θ[l, 0, 0]. That is RY for `hea_ring`
and RX for `rxry_czbrick`; both have the ordinary ±π/2 shift rule. No RZ is ever a predeclared position.

| label | layer |
|---|---|
| EARLY | 0 (first layer) |
| MIDDLE | floor(depth/2) |
| LATE | depth − 1 (final layer) |

At depth 2, MIDDLE (layer 1) and LATE (layer 1) are the same parameter. It is simulated and reported once,
under LATE, so depth-2 cells have two distinct positions. In regime `dn` the MIDDLE and LATE layers move with n
by definition. The three positions share each θ sample, so position differences are paired by θ and seed.

## 5. Structural-zero audit (before the main run)

- Sample: 200 θ per (family, regime, n), on a stream independent of the master seeds,
  `SeedSequence([0xB1, 0xA0D17, family, regime, n])`.
- Per position, four computations are compared, with agreement measured as |difference|/S per θ and
  tolerance 1e-9:
  1. F± from the production forward/backward brackets;
  2. F± from independent full re-simulation at θ ± π/2 e_k;
  3. the analytic derivative from generator insertion, which uses no shift rule;
  4. PennyLane autograd on the repo `HardwareEfficientAnsatz` (Family 1) or on an independent PennyLane
     template (Family 2), at every audited n.

  Any disagreement STOPs the run as an implementation error.
- Numerical zero: |r| ≤ 1e-10.
- Classes:
  - STRUCTURAL: every audited θ is a numerical zero.
  - DEGENERATE: zero fraction above 0.01 (but not 1), or Var(r) ≤ 1e-20.
  - VALID: otherwise.
- Positive control: the final-layer RZ on qubit 0 of the repo HEA must come out STRUCTURAL. The final CNOT ring
  fixes ⟨0^n| and RZ is diagonal. Otherwise the audit cannot detect structural zeros and the run STOPs.
- Fallback rule (used only if a predeclared position is not VALID): take the nearest earlier rotation of the
  same gate type (same rotation index) in program order with VALID audit statistics. Record the original
  position, the fallback and the reason in `position_fallbacks.csv`. A structural position never enters a fit.

## 6. Seeds and sample counts

- Master seeds: 11000, …, 11009. They are 10 independent seeds, disjoint from Stage 7 (0) and B3 (10000–10019);
  the driver enforces this.
- Entangling sweeps: 4,000 θ per (family, regime, n, seed), drawn from
  `SeedSequence([0xB1, family, regime, n, seed])`. All positions share these θ.
- LE and SWAP quantities are always formed from the same per-θ F₊ and F₋ arrays.
- Exact analytic shot requirements are used; there is no finite-shot Monte Carlo in the scaling analysis.
- There is no cell-specific reduction. The counts above hold for every cell.

## 7. Per-θ quantities and edge cases

For each θ the run computes:
- F±, S, Δ, r, g and Q;
- the variance prefactors (S−Q)/4 and (2−Q)/4;
- M_LE and M_SWAP at SNR ρ = 1, in log10 and continuous (exact analytic, no ceiling);
- R = M_SWAP/M_LE and R_identity = (2−Q)/(S−Q).

The two variances are computed on separate arithmetic paths: Bernoulli for LE, the SWAP ancilla probability
q = (1+F)/2 for SWAP. R_identity is computed from S and Q directly.

SNR 2 adds exactly log10 4 to every θ under the continuous convention, so its slopes equal the SNR-1 slopes and
it is not fitted separately.

Edge cases are flagged and counted, never dropped silently:

| case | handling |
|---|---|
| S = 0 | r undefined (NaN), counted |
| Δ = 0 | log10\|r\| = −∞ and M = +∞; they stay in the medians as order statistics |
| zero LE variance | M_LE = 0 |
| S < 1e-280 | underflow flag |

Medians run over every non-NaN row, and NaN rows are counted in `sample_summary.csv`. A non-finite median STOPs
the fit.

The Stage 7 integer-budget convention, log10 max(ceil M, 1), is used only in the RX regression comparison with
B3, because B3 used it.

## 8. Exact shot-ratio identity (implementation check)

Every non-degenerate θ (S > 0, Δ ≠ 0, nonzero LE variance) of every cell must satisfy
|R − R_identity|/R_identity ≤ 1e-10. The maximum absolute error, maximum relative error and number of
excluded rows are reported. A violation STOPs the run: it is an implementation error, not a result.

## 9. RX regression arm (Family 0), mandatory gate

- B1 arm: 10 B1 seeds × n = 2..20 × 25,000 θ per (seed, n), the B3 per-seed size. Every θ goes through the
  generic B1 per-θ pipeline (F₊ and F₋ from the closed form).
- B3 intervals:
  - b_LE, b_SWAP and the gap (SNR 1, ceil convention): read from `results/b3_hardening/seed_summary.csv`, rows
    `primary_2_20` and `n_ge_8`.
  - b_S and b_r: B3 published no intervals for these. B1 regenerates the B3 θ populations (B3 seeds
    10000–10019, 25,000 θ, stream 20) and computes them with B3's own interval settings (10,000 bootstrap
    replicates, seed 2026). It first checks that the regenerated populations reproduce B3's published per-seed
    LE and SWAP slopes to ≤ 1e-12, and STOPs otherwise.
- PRIMARY acceptance (gate; range n = 2..20): for each of b_LE (ceil), b_SWAP (ceil), gap (ceil), b_S and b_r,
  the B1 10-seed mean must lie inside the B3 seed 95% percentile interval. This is the rule B3 used to check
  Stage 7.
- If any primary check fails, this is CASE E and the run STOPs before any entangling result is interpreted.
- Secondary checks (reported, not gating):
  - the n ≥ 8 range;
  - overlap of the B1 and B3 bootstrap CIs of the mean;
  - the number of B1 seeds inside the B3 interval;
  - approximate values: |b_S − log10 4|, |b_r|, |b_LE − log10 4| ≤ 0.02 and |b_SWAP − log10 16| ≤ 0.04.
- The RX arm is also run through the full B1 slope-rule analysis (continuous M, ranges 2..20 and 8..20).

## 10. Fits, residuals and intervals

- For each (family, regime, position, seed):
  - take the median over θ at each n;
  - fit by OLS over n (`qlo.stage6.analysis.linear_fit`, = `np.polyfit`);
  - save slopes, intercepts, R² and residuals.
- Fit ranges:
  - PRIMARY: the whole grid of the regime.
  - SECONDARY: n ≥ 8 of the same grid (d2 and d4: 8..16; dn: 8..14; RX: 8..20).
- Per seed:
  - ε_LE = b_LE − (b_S + 2b_r);
  - ε_SWAP = b_SWAP − (2b_S + 2b_r);
  - ε_gap = (b_SWAP − b_LE) − b_S;
  - slope ratio b_SWAP/b_LE, against the predicted (2b_S+2b_r)/(b_S+2b_r).
- Intervals use the B3 `qlo.hardening.intervals.summarize`: seed mean, SD, median, IQR, 95% percentile interval
  and bootstrap 95% CI of the seed mean, with 10,000 replicates and boot seed 2026. Independent seeds are the
  primary uncertainty.
- **PRIMARY acceptance per cell:** the bootstrap 95% CI of the seed-mean ε_gap contains 0.
- Also reported:
  - the 95% percentile interval;
  - the same checks for ε_LE and ε_SWAP;
  - effect sizes in decades/qubit, absolute and relative to b_S;
  - a secondary practical-equivalence check (bootstrap CI inside ±0.02 decades/qubit).
- Limitation: with 10 seeds, the percentile bootstrap of the mean can under-cover slightly. This is reported
  as a limitation and the rule is not changed.

## 11. Exponent-doubling check (§15)

Consistency of b_SWAP/b_LE with 2 is tested only when the bootstrap CI of b_r contains 0 **and**
|mean b_r| ≤ 0.10 × mean b_S. In that case the test is whether the bootstrap CI of the observed ratio contains 2.
Otherwise the result table shows the observed ratio against the predicted (2b_S+2b_r)/(b_S+2b_r). The
difference between the two always gets a CI.

## 12. Concentration classification (per cell and range, on the seed-mean median log10 S)

**CLEARLY CONCENTRATED** requires all five:
1. the b_S bootstrap CI lies above 0;
2. the median S is strictly decreasing across the range;
3. the mean per-seed R² of the log10 S fit is ≥ 0.99;
4. curvature |b_S(upper half) − b_S(lower half)| ≤ 0.25 b_S, where the halves are the first and last
   ceil(k/2) points;
5. the median S is ≤ 0.1 at every n in the range.

**TRANSITIONAL**: (1) and (2) hold and the median S at the largest n is ≤ 0.1, but (3), (4) or (5) fails.

**NOT CLEARLY CONCENTRATED**: otherwise.

The exact identity (§8) is checked separately and does not depend on this class.

## 13. Outcome classification (predeclared)

Per-cell rule check:

| label | condition |
|---|---|
| CONSISTENT | the ε_gap, ε_LE and ε_SWAP bootstrap CIs all contain 0 |
| GAP-ONLY | only the ε_gap CI contains 0 |
| DEVIATES | the ε_gap CI excludes 0 |

Per-cell case:

| case | condition |
|---|---|
| A | CONSISTENT and CLEARLY CONCENTRATED |
| B | not CONSISTENT and not clearly concentrated; the identity holds, so this is a finite-n or transition deviation |
| D | not CONSISTENT although CLEARLY CONCENTRATED; investigate, do not hide |
| — | "consistent (not clearly concentrated)" otherwise |

§22 outcome per (family, regime, range), across positions. "b_r approximately zero" means the same thing as
the doubling-eligibility rule of §11.
- **A**: b_r is approximately zero at every position.
- **B**: some position has b_r not approximately zero, while ε_gap is consistent with 0 everywhere.
- **C**: the ε_gap CI excludes 0 at some position.

Overall B1 outcome (§23). Every case that applies is listed, separately for the primary and the secondary range:
- **E**: the RX regression fails (STOP).
- **A**: every clearly concentrated cell is CONSISTENT.
- **B**: the identity holds and every non-CONSISTENT cell is outside the clearly concentrated regime.
- **C**: within a family and regime, the rule check differs between positions, and b_r differs between those
  positions.
- **D**: some clearly concentrated cell is not CONSISTENT.

## 14. Secondary checks

- θ bootstrap, limited subset: regime d4, seed 11000, both families, all positions, primary range. It uses
  2,000 paired resamples of the θ rows within each n, and its spread is compared with the seed spread.
- Conditional sign-law spot check (§20):
  - cells: n = 12, seed 11000, every family × regime × distinct position;
  - θ rows: those closest to the 0.10, 0.25, 0.50, 0.75 and 0.90 quantiles of S in that cell;
  - shots: M = 4^k, k = 0..8;
  - probabilities: exact P(correct | ĝ ≠ 0) for the Loschmidt estimator, from B3's cancellation-free binomial
    difference (`direction_accurate`), with p_pos = F₋ and p_neg = F₊;
  - comparison: the error against (1+|r|)/2, plotted against M·S. Nothing is fitted.
- A2 comparison (§21): last phase only, and only for cells that genuinely correspond to an A2 run (same family,
  depth and parameter; A2 shifted the first rotation on qubit 0 of the repo HEA, i.e. B1's EARLY position). It is
  qualitative agreement, not exact equality, because A2 used its own sample size and seed.

## 15. Machine-readable configuration (`B1Config().to_json()`)

sha256 of this JSON: `2b7306ae18f9f6caf833670faf6ab55d48d11dcbb394d13930ab70bc5d77e497`

<!-- B1-CONFIG-JSON-BEGIN -->
```json
{
  "audit_agreement_tol": 1e-09,
  "audit_min_var_r": 1e-20,
  "audit_pennylane": true,
  "audit_samples": 200,
  "audit_valid_max_zero_fraction": 0.01,
  "audit_zero_tol_r": 1e-10,
  "b3_regeneration_tol": 1e-12,
  "b3_seeds": [
    10000,
    10001,
    10002,
    10003,
    10004,
    10005,
    10006,
    10007,
    10008,
    10009,
    10010,
    10011,
    10012,
    10013,
    10014,
    10015,
    10016,
    10017,
    10018,
    10019
  ],
  "boot_seed": 2026,
  "br_small_fraction": 0.1,
  "conc_curvature_max": 0.25,
  "conc_median_S_max": 0.1,
  "conc_r2_min": 0.99,
  "equivalence_margin": 0.02,
  "families": [
    "hea_ring",
    "rxry_czbrick"
  ],
  "identity_rel_tol": 1e-10,
  "n_boot_seed": 10000,
  "n_grid_d2": [
    4,
    6,
    8,
    10,
    12,
    14,
    16
  ],
  "n_grid_d4": [
    4,
    6,
    8,
    10,
    12,
    14,
    16
  ],
  "n_grid_dn": [
    4,
    6,
    8,
    10,
    12,
    14
  ],
  "positions": [
    "EARLY",
    "MIDDLE",
    "LATE"
  ],
  "regimes": [
    "d2",
    "d4",
    "dn"
  ],
  "rho": 1.0,
  "rotation_index": 0,
  "rx_component": 0,
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
  "rx_sanity_tol_bSWAP": 0.04,
  "rx_sanity_tol_bS_bLE_br": 0.02,
  "rx_stream": 20,
  "samples_per_cell": 4000,
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
  "sign_S_quantiles": [
    0.1,
    0.25,
    0.5,
    0.75,
    0.9
  ],
  "sign_n": 12,
  "sign_seed_index": 0,
  "sign_shots": [
    1,
    4,
    16,
    64,
    256,
    1024,
    4096,
    16384,
    65536
  ],
  "theta_boot_regime": "d4",
  "theta_boot_reps": 2000,
  "theta_boot_seed_index": 0
}
```
<!-- B1-CONFIG-JSON-END -->
