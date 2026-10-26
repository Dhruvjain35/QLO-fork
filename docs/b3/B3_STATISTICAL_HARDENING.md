# B3: Statistical hardening of the Stage 7 results

Delegated-track task B3 from Satyabrat's work allocation. Baseline: commit `ba51866` (Stage 7, 180 tests).
B3 adds uncertainty estimates to the existing Stage 7 evidence. It is not a new research stage, it makes no novelty
determination, and it does not modify any Stage 1–7 report, result or scientific definition. All Stage 7 quantities
are computed by calling the frozen Stage 5–7 functions.

Code: `src/qlo/hardening/`, `src/qlo/experiments/b3_hardening.py`, `tests/test_b3_hardening.py`.
Outputs: `results/b3_hardening/` (interval definitions in `results/b3_hardening/CI_METHODS.md`).

## 1. Purpose

Stage 7 reported, on one fixed fidelity landscape, the shots a finite-shot parameter-shift gradient needs. Median
required shots grow at a fitted slope of 0.600–0.607 decades per qubit for the Loschmidt (projector) readout and
1.197–1.203 for the SWAP test, with R² ≥ 0.9999. Those numbers came from one θ population (master seed 0). B3 asks:

1. How stable are the numbers on genuinely new initialization samples? (SEED, primary)
2. How much of each number is finite-θ sampling noise? (THETA, secondary)
3. Are the Stage 7 point estimates compatible with the hardened intervals?

## 2. Frozen Stage 7 baseline

Stage 7 is regenerated, not altered. Running the per-θ B3 pipeline on the Stage 7 seed and θ streams reproduces:
- all 100 Stage 7 required-shot medians (10 n × 2 schemes × 5 targets) to ≤ 3.6e-15 (`run_meta.json`);
- all 180 Stage 7 fixed-M probability medians in `paired_estimator_comparison.csv` exactly (difference 0.0).

Test 5 shows that the per-θ pipeline and the seed-level fit reproduce the Stage 7 implementation on the same data.
Test 6 reproduces the published Stage 7 closed-form (SNR) medians and slopes at full size (100k θ) to 1e-12.

## 3. Independent-seed design (PRIMARY)

- **Seeds.** 20 master seeds, 10000–10019. They are disjoint from the Stage 7 seed 0; this is checked in code and tested.
- **Required shots.** n = 2, 4, …, 20 (primary) plus 22 and 24 (extension), with 25,000 fresh θ per (seed, n). The
  sample size is the same for every cell. Within a seed, one θ array per n feeds both schemes and all 10
  (scheme, target) series. Targets match Stage 7: SNR ≥ 1, SNR ≥ 2, P_correct ≥ 0.75, P_correct ≥ 0.90,
  P(ĝ ≠ 0) ≥ 0.90.
- **Per-seed fit.** The Stage 7 fit, `median log10 M = a + b n`, is applied over three ranges:
  - n = 2..20 (primary, the Stage 7 range);
  - n = 8..20 (Stage 7 also reported these slopes);
  - n = 2..24 (extended, used only because 22 and 24 passed the checks in §6).

  Each fit is saved with slope, intercept, R², max residual, the n values used, θ per n, the method mix
  (closed form / exact / normal-cc / Skellam) and a diagnostic OLS slope SE (`seed_slopes.csv`).
- **Summary over seeds** (`seed_summary.csv`): mean, SD, median, IQR, min, max, the 95% percentile interval, and a 95%
  bootstrap CI of the mean, resampling seeds.
- **Exponent gap.** `γ_SWAP − γ_LE` is formed within each seed and then summarized. LE and SWAP results from the same
  seed are never treated as independent.

## 4. Theta-bootstrap design (SECONDARY)

- **Reference population.** The regenerated Stage 7 population (seed 0): 100,000 θ per n for required shots and 20,000
  per n for fixed-M probabilities. Stage 7 did not save per-θ values, so they were recomputed deterministically
  (§2 confirms they are identical).
