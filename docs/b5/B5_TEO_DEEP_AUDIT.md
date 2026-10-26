# B5 follow-up: deep audit of Teo 2023

**Source.** Y. S. Teo, *Optimized numerical gradient and Hessian estimation for variational quantum algorithms*,
Phys. Rev. A **107**, 042421 (2023), doi:10.1103/PhysRevA.107.042421.

**Version reviewed.** arXiv:2206.12643**v3** (2022-11-20, 24 pp., journal-ref Phys. Rev. A 107, 042421 (2023)). Read in
full:
- every page viewed, including Appendices A–D and Tables I–II;
- the LaTeX source read for Secs. II–VII and Apps. A–C;
- v1 (2022-06-25) and v2 (2022-06-28) compared structurally.

The APS version of record (published 2023-04-17) was **not inspected**: the DOI resolves to link.aps.org, which
returned an HTTP 403 challenge page (not bypassed), and the published version is not open access. **Every locator below
is an arXiv v3 locator.** Published page and equation numbers are unverified (`B5_VERSION_GAP.md` §3).

**Version history.**
- The v3 arXiv comment lists an updated Fig. 4, an added Fig. 6, and added Secs. IV C, V C, VII and App. C 5.
- Compared with v1/v2: SPS, the §VII "potential pitfall" (D_θ0, wrong update directions) and the "random guesses"
  wording of the conclusion are present only in v3.
- The PS MSE and the critical copy number N_* are present in v1/v2, under different section numbers.

**Conventions.**
- Evidence ids D-01 … D-NL27 refer to [`B5_EVIDENCE_LEDGER.md`](B5_EVIDENCE_LEDGER.md).
- Statements marked *(our algebra)* are derived in this audit. They are not in the source and carry no novelty label.
- Stage 7 notation: F± = A(1∓s)/2, g = As/2, M shots per shifted circuit, independent batches. In Teo's formulas s
  is his shift angle (Eq. 11); in Stage 7 expressions s = sin θ_k.

## 1. Setup

- **Model function** (Eq. 1, p. 2): f_Q(θ; x) = ⟨0|U†_{θ;x} O U_{θ;x}|0⟩.
  - U = ∏_l V_l(x) W_l(θ_l), with trainable modules W_l and non-trainable encodings V_l.
  - The VQA loop is sketched in Fig. 1.
- **PEPQCs** (Pauli-encoded parametrized quantum circuits, p. 3).
  - Every trainable parameter enters through a single-qubit Pauli rotation; entanglement comes from CNOTs (Fig. 2).
  - Hence σ² = 1 for every generator, and the translation identity f(θ + θ₀) = f + sin θ₀ ∂f + (1 − cos θ₀)∂²f holds
    (Eq. A7, p. 13).
- **Observable** (p. 3): O = Σ_k h_k O_k/‖h‖, a weighted sum of multiqubit **Pauli** operators.
  - Eigenvalues are ±1, and the O_k are traceless (used in the Haar averages).
  - "Each O_k is sampled *independently*", each in its own eigenbasis (p. 3; ledger D-01).
- **Circuit ensemble.**
  - Trainable modules are treated as approximate unitary two-designs (hardware-efficient circuits of polynomial
    depth, p. 3, ref. [72]).
  - Exact results require the **two-design-sandwich (TDS) condition** (Case I of Fig. 7, p. 13): every module that
    carries a derivative sits between two two-design modules.
  - Cases II–VII give upper bounds through Tab. I (p. 18).
- **Numerics.**
  - ε_opt, finite-copy and approximation errors for n = 2–15 (Fig. 6) and GD studies for n ≤ 12 (Fig. 3).
  - Monte Carlo at d = 2⁸ for two tasks (Fig. 4): a supervised-learning task with observable Y ⊗ 1^(n−1), and a
    trace-subtracted 96-term water-molecule Hamiltonian (App. D, Tab. II).
  - 500 random PEPQCs × 500 experiments per point, at the initial optimisation step.

## 2. Estimators

All estimators are linear combinations of estimated function values from the same Pauli measurements.

