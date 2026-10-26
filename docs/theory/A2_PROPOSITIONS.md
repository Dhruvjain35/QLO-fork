# Measurement cost of parameter-shift gradients: propositions and proofs

This note turns the principal track's A2 statements (`principal/QLO_Principal_Track.md` §3, item 4 of §6) into
propositions with explicit hypotheses and proofs. It adds the noise corollaries that B4 tests
(`docs/b4/B4_NOISE_OVERLAY.md`).

- §§1–4 restate A2 precisely; they do not change its content.
- §5 identifies the finite-n residual measured in B1.
- §§6–7 (noise) were written and committed **before** the B4 sweep. They serve as B4's predictions.

No novelty claim is made here. Novelty determinations belong to the principal track (A1).

## 0. Setting and notation

- **States.** A trial state ρ(θ) on n qubits. It may be mixed, so noise is allowed. The target is a pure state
  |φ⟩ = V|0ⁿ⟩.
- **Fidelity and cost.** F(θ) = ⟨φ|ρ(θ)|φ⟩, with cost C = 1 − F.
- **Parameter.** θ_k enters through e^{−iθ_k P/2} with P a Pauli string, so the two-term shift rule is exact:
  F± = F(θ ± (π/2) e_k).
- **Derived quantities.**
  - S = F₊ + F₋ and Δ = F₋ − F₊;
  - r = Δ/S for S > 0;
  - the gradient g = ∂C/∂θ_k = Δ/2;
  - Q = F₊² + F₋².
- **Batches.** One independent batch of M shots is taken at each shift.

The two readouts:

- **Loschmidt (LE).** Each shot is Bernoulli(F±): apply V†, then test for 0ⁿ. With F̂ = K/M,
  ĝ_LE = (F̂₋ − F̂₊)/2.
- **SWAP.** Each shot is Z ∈ {±1} with E[Z] = Tr(ρ±|φ⟩⟨φ|) = F±; the target copy is pure. With F̂ = mean Z,
  ĝ_SW = (F̂₋ − F̂₊)/2.
  - The ancilla and destructive (Bell-basis) SWAP tests have identical outcome statistics (B2 §5).

Both estimators are unbiased for g. Required shots are defined by SNR = |g|/√Var ĝ ≥ ρ, using the continuous M.

## 1. Proposition 1 (exact shot-ratio identity)

For every θ with Δ ≠ 0 and S − Q > 0:

    Var ĝ_LE = (S − Q)/(4M),        Var ĝ_SW = (2 − Q)/(4M),
    M_LE = ρ²(S − Q)/Δ²,            M_SW = ρ²(2 − Q)/Δ²,
    R := M_SW / M_LE = (2 − Q)/(S − Q) ≥ 1.

R = 1 only if F₊ = F₋ = 1.

*Proof.*
1. Independent batches give Var ĝ = [v(F₊) + v(F₋)]/(4M), where v is the single-shot variance.
2. For a Bernoulli(F) shot, v = F(1−F), so the sum is S − Q.
3. For a ±1 shot with mean F, v = 1 − F², so the sum is 2 − Q.
4. Solving SNR = ρ gives the two M's.
5. Their ratio cancels ρ and Δ, which gives R.
6. R ≥ 1 because 2 ≥ S. ∎

**Remarks.**
1. Nothing about the circuit, the parameter distribution or purity is used. Only the fact that both readouts
   estimate the same pair F± is needed. Proposition 1 therefore holds under any noise acting on the trial state,
   provided the SWAP target copy is the ideal |φ⟩.
2. B1 checked R against (2−Q)/(S−Q) on 6.74 × 10⁶ θ, with maximum relative error 1.75 × 10⁻¹¹ (B1 §14).

## 2. Proposition 2 (slope rule in the concentrated regime)

**Hypotheses.** Let θ be random and n → ∞. Assume:
- **(H1) Shift family.** log₁₀ S_n = −b_S n + X_n and log₁₀|r_n| = −b_r n + Y_n, where (X_n, Y_n) converges in
  distribution to (X, Y).
- **(H2)** S_n → 0 in probability.
- **(H3)** The limiting variables −X − 2Y and −2X − 2Y have unique medians.

**Conclusion.**

    median log₁₀ M_LE = (b_S + 2b_r) n + c_LE + o(1)
    median log₁₀ M_SW = (2b_S + 2b_r) n + c_SW + o(1)

So the median slopes are b_LE = b_S + 2b_r and b_SW = 2b_S + 2b_r, and **b_SW − b_LE = b_S**.