- **Procedure.** 2,000 replicates. For each replicate and each n, one resampling-count vector is applied to every series
  of that population, so LE and SWAP stay paired on the same θ. Medians are recomputed, slopes refitted, and the gap
  formed within the replicate (`theta_bootstrap_slopes.csv.gz`, `bootstrap_summary.csv`).
- **Optional two-level bootstrap.** 2,000 replicates: resample seeds, then θ within each selected seed and n; the
  estimand is the mean slope over seeds, n = 2..20 only. It is reported in its own rows labelled HIERARCHICAL.

## 5. Why the two intervals differ

The SEED interval measures how much a complete fresh replicate moves. The THETA interval measures sampling noise inside
one fixed 100k population. Because the THETA reference *is* the Stage 7 population, "Stage 7 inside the THETA CI" is
nearly automatic and is not evidence of robustness; its width is the useful information. Details are in
`results/b3_hardening/CI_METHODS.md`.

## 6. Extended n / M range

**n = 22, 24: accepted** into the separately labelled extended fit. The primary fit stays at n = 2..20.

The predeclared per-point checks, run for every (seed, n) (`numerics.py`, `numerical_checks.csv`):
- every per-θ value is finite;
- no underflow (smallest A seen: 10^−37.3, far above the 1e-280 guard);
- no SWAP exact-bisection row has a float tie between q₋ and q₊;
- the Loschmidt direction and nonzero inversions are verified on 300 rows per target: P(M) ≥ q, and P(M_b) < q with
  M_b = min(M − 1, ⌊M(1 − 1e-5)⌋).

The SWAP direction targets at n ≥ 20 use the continuity-corrected normal inversion for 100% of θ, as in Stage 7. Its
error against exact integer inversion was measured at four budget decades (`numerical_extension.json`):
1.1e-4 / 1.2e-5 / 1.2e-6 / 9.4e-8 decades at 10^3.5 / 10^4.5 / 10^5.5 / 10^6.5 shots for q = 0.75 (similar for 0.90).
The error falls about 10× per decade, so the approximation becomes more accurate exactly where n = 22 and 24 need it.
All n = 22 and 24 points (20 seeds plus the reference) passed every check.

During development, the first version of the inversion check was too strict. It failed rows for two reasons that are
properties of the Stage 6/7 bisection, not numerical failures: log-space resolution at M ≳ 10⁹, and float equality at
the threshold above 2⁵³ shots. It was corrected before the full run. The tolerances are documented in `numerics.py` and
are tested to still reject a mis-inverted budget (test 10). The M = 1 floor artifact found at the same time is listed
under discrepancies (D4).

**M grid** for fixed-shot probabilities: 16, 64, 256, 1024, 4096, 16384, 65536, at every n = 2..24. These are exact
difference-of-binomial probabilities (no simulation), checked separately by finite-shot Monte Carlo at
M = 1024 / 16384 / 65536 and n = 8–24 (`mc_validation.csv`, 20,000 replicates per cell, Wilson intervals): 56 of 60
checks fall inside their Wilson interval, versus about 57 expected. The four misses are scattered and not systematic.

## 7. Loschmidt slope robustness (n = 2..20; 20 seeds × 25k θ)

| target | seed mean | seed SD | seed 95% percentile | seed-mean 95% CI | THETA 95% CI | HIERARCHICAL 95% CI | Stage 7 |
|---|---|---|---|---|---|---|---|
| SNR ≥ 1 | 0.6053 | 0.0010 | [0.6034, 0.6070] | [0.6049, 0.6057] | [0.6048, 0.6070] | [0.6047, 0.6060] | 0.6059 |
| SNR ≥ 2 | 0.6064 | 0.0010 | [0.6044, 0.6083] | [0.6060, 0.6069] | [0.6059, 0.6082] | [0.6058, 0.6071] | 0.6070 |
| P_c ≥ 0.75 | 0.6032 | 0.0009 | [0.6015, 0.6050] | [0.6028, 0.6036] | [0.6027, 0.6048] | [0.6026, 0.6039] | 0.6038 |
| P_c ≥ 0.90 | 0.6047 | 0.0009 | [0.6029, 0.6065] | [0.6043, 0.6051] | [0.6043, 0.6064] | [0.6040, 0.6053] | 0.6054 |
| P_nz ≥ 0.90 | 0.5995 | 0.0010 | [0.5981, 0.6014] | [0.5990, 0.5999] | [0.5990, 0.6011] | [0.5988, 0.6001] | 0.6001 |

