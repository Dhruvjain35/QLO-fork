# Stage 6 — Do all finite-shot barren plateaus fail the same way?

Two analytically controlled global barren plateaus on the same circuit, compared at the level
of the finite-shot parameter-shift estimator. No optimizer is implemented. The Stage 3–5
projector code is reused unmodified. All numbers below are from one run of
`python -m qlo.experiments.stage6 --workers 5` (365 s wall, 2.2 GB peak, `results/stage6/`).

## 1. Motivation
Stage 5 showed that on the global **projector** benchmark the finite-shot estimator fails by
*count starvation*: both shifted success probabilities are O(A_k) ≈ 4^{−(n−1)}, so at any
realistic M both counts are usually 0 and ĝ ≡ 0 (the "dead zone"), which retrodicted Stage 4's
never-moving trajectories with no free parameter. Stage 6 asks whether that is *the* way finite
shots fail on a barren plateau, or one of several.

## 2. Why Stage 5 is not automatically universal
The dead-zone mechanism needs the two shifted Bernoulli probabilities to sit near 0 (or 1). A
global Pauli-parity cost puts them near 1/2 instead, where a tie K₊ = K₋ has probability only
≈ 1/√(πM) no matter how small the gradient is. Same estimator algebra, different location of the
outcome probabilities, so a different failure mode is possible.

## 3. Prior-work boundary
- Cerezo et al., Nat. Commun. 12, 1791 (2021): cost-function-dependent barren plateaus (global vs local).
- Wang et al., Nat. Commun. 12, 6961 (2021): noise-induced barren plateaus; finite-shot resolvability.
- Larocca et al., Nat. Rev. Phys. 7, 174–189 (2025): review.
- Aghaei Saem, Tafreshi, Holmes, Thanasilp, Quantum Sci. Technol. 11, 015049 (2026),
  doi:10.1088/2058-9565/ae2202: exponential concentration at the level of measurement-outcome
  probabilities, including a global Pauli-Z example.
- Qin, arXiv:2608.09810 (2026): finite-shot / SNR / resource analysis for SPSA.

That barren plateaus impose exponential measurement burdens, that concentration can be analysed at
the level of outcome probabilities, and that global Pauli observables concentrate under finite-shot
training are all **already established**. Stage 6 does not claim any of them. See §19–21.

## 4. Projector benchmark recap (frozen, Stages 3–5)
`|ψ(θ)⟩ = ⊗_j RX(θ_j)|0^n⟩`, θ_j ~ iid U[−π, π]. `C_G = 1 − ∏_j cos²(θ_j/2)`,
`A_k = ∏_{j≠k} cos²(θ_j/2)`, `F_± = A_k(1 ∓ s_k)/2`, `ĝ = (K₋ − K₊)/(2M)`,
`Var_θ[∂C_G/∂θ_k] = (1/8)(3/8)^{n−1}`, typical `A_k ≈ 4^{−(n−1)}`.

## 5. Global parity benchmark (new)
Same circuit and initialization. With `B_k = ∏_{j≠k} cos θ_j`, `s_k = sin θ_k`:

    μ_Z(θ) = ⟨Z_1⋯Z_n⟩ = ∏_j cos θ_j,      C_Z(θ) = [1 − μ_Z(θ)]/2 ∈ [0, 1]
    g_{Z,k} = ∂C_Z/∂θ_k = ½ s_k B_k
    μ(θ ± π/2 e_k) = ∓ s_k B_k  ⇒  p_± = C_Z(θ ± π/2 e_k) = (1 ± s_k B_k)/2
    ĝ_{Z,k} = (K₊ − K₋)/(2M),  K_± ~ Bin(M, p_±) independent
    E[ĝ] = g,  Var(ĝ | θ) = [1 − (s_k B_k)²]/(8M) = (1 − 4g²)/(8M)
    SNR² = 2M(s_k B_k)²/[1 − (s_k B_k)²],   M_SNR(ρ) = ρ²[1 − (sB)²]/[2(sB)²]