*Proof.*
1. By Proposition 1, log₁₀ M_LE − 2 log₁₀ρ = −log₁₀ S − 2 log₁₀|r| + log₁₀(1 − Q/S).
2. Since Q ≤ S², we have 0 ≤ Q/S ≤ S. So the last term lies in [log₁₀(1 − S), 0] and tends to 0 in probability
   by (H2).
3. Hence log₁₀ M_LE − (b_S + 2b_r) n = −X_n − 2Y_n + o_p(1), which converges in distribution to −X − 2Y.
4. Under (H3), convergence in distribution implies convergence of the median.
5. The SWAP case is identical. It uses log₁₀ M_SW − 2 log₁₀ρ = log₁₀(2 − Q) − 2 log₁₀ S − 2 log₁₀|r|, and
   log₁₀(2 − Q) → log₁₀ 2. ∎

**Remarks.**
- The intercepts satisfy c_LE = median(−X − 2Y). In general this is **not**
  −median X − 2 median Y, because medians do not add. Under (H1) the slopes are unaffected; only the constants are.
- (H1) is the precise content of "typical log S and log |r| fall linearly". It is an assumption about the circuit
  family, checked empirically in B1. It is not a theorem about circuits.

## 3. Proposition 3 (when the exponent doubles)

Under Proposition 2, with b_S > 0 and b_S + 2b_r > 0:

    b_SW / b_LE = (2b_S + 2b_r)/(b_S + 2b_r).

- If b_r = 0, the ratio equals 2.
- If b_r > 0, it lies strictly between 1 and 2.
- If −b_S/2 < b_r < 0, it is larger than 2.

*Proof.* Substitute and compare the numerator with twice the denominator: 2b_S + 2b_r − 2(b_S + 2b_r) = −2b_r. ∎

## 4. Proposition 4 (conditional sign law for Loschmidt)

Let K± ~ Bin(M, F±) be independent, and let ĝ_LE ∝ K₋ − K₊. Then as M S → 0:

    P(sign ĝ_LE = sign g | ĝ_LE ≠ 0) = (1 + |r|)/2 + O(M S).

*Proof.*

1. The probability of a nonzero estimate is

        P(K₋ ≠ K₊) = P(exactly one count) + P(≥ 2 counts, K₋ ≠ K₊)
                   = M F₋(1−F₋)^{M−1}(1−F₊)^M + M F₊(1−F₊)^{M−1}(1−F₋)^M + O((MS)²)
                   = M S (1 + O(MS)).

2. The probability that the count lands in the batch with the larger fidelity is M max(F±) (1 + O(MS)).

3. The ratio of the two is max(F±)/S + O(MS) = (1 + |r|)/2 + O(MS). ∎

**Check.** B1 (§20) evaluated this exactly on 720 (cell, θ, M) points. The maximum error is 9 × 10⁻⁵ for
MS ≤ 10⁻³ and 4.8 × 10⁻⁴ for MS ≤ 10⁻², growing ∝ MS as stated.

## 5. Where the finite-n residual comes from (B1)

B1 measured ε_gap = (b_SW − b_LE) − b_S at −0.002 to −0.005 decades/qubit. It splits exactly
(`results/b1_entangling/posthoc_gap_decomposition.csv`) as:

    ε_gap = [slope(median log₁₀ R) − b_S]  +  [slope(median log₁₀ M_SW − median log₁₀ M_LE − median log₁₀ R)]
                   (A: O(S) term)                        (D: non-additivity of medians)

**Term A.** log₁₀ R is a decreasing function of S alone, so median log₁₀ R = log₁₀ 2 − median log₁₀ S + O(S)
exactly. A vanishes as S → 0. Measured: −0.002 decades/qubit on n = 4–16, falling to ≤ 3 × 10⁻⁴ for n ≥ 8.

**Term D.** This is the median non-additivity of Proposition 2's remark, at finite n. It is nonzero exactly when
(H1) fails at the sizes probed, i.e. when the shape of (X_n, Y_n) still changes with n:
- shallow circuits: about −0.003;
- deep circuits: ≈ 0.

Proposition 2 itself is not contradicted. Its hypothesis is only approximately met in shallow circuits at n ≤ 16.

## 6. Proposition 5 (global depolarizing noise) — prediction for B4

**Model.** After each of L layers, apply ρ ↦ (1 − p)ρ + p I/d, with d = 2ⁿ. This channel commutes with unitaries,
so the output is

    ρ' = q ρ + (1 − q) I/d,   q = (1 − p)^L.

**Exact consequences.** These follow for the same θ, shifts included:

    F±' = q F± + (1 − q)/d,    S' = q S + 2(1 − q)/d,    Δ' = q Δ,    r' = q Δ / S'.

