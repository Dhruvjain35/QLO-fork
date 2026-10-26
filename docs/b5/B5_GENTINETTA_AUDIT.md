# B5 follow-up: audit of Gentinetta et al. 2024

**Source.** G. Gentinetta, A. Thomsen, D. Sutter, S. Woerner, *The complexity of quantum support vector machines*,
Quantum **8**, 1225 (2024), doi:10.22331/q-2024-01-11-1225. CC BY 4.0.

**Version reviewed.** The published Quantum PDF is primary (30 pp.; footer "Accepted in Quantum 2023-12-25";
published 2024-01-11).
- It is the arXiv:2203.00031v2 file (margin stamp "arXiv:2203.00031v2 [quant-ph] 7 Jan 2024"; arXiv comment "v2:
  published version").
- All pages were read, including Appendices A–C (pp. 21–30), and the v2 LaTeX source (`main.tex`) was searched.
- The code/data archive (Zenodo, ref. [29]) was not reviewed. arXiv v1 (2022-02-28) was not compared.
- Evidence ids E-01 … E-NL06 refer to [`B5_EVIDENCE_LEDGER.md`](B5_EVIDENCE_LEDGER.md).

**Notation clash.** In this paper **M is the training-set size**, and **R is the number of shots** per kernel entry or
per expectation value. In Stage 7, M is the number of shots per shifted circuit. Every M below is the paper's
data-set size unless marked "Stage 7 M".

## 1. Estimator

- **Kernel entries (QSVM, dual and primal)**: k(x_i, x_j) = |⟨ψ(x_i)|ψ(x_j)⟩|² (Eq. 6, p. 6), estimated by an inversion
  (Loschmidt-type) test (Fig. 1, p. 7; E-02).
  - Prepare E(x_j)†E(x_i)|0⟩^⊗q and measure every qubit in the computational basis.
  - k_R = (1/R) Σ_l k̂^(l), where k̂^(l) = 1 if the all-zero string is observed and 0 otherwise (Eq. 9, p. 8).
- **Approximate QSVM** (a variational model): h_θ(x) = ⟨ψ(x)|W(θ)†Z^⊗q W(θ)|ψ(x)⟩ ∈ [−1, 1], a global observable (p. 8), and
  c_θ(x) = sign[h_θ(x) + b] (Eqs. 7–8, p. 7; Fig. 2).
  - Each ±1 outcome Q is used through (1 + Q)/2 ~ Bernoulli(p) (§4.4, p. 14; E-05).
- **No SWAP-test estimator appears.** Neither "SWAP" nor "Loschmidt" occurs in the paper or its LaTeX source. The
  all-zero-frequency test is the paper's only kernel readout.

## 2. Statistical model

- **Kernel entries.**
  - i.i.d. Bernoulli shots with mean k_ij (App. A.1, Eq. 20, p. 21).
  - E[(E_R)_ij] = 0 (Eq. 22) and E[|(E_R)_ij|²] = (1/R²)[R k_ij + 2·C(R,2) k_ij²] − k_ij² ≤ k_ij/R = O(1/R) (Eq. 24,
    p. 22). The middle expression simplifies to k_ij(1 − k_ij)/R (our algebra), the Loschmidt per-shot variance divided
    by R.
  - Fourth moment O(1/R²) (Eq. 25).
- **Kernel matrix.** Latała's theorem gives E‖K_R − K‖₂ = O(√(M/R)) (Eqs. 26–27, p. 23; Eq. 10, p. 9).
- **Numerics.** Noisy entries are drawn from the binomial distribution B(R, K_ij) with R = 10⁹–10¹⁹ (§4.2, p. 12;
  footnotes 6–7). R is chosen very large so that ‖K − K_R‖ < μ holds (Theorem 4).
- **Approximate QSVM.**
  - σ_Q² = 4σ²_Bernoulli = 4p(1 − p) ≤ 1, so the standard deviation of the sample mean is σ_Q/√R.
  - R = O(1/ε²) shots per expectation value give an O(ε) confidence interval (pp. 14–15).
- **No gradient-estimator statistics.** No law, variance, zero probability or sign probability of a gradient estimator
  is derived.

## 3. Shot complexity

| Approach | Analytical | Empirical | Variable | Locator |
|---|---|---|---|---|
| Dual (QP on the full kernel matrix) | R = O(M^(8/3)/ε²) per entry; R_tot = O(M^4.67/ε²) | R_tot = O(M^(4.8±0.4)/ε²) (separable), O(M^(4.5±0.3)/ε²) (overlapping); R ≈ ε^(−2) (fits −1.989 to −1.998) | M (data size), ε (decision-function error) | Eq. (11), p. 9; Lemma 5, Eq. (37), pp. 24–26; Figs. 5–6, Tab. 2 (E-03) |
| Primal (kernelised Pegasos, SGD) | R_tot = O(min{M²/(λ³ε⁶), 1/(λ⁵ε¹⁰)}) under Assumption 2 | O(1/ε^(8.3±1.6)) (separable), O(1/ε^(9.5±1.0)) (overlapping) | ε, M | §3.2, Eqs. (12)–(14), pp. 9–10; Figs. 7–9; App. B (E-04) |
| Approximate QSVM (variational, SPSA) | R_tot = O(1/ε³) conjectured (Eq. 18) | O(1/ε^(2.9±0.3)), O(1/ε^(2.8±0.3)) from 2-dimensional data (8 parameters); ≈ 2.2 for 8-dimensional data (16 parameters) | ε at two fixed sizes | §4.4, pp. 14–17; Figs. 10–11 (E-05) |

- All complexities are **polynomial** in M and ε, at fixed problem sizes (8 qubits for the kernel experiments; 2- and
  8-dimensional data for the approximate QSVM).
- **No n-dependence is stated.** Exponential concentration is explicitly assumed away: Assumption 1 (noisy halfspace
  learning) and the remark that the feature map "has been chosen reasonably" (p. 2; E-01).

## 4. Do Loschmidt or SWAP readouts appear?

- **Loschmidt-type: yes, at the kernel level.** The all-zero-outcome inversion test (Fig. 1) is the Loschmidt readout of
  Stages 5–7, applied to a data-dependent fidelity rather than to a trainable-parameter landscape.
  - The paper writes its Bernoulli variance (Eq. 24) but does not call it a Loschmidt echo.
  - It does not discuss its collapse under concentration (rows 2, 14a: E-NL02).
- **SWAP: no.** Searches for SWAP, swap test, Loschmidt, echo, projector, POVM, readout and measurement scheme returned
  nothing relevant (E-NL02).
- Consequently no comparison of two readouts of one quantity exists (row 4 is RELATED BUT DIFFERENT through E-02:
  one readout's variance only).

## 5. Do parameter-shift gradients appear?

- **No.** "Parameter shift", "finite difference" and "mean squared error" do not occur.
- The gradient-type objects are:
  - **Pegasos sub-gradients** (§2.2, pp. 5–6). These are computed classically, on the weight vector w, from estimated
    kernel values; they are not gradients with respect to circuit parameters.
  - **SPSA estimates** for the approximate QSVM (§4.4, p. 16). The paper chooses SPSA "which ensures that the scaling is
    independent of d" (d = number of trainable parameters), combined with SGD over batches of 5 data points.
  - **Full gradient descent with a statevector simulator** (R → ∞) for the noiseless reference θ_∞ (p. 16). How the
    gradient is computed is not stated (expectation values are exact); no estimator is analysed.

## 6. Does training involve variational parameters?

- **Dual and primal QSVM: no.** The quantum circuit only evaluates kernel entries. Training is a convex optimisation
  over classical variables: α in the quadratic program (29), or Pegasos's integer coefficients (Algorithm 1).
- **Approximate QSVM: yes.** θ ∈ ℝ^d of a RealAmplitudes circuit W(θ) and a bias b (Eqs. 7–8; §4.4). This is the only
  variational part, and it is trained with SPSA, not parameter shift (E-05).

## 7. Is the kernel estimator just an input to a classical optimisation?

**Yes, for the dual and primal QSVM.**
- The kernel matrix K_R (dual) or individual kernel values k_R (Pegasos, line 14 of Algorithm 1) are estimated on the
  quantum device. They are then consumed by a classical QP solver (`quadprog`) or by classical sub-gradient updates.
- Shot noise reaches the decision function only through these classical inputs, analysed by perturbation bounds:
  Daniel's theorem for QPs (Theorem 4) and Assumption 2 for Pegasos.
- The prediction step also needs kernel estimates, but it is O(S²/ε²) and subdominant (p. 7).

## 8. Kernel training complexity vs VQA parameter-shift gradient complexity

These are different quantities and must not be compared numerically.

| Aspect | Gentinetta 2024 (dual QSVM) | Stage 7 |
|---|---|---|
| What is estimated | Kernel values k(x_i, x_j) (fidelities between data-encoded states) | Shifted fidelities F± at trainable parameters, combined into ĝ |
| Error measure | max_x \|h_R(x) − h(x)\| (decision function) via E‖K_R − K‖₂ | Per-θ SNR or sign reliability of one gradient component |
| Scaling variable | Data size M and accuracy ε at fixed n | Number of qubits n |
| Concentration | Assumed absent (Assumption 1) | Present (barren plateau; log-typical A = 4^(−(n−1))) |
| Readout | All-zero frequency only | Loschmidt vs SWAP |
| Result form | Polynomial: O(M^4.67/ε²) | Exponential: median ≈ 4ⁿ vs ≈ 16ⁿ |

The only shared ingredient is the Loschmidt-type Bernoulli fidelity estimate and its variance k(1−k)/R. That puts
Gentinetta beside Aghaei Saem (B-10a) as a source for the Loschmidt per-shot variance at the fidelity level (E-02).

## 9. Candidate status from this paper

- **C1:**
  - RELATED BUT DIFFERENT: the single-entry binomial law and the Bernoulli variance at the fidelity level (E-02).
  - NOT LOCATED at the gradient level (E-NL09).
- **C2:** not located (E-NL13).
- **C3:**
  - RELATED BUT DIFFERENT: kernel training complexity (E-03, E-04) and SPSA training complexity (E-05).
  - NOT LOCATED: any n-exponent, readout comparison or 4ⁿ/16ⁿ (E-NL02).
  - The exponential-measurement statement for concentrated kernels is EXPLICIT, as background attributed to Thanasilp
    et al. (E-01).
- **C4:**
  - RELATED BUT DIFFERENT: the noiseless reference optimisation warm-started from the noisy endpoint θ_R (E-06). It is
    not a matched start and has no signal-free control.
  - NOT LOCATED: random walk and vector metrics (E-NL08).

- **Context row 28** (global-Z parity training numerics): RELATED BUT DIFFERENT (E-05). The global Z^⊗q observable is
  trained with finite shots, but with SPSA on ZZFeatureMap + RealAmplitudes circuits, not with parameter shift on a
  single rotation layer.

`NOT LOCATED` means only: not found in the reviewed version after the logged searches. This audit is evidence for A1
and does not make the novelty decision.
