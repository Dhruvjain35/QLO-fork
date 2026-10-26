# B5 follow-up: which statistic each result uses

Shot-scaling statements are comparable only if they use the same random variable, statistic, ensemble and measurement.
This table records those choices for every prior result relevant to candidates C1–C4, against Stage 7.

- Evidence ids refer to [`B5_EVIDENCE_LEDGER.md`](B5_EVIDENCE_LEDGER.md).
- Shot conventions are converted in [`B5_SHOT_CONVENTIONS.md`](B5_SHOT_CONVENTIONS.md).
- Statements marked *(our algebra)* are derived in this audit and are not in any source.

## 1. Table

| Paper | Result | Random variable | Statistic used | Scaling variable | Shot convention | Circuit ensemble | Parameter ensemble | Measurement scheme | Comparable to Stage 7? | Reason |
|---|---|---|---|---|---|---|---|---|---|---|
| Stage 7 (reference) | Loschmidt required shots ≈ 4ⁿ: median log₁₀M slope 0.600–0.607 (STAGE7.md §12) | Required integer M at fixed θ for SNR ≥ 1, 2; P_correct ≥ 0.75, 0.90; P(ĝ≠0) ≥ 0.9 | **Median over θ** (IQR, q90 also reported); reference slope from the log-typical A = 4^(−(n−1)) | n = 2…20 | M shots per shifted circuit; 2M per component; independent batches | Product RX circuit (not a two-design) | θ ~ U[−π, π]ⁿ, 100 000 θ per n, k = 0 | Global projector \|0ⁿ⟩⟨0ⁿ\|, 0/1 outcomes | — | Reference row |
| Stage 7 (reference) | SWAP required shots ≈ 16ⁿ: slope 1.197–1.203 | As above | As above | n = 2…20 | As above | As above | As above | SWAP-test ancilla Z, ±1 outcomes | — | Reference row |
| Teo 2023 | MSE_PS = d/(N_T(d+1) sin² s) (Eq. 13; D-02) | (Ŷ − Y)² for one gradient component | **Mean** over sampling, over Haar two-design modules and over inputs x | d = 2ⁿ at fixed N_T | N_T = total copies per component per Pauli term (= 2N) | Two-design modules (TDS, Case I) | Haar over trainable modules; data x averaged | Pauli observables in their eigenbases, ±1 outcomes, term by term | Partly | Same estimator, and the same ±1 per-shot variance as SWAP (D-03b). But the statistic is a circuit mean and the ensemble a two-design; no Loschmidt readout |
| Teo 2023 | N_* ≅ 32(d²−1)/(3d), so N_* ≳ O(2ⁿ) (Eq. 24, Fig. 5; D-06) | Copy number at which two estimators' MSEs are equal | Equality of circuit-averaged MSEs | d | N_T | TDS | Haar | Pauli, ±1 | No | Estimator crossover, not a resolution requirement. At N_* PS already has relative MSE 3/16 (our algebra) |
| Teo 2023 | D_θ0 ≳ O(poly(d)/N), so "N must … be exponentially large in n" (Eq. 26; D-07a) | max Var[f̂(θ ± θ0)] / \|f(θ+θ0) − f(θ−θ0)\|² | **Circuit average of a ratio**; order-of-magnitude argument | n (base unspecified) | N copies per shifted function | Two-design circuits | Haar | Pauli, ±1 (numerator O(1/N)) | Partly | Closest located analogue of Stage 7's per-θ SNR, but (i) averaged instead of median, and (ii) the literal average diverges on Stage 7's landscape (§2) |
| Teo 2023 | ⟨E[(PS)²]⟩ → 1/(2d) + 1/N_T → 1/N_T (Eq. 18; D-04) | Squared estimate of one component | Circuit mean | d at fixed N_T | N_T | TDS | Haar | Pauli, ±1 | Partly | Component-wise mean-square analogue of Stage 7's median full-vector norm ratio ‖ĝ‖/‖g‖ |
| Aghaei Saem 2026 | Cor. 2/4: parameter-shift GD indistinguishable from a random walk with probability ≥ 1 − c, c ∈ O(exp(−n)) (B-06a) | Update vector and whole trajectory | **Probability over random initialisations** that a hypothesis test cannot beat a parameter-independent null | n (polynomial vs exponential resources) | N shots per POVM per estimated quantity (per shifted loss term) | Any landscape whose POVM outcome probabilities concentrate (Def. 1) | Random initialisation | Pauli observables, two-outcome POVMs, ±1 | Partly | Event probability over θ, not a per-θ required-shot statistic; ±1 null only (the Loschmidt (0, 1) null is not the case written in (B15)) |
| Aghaei Saem 2026 | ε_N ≲ 1, so N ∈ Ω(exp n) (Eq. 12), with Var^(LE) = F(1−F) and Var^(SWAP) = 1 − F² (B-10a/b/c) | Estimated loss ℓ̂(α) | **Per-point estimator variance over landscape variance Var_α** (rule of thumb) | n | N shots per estimate | Two-design (fidelity example) | α over the variable space | Loschmidt and SWAP named for fidelity | Partly | Divides by the landscape-wide spread, not the local signal. On a heavy-tailed landscape this gives different bases ((4/3)ⁿ, (8/3)ⁿ; B5_MATH_COMPARISON §6.3) |
| Aghaei Saem 2026 | Figs. 3–4: 150 vs 2¹⁵ shots (n = 15); 10n vs 2ⁿ shots (n = 9–17) (B-07a, B-08a) | Displacement (1/N_p)‖θ^(t) − θ^(0)‖₁; loss curves | Mean and variance over initialisations; individual curves | Shot regime; n | N per loss estimate | Single X-rotation layer (the Stage 3–7 circuit family) | Uniform random initialisation | Global Pauli-Z (parity), ±1 | Partly | Same circuit family, but a parity cost, not fidelity, and qualitative shot regimes rather than required-shot medians |
| Thanasilp 2024 | P(κ̂ = 0) ≥ 1 − δ, δ ∈ O(c^(−n)); exact factor (1 − s)^N (SI Supp. Prop. 2; A-05, A-06a) | One fidelity (kernel) estimate | Probability over shots, integrated over the data distribution of κ | n via δ | N shots per kernel entry | Expressive or product embeddings (data-encoded) | Data pairs (x, x′) | Loschmidt (0/1) | Partly | Fidelity level; integrates over data instead of reporting per-point required shots |
| Thanasilp 2024 | SI Supp. Fig. 4: Loschmidt needs N ∈ Ω(2ⁿ) for a fixed non-zero fraction; SWAP "at least exponentially" (A-10a/b) | Per-entry estimate | **Fraction** of entries (over N_s = 25 inputs) that are non-zero (LE) or pass a binomial test (SWAP) | n = 5–40 | N shots per kernel value | Product single-qubit R_y encoding | Data uniform on [0, 2π] | Loschmidt and SWAP | Partly | Same product family and both readouts, but fidelity level. Ω(2ⁿ) refers to the mean scale μ = 2^(−n), a lower bound consistent with the log-typical 4ⁿ (PI-2) |
| Thanasilp 2024 | N ≥ 2‖O‖²_∞ log(2/p)/(ε̃² Var_α[X]) ∈ Ω(b^(2n)) (SI Supp. Prop. 5; A-12a) | Expectation-value estimate | Relative error against landscape variance; Hoeffding (range-based) | n via b | N per expectation value | General | α | Any bounded observable (range only) | No | Identical for both readouts by construction; ignores the per-shot variance that separates them |
| Arrasmith 2021 | Var_θ[ΔC] ≤ m²L²F(n) (Prop. 1, Cor. 1; C-02) | Exact cost difference ΔC | Mean and variance over random parameter points; Chebyshev | n via b | None (no measurement model) | Any cost with a barren plateau (Def. 1) | θ_A random; θ_B a translate or independent | None | No | Landscape statistic; says nothing about estimator distributions |
| Arrasmith 2021 | Median N_total to reach C = 0.4 grows exponentially (Fig. 3; C-04a/b) | Total shots used in one optimisation run | **Median over 20 runs** (N tuned per n) | n = 5–11 | N per cost evaluation; N_total per run | Layered hardware-efficient ansatz, p = n | Random initial angles | Local cost (observable from single-qubit projectors; readout circuit not described) | No (qualitatively consistent) | Different cost, readout and statistic (per-run total to a threshold); no exponent reported |
| Gentinetta 2024 | R_tot = O(M^4.67/ε²) for the dual QSVM (Eq. 11; E-03) | Decision-function error max_x \|h_R − h\| | Expected operator-norm error, then a probability > 1/2 (Markov/Chebyshev) | Data size M and accuracy ε (fixed n) | R shots per kernel entry | Fixed ZZ feature map | Training data | Loschmidt-type all-zero frequency | No | Kernel training complexity; no n-scaling; concentration assumed away |
| Gentinetta 2024 | R_tot = O(1/ε^(2.9±0.3)) for the approximate QSVM (Figs. 10–11; E-05) | Decision-function error after training | Mean over 10 repetitions (percentile bars) | ε (two fixed sizes: 2- and 8-dimensional data) | R shots per expectation value; SPSA steps | ZZFeatureMap + RealAmplitudes | Random initial weights | Global Z^⊗q, ±1 | No | SPSA, not parameter shift; ε-scaling at fixed n |

