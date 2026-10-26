# Stage 7 — One landscape, two measurement schemes

Stage 6's projector-vs-parity contrast compared two *different* cost landscapes: parity has 2^{n−1}
global minima and a larger typical gradient. Stage 7 removes that confound. The state, fidelity
objective, parameter vector, exact gradient and optimization landscape are all held fixed, and only the
physical readout of the fidelity changes: a **Loschmidt / projector** measurement vs a **SWAP test**.
No optimizer is implemented. Stage 3–6 code is reused unmodified. All numbers are from one run of
`python -m qlo.experiments.stage7 --workers 5` (`results/stage7/`).

## 1. Motivation
Stage 6 found count starvation (projector) vs directional ambiguity (parity), with both needing ≈ 4ⁿ shots.
But the two objectives differed in landscape, so part of that contrast could come from cost geometry
rather than from measurement statistics. Here both schemes estimate the *same* number.

## 2. The Stage 6 landscape confound
Parity: C_Z = (1 − ∏cos θ_j)/2, with 2^{n−1} global minima and typical |g| ≈ 2^{−(n+1)}. Projector: C = 1 − ∏cos²(θ_j/2),
with one minimum and typical |g| ≈ 4^{−n}. Stage 6's matched-|g| analysis controlled the gradient magnitude but not the
landscape. Stage 7 needs no post-hoc matching at all (§13).

## 3. Prior-work boundary (details in §18–19)
Already established, and **not claimed here**:
- Loschmidt fidelity estimates collapse toward zero under exponential concentration.
- SWAP-test estimates become statistically indistinguishable from data-independent ≈ 50/50 outcomes.
- Different POVMs for the same fidelity have different finite-shot variances.
- Exponentially concentrated quantities need exponential measurement resources.
- Global-Pauli parameter-shift GD with polynomial shots is statistically indistinguishable from a random walk.

Sources: Thanasilp et al., Nat. Commun. 15, 5200 (2024), and Aghaei Saem, Tafreshi, Holmes, Thanasilp,
Quantum Sci. Technol. 11, 015049 (2026), doi:10.1088/2058-9565/ae2202. **Stage 7 is a replication /
specialization / extension test.**

## 4. Common fidelity landscape (frozen, Stages 3–5)
`|ψ(θ)⟩ = ⊗_j RX(θ_j)|0ⁿ⟩`, θ_j ~ iid U[−π, π], target `|0ⁿ⟩`, `F = ∏_j cos²(θ_j/2)`, `C = 1 − F`. For component k:
`A = ∏_{j≠k} cos²(θ_j/2)`, `s = sin θ_k`, `F_± = F(θ ± π/2 e_k) = A(1 ∓ s)/2`, `g = ∂C/∂θ_k = A s/2`.
The shifted fidelities match the circuit fidelity to 2.2e-16. The gradient matches a central finite difference to 8.6e-11.

## 5. Loschmidt (projector) estimator
Each shot is Bernoulli(F), with `K_± ~ Bin(M, F_±)`, `F̂ = K/M`, `Ĉ = 1 − F̂`, and
`ĝ_LE = (Ĉ₊ − Ĉ₋)/2 = (K₋ − K₊)/(2M)`, `E ĝ = g`,
`Var = [F₊(1−F₊) + F₋(1−F₋)]/(4M) = [A − A²(1+s²)/2]/(4M)`, `SNR² = M A s²/[1 − A(1+s²)/2]`.
This is the Stage 5 estimator. The variance and SNR agree with the Stage 5 functions to ≤ 1e-12 relative (tests).

## 6. SWAP-test estimator
The ancilla Z of the standard SWAP test has `E Z = F`, i.e. `P(+1) = q = (1 + F)/2`. With `K_±` counting +1 outcomes,
`F̂ = 2K/M − 1` and `Ĉ = 1 − F̂ = 2 − 2K/M`, so

    ĝ_SWAP = (Ĉ₊ − Ĉ₋)/2 = (K₋ − K₊)/M.