Edge cases are handled exactly: sB = 0 gives SNR 0 and M_SNR = ∞; |sB| = 1 gives deterministic outcomes, SNR = ∞ and M = 0.

## 6. Exact-gradient barren-plateau scaling (`parity_theory_validation.json`)
`Var_θ[g_{Z,k}] = ¼ E[sin²] ∏_{j≠k} E[cos²] = 2^{−(n+2)}`, which is exponential. Monte Carlo with 400 000 θ
per n; the standard error uses the **exact** 4th moment `E[g⁴] = (1/16)(3/8)^n` (kurtosis (3/2)^n):

| n | Var_emp | 2^{−(n+2)} | ratio | z | kurtosis |
|---|---|---|---|---|---|
| 2 | 0.06260 | 0.06250 | 1.002 | +0.94 | 2.25 |
| 3 | 0.03129 | 0.03125 | 1.001 | +0.47 | 3.38 |
| 4 | 0.01556 | 0.01562 | 0.996 | −1.33 | 5.06 |
| 6 | 3.907e-3 | 3.906e-3 | 1.000 | +0.02 | 11.4 |
| 8 | 9.706e-4 | 9.766e-4 | 0.994 | −0.78 | 25.6 |

Means are consistent with 0 (|z| ≤ 1.1). The 100 000-sample scaling runs (`parity_scaling_summary.csv`)
reproduce `E[g²]` at every n = 2…20 (e.g. n=20: 2.383e-7 vs 2.384e-7).

**Not a structural zero.** For every n ∈ {2,3,4,6,8} and every k, θ = (π/2)e_k gives g_k = ½
exactly. Over 2 000 random θ, every component has max|g_k| ≥ 0.24, and there are 0 exact-zero entries
out of 46 000. Every derivative is a non-trivial function of θ, so the small typical values are
concentration, not symmetry.

**Typical vs RMS scale.** `E[log|cos θ|] = E[log|sin θ|] = −log 2` (quadrature: −0.6931471805599465 /
−0.6931471805599472; theory −0.6931471805599453) and `Var[log|cos θ|] = π²/12` (0.822467033424). So
`E log|s_k B_k| = −n log 2`, and the log-typical gradient is `|g|_typ ≈ 2^{−(n+1)}`, while the RMS is
`2^{−n/2−1}`. The gap between them is exponential. Median- and variance-based statements about this benchmark are not
interchangeable.

## 7. Finite-shot parity distribution (validated)
Algebraic identities over 200 random (n, θ, k, M) cases, maximum error: gradient vs central finite difference 6.1e-11;
gradient vs sB/2 5.6e-17; μ_± 2.8e-16; p_± 1.7e-16; variance formula (relative) 4.1e-16; SNR formula (relative) 5.7e-16;
count identity 6.9e-17. Unbiasedness and the variance are also verified *exactly* by enumerating the full joint distribution of
(K₊, K₋) in the tests.

**Monte Carlo vs exact** (`direction_probability_validation.csv`; both benchmarks, n ∈ {4,6,8,10,12},
θ at the lower-quartile, median and upper-quartile |g| of a seeded pool, M ∈ {16, 256, 4096},
20 000 binomial replicates per cell, 90 cells). In the 78 cells with ≥ 30 expected non-zero draws,
the z-scores of empirical vs exact probability have mean / SD −0.06 / 0.92 (P_zero), +0.10 / 1.07
(P_correct) and −0.06 / 1.00 (P_wrong). Σz² for P_correct is 89.6 on 78 dof (p ≈ 0.17). Sample
variance / analytic variance lies in [0.890, 1.154] and max |z_mean| = 2.88. The other 12 cells are
deep-projector rare-event cells (expected non-zero draws 0.0001–25). There, sample moments are meaningless
and only counts are compared. Raw Wilson-CI coverage is 83/90 (P_zero) and 81/90 (P_correct). The
two are not independent per cell, and the aggregate z test above is the appropriate summary.