### Closure-audit additions

| Paper | Result | Random variable | Statistic used | Scaling variable | Shot convention | Circuit ensemble | Parameter ensemble | Measurement scheme | Comparable to Stage 7? | Reason |
|---|---|---|---|---|---|---|---|---|---|---|
| Mari 2021 | Var(ĝ) = [σ₀²(θ+s) + σ₀²(θ−s)]/(4N sin² s) (Eq. 45; F-01) | One gradient component at fixed θ | **Per-θ** variance / MSE over measurement outcomes | N (shots) | N shots per shifted circuit | Any rotation-like circuit (numerics: one 5-qubit circuit) | One fixed θ (Eq. A1) | Generic observable; σ₀² unspecified (both fidelity readouts named on p. 3) | Yes, structurally | Same estimator, same per-θ statistic and same shot convention; readout-specific σ₀² must be supplied (F-02) |
| Mari 2021 | FD/PS crossover at N ≈ 50 (Fig. 6; F-07) | Copy number at equal MSE | Equality of per-θ MSEs, simulated | N | N per expectation value | One 5-qubit circuit | One θ | σ_z on one qubit | No | Estimator crossover at one point, not a resolution threshold or an n-scaling |
| Zhan 2025 | v_proj = c(1 − c)/N, v_scm = (1 − c²)/N; swap-type less precise at small c (H-01, H-02) | One overlap estimate | MSE averaged over Haar pairs at fixed overlap (per-overlap for these two strategies) | c, N (and d) | N copies (pairs for joint strategies) | Qubit pairs; general d in the SI | Fixed overlap c | Projection onto a known state vs SCM / swap test | Partly | Same two per-copy variances as Stage 7's readouts, at the fidelity level; no gradients or concentration |
| Miranskyy 2025 | N_swap/N_inverse = ln F / ln[(1 + F)/2] → 2 as F → 1 (G-01) | Number of shots to detect a deviation | Asymptotic quantum-Chernoff detection count at error probability P_e | F (near 1) | N shots per test | Program-testing states | — | Inverse (Loschmidt-type) test vs swap test | No | Detection statistic near F = 1; differs from the estimation ratio (1 + F)/F away from F = 1 (B5_MATH_COMPARISON §9.2) |