**The sign was checked, not assumed.** Built from the Ĉ definitions, the estimator equals the simplified
form to 1.4e-16. Its exact mean, from enumerating the joint count distribution, equals the finite-difference
derivative, and the sign of q₋ − q₊ equals the sign of g.
`E ĝ = q₋ − q₊ = (F₋ − F₊)/2 = A s/2 = g`. `Var F̂ = (1 − F²)/M`.
`Var ĝ = [2 − F₊² − F₋²]/(4M) = [2 − A²(1+s²)/2]/(4M)` (using `F₊² + F₋² = A²(1+s²)/2`, checked to 1.1e-16).
`SNR² = M A² s²/[2 − A²(1+s²)/2]`.

Unbiasedness and both variances were verified by **exact enumeration** (bias ≤ 1.3e-16, variance relative error
≤ 2e-15) at four (A, s, M) points. Over 300 random cases: closed vs generic variance ≤ 6.7e-16 relative, SNR vs g²/Var
≤ 6.5e-16.

**Deep plateau (A → 0).** `SNR²_LE / (M A s²) → 1` and `SNR²_SWAP / (M A² s²/2) → 1` (both 1.000 at A = 1e-4).
The paired SNR ratio is `SNR²_SWAP/SNR²_LE ≈ A/2`.

## 7. Exact finite-shot gradient distributions
Both estimators have the form `ĝ = c (K_pos − K_neg)/M` with independent binomial counts:
- **Loschmidt:** p_pos = F₋, p_neg = F₊, c = ½. Both probabilities are O(A), near 0.
- **SWAP:** p_pos = q₋, p_neg = q₊, c = 1. Both probabilities are ½ + O(A), near ½.

In both schemes `c (p_pos − p_neg) = g` exactly. The implied gradient differs from A s/2 by ≤ 1.7e-16 over 20 000 θ per n,
for every n (`theory_validation.json → common_landscape`). All zero/sign probabilities come from the Stage 6 exact
difference-of-binomials code. It matches brute force to 3.4e-14 and has passed integer-M monotonicity checks (largest
decrease of P_correct: 3e-11; P_zero never increases).

**Precision note.** For SWAP, q₋ − q₊ = A s/2 is lost next to ½ once A|s| ≲ 1e-16. Every SWAP quantity that depends on
the difference (required shots, SNR, information distances) is therefore computed from the exact A s/2 or in log space.
The fixed-M exact probabilities at n ≥ 6 are affected for 0.005–11% of θ, where the float q₊ = q₋. There the computed P_correct
equals the zero-signal value (1 − P_zero)/2, while the true value exceeds it by less than about 1e-7 at the tested M
(`swap_frac_float_tie`).

`figures/same_landscape_two_estimators.png` shows the two exact distributions for one θ at n = 4, 8, 12 (M = 1024):
- **Loschmidt:** mass concentrated on a few atoms, mostly at exactly 0 (P(ĝ=0) = 0.007, 0.917, 0.999).
- **SWAP:** a wide, nearly symmetric lattice distribution about 0 (P(ĝ=0) = 0.017–0.018), with sd ≈ 1/√(2M) regardless of g.

## 8. Exact-zero probability
Median P(ĝ_k = 0 | θ, M) over 20 000 θ per n (`paired_estimator_comparison.csv`):

| n | LE M=64 | SWAP M=64 | LE M=1024 | SWAP M=1024 | LE M=16384 | SWAP M=16384 |
|---|---|---|---|---|---|---|
| 4 | 0.235 | 0.070 | 7.3e-4 | 0.0167 | 4e-37 | 0.0018 |
| 6 | 0.879 | 0.0704 | 0.222 | 0.0176 | 5.6e-4 | 0.0044 |
| 8 | 0.992 | 0.0704 | 0.876 | 0.0176 | 0.217 | 0.0044 |
| 10 | 0.9995 | 0.0704 | 0.992 | 0.0176 | 0.882 | 0.0044 |
| 12 | 1.000 | 0.0704 | 0.9995 | 0.0176 | 0.992 | 0.0044 |
| 20 | 1.000 | 0.0704 | 1.000 | 0.0176 | 1.000 | 0.0044 |

SWAP P_zero sits at the zero-signal central-binomial value `C(2M,M)/4^M ≈ 1/√(πM)` (0.0704, 0.0176, 0.0044) for every
n ≥ 6. At A = 1e-12 the exact SWAP P_zero equals the central binomial to ≤ 7.8e-10 relative for M ≤ 10⁵. Loschmidt
P_zero → 1 (0.9999 at A = 1e-8, M = 10⁴). **This contrast is already known at the fidelity level. It is reproduced
here for the gradient estimator.**