- Per-seed R² ≥ 0.9998 in every seed.
- The diagnostic OLS slope SE (0.0013–0.0026) is of the same order as the seed SD here. It measures a different thing,
  and per §5 of CI_METHODS it is not used as a confidence interval.
- n = 8..20: seed mean 0.6014–0.6017, seed-mean CI about ±0.001.
- Extended n = 2..24: 0.6002–0.6051, THETA CI width about 0.0018.

## 8. SWAP slope robustness (n = 2..20)

| target | seed mean | seed SD | seed 95% percentile | seed-mean 95% CI | THETA 95% CI | HIERARCHICAL 95% CI | Stage 7 |
|---|---|---|---|---|---|---|---|
| SNR ≥ 1 | 1.2014 | 0.0019 | [1.1985, 1.2050] | [1.2006, 1.2022] | [1.2003, 1.2046] | [1.2002, 1.2026] | 1.2025 |
| SNR ≥ 2 | 1.2015 | 0.0019 | [1.1987, 1.2051] | [1.2007, 1.2023] | [1.2005, 1.2048] | [1.2003, 1.2028] | 1.2026 |
| P_c ≥ 0.75 | 1.1962 | 0.0019 | [1.1935, 1.1999] | [1.1955, 1.1971] | [1.1952, 1.1994] | [1.1950, 1.1975] | 1.1973 |
| P_c ≥ 0.90 | 1.1997 | 0.0019 | [1.1969, 1.2034] | [1.1989, 1.2006] | [1.1987, 1.2030] | [1.1985, 1.2010] | 1.2008 |

- n = 8..20: seed mean 1.2024 for every SWAP target, seed-mean CI [1.2007, 1.2043].
- Extended n = 2..24: 1.1985–1.2022.
- The SWAP "P_nz ≥ 0.90" slope is 0.0056 in every seed and every bootstrap replicate. This is by construction: its
  per-θ requirement is 32 shots for n ≥ 6, independent of θ. It has no reference value and is not a headline.

## 9. Exponent-gap robustness (paired within seed)

| target | n = 2..20 seed mean [seed-mean CI] | seed 95% percentile | THETA CI | HIERARCHICAL CI | n = 8..20 seed mean [CI] |
|---|---|---|---|---|---|
| SNR ≥ 1 | 0.5961 [0.5956, 0.5966] | [0.5945, 0.5982] | [0.5953, 0.5979] | [0.5954, 0.5968] | 0.6008 [0.5998, 0.6017] |
| SNR ≥ 2 | 0.5951 [0.5947, 0.5955] | [0.5938, 0.5971] | [0.5943, 0.5968] | [0.5944, 0.5958] | 0.6008 [0.5998, 0.6017] |
| P_c ≥ 0.75 | 0.5931 [0.5927, 0.5936] | [0.5916, 0.5952] | [0.5924, 0.5947] | [0.5923, 0.5937] | 0.6009 [0.5999, 0.6018] |
| P_c ≥ 0.90 | 0.5950 [0.5946, 0.5955] | [0.5935, 0.5970] | [0.5942, 0.5967] | [0.5945, 0.5958] | 0.6008 [0.5999, 0.6018] |

- The paired gap's seed SD is about 0.0011. If the LE and SWAP slopes were independent it would be
  √(0.0010² + 0.0019²) ≈ 0.0021; the reduction comes from LE and SWAP sharing θ within a seed.
- Over n = 2..20 the gap sits 0.005–0.009 below log10 4 = 0.6021, and every interval excludes 0.6021. Over n = 8..20
  every interval contains 0.6021. The full-range shortfall therefore comes from the small-n points (n = 2, 4), where
  the asymptotic scaling does not yet hold. This is a fit-range effect and not a new claim.