| Estimator | Definition | Locator |
|---|---|---|
| Function | f̂ = Σ_k (h_k/‖h‖) Σ_l o_kl ν_kl, with ν_kl the multinomial relative frequencies | Eq. (4), p. 4; App. C 1, Eq. (C1), p. 19 |
| FD | [f(θ+ε/2) − f(θ−ε/2)]/ε = sinc(ε/2) ∂f | Eq. (5), p. 4 |
| GD (generalised difference) | Σ_j c_j FD^(jε), Σ c_j = 1 | Eqs. (9)–(10), p. 5; (A8)–(A11), p. 14 |
| PS | [f(θ+s) − f(θ−s)]/(2 sin s), exact for any s | Eq. (11), p. 5 |
| SPS (scaled PS, from ref. [61]) | λ·PS, 0 ≤ λ ≤ 1 | §IV C, Eq. (14), p. 6 |

- Hessian versions: Eqs. (6) and (12).
- Stage 7 uses only the unscaled PS estimator at s = π/2, with one independent batch per shifted circuit.

## 3. Error metric

- **MSE (Eq. 2, p. 3):** MSE(Y) = ⟨E[(Ŷ − Y)²]⟩, averaged three ways:
  - E over sampling;
  - ⟨·⟩ over the trainable-circuit ensemble (Haar averages);
  - the overline over the non-trainable inputs x.
- The text cautions that "the MSEs involve circuit averages of gradient and Hessian components" (p. 4).
- MSE(Y) = Σ_k h_k² MSE(Ŷ_k)/‖h‖², by independent sampling of the O_k, if the Ŷ_k are unbiased (p. 4).
- **Decomposition (Eq. 7, p. 4):** MSE = Δ²_copy + Δ²_ε, the finite-copy error plus the approximation (nonzero-ε)
  error; Δ²_ε = 0 for PS.
- **§VII (Eq. 26, p. 11):**
  D_θ0 = ⟨max{Var[f̂(θ ± θ0)]}/|f(θ+θ0) − f(θ−θ0)|²⟩, a circuit-averaged worst-case relative spread.
- **Statistic type.** Every result is a **circuit-averaged second moment** (or a ratio averaged over circuits).
  - None is a fixed-θ quantity, a distribution, a quantile or a typical (log-mean) value.
  - Stage 7 instead uses per-θ exact distributions and **medians over θ** (`B5_STATISTIC_COMPARISON.md`).

## 4. Shot convention

- **N** — the number of "clicks" (copies) recorded when measuring one function f_{Q,k} at fixed parameters (p. 4;
  App. C 1).
- **N_T** — the total number of copies "distributed equally to all sampled quantum-circuit functions" of one
  estimator **per circuit-observable basis operator** O_k (p. 4).
  - N_T = 2N for an FD gradient component; the convention is defined for FD (p. 4), and the PS/SPS formulas use it
    unchanged (Eq. 13 is consistent with an equal split; our check).
  - N_T = 3N for a diagonal and 4N for an off-diagonal Hessian component.
  - GD spreads N_T over 2J, 2J + 1 and 4J functions respectively (p. 5).
  - App. C 2 (p. 19) uses N_T = N for a single function estimate.
- For an observable with K Pauli terms the total is K·N_T per component, because each O_k is sampled independently.
- In §VII, the "N sampling copies" of D_θ0 are copies per shifted function.
- **Conversion to Stage 7.** Stage 7's M (shots per shifted circuit) ↔ Teo's N, and Stage 7's 2M per component ↔ Teo's
  N_T for K = 1. In Stage 7 units, Teo's PS MSE at s = π/2 is d/(2M(d+1)). Full table: `B5_SHOT_CONVENTIONS.md`.

## 5. BP scaling assumptions

- **Circuit averages (Tab. I, p. 18; App. B 2–B 4).** ⟨(∂f_{Q,k})²⟩ =
  - d²/(2(d+1)(d²−1)) for Case I;
  - ≤ d/(2(d²−1)) for Case II;
  - ≤ 1/(d+1) for Case III.
- Hessian components are similar; all are O(1/d), which the text calls "manifestations of the so-called barren-plateau
  phenomenon" (p. 6; D-10).
- ⟨f_{Q,k}²⟩ = 1/(d+1) for any shift (Eq. C3, p. 19; App. B 1, Eq. B14).
- **Statistic.** These are arithmetic means over Haar two-design modules. No typical (median or log-mean) values and no
  product (non-two-design) landscapes are treated.
- **Contrast with Stages 3–7** (product RX circuit, θ ~ U[−π, π]ⁿ):
  - Var_θ[∂_kC] = (1/8)(3/8)^(n−1) (Stage 3);
  - E_θF = 2^(−n);
  - E_θF² = (3/8)ⁿ;
  - log-typical A = 4^(−(n−1)) (Stage 5 Prop. 5).
