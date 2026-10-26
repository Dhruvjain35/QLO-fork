# Stage 5 — Finite-shot gradient dead zones on the controlled projector benchmark

Exact, mechanistic characterization of *why* finite-shot parameter-shift gradients failed
as an exploration mechanism in Stage 4. No optimizer is implemented or evaluated here.
Statements are labelled **Proposition** only when the assumptions are explicit; nothing
is claimed as a general theorem.

## 1. Motivation from Stage 4
Stage 4 found that on the verified global barren plateau (Stage 3) finite-shot SGD was
indistinguishable from exact GD at matched learning rate and from covariance-matched
Gaussian noise, and that at n = 12 a large fraction of finite-shot trajectories had an
estimated gradient *identically zero* for all 2000 iterations (54 % at M = 16, 29 % at
M = 1024). Stage 5 asks: how does a finite measurement budget convert an exponentially
small gradient into a high-probability exactly-zero estimator, and how does the shot cost
of resolvability scale with n? The matched local cost is the control.

## 2. Controlled benchmark (frozen from Stage 3/4)
`|ψ(θ)> = ⊗_j RX(θ_j)|0^n>`, `θ_j ~ iid U[−π, π]`, `F = ∏_j cos²(θ_j/2)`, `C_G = 1 − F`.
For component k: `A_k = ∏_{j≠k} cos²(θ_j/2)`, `s_k = sin θ_k`.

## 3. Exact finite-shot gradient distribution
**Proposition 1 (shifted fidelities; verified to 1e-15 in tests).**
`F₊ = F(θ + π/2 e_k) = A(1−s)/2`, `F₋ = A(1+s)/2`, hence `F₊ + F₋ = A`,
`F₊² + F₋² = A²(1+s²)/2`, and `g_k = ∂C/∂θ_k = A s/2 = ½(F₋ − F₊)`.
*Proof.* `cos²((θ_k ± π/2)/2) = (1 + cos(θ_k ± π/2))/2 = (1 ∓ sin θ_k)/2`. ∎

**Proposition 2 (estimator identity).** With `K₊ ~ Bin(M, F₊)`, `K₋ ~ Bin(M, F₋)`
independent (one batch per shift) and `Ĉ = 1 − K/M`,
`ĝ_k = ½[Ĉ₊ − Ĉ₋] = (K₋ − K₊)/(2M)`. Its support is `{j/(2M) : j = −M..M}`; it is unbiased
(`E ĝ_k = (F₋ − F₊)/2 = g_k`). The estimator is a difference of two independent binomials.

## 4. Exact zero-estimator probability
**Proposition 3.** `ĝ_k = 0 ⟺ K₊ = K₋`, so
`P₀(θ, M, k) := P(ĝ_k = 0 | θ, M) = Σ_{r=0}^{M} Bin(r; M, F₊) Bin(r; M, F₋)`, and
`P_both0 := (1−F₊)^M (1−F₋)^M ≤ P₀` (equal non-zero counts also give zero).
Numerics: log-pmfs from the recurrence `log C(M,r) = Σ_{i≤r} log((M−i+1)/i)` and
`logsumexp`, summed over the window where both pmfs are non-negligible; exact to float
rounding whenever the window starts at r = 0 (true for every required-shot solve below,
where `M F± = O(1–100)`); stable at M = 10²⁰. Verified against brute-force
`scipy.stats.binom` sums to 2.6e-15 for M < 80 and to 1e-11 relative at M = 2×10⁶.

## 5. Deep-plateau approximations (A ≪ 1) — approximations, not identities
Poisson limit `K± ~ Poisson(M F±)` gives the closed form
`P₀ ≈ e^{−MA} I₀(MA |cos θ_k|)` (the `I₀` factor is exactly the equal-non-zero-count
contribution). The cruder rare-event form `P₀ ≈ P_both0 ≈ e^{−MA}` drops that factor and
yields `M_nonzero(q) ≈ −log(1−q)/A`. Both are labelled asymptotic; §8 quantifies them.