## 10. Conditional sign-law robustness

The fixed prediction is P(correct | ĝ_LE ≠ 0) → (1 + |s|)/2, with population median (1 + 1/√2)/2 = 0.85355. It is
not refitted. Cells cover n = 12–24 and M = 16–65536 (`sign_law_summary.csv`).

- **Deep regime** (n ≥ 18, every M; n = 16 at M ≤ 4096; n = 12–14 at M ≤ 256 to 1024): the prediction lies inside the
  THETA CI and the SEED 95% percentile interval in every cell.
  - Example, n = 20 and M = 1024: SEED mean 0.8547, percentile [0.8494, 0.8592]; THETA [0.8490, 0.8563].
  - Per-θ discrepancy (exact − (1+|s|)/2) at n = 20, M = 16: median 1.9e-12, 95th percentile 1.6e-7.
- **The prediction is reproduced per θ, not just in the median.** Using cancellation-free probabilities (D2), the
  observed reference median at n = 20 is 0.85267 for M = 16–1024. That equals the median of (1+|s|)/2 in the same
  20,000-θ sample (0.85267) to five digits. The gap to the population value 0.85355 is the θ-sampling noise of a median;
  it sits inside both intervals.
- **Departures.** The discrepancy is always ≥ 0 and grows with M·A, as expected for a statement that holds only in the
  M·A → 0 limit. At n = 12 (M ≥ 1024), n = 14 (M ≥ 1024 to 4096) and n = 16 (M ≥ 16384), the prediction falls outside
  the intervals: for example n = 12, M = 4096 gives an observed median of 0.868. The predeclared "deep regime" label
  (reference median LE P_zero ≥ 0.99) put most of these cells inside the regime. That criterion was too loose to
  guarantee the asymptotic limit (D3).

## 11. Fixed-shot zero and sign probabilities (`fixed_shot_summary.csv`)

- **Loschmidt P_zero.** Reaches 1 at fixed M as n grows, with tight intervals. At M = 1024 and n = 8, the reference
  median is 0.8755, THETA [0.867, 0.884], SEED percentile [0.870, 0.888].
- **SWAP P_zero.** Equals the central-binomial value C(2M, M)/4^M at every n ≥ 6 (0.07039, 0.01763 and 0.002204 at
  M = 64, 1024 and 65536), with intervals of width < 1e-6.
- **SWAP P(correct | ĝ ≠ 0).** 0.5000 at n ≥ 12 for every M.
- **Float ties.** The fraction of θ whose float q₊ = q₋ is 0.36% (n = 12), 11.3% (n = 20), 19.4% (n = 22) and 28.6%
  (n = 24). For those θ, the reported SWAP P_correct is the zero-signal value; the true value exceeds it by under about
  1e-7 at these M (Stage 7 §7). The SWAP fixed-M direction values at n ≥ 16 are therefore resolved only to about 1e-7.
  This does not affect the required-shot fits, which use the exact Δ = As/2.

## 12. Full-vector reliability (`vector_summary.csv`; 20 seeds × 400 θ × 25 shot replicates)

At n = 12, M = 1024. Values are the seed median, [IQR], and SEED 95% percentile interval.

| | Loschmidt | SWAP | Stage 7 (LE / SWAP) |
|---|---|---|---|
| P(full ĝ = 0) | 0.737 [0.725, 0.750], (0.714, 0.769) | 0, (0, 0) | 0.735 / 0 |
| median cos, given ĝ ≠ 0 | 0.704 [0.678, 0.724], (0.657, 0.749) | 0.0091 [0.0066, 0.0106], (0.0021, 0.0172) | 0.742 / 0.0094 |
| P(ĝ·g > 0) | 0.216 [0.207, 0.223], (0.187, 0.235) | 0.511 [0.509, 0.513], (0.503, 0.522) | 0.218 / 0.510 |
| component sign accuracy | 0.070 [0.065, 0.072], (0.056, 0.081) | 0.494 [0.493, 0.496], (0.492, 0.498) | 0.078 / 0.493 |
| median log10 ‖ĝ‖/‖g‖ | 0.400 [0.366, 0.428], (0.335, 0.468) | 4.58 [4.52, 4.67], (4.31, 4.80) | 0.328 / 4.55 |

