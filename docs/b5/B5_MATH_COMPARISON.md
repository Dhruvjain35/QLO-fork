# B5 mathematical comparison: Stage 7 formulas vs the two prior papers

Purpose: place every Stage 7 formula beside what Thanasilp et al. 2024 (paper **A**) and Aghaei Saem et al. 2026
(paper **B**, reviewed as arXiv:2507.22054v2) explicitly contain. §8, added in the follow-up audit, does the same for
Teo 2023 (paper **D**, reviewed as arXiv:2206.12643v3; evidence ids D-xx). §9, added in the closure audit, places the
principal track's shot-ratio identity beside Mari 2021 (**F**), Miranskyy 2025 (**G**) and Zhan et al. 2025 (**H**).

**This document does not decide novelty.** For each Stage 7 expression it records one of:
- **exact prior-work match located**;
- **related formula located**;
- **no explicit formula located**.

Algebra that connects a prior formula to a Stage 7 formula is collected separately in §6, *Derived implications of
prior work*. That algebra is ours: neither source performs it. It carries no novelty label of any kind.

Notation (Stage 3–7, frozen): |ψ(θ)⟩ = ⊗_j RX(θ_j)|0ⁿ⟩, θ_j ~ U[−π, π], F = ∏_j cos²(θ_j/2), C = 1 − F. For component k:
- A = ∏_{j≠k} cos²(θ_j/2), s = sin θ_k;
- F± = F(θ ± (π/2)e_k) = A(1 ∓ s)/2;
- g = ∂C/∂θ_k = As/2;
- M shots per shifted circuit, one independent batch per (k, ±).

Evidence ids (A-xx, B-xx) refer to [`B5_EVIDENCE_LEDGER.md`](B5_EVIDENCE_LEDGER.md). † = present only in arXiv v2 of
paper B (absent from v1; published-version status unverified).

## 1. Landscape quantities

| Stage 7 expression | Status in A | Status in B |
|---|---|---|
| F = ∏ cos²(θ_j/2) concentrates over θ ~ U[−π, π]ⁿ | **Exact match (distributional)**: Prop. 3 / SI Eqs. (207)–(216). Fidelity of product single-qubit rotations with uniform angles, Var ≤ E[κ²] = (3/8)ⁿ, E[κ] = 2^(−n) (A-03). Stated for a kernel κ(x, x′) with y-axis rotations; the per-factor law equals Stage 7's x-rotation factor (our observation; it would not hold for z-rotations). | Related: same circuit used with global-Z costs (B-08c). Fidelity concentration stated only for a 2-design (B-09a†). |
| Log-typical scale A_typ = 4^(−(n−1)) (E log cos²(θ/2) = −2 log 2, Stage 5 Prop. 5) | No explicit formula located (A uses the mean 2^(−n) and second moment only). | No explicit formula located. |
| F± = A(1 ∓ s)/2, g = As/2 (shifted fidelities, exact gradient) | No explicit formula located (no parameter shift in A). | No explicit formula located (generic shift rule Eq. (6) only; B-01). |

## 2. Loschmidt (projector) readout