## 9. Directional correctness
Median over θ:

| n | M | LE P_correct | SWAP P_correct | LE P(correct \| ĝ≠0) | SWAP P(correct \| ĝ≠0) |
|---|---|---|---|---|---|
| 4 | 1024 | 0.999 | 0.622 | 0.9998 | 0.632 |
| 6 | 1024 | 0.610 | 0.500 | 0.962 | 0.509 |
| 8 | 1024 | 0.099 | 0.492 | 0.905 | 0.501 |
| 10 | 1024 | 0.0064 | 0.491 | 0.875 | 0.500 |
| 12 | 16384 | 0.0067 | 0.498 | 0.881 | 0.500 |
| 20 | 16384 | 9e-8 | 0.498 | 0.854 | 0.500 |

**Loschmidt: a non-zero estimate keeps the sign.** In the deep plateau (M·A → 0), a non-zero estimate is
almost always a single count. It came from the F₋ circuit with probability F₋/(F₊ + F₋) = (1 + s)/2, so

    P(correct | ĝ_LE ≠ 0) → (1 + |s|)/2      independent of A, M and n.

The theory table confirms this: 0.750–0.796 at s = ½ for A from 1e-2 to 1e-6, reaching 0.7505 once P_zero ≥ 0.99.
Over θ ~ U[−π, π] the median of |sin θ| is 1/√2, so the predicted median is (1 + 1/√2)/2 = 0.8536. **Observed at n = 20:
0.8533–0.8537 for every M.**

**SWAP: the sign is a coin flip.** Median P(correct | ĝ ≠ 0) = 0.500 for n ≥ 10 at every tested M.

The continuity-corrected normal approximation Φ((M d − ½)/√(M v)) matches exact SWAP P_correct to ≤ 1.3e-3 at M = 16, and
to ≤ 7e-5 once M ≥ 256. Plain Φ(SNR) is off by up to 0.070 because it ignores the tie mass.

## 10. SNR (paired)
Median log₁₀(SNR_SWAP/SNR_LE) at identical θ and M: −0.44 (n=2), −0.91 (4), −1.50 (6), −2.09 (8), −2.71 (10), −3.30 (12),
−3.92 (14), −4.50 (16), −5.11 (18), −5.73 (20). About −0.30 per qubit, i.e. SNR² ratio ≈ A/2 ≈ 4^{−n}.

## 11. Typical initialization scaling
`E[log A] = −2(n−1) log 2` (empirical means match, `scaling_summary.csv`), so the log-typical A is 4^{−(n−1)}. This is not
`E[A] = 2^{−(n−1)}`. The predeclared log-typical references were M_LE ∝ 1/(A s²) ≈ 4ⁿ and M_SWAP ∝ 1/(A² s²) ≈ 16ⁿ.

## 12. Required-shot complexity (`scaling_summary.csv`, `scaling_fits.json`)
100 000 θ per n, n = 2…20, k = 0, the same θ for both schemes. Median log₁₀ M:

| n | LE SNR≥1 | SWAP SNR≥1 | LE P_c≥0.75 | SWAP P_c≥0.75 | LE P_c≥0.90 | SWAP P_c≥0.90 | LE P_nz≥0.9 | SWAP P_nz≥0.9 |
|---|---|---|---|---|---|---|---|---|
| 2 | 0.78 | 1.54 | 0.85 | 1.38 | 1.11 | 1.82 | 1.00 | 1.30 |
| 4 | 2.08 | 3.91 | 2.07 | 3.58 | 2.39 | 4.13 | 2.13 | 1.51 |
| 6 | 3.30 | 6.32 | 3.29 | 5.98 | 3.62 | 6.53 | 3.34 | 1.51 |
| 8 | 4.49 | 8.69 | 4.48 | 8.35 | 4.81 | 8.91 | 4.53 | 1.51 |
| 10 | 5.70 | 11.11 | 5.69 | 10.77 | 6.01 | 11.32 | 5.73 | 1.51 |
| 12 | 6.90 | 13.52 | 6.90 | 13.17 | 7.22 | 13.73 | 6.94 | 1.51 |
| 16 | 9.32 | 18.34 | 9.32 | 18.00 | 9.64 | 18.56 | 9.35 | 1.51 |
| 20 | 11.72 | 23.14 | 11.71 | 22.80 | 12.04 | 23.36 | 11.75 | 1.51 |