## 2. One per-shot variance, several exponents (worked example on Stage 7's landscape)

*(Our algebra, with Stage 7 notation.)*
- Per-shot variances (B-10a; D-03b): Loschmidt F(1 − F) and SWAP 1 − F².
- Gradient variances (Stage 7 §5–§6): Var_LE = [A − A²(1+s²)/2]/(4M) and Var_SWAP = [2 − A²(1+s²)/2]/(4M).
- Landscape moments for θ ~ U[−π, π]ⁿ:
  - E_θA = 2^(−(n−1)) and E_θA² = (3/8)^(n−1);
  - E_θs² = 1/2;
  - E_θg² = (1/8)(3/8)^(n−1);
  - log-typical A = 4^(−(n−1)).

| Statistic | Loschmidt | SWAP | Comment |
|---|---|---|---|
| Per-θ target (SNR ≥ ρ or P_correct ≥ q), **median over θ** (Stage 7) | ≈ 4ⁿ | ≈ 16ⁿ | M ∝ 1/(As²) vs 2/(A²s²); the median follows the log-typical A |
| Per-θ target, **mean over θ** of the required M | ∞ | ∞ | E_θ[1/A] = E_θ[1/A²] = ∞, since sec²(θ_j/2) is not integrable over [−π, π] |
| **Ratio of means**: E_θVar ≤ E_θg² (mean-square resolution) | M = 2(4/3)^(n−1) − 3/2, i.e. (4/3)ⁿ | M = 4(8/3)^(n−1) − 3/2, i.e. (8/3)ⁿ | Checked numerically at n = 4–20 |
| **Mean of a ratio**: Teo's D_θ0 = ⟨Var/Δ²⟩ on this landscape | ∞ | ∞ | Same divergence as row 2 |
| Teo's two-design ensemble, mean-square criterion (gradient level) | not in Teo's model | N_T ≥ 2(d²−1)/d, i.e. M ≈ 2ⁿ | From Eq. (13) and Tab. I |
| B's ε_N on the fidelity, product landscape (B5_MATH_COMPARISON §6.3 b) | (2/3)ⁿ at log-typical F; (4/3)ⁿ at mean F | (8/3)ⁿ | Depends on which F is inserted |
| B's ε_N on the fidelity, two-design (B5_MATH_COMPARISON §6.3 a) | ≈ 2ⁿ | ≈ 4ⁿ | Fidelity level, not gradient level |