- The product circuit has no entangling two-design modules, so **the TDS condition does not hold** for it. Teo's exact
  (Case I) expressions therefore do not apply to Stage 7's landscape as written.

## 6. Main theorems/formulas

Two-design (TDS) results unless noted. Gradient components only; Hessian analogues are in the same equations.

| Quantity | Formula (arXiv v3) | Locator |
|---|---|---|
| FD MSE | 4d/(N_T(d+1)ε²) + d²[1 − sinc(ε/2)]²/(2(d+1)(d²−1)) | Eq. (8), p. 5 |
| PS MSE | d/(N_T(d+1) sin² s) ≥ d/(N_T(d+1)), minimised at s = π/2 | Eq. (13), p. 5 |
| SPS MSE | dλ²/(N_T(d+1) sin² s) + d²(1−λ)²/(2(d+1)(d²−1)) | Eq. (14), p. 6 |
| Optimal FD step | ε_opt ≅ (2304(d²−1)/(N_T d))^(1/6) | Eq. (15), p. 6 |
| Optimal FD MSE | ≅ (3/32)^(1/3) d^(4/3)/((d+1)(d²−1)^(1/3) N_T^(2/3)), i.e. O(1/(N_T^(2/3) d^(1/3))) | Eq. (16), p. 6; Eq. (C10), p. 20 |
| Average squared estimates | FD → [sinc(ε_opt/2)]²/(2d) + 4/(N_T ε_opt²); PS → 1/(2d) + 1/N_T → 1/N_T | Eqs. (17)–(18), p. 6 |
| GD optimum and bounds | min_c c^T M c = (1^T M^(−1) 1)^(−1); Cauchy–Schwarz upper bounds | Eqs. (19)–(21), p. 7 |
| Optimal SPS factor | λ_opt = dN_T/(2d² + dN_T − 2) | Eq. (22), p. 8 |
| Optimal SPS MSE | d²/((d+1)(2d² + dN_T − 1)) as printed (see note) | Eq. (23), p. 8 |
| SPS beats PS | MSE_SPS,opt < MSE_PS for any d ≥ 2, N_T > 0 | p. 9; App. C 5, Eqs. (C17)–(C19), p. 22 |
| Critical copy number | N_* ≅ 32(d²−1)/(3d) | Eq. (24), p. 9; Fig. 5 |
| Relative spread | D_θ0 ≳ O(poly(d)/N) | Eq. (26), p. 11 |
| Function MSE | MSE(f) = (1/N_T)(1 − ⟨f²⟩) = d/(N_T(d+1)) | Eqs. (C2)–(C4), p. 19 |
| General cases | FD (C5)–(C9), GD (C11)–(C16), SPS (C17)–(C19) | App. C 3–C 5, pp. 19–22 |

**Observation (arithmetic check; no effect on Stage 7).** Minimising Eq. (14) at s = π/2 over λ gives exactly
Eq. (22)'s λ_opt. The minimum value is d²/((d+1)(2d² + dN_T − **2**)), the same value that the general-case
Eq. (C18) gives with the Case-I average. The gradient line of Eq. (23) is printed with "− 1", in both the PDF and the
LaTeX source (line 334). Checked numerically at (d, N_T) = (4, 10), (16, 100), (256, 2000). The difference is O(1/d²)
relative. The Hessian lines of Eq. (23) are consistent with Eq. (22). Whether the published version differs is
unverified.

## 7. Critical copy-number result

- **Statement.** N_* is the N_T at which an optimally tuned difference estimator (FD or GD) and PS have equal average
  MSE (p. 9). Under TDS and N_* ≫ d (Eq. 24, p. 9):
  - N_* ≅ 32(d²−1)/(3d) for gradient components;
  - N_* ≅ 81(d²−1)/(16d) for diagonal Hessian components;
  - N_* ≅ 9(d²−1)²/d³ for off-diagonal Hessian components.
- Eq. (25) gives loose lower bounds for GD. "In this regime, N_* ≳ O(2ⁿ)", and Fig. 5 (p. 10) shows N_* growing
  exponentially for n = 1–9 (D-06).
- The abstract states that "this critical number grows exponentially with the circuit-qubit number" (p. 1).
- **Meaning.** Below N_*, the optimised difference estimator has the smaller circuit-averaged MSE. It is a crossover
  between two estimators applied to the same Pauli measurements.