| # | Stage 7 expression | Status in A | Status in B |
|---|---|---|---|
| 2.1 | One shot ~ Bernoulli(F); F̂ = K/M | **Exact match located (fidelity level)**: main Eq. (12) + LE paragraph p. 4; SI Eq. (17) (A-05, A-08b). | **Exact match located (fidelity level)**: POVM {\|0⟩⟨0\|^⊗n, 𝟙 − \|0⟩⟨0\|^⊗n}, Fig. 5a (B-09a†). |
| 2.2 | P(F̂ = 0) = (1 − F)^M | **Exact match located**: (1 − s)^N inside SI Eqs. (26)–(27); (1 − μ)^N ≈ 1 − Nμ on p. 4 (A-05, A-06a). | Related: fixed distribution (0, 1) ⇒ estimate zero w.h.p. (B-09a†). No formula. |
| 2.3 | Var(F̂_LE) = F(1 − F)/M | Related: follows in one line from the stated outcome model; not written (A-08b). | **Exact match located (per shot)**: Var^(LE) = F(1 − F), §IV p. 10 (B-10a†). |
| 2.4 | ĝ_LE = (Ĉ₊ − Ĉ₋)/2 = (K₋ − K₊)/(2M) | No explicit formula located. | Related: generic finite-shot parameter-shift update, Eq. (6) (B-01). The Loschmidt gradient estimator is not written. |
| 2.5 | Var(ĝ_LE) = [F₊(1 − F₊) + F₋(1 − F₋)]/(4M) = [A − A²(1+s²)/2]/(4M) | No explicit formula located. | **Fidelity-estimator variance located, gradient-estimator variance not located** (B-10a†). Algebra: §6.2. |
| 2.6 | SNR²_LE = MAs²/[1 − A(1+s²)/2] | No explicit formula located. | No explicit formula located. |
| 2.7 | P(ĝ_LE = 0) = Σ_r Bin(r; M, F₊) Bin(r; M, F₋) (≥ (1 − F₊)^M(1 − F₋)^M) | Related: single-estimate (1 − s)^N only (A-06b). | Related: fidelity-level zero w.h.p. only (B-09b†). |
| 2.8 | P_correct, P_wrong (exact difference of binomials); P_correct → 0 through zeros | No explicit formula located. | No explicit formula located. Indistinguishability results are related (B-06c), but they concern the Pauli/±1 case. |
| 2.9 | P(correct \| ĝ_LE ≠ 0) → (1 + \|s\|)/2 as M·A → 0; population median (1 + 1/√2)/2 | No explicit formula located (A-NL13). | No explicit formula located (B-NL13). No prior formula from which it follows was located. Stage 7 §9 derives it from the single-count argument F₋/(F₊ + F₋) = (1 + s)/2. |
| 2.10 | Required shots: M_SNR ≈ ρ²/(As²), median ∝ 4ⁿ; fitted slopes 0.600–0.607 decades/qubit | Related: kernel-level numerics, "N ∈ Ω(2ⁿ)" for a fixed non-zero fraction (SI Fig. 4a; A-10b). | Related, implied only: Eq. (12) + Var^(LE) (B-10c†). Algebra: §6.3. |

## 3. SWAP-test readout

| # | Stage 7 expression | Status in A | Status in B |
|---|---|---|---|
| 3.1 | One shot: ancilla +1 w.p. q = (1 + F)/2; F̂ = 2K/M − 1 | **Exact match located (fidelity level)**: p₊ = 1/2 + κ/2, main p. 4; SI Eq. (46) (A-08). | **Exact match located (fidelity level)**: ancilla POVM {\|0⟩⟨0\|, \|1⟩⟨1\|}, Fig. 5b (B-09a†). |
| 3.2 | q± = (1 + F±)/2 | No explicit formula located (no shifts). | No explicit formula located. |
| 3.3 | Var(F̂_SWAP) = (1 − F²)/M | Related: follows from the stated outcome model; not written (A-08b). | **Exact match located (per shot)**: Var^(SWAP) = 1 − F², §IV p. 10 (B-10a†). |
| 3.4 | ĝ_SWAP = (Ĉ₊ − Ĉ₋)/2 = (K₋ − K₊)/M | No explicit formula located. | Related: Eq. (B18) writes the Pauli (±1-outcome) parameter-shift update as a difference of two ±1 means. Same structure with ℓ = F (B-06b). |
| 3.5 | Var(ĝ_SWAP) = [2 − F₊² − F₋²]/(4M) = [2 − A²(1+s²)/2]/(4M) | No explicit formula located. | **Fidelity-estimator variance located, gradient-estimator variance not located** (B-10a†). Algebra: §6.2. |
| 3.6 | SNR²_SWAP = MA²s²/[2 − A²(1+s²)/2] | No explicit formula located. | No explicit formula located. |
| 3.7 | P(ĝ_SWAP = 0) → C(2M, M)/4^M ≈ 1/√(πM) (n-independent) | Related: null estimate κ̂^(rand) = mean of ±1 equiprobable outcomes (Eq. 14; A-08). Tie probability not computed. | Related: null outcomes z = ±1 equiprobable (B15, B19, B26; B-06b). Tie probability not computed. Algebra: §6.5. |
| 3.8 | P_correct → (1 − P_zero)/2 (coin-flip sign) | No explicit formula located. | Related: indistinguishable from a sign-symmetric null (B-06c). No formula. |
| 3.9 | Required shots: M_SNR ≈ 2ρ²/(A²s²), median ∝ 16ⁿ; fitted slopes 1.197–1.203 decades/qubit | Related: kernel-level numerics, "at least exponentially" (SI Fig. 4b; A-10b). | Related, implied only (B-10c†). Algebra: §6.3. |

## 4. Paired (same-θ) readout comparison