IQR and q90 for every cell are in `scaling_summary.csv` (heavy upper tails for both schemes: see §12.2).

### 12.1 Scaling fits (median log₁₀ M = a + b n, 10 points, slopes not forced)

| scheme | target | slope b | reference | \|b − ref\| | R² | max residual |
|---|---|---|---|---|---|---|
| LE | SNR ≥ 1 | 0.6059 | log₁₀4 = 0.6021 | 0.004 | 0.99994 | 0.064 |
| LE | SNR ≥ 2 | 0.6070 | 0.6021 | 0.005 | 0.99990 | 0.088 |
| LE | P_c ≥ 0.75 | 0.6038 | 0.6021 | 0.002 | 0.99999 | 0.016 |
| LE | P_c ≥ 0.90 | 0.6054 | 0.6021 | 0.003 | 0.99996 | 0.051 |
| LE | P_nz ≥ 0.9 | 0.6001 | 0.6021 | 0.002 | 0.99996 | 0.051 |
| SWAP | SNR ≥ 1 | 1.2025 | log₁₀16 = 1.2041 | 0.002 | 0.99999 | 0.042 |
| SWAP | SNR ≥ 2 | 1.2026 | 1.2041 | 0.002 | 0.99999 | 0.042 |
| SWAP | P_c ≥ 0.75 | 1.1973 | 1.2041 | 0.007 | 0.99992 | 0.149 |
| SWAP | P_c ≥ 0.90 | 1.2008 | 1.2041 | 0.003 | 0.99998 | 0.075 |
| SWAP | P_nz ≥ 0.9 | 0.0056 | none (≈ M-only) | — | 0.27 | 0.13 |

Restricted to n ≥ 8, the slopes are LE 0.6031–0.6037 and SWAP 1.2060. **On the identical landscape, a SWAP-test
gradient needs ≈ 16ⁿ shots against ≈ 4ⁿ for the Loschmidt gradient.** SWAP's "non-zero estimate" requirement is flat at
32 shots (10^1.505), because the central-binomial tie probability depends only on M.

### 12.2 Methods and their measured error
- **SNR:** closed form in log space, integer ceiling, for both schemes.
- **Loschmidt direction:** exact integer bisection of the exact P_correct for 99.2–99.6% of θ. The remaining 0.4–0.8%
  (|s| tiny, M·A > 10⁴) use the Skellam/normal limit, validated against exact in Stage 6 (≤ 0.004 decades for n ≥ 12).
- **SWAP direction:** exact integer bisection wherever the normal estimate is ≤ 10⁴ shots. That is 90% (n = 2), 56% (4), 26% (6),
  9% (8) and 0% (n = 20) of θ. Beyond that, the closed-form continuity-corrected normal inversion is used. At the handover
  (10^3.4–10^5.6 shots) it matches exact integer inversion to ≤ 1.3e-4 decades.
- **Non-zero targets:** exact for both schemes.
- Every row converged. The inversion test checks that M reaches the target and M − 1 does not.

## 13. Same-θ paired comparison
There is no matched-gradient device, because the exact gradient is identical by construction and checked programmatically (§7).
**Every difference below comes from the measurement statistics.** Paired median log₁₀(M_SWAP/M_LE) at identical θ:

| n | SNR≥1 | P_c≥0.75 | P_c≥0.90 | P_nz≥0.9 |
|---|---|---|---|---|
| 2 | 0.71 | 0.52 | 0.64 | 0.30 |
| 6 | 2.99 | 2.66 | 2.89 | −1.83 |
| 10 | 5.40 | 5.07 | 5.30 | −4.23 |
| 12 | 6.60 | 6.27 | 6.50 | −5.44 |
| 16 | 9.02 | 8.68 | 8.91 | −7.85 |
| 20 | 11.42 | 11.08 | 11.31 | −10.25 |

For every SNR and sign target, SWAP needs more shots on **100%** of θ at every n. For "non-zero estimate", SWAP needs
fewer on 72.8% of θ at n = 4, on ≥ 99.99% for n ≥ 14 and on 100% for n ≥ 18. The paired SNR and probability differences are in §8–10.

## 14. Full-gradient reliability (`vector_reliability.csv`; 400 θ × 25 repetitions, same θ for both schemes)