**PennyLane** (`pennylane_validation.csv`; `default.qubit` with finite shots, a global Z^⊗n measurement,
n ∈ {3,4,6}, M ∈ {16,64,256}, 3 θ each, 400 repetitions, 27 cells). Every estimate lies on the lattice
j/(2M). Mean vs exact g: max |z| = 1.58. PennyLane vs direct binomial model: z SD 0.96, max |z| 3.02.
Var_PL / analytic: mean 0.997, range [0.854, 1.141] (sampling SD ≈ 0.07). P_correct is inside the Wilson
CI in 27/27 cells and P_zero in 25/27.

## 8. Exact zero-estimator probability
`P_zero = Σ_r Bin(r; M, p_a) Bin(r; M, p_b)` (`exact_distribution.py`, windowed log-pmf reused from
Stage 5, CDF by complemented incomplete beta). At zero signal (p₊ = p₋ = ½) this is the central-binomial
identity `P_zero = C(2M, M)/4^M ~ 1/√(πM)`:

| M | exact | C(2M,M)/4^M | 1/√(πM) | rel. err vs asymptotic |
|---|---|---|---|---|
| 1 | 0.5000 | 0.5000 | 0.5642 | 0.114 |
| 10 | 0.1762 | 0.1762 | 0.1784 | 0.0124 |
| 1 000 | 0.01784 | 0.01784 | 0.01784 | 1.25e-4 |
| 10⁶ | 5.642e-4 | 5.642e-4 | 5.642e-4 | 1.27e-7 |

(Agreement with the central binomial is 3e-16 at small M and 4e-9 at M = 10⁶. The relative error vs the asymptotic
form is 1/(8M) to leading order, as expected.)

**The central contrast.** At fixed M and growing n (M = 1024, median over 20 000 θ, `failure_fraction.csv`):

| n | projector median P_zero | parity median P_zero |
|---|---|---|
| 4 | 0.0004 | 0.000005 |
| 6 | 0.230 | 0.0104 |
| 8 | 0.882 | 0.0171 |
| 10 | 0.9919 | 0.0176 |
| 12 | 0.99948 | 0.0176 |
| 16 | 0.999998 | 0.0176 (= 1/√(π·1024) = 0.01763) |

On the projector P_zero goes to 1. On parity it saturates at the zero-signal value 1/√(πM) and never
approaches 1. **This alone does not make parity trainable** (§9, §11).

## 9. Directional correctness
Exact `P_correct`, `P_wrong`, `P_zero` for the difference of two binomials (`directional.py`). In
every test they sum to 1 to within 1e-10. They are symmetric under g → −g. The bisection used for required shots
assumes P_correct is non-decreasing in *integer* M. That was checked on a grid for both benchmarks
(the largest decrease is 2.7e-10, which is rounding at P ≈ 1).

As the parity signal vanishes, the direction becomes uninformative while P_zero stays small:

| sB | M | P_correct | P_wrong | P_zero |
|---|---|---|---|---|
| 1e-2 | 1 000 | 0.665 | 0.319 | 0.016 |
| 1e-3 | 1 000 | 0.509 | 0.473 | 0.018 |
| 1e-4 | 1 000 | 0.493 | 0.489 | 0.018 |
| 1e-3 | 10⁶ | 0.921 | 0.079 | 0.0002 |
| 1e-5 | 10⁶ | 0.505 | 0.494 | 0.0006 |
| 0 | 10⁶ | 0.4997 | 0.4997 | 0.0006 |

Median P_correct at M = 1024 over random θ: parity 1.000 / 0.843 / 0.592 / 0.517 / 0.498 / 0.493 / 0.492
at n = 4…16 (it tends to (1 − P_zero)/2 = 0.491, a coin flip given a non-zero estimate). Projector:
0.999 / 0.596 / 0.095 / 0.0065 / 0.0004 / 2e-5 / 1e-6. The projector's P_correct goes to **0**, not
to ½, because its missing probability mass is almost entirely the exact-zero event, not wrong signs.

