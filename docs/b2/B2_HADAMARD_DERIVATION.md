# B2 Hadamard-test fidelity estimator: derivation

This was written before the B2 sweep, as the principal B2 bullet requires: the estimator, its finite-shot mean,
its variance, its gradient estimator and its low-overlap limit come first, and slopes are fitted only after the
formulas pass numerical checks. Code: `src/qlo/b2/hadamard_theory.py`. Checks: `tests/test_b2_estimators.py` and
`results/b2_estimators/hadamard_variance_validation.csv`.

## 1. What a Hadamard test measures

Take target |φ⟩ = V|0ⁿ⟩, trial |ψ⟩ = U(θ)|0ⁿ⟩, W = V†U and overlap a = ⟨φ|ψ⟩ = ⟨0ⁿ|W|0ⁿ⟩ = x + iy.

- **Real quadrature:** ancilla H, controlled-W, H, then measure Z on the ancilla. One shot gives X ∈ {+1, −1}
  with E[X] = x.
- **Imaginary quadrature:** the same circuit with S† on the ancilla before the last H. It gives Y ∈ {+1, −1}
  with E[Y] = y.

Each shot is a ±1 variable with P(+1) = (1 + q)/2, where q = x or y. The test returns the amplitude, not the
fidelity. The fidelity is F = |a|² = x² + y², so it needs **both** quadratures unless the phase of a is known.

On the Stage 7 RX product, ⟨0|RX(θ)|0⟩ = cos(θ/2) is real, so y = 0 at every θ and every shift. B2's primary
estimator still measures both quadratures, because it is defined for a general complex overlap; it does not use
this landscape-specific fact. The circuit validation uses random hardware-efficient circuits with genuinely complex
overlaps.

## 2. Why the plug-in estimator is biased

With M shots and sample mean x̄ = S/M, where S = ΣXᵢ, E[x̄²] = x² + Var(x̄) = x² + (1 − x²)/M. The plug-in
x̄² + ȳ² therefore overestimates F by (2 − x² − y²)/M ≈ 2/M. In a barren plateau F is about 4^−n, so this bias is
much larger than F itself at any affordable M. B2 does not use it as an estimator.

## 3. The unbiased U-statistic

For M ≥ 2 shots of one quadrature:

    U = (2 / [M(M−1)]) Σ_{i<j} XᵢXⱼ = (S² − M) / [M(M−1)]

The second form uses Xᵢ² = 1, so S² = M + 2Σ_{i<j}XᵢXⱼ. For i ≠ j the shots are independent, so E[XᵢXⱼ] = q² and
**E[U] = q²**.

The fidelity estimator takes independent x- and y-batches and adds them:

    F̂_HT = U_x + U_y,   E[F̂_HT] = x² + y² = F

F̂_HT is not confined to [0, 1]. For example, S = 0 gives U = −1/(M−1). It is never clipped, because clipping
would reintroduce bias.

## 4. Exact variance

Write U = c·P with P = Σ_{i<j} XᵢXⱼ and c = 2/[M(M−1)]. Then Var P is a sum of covariances over pairs of pairs.

**The same pair {i, j}** (there are M(M−1)/2 of these):

    Var(XᵢXⱼ) = E[Xᵢ²Xⱼ²] − q⁴ = 1 − q⁴

**Pairs sharing exactly one index**, such as {i, j} and {i, k} (there are M(M−1)(M−2) ordered pairs of pairs):

    Cov = E[Xᵢ² XⱼXₖ] − q⁴ = q² − q⁴

**Disjoint pairs** are independent, so their covariance is 0.

Adding these up:

    Var P = M(M−1)/2 · (1 − q⁴) + M(M−1)(M−2) · q²(1 − q²)

    Var U = c² Var P = [2(1 − q⁴) + 4(M−2) q²(1 − q²)] / [M(M−1)]

With independent quadrature batches:

    Var F̂_HT = Var U_x + Var U_y