| Stage 7 expression | Status in A | Status in B |
|---|---|---|
| SNR²_SWAP / SNR²_LE = A(1 − A(1+s²)/2)/(2 − A²(1+s²)/2) → A/2 | No explicit formula located. | No explicit formula located (implied by B-10a† after §6.2). |
| Exponent gap ≈ log₁₀4 per qubit (0.600–0.607 vs 1.197–1.203) | No explicit formula located (A-NL17). | No explicit formula located (B-NL17). |
| Per-shot TV: A\|s\| (LE) vs A\|s\|/2 (SWAP). Squared Hellinger ∝ A (LE) vs ∝ A² (SWAP) | Related: 1-norm (TV) hypothesis-testing bounds only (A-11). | Related: 1-norm bounds only (B-16). |
| Zero-vs-random failure split survives on an identical landscape | Related: the split is shown for kernels (same kernel, two tests; A-09a, A-10a). | Related: the split is stated for one fidelity objective under a 2-design (B-09a†). |

## 5. Full-vector and trajectory quantities

| Stage 7 expression | Status in A | Status in B |
|---|---|---|
| P(full ĝ = 0) = ∏_k P₀(θ, M, k) (independent batches) | Related: Pr[K̂ = 𝟙] = ∏_{i<j} Pr[κ̂_ij = 0] for an estimated Gram matrix (SI Eqs. 33–36; A-07). | Related: fidelity-level zero only (B-09b†). |
| Median cos(ĝ, g); P(ĝ·g > 0); component sign accuracy | No explicit formula located. | Related: update vector indistinguishable from a parameter-independent random vector (B-06d). No metric computed. |
| ‖ĝ‖/‖g‖ (SWAP ≈ 10^4.5 at n = 12, M = 1024) | No explicit formula located. | Related: null update magnitude is parameter-independent (B15; B-06e). Algebra: §6.6. |
| SWAP-driven GD vs signal-free random walk from identical starts; F_final as endpoint | No explicit formula located (A-NL24); random-matrix model control only (A-09b). | Related/explicit: random-walk reference on displacement statistics, Fig. 3b–c (B-07b); start matching not stated (B-07c). |
| Loschmidt-driven GD "frozen" (58–94% exactly-zero steps at n ≥ 10) | No explicit formula located. | No explicit statement located. Follows from applying Theorem 2 / Corollary 3 to the (0, 1) fixed distribution (§6.7). |

---

## 6. Derived implications of prior work

The algebra below is **ours**. Each step starts from a formula located in a source and states every assumption added.
None of it is stated in either source. It is recorded so that the principal audit can see exactly how far the
located prior formulas reach. It is not a judgment of novelty.

### 6.1 From A's single-estimate zero probability to the r = 0 term of the gradient zero probability

Located (A-06a): P(κ̂ = 0 | κ = s) = (1 − s)^N for one Loschmidt estimate from N shots.

Added assumptions: two shifted fidelities F± estimated with M shots each, independent batches; the parameter-shift
estimate is zero iff the two counts are equal.

Then P(ĝ_LE = 0) = P(K₊ = K₋) = Σ_{r=0}^{M} Bin(r; M, F₊) Bin(r; M, F₋). Its r = 0 term,
(1 − F₊)^M (1 − F₋)^M, is the product of two of A's factors and is a lower bound on P(ĝ = 0). The r ≥ 1 terms
(equal nonzero counts) have no counterpart in A. Stage 5 quantified them: the cruder "both counts zero" form misses
≈ 0.18 of probability at typical |s|, and the Poisson-limit form e^(−MA) I₀(MA|cos θ_k|) includes them.

### 6.2 From B's per-shot variances to Stage 7's gradient-estimator variances

Located (B-10a†): Var^(LE) = F(1 − F), Var^(SWAP) = 1 − F² (one shot, fidelity / infidelity estimate).

Added assumptions: Ĉ± = 1 − F̂± from M shots each; ĝ = (Ĉ₊ − Ĉ₋)/2; independent batches (Stage 7 design); shift
identities F₊ + F₋ = A and F₊² + F₋² = A²(1+s²)/2 (Stage 5 Prop. 1, not in either source).

- Var(ĝ_LE) = [F₊(1 − F₊) + F₋(1 − F₋)]/(4M) = [A − A²(1+s²)/2]/(4M)
- Var(ĝ_SWAP) = [(1 − F₊²) + (1 − F₋²)]/(4M) = [2 − A²(1+s²)/2]/(4M)
- With g = As/2: SNR²_LE = MAs²/[1 − A(1+s²)/2] and SNR²_SWAP = MA²s²/[2 − A²(1+s²)/2]. Their ratio → A/2 as A → 0.

These are Stage 7's §5–§6 expressions. The step from B's formulas is one line plus the landscape identities, which
are not in B.