- It is **not** a threshold for resolving the gradient. *(Our algebra:)* at N_T = N_*,
  MSE_PS/⟨(∂f)²⟩ = [d/(N_*(d+1))]/[d²/(2(d+1)(d²−1))] = 2(d²−1)/(N_* d) = 3/16.
  So the crossover lies where PS already resolves the gradient in mean square. A mean-square resolution threshold for
  PS, MSE_PS ≤ ⟨(∂f)²⟩, is N_T ≥ 2(d²−1)/d ≈ 2d, a factor 16/3 below N_*.
- **In Stage 7 units** (N_T = 2M): M_* ≈ (16/3)·2ⁿ. Its base is 2, set by the two-design average ⟨(∂f)²⟩ ≈ 1/(2d).
  It cannot be compared with Stage 7's per-θ medians (4ⁿ, 16ⁿ).

## 8. Relation to Stage 5

Stage 5 analysed the Loschmidt (projector) parameter-shift gradient on the product landscape:
- the exact difference-of-binomials law and P₀ (Props. 2–3);
- the variance [A − A²(1+s²)/2]/(4M) and SNR (Prop. 4);
- the log-typical scale 4^(−(n−1)) (Prop. 5);
- median required-shot slopes ≈ 0.60 (§8);
- a term-wise local-cost control (§9).

Against Teo:
- **Overlap.** Both analyse finite-copy parameter-shift gradient estimators and their exponential copy demand. Stage 5
  §13 already treats "exponentially vanishing gradients impose exponential measurement-resolution costs" as known
  literature. Teo 2023 is an additional instance of that known territory and is not cited in STAGE5.md.
- **Different readout.**
  - Teo's per-shot variance is the ±1 (Pauli) variance 1 − f², which follows from (C1); Teo writes only its average,
    1 − ⟨f²⟩ (Eq. C2).
  - Stage 5's projector outcome is 0/1 with variance F(1 − F). Teo's model does not contain it (D-NL02).
  - Stage 5's local control, read out term by term through single-qubit projectors, does fit Teo's
    independent-Pauli-term model, since each single-qubit projector is (1 + Z_j)/2. That is a structural similarity, not a stated result.
- **Different statistic.** Teo uses circuit-averaged MSEs under TDS. Stage 5 uses exact per-θ laws and medians over θ.
- **Not in Teo:** P₀, the Poisson-limit I₀ form, the log-typical scale, the dead-zone fraction.
- **Not in Stage 5:** N_* (Stage 5 has no FD/GD/SPS estimators).

## 9. Relation to Stage 7

**Exact correspondence for the SWAP readout (our algebra; D-02, D-03b).**
- The SWAP-test ancilla Z is a ±1 observable with mean F. Teo's per-θ identity from (C1) gives
  Var[f̂] = (1 − f²)/N for it.
- Applied to the PS difference with s = π/2 and N = M per shift (N_T = 2M):
  - Var[PS(θ)] = [2 − f(θ+)² − f(θ−)²]/(4M);
  - with f = F± this is Stage 7's Var(ĝ_SWAP) = [2 − A²(1+s²)/2]/(4M), identical term by term.
- Checked numerically at three (A, s, M) points, with Monte Carlo agreement to sampling error.
- Teo's averaged form gives d/(2M(d+1)) ≈ 1/(2M). This is the deep-plateau value of Stage 7's SWAP variance, and
  Stage 7's measured SWAP noise sd ≈ 1/√(2M) is "independent of n" in Teo's sense.

**No correspondence for the Loschmidt readout.**
- Stage 7's Loschmidt shot is a 0/1 outcome of the global projector |0ⁿ⟩⟨0ⁿ|, with per-shot variance F(1 − F) ≈ F.
- Teo's framework assumes traceless Pauli observables, measured term by term. The projector is a sum of 2ⁿ Z-strings
  with weights 2^(−n). Under Teo's prescription (each O_k sampled independently) it would be estimated from 2ⁿ separate
  settings, a different estimator from the single-setting Bernoulli readout.
- *(Our algebra.)* The ±1 encoding O′ = 2Π − 1 reproduces the Loschmidt variance (1 − (2F − 1)²)/4 = F(1 − F), but O′ is
  neither a Pauli string nor traceless. It lies outside Teo's averaged results, and Teo does not consider it.
- **Structural reason (our algebra).** Under Teo's two-design averaging the traceless observable concentrates at the
  centre of its ±1 spectrum (⟨f²⟩ = 1/(d+1)), where the per-shot variance is maximal (≈ 1). That is the SWAP regime.
  The Loschmidt projector concentrates at the edge of its spectrum (F ≈ 0), where the per-shot variance is ≈ F. Teo's
  averaged numerator "O(1/N)" in D_θ0 (p. 11) is therefore the SWAP-type case.