| n | M | LE P(ĝ=0) | LE median cos (all / nonzero) | LE P(ĝ·g>0) | SWAP P(ĝ=0) | SWAP median cos | SWAP P(ĝ·g>0) | SWAP median log₁₀‖ĝ‖/‖g‖ |
|---|---|---|---|---|---|---|---|---|
| 6 | 1024 | 0.140 | 0.96 / 0.98 | 0.76 | 0 | 0.24 | 0.66 | 1.19 |
| 8 | 1024 | 0.308 | 0.67 / 0.90 | 0.60 | 0 | 0.079 | 0.58 | 2.11 |
| 10 | 1024 | 0.553 | 0 / 0.82 | 0.36 | 0 | 0.026 | 0.53 | 3.36 |
| 12 | 64 | 0.899 | 0 / 0.51 | 0.083 | 0 | 0.006 | 0.51 | 5.16 |
| 12 | 1024 | 0.735 | 0 / 0.74 | 0.22 | 0 | 0.009 | 0.51 | 4.55 |

- **Loschmidt:** often there is no vector at all (91% of components exactly zero at n = 12, M = 1024). When a vector exists
  it is well aligned (median cos 0.74), and its norm is the right size (median log₁₀ norm ratio 0.33).
- **SWAP:** there is always a vector. Its norm is 10^4.5 times ‖g‖, so it is almost entirely noise. Its direction is
  uncorrelated with g (median cos 0.009), and it is a descent direction 51% of the time.

## 15. Information-distance view (`information_distance.csv`)
Per-shot distances between the + and − shifted single-shot distributions, median log₁₀ over 20 000 θ:

| n | LE TV | SWAP TV | LE H² | SWAP H² | LE KL | SWAP KL |
|---|---|---|---|---|---|---|
| 4 | −1.81 | −2.12 | −2.61 | −4.53 | −1.99 | −3.93 |
| 10 | −5.39 | −5.69 | −6.19 | −11.68 | −5.56 | −11.08 |
| 20 | −11.36 | −11.66 | −12.17 | −23.62 | −11.55 | −23.02 |

**Total variation cannot tell the schemes apart.** SWAP's TV is exactly half of Loschmidt's (δ = A s/2 vs A s). The
squared Hellinger distance, whose inverse sets the sample complexity of telling the two shifted distributions apart, does:
- Loschmidt: p ≈ 0, so H² ≈ (√F₋ − √F₊)² ∝ A ≈ 4^{−n}.
- SWAP: p ≈ ½, so H² ≈ δ²/(8 p(1−p)) ∝ A² ≈ 16^{−n}.

Hellinger reproduces the two fitted shot exponents (−0.60 and −1.20 decades per qubit), and the Bhattacharyya distance
agrees. This is a concrete two-Bernoulli specialization consistent with the outcome-distribution view of Aghaei Saem et al.
**It is not a new theorem.**

## 16. PennyLane validation (`pennylane_validation.csv`)
Explicit circuits for n ∈ {2, 3, 4}, M ∈ {32, 128, 512}, 3 θ each (lower-quartile / median / upper-quartile |g|),
300 repetitions per shifted circuit, 27 cells per scheme.
- **Loschmidt:** computational-basis samples; a shot succeeds iff all bits are 0.
- **SWAP:** H on the ancilla, n CSWAPs between |ψ(θ)⟩ and a |0ⁿ⟩ register, H, then sample ancilla Z (2n + 1 qubits).
  The analytic ancilla ⟨Z⟩ equals F to 2.2e-16.

| check | Loschmidt | SWAP |
|---|---|---|
| F̂ mean vs F, z (max / sd) | 3.16 / 1.05 | 2.08 / 0.89 |
| F̂ variance ratio | 0.877–1.143 | 0.892–1.151 |
| ĝ mean vs exact g, z (max / sd) | 2.95 / 1.08 | 3.14 / 1.10 |
| ĝ mean vs direct binomial, max \|z\| | 3.27 | 2.01 |
| ĝ variance ratio (mean) | 0.889–1.112 (1.008) | 0.829–1.142 (0.994) |
| P_zero in Wilson CI | 27/27 | 25/27 |
| P_correct in Wilson CI | 27/27 | 24/27 |