**Operational terminology (project-specific, not established literature terms).** A *finite-shot
gradient dead zone* (Stage 5) is where the estimator is usually exactly zero. A *directional ambiguity
region* (introduced here) is where, for component k, `P_correct(θ, M, k) ≤ q`, with q ∈ {0.55, 0.60, 0.75}. There
the estimator usually moves, but its direction is statistically unreliable.

**Normal approximation.** With D = K₊ − K₋, E[D] = M sB and Var D = M[p₊(1−p₊) + p₋(1−p₋)], so
|E D|/sd(D) is exactly the component SNR. Φ(SNR) overestimates P_correct by up to 0.070 at M = 16 (it
ignores the tie mass). The continuity-corrected Φ((|E D| − ½)/sd) is within 1.5e-3 at every tested
(sB, M) (`normal_approximation` in the theory JSON). The approximation is used only where exact evaluation is
expensive (§11).

## 10. Component SNR
Parity: `SNR² = 2M(sB)²/(1 − (sB)²)`. Projector (Stage 5): `SNR² = M A s²/(1 − A(1+s²)/2)`, i.e. ≈ M A s².
The per-shot noise differs by a factor of order 1/A. It is O(1) for parity and O(A) for the projector.
Because of that, the projector's exponentially smaller |g| is partly compensated by its exponentially smaller noise,
and the two benchmarks end up needing nearly the same number of shots (§11) despite medians of |g| that differ by about 5.5
decades at n = 20 (10^−6.16 vs 10^−11.72).

## 11. Typical required-shot scaling (`projector_parity_comparison.csv`, `scaling_fits.json`)
100 000 θ per n, n = 2…20, k = 0. Median log₁₀ M [IQR]:

| n | parity SNR≥1 | parity P_c≥0.75 | parity P_c≥0.90 | projector SNR≥1 | projector P_c≥0.75 | projector P_c≥0.90 |
|---|---|---|---|---|---|---|
| 2 | 0.54 [−0.15, 1.38] | 0.60 [0.30, 1.26] | 0.95 | 0.73 [0.02, 1.61] | 0.85 [0.30, 1.58] | 1.11 |
| 6 | 2.99 [1.89, 4.39] | 2.69 [1.67, 4.05] | 3.22 | 3.30 [2.19, 4.69] | 3.29 [2.21, 4.65] | 3.61 |
| 10 | 5.41 [3.91, 7.18] | 5.07 [3.58, 6.84] | 5.63 | 5.72 [4.21, 7.49] | 5.71 [4.23, 7.46] | 6.03 |
| 14 | 7.82 [6.01, 9.89] | 7.47 [5.66, 9.55] | 8.03 | 8.12 [6.32, 10.22] | 8.11 [6.34, 10.19] | 8.44 |
| 20 | 11.41 [9.22, 13.88] | 11.07 [8.88, 13.54] | 11.62 | 11.71 [9.51, 14.22] | 11.71 [9.52, 14.19] | 12.03 |

(q90 at n = 20: parity 16.0 (P_c≥0.75) and projector 16.7, i.e. heavy upper tails on both.)

Median fits `log₁₀ M = a + b n` (10 points, slope not forced):

| statistic | parity slope | R² | projector slope | R² |
|---|---|---|---|---|
| SNR ≥ 1 | 0.6026 | 0.99998 | 0.6056 | 0.99986 |
| SNR ≥ 2 | 0.6026 | 0.99998 | 0.6056 | 0.99986 |
| P_correct ≥ 0.75 | 0.5877 | 0.99953 | 0.6025 | 0.99998 |
| P_correct ≥ 0.90 | 0.5958 | 0.99992 | 0.6040 | 0.99994 |

The reference is log₁₀ 4 = 0.6021. **Both benchmarks need ≈ 4ⁿ shots for reliable gradient information.**
The parity P_c ≥ 0.75 slope is slightly lower because the integer floor M ≥ 1 raises its small-n points. At n = 2 about 10^0.6 = 4
shots already suffice for many θ.