- **Reading.** The same per-shot variances produce bases 2, 8/3, 4 or 16, or an infinite mean, depending only on the
  statistic and ensemble.
- **Sample check.** Sample means of 1/cos²(θ/2) were 1.7×10⁴, 6.7×10⁵ and 4.2×10⁶ at 10³, 10⁵ and 10⁷ samples; the
  median stayed ≈ 2.
- **Gap between readouts.** In every finite row, the SWAP base exceeds the Loschmidt base. The size of the gap, a factor
  4 per qubit in the median rows, is specific to the per-θ median statistic.

## 3. Explicit comparison: Stage 7 vs Teo vs Aghaei Saem vs Thanasilp

- **Stage 7.**
  - Per θ: the exact law of ĝ (difference of binomials), then the smallest integer M that meets a target.
  - Across θ: medians and quantiles of that M over θ ~ U[−π, π]ⁿ.
  - Exponents are least-squares slopes of median log₁₀M against n, compared with log₁₀4 and log₁₀16 from the
    log-typical A.
  - The heavy upper tail is reported (IQR, q90), not averaged.
- **Teo.** Every quantity is a circuit mean (Haar over two-design modules, also over sampling and data):
  - MSEs (Eqs. 8, 13, 14, 16, 23);
  - the crossover N_* (Eq. 24);
  - the mean-square magnitudes (Eqs. 17–18).

  D_θ0 (Eq. 26) is a mean of a per-circuit ratio, used only for an order-of-magnitude argument. No per-circuit
  distribution, quantile or typical value is computed. The same ±1 per-shot variance as Stage 7's SWAP readout enters,
  but averaging it over a two-design gives a 2ⁿ scale, not 16ⁿ (§2).
- **Aghaei Saem.**
  - Main statements are **probabilities over initialisations** that a polynomial-shot procedure is statistically
    indistinguishable from a variable-independent one (Theorem 1, Corollaries 1–4). The relevant statistic is a
    hypothesis-test success probability, and "exponential" enters through c ∈ O(exp(−n)).
  - The ε_N rule of thumb compares a **per-point** estimator variance with the **landscape-wide** variance Var_α. On
    Stage 7's heavy-tailed landscape that denominator is dominated by rare near-target θ ((3/8)ⁿ ≫ 16^(−n)).
  - Numerics report means and variances of displacements over initialisations.
- **Thanasilp.** Statements are at the kernel (fidelity) level:
  - probabilities over data and shots (Props. 1–2);
  - a range-based (Hoeffding) shot count against Var_α (SI Supp. Prop. 5), identical for both readouts;
  - numerical fractions of non-zero or non-null estimates (SI Supp. Fig. 4). The "Ω(2ⁿ)" there is tied to the mean
    kernel value μ = 2^(−n) (PI-2).

## 4. Statistic-mismatch findings

1. **Circuit means vs per-θ medians.** Teo's results are circuit-averaged; Stage 7's are medians over θ. The same
   ±1-outcome variance yields 2ⁿ (Teo's two-design mean-square), (8/3)ⁿ (mean-square on Stage 7's landscape) or 16ⁿ
   (Stage 7's median). Teo's results therefore cannot be cited as giving, or as contradicting, Stage 7's 16ⁿ.
2. **Averages of ratios diverge on Stage 7's landscape.** Any "average required shots" or Teo-style ⟨Var/Δ²⟩ is
   infinite for θ ~ U[−π, π]ⁿ (E_θ[1/A] = ∞). Stage 7's use of medians is necessary, not a stylistic choice, and
   averaged statements from the literature do not transfer.
3. **Landscape variance vs local signal.** Aghaei Saem's ε_N and Thanasilp's Supp. Prop. 5 normalise by Var_α, which a
   heavy tail inflates. Stage 7 normalises per point by g². The resulting exponents differ (§2).
4. **Event probabilities vs required-shot statistics.** Aghaei Saem's corollaries give the probability (over θ) that a
   polynomial-shot procedure is indistinguishable from a null. Stage 7 gives the shots needed per θ to reach a target.
   One does not determine the other without extra assumptions.
5. **Mean scale vs log-typical scale.** Thanasilp's Ω(2ⁿ) refers to the mean kernel value; Stage 5/7's 4ⁿ refers to the
   log-typical value. These are consistent (Ω is a lower bound) but are not the same statistic (PI-2).
6. **Totals per run vs per-component shots.** Arrasmith's median N_total to a cost threshold aggregates over a whole run,
   N tuning and optimiser behaviour. It is not a per-component shot count.
7. **Data-size complexity vs qubit-number exponents.** Gentinetta's complexities scale with the data size M and the
   accuracy ε at fixed n, with concentration assumed away. They are not n-exponents.

This document is evidence for A1 and does not make the novelty decision.