Bootstrap CIs of the seed mean are in the CSV. Component sign accuracy counts exactly-zero components as incorrect.

- 45 of 350 Stage 7 vector values fall outside the 20-seed percentile interval (12.9%), including LE norm ratio 0.328
  above.
- This is the rate expected for a typical replicate. A fresh exchangeable draw lands outside the 2.5–97.5% percentile
  interval of 20 others 12.8% of the time (`interval_diagnostics.json`), because 20 seeds give only a coarse
  percentile interval.
- 26 of the 45 misses are at n = 4. There, Stage 7's 400-θ draw ranks 19th of 21 in mean log F, a high-fidelity draw,
  and all n = 4 metrics shift together.

## 13. Random-walk diagnostic

Setup: the Stage 7 diagnostic with η = 0.3, unchanged. 20 master seeds × 50 paired starts gives 1,000 starts per n, and
500 iterations. Exact GD, LE, SWAP and the SWAP-noise random walk start from the identical θ in every start (asserted in
code; tests 12 and 13). Files: `random_walk_summary.csv`, `random_walk_stratified_posthoc.csv`.

Pooled over all starts (SEED: seed-mean 95% CI):

| n = 10, M = 64 | SWAP | random walk | exact GD |
|---|---|---|---|
| wrong-direction step fraction | 0.461 [0.454, 0.467] | 0.500 [0.499, 0.501] | 0 |
| mean cos (nonzero steps) | 0.037 [0.032, 0.043] | 0.0001 [−0.0006, 0.0008] | 1 |
| P(F_final ≥ 0.5) | 0.165 [0.143, 0.188] | 0 | 0.140 [0.119, 0.161] |

- SWAP vs random walk, median Δlog10 F_final: +0.54 [0.33, 0.76] at M = 64 and +0.34 [0.26, 0.42] at M = 1024.
- At n = 12: SWAP mean cos 0.013 [0.009, 0.016] (M = 64); P(F_final ≥ 0.5) 0.055 [0.040, 0.070] vs 0 for the random
  walk.
- SWAP vs exact GD, ΔP(F_final ≥ 0.5): +0.025 [0.015, 0.035] at n = 10, M = 64; +0.002 [−0.007, 0.011] at n = 12,
  M = 64; +0.004 [0.000, 0.009] and 0.000 [−0.004, 0.004] at M = 1024 for n = 10 and 12.
- LE vs exact GD: ΔP = 0 at n = 10 and 12. LE takes exactly-zero steps 76% of the time (n = 10, M = 64) and 89%
  (n = 12, M = 64).

**Stratified by starting fidelity** (post-hoc, labelled as such):
- **Starts with F0 below the median** (the typical initialization). SWAP is consistent with the signal-free walk:
  - n = 10, M = 1024: mean cos 0.0004 [−0.0014, 0.0024], wrong fraction 0.501 [0.498, 0.503].
  - n = 12, M = 1024: mean cos 0.0004 [−0.0007, 0.0015].
  - n = 12, M = 64: mean cos 0.0011 [−0.0002, 0.0025].
  - At n = 10, M = 64 a residual cos of 0.003 [0.0008, 0.0054] is still resolved.
- **Starts between the median and 90th percentile of F0.** A small residual signal is resolved: mean cos 0.030–0.039 at
  n = 10 and 0.004 at n = 12.
- **Top 10% of F0** (median log10 F0 = −2.5 at n = 10, −3.3 at n = 12). Here the gradient is resolvable and SWAP tracks
  exact GD: P(F_final ≥ 0.5) is 0.91 vs 1.0 at n = 10 / M = 64, and 0.50 vs 0.50 at n = 12.