### 6.3 From B's resolution ratio ε_N to shot exponents — the result depends on the criterion and the ensemble

Located (B-10b†, B-10c†): ε_N(α) = Var_ρ(α)[ℓ̂(α)]/(N Var_α[ℓ(α)]). Resolution needs ε_N ≲ 1, together with the two
per-shot variances. The source computes no exponent.

**(a) The source's own setting (2-design, fidelity level).** For a Haar-random state and fixed target in dimension
d = 2ⁿ:
- F ~ Beta(1, d − 1), so E F = 1/d, Var F = (d − 1)/(d²(d + 1)) ≈ d^(−2), and median F ≈ (ln 2)/d (checked by
  sampling at n = 6, 10).
- Loschmidt: N ≳ F(1 − F)/Var F ≈ d = 2ⁿ at typical F.
- SWAP: N ≳ (1 − F²)/Var F ≈ d² = 4ⁿ.

The SWAP requirement is approximately the square of the Loschmidt one (ratio ≈ 1/F). This is a readout-dependent
exponent **at the fidelity level under a 2-design**, implied by the source's formulas but not stated.

**(b) The same ε_N criterion on Stage 7's product landscape (fidelity level).** Var_θ F = (3/8)ⁿ − 4^(−n) ≈ (3/8)ⁿ
(checked by sampling), log-typical F = 4^(−n).
- Loschmidt: N ≳ F/Var_θ F, which is (2/3)ⁿ at the log-typical F (no exponential budget) or (4/3)ⁿ at the mean F = 2^(−n).
- SWAP: N ≳ 1/Var_θ F = (8/3)ⁿ.

These differ from Stage 7's exponents and depend on which scale of F is inserted. Var_θ F is dominated by rare near-target θ (heavy tail: (3/8)ⁿ ≫ F_typ² =
16^(−n)), so ε_N measures resolution against the landscape-wide spread, not against the local signal. The source calls
ε_N a rule of thumb.

**(c) A per-point signal-to-noise criterion (the criterion Stage 7 uses).**
- Fidelity level: N ≳ Var_1/F², i.e. ≈ 1/F (LE) vs ≈ 1/F² (SWAP).
- Gradient level (§6.2): M ≈ ρ²/(As²) (LE) vs ≈ 2ρ²/(A²s²) (SWAP).
- With the log-typical A = 4^(−(n−1)) (Stage 5 Prop. 5): median log₁₀ M grows by log₁₀4 = 0.602 (LE) and
  log₁₀16 = 1.204 (SWAP) decades per qubit. These are the references for Stage 7's fitted 0.600–0.607 and
  1.197–1.203.

**What is needed beyond the located formulas to reach Stage 7's gradient-level 4ⁿ vs 16ⁿ:**
1. B's per-shot variances (B-10a†).
2. The parameter-shift difference with independent batches.
3. The product-landscape shift identities.
4. A per-θ criterion (SNR ≥ ρ or P_correct ≥ q) instead of B's ε_N.
5. The log-typical value of A (not in A or B).
6. For sign targets, exact difference-of-binomial inversion (Stage 6/7; not located).

Neither source performs steps 2–6, and neither compares the readouts on a same-θ grid.

### 6.4 Why the located 1-norm (total-variation) bounds do not separate the readouts

Located: A's SI Eq. (14) (success ≤ 1/2 + N|ε|/2 for binary distributions; A-11) and B's Eq. (A19) (success ≤ 1/2 +
N‖P₀ − P₀′‖₁/4; B-16). Both tests in the sources compare an outcome distribution with a fixed one.

Our application to the two shifted per-shot distributions:
- TV_LE = |F₋ − F₊| = A|s|
- TV_SWAP = |q₋ − q₊| = A|s|/2

Both are linear in A, so a 1-norm bound of this form gives the same 1/(A|s|) threshold for both readouts. The squared
Hellinger distance, which governs the sample complexity of telling the two apart, scales differently:
- H²_LE ≈ A(√(1+s) − √(1−s))²/4 ∝ A
- H²_SWAP ≈ (As/2)²/2 ∝ A²

This was checked numerically at A = 10^(−4), 10^(−6) and s = 0.5, and it matches Stage 7 §15. The readout dependence
is therefore invisible to the located 1-norm machinery and appears only with a variance- or Hellinger-type criterion.

### 6.5 SWAP null tie probability from the located null distributions

Located: A's κ̂^(rand) = (1/N) Σ λ̃_m and B's z = ±1 means (B19, B26). Each is 2K/N − 1 with K ~ Bin(N, 1/2).

