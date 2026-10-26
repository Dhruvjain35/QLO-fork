# B2: four fidelity-gradient estimators on one landscape

**Branch:** `dhruv/b2-additional-estimators`, built on `dhruv/stage7-upstream-integration` (193b4c7: principal
A1–A4 + Stage 7; no B1/B3/B5 files).

**Design freeze:** d601d5a (`B2_CONFIG.md`, `B2_HADAMARD_DERIVATION.md`), committed before any RX-product
required-shot or slope number was computed.

**Results:** `results/b2_estimators/`. **Code:** `src/qlo/b2/`, `src/qlo/experiments/b2_estimators.py`.
**Tests:** `tests/test_b2_estimators.py`.

AI assistance: the code, runs and report were produced with an AI coding assistant (Claude) under Dhruv's
direction. All numbers come from committed code and the frozen config.

## 1. Purpose

Stage 7 compared two readouts of one fidelity objective, Loschmidt and ancilla SWAP. B2 adds two more:

- the **destructive (Bell-basis) SWAP test**;
- a **Hadamard-test** fidelity estimator.

All four act on the same θ, state, target, F, cost, shift points and exact gradient. This turns the two-point
comparison into a four-estimator spectrum. B2 makes no novelty claim.

## 2. Frozen Stage 7 objective

The landscape is the Stage 7 RX product:
- state ⊗_j RX(θ_j)|0ⁿ⟩, target |0ⁿ⟩, F = |⟨0ⁿ|ψ⟩|², cost C = 1 − F;
- shifted component k = 0, with Δ = F₋ − F₊ and g = Δ/2;
- θ is the exact Stage 7 population (seed 0, stream 20, 100,000 θ per n, n = 2..20), plus 10 replicate seeds
  (12000–12009) × 25,000 θ for slope intervals.

The Loschmidt and SWAP medians reproduce Stage 7's `scaling_summary.csv` to 1.8e-15 on all 40 (scheme, SNR, n)
cells (`stage7_regression.csv`). Stage 7 is unchanged.

## 3. Four estimator definitions

| estimator | one shot | fidelity estimate | Var F̂ (exact) | gradient | executions per gradient |
|---|---|---|---|---|---|
| Loschmidt | Bernoulli(F) | K/M | F(1−F)/M | (F̂₋−F̂₊)/2 | 2M |
| ancilla SWAP | Z = ±1, P(+1) = (1+F)/2 | mean Z | (1−F²)/M | (F̂₋−F̂₊)/2 | 2M |
| destructive SWAP | Z = ∏(−1)^{aᵢbᵢ} over Bell pairs | mean Z | (1−F²)/M | (F̂₋−F̂₊)/2 | 2M |
| Hadamard U-statistic | X, Y = ±1, E = Re a, Im a | U_x + U_y | Var U_x + Var U_y | (F̂₋−F̂₊)/2 | 4M |

M is shots per shift for the first three, and shots per quadrature per shift for Hadamard. All four are unbiased
for F and g.

## 4. Access-model differences

The four estimators need different hardware capabilities. B2 is a **statistical** comparison under each
estimator's own access model, not a hardware-cost comparison.

- **Loschmidt** needs the target inverse V†.
- **Both SWAP tests** need two state copies per shot.
- **Hadamard** needs a coherent controlled-(V†U).

See §18 and `resource_accounting.csv`.

## 5. Destructive SWAP derivation

Take two copies A (|ψ⟩) and B (|φ⟩) and apply CNOT(Aᵢ→Bᵢ) then H(Aᵢ) on every qubit pair. This maps the Bell
basis to the computational basis. The singlet goes to (aᵢ, bᵢ) = (1, 1), and it is the only Bell state with
SWAPᵢ eigenvalue −1.

The single-shot record therefore gives Z = ∏ᵢ(−1)^{aᵢbᵢ}, an eigenvalue of SWAP = ⊗ᵢ SWAPᵢ. Hence:

- E[Z] = Tr[SWAP (ρ_A ⊗ ρ_B)] = |⟨φ|ψ⟩|² = F for pure states;
- Z² = 1, so Var Z = 1 − F² and P(Z = +1) = (1+F)/2.

These are exactly the ancilla-SWAP statistics, so with independent shots the fidelity and gradient estimators
are identical in distribution. Any mismatch would be a bug (Case C).

## 6. Destructive SWAP validation (`destructive_swap_validation.csv`, `swap_destructive_vs_ancilla_rx.csv`)

**Exact circuits.** Both tests were simulated as explicit gate sequences: 2n+1 qubits with Fredkin gates for
ancilla SWAP, 2n qubits with CNOT+H for destructive SWAP. On random complex pure-state pairs, n = 1–4, both give
P(+1) = (1+F)/2 to **4.4e-16**. The destructive E[Z] = F and Var Z = 1 − F² hold to the same precision.

**Finite shots.** At M = 64, 256 and 1024, full 2n-bit measurement records were drawn from the destructive
circuit's distribution and compared with the ancilla circuit and the Bernoulli model (36 cells).
- Mean z-scores |z| ≤ 2.42.
- Sample variance × M within 8% of 1 − F². This is consistent with reps of 2,000–4,000.

**RX sweep (control).** For the sweep, destructive SWAP gets its own path: E[Z±] built from explicit 2-qubit
Bell-circuit probabilities on each pair. It never calls ancilla-SWAP formulas.
- Required shots agree with Stage 7's ancilla SWAP to a median of about 1e-14 decades, with 99.9% of θ within
  2.7e-9 decades.
- Slopes agree to **9.6e-15**.
- The largest per-θ gap, 4e-4 decades, is float precision in the extreme tail. There a single pair overlap is
  about 1e-19, so E[z] = 1 − 2P(singlet) is formed next to P ≈ ½.

**Case C is not triggered.**

## 7. Hadamard overlap measurement

The real-quadrature test is H, controlled-W, H, measure ancilla Z, with E = Re⟨0ⁿ|W|0ⁿ⟩ and W = V†U. Inserting
S† before the last H gives E = Im. (Full derivation: `B2_HADAMARD_DERIVATION.md`.)

On the RX product, ⟨0|RX(θ)|0⟩ = cos(θ/2) is real, so y = 0 exactly. The primary estimator still measures both
quadratures, because it is defined for general complex overlaps; this landscape fact is not exploited.

## 8. Why naive squared sample means are biased

E[x̄²] = x² + (1 − x²)/M, so x̄² + ȳ² overestimates F by about 2/M. On a barren plateau F ≈ 4^−n, which is far
below 2/M at any affordable M. The plug-in estimator is not used anywhere.

## 9. Unbiased Hadamard U-statistic

U = (S² − M)/[M(M−1)] = (2/[M(M−1)]) Σ_{i<j} XᵢXⱼ, so E[U] = q². The fidelity estimator is
F̂_HT = U_x + U_y, from independent batches, and E[F̂_HT] = F.

It is not confined to [0, 1] and is never clipped. Exact frequencies (`hadamard_variance_validation.csv`):

| case | P(F̂ < 0) | P(F̂ > 1) |
|---|---|---|
| a = 0 | 0.25 (M = 2) to 0.63 (M = 256) | 0.25 (M = 2) to 0 (M ≥ 16) |
| x = 0.31, y = −0.42 | 0.42 (M = 3) to 0 (M = 256) | |

## 10. Exact Hadamard variance derivation

Summing covariances over pairs of pairs gives

    Var U = [2(1 − q⁴) + 4(M−2) q²(1 − q²)] / [M(M−1)]

and Var F̂_HT = Var U_x + Var U_y.

It was checked three ways:
- exhaustive enumeration of all 2^M sequences (M = 2–6);
- the exact lattice pmf for M ≤ 256, five (x, y) cases including non-real overlaps;
- 200,000-replicate Monte Carlo.

Results: the bias, variance error and pmf normalisation agree to ≤ **1.8e-15**. Monte Carlo mean |z| ≤ 2.19 and
variance relative error ≤ 1.3% (`figures/hadamard_variance_validation.png`). **Case D is not triggered.**