**Required shots.** Full statistic comparison in `B5_STATISTIC_COMPARISON.md`; algebra in `B5_MATH_COMPARISON.md` §8.

| Criterion and ensemble | LE (projector) | SWAP / ±1 Pauli | Source |
|---|---|---|---|
| Teo's mean-square criterion, two-design average: MSE_PS ≤ ⟨(∂f)²⟩ | not in Teo's model | N_T ≥ 2(d²−1)/d, i.e. M ≈ 2ⁿ | implied by Eq. (13) + Tab. I (our algebra) |
| Same mean-square criterion on Stage 7's product landscape: E_θVar ≤ E_θg² | M = 2(4/3)^(n−1) − 3/2 → (4/3)ⁿ | M = 4(8/3)^(n−1) − 3/2 → (8/3)ⁿ | our algebra (variances from B-10a / D-03b) |
| Teo's D_θ0 (circuit average of variance/difference²) on Stage 7's landscape | diverges (E_θ[1/A] = ∞) | diverges (E_θ[1/A²] = ∞) | our algebra |
| Stage 7: per-θ SNR or sign target, **median over θ** | ≈ 4ⁿ (slopes 0.600–0.607) | ≈ 16ⁿ (slopes 1.197–1.203) | STAGE7.md §12 |

- **Divergence.** With θ_j ~ U[−π, π], E[sec²(θ_j/2)] = ∞. A sample check gave sample means of 1/cos²(θ/2) of
  1.7×10⁴, 6.7×10⁵ and 4.2×10⁶ for 10³, 10⁵ and 10⁷ samples, with the median ≈ 2.