Max |z| ≈ 3 over 54 cells is consistent with chance (z SD ≈ 1). Every estimate lies on its lattice (j/(2M) and j/M).

## 17. Same-landscape optimization diagnostic (`optimization_summary.csv`, `optimization_curves.csv`)
This is a diagnostic, not an optimizer study.
- **Setup:** θ ← θ − η ĝ with η = 0.3, **predeclared, not tuned**. It is the finite-shot learning rate selected by the
  Stage 4 protocol on this same benchmark, used unchanged for every variant including exact GD. 50 seeds and 500 iterations
  per n ∈ {6, 8, 10, 12}. Every variant starts from the **same θ₀ per seed** (checked in tests).
- **Budgets:**
  - *Equal shots:* LE and SWAP at the same M. This is also equal total sample count, since both use 2M shots per component per step.
  - *Equal state-copy budget:* SWAP at M/2, because each SWAP shot consumes two state registers.
  - *Random-walk control:* SWAP counts with the signal removed (q₊ = q₋ = ½).

| n | variant | median F_final | P(F_final ≥ 0.5) | wrong-direction steps | zero steps | F_final vs exact, paired (better / worse) | median log₁₀ F_best gain |
|---|---|---|---|---|---|---|---|
| 6 | exact | 1.000 | 0.60 | 0 | 0 | — | 1.76 |
| 6 | LE M=64 | 0.998 | 0.58 | 0.146 | 0.296 | 0.26 / 0.72 | 1.87 |
| 6 | SWAP M=64 | 0.994 | 0.54 | 0.367 | 0 | 0.26 / 0.74 | 2.11 |
| 6 | SWAP random walk M=64 | 6.1e-4 | 0.00 | 0.505 | 0 | 0.24 / 0.76 | 0.98 |
| 10 | exact | 2.6e-6 | 0.08 | 0 | 0 | — | 0.03 |
| 10 | LE M=64 | 2.6e-6 | 0.06 | 0.031 | 0.857 | 0.32 / 0.46 | 0.04 |
| 10 | SWAP M=64 | 1.3e-6 | 0.06 | 0.485 | 0 | 0.50 / 0.50 | 1.66 |
| 10 | SWAP random walk M=64 | 3.5e-6 | 0.00 | 0.498 | 0 | 0.54 / 0.44 | 1.27 |
| 12 | exact | 1.07e-7 | 0.00 | 0 | 0 | — | 0.002 |
| 12 | LE M=1024 | 1.06e-7 | 0.00 | 0.039 | 0.777 | 0.32 / 0.14 | 0.002 |
| 12 | SWAP M=1024 | 1.18e-7 | 0.02 | 0.493 | 0 | 0.46 / 0.34 | 0.51 |
| 12 | SWAP random walk M=1024 | 1.18e-7 | 0.00 | 0.500 | 0 | 0.34 / 0.48 | 0.47 |

(All variants, including M = 1024 and the state-copy-matched rows, are in the CSV.)
- **n = 6 (resolvable):** both schemes track exact GD (P(F_final ≥ 0.5) 0.54–0.64 vs 0.60), while the random walk reaches it
  in 0% of runs. The SWAP state-copy-matched runs (M/2) are no worse than equal-shot SWAP.
- **n ≥ 10 (deep):**
  - Loschmidt GD is **frozen**. 58–94% of steps are exactly zero, and F barely moves (median gain ≤ 0.04 decades), as with exact GD.
  - SWAP GD **moves but is a random walk**. Wrong-direction steps run 48–50%, and the mean cosine is 0.01. The paired F_final
    comparison with exact GD is a coin flip (0.50 / 0.50), and its F_best gain matches the signal-free random-walk control
    (10^1.66 vs 10^1.27 at M = 64; 10^0.51 vs 10^0.47 at n = 12, M = 1024).
- **F_best is misleading.** It is a running maximum, which any random walk inflates. SWAP "beats" exact GD on F_best in
  80–92% of paired seeds at n ≥ 10, and so does the random-walk control. **F_final is the fair endpoint.** On it, neither
  scheme gains anything over exact GD. At n = 10, P(F_final ≥ 0.5) is 0.08 for exact GD, 0.06–0.08 for LE and 0.04–0.14
  for SWAP (50 seeds; the Wilson CIs overlap), against 0 for the random walk. At n = 12 every variant is at or below 0.04.