## 11. Hadamard parameter-shift gradient

ĝ_HT = (F̂₋ − F̂₊)/2 from four independent batches (x₊, y₊, x₋, y₋), with E = g and

    Var ĝ = [A + B(M−2)]/[4M(M−1)],  A = 2Σ(1 − q⁴),  B = 4Σ q²(1 − q²)

Unbiasedness and the variance formula were checked against the exact joint pmf of ĝ for M = 2–16 (error
≤ 8.9e-16). Because the variance depends on how F splits into x² + y², x± and y± are recorded per θ, not only F.

**Required shots.** SNR ≥ ρ becomes a quadratic in M. B2 solves it for the smallest integer M ≥ 2 by the
closed-form root followed by an exact integer check (`required_m_ht`; tested to be minimal and sufficient).

**Deep limit** (derived before the sweep, `B2_HADAMARD_DERIVATION.md` §6). Var ĝ ≈ 2/M² + S/M, which gives

    M_HT ≈ 2ρ²[1 + √(1 + 2r²/ρ²)]/(r²S)

This is the same 1/(r²S) form as Loschmidt's M_LE ≈ ρ²/(r²S), so B2 **predicted** the Loschmidt exponent at
8–10.9× the executions.

## 12. Shot conventions

| estimator | internal M | circuit executions per gradient component | state copies per shot |
|---|---|---|---|
| Loschmidt | per shift | 2M | 1 |
| ancilla SWAP | per shift | 2M | 2 |
| destructive SWAP | per shift | 2M | 2 |
| Hadamard | per quadrature per shift | 4M | 1 |

The primary unit is total executions. The internal M is reported alongside.

## 13. Circuit validation (`hadamard_circuit_validation.csv`)

The circuits were random 2-layer hardware-efficient circuits, n = 1–4, with genuinely complex overlaps (|Im a| up
to 0.92). Both the numpy statevector and the PennyLane `qml.ctrl` Hadamard tests return Re a and Im a to
**6.7e-16**, and x² + y² = F to the same precision.

## 14. RX-product required-shot scaling (SNR 1)

Median log10 required, Stage 7 population, 100,000 θ:

| estimator | n = 10: internal M | n = 10: total executions | n = 20: internal M | n = 20: total executions |
|---|---|---|---|---|
| Loschmidt | 5.697 | 5.998 | 11.725 | 12.026 |
| ancilla SWAP | 11.109 | 11.410 | 23.142 | 23.443 |
| destructive SWAP | 11.109 | 11.410 | 23.142 | 23.443 |
| Hadamard U | 6.373 | 6.975 | 12.399 | 13.001 |

The Hadamard/Loschmidt ratio of median total executions is 9.0 at n = 2 and 9.4–9.55 for n ≥ 4
(`figures/hadamard_required_shots.png`). That is inside the 8–10.9 band predicted in §11.

## 15. Four-estimator slope comparison

Slopes are of median log10 required (total executions), each called an RX-product benchmark scaling. The
replicate column is the 10-seed mean with its 95% percentile interval.

| estimator | range | Stage 7 population slope | R² | replicate seeds |
|---|---|---|---|---|
| Loschmidt | 2–20 | 0.6059 | 0.99994 | 0.6058 [0.6048, 0.6064] |
| Loschmidt | 8–20 | 0.6037 | 0.99999 | 0.6030 [0.6009, 0.6053] |
| ancilla SWAP | 2–20 | 1.2025 | 0.99999 | 1.2022 [1.2003, 1.2045] |
| ancilla SWAP | 8–20 | 1.2060 | 0.99999 | 1.2051 [1.2013, 1.2113] |
| destructive SWAP | 2–20 | 1.2025 | 0.99999 | 1.2022 [1.2003, 1.2045] |
| destructive SWAP | 8–20 | 1.2060 | 0.99999 | 1.2051 [1.2013, 1.2113] |
| Hadamard U | 2–20 | 0.6066 | 0.99992 | 0.6063 [0.6051, 0.6075] |
| Hadamard U | 8–20 | 0.6037 | 0.99999 | 0.6031 [0.6008, 0.6055] |