Added assumption: two independent such means, one per shift.

Then P(equal) = Σ_r C(N, r)² 4^(−N) = C(2N, N)/4^N ≈ 1/√(πN) (Vandermonde), independent of n. Checked: 0.017839 at
N = 1000 vs 1/√(1000π) = 0.017841. Stage 6/7's SWAP P_zero plateau. Not computed in either source.

### 6.6 Magnitude of B's null update

Located: B15, [Δ_N]_k = −(η/2) Σ_i c_i (Z̄_ik − Z̄′_ik), with Z̄ means of N equiprobable ±1 values.

Then E[Δ_k] = 0 and E‖Δ_N‖² = (η²/4) · N_p · (2/N) · Σ_i c_i². This is parameter-independent, while the exact step
η‖∇L‖ is exponentially small on a barren plateau, so the ratio of estimated to exact step norms grows as ‖∇L‖ shrinks.
Stage 7's measured SWAP per-component noise sd ≈ 1/√(2M) and median log₁₀ ‖ĝ‖/‖g‖ ≈ 4.5 at n = 12, M = 1024 are the
corresponding Stage 7 quantities. B states no norm comparison.

### 6.7 Loschmidt "frozen" dynamics from B's framework (not stated in B)

Located: B's Theorem 2 / Corollary 3, and the Loschmidt fixed distribution P_fixed = (0, 1) (B-09a†).

Our application: under P_fixed every outcome is "not all-zero", so every fixed-distribution fidelity estimate is
exactly 0 and the corresponding parameter-shift update is exactly zero. The fixed-distribution dynamics is therefore
a stationary point ("frozen"), not the ±1 random walk of B15, which is written for Pauli/±1 outcomes. Stage 7 §17
observed Loschmidt GD frozen (58–94% exactly-zero steps at n ≥ 10). Neither source states this contrast.

### 6.8 A's shot count and its constant-fluctuation assumption

Located (A-12a): A's sufficient shot count N ≥ 2‖O‖²_∞ log(2/p)/(ε̃² Var_α[X]) (SI Supp. Prop. 5) is Hoeffding-based, so
it uses only the outcome range. A's Gram-matrix corollary (SI Eq. 150) additionally assumes that "statistical
fluctuations associated with individual measurement outcomes stay constant". The source frames the count as a
requirement.

Our observation: replacing the range by the actual per-shot variance σ² (CLT/Bernstein-type reasoning) gives
N ≈ σ²/(ε̃² Var_α[X]).
- SWAP (±1 outcomes): σ² = 1 − F² ≈ 1, so the constant-fluctuation assumption holds.
- Loschmidt (0/1 outcomes): σ² = F(1 − F) ≈ F is exponentially small, so the assumption fails and the variance-aware
  count is smaller by the factor F.

This is the same mechanism that separates Stage 7's per-θ requirements (∝ 1/A for Loschmidt vs ∝ 1/A² for SWAP).
A states the assumption but does not connect it to the choice of readout.

## 7. One-line summary per candidate

- **C1 (exact zero/sign probabilities).**
  - Located: fidelity-level zero probability (A, B†) and the ±1 difference structure of the Pauli update (B).
  - Not located: the gradient-level difference-of-binomials pmf, P(ĝ = 0) with equal-count terms, P_correct and
    P_wrong.
- **C2 (conditional Loschmidt sign law).** No formula located in either source, and no located formula implies it.
- **C3 (readout-dependent gradient exponent on one landscape).**
  - Located: per-shot fidelity variances and a resolution ratio (B†), and fidelity-level same-kernel numerics (A).
  - Gradient-level exponents follow only via §6.2–§6.3 with added assumptions; the 4ⁿ vs 16ⁿ pair is not stated.
- **C4 (vector / trajectory consequences).**
  - Located: random-walk indistinguishability and displacement-statistics comparison (B), and a product-form joint
    zero probability for Gram matrices (A).
  - Not located: cosine, norm-ratio, dot-sign and component-sign metrics, and matched-start comparisons with a
    zero-signal control on fidelity endpoints.

## 8. Comparison with Teo 2023

Source: Y. S. Teo, Phys. Rev. A 107, 042421 (2023), **reviewed as arXiv:2206.12643v3**. The APS version was not
inspected (`B5_VERSION_GAP.md` §3). Full audit: [`B5_TEO_DEEP_AUDIT.md`](B5_TEO_DEEP_AUDIT.md). Teo's N_T is the
total number of copies per gradient component per Pauli term; in Stage 7 units **N_T = 2M**. Algebra marked *(ours)* is
not in the source.