## 18. Replication of known prior-work behaviour (`prior_work_replication.csv`) — REPLICATIONS, not findings
At the level of the fidelity estimate itself, M = 1024, median over 20 000 θ:

| n | median F | LE P(F̂ = 0) | fraction of θ with LE P(F̂=0) ≥ 0.9 | SWAP \|E F̂\|/sd | SWAP TV to the F = 0 distribution (exact) |
|---|---|---|---|---|---|
| 4 | 8.7e-3 | 1.3e-4 | 0.15 | 0.28 | 0.105 |
| 8 | 3.1e-5 | 0.969 | 0.60 | 9.9e-4 | 5.4e-4 |
| 12 | 1.2e-7 | 0.9999 | 0.90 | 3.8e-6 | 7.3e-7 |
| 20 | 1.9e-12 | 1.000 | 0.999 | 6.0e-11 | 2.3e-11 |

1. The Loschmidt estimate returns F̂ = 0 most of the time (Thanasilp et al. 2024; Aghaei Saem et al. 2026). ✔ replicated.
2. The SWAP estimate approaches a parameter-independent distribution centred on zero fidelity: ancilla outcomes ≈ 50/50,
   and the exact TV distance to the F = 0 null distribution → 0 (normal-limit TV agrees to 3 digits). ✔ replicated.

Trajectory level (§17): SWAP-estimated GD at n ≥ 10 is statistically indistinguishable from a signal-free random walk under
polynomial shots. This matches the random-walk statement of Aghaei Saem et al. (made there for a global-Pauli example).
✔ replicated in this fidelity setting.

## 19. Prior work and what Stage 7 adds
**Thanasilp et al. (2024)** already show, for exponentially concentrated fidelity quantum kernels, that Loschmidt-echo
estimates collapse toward zero and that SWAP-test estimates become effectively random / data-independent under polynomial
shot budgets.

**Aghaei Saem et al. (2026)** already show:
- outcome-probability concentration is the correct measurement-level object;
- different POVMs for the same quantity can have different estimator variances and statistical behaviour;
- Loschmidt and SWAP give different fixed distributions for the same fidelity (rare-event vs ≈ 50/50);
- global-Pauli parameter-shift optimization with polynomial measurement resources can be statistically
  indistinguishable from a random walk.

**We therefore do not claim any of these.** Stage 7 focuses more narrowly on:
- the finite-shot *parameter-shift gradient* distributions under both schemes on one landscape;
- exact zero/sign probabilities, including the deep-limit conditional sign law P(correct | ĝ_LE ≠ 0) → (1 + |s|)/2;
- same-landscape gradient shot complexity (≈ 4ⁿ vs ≈ 16ⁿ, with measured exponents);
- full gradient-vector reliability;
- trajectory consequences with paired starts and a random-walk control.

We have not checked those papers line by line for an equivalent gradient-level statement. No quotations or page numbers
are given, because none were verified.

## 20. Candidate additive results (predeclared A–F; none claimed novel)
- **A.** Exact gradient mass at zero: LE → 1; SWAP → C(2M,M)/4^M, independent of n. Shown (§8).
- **B.** Exact sign probabilities: LE P_correct → 0 through zeros; SWAP → (1 − P_zero)/2. Shown (§9).
- **C.** Conditional LE sign quality: P(correct | ĝ ≠ 0) → (1 + |s|)/2, median over θ (1 + 1/√2)/2 = 0.854. Derived and
  matched to 4 digits (§9).
- **D.** Measurement-dependent shot exponent on an identical landscape: slope 0.60 (LE) vs 1.20 (SWAP) decades per
  qubit, for SNR and sign targets alike (§12). Explained by the SNR ratio ≈ A/2 and the Hellinger scaling A vs A² (§10, §15).
- **E.** Vector level: LE gives "no vector, or an aligned one"; SWAP gives "a vector of norm 10^4.5·‖g‖ with cos ≈ 0" (§14).
- **F.** Trajectories: LE frozen, SWAP a random walk (control-matched), at n ≥ 10. Both track exact GD at n = 6 (§17).

## 21. Outcome classification (Task 23)
**CASE C, which contains CASE A.**
- **A holds.** LE shows count starvation (P_zero → 1). SWAP shows low P_zero (1/√(πM)) with directional ambiguity (P_correct → ½).
  Both need exponential budgets. The Stage 6 mechanism distinction **survives removal of the landscape confound**, so it is
  a property of the measurement, not of cost geometry.