- The internal-M slopes are identical, because the factor 2M or 4M only changes the intercept.
- At SNR 2: Loschmidt 0.6070, SWAP 1.2026 (both), Hadamard 0.6071.
- Residuals are in `slope_summary.csv`.

**Exponents form two classes:**
- about log10 4: Loschmidt and Hadamard, whose intervals overlap;
- about log10 16: both SWAPs, identical.

## 16. Fixed-budget failure modes (`fixed_budget_failure_modes.csv`, figures 6–8)

Total budgets T = 32 to 32,768. Internal M = T/2 for Loschmidt and both SWAPs, T/4 for Hadamard. n = 6, 10, 14, 18.

- **Loschmidt fails by exact zeros.** At n = 10, P(ĝ = 0) is 0.85–1.0 for every budget. When the estimate is
  nonzero it is usually right: P(correct | nonzero) is 0.84–0.91, near (1+|r|)/2.
- **Both SWAPs fail by random signs.** P(zero) falls as ~M^−½ (0.14 to 0.004), and P(correct) ≈ P(wrong) ≈ 0.5.
  The two columns are identical to every printed digit.
- **Hadamard also fails by random signs, not by zeros.** At n = 10, P(zero) is 0.16 to 0.0004, and P(correct) is
  0.42 to 0.51, with P(correct | nonzero) about 0.50.
  - Its median SNR at a fixed budget is above SWAP's: at n = 10, T = 32,768, it is 0.023 against 0.0004.
  - It is below Loschmidt's (0.20).
  - Where the budget nears the requirement (n = 6, T = 32,768) its sign accuracy rises to 0.79, against 0.53 for
    SWAP and 1.00 for Loschmidt.
- **Hadamard method by budget:** exact lattice enumeration for M ≤ 512, seeded Monte Carlo (20,000 replicates)
  above that.

## 17. Hadamard sign / direction behaviour

The exact pmf of ĝ_HT (`figures/hadamard_distribution_examples.png`; n = 10 median-S θ; M = 8, 32, 128) is a
broad, symmetric lattice distribution centred near 0. Its width is set by about 2/M² + S/M, far above the true
|g| ≈ 1e-6. Exact zeros are rare and fall with M.

This is **noise-dominated random-sign failure**, the same failure type as SWAP, and not Loschmidt's exact-zero
starvation. The reason is that the U-statistic subtracts a deterministic M from S² in every batch, so the estimate
is almost never exactly zero.

Hadamard therefore combines **Loschmidt's exponent with SWAP's failure type**, at about 9.5× Loschmidt's
executions.

## 18. Resource-normalized comparison (`resource_accounting.csv`, figure 9)

| estimator | qubits per shot | copies | extra operations | executions per gradient |
|---|---|---|---|---|
| Loschmidt | n | 1 | needs V† (here identity) | 2M |
| ancilla SWAP | 2n+1 | 2 | n Fredkin gates + ancilla | 2M |
| destructive SWAP | 2n | 2 | n CNOT + n H, depth 2, no ancilla | 2M |
| Hadamard | n+1 | 1 | every gate of V†U controlled by the ancilla; 2 quadratures | 4M |

Measured in total executions, Hadamard costs about 9.5× Loschmidt, and the SWAPs cost about 10^5.4 (n = 10) to
10^11.4 (n = 20) times Loschmidt. No hardware-cost claim is made: copies, qubit-executions and control overhead
differ between estimators.

## 19. Optional entangling spot check (SECONDARY)

Setup: repo-layout HEA, depth = n, EARLY parameter (RY, qubit 0, layer 0), n = 6–12, 2,000 θ. Complex amplitudes
came from an explicit statevector that matches PennyLane to 1.7e-16 (`entangling_spotcheck*.csv`).