- The same per-shot variance (Teo's ±1 model) therefore gives 2ⁿ, (8/3)ⁿ or 16ⁿ, depending on the ensemble and the
  statistic. Only the per-θ median with the log-typical A gives 16ⁿ.

**Other Stage 7 items.**
- Teo has no zero or sign probabilities, no conditional sign law, no vector metrics and no trajectories. §VII's
  "many wrong update directions" (p. 11) is a qualitative remark (D-08a).
- Teo's Eq. (18) (PS mean-square estimate → 1/N_T while ⟨(∂f)²⟩ ≈ 1/(2d)) is a circuit-averaged, component-wise
  analogue of Stage 7's SWAP norm inflation (D-04).

## 10. What overlaps explicitly

- **Finite-copy PS gradient errors, analysed analytically:** MSE_PS(∂f) = d/(N_T(d+1) sin² s) (Eq. 13). The second
  moment of the same estimator family as Stage 7, for Pauli (±1) readouts, averaged over two-design circuits (D-02).
- **PS errors do not shrink with n** at fixed copies: Eqs. (17)–(18) and the conclusion, p. 12 (D-04).
- **Exponential copy requirement for trainability,** base unspecified: D_θ0 ≳ O(poly(d)/N), "N must thus at least be
  exponentially large in n for trainability" (Eq. 26, p. 11; D-07a).
- **Noisy estimates can point the wrong way** even at small MSE: qualitative only (§VII, p. 11; D-08a).
- **Better estimation is not better trainability:** "These are clearly two separate problems" (p. 10; D-08b).
- **Two-design gradient concentration**, ⟨(∂f)²⟩ ≤ O(1/d) (Tab. I; D-10).

## 11. What is only implied

One item: Stage 7's SWAP gradient variance and its 16ⁿ median shot scaling (matrix row 16, D-03b, PARTIAL / IMPLIED).
The required write-out:

1. **Original equation.**
   - Per-θ multinomial identities, Eq. (C1) (p. 19), for a ±1 observable: E[ν] = p and the second moments.
   - Their circuit average, Eq. (C2): MSE(f) = (1/N_T)(1 − ⟨f²⟩).
   - Its two-design PS form, Eq. (13): MSE_PS(∂f) = d/(N_T(d+1) sin² s).
2. **Ensemble and assumptions in the source.**
   - Two-design trainable modules (TDS).
   - Traceless Pauli observable measured in its eigenbasis.
   - Independent multinomial sampling, copies split equally between the shifted circuits.
   - Average over circuits, sampling and inputs.
3. **Statistic.** Circuit-averaged MSE, a mean of a second moment. For D_θ0 it is the circuit average of a
   variance-to-squared-difference ratio. Neither is a median, quantile or typical value.
4. **Extra algebra** (our algebra, not in the source).
   - (a) Use (C1) at fixed θ, without the circuit average: Var[f̂(θ)] = (1 − f(θ)²)/N.
   - (b) PS difference at s = π/2 with N per shift: Var[PS] = [2 − f₊² − f₋²]/(4N).
   - (c) Set f = F± (SWAP-test ancilla Z) and N = M.
   - (d) Insert the shift identities F₊ + F₋ = A and F₊² + F₋² = A²(1+s²)/2 (Stage 5 Prop. 1):
     Var = [2 − A²(1+s²)/2]/(4M).
   - (e) SNR² = MA²s²/[2 − A²(1+s²)/2], so M_SNR ≈ 2ρ²/(A²s²).
   - (f) For sign targets, use exact difference-of-binomial inversion (Stage 6/7). This is not derivable from moments.
5. **Extra Stage 7-specific assumptions.**
   - The product RX landscape F = ∏cos²(θ_j/2), which is not a two-design, so TDS fails.
   - The SWAP test as the readout.
   - Independent batches per (k, ±).
   - A per-θ target (SNR ≥ ρ or P_correct ≥ q) instead of a circuit-averaged MSE.
   - θ ~ U[−π, π]ⁿ, with the **median** over θ and the log-typical A = 4^(−(n−1)) (Stage 5 Prop. 5). This yields
     median M ∝ 16^(n−1), i.e. slope log₁₀16 = 1.204.

The Loschmidt 4ⁿ is **not** implied by Teo:
- the 0/1 projector readout (per-shot variance F(1 − F)) lies outside Teo's Pauli model;
- it must be imported from Aghaei Saem et al. (B-10a, Var^(LE) = F(1 − F)) or Gentinetta et al. (E-02);
- Teo + B + steps 4–5 then gives M_SNR ≈ ρ²/(As²) and the median ∝ 4^(n−1).

## 12. What is different

| Aspect | Teo 2023 | Stage 7 |
|---|---|---|
| Object compared | Estimators (FD, GD, PS, SPS) applied to the same measurements | Readouts (Loschmidt projector vs SWAP test) with the same PS estimator |
| Readout | Pauli observables, term by term, ±1 outcomes | Global projector (0/1) and SWAP ancilla (±1) for the same F |
| Landscape / ensemble | Two-design modules (TDS); Haar averages | Product RX circuit; θ ~ U[−π, π]ⁿ; not a two-design |
| Statistic | Circuit-averaged MSE; average ratio D_θ0 | Per-θ exact laws; median and quantiles over θ |
| Scaling variable | d = 2ⁿ at fixed N_T; N_* in copies | Required M per θ, median vs n (slopes in decades/qubit) |
| Output | MSE values, ε_opt, λ_opt, N_* ∝ 2ⁿ | P(ĝ = 0), P_correct, conditional sign law, 4ⁿ vs 16ⁿ, vector and trajectory metrics |
| Exponent mechanism | Estimator choice changes the n-scaling of the error at fixed copies (D-05b) | Readout choice changes the required-shot exponent at a fixed estimator |

## 13. What is not located

After full reading and the searches logged in the ledger (D-NL09, D-NL13, D-NL02, D-NL17, D-NL20, D-NL27), the
following were not located in arXiv v3:

- the probability that a gradient estimate is exactly zero, at component or vector level (matrix rows 9, 19);
- exact sign probabilities P_correct and P_wrong (rows 10–11 are RELATED BUT DIFFERENT: qualitative remark only);
- the full estimator law (pmf, difference-of-binomials, tie probability; row 12 is RELATED BUT DIFFERENT: moments
  only);
- the conditional Loschmidt sign law P(correct | ĝ ≠ 0) → (1 + |sin θ_k|)/2 (row 13);
- any Loschmidt/projector or SWAP-test readout, or a comparison of readouts for one quantity (rows 2, 4, 14a, 14b, 15);
- explicit 4ⁿ or 16ⁿ shot scalings (row 17);
- cosine similarity, dot-product sign, matched starts and signal-free controls (rows 20, 22, 24, 25);
- product single-qubit-rotation landscapes and global-Z parity numerics (rows 27, 28).

`NOT LOCATED` means only: not found in arXiv:2206.12643v3 after the logged searches. The APS version of record was not
inspected. This audit is evidence for A1 and does not make the novelty decision.