**Methods and their measured error.**
- **SNR targets:** closed form for both benchmarks.
- **Parity direction targets:** exact. The requirement depends on θ only through |sB|, so it is solved by
  exact integer bisection on a 3 000-point grid of log₁₀|sB| ∈ [−2.5, 0) (M up to ≈ 2×10⁴). Each sample takes
  the grid value at or just below its |sB|, which is a guaranteed upper bound, off by at most one integer step. A cross-check
  against per-sample exact bisection found overshoot ≤ 0.058 decades and never undershoot. That covers 99% of samples at n = 2 and 0.7% at
  n = 20. Beyond the grid, the normal inversion is used. At the grid edge (M ≈ 10⁴) its error is ≤ 0.011 decades (P_c ≥ 0.75)
  and ≤ 0.003 decades (0.90), shrinking with M. At small M the normal inversion is badly wrong (median 0.09 decades, up to 1.0),
  which is why it is not used there.
- **Projector direction targets:** exact integer bisection for every sample, with a per-sample bracket
  around z_q²/(A s²), widened automatically on failure. All rows converge (reached fraction 1.000). The 0.4–0.8% of
  samples with |s| ≲ 0.02 (M·A > 10⁴) use the Skellam/normal limit. A subsample check of Skellam vs exact
  gives a maximum difference of ≤ 0.004 decades for n ≥ 12 (up to 0.30 decades at n = 2, where p is not small).

## 12. Matched-signal comparison (`matched_signal_analysis.csv`)
The two objectives have different gradient distributions, so differences are compared at **matched
|g_true|**. θ from both benchmarks is pooled over n ∈ {4,…,16} (20 000 per n), binned by log₁₀|g| (0.5-wide
shared bins, 19 bins from −9.25 to −0.25). A bin is reported only if both benchmarks have ≥ 200 samples in it.

| log₁₀\|g\| | M | parity P_zero | proj. P_zero | parity P_correct | proj. P_correct | parity sd(ĝ) | proj. sd(ĝ) |
|---|---|---|---|---|---|---|---|
| −5.25 | 1024 | 0.018 | 0.960 | 0.491 | 0.026 | 1.1e-2 | 8.7e-5 |
| −4.25 | 1024 | 0.018 | 0.780 | 0.493 | 0.162 | 1.1e-2 | 2.7e-4 |
| −3.25 | 1024 | 0.018 | 0.250 | 0.513 | 0.653 | 1.1e-2 | 8.3e-4 |
| −3.25 | 16384 | 0.004 | 0.002 | 0.584 | 0.983 | 2.8e-3 | 2.1e-4 |
| −2.25 | 1024 | 0.015 | 0.005 | 0.695 | 0.978 | 1.1e-2 | 2.4e-3 |

**The mechanism difference persists at matched |g|.** At every |g| and M, parity's P_zero is at its
zero-signal floor, while the projector's goes from ≈ 1 to ≈ 0 as |g| grows. The shifted
probabilities show why. Parity's are ≈ ½ in every bin. The projector's are ≈ A, tracking |g| (from 5e-9 to 0.39 across the bins).

**But the ranking reverses.** At the same |g|, once the projector escapes its dead zone it gets the sign
right *more* often than parity (e.g. log₁₀|g| = −3.25, M = 16384: 0.983 vs 0.584). Its conditional
noise is 10–100× smaller. So neither benchmark is simply harder at matched gradient. They fail
differently: the projector by withholding information (zeros), parity by diluting it (noise of O(1) per shot).

## 13. Vector directional reliability (`vector_reliability.csv`)
Full gradients with an independent batch per (k, ±), 300 θ × 20 repetitions per (n, M). All quantities are measured
directly, with no independence assumed across components. A zero estimate counts as cos = 0 in the all-draws columns.