This qualifies a Stage 7 statement (D1).

## 14. Stage 7 point-estimate interval check (`stage7_interval_check.csv`)

The predeclared primary criterion is the SEED 95% percentile interval, because the Stage 7 estimate is one replicate.

| metric | Stage 7 | SEED 95% percentile | inside SEED? | THETA 95% CI | inside THETA? |
|---|---|---|---|---|---|
| LE headline range (5 targets) | 0.6001–0.6070 | per target, envelope [0.5981, 0.6083] | **yes, all 5** | envelope [0.5990, 0.6082] | yes, all 5 |
| SWAP headline range (4 targets) | 1.1973–1.2026 | per target, envelope [1.1935, 1.2051] | **yes, all 4** | envelope [1.1952, 1.2048] | yes, all 4 |
| each of the 10 fitted targets, n = 2..20 | §7–8 | §7–8 | yes, 10/10 | §7–8 | yes, 9/10 (see note) |
| each fitted target, n = 8..20 (LE 0.6031–0.6037, SWAP 1.2060) | | | yes, 9/9 | | yes, 9/9 |
| exponent gaps, n = 2..20 and 8..20 | | | yes, 8/8 | | yes, 8/8 |

- **Flagged, stricter column.** Most Stage 7 slopes lie *above* the bootstrap CI of the seed **mean**: 24 of 27 rows
  fail `inside_seed_mean_ci`. Investigation:
  - All rows share one θ population, so they move together and are not 27 independent misses.
  - After rescaling the seed SD from 25k to 100k θ, the z diagnostic is +0.68 to +1.62 (median about +1.1). That is a
    single draw about one standard deviation above the mean.
  - The seed-mean CI describes the average over 20 replicates (half-width about 0.0004). It is not the right yardstick
    for one replicate whose own θ-sampling SE is about 0.0006 (THETA bootstrap).
  - Conclusion: Stage 7's seed-0 population gave slopes about 0.0006 (LE) and 0.001 (SWAP) above the multi-seed average.
    That is well within replicate variation. The Stage 7 numbers are not altered.
- **Note.** The SWAP P_nz slope is "outside" its zero-width THETA interval only through float equality (0.0055669 in
  every replicate; §8). It is not a meaningful miss.

## 15. Numerical limitations

1. **SWAP fixed-M direction probabilities** at n ≥ 16 are float-limited for 3–29% of θ (true value within about 1e-7;
   §11). The required shots avoid this by using the exact Δ.
2. **SWAP direction required shots** at n ≥ 20 rely entirely on the continuity-corrected normal inversion. It is
   validated up to 10^6.5 shots with error shrinking about 10× per decade, but it cannot be checked exactly at 10²⁰⁺.
3. **Loschmidt direction required shots, 0.4–0.8% of θ** (|s| tiny, M·A > 10⁴) use the Skellam limit, as in Stage 7.
4. **Exact Loschmidt P_correct is not monotone in M at the 1e-5 level when M·A ≈ 10³–10⁴.** This was found in 99 of
   546,654 exact rows in the 11 affected (seed, n) points, all with |s| < 0.04.
   - Consequence: the returned M overshoots the minimal budget by at most 1e-4 decades (median 4e-6) —
     `numerical_nonmonotone_rows.csv`.
   - These 11 points are inside n = 2..20 and stay in the primary fit, which is never filtered. They are the only
     points that fail the per-point check (241 of 252 pass).
5. **The deep-regime criterion for the sign law** (median P_zero ≥ 0.99) is too loose (§10).

## 16. Discrepancies (flagged; Stage 7 unchanged)

- **D1. Random-walk statement too broad for the start population.** Stage 7 (§17, README) says SWAP-driven GD at
  n ≥ 10 is statistically indistinguishable from a signal-free random walk. With 1,000 paired starts that is not true
  for the start population as a whole: SWAP keeps a small, resolved signal (cos 0.01–0.05, wrong steps 0.46–0.49, and
  success rates matching exact GD rather than 0). The difference comes from the high-F0 tail. For the typical start
  (F0 below median) the statement holds within the intervals. With Stage 7's 50 starts the difference was not
  resolvable (Stage 7 already reported P(F_final ≥ 0.5) SWAP 0.06–0.08 vs random walk 0 at n = 10).
