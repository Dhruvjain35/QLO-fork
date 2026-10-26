# B4: depolarizing-noise overlay

- **Design:** frozen in [`B4_CONFIG.md`](B4_CONFIG.md) (commit a226e85), with the predictions written beforehand as
  Propositions 5 and 6 of [`docs/theory/A2_PROPOSITIONS.md`](../theory/A2_PROPOSITIONS.md).
- **Results:** `results/b4_noise/`.
- **Code:** `src/qlo/b4/`, `src/qlo/experiments/b4_noise.py`.
- **Tests:** `tests/test_b4_noise.py`.
- **Re-run:** `python -m qlo.experiments.b4_noise`, about 30 s once the B1 caches exist.

No novelty claim is made.

## Summary

1. **The exact shot-ratio identity survives noise.** M_SW/M_LE = (2−Q)/(S−Q) holds on all 41.2 million noisy θ rows
   (max relative error 1.75 × 10⁻¹¹, none excluded), as Proposition 1 says it must.
2. **The general slope rule survives noise.** b_SW − b_LE stays within 0.012 decades/qubit of b_S in every cell and at
   every noise level, including cells where the exponents change a lot.
3. **Exponent doubling does *not* survive global depolarizing noise.** The fidelity floor (1−q)/2ⁿ creates b_r > 0.
   On the Stage 7 RX product:
   - the Loschmidt shot exponent moves from 4ⁿ to **8ⁿ** (local slope 0.90 against log₁₀ 8 = 0.903);
   - SWAP stays at **16ⁿ**;
   - the ratio falls from 2 to **4/3** (1.334 measured).

   The transition happens inside the tested range, at n* ≈ 15, 12, 9 and 5 for p = 10⁻⁴, 10⁻³, 10⁻² and 10⁻¹.
4. **Local depolarizing on the same circuit keeps doubling.** b_r = 0 exactly, and b_S drops to the
   Proposition 6 value (0.5834, 0.5451 and 0.4451 measured against 0.5831, 0.5447 and 0.4449). The ratio stays at
   about 2.
5. **The noise model, not just its strength, decides whether the exponent doubles.**

## 1. Why noise matters for this project

Every result before B4 assumed ideal, noiseless measurement. The principal track lists depolarizing noise as
uncovered (principal §3, "Regime of validity"), and so do the B1 and B2 reports. On hardware the trial state is mixed,
so B4 asks which parts of the measurement-cost picture are statements about statistics, and therefore survive noise,
and which are statements about pure-state concentration, and therefore may not.

## 2. Models and why the overlay is exact

| model | channel | exact consequence | where |
|---|---|---|---|
| global depolarizing | (1−p)ρ + p I/2ⁿ after each of L layers | F±' = qF± + (1−q)/2ⁿ, q = (1−p)^L, Δ' = qΔ | RX product (L = 1); all 16 B1 cells (L = 2, 4 or n) |
| local depolarizing | (1−p)ρ_j + p I/2 per qubit after its rotation | F±' = ∏_{j≠k} f_j · [(1−p)(1∓s)/2 + p/2], Δ' = ∏_{j≠k} f_j (1−p) s | RX product (stays a product state) |

**Global.** Global depolarizing commutes with unitaries, so the noisy shifted fidelities are exact functions of the
noiseless ones. B4 therefore reuses the B1 per-θ caches (same θ, seeds, circuits and positions) and the Stage 7 θ
stream for the RX product. No re-simulation is needed.

**Readout.** Noise acts on the trial state. The SWAP target copy is ideal, so both readouts estimate the same F±', as
in Stage 7.

**Precision fix.** At large n the floor (1−q)/2ⁿ is much bigger than qF±. Computing Δ' as a float difference of the
two overlaid fidelities then cancels to 0 in 0.06% of RX rows (far tail only). Δ' is therefore computed exactly as
qΔ, and passed through the per-θ pipeline with a consistency check (`quantities.per_theta(delta=...)`). Before the
fix 3,039 rows had to be excluded from the identity check. After it, none are.

## 3. Validation

| check | result |
|---|---|
| global overlay vs density-matrix simulation (PennyLane `default.mixed`, global-depolarizing Kraus channel after every layer); RX product and repo HEA depth 2, n = 2, 3 | max error 6.7 × 10⁻¹⁶ |
| local formula vs density matrix (`DepolarizingChannel`, p_PL = 3p/4), n = 2–4, both shifts | max error 5.1 × 10⁻¹⁴ |
| p = 0 reproduces the committed B1 medians (1,160 cell × n × seed rows) | max \|diff\| 3.6 × 10⁻¹⁵ |
| exact identity under noise, 41.2 M θ rows | max relative error 1.75 × 10⁻¹¹, 0 excluded |
| B4 tests | 14 passed |

## 4. RX product, global depolarizing

These are 10-seed means, full range n = 2–20 / n ≥ 8 (`predictions_vs_measured.csv`):

| p | b_S | b_r | b_LE | b_SW | b_SW/b_LE | ε_gap |
|---|---|---|---|---|---|---|
| 0 | 0.601 / 0.602 | 0.000 / 0.000 | 0.606 / 0.602 | 1.201 / 1.203 | 1.98 / 2.00 | −0.007 / −0.001 |
| 10⁻⁴ | 0.537 / 0.489 | 0.081 / 0.120 | 0.674 / 0.717 | 1.201 / 1.203 | 1.78 / 1.68 | −0.010 / −0.004 |
| 10⁻³ | 0.473 / 0.397 | 0.137 / 0.195 | 0.736 / 0.804 | 1.201 / 1.203 | 1.63 / 1.50 | −0.008 / +0.002 |
| 10⁻² | 0.403 / 0.329 | 0.200 / 0.260 | 0.803 / 0.868 | 1.201 / 1.203 | 1.49 / 1.39 | −0.006 / +0.006 |
| 10⁻¹ | 0.343 / 0.305 | 0.256 / 0.293 | 0.861 / 0.895 | 1.201 / 1.203 | 1.39 / 1.34 | −0.004 / +0.003 |
| asymptote (Prop. 5) | 0.301 | 0.301 | 0.903 | 1.204 | 1.333 | 0 |