- **C also holds, so this is not B.** The two schemes do *not* share an exponent. SWAP's median required shots grow as
  ≈ 16ⁿ (slope 1.197–1.203) against ≈ 4ⁿ (0.600–0.607) for LE, for every SNR and sign target. On 100% of paired θ SWAP
  needs more.
- **Not D.** The differences do not disappear once the landscape is matched.
- **A result that revises Stage 6:** Stage 6 found both benchmarks at ≈ 4ⁿ and concluded that the failure mode differs but
  the cost doesn't. Stage 7 shows that the readout alone can change the exponent. The equal exponents in Stage 6 held
  because the parity landscape's larger gradient offset its ½-centred noise; they were not a universal property.

## 22. Novelty status
**UNCONFIRMED.** The zero-vs-random distinction and the random-walk behaviour are prior work (§19). A–F are
gradient-level specializations. In particular D (the same-landscape 16ⁿ vs 4ⁿ gradient exponent) and C (the conditional
sign law) could already be stated or implied in Thanasilp et al. 2024 or Aghaei Saem et al. 2026. D follows directly from
the per-shot variances, which those works discuss. A line-by-line check of both papers is required before any claim.

## 23. Resource accounting (Task 16)
Shot count is not physical cost.
- **Loschmidt:** target |0ⁿ⟩, so the overlap is read directly in the computational basis. One variational-state
  preparation per shot, n qubits.
- **SWAP:** an ancilla plus two n-qubit registers (variational state and target) per shot, i.e. 2n + 1 qubits, n
  controlled-SWAPs and two state preparations per shot.

`resource_accounting()` records measurement shots and an abstract state-copy count (SWAP = 2× LE at equal shots).
Stage 7 compares **statistical** sample complexity only. It makes no hardware-cost or gate-count claim. (The SWAP
disadvantage is already 16ⁿ vs 4ⁿ in shots; the state-copy factor of 2 is a constant on top.)

## 24. Limitations
- One circuit family (product RX), one target (|0ⁿ⟩, where the Loschmidt readout is a single computational-basis outcome),
  one initialization distribution, and k = 0 for the scaling statistics.
- Independent batches per (k, ±). No shared-sample estimators, destructive-SWAP / Bell-basis variants, or hardware noise.
- SWAP required shots beyond 10⁴ come from the continuity-corrected normal inversion (error ≤ 1.3e-4 decades at the handover).
- At large n, fixed-M SWAP P_correct is float-limited for 0.005–11% of θ (true value within about 1e-7 of the reported one).
- The optimization diagnostic uses 50 seeds, 500 iterations and one untuned η.
- Novelty unconfirmed (§22).

## 25. Recommended Stage 8
1. **Line-by-line literature check** of Thanasilp et al. 2024 and Aghaei Saem et al. 2026 for C and D, before any write-up.
2. **Other readouts of the same fidelity:** destructive SWAP / Bell-basis measurement and shadow-based estimators, to see
   whether the exponent is set by where the outcome probabilities sit (≈ 0 vs ≈ ½), as §15 suggests.
3. **Shared-sample (correlated) parameter-shift estimators**, which change off-diagonal covariance and possibly which failure mode dominates.

## Validation summary (engineering)
- `pytest -W error::DeprecationWarning`: **180 passed** (166 Stage 1–6 + 14 Stage 7 test functions covering spec items 1–18).
- Identities ≤ 8.6e-11. Exact enumeration: bias ≤ 1.3e-16, variance ≤ 2e-15 relative. Difference distribution vs brute
  force 3.4e-14. Deep-limit SWAP P_zero vs the central binomial ≤ 7.8e-10. Common-gradient identity ≤ 1.7e-16 for n = 2…20.
- Stage 3–6 code unmodified.

## Re-run
```
.venv/bin/python -m pytest -v -W error::DeprecationWarning
.venv/bin/python -m qlo.experiments.stage7 --workers 5     # -> results/stage7/, ~15–20 min on 5 cores, ≤ 2.4 GB peak
.venv/bin/python -m qlo.experiments.stage7 --fast          # smoke run
```
`--workers` changes wall time only. Every per-n solve is seeded by (n, seed).