Proposition 1 still holds with primed quantities.

**Asymptotic exponents.** Suppose the noiseless family satisfies (H1) with exponents (b_S, b_r) and p > 0 is fixed.

**(a) Fixed depth (q constant), b_S > log₁₀ 2.** The noiseless typical S falls faster than the floor 2(1−q)/d, so the
floor eventually dominates S'. Then

    b_S' → log₁₀ 2,   b_r' → b_S + b_r − log₁₀ 2.

*Proof.* S' ~ 2(1−q) 2^{−n}, and r' = qΔ/S' with Δ = rS ~ 10^{−(b_S + b_r) n}. ∎

**(b) Fixed depth, b_S = log₁₀ 2.** Both terms of S' scale as 2^{−n}, so b_S' = log₁₀ 2 and b_r' = b_r.

**(c) Depth L = n.** Here q = (1 − p)ⁿ → 0, so S' → 2/d and

    b_S' → log₁₀ 2,   b_r' → b_S + b_r − log₁₀ 2 − log₁₀(1 − p).

**Predictions for the RX product** (Stage 7: L = 1, b_S = log₁₀ 4, b_r = 0):

    b_S' → log₁₀ 2,  b_r' → log₁₀ 2,  b_LE' → log₁₀ 8,  b_SW' → log₁₀ 16 (unchanged),  ratio → 4/3.

- Global depolarizing raises the Loschmidt exponent from 4ⁿ to 8ⁿ.
- It leaves the SWAP exponent at 16ⁿ.
- It **breaks** exponent doubling through b_r' > 0, while the general slope rule of Proposition 2 still holds.
- The crossover happens at the n where q·median S(n) ≈ 2(1−q)2^{−n}, roughly 2^{−n*} ≈ 2p/(1−p) times a
  family-dependent constant. For p = 10⁻³ that is n* ≈ 10, so it falls **inside** the probed range.

**Predictions for the B1 cells** (noiseless b_S from B1):

| cell | b_S' | b_r' |
|---|---|---|
| HEA d2 (b_S ≈ 0.376) | → 0.301 | → ≈ 0.075 |
| HEA d4 (0.319) | → 0.301 | → ≈ 0.018 |
| RX–RY + CZ d2 / d4 (0.382 / 0.340) | → 0.301 | → ≈ 0.081 / 0.039 |
| depth-n cells (b_S ≈ 0.303) | → 0.301 | → −log₁₀(1 − p): 4.4 × 10⁻³ at p = 10⁻², 4.6 × 10⁻² at p = 10⁻¹ |

These limits are asymptotic. At n ≤ 16 B4 measures how far each cell has moved toward them. It does not assume they
are reached.

## 7. Proposition 6 (local depolarizing on the product circuit) — prediction for B4

**Model.** Single-qubit depolarizing with probability p on every qubit after its rotation. For the product circuit
the state remains a product: ρ' = ⊗_j[(1 − p)ρ_j + p I/2]. With c_j = cos²(θ_j/2):

    f_j = (1 − p) c_j + p/2,   F±' = ∏_{j≠k} f_j · [(1 − p)(1 ∓ s)/2 + p/2],
    S' = ∏_{j≠k} f_j,   r' = (1 − p) s.

**Consequences.**
1. r' has an n-independent law, so **b_r' = 0**, and exponent doubling survives local depolarizing on this family.
2. log₁₀ S' is a sum of n − 1 iid terms, so

        b_S'(p) = −E log₁₀ f = −(2/ln 10) ln[(√(1 − p/2) + √(p/2))/2].

   This uses the arcsine law of c_j. The identity was verified against numerical integration to 10⁻¹⁵.
3. Hence b_LE' = b_S'(p) and b_SW' = 2b_S'(p), with ratio 2.

| p | b_S'(p) | Loschmidt base | SWAP base |
|---|---|---|---|
| 0 | 0.6021 (log₁₀ 4) | 4ⁿ | 16ⁿ |
| 10⁻³ | 0.5831 | | |
| 10⁻² | 0.5447 | | |
| 0.1 | 0.4449 | | |
| 0.5 | 0.3311 | | |
| 1 | 0.3010 (log₁₀ 2) | | |

Local noise **lowers** both exponents and keeps their ratio at 2.

Comparing Propositions 5 and 6: whether noise breaks exponent doubling depends on the noise model, not only on its
strength. Correlated global depolarizing creates a 2^{−n} fidelity floor that the signal Δ does not share, so
b_r' > 0. Local depolarizing on a product state lifts every factor equally and keeps r' independent of n.