## 6. Conditional variance and SNR (exact)
**Proposition 4.** `Var(ĝ_k|θ) = [F₊(1−F₊) + F₋(1−F₋)]/(4M) = [A − A²(1+s²)/2]/(4M)`,
`SNR_k² = g_k²/Var = M A s² / [1 − A(1+s²)/2]`, and for `s ≠ 0`, `A ≠ 0`
`M_SNR(ρ) = ρ² [1 − A(1+s²)/2] / (A s²)` (integer budget `⌈M_SNR⌉`).
Edge cases handled explicitly: `s = 0` or `A = 0` ⇒ SNR = 0, `M_SNR = ∞`;
`A = 1, s² = 1` ⇒ deterministic estimator (`F± ∈ {0,1}`), `M_SNR = 0`.
Verified against the Stage 4 form to 1e-12 relative on 200 random (n, θ, k, M).

## 7. Typical initialization scaling
**Proposition 5.** For `θ ~ U[−π, π]`: `E[log cos²(θ/2)] = −2 log 2` (quadrature:
−1.386294 vs −1.386294, |err| < 1e-8), `Var[log cos²(θ/2)] = π²/3`, `E[cos²(θ/2)] = ½`.
Hence `E[log A_k] = −2(n−1) log 2`, the **geometric (log-typical) scale is
`exp E[log A_k] = 4^{−(n−1)}`**, while the **arithmetic mean is `E[A_k] = 2^{−(n−1)}`**.
These differ by a factor `2^{n−1}`: the mean of A is dominated by rare initializations
near the target, the typical initialization is exponentially deeper. Everything that
scales like `1/A` (nonzero-probability and SNR shot requirements) therefore inherits
`4^{n−1}` growth at a *typical* initialization — a distributional statement, not a
per-initialization one.

## 8. Global shot complexity (`shot_scaling_summary.csv`, `scaling_fits.json`)
100 000 θ per n, n = 2…20, k = 0. For every θ the **exact integer** M with
`1 − P₀(M) ≥ q` was found by vector bisection on Proposition 3 (bracket verified for
100 % of samples; the "hybrid" fallback was never needed because the exact sum is
cheap in the relevant regime `M F± = O(1–100)`); the Poisson-limit and rare-event
approximations were recorded alongside. `M_SNR` is closed form.

| n | median log10 M, P(ĝ≠0)≥0.5 | P(ĝ≠0)≥0.9 [IQR] | SNR≥1 | SNR≥2 [IQR] | E[log A] emp / theory | E[A] emp / theory |
|---|---|---|---|---|---|---|
| 2 | 0.30 | 1.00 [0.60, 1.54] | 0.72 | 1.33 [0.63, 2.21] | −1.389 / −1.386 | 0.500 / 0.500 |
| 4 | 1.38 | 2.15 [1.43, 3.14] | 2.08 | 2.68 [1.79, 3.84] | −4.161 / −4.159 | 0.1247 / 0.125 |
| 6 | 2.59 | 3.34 [2.34, 4.63] | 3.30 | 3.90 [2.79, 5.31] | −6.946 / −6.931 | 0.0310 / 0.0313 |
| 8 | 3.79 | 4.54 [3.32, 6.04] | 4.49 | 5.09 [3.79, 6.70] | −9.706 / −9.704 | 7.77e-3 / 7.81e-3 |
| 10 | 4.99 | 5.74 [4.33, 7.42] | 5.70 | 6.30 [4.82, 8.08] | −12.48 / −12.48 | 1.98e-3 / 1.95e-3 |
| 12 | 6.18 | 6.93 [5.34, 8.80] | 6.90 | 7.50 [5.84, 9.45] | −15.22 / −15.25 | 5.14e-4 / 4.88e-4 |
| 14 | 7.42 | 8.16 [6.41, 10.20] | 8.13 | 8.73 [6.92, 10.83] | −18.06 / −18.02 | 1.21e-4 / 1.22e-4 |
| 16 | 8.59 | 9.35 [7.47, 11.51] | 9.31 | 9.91 [7.98, 12.14] | −20.77 / −20.79 | 3.07e-5 / 3.05e-5 |
| 18 | 9.80 | 10.55 [8.53, 12.84] | 10.53 | 11.13 [9.05, 13.46] | −23.54 / −23.57 | 8.3e-6 / 7.6e-6 |
| 20 | 11.00 | 11.75 [9.61, 14.17] | 11.72 | 12.32 [10.13, 14.80] | −26.33 / −26.34 | 1.75e-6 / 1.91e-6 |