### 8.1 Stage 7 quantities beside Teo's estimator and MSE

| Stage 7 quantity | Stage 7 expression | Teo 2023 (arXiv v3) | Status |
|---|---|---|---|
| Estimator | ĝ = (Ĉ₊ − Ĉ₋)/2 at shift π/2, independent batches of M shots | PS = [f(θ+s) − f(θ−s)]/(2 sin s) (Eq. 11, p. 5), with N_T/2 copies per shifted function (p. 4) | Same estimator family (s = π/2; f = F, so ĝ = −PS of F) |
| Var(ĝ_SWAP) | [2 − F₊² − F₋²]/(4M) = [2 − A²(1+s²)/2]/(4M) | Per θ: not written; implied by Eq. (C1) for a ±1 observable: [2 − f₊² − f₋²]/(2N_T) at Teo's shift π/2, which equals the Stage 7 form with f = F± and N_T = 2M *(ours; checked numerically)*. Two-design average: d/(N_T(d+1) sin² s) (Eq. 13) | **PARTIAL / IMPLIED** per θ (D-03b); EXPLICIT as a two-design average (D-02) |
| Var(ĝ_LE) | [F₊(1−F₊) + F₋(1−F₋)]/(4M) = [A − A²(1+s²)/2]/(4M) | No projector (0/1) readout; Pauli ±1 observables only | **Not located** (D-NL02) |
| SNR², required M (SNR ≥ ρ) | LE: M = ρ²[1 − A(1+s²)/2]/(As²); SWAP: M = ρ²[2 − A²(1+s²)/2]/(A²s²) | No SNR. D_θ0 = ⟨max Var[f̂(θ±θ0)]/\|f(θ+θ0) − f(θ−θ0)\|²⟩ (Eq. 26) is a circuit-averaged inverse squared SNR of the shifted difference, with an O(1/N) numerator (±1 case) | Related but different (D-07a/b) |
| P(ĝ = 0) | LE: Σ_r Bin(r;M,F₊)Bin(r;M,F₋); SWAP → C(2M,M)/4^M | None (moments only) | **Not located** (D-NL09) |
| Exact law of ĝ | Difference of two independent binomials | Multinomial moments up to second order only (Eq. C1) | Related but different (D-03a) |
| P_correct, P_wrong | Exact difference-of-binomials sums | Qualitative "many wrong update directions" (§VII, p. 11) | Related but different (D-08a) |
| P(correct \| ĝ_LE ≠ 0) → (1+\|s\|)/2 | Single-count limit | None | **Not located** (D-NL13) |
| Mean-square estimate vs gradient | SWAP ‖ĝ‖/‖g‖ median ≈ 10^4.5 (n = 12, M = 1024) | ⟨E[(PS)²]⟩ → 1/(2d) + 1/N_T (Eq. 18); ratio to ⟨(∂f)²⟩ = 1 + 2d/N_T *(ours)* | Related but different (D-04) |
| Required-shot exponent | Median over θ: ≈ 4ⁿ (LE), ≈ 16ⁿ (SWAP) | N_* ≅ 32(d²−1)/(3d) (Eq. 24): an FD/PS crossover, base 2; D_θ0: "exponentially large", base not given | Related but different (D-06, D-07a); 4ⁿ/16ⁿ not located (D-NL17) |

### 8.2 Can Teo plus added assumptions reproduce SWAP's 16ⁿ? Yes, but only with all of the following

Starting point: Teo's Eq. (C1). The five-part write-out is in `B5_TEO_DEEP_AUDIT.md` §11.
1. **Per-θ use of (C1).** Teo writes only circuit averages (Eq. C2). At fixed θ the ±1 identity gives
   Var[f̂] = (1 − f²)/N.
2. **SWAP readout as the ±1 observable.** The SWAP-test ancilla Z has mean F. Its circuit (2n + 1 qubits, parameters
   still in Pauli rotations) fits Teo's PEPQC form, but not his two-design averages.
3. **Shot convention.** N = M per shifted circuit, N_T = 2M, independent batches.
4. **Product-landscape identities** F₊ + F₋ = A and F₊² + F₋² = A²(1+s²)/2 (Stage 5 Prop. 1). This gives Stage 7's
   Var(ĝ_SWAP) exactly.
5. **Per-θ criterion plus median over θ with the log-typical A.**
   - SNR ≥ ρ gives M ≈ 2ρ²/(A²s²).
   - With A_typ = 4^(−(n−1)) (Stage 5 Prop. 5), the median grows as 16^(n−1) (slope log₁₀16 = 1.204).
   - Sign targets additionally need exact difference-of-binomial inversion, which no moment formula supplies.