Fits over a fixed n range mix the regimes on either side of the crossover. The **local** slopes over 3-point windows
(`window_slopes.csv`, `figures/transition_profile_rx_global.png`) show the transition directly:

| quantity | before n* | after n* |
|---|---|---|
| b_LE | log₁₀ 4 | log₁₀ 8 (0.90 at n ≈ 16–18 for p ≥ 10⁻²) |
| b_r | 0 | log₁₀ 2 |
| b_SW | log₁₀ 16 | log₁₀ 16 (unchanged; all p overlap) |
| exponent ratio | 2 | 1.334 |

The crossover n*, where q·median S equals the floor (`crossover.csv`), is 15.4, 12.1, 8.7 and 5.2 for
p = 10⁻⁴, 10⁻³, 10⁻² and 10⁻¹.

**Mechanism.** SWAP's per-shot variance (2−Q ≈ 2) never depended on S, so a fidelity floor cannot change it. The
Loschmidt variance is ∝ S. The floor props S up at 2^{1−n}, while the signal Δ' = qΔ keeps falling at 4^{−n}. The
Loschmidt readout loses its advantage from the vanishing-noise property, and that loss is exactly the b_r' = log₁₀ 2
term.

## 5. RX product, local depolarizing

| p | b_S measured (n ≥ 8) | b_S Prop. 6 | b_r | ratio (n ≥ 8) |
|---|---|---|---|---|
| 10⁻³ | 0.5834 | 0.5831 | −0.0001 | 2.00 |
| 10⁻² | 0.5451 | 0.5447 | −0.0001 | 2.00 |
| 10⁻¹ | 0.4451 | 0.4449 | −0.0001 | 1.99 |

Local noise makes both readouts cheaper per qubit, because each factor of F is lifted. It keeps r = (1−p) sin θ_k,
which does not depend on n, so doubling survives (`figures/local_noise_bS_vs_formula.png`).

## 6. Entangling cells (B1), global depolarizing

Ranges are over all 16 cells:

| p | b_r (n ≥ 8) | b_SW/b_LE (n ≥ 8) |
|---|---|---|
| 10⁻⁴ | −0.002 to 0.005 | 1.98–2.02 |
| 10⁻³ | −0.002 to 0.012 | 1.97–2.01 |
| 10⁻² | 0.003 to 0.028 | 1.90–1.98 |
| 10⁻¹ | 0.012 to 0.053 | 1.74–1.93 |

**Depth = n** (q = (1−p)ⁿ). Measured b_r' tracks Proposition 5(c):
- HEA EARLY: 0.051 against a predicted 0.048 at p = 10⁻¹, and 0.008 against 0.006 at p = 10⁻²;
- brickwork EARLY: 0.049 against 0.046;
- the ratio is 1.74 / 1.75 against a predicted 1.76 / 1.77.

**Fixed depth** (q constant). Here the floor must overtake a signal that decays at only 2.2–2.4ⁿ, so the crossover
is late. At n ≤ 16 the crossover is inside the range only at p = 10⁻¹, for 14 of the 17 cells (every family, depth and position, RX product included) (`crossover.csv`).
The measured b_r' has moved 0.1–69% of the way to its asymptote, and the fraction grows with p
(`fraction_toward_asymptote_b_r`). These cells are pre-asymptotic, as Proposition 5 anticipates. They are not a
contradiction.

**Gap rule.** ε_gap stays between −0.012 and +0.006 decades/qubit in every cell and at every p. It is largest at
p = 10⁻², where several cells sit in the middle of their transition and (H1) is most strained
(`figures/gap_rule_under_noise.png`).

## 7. What B4 supports

- **The exact identity is a statement about readout statistics.** It holds for noisy (mixed) trial states, exactly as
  Proposition 1 predicts.
- **The general slope rule b_SW − b_LE = b_S survives depolarizing noise** at all tested strengths, to ≤0.012
  decades/qubit.
- **"The exponent doubles" is a statement about pure-state concentration.** Global depolarizing breaks it through a
  fidelity floor:
  - on the product benchmark, Loschmidt rises from 4ⁿ to 8ⁿ and SWAP stays at 16ⁿ, so the ratio falls to 4/3;
  - in depth-n entangling circuits, noise adds −log₁₀(1−p) to b_r.
- **Local depolarizing on the product circuit preserves doubling**, with b_S lowered to a closed-form value. Whether
  doubling survives depends on the noise model.

## 8. What B4 does not establish

- Local depolarizing on entangling circuits. That needs density-matrix simulation and is untested here; only the
  product case is exact.
- Other noise channels: amplitude damping, dephasing, coherent errors, readout error.
- SWAP tests in which **both** copies are noisy. That readout estimates Tr(ρσ), a different quantity.
- The asymptotic fixed-depth entangling exponents. At n ≤ 16 those cells are pre-crossover except at p = 10⁻¹.
- Any hardware-cost comparison, or any novelty claim.