(90th percentiles and geometric means are in the CSV; e.g. P(ĝ≠0)≥0.9 at n=20: q90 = 16.6.)
`E[A]` fluctuates at large n because A is heavy-tailed (as in Stage 3); `E[log A]` does not.

**Fits `median log10 M = a + b n`** (theory reference log10 4 = 0.6021 for anything ∝ 1/A at the log-typical A; log10 2 = 0.3010 would be the arithmetic-mean scaling):

| statistic | slope b | R² | max |residual| | closer to |
|---|---|---|---|---|
| P(ĝ≠0) ≥ 0.5 | **0.5980** | 0.99991 | 0.079 (n=2) | log10 4 |
| P(ĝ≠0) ≥ 0.9 | **0.5989** | 0.99997 | 0.041 | log10 4 |
| SNR ≥ 1 | **0.6069** | 0.99987 | 0.101 (n=2) | log10 4 |
| SNR ≥ 2 | **0.6069** | 0.99987 | 0.101 | log10 4 |
| geometric mean, P(ĝ≠0)≥0.9 | 0.6031 | 0.99998 | — | log10 4 |
| geometric mean, SNR≥2 | 0.6109 | 0.99960 | — | log10 4 |
| q25 / q75 / q90, P(ĝ≠0)≥0.9 | 0.505 / 0.696 / 0.784 | ≥0.998 | — | (see note) |

Slopes were not forced. The median and geometric-mean slopes sit within 0.005 of log10 4
(the geometric mean must, since `E[log M] = const − E[log A]` exactly in the rare-event
regime). Other quantiles fan out because `Var[log A] = (n−1)π²/3` grows with n: the
lower quartile of initializations needs ~10^{0.5n}, the 90th percentile ~10^{0.78n}
shots. An `n log 2` (arithmetic-mean) model is rejected by every statistic (slope error
0.30 vs 0.004). **Typical shot requirements grow as 4^{n−1}; this is a distributional
statement, and individual initializations range over orders of magnitude around it.**

Approximation quality on the same samples (median |Δ log10 M| vs exact, target 0.9):
Poisson limit 5e-7 (n≥10) to 0.04 (n=2), max 0.42 at n=2; rare-event 0.17 at every n
(a constant factor ≈ 1.5 at typical |s|, but up to 36× at the 99 % target when |s| is
small — see `representative_targets.csv`: ratio approx/exact 0.03–0.99). The
approximation-accuracy map (`theory_validation.json`) gives max |P₀ error| of the Poisson
limit = 1.8e-7, 1.8e-5, 1.8e-4, 1.8e-3, 0.019 for A = 1e-6, 1e-4, 1e-3, 1e-2, 0.1 (∝ A),
while the rare-event form's error stays ≈ 0.18 at every A because it drops the
equal-non-zero-count mass. **P₀ ≈ e^{−MA} is adequate only for order-of-magnitude
statements; the Poisson-limit form is quantitatively exact deep in the plateau.**

## 9. Local-cost control (`local_control_summary.csv`)
`C_L = 1 − (1/n)Σ_j cos²(θ_j/2)`, `g_{L,k} = sin θ_k/(2n)`. **Term-wise estimator**
(measurement-efficient; exploits the known decomposition — measures only qubit k's
projector at the two shifts): `p± = (1∓s)/2`, `ĝ_{L,k} = (K₋ − K₊)/(2Mn)`.
**Proposition 6.** `Var(ĝ_{L,k}|θ) = cos²θ_k/(8Mn²)` and `SNR_L² = 2M tan²θ_k`
(verified to 2e-13 relative). The explicit n cancels: `1/(2n)` in the gradient vs
`1/n` in the standard deviation. Consequences at every n ∈ 2…20: median M for
P(ĝ≠0) ≥ 0.5 is **1**, for ≥ 0.9 is **2**, for SNR ≥ 1 is 0.5 (→ 1 shot), for SNR ≥ 2
is 2 (fitted slopes 0.0000, 0.0000, 0.0001, 0.0001); median `P₀` at M = 16 is 2e-6 and
at M = 1024 underflows to 0. This does NOT say local training is free — the local
cost's landscape and its own trainability are a different question — only that for this
benchmark and this estimator the *measurement* burden does not carry the exponential
width dependence.