**Without step 5 the base differs** (B5_STATISTIC_COMPARISON.md §2):
- Teo's own two-design average with a mean-square criterion gives N_T ≥ 2(d²−1)/d, i.e. M ≈ 2ⁿ.
- Stage 7's landscape with a mean-square criterion gives M = 4(8/3)^(n−1) − 3/2.
- Teo's average-of-ratio D_θ0 diverges on Stage 7's landscape (E_θ[1/A²] = ∞).

So Teo supplies the SWAP-type per-shot variance structure, and the 16ⁿ comes from Stage 7's landscape and statistic.

### 8.3 Can Teo plus added assumptions reproduce Loschmidt's 4ⁿ? Not from Teo's model

- **The readout is outside the model.** Teo's observables are traceless Pauli strings with ±1 eigenvalues, each sampled
  independently. Loschmidt's per-shot outcome is the 0/1 projector |0ⁿ⟩⟨0ⁿ| with variance F(1 − F).
- **Term-by-term sampling gives a SWAP-like estimator.** Under Teo's prescription the projector, a sum of 2ⁿ Z-strings
  with weight 2^(−n), would be estimated from 2ⁿ − 1 independently sampled settings. *(Ours:)* the resulting
  per-total-copy variance is O(1), e.g. ≈ 0.92 at n = 6 for a random θ, against F(1 − F) ≈ 1.5×10⁻³ for the
  single-setting Loschmidt estimate.
- **Shared samples recover Loschmidt exactly.** Measuring all Z-strings on the same computational-basis shots gives
  2^(−n) Σ_S Z_S(b) = 1[b = 0ⁿ], i.e. exactly the Loschmidt estimator. That is a different sampling scheme from Teo's
  (compare Aghaei Saem's measure-first remark, B-12).
- **The ±1 encoding is outside Teo's averaged results.** O′ = 2Π − 1 reproduces Var = F(1 − F) for F̂, but it is
  neither a Pauli string nor traceless, so Teo's averaged results (e.g. ⟨f²⟩ = 1/(d+1)) do not apply. Teo does not
  consider it.
- **Structural reason (ours).**
  - Traceless observables concentrate at the centre of their spectrum under two-design averaging, where the ±1 variance
    is ≈ 1: the SWAP regime.
  - The projector concentrates at the edge of its spectrum (F ≈ 0), where the variance is ≈ F.
  - Teo's "numerator approaches O(1/N)" (p. 11) is the former case.
- **4ⁿ therefore needs the projector variance from another source:** Aghaei Saem's Var^(LE) = F(1 − F) (B-10a) or
  Gentinetta's Bernoulli kernel variance (E-02). It then needs steps 3–5 of §8.2 with M ≈ ρ²/(As²), so the median
  grows as 4^(n−1).

### 8.4 What Teo adds to the comparison

- **Located in Teo:**
  - an analytic, circuit-averaged MSE for finite-copy PS gradients (EXPLICIT; D-02);
  - the statement that PS errors do not shrink with n at fixed copies (D-04);
  - an exponential copy requirement for distinguishing shifted values, D_θ0 (D-07a);
  - a qualitative wrong-direction remark (D-08a).
- **Implied only:** Stage 7's per-θ SWAP variance and its 16ⁿ median, after steps 1–5 (D-03b).
- **Not located:** the Loschmidt variance and 4ⁿ, any readout comparison, exact zero/sign probabilities, the conditional
  sign law and the explicit 4ⁿ/16ⁿ pair (D-NL02, D-NL09, D-NL13, D-NL17).

## 9. Closure-audit sources and the principal track's shot-ratio identity

Added in the closure audit ([`B5_CLOSURE_AUDIT.md`](B5_CLOSURE_AUDIT.md)).
- **Sources:**
  - Mari, Bromley, Killoran 2021 (paper **F**, arXiv:2008.06517v2);
  - Miranskyy 2025 (paper **G**, arXiv:2510.22418v1);
  - Zhan et al. 2025 (paper **H**, Light Sci. Appl. 14, 83).
- **Identity being compared:** the principal track's A2 ratio identity (`principal/QLO_Principal_Track.md` §3),
  R = M_SW/M_LE = [2 − F₊² − F₋²]/[F₊(1 − F₊) + F₋(1 − F₋)] → 2/S.
- Algebra marked *(ours)* is not in any source.

### 9.1 Ingredients of the identity, by source

| Ingredient | Where printed | Status |
|---|---|---|
| Per-θ parameter-shift variance with a separate single-shot variance at each shift, [σ₀²(θ + s) + σ₀²(θ − s)]/(4N sin² s) | Mari Eq. (45), p. 7 (F-01) | EXPLICIT (σ₀² unspecified; F-02) |
| Loschmidt-type per-shot variance F(1 − F) | Aghaei Saem §IV/§4, p. 10 (B-10a); Zhan SI §V, p. 23, v_proj = c(1 − c)/N for projection onto a known state (H-01) | EXPLICIT (fidelity level) |
| SWAP-type per-shot variance 1 − F² | Aghaei Saem p. 10 (B-10a); Zhan Eq. (10), p. 9 (SCM) and SI p. 17 (ideal swap test) (H-01) | EXPLICIT (fidelity level) |
| Outcome models only (variances follow in one line) | Thanasilp p. 4, SI Eqs. (17), (46) (A-19); Miranskyy §3.1, Eq. (10), App. C–D (G-02) | PARTIAL / IMPLIED |
| The ratio for gradients, R | Not printed in A–H | Implied by the variances at the two shifts (A-19, B-18, G-02, H-03) |
| The exponent rule b_SW − b_LE = b_S | Not printed in A–H | Implied only with a concentrated ensemble and median log-slopes (A-19, B-18, G-02, H-03); the accounting structure (shot exponent = variance exponent − signal exponent) is printed in a different setting by Sulimov & Lehmann 2026, Eq. (2) (screened, not added; `B5_CLOSURE_SEARCH.md` §4) |

*(Ours.)* Mari's Eq. (45) at s = π/2, with N = M per shift, gives:
- with σ₀² = F(1 − F): Var(ĝ_LE) = [F₊(1 − F₊) + F₋(1 − F₋)]/(4M);
- with σ₀² = 1 − F²: Var(ĝ_SWAP) = [2 − F₊² − F₋²]/(4M).

Their ratio at equal SNR is R. Mari's own approximation (Assumption 1, Eq. 47) would replace the sum of the two
shifted single-shot variances by 2σ₀²(θ). *(Ours.)* For the Loschmidt readout at small fidelity that sum is ≈ F₊ + F₋ = A
at x = π/2, while 2σ₀²(θ) ≈ A(1 + cos θ_k): the assumption fails by the factor (1 + cos θ_k) and holds only where
cos θ_k ≈ 0. For the SWAP readout both sides are ≈ 2 and it holds. Mari's printed Eq. (49) has a factor-2 typo (2N for
4N; B5_MARI_AUDIT.md §6).