Unlike Loschmidt and SWAP, this depends on how F splits between x² and y², not on F alone. B2 therefore records
x± and y± for every θ.

**Checks.** The variance was checked in two ways:
- exhaustive enumeration of all 2^M outcome sequences for M = 2..6 and q ∈ {0, 0.3, −0.7, 0.95};
- the exact pmf of S = 2K − M with K ~ Bin(M, (1+q)/2), for M up to 256.

Both agree with the formula to ≤ 3e-16.

## 5. Parameter-shift gradient

The estimator is

    ĝ_HT = (F̂_HT(θ − π/2 e_k) − F̂_HT(θ + π/2 e_k)) / 2

with four independent batches of M shots: (x₊, y₊, x₋, y₋). It is unbiased, E[ĝ_HT] = (F₋ − F₊)/2 = Δ/2 = g, and

    Var ĝ_HT = [Var F̂₊ + Var F̂₋] / 4 = [A + B(M−2)] / [4M(M−1)]

where A = 2Σ(1 − q⁴) and B = 4Σ q²(1 − q²), both summed over the four quadratures q ∈ {x₊, y₊, x₋, y₋}.

**Shot convention.** M is the number of shots per quadrature per shift. A gradient component costs **4M** circuit
executions. Loschmidt and SWAP cost 2M.

**Required shots.** Var ĝ is decreasing in M. SNR = |g|/√Var ≥ ρ is equivalent to
c M(M−1) − B M − (A − 2B) ≥ 0, with c = 4g²/ρ² = Δ²/ρ². B2 takes the closed-form root, rounds it up to an
integer M ≥ 2, and corrects it by evaluating the exact variance at M − 1 and M (`required_m_ht`).

## 6. Low-overlap (barren-plateau) limit

Let all four quadratures go to zero, so F± → 0. Then:

    Var U → 2/[M(M−1)]                  so  Var F̂_HT → 4/[M(M−1)] ≈ 4/M²   (two quadratures)

A fidelity near zero is estimated with variance O(1/M²), not the O(F/M) of the projector or the O(1/M) of SWAP.
The U-statistic of a near-zero mean is a product of two near-zero sample means.

For the gradient, A → 8 and B → 4Σq² = 4(F₊ + F₋) = 4S, because x² + y² = F at each shift. To leading order:

    Var ĝ_HT ≈ 2/M² + S/M

So the S/M term cannot be dropped. With Δ = rS, SNR ≥ ρ becomes (Δ²/4)M² − ρ²S M − 2ρ² ≥ 0, which gives

    M_HT ≈ 2ρ² [1 + √(1 + 2r²/ρ²)] / (r² S)

Compare M_LE ≈ ρ²/(r² S). At the solution M·S ≈ 2ρ²[1 + √(1 + 2r²/ρ²)]/r² ≥ 4ρ²/r² ≥ 4ρ², so the 2/M² term
never dominates at the required budget.

**Consequence, predicted before the sweep:**

- M_HT has the same 1/(r² S) dependence as M_LE, with a constant factor 2[1 + √(1 + 2r²/ρ²)] between 4 and
  2(1 + √3) ≈ 5.46.
- In total circuit executions (4M against 2M) the Hadamard estimator needs roughly 8 to 11 times the Loschmidt
  executions.
- The median shot exponent should therefore match Loschmidt's, b_S + 2b_r, which is log10 4 on the RX product,
  not SWAP's.

This is predeclared Case B (B2_CONFIG.md). The sweep checks it and does not assume it.

## 7. Failure-mode vocabulary

F̂_HT lives on the lattice (S_x² + S_y² − 2M)/[M(M−1)]. Its gradient is zero only when S_x₋² + S_y₋² equals
S_x₊² + S_y₊². That is not a rare-event starvation: at small M S, the counts are not mostly zero. B2 therefore
measures the exact sign probabilities and P(ĝ = 0), from small-M enumeration plus seeded Monte Carlo, and labels
the failure only after seeing the distributions.