## 10. Finite-shot gradient dead zone — operational definition
*Introduced for this analysis; not established terminology.* A point θ is in an
**(M, q)-dead zone for component k** if `P(ĝ_k = 0 | θ, M) ≥ q`. Separately, for the
full gradient with one independent batch per (k, ±) (the Stage 4 estimator),
`P(ĝ = 0 | θ, M) = ∏_k P₀(θ, M, k)` — the product form holds *only* under that
conditional independence. Levels q ∈ {0.5, 0.9, 0.99} are used below.

## 11. Dead-zone volume (`deadzone_fraction.csv`; 100 000 θ per n; full-gradient: 5 000 θ)
Initialization dead-zone fraction `P_θ[P₀ ≥ q]`, component k = 0, q = 0.9:

| n \ M | 16 | 64 | 256 | 1024 | 4096 | 16384 |
|---|---|---|---|---|---|---|
| 4 | 0.313 | 0.201 | 0.125 | 0.075 | 0.045 | 0.026 |
| 6 | 0.629 | 0.482 | 0.353 | 0.251 | 0.172 | 0.115 |
| 8 | 0.846 | 0.733 | 0.606 | 0.484 | 0.372 | 0.278 |
| 10 | 0.948 | 0.887 | 0.803 | 0.701 | 0.593 | 0.485 |
| 12 | 0.985 | 0.960 | 0.915 | 0.851 | 0.769 | 0.678 |
| 14 | 0.997 | 0.988 | 0.970 | 0.936 | 0.888 | 0.825 |
| 16 | 0.999 | 0.997 | 0.990 | 0.975 | 0.952 | 0.915 |

Full-gradient fraction `P_θ[∏_k P₀ ≥ 0.9]`: n=4: 0.070 → 0.001; n=8: 0.564 → 0.071;
n=12: 0.896 → 0.363; n=16: 0.987 → 0.716 (M = 16 → 16384). q = 0.5 and 0.99 tables are
in the CSV (e.g. q=0.99, M=1024: 0.03, 0.13, 0.30, 0.52, 0.71, 0.85, 0.93 for n = 4…16).
At fixed M the fraction approaches 1 with n; multiplying M by 1024 buys roughly 4–5
qubits, consistent with §8.

## 12. Stage 4 prediction / retrodiction (`stage4_prediction*.csv`)
Using the *actual* 100 Stage 4 start points `θ₀` (seeds 1000–1099, n = 12): per
component `P₀(θ₀, M, k)`, full-vector `P_full = ∏_k P₀`, and — because a zero full
gradient leaves θ unchanged so successive iterations are iid — the exact probability of
never moving in T = 2000 iterations, `P_full^T`. Prediction is paired with the observed
Stage 4 runs at the same θ₀ (5 replicates each), so initialization variance cancels:

| M | observed never-moved / 500 | paired prediction ± SD | z | seeds predicted stuck (P>0.5) / observed majority-stuck | disagreeing seeds |
|---|---|---|---|---|---|
| 16 | 250 (50.0 %) | 244.8 ± 4.8 | +1.08 | 52 / 53 | 1 |
| 64 | 199 (39.8 %) | 198.1 ± 4.8 | +0.19 | 41 / 41 | 2 |
| 256 | 149 (29.8 %) | 154.2 ± 4.5 | −1.14 | 31 / 30 | 3 |
| 1024 | 121 (24.2 %) | 114.0 ± 4.5 | +1.56 | 23 / 25 | 2 |

The mean single-iteration full-zero probability is 0.966 / 0.917 / 0.848 / 0.762, and
`P_stuck` is bimodal over θ₀ (52 % of starts have `P_stuck > 0.5` at M = 16): a start
either has every `A_k` small enough that `M·A_k ≲ 1/T` for all k, or it does not.
**Stage 4's zero-quantization is quantitatively retrodicted with no free parameter.**
Erratum to STAGE4.md: the fractions quoted there (54/44/34/29 %) used
`log10(F_best/F0) < 1e-12` only and therefore also counted runs that moved *downhill*;
the exact never-moved fractions are 50.0/39.8/29.8/24.2 %.