| estimator | slope of median log10 total executions |
|---|---|
| Loschmidt | 0.302 |
| Hadamard | 0.302 |
| SWAP (both) | 0.604 |

The Hadamard/Loschmidt execution ratio is 10^0.95 ≈ 9. The ordering and the exponent classes are therefore the
same as on the product circuit, with B1's entangling bases (about 2 and 4 per qubit) instead of 4 and 16. In this
spot check, destructive SWAP uses the validated ±1 model, because the state is not a product and an explicit
24-qubit Bell simulation was not run.

## 20. Numerical limitations

- **Stage 5 closed form.** F₊ = A(1−s)/2 loses relative precision when sin θ_k → 1 (cancellation). This is a
  frozen Stage 7 formula, kept unchanged. The amplitude path agrees to 5.7e-8 relative in that tail.
- **Destructive SWAP tail.** The Bell-pair E[z] is accurate to about 1e-16 absolute, so in tail rows with pair
  overlaps around 1e-19 the per-θ required shots differ from ancilla SWAP by up to 4e-4 decades. Medians and
  slopes agree to 1e-14.
- **Integer budgets.** Hadamard M is an exact integer. Loschmidt and SWAP use the Stage 7 ceil convention, which
  becomes continuous above 1e15 shots (n ≳ 14 for SWAP), as in Stage 7.
- **Fixed-budget Hadamard sample.** Fixed-budget Hadamard uses 300 θ (exact for M ≤ 512, Monte Carlo above). The
  others use 2,000 θ.
- **Distribution figure.** The exact-distribution figure uses M ≤ 128. The joint pmf at M = 512 needs a ~66k × 66k
  grid, so that panel was dropped (logged).
- **Case E.** The Hadamard inversion is stable to n = 20 (R² 0.99992, no non-finite rows), so Case E is not
  triggered.

## 21. Hardware / access limitations

The comparison is per estimator shot under each estimator's own access model:

| estimator | requires |
|---|---|
| Hadamard | a coherent controlled-(V†U), deeper per circuit |
| both SWAPs | two copies; the ancilla version also needs Fredkin gates |
| Loschmidt | V† |

There is no noise (B4), no shared or adaptive shot allocation, and no compilation cost. B2 does not say which
estimator is cheaper on hardware.

## 22. B2 outcome

**Case B, with a qualification.**

- Destructive SWAP reproduces ancilla SWAP exactly: circuits to 4.4e-16, slopes to 1e-14.
- The Hadamard U-statistic collapses onto the **Loschmidt exponent** (0.6066 against 0.6059 on n = 2..20; both
  0.6037 on n ≥ 8), at a constant 9.4–9.5× the executions, as derived in advance.
- **Qualification:** its finite-shot failure is SWAP-like random sign, not Loschmidt-like exact zeros. So there are
  four circuits but two exponent classes, while the failure-type behaviour splits differently: Loschmidt alone
  starves on zeros.
- Cases C, D and E are not triggered.

## 23. What B2 supports

- Destructive and ancilla SWAP are statistically identical estimators for pure states, as required, with
  different circuits.
- A correct Hadamard-test fidelity estimator is unbiased and needs both quadratures. Its exact variance is derived
  and validated.
- On the RX product, and in the entangling spot check, the Hadamard estimator has the Loschmidt shot exponent,
  not the SWAP one. Its constant is about 9.5× in executions.
- On these landscapes the shot exponent is set by whether the estimator's per-shot noise vanishes with F
  (Loschmidt, Hadamard) or not (SWAP). The way it fails at a fixed budget is a separate property.

## 24. What B2 does NOT establish

- Hardware cost or wall-clock superiority of any estimator.
- Behaviour under noise (B4), other targets, non-product targets for the destructive SWAP sweep, multi-term shift
  rules, or adaptive or shared shot schedules.
- A universal Hadamard exponent: these are RX-product benchmark scalings plus one small entangling spot check.
- Other Hadamard estimators. A known-real-overlap variant that skips the y batch would change the constant only;
  it is not the primary estimator and was not run.
- Any novelty or priority.