### 9.2 Fidelity-level comparisons: estimation (Zhan) vs detection (Miranskyy)

*(Ours.)* With equal shifted fidelities, or at the fidelity level, the per-shot variance ratio is
(1 − F²)/(F(1 − F)) = (1 + F)/F.
- **Zhan et al. (H-02)** compare estimation precision for one overlap:
  - The swap-type estimators are less precise at small overlap and more precise at large overlap than the
    tomography-based ones.
  - The tomography–projection vs SCM crossover c_t = 4/11 comes from the extra tomography term 2κc(1 − c)/N with
    κ = 11/8: (2κ + 1)c(1 − c) = 1 − c² gives c = 1/(2κ) = 4/11.
  - With a **known** target (no tomography; the Loschmidt setting), the ratio (1 + c)/c ≥ 2 holds for every c < 1, and
    the source calls projection the optimal strategy in that case (SI p. 23).
- **Miranskyy (G-01)** compares **detection** shot counts from the quantum Chernoff bound, N ∝ 1/(−ln Q) with Q = F or
  (1 + F)/2, giving ln F / ln[(1 + F)/2]. The two ratios agree only as F → 1:

| F | Detection ratio ln F / ln[(1 + F)/2] (Miranskyy) | Variance ratio (1 + F)/F (estimation) |
|---|---|---|
| 0.999 | 2.0005 | 2.0010 |
| 0.99 | 2.0050 | 2.0101 |
| 0.9 | 2.0541 | 2.1111 |
| 0.5 | 2.4094 | 3.0000 |
| 0.1 | 3.8515 | 11.000 |
| 0.01 | 6.7406 | 101.00 |

The detection ratio grows like log₂(1/F) and the estimation ratio like 1/F (ours). Miranskyy's factor of two is
therefore specific to near-identity detection. Stage 7's regime (F ≈ 0, estimation) sits in the right-hand column.

This document is evidence for the principal novelty audit. It does not make the novelty decision.