## 13. Relation to known barren-plateau resolvability literature
That exponentially vanishing gradients impose exponential measurement-resolution costs
is already established in the broader literature — e.g. Wang et al., Nat. Commun. 12,
6961 (2021) (noise-induced barren plateaus and finite-shot resolvability); Larocca et
al., Nat. Rev. Phys. 7, 174–189 (2025) (review); Qin, arXiv:2608.09810 (2026)
(finite-shot / SNR / resource analysis for SPSA). Stage 5 does not add to that general
fact. Its contribution is narrower: an exact, mechanistic finite-shot quantization /
dead-zone analysis (exact estimator distribution, exact `P(ĝ=0)`, exact SNR, typical
`4^{n−1}` scaling, term-wise local contrast, parameter-free retrodiction of Stage 4)
for the controlled projector-cost benchmark validated in Stages 3–4.

## 14. What is specific to this benchmark
The product structure `F = ∏ cos²(θ_j/2)` (so `F₊ + F₋ = A` and the two shifted
probabilities share the common factor A); the projector cost (single ±1-free
Bernoulli outcome per shot, hence exact binomial counts); the uniform initialization
(which fixes `E[log cos²] = −2 log 2` and hence the `4^{n−1}` constant); one independent
batch per (k, ±); the term-wise local estimator (which requires knowing the cost's
decomposition). The constants 4 and 2, the `I₀` form, and the exact `n`-cancellation in
the local SNR all depend on these.

## 15. What may generalize (hypotheses, not results)
For any cost whose parameter-shift estimator is a difference of two independent
count-based estimates, `ĝ = 0` requires equal counts, and when both success
probabilities are O(A) the zero probability behaves like `e^{−cMA}` times a
correction; the qualitative conclusion "shots-to-resolve ∝ 1/(gradient-scale
probability), hence exponential in n on a barren plateau, with a log-normal-like spread
over initializations" is expected to survive. The *constants*, the closed forms, and the
independence of the local burden on n are not expected to.

## 16. What has NOT been proved
No general theorem for arbitrary costs, ansätze, initializations or measurement
allocations; no lower bound on shots for *any* estimator (only this parameter-shift
estimator with independent batches); nothing about correlated / shared-sample
strategies, SPSA, or adaptive shot schedules; nothing about hardware noise; nothing
about novelty (unconfirmed absent a dedicated literature review); nothing about FDT,
QLO, escape times, or quantum advantage. The `4^{n−1}` statement is about the log-typical
initialization under `U[−π,π]`, not about every initialization and not about `4^n`.

## Validation summary (engineering)
- Identities (§3, §6, §9): max abs/relative error ≤ 4e-15 (global), 2e-13 (local) on 200 random (n, θ, k, M).
- `P₀` vs brute force: 2.6e-15 (M<80), 1e-11 relative (M = 2×10⁶); finite and stable at M = 10²⁰.
- Monte Carlo (`monte_carlo_validation.csv`, 75 cells, 20 000 binomial replicates, θ at lower-quartile / typical / upper-quartile A for n = 4…12, M at ⅛…8× the P(ĝ≠0)=0.5 threshold): exact `P₀` inside the Wilson 95 % CI in 70/75 cells (≈5 % misses expected), max |z| of the mean 2.76, empirical/analytic variance 0.92–1.06, empirical/analytic SNR 0.97–1.05; max |Poisson − exact| = 0.008, max |rare-event − exact| = 0.158.
- PennyLane (`pennylane_validation.csv`, n = 3, 4, 6 × 3 θ × M = 16, 64, 256, 400 reps each): exact `P₀` inside the PennyLane Wilson CI in 27/27 cells, PennyLane-vs-binomial mean |z| ≤ 1.70, PennyLane/analytic variance ratio 0.85–1.72 (mean 1.00; the 1.72 is a cell with 8 non-zero draws out of 400, i.e. the small-count regime).
- Stage 4 retrodiction: paired |z| ≤ 1.6 at all four M.