| n | M | proj. P(ĝ=0) | proj. median cos (all / nonzero) | proj. P(ĝ·g>0) | parity P(ĝ=0) | parity median cos | parity P(ĝ·g>0) |
|---|---|---|---|---|---|---|---|
| 8 | 1024 | 0.312 | 0.68 / 0.93 | 0.59 | 0 | 0.73 | 0.88 |
| 10 | 1024 | 0.522 | 0 / 0.78 | 0.39 | 0 | 0.39 | 0.77 |
| 12 | 64 | 0.929 | 0 / 0.41 | 0.06 | 0 | 0.07 | 0.58 |
| 12 | 1024 | 0.784 | 0 / 0.71 | 0.17 | 0 | 0.18 | 0.69 |
| 12 | 16384 | 0.563 | 0 / 0.80 | 0.35 | 0 | 0.38 | 0.80 |

**Projector:** often there is no vector at all, but when there is one it is well aligned. **Parity:** there is always a
vector, and it becomes nearly orthogonal to the true gradient (median cos 0.07–0.18 at n = 12, M ≤ 1024), though it is still a descent direction somewhat
more often than not.

## 14. Information-distance interpretation (`information_distance.csv`)
Per-shot distances between Bernoulli(p_pos) and Bernoulli(p_neg), median over 20 000 θ:

| n | parity 1/H² | projector 1/H² | parity 1/TV² | projector 1/TV² |
|---|---|---|---|---|
| 4 | 2.4e2 | 4.1e2 | 1.2e2 | 4.3e3 |
| 10 | 1.0e6 | 1.6e6 | 5.0e5 | 6.5e10 |
| 16 | 4.1e9 | 6.0e9 | 2.1e9 | 9.1e17 |
| 20 | 1.0e12 | 1.8e12 | 5.2e11 | 6.8e22 |

The squared Hellinger distance, which sets the sample complexity of telling the two shifted distributions apart,
shrinks at essentially the same exponential rate for both benchmarks (≈ 4ⁿ), matching §11. Total
variation does not track sample complexity when p ≈ 0 (TV² ≪ H² there), which is why the projector's 1/TV²
looks exponentially worse. This is a concrete estimator-level specialization consistent with the
outcome-probability distinguishability framework of Aghaei Saem et al. **It is not a replacement for that
framework** and adds nothing to its general statements.

## 15. Projector failure mode
**Count starvation / exact-zero quantization.** Both shifted probabilities are O(A) ≈ 4^{−(n−1)}. Up to
M ~ 1/A, both counts are usually 0 and ĝ ≡ 0. Fixed-shot failure fractions (`failure_fraction.csv`, 20 000 θ): the fraction
with P_zero ≥ 0.9 reaches 0.9995 (M=16), 0.976 (M=1024) and 0.915 (M=16384) at n = 16. When the estimator is non-zero,
it is informative (§12, §13).

## 16. Parity failure mode
**Directional ambiguity / sign loss.** Both shifted probabilities are ≈ ½, and the per-shot noise is O(1)
while the signal is ≈ 2^{−(n+1)}. The estimator is non-zero with probability 1 − 1/√(πM) at every n, but its sign becomes a coin flip. The fraction with
P_zero ≥ 0.9 is **0** in all 42 (n, M) cells. The fraction with P_correct ≤ 0.60 reaches 0.9998 (M=16), 0.975 (M=1024)
and 0.913 (M=16384) at n = 16.

`figures/mechanism_map.png` classifies each (n, M) by majority of initializations (2 = ≥ 50% of θ have
P_zero ≥ 0.9; else 1 = ≥ 50% have P_correct ≤ 0.60; else 0). The projector is count-starved in 27 of 42
cells: every tested M for n ≥ 12, M ≤ 4096 at n = 10, M ≤ 256 at n = 8, and M = 16 at n = 6. Parity is
count-starved in 0 of 42. It is directionally ambiguous in 30 of 42: every tested M for n ≥ 10,
M ≤ 1024 at n = 8, and M ≤ 64 at n = 6.