- **D2. Loschmidt P(correct | ĝ ≠ 0) is computed with cancellation in Stage 7.** Stage 7 forms P_correct (for s < 0)
  and 1 − P_zero by subtraction from about 1. Deep in the dead zone this keeps only a few digits:
  - at n = 20, 1,064 of 20,000 reference θ give NaN and per-θ errors reach 0.63;
  - medians move by about 0.001. Stage 7's reported 0.8533–0.8537 at n = 20 is reproduced exactly with its own
    formula; the cancellation-free values are 0.8527–0.8530;
  - the conclusion is unchanged, and the agreement is tighter than Stage 7 stated (§10).

  B3 uses both tails summed directly (`seed_replicates.direction_accurate`) for the sign law. It reports the Stage 7
  method alongside and does not alter Stage 7 code.
- **D3. Sign-law regime boundary.** The prediction fails at n = 12–16 for large M, inside the predeclared "deep" label.
  This is consistent with the law being an M·A → 0 limit. It is reported, not refitted.
- **D4. M = 1 floor artifact.** The Stage 6/7 bisection never evaluates 10^lo = 1 exactly, so rows whose true
  requirement is 1 shot are returned as 2. This affects 806 + 320 of the verified LE direction rows: 1,089 at n = 2, 36 at n = 4
  and 1 at n = 6. It cannot move a median unless the median budget is ≤ 2 shots, which never happens. It does not affect any
  fit.
- **D5. Stage 7 seed-0 slopes are about 1 SD above the multi-seed mean** (§14). Within replicate variation.

## 17. What B3 strengthens

- The measurement-dependent shot exponents are stable on fresh θ populations:
  - Loschmidt about 0.600–0.606;
  - SWAP about 1.196–1.202;
  - every seed's R² ≥ 0.9998;
  - seed-to-seed SD 0.001 (LE) and 0.002 (SWAP).
- The paired exponent gap is tighter still (SD about 0.001) and stays positive and near 0.59–0.60 in every seed.
- The scaling persists unchanged to n = 24 under numerically validated checks.
- Every Stage 7 headline slope lies inside both the seed-replicate and θ-bootstrap intervals.
- Exact zero/sign probabilities and full-gradient vector statistics replicate across 20 seeds at the rate expected for
  a typical replicate.
- The Loschmidt conditional sign law is confirmed per θ in its stated limit, more tightly than Stage 7 reported.

## 18. What B3 does NOT establish

- Anything beyond the RX-product circuit, the |0ⁿ⟩ target, U[−π, π] initialization, component k = 0 and independent
  batches per (k, ±). B1, the entangling sweeps, is not started.
- Anything about other readouts (B2), hardware noise (B4, Satyabrat's), shot-to-runtime normalization (A3) or a
  general theorem (A2).
- Novelty or prior-work status of any result. That is A1, a principal-track task, and it is untouched here.
- That SWAP-driven GD is a pure random walk for every start (D1).
- Exactness of SWAP required shots at n ≥ 20 beyond the measured normal-inversion error trend.

## Reproduce

```
.venv/bin/python -m pytest -v -W error::DeprecationWarning
.venv/bin/python -m qlo.experiments.b3_hardening --workers 8      # per-theta caches -> --work-dir (default: external SSD)
.venv/bin/python -m qlo.experiments.b3_hardening --fast --work-dir /tmp/b3fast --out-dir /tmp/b3fast_out   # smoke
```

The full computation took 3.2 h wall on 8 workers on a heavily shared machine (other jobs held the load average at
50–150); expect about 1 h unloaded. Caches make re-analysis cheap. Every result depends only on the fixed seeds, not on
`--workers`.

*AI assistance:* implementation and analysis were done with Claude Code under the project's predeclared protocol;
the results and their interpretation were reviewed by the author.