## 17. What both share
- An exponential barren plateau in the exact gradient (verified; not structural zeros).
- An exponential shot requirement for reliable gradient information: median ≈ 4ⁿ for both SNR and sign
  targets, with nearly identical constants (§11). Squared Hellinger distance shrinks at the same rate (§14).
- The same estimator algebra: a difference of two independent binomial counts.

## 18. What differs
- The failure *distribution*. Projector: P_zero → 1, and P_correct → 0 through zeros. Parity: P_zero ≈ 1/√(πM)
  for all n, and P_correct → (1 − P_zero)/2 ≈ ½ through random signs.
- This persists at matched |g| (§12), so it is not merely a signal-magnitude effect. It follows from where the
  two Bernoulli parameters sit (near 0 vs near ½).
- Vector level: "no vector" vs "a vector nearly orthogonal to the gradient" (§13).
- Optimization diagnostic (Task 17, §22): identical fixed-η GD from **paired** start points, 20 seeds,
  300 iterations. At n = 10 the projector finite-shot runs take an exactly-zero step 60–87% of the time and stay at C ≈ 1, as does
  exact GD. Parity finite-shot runs never take a zero step (mean cos with the exact gradient 0.19–0.33) and still reach
  C ≈ 10⁻⁴–3×10⁻³, as exact GD does (C → 0). **Caveat: the parity landscape has 2^{n−1} global minima
  (θ_j ∈ {0, π} with an even number of π's), the projector only one, and parity's typical |g| is
  exponentially larger (2^{−(n+1)} vs 4^{−n}).** The optimization contrast is therefore a landscape difference
  as much as a measurement one, and it is not evidence that directional ambiguity is benign.

## 19. What is already known
Exponential measurement burden on barren plateaus (Wang et al. 2021; Larocca et al. 2025; Qin 2026);
concentration of outcome probabilities and statistical indistinguishability under finite budgets,
including a single-layer X-rotation circuit with a global Pauli-Z observable (Aghaei Saem et al. 2026);
global vs local cost dependence (Cerezo et al. 2021).

### Relationship to Aghaei Saem et al. (2026)
Their work develops a general framework for exponential concentration at the level of POVM outcome
probabilities and for statistical indistinguishability under finite measurement budgets. Their numerical work
includes a single-layer X-rotation circuit with a global Pauli-Z observable, essentially this stage's
parity benchmark. Stage 6 therefore does **not** claim that outcome-probability concentration is new,
that finite-shot failure of a global Pauli cost is new, or that exponential measurement burden is new. Our
narrower question is whether two analytically controlled barren plateaus with different outcome
structures show *distinct finite-shot gradient-estimator failure modes*: count starvation / exact-zero
quantization vs directional ambiguity / sign loss. We have not checked their paper in detail
for an equivalent estimator-level decomposition. That comparison is required before any novelty claim.

## 20. Candidate contribution (if it survives the literature check)
An exact, estimator-level decomposition of finite-shot parameter-shift failure into P_zero / P_correct /
P_wrong for two analytically controlled barren plateaus. It shows that equal ≈ 4ⁿ shot complexity can
come with qualitatively different estimator distributions (count starvation vs sign loss), that the
difference persists at matched gradient magnitude, and that it is fixed by where the shifted outcome
probabilities sit (near 0 vs near ½). Within that, the zero-signal central-binomial floor P_zero → C(2M,M)/4^M
≈ 1/√(πM) marks the parity case.

## 21. Novelty status
**UNCONFIRMED.** No dedicated literature review has been done. Aghaei Saem et al. (2026) is the closest
known work and may already contain an equivalent decomposition.

## 22. Limitations
- Two benchmarks, one circuit family (product RX), one initialization distribution (U[−π, π]), k = 0 for
  the scaling statistics, one independent batch per (k, ±). No correlated/shared-sample estimators, SPSA,
  adaptive shot schedules or hardware noise.
- The matched-signal analysis pools n ∈ {4,…,16}, so bins mix circuits of different n (within a bin the
  projector's p values still track |g|; parity's are ½ throughout).
- Parity direction shots beyond |sB| < 10^{−2.5} use the normal inversion (error ≤ 0.011 decades, measured).
  About 0.4–0.8% of projector samples use the Skellam/normal limit.
- The Task 17 diagnostic is 20 seeds, 300 iterations, untuned η = 0.3. It is not an optimizer study, and the landscapes
  differ (§18).
- A first, **unpaired** version of that diagnostic (start points drawn from a seed that included M)
  appeared to show finite shots *beating* exact GD. With paired start points this disappears (parity: finite
  shots end above exact GD on 18–20/20 seeds). The shipped code pairs them. Recorded here so the artifact is not
  rediscovered as a finding.

## 23. Recommended Stage 7
1. **Literature check first:** compare §12–§16 against Aghaei Saem et al. (2026) and the
   finite-shot SPSA analysis of Qin (2026) before any further claims.
2. **Remove the landscape confound:** a parity-like observable with a *single* global minimum, or the
   projector measured in a rotated basis that moves its outcome probabilities toward ½, so that the outcome
   location changes while the landscape does not.
3. **Shared-sample / correlated estimators:** whether off-diagonal covariance changes which failure mode
   dominates.

## Outcome classification (Task 24)
**CASE A, with a qualification (partly CASE E).**
- Projector P_zero → 1 (median 0.999998 at n = 16, M = 1024). Parity P_zero stays at 1/√(πM) (0.0176). ✔
- Parity P_correct → ≈ random (0.492 at n = 16, where the ceiling is 0.491 once ties are removed). ✔
- Both require exponentially growing shots: median slopes 0.588–0.606 vs log₁₀ 4 = 0.602. ✔
- Matched |g|: the difference persists, so this is not CASE C. Parity is never directionally reliable at polynomial M, so this is not CASE D.
- Qualification (E): at matched |g| the projector is *more* directionally reliable than parity once it
  escapes the dead zone. Which failure mode is "worse" depends on |g| and M. The claim is "distinct
  failure modes", not that one benchmark is uniformly harder.

## Validation summary (engineering)
- `pytest`: 166 passed (146 Stage 1–5 + 20 Stage 6), run with `-W error::DeprecationWarning`.
- Identities ≤ 6.1e-11. The exact difference-of-binomials code matches brute force to 4.5e-14 at small M and matches
  scipy double sums to ≤ 4e-11 up to M = 10⁸. The central-binomial identity holds to 4e-9 at M = 10⁶.
- Bugs found and fixed during Stage 6, before any result was recorded:
  1. `binom_cdf` evaluated I_{1−p}; for p ≲ 1e-16, `1 − p` rounds to 1 and returned CDF = 1, collapsing
     projector probabilities at M ≳ 10¹⁹. It now uses the complemented incomplete beta in p, with a regression test.
  2. Required-shot bisection evaluated the float-M binomial formula *between* integers. It now evaluates only integer
     budgets.
  3. Projector bisection over a global [1, 10³⁰] bracket built summation windows of ~4×10⁸ entries and exhausted memory.
     It now uses per-sample brackets.
  4. Parity direction targets originally used normal inversion everywhere; they are now exact where the approximation
     is poor.
  5. The variance-check z-score assumed Gaussian kurtosis; it now uses the exact 4th moment.
  6. The Task 17 start points were unpaired; they are now paired.
- Stage 3–5 code is unmodified.

## Re-run
```
.venv/bin/python -m pytest -v -W error::DeprecationWarning
.venv/bin/python -m qlo.experiments.stage6 --workers 5      # -> results/stage6/, ~6 min, ~2.2 GB peak
.venv/bin/python -m qlo.experiments.stage6 --fast            # smoke run
```
`--workers` changes wall time only. Every per-(benchmark, n) solve is seeded by (n, seed).
