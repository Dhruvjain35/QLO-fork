# B5 evidence ledger

This ledger is the evidence packet for the principal novelty audit (A1). It records what eight prior papers
explicitly contain, where, and under which assumptions. Papers A and B were reviewed in the initial B5 round
(commit dfd2c6b). Papers C, D and E, and the entries for matrix rows 29–30, were added in the follow-up audit
(2026-10-04); see [`B5_FOLLOWUP_AUDIT.md`](B5_FOLLOWUP_AUDIT.md). Papers F, G and H, and the entries for matrix rows
31–33, were added in the closure audit (2026-10-05); see [`B5_CLOSURE_AUDIT.md`](B5_CLOSURE_AUDIT.md). **It makes no
novelty determination.**

Papers:

- **A** — S. Thanasilp, S. Wang, M. Cerezo, Z. Holmes, *Exponential concentration in quantum kernel methods*,
  Nature Communications **15**, 5200 (2024), doi:10.1038/s41467-024-49287-w. Reviewed: the published article
  (13 pp., online 2024-06-18) and its Supplementary Information PDF (`41467_2024_49287_MOESM1_ESM.pdf`, 51 pp.).
  Main-text locators are the published equation/figure numbers. Locators prefixed **SI** use the Supplementary
  Information's own numbering.
- **B** — R. Aghaei Saem, B. Tafreshi, Z. Holmes, S. Thanasilp, *Pitfalls when tackling the exponential concentration
  of parameterized quantum models*, Quantum Science and Technology **11**, 015049 (2026),
  doi:10.1088/2058-9565/ae2202 (online 2026-01-30). **The published (IOP) text could not be retrieved:** every IOP URL
  returned a bot-protection page, and no repository copy of the published version was found. **Every B locator below
  therefore refers to arXiv:2507.22054v2 (2026-06-04)**, read in full from its PDF and LaTeX source. Where the
  item is absent from arXiv:2507.22054v1 (2025-07-29), this is stated. Published-version page, equation and
  section numbers have **not** been verified (see "Open items" at the end).
  *Follow-up update (2026-10-04):* the version of record was retrieved through its DOI (open access, CC BY 4.0).
  Its text matches arXiv v2, with the same equation, figure, theorem and corollary numbers and arabic section
  numbers. Every B entry was re-located in it; the page crosswalk is in [`B5_VERSION_GAP.md`](B5_VERSION_GAP.md).
  The B entries below keep their arXiv v2 locators unchanged.
- **C** — A. Arrasmith, M. Cerezo, P. Czarnik, L. Cincio, P. J. Coles, *Effect of barren plateaus on gradient-free
  optimization*, Quantum **5**, 558 (2021), doi:10.22331/q-2021-10-05-558. Reviewed: the published Quantum PDF
  (12 pp.; accepted 2021-06-04, published 2021-10-05). It is the arXiv:2011.12245v2 file (2021-09-30, "Updated to
  final publication version"); the LaTeX source was also read. Locators are the published numbers.
- **D** — Y. S. Teo, *Optimized numerical gradient and Hessian estimation for variational quantum algorithms*,
  Phys. Rev. A **107**, 042421 (2023), doi:10.1103/PhysRevA.107.042421. **Reviewed as arXiv:2206.12643v3**
  (2022-11-20, journal-ref PRA 107, 042421; 24 pp. + LaTeX source). The APS version of record (2023-04-17) returned
  an access challenge (HTTP 403) and is not open access; its page and equation numbers are **unverified**. Every D
  locator is an arXiv v3 locator. v1/v2 (2022-06) lack Secs. IV C, V C, VII and App. C 5 (B5_TEO_DEEP_AUDIT.md §1).
- **E** — G. Gentinetta, A. Thomsen, D. Sutter, S. Woerner, *The complexity of quantum support vector machines*,
  Quantum **8**, 1225 (2024), doi:10.22331/q-2024-01-11-1225. Reviewed: the published Quantum PDF (30 pp.; accepted
  2023-12-25, published 2024-01-11). It is the arXiv:2203.00031v2 file ("v2: published version"); the LaTeX source
  was also read. Locators are the published numbers.
- **F** — A. Mari, T. R. Bromley, N. Killoran, *Estimating the gradient and higher-order derivatives on quantum
  hardware*, Phys. Rev. A **103**, 012405 (2021), doi:10.1103/PhysRevA.103.012405. **Reviewed as arXiv:2008.06517v2**
  (2021-02-26; 17 pp.), which is byte-identical to the open-access post-print in the authors' institutional repository.
  The APS version of record returned an access challenge (HTTP 403); its numbers are unverified.
- **G** — A. Miranskyy, *The Cost of Certainty: Shot Budgets in Quantum Program Testing*, arXiv:2510.22418v1
  (2025-10-25; 30 pp.), a preprint with no journal reference.
- **H** — H. Zhan, B. Wang, M. Mi, J. Xie, L. Xu, A. Zhang, L. Zhang, *Experimental benchmarking of quantum state
  overlap estimation strategies with photonic systems*, Light: Science & Applications **14**, 83 (2025),
  doi:10.1038/s41377-025-01755-8. Reviewed: the published version (12 pp.) and the published Supplementary Information
  (26 pp.); arXiv:2406.06810v1 (2024-06-10) cross-checked for dating.

Allowed classifications (follow-up vocabulary; every C–H entry and every entry added for rows 29–33 uses only these
four):

- `EXPLICIT` — the source states it.
- `PARTIAL / IMPLIED` — the source's formulas imply the item only after extra algebra and assumptions that the
  source does not perform. The algebra and added assumptions are written out in the entry or in the linked document.
- `RELATED BUT DIFFERENT` — the source contains a related statement about a different object, statistic, ensemble,
  estimator or measurement.
- `NOT LOCATED` — not found in the reviewed version after the listed searches. It means only that, **not**
  that the item is absent from the literature.

Legacy label: `PARTIAL / RELATED` is the initial-round label for a related but non-identical statement. It is kept
unchanged on the papers A and B entries that carry it (no initial-round classification was altered), and it plays
the role of `RELATED BUT DIFFERENT`.

One entry is one (source location, claim) pair. Where a single location supports several claims at different
strengths, it appears as separate entries (e.g. A-06a and A-06b). Matrix rows refer to `B5_PRIOR_WORK_MATRIX.md`.
Candidate ids: C1–C4 are the four Stage 7 candidate contributions; F-A…F-H are the "already expected prior" facts
of the B5 brief; CTX is context.

Stage 7 notation used in "Relation to Stage 7":
- F = ∏ cos²(θ_j/2), A = ∏_{j≠k} cos²(θ_j/2), s = sin θ_k, F± = A(1∓s)/2, g = As/2;
- Loschmidt (LE) counts K± ~ Bin(M, F±);
- SWAP probabilities q± = (1+F±)/2.
- In Teo's (paper D) formulas, s is Teo's shift angle (his Eq. 11), not sin θ_k.

---

## Paper A — Thanasilp et al., Nat. Commun. 15, 5200 (2024)

<a id="A-01"></a>
### A-01 · Definition 1 (exponential concentration), Eqs. (9)–(11)
- **Paper:** A
- **Candidate:** F-A
- **Matrix rows:** 1
- **Claim category:** Exponential concentration of measured quantities (definition)
- **Classification:** EXPLICIT
- **Section:** Results
- **Subsection:** Why exponential concentration is problematic
- **Equation:** (9), (10), (11)
- **Figure:** —
- **Appendix:** SI Eqs. (18)–(19) restate it
- **Page:** 4
- **Source version:** Published version (Nat. Commun. 15, 5200; online 2024-06-18)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** A quantity X(α) measured as an expectation value is deterministically exponentially concentrated if |X(α) − μ| ≤ β ∈ O(1/bⁿ) for all α, and probabilistically concentrated if Pr_α[|X(α) − μ| ≥ δ] ≤ β/δ² with β ∈ O(1/bⁿ), b > 1. By Chebyshev, an exponentially small Var_α[X(α)] suffices. For kernels, α = {x, x′} and X = κ(x, x′).
- **Mathematical expression:** Pr_α[|X(α) − μ| ≥ δ] ≤ β/δ², β ∈ O(1/bⁿ); Var_α[X(α)] ∈ O(1/bⁿ)
- **Assumptions:** X(α) is the expectation of an observable; α drawn from a stated distribution.
- **Scope:** General definition; applied to fidelity and projected quantum kernels.
- **Relation to Stage 7:** Stage 7's fidelity F and gradient g over θ ~ U[−π, π]ⁿ concentrate in this sense (Stage 3 verified Var_θ[∂_k C] = (1/8)(3/8)^(n−1)).
- **Does NOT establish:** Anything about finite-shot parameter-shift gradient estimators, readout-dependent shot exponents, or zero/sign statistics.

<a id="A-02"></a>
### A-02 · Theorem 1 (expressivity-induced concentration), Eqs. (20)–(22)
- **Paper:** A
- **Candidate:** F-A
- **Matrix rows:** 1
- **Claim category:** Exponential concentration of the fidelity kernel (expressive / near-2-design embeddings)
- **Classification:** EXPLICIT
- **Section:** Results
- **Subsection:** Sources of exponential concentration — 1. Expressivity-induced concentration
- **Equation:** (17)–(22)
- **Figure:** Fig. 6
- **Appendix:** SI Note IV (proof)
- **Page:** 6–7
- **Source version:** Published version (Nat. Commun. 15, 5200; online 2024-06-18)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Kernel values concentrate around their mean with a bound G_n(ε_U)/δ² set by an expressivity measure ε_U. For the fidelity kernel, G_n includes β_Haar = 1/(2^(n−1)(2ⁿ+1)). Close to a 2-design the kernel exponentially concentrates (fidelity-kernel mean 1/2ⁿ) and exponentially many shots are needed.
- **Mathematical expression:** Pr[|κ − E κ| ≥ δ] ≤ G_n(ε_U)/δ²; G_n = β_Haar + ε_U(ε_U + 2√β_Haar); β_Haar = 1/(2^(n−1)(2ⁿ+1))
- **Assumptions:** x, x′ drawn from the same distribution (relaxed in SI Note IV A); pure input states.
- **Scope:** Data-embedding ensembles; Haar / 2-design limit.
- **Relation to Stage 7:** Background. The Stage 7 landscape is a product (non-2-design) landscape (see A-03).
- **Does NOT establish:** Product-landscape typical (log-mean) values, finite-shot gradient statistics, readout comparison.

<a id="A-03"></a>
### A-03 · Proposition 3 (global-measurement-induced concentration), Eq. (26); SI Note VI Eqs. (207)–(216)
- **Paper:** A
- **Candidate:** F-A; CTX
- **Matrix rows:** 1, 27
- **Claim category:** Concentration of the fidelity between tensor-product single-qubit-rotation states
- **Classification:** EXPLICIT
- **Section:** Results
- **Subsection:** Sources of exponential concentration — 3. Global-measurement-induced concentration
- **Equation:** (26); SI (207)–(216), esp. SI (213), (214), (216)
- **Figure:** Fig. 7
- **Appendix:** SI Note VI (proof)
- **Page:** 8–9 (main; Fig. 7 on p. 9); SI 35
- **Source version:** Published version (Nat. Commun. 15, 5200) + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Setting: fidelity kernel, product embedding U(x) = ⊗_k U_k(x_k) of single-qubit y-axis rotations, components independent and uniform on [−π, π], input |0⟩^⊗n. Result: Pr[|κ − 1/2ⁿ| ≥ δ] ≤ (3/8)ⁿ/δ². The proof shows E[κ²] = (3/8)ⁿ (per-qubit factor 3/8, SI Eq. 214) and E[κ] = 1/2ⁿ (SI Eq. 216). Fig. 7 confirms the exponential variance decay numerically for single layers of R_x, R_y and H·R_z.
- **Mathematical expression:** Var[κ^FQ] ≤ E[(κ^FQ)²] = (3/8)ⁿ; E[κ^FQ] = 2^(−n)
- **Assumptions:** U_k(x_k) = e^(−i x_k Y) (SI); x_k iid uniform on [−π, π]; product input state.
- **Scope:** The fidelity value between two encoded product states (a kernel), not a cost gradient; y-axis rotations only (U_k = e^(−i x_k Y)). The same single-qubit overlap law (cos² of a uniform angle) also holds for x-axis rotations acting on |0⟩ (our observation, not stated in the source) but not for z-axis rotations (overlap ≡ 1). The third case in Fig. 7 is Hadamard followed by R_z.
- **Relation to Stage 7:** The per-qubit factor is cos² of a uniformly distributed angle. For the R_x circuit of Stage 3–7 the same law holds (our observation): cos²(θ_j/2), θ_j ~ U[−π, π], has mean 1/2 and second moment 3/8. The Stage 7 fidelity landscape therefore belongs to this concentrating family. Stage 5/7 additionally used E[log cos²(θ/2)] = −2 log 2 (log-typical A = 4^(−(n−1))), which this proposition does not state.
- **Does NOT establish:** The gradient variance (1/8)(3/8)^(n−1) (Stage 3; Cerezo et al. 2021), log-typical values, shifted fidelities F±, or any finite-shot quantity.

<a id="A-04"></a>
### A-04 · SI Supplemental Proposition 6 (generalised global-measurement concentration), SI Eqs. (217)–(218)
- **Paper:** A
- **Candidate:** F-A
- **Matrix rows:** 1
- **Claim category:** Fidelity-kernel concentration for arbitrary local (product) unitaries
- **Classification:** EXPLICIT
- **Section:** SI Note VI
- **Subsection:** A. Extension to arbitrary local unitaries
- **Equation:** SI (217)–(228)
- **Figure:** —
- **Appendix:** SI Note VI A
- **Page:** SI 36–37
- **Source version:** Supplementary Information (MOESM1) to the published version
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** For a general product embedding of independent local unitaries, the fidelity kernel concentrates with bound ∏_k G₁^(k)(ε_k)/δ², where G₁^(k) = 1/3 + ε_k(ε_k + √(4/3)). For fully random single-qubit unitaries this bound is 1/3ⁿ.
- **Mathematical expression:** Pr[|κ − μ| ≥ δ] ≤ ∏_k G₁^(k)/δ²; G₁^(k) = 1/3 + ε_k(ε_k + √(4/3))
- **Assumptions:** Independent components; product initial state; x and x′ drawn from the same distribution (used in the proof, SI p. 37).
- **Scope:** Fidelity kernel; product embeddings.
- **Relation to Stage 7:** Background generalisation of A-03.
- **Does NOT establish:** Any finite-shot or gradient-level statement.

<a id="A-05"></a>
### A-05 · Loschmidt Echo estimate and Proposition 1, Eq. (13)
- **Paper:** A
- **Candidate:** F-B
- **Matrix rows:** 2
- **Claim category:** Loschmidt (overlap-test) fidelity estimates collapse to zero
- **Classification:** EXPLICIT
- **Section:** Results
- **Subsection:** Why exponential concentration is problematic
- **Equation:** (12), (13)
- **Figure:** Fig. 1 (caption), Fig. 2
- **Appendix:** SI Supplemental Proposition 2 (full version)
- **Page:** 4 (Fig. 1 on p. 2; Fig. 2 on p. 5)
- **Source version:** Published version (Nat. Commun. 15, 5200; online 2024-06-18)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** In the Loschmidt Echo test, the kernel is the probability of the all-zero bitstring, with outcome 1 for all-zero and 0 otherwise. If the kernel concentrates to an exponentially small μ, the chance of never seeing all-zero in N shots is (1 − μ)^N ≈ 1 − Nμ, so it is likely that the statistical estimate is zero. Proposition 1: with N ∈ O(poly(n)) shots and a training set of size N_s, the estimated Gram matrix equals the identity with probability ≥ 1 − δ′, δ′ ∈ O(c^(−n)).
- **Mathematical expression:** P(no all-zero outcome in N shots) = (1 − μ)^N ≈ 1 − Nμ; Pr[K̂ = 𝟙] ≥ 1 − δ′, δ′ ∈ O(c^(−n))
- **Assumptions:** Kernel exponentially concentrates to an exponentially small μ (Def. 1); N ∈ O(poly(n)); independent shots; N_s ∈ O(poly(n)) for the Gram-matrix statement (SI pp. 7–8).
- **Scope:** Fidelity-kernel estimates (one estimate per data pair).
- **Relation to Stage 7:** Same outcome model as Stage 7's Loschmidt readout (Bernoulli(F) per shot). Stage 7 §18 lists the fidelity-level zero estimate as a replication of prior work.
- **Does NOT establish:** The zero probability of a parameter-shift gradient (a difference of two shifted estimates), the equal-nonzero-count (tie) contribution, or sign statistics.

<a id="A-06a"></a>
### A-06a · SI Supplemental Proposition 2, SI Eqs. (20)–(32)
- **Paper:** A
- **Candidate:** F-B
- **Matrix rows:** 2
- **Claim category:** Exact single-estimate Loschmidt zero probability (fidelity level)
- **Classification:** EXPLICIT
- **Section:** SI Note III
- **Subsection:** A. Fidelity quantum kernel — 1. Loschmidt Echo test
- **Equation:** SI (20), (21); proof SI (26)–(32)
- **Figure:** —
- **Appendix:** SI Note III A 1
- **Page:** SI 7–8
- **Source version:** Supplementary Information (MOESM1) to the published version
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** With polynomially many shots, the Loschmidt estimate of the fidelity kernel is zero with probability ≥ 1 − δ, δ ∈ O(c^(−n)). The proof writes P(κ̂ = 0) as an integral of the exact conditional probability (1 − s)^N over the kernel-value distribution, then lower-bounds it by (1 − N(μ + β^(1/4)))(1 − √β).
- **Mathematical expression:** Pr[κ̂ = 0] = ∫₀¹ (1 − s)^N Pr[κ = s] ds ≥ (1 − N(μ + β^(1/4)))(1 − √β)
- **Assumptions:** Probabilistic exponential concentration with μ ∈ O(1/b′ⁿ), β ∈ O(1/bⁿ); N ∈ O(poly(n)).
- **Scope:** A single fidelity (kernel) estimate.
- **Relation to Stage 7:** The conditional factor (1 − s)^N is the exact zero probability of one Loschmidt fidelity estimate. Stage 7 §18 reports P(F̂ = 0) = (1 − F)^M at the fidelity level.
- **Does NOT establish:** Gradient-level P(ĝ = 0) (see A-06b).

<a id="A-06b"></a>
### A-06b · SI Supplemental Proposition 2 proof, SI Eqs. (26)–(27), read against the gradient-level question
- **Paper:** A
- **Candidate:** C1
- **Matrix rows:** 9
- **Claim category:** Gradient-level exact zero probability P(ĝ = 0)
- **Classification:** PARTIAL / RELATED
- **Section:** SI Note III
- **Subsection:** A. Fidelity quantum kernel — 1. Loschmidt Echo test
- **Equation:** SI (26)–(27)
- **Figure:** —
- **Appendix:** SI Note III A 1
- **Page:** SI 7
- **Source version:** Supplementary Information (MOESM1) to the published version
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Only the zero probability of a single fidelity estimate is derived, P(κ̂ = 0 | κ = s) = (1 − s)^N. No parameter-shift difference of two estimates is considered anywhere in the paper.
- **Mathematical expression:** P(κ̂ = 0 | κ = s) = (1 − s)^N
- **Assumptions:** As A-06a.
- **Scope:** Fidelity level, not gradient level.
- **Relation to Stage 7:** Stage 5/7 gradient-level law: P(ĝ = 0) = Σ_r Bin(r; M, F₊) Bin(r; M, F₋). Its r = 0 term, (1 − F₊)^M (1 − F₋)^M, is a product of two factors of the source's form. The r ≥ 1 equal-count terms have no counterpart in the source. Algebra in B5_MATH_COMPARISON §6.1.
- **Does NOT establish:** The difference-of-binomials law, the tie (r ≥ 1) mass, the Poisson-limit e^(−MA) I₀(MA|cos θ_k|) form, or any statement about gradients.

<a id="A-07"></a>
### A-07 · SI Eqs. (33)–(36): joint all-zero probability of the estimated Gram matrix
- **Paper:** A
- **Candidate:** C4
- **Matrix rows:** 19
- **Claim category:** Joint probability that a whole collection of Loschmidt estimates is exactly zero
- **Classification:** PARTIAL / RELATED
- **Section:** SI Note III
- **Subsection:** A. Fidelity quantum kernel — 1. Loschmidt Echo test (second half of the proof of Supp. Prop. 2)
- **Equation:** SI (33)–(36)
- **Figure:** —
- **Appendix:** SI Note III A 1
- **Page:** SI 8
- **Source version:** Supplementary Information (MOESM1) to the published version
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Kernel estimates for different data pairs are independent. So the probability that every off-diagonal Gram entry is estimated as exactly zero (K̂ = 𝟙) is the product of per-entry zero probabilities, bounded below by (1 − δ)^(N_s(N_s − 1)/2) ≥ 1 − N_s(N_s − 1)δ/2.
- **Mathematical expression:** Pr[K̂ = 𝟙] = ∏_{i<j} Pr[κ̂_ij = 0] ≥ (1 − δ)^(N_s(N_s−1)/2)
- **Assumptions:** Independent estimates per pair; per-entry concentration.
- **Scope:** Gram matrix of kernel values, not a gradient vector.
- **Relation to Stage 7:** Structurally the same as Stage 5 §10 and Stage 7 §14 (full-gradient zero probability = ∏_k P₀ under independent batches). The source applies it to kernel matrices, not gradient vectors.
- **Does NOT establish:** The full-gradient-vector zero probability, its values at the Stage 7 settings, or the conditional alignment of nonzero vectors.

<a id="A-08"></a>
### A-08 · SWAP-test estimate and Proposition 2, Eq. (14); SI Eqs. (46)–(49), (54)
- **Paper:** A
- **Candidate:** F-C
- **Matrix rows:** 3
- **Claim category:** SWAP-test fidelity estimates become data-independent random variables
- **Classification:** EXPLICIT
- **Section:** Results
- **Subsection:** Why exponential concentration is problematic
- **Equation:** (14); SI (46)–(49), SI (54)
- **Figure:** Fig. 1 (caption), Fig. 2; SI Fig. 3
- **Appendix:** SI Note III A 2 (Supplemental Lemma 3, Supplemental Corollary 2)
- **Page:** 4 (main; Fig. 1 on p. 2, Fig. 2 on p. 5); SI 9–13
- **Source version:** Published version (Nat. Commun. 15, 5200) + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** SWAP-test outcomes are +1 with probability p₊ = 1/2 + κ/2 and −1 otherwise, so the kernel is a perturbation of the uniform distribution. With polynomially many shots, each estimate is, with probability exponentially close to 1 over input pairs, statistically indistinguishable from κ̂^(rand) = (1/N) Σ λ̃_m with λ̃_m = ±1 equiprobable. For a polynomial-size training set the estimated Gram matrix is indistinguishable from a data-independent random matrix.
- **Mathematical expression:** P_κ = {(1+κ)/2, (1−κ)/2}; P₀ = {1/2, 1/2}; κ̂_N^(rand) = (1/N) Σ_m λ̃_m
- **Assumptions:** Exponential concentration to an exponentially small μ; N ∈ O(poly(n)); statements hold with probability ≥ 1 − δ_κ over input pairs; N_s ∈ O(poly(n)) for the Gram-matrix and model statements (SI Supp. Cors. 1–2, union bound SI Eqs. 59–61); statistical indistinguishability defined at success probability ≤ 0.51 (SI Def. 2).
- **Scope:** Fidelity-kernel estimates.
- **Relation to Stage 7:** Same outcome model as Stage 7's SWAP readout (q = (1+F)/2). Stage 7 §18 lists the data-independent SWAP fidelity estimate as a replication of prior work.
- **Does NOT establish:** A gradient-level SWAP estimator, its zero/tie probability (central binomial), its sign statistics, or its shot exponent.

<a id="A-08b"></a>
### A-08b · Outcome models of the two tests, Eqs. (12), (14); SI Eqs. (17), (46) — read against estimator variances
- **Paper:** A
- **Candidate:** F-D
- **Matrix rows:** 4
- **Claim category:** Different estimator variances for Loschmidt vs SWAP
- **Classification:** PARTIAL / RELATED
- **Section:** Results; SI Note III A
- **Subsection:** Why exponential concentration is problematic; SI III A 1–2
- **Equation:** (12), (14); SI (17), (46), (47)
- **Figure:** SI Fig. 1
- **Appendix:** SI Note III A
- **Page:** 4; SI 5–6, 9
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Both tests are written as empirical means of single-shot outcomes. Loschmidt: outcome 1/0 with P(1) = κ. SWAP: ±1 with P(+1) = (1+κ)/2. The two outcome distributions are fully specified, but the per-shot estimator variances (κ(1 − κ) and 1 − κ²) are not written down or compared.
- **Mathematical expression:** LE: λ ∈ {1, 0}, P(1) = κ; SWAP: λ ∈ {+1, −1}, P(+1) = (1+κ)/2
- **Assumptions:** —
- **Scope:** Fidelity-kernel level.
- **Relation to Stage 7:** The variances follow from these outcome models in one line (B5_MATH_COMPARISON §2.3, §3.3). Paper B states them explicitly (B-10a).
- **Does NOT establish:** The variance expressions themselves, or any consequence of their difference for shot exponents.

<a id="A-09a"></a>
### A-09a · Fig. 1 caption, Corollary 1 Eqs. (15)–(16), Figs. 2–3: same-kernel Loschmidt vs SWAP behaviour
- **Paper:** A
- **Candidate:** F-B; F-C; C3
- **Matrix rows:** 14a
- **Claim category:** Same-objective Loschmidt vs SWAP comparison at the fidelity/kernel-estimate level
- **Classification:** EXPLICIT
- **Section:** Introduction; Results
- **Subsection:** Why exponential concentration is problematic
- **Equation:** (15), (16)
- **Figure:** Fig. 1, Fig. 2, Fig. 3
- **Appendix:** SI Supplemental Corollaries 1–2
- **Page:** 2 (Fig. 1); 5 (Corollary 1, Figs. 2–3)
- **Source version:** Published version (Nat. Commun. 15, 5200; online 2024-06-18)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** For the same kernels and data, the two readouts behave differently. Loschmidt gives an identity estimated Gram matrix and zero predictions on unseen data. SWAP gives a random matrix and predictions that fluctuate around zero. Fig. 3 shows this numerically for an engineered 40-qubit dataset (tensor-product encoding, N = 1000 shots per kernel value, 10 repetitions), comparing training with exact kernels, LE estimates, SWAP estimates and a random matrix.
- **Mathematical expression:** a₀(y, λ) = y/(1 − λ) (LE); a_rand(y, λ) = (K̂_N^(rand) − λ𝟙)^(−1) y (SWAP)
- **Assumptions:** Kernel concentration; polynomial shots; kernel ridge regression; statements hold with probability exponentially close to 1; N_s ∈ O(poly(n)).
- **Scope:** Kernel estimates and downstream kernel-ridge-regression models; no parameter-shift gradients.
- **Relation to Stage 7:** A same-objective, two-readout comparison exists here at the kernel (fidelity) level. Stage 7's comparison is at the parameter-shift-gradient level on a paired θ grid.
- **Does NOT establish:** Gradient-level comparison, shot-exponent comparison, zero/sign probabilities.

<a id="A-09b"></a>
### A-09b · Fig. 3 "random" curve: a data-independent random-matrix baseline
- **Paper:** A
- **Candidate:** C4
- **Matrix rows:** 25
- **Claim category:** Signal-free control
- **Classification:** PARTIAL / RELATED
- **Section:** Results
- **Subsection:** Why exponential concentration is problematic
- **Equation:** —
- **Figure:** Fig. 3 (legend entry "random"); SI Fig. 6 (projected kernel analogue)
- **Appendix:** SI Note III B 2
- **Page:** 5–6; SI 19
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Fig. 3 includes a model trained on a random matrix whose off-diagonal entries are data-independent random variables. With SWAP estimates, the relative test loss follows that random-matrix control.
- **Mathematical expression:** —
- **Assumptions:** As A-09a.
- **Scope:** Kernel-model generalisation; not an optimisation trajectory.
- **Relation to Stage 7:** A signal-free control exists, applied to a trained kernel model rather than to a gradient-descent trajectory with matched starts.
- **Does NOT establish:** A random-walk optimisation control, matched-start trajectories, or alignment metrics.

<a id="A-10a"></a>
### A-10a · SI Supplementary Fig. 4 and SI Note III A 3: numerical Loschmidt vs SWAP on product-R_y kernels
- **Paper:** A
- **Candidate:** C3; F-E
- **Matrix rows:** 5, 14a
- **Claim category:** Numerical same-kernel comparison of the two readouts and the shot burden
- **Classification:** EXPLICIT
- **Section:** SI Note III
- **Subsection:** A. Fidelity quantum kernel — 3. Numerical simulation
- **Equation:** —
- **Figure:** SI Supplementary Fig. 4 (a) Loschmidt Echo, (b) SWAP
- **Appendix:** SI Note III A 3
- **Page:** SI 13–14
- **Source version:** Supplementary Information (MOESM1) to the published version
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** "exponentially many measurement shots are required i.e., N ∈ Ω(2ⁿ)"
- **Source statement (paraphrase):** Setup: N_s = 25 inputs with components uniform on [0, 2π], tensor product of single-qubit R_y encodings, n = 5–40, shots per kernel value up to ~2×10⁶. Loschmidt: the fraction of zero estimates falls with N, and a fixed non-zero fraction (~0.75) needs N ∈ Ω(2ⁿ). At 30 and 40 qubits every estimate is zero even at 2×10⁶ shots. SWAP: the fraction of estimates passing a binomial test against the uniform distribution (p < 0.01) needs N to grow at least exponentially. Vertical lines mark 2ⁿ.
- **Mathematical expression:** Empirical: zero ratio (LE) and binomial-test success ratio (SWAP) vs N for n ∈ {5, 7, 10, 15, 20, 30, 40}
- **Assumptions:** Product-R_y encoding with uniform data; independent shots; binomial test at p < 0.01.
- **Scope:** Kernel (fidelity) estimates; numerical; no fitted exponents.
- **Relation to Stage 7:** Closest located analogue of Stage 5–7's per-θ shot requirements, on the same product-rotation fidelity family, but at the fidelity (not gradient) level and with different success metrics.
- **Does NOT establish:** Gradient-level shot requirements, a fitted exponent for either readout, or a comparison of the two exponents.

<a id="A-10b"></a>
### A-10b · SI Supplementary Fig. 4, read against the gradient-exponent questions
- **Paper:** A
- **Candidate:** C3
- **Matrix rows:** 15, 16
- **Claim category:** Shot-complexity exponent for each readout
- **Classification:** PARTIAL / RELATED
- **Section:** SI Note III
- **Subsection:** A. Fidelity quantum kernel — 3. Numerical simulation
- **Equation:** —
- **Figure:** SI Supplementary Fig. 4
- **Appendix:** SI Note III A 3
- **Page:** SI 14
- **Source version:** Supplementary Information (MOESM1) to the published version
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** For Loschmidt, the source states N ∈ Ω(2ⁿ) is needed for a fixed non-zero fraction, a lower-bound statement at the kernel level based on numerics. For SWAP it states "at least exponentially". Neither exponent is fitted and the two are not compared.
- **Mathematical expression:** N_LE ∈ Ω(2ⁿ) (numerical, kernel level); N_SWAP: exponential (unspecified base)
- **Assumptions:** As A-10a.
- **Scope:** Kernel (fidelity) level; numerical.
- **Relation to Stage 7:** Stage 5/7 report per-θ median requirements at the gradient level: ≈4ⁿ for LE (log-typical A = 4^(−(n−1))) and ≈16ⁿ for SWAP. The SI Fig. 4 caption ties the 2ⁿ vertical lines to the Hilbert-space dimension. Elsewhere the source gives the mean fidelity kernel 2^(−n) for this family (Prop. 3). Reading 2ⁿ as an arithmetic-mean scale, as opposed to Stage 5's log-typical 4^(−(n−1)), is ours. Ω(2ⁿ) is a lower bound and does not contradict ≈4ⁿ.
- **Does NOT establish:** Exponent values, the 4ⁿ vs 16ⁿ pair, gradient-level results.

<a id="A-11"></a>
### A-11 · SI Note II: Supplemental Lemmas 1–2, Supplemental Proposition 1 (SI Eq. 14); SI Definitions 2–3
- **Paper:** A
- **Candidate:** F-F
- **Matrix rows:** 6
- **Claim category:** Outcome-distribution hypothesis testing / statistical indistinguishability as the finite-shot object
- **Classification:** EXPLICIT
- **Section:** SI Note II; SI Note III A 2
- **Subsection:** A. One sample; B. Many samples; SWAP test
- **Equation:** SI (1), (9), (14), (15), (48)
- **Figure:** SI Fig. 2
- **Appendix:** SI Notes II–III
- **Page:** SI 2–4, 10, 12
- **Source version:** Supplementary Information (MOESM1) to the published version
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** One-sample success probability ≤ 1/2 + ‖P − Q‖₁/4. N-sample product bound ‖P^⊗N − Q^⊗N‖₁ ≤ N‖P − Q‖₁. For binary P₀ = (p₀, 1 − p₀) vs P_ε = (p₀ + ε, 1 − p₀ − ε), success ≤ 1/2 + N|ε|/2. Statistical indistinguishability is defined as success ≤ 0.51 (distributions, Def. 2) and extended to any map of the samples (outputs, Def. 3).
- **Mathematical expression:** Pr[right decision] ≤ 1/2 + N|ε|/2 (binary); ‖P^⊗N − Q^⊗N‖₁ ≤ N‖P − Q‖₁
- **Assumptions:** Independent samples; equal priors.
- **Scope:** Binary outcome distributions (kernel tests); 1-norm (total-variation) bounds.
- **Relation to Stage 7:** Stage 7 §15 notes that per-shot total variation is ∝ A for both readouts (SWAP's is exactly half of Loschmidt's), whereas squared Hellinger scales as A (LE) vs A² (SWAP). A 1-norm-based bound of this form gives the same 1/A threshold for both readouts (B5_MATH_COMPARISON §6.4).
- **Does NOT establish:** Hellinger/variance-based sample complexity or a readout-dependent exponent.

<a id="A-12a"></a>
### A-12a · SI Supplemental Proposition 5 (SI Eqs. 142–149) and Supplemental Corollary 5 (SI Eq. 150)
- **Paper:** A
- **Candidate:** F-E
- **Matrix rows:** 5
- **Claim category:** Exponential shot count sufficient for resolving concentrated quantities
- **Classification:** EXPLICIT
- **Section:** SI Note III
- **Subsection:** D. Sufficient condition to resolve kernel values
- **Equation:** SI (142)–(150)
- **Figure:** —
- **Appendix:** SI Note III D
- **Page:** SI 28–29
- **Source version:** Supplementary Information (MOESM1) to the published version
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** "exponential scaling in measurement shots is indeed required"
- **Source statement (paraphrase):** With relative error ε̃ = ε/√Var_α[X], Hoeffding's inequality makes N ≥ 2‖O‖²_∞ log(2/p)/(ε̃² Var_α[X]) shots sufficient. Under exponential concentration this scales as Ω(b^(2n)/ε̃²), assuming ‖O‖_∞ ∈ O(1). For a full Gram matrix it is Ω(N_s² b^(2n)/ε̃²). The source presents these counts as requirements (SI p. 28; Cor. 5 "the number of measurement shots N required"), although the argument is a Hoeffding sufficiency bound.
- **Mathematical expression:** N ≥ 2‖O‖²_∞ log(2/p) / (ε̃² Var_α[X(α)]) ∈ Ω(b^(2n)/ε̃²)
- **Assumptions:** Bounded observable (‖O‖_∞ ∈ O(1)); Hoeffding (range-based) concentration; relative-error criterion ε̃ ≲ 1; Supp. Cor. 5 additionally assumes "statistical fluctuations associated with individual measurement outcomes stay constant" (SI p. 29).
- **Scope:** Any expectation-value estimate; the bound depends on the outcome range ‖O‖_∞, not on the measurement scheme's variance. The constant-fluctuation assumption of Supp. Cor. 5 holds for ±1 (SWAP-type) outcomes but not for the Loschmidt 0/1 outcome at small F (per-shot variance F(1 − F)). The source does not discuss this.
- **Relation to Stage 7:** This is the source's shot-count statement. It is range-based, so it cannot separate Loschmidt from SWAP exponents. The per-outcome fluctuation that Cor. 5 assumes constant is exactly what differs between the readouts in Stage 7 (per-shot variance F(1 − F) vs 1 − F²), giving ∝ 1/A vs ∝ 1/A² requirements. The source does not draw this connection.
- **Does NOT establish:** A measurement-dependent exponent, gradient-level requirements, or a proven necessary (lower-bound) shot count (the count is framed as required but derived from a sufficiency bound).

<a id="A-13"></a>
### A-13 · Main-text statements of the exponential shot burden
- **Paper:** A
- **Candidate:** F-E
- **Matrix rows:** 5
- **Claim category:** Exponential measurement burden under concentration
- **Classification:** EXPLICIT
- **Section:** Introduction; Results; Discussion
- **Subsection:** Introduction (p. 2); after Theorem 1 (p. 6); Discussion (p. 11)
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 2, 6, 11
- **Source version:** Published version (Nat. Commun. 15, 5200; online 2024-06-18)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** When kernels exponentially concentrate, resolving them needs exponentially many shots. With polynomially many shots the trained model is independent of the input data.
- **Mathematical expression:** —
- **Assumptions:** Exponential concentration.
- **Scope:** Kernel estimation.
- **Relation to Stage 7:** The general fact Stage 5–7 take as given. Stage 7 adds readout-specific gradient-level exponents (see A-10b and B-10c for the closest prior statements).
- **Does NOT establish:** Readout-dependent exponents; gradient-level statements.

<a id="A-14"></a>
### A-14 · Corollary 1 (Eqs. 15–16); SI Definition 3, Supplemental Corollaries 1–2 (SI Eqs. 37–38, 54–57)
- **Paper:** A
- **Candidate:** F-H
- **Matrix rows:** 26
- **Claim category:** Post-processing (training/prediction) cannot recover information lost to concentration
- **Classification:** EXPLICIT
- **Section:** Results; SI Note III A
- **Subsection:** Why exponential concentration is problematic; SI III A 1–2
- **Equation:** (15), (16); SI (37)–(45), (54)–(61)
- **Figure:** SI Fig. 3
- **Appendix:** SI Note III A
- **Page:** 5; SI 8–13
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Any map applied to samples from indistinguishable distributions gives indistinguishable outputs (SI Def. 3). Optimal kernel-ridge parameters and predictions trained on concentrated estimates are, with probability exponentially close to 1, equal to (Loschmidt) or indistinguishable from (SWAP) data-independent quantities.
- **Mathematical expression:** Pr[a_opt = a₀(y, λ)] ≥ 1 − δ (LE); outputs of Φ on indistinguishable samples are indistinguishable (Def. 3)
- **Assumptions:** Kernel concentration; polynomial shots; polynomial training set.
- **Scope:** Kernel methods.
- **Relation to Stage 7:** The no-post-processing fact that Stage 7 does not claim.
- **Does NOT establish:** Gradient-level statements.

<a id="A-15"></a>
### A-15 · SI Note III C: Supplemental Lemma 6, Proposition 4, Corollary 4 (SI Eqs. 134–141)
- **Paper:** A
- **Candidate:** F-H
- **Matrix rows:** 26
- **Claim category:** Multi-copy coherent processing does not distinguish exponentially close states
- **Classification:** EXPLICIT
- **Section:** SI Note III
- **Subsection:** C. Indistinguishability of concentrated quantum states
- **Equation:** SI (134)–(141)
- **Figure:** —
- **Appendix:** SI Note III C
- **Page:** SI 27–28
- **Source version:** Supplementary Information (MOESM1) to the published version
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Given m copies of ρ or σ, the optimal success probability is ≤ 1/2 + m‖ρ − σ‖₁/4. For exponentially close states and polynomial m, they remain indistinguishable even with coherent processing. Hence multi-copy error-mitigation schemes cannot remove concentration-induced data independence.
- **Mathematical expression:** Pr[right decision] ≤ 1/2 + m‖ρ − σ‖₁/4
- **Assumptions:** ‖ρ − σ‖₁ ∈ O(1/bⁿ); m ∈ O(poly(n)).
- **Scope:** State-level distinguishability.
- **Relation to Stage 7:** Background; Stage 7 makes no state-discrimination claim.
- **Does NOT establish:** Anything about specific readouts' gradient exponents.

<a id="A-16"></a>
### A-16 · SI Note VIII (error mitigation), Supplemental Theorem 1 (SI Eqs. 274–278); main text p. 10
- **Paper:** A
- **Candidate:** F-H
- **Matrix rows:** 26
- **Claim category:** Error mitigation cannot remove (noise-induced) kernel concentration
- **Classification:** EXPLICIT
- **Section:** SI Note VIII; Results
- **Subsection:** SI VIII; main text "4. Noise-induced concentration"
- **Equation:** SI (274)–(278)
- **Figure:** —
- **Appendix:** SI Note VIII
- **Page:** SI 42–43; main 10
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Quoting a result of its Ref. [18] (Wang et al.), common error-mitigation strategies within a unified framework concentrate onto a state-independent fixed point at linear depth. So they cannot mitigate noise-induced exponential concentration of kernel values, and can even impair resolvability.
- **Mathematical expression:** |C_m − F₀| ∈ O(2^(−bn) a_max |T_EM| M_max)
- **Assumptions:** Local depolarising noise; circuit depth Ω(n); the cited theorem's assumptions.
- **Scope:** Noisy kernels; error mitigation.
- **Relation to Stage 7:** Background (Stage 7 is noiseless; B4 is Satyabrat's).
- **Does NOT establish:** Anything about noiseless finite-shot gradient readouts.

<a id="A-17"></a>
### A-17 · Proposition 4 (Eq. 37), Fig. 9; SI Notes IX–X: trainable embeddings
- **Paper:** A
- **Candidate:** CTX
- **Matrix rows:** —
- **Claim category:** Exponentially flat training landscape of kernel target alignment (trainability)
- **Classification:** EXPLICIT
- **Section:** Results
- **Subsection:** Training parameterized quantum kernels
- **Equation:** (35)–(37); SI (280)–(342)
- **Figure:** Fig. 9
- **Appendix:** SI Notes IX–X
- **Page:** 10–11; SI 43–50
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** The deviation probability of the kernel target alignment over variational parameters is "approximately bounded" by the variances of the parameterised kernels. If those vanish exponentially, the source concludes that the alignment landscape is exponentially flat and untrainable with polynomially many shots. Fig. 9 shows the exponential decay of Var_θ[TA] (exact variances over 500 initialisations of a single R_y layer + HEE; no finite-shot simulation).
- **Mathematical expression:** Pr_θ[|TA(θ) − E TA| ≥ δ] ≲ M Σ_{ij} Var_θ[κ_θ(x_i, x_j)]/δ² ("approximately bounded", Eq. (37))
- **Assumptions:** As stated in Proposition 4.
- **Scope:** Trainability of parameterised kernels; no finite-shot gradient-estimator analysis, no trajectories.
- **Relation to Stage 7:** Context only; listed so that the absence of a random-walk statement in paper A (A-NL08) is not mistaken for absence of any trainability content.
- **Does NOT establish:** Random-walk behaviour, parameter-shift finite-shot statistics, or trajectory comparisons.

<a id="A-18"></a>
### A-18 · Source's own survey of prior work: Introduction (p. 2) and SI Note I
- **Paper:** A
- **Candidate:** CTX
- **Matrix rows:** —
- **Claim category:** Source's positioning of earlier work (for follow-up only)
- **Classification:** EXPLICIT
- **Section:** Introduction; SI Note I
- **Subsection:** SI I.A–I.D
- **Equation:** —
- **Figure:** —
- **Appendix:** SI Note I
- **Page:** 2; SI 1–2
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** The source says its refs. 8 and 16 rigorously study the shots needed to train the fidelity kernel without addressing concentration. SI I.D says its SI refs. [9, 10] study shot noise in kernel methods without concentration. SI I.B says its SI ref. [3] suggests, without proving, that exponentially many shots are needed for certain embeddings.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** Bibliographic.
- **Relation to Stage 7:** Feeds B5_FOLLOWUP_SOURCES.md (shot-complexity studies of fidelity-kernel estimation).
- **Does NOT establish:** Anything about those works' contents (not reviewed in B5).

### Paper A — not-located search log

All entries below: whole paper reviewed (main text pp. 1–13 and SI pp. 1–51), by reading every page plus text
searches of the extracted text. Common search terms for all entries: gradient, parameter shift, parameter-shift,
derivative, sign, direction, conditional, tie, binomial, Skellam, cosine, angle, inner product, norm, random walk,
trajectory, exponent, 4^n, 16^n, sample complexity, shots, SNR, signal-to-noise.

<a id="A-NL07"></a>
### A-NL07 · Parameter-shift finite-shot analysis
- **Paper:** A
- **Candidate:** C1; C3
- **Matrix rows:** 7
- **Claim category:** Parameter-shift finite-shot analysis
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: parameter shift, parameter-shift, gradient estimator, derivative, finite-difference. "Gradient" appears only in barren-plateau background and reference titles. Kernel target alignment (A-17) is treated through variances, not finite-shot gradient estimators.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** Search covered main text, all SI notes and figure captions.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL08"></a>
### A-NL08 · Parameter-shift random-walk behaviour
- **Paper:** A
- **Candidate:** C4; F-G
- **Matrix rows:** 8
- **Claim category:** Random-walk behaviour of finite-shot gradient descent
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: random walk, trajectory, gradient descent, optimization step, update rule. The closest content is the random-matrix Gram estimate (A-08, A-09b) and the kernel-target-alignment trainability statement (A-17), neither of which concerns gradient-descent trajectories.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL10"></a>
### A-NL10 · Exact gradient P_correct
- **Paper:** A
- **Candidate:** C1
- **Matrix rows:** 10
- **Claim category:** Exact finite-shot gradient correct-sign probability
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: sign, correct direction, direction, P_correct, probability of correct sign, binomial difference. No sign or direction statistics are given for any estimate.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL11"></a>
### A-NL11 · Exact gradient P_wrong
- **Paper:** A
- **Candidate:** C1
- **Matrix rows:** 11
- **Claim category:** Exact finite-shot gradient wrong-sign probability
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: wrong sign, sign, direction, P_wrong. No sign statistics appear.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL12"></a>
### A-NL12 · Exact difference-of-binomials gradient law
- **Paper:** A
- **Candidate:** C1
- **Matrix rows:** 12
- **Claim category:** Distribution of a difference of two binomial counts (parameter-shift estimator)
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: binomial, difference, Skellam, tie, equal counts. "Binomial" occurs only for the binomial hypothesis test of SI Figs. 4–5. All estimates are single empirical means; no difference of two estimates is analysed.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL13"></a>
### A-NL13 · Conditional Loschmidt sign law
- **Paper:** A
- **Candidate:** C2
- **Matrix rows:** 13
- **Claim category:** P(correct sign | nonzero estimate) for the Loschmidt readout
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: conditional, given nonzero, sign, direction, success probability, single count, (1+|sin|)/2. Conditional probabilities appear only as the zero-estimate integrand P(κ̂ = 0 | κ = s) (A-06a) and in hypothesis-test success probabilities (SI Eqs. (2)–(3), (50)). None is a sign law.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL14b"></a>
### A-NL14b · Same-objective Loschmidt vs SWAP comparison at the parameter-shift-gradient level
- **Paper:** A
- **Candidate:** C3
- **Matrix rows:** 14b
- **Claim category:** Same-θ, same-gradient comparison of two readouts
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: gradient, parameter shift, same landscape, same objective. The two-readout comparison exists only for kernel estimates (A-09a, A-10a).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL17"></a>
### A-NL17 · Explicit 4ⁿ vs 16ⁿ comparison
- **Paper:** A
- **Candidate:** C3
- **Matrix rows:** 17
- **Claim category:** Explicit pair of shot exponents 4ⁿ (LE) and 16ⁿ (SWAP)
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: 4^n, 16^n, 4n, 16n, exponent, base of exponential, decades per qubit, slope. Exponential statements are Ω(2ⁿ) (numerical, LE, kernel level; A-10b), Ω(b^(2n)) (scheme-independent sufficient bound; A-12a), and "at least exponentially" (SWAP; A-10b).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL18"></a>
### A-NL18 · Measurement scheme changing the gradient-resolution exponent
- **Paper:** A
- **Candidate:** C3
- **Matrix rows:** 18
- **Claim category:** Readout-dependent exponent of the resolution shot count
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** Nearest content: SI Note III D (A-12a)
- **Equation:** Nearest content: SI (143)–(144)
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: exponent, measurement strategy, readout, POVM, shot scaling, resolution. The source's resolution bound (SI Supp. Prop. 5) is range-based and identical for both tests, and no statement ties the exponent to the measurement scheme.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL20"></a>
### A-NL20 · Estimated/exact gradient cosine similarity
- **Paper:** A
- **Candidate:** C4
- **Matrix rows:** 20
- **Claim category:** Cosine similarity of estimated vs exact gradient vectors
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: cosine, angle, alignment, inner product, gradient vector. "Angle" occurs only for rotation angles of the encodings.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL21"></a>
### A-NL21 · Gradient norm inflation
- **Paper:** A
- **Candidate:** C4
- **Matrix rows:** 21
- **Claim category:** Norm of estimated vs exact gradient
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: norm (hits are Schatten/1-norms of states or distributions, the feature-space norm ‖a‖_H of the kernel-ridge regulariser (main p. 3) and operator norms ‖O‖_∞ (SI Supp. Prop. 5)), gradient norm, magnitude.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL22"></a>
### A-NL22 · Probability that ĝ·g > 0
- **Paper:** A
- **Candidate:** C4
- **Matrix rows:** 22
- **Claim category:** Probability that the estimated gradient is a descent direction
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: inner product, dot product, descent direction, sign.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL23"></a>
### A-NL23 · Component sign accuracy
- **Paper:** A
- **Candidate:** C4
- **Matrix rows:** 23
- **Claim category:** Fraction of gradient components with correct sign
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: sign, component, sign accuracy.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL24"></a>
### A-NL24 · Matched-start finite-shot optimisation trajectories
- **Paper:** A
- **Candidate:** C4
- **Matrix rows:** 24
- **Claim category:** Trajectories from identical starts under different readouts/shot budgets
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: trajectory, iteration, initialization, paired, matched. Kernel ridge regression is solved in closed form. Fig. 9 reports variances over 500 random initialisations, not trajectories.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL28"></a>
### A-NL28 · Global-Z (parity) parameter-shift training numerics on a single rotation layer
- **Paper:** A
- **Candidate:** CTX
- **Matrix rows:** 28
- **Claim category:** Finite-shot training numerics with a global Pauli-Z cost on a single-qubit-rotation layer
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: Pauli-Z, parity, global observable, training curve. Single rotation layers appear only as kernel embeddings (Prop. 3, Fig. 7, main Fig. 3, SI Fig. 4) and as the trainable R_y layer of Fig. 9 (Var_θ[TA] only, no training curves).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

---

## Paper B — Aghaei Saem, Tafreshi, Holmes, Thanasilp, QST 11, 015049 (2026)

All B locators: **arXiv:2507.22054v2** (dated 2026-06-04). The published (IOP) version was not inspected.
"v1" = arXiv:2507.22054v1 (2025-07-29).

<a id="B-01"></a>
### B-01 · §II Framework: procedure P, Eqs. (1)–(4), (6)
- **Paper:** B
- **Candidate:** C1; C3
- **Matrix rows:** 7
- **Claim category:** Parameter-shift gradient descent with finite-shot loss estimates, inside the general procedure
- **Classification:** EXPLICIT
- **Section:** II. Framework
- **Subsection:** Gradient-based and non-gradient based training
- **Equation:** (1)–(4), (6)
- **Figure:** Fig. 2
- **Appendix:** App. B Eq. (B17) (formal re-statement)
- **Page:** 3–4 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); same equation numbers in v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Each quantity ℓ_i is estimated from N POVM outcomes (outcome probabilities p_k = Tr[ρ M_k]). For vanilla gradient descent with the parameter-shift rule, the k-th update uses the difference of estimated losses at θ ± (π/2)ê_k. For a single Pauli observable this needs N_ℓ = 2N_p estimated quantities.
- **Mathematical expression:** [Φ_P]_k = θ_k − (η/2)[L̂(θ + (π/2)ê_k) − L̂(θ − (π/2)ê_k)]
- **Assumptions:** Circuits obeying the parameter-shift rule; polynomially many quantities.
- **Scope:** General loss functions; the finite-shot statistics are analysed only through the indistinguishability results (B-04–B-06).
- **Relation to Stage 7:** Stage 7's estimator ĝ = [Ĉ(θ + π/2 e_k) − Ĉ(θ − π/2 e_k)]/2 with independent batches is this update's gradient term with an infidelity loss.
- **Does NOT establish:** The distribution, variance, zero or sign probabilities of the parameter-shift estimate for any specific readout.

<a id="B-02"></a>
### B-02 · §II "Polynomial POVMs in disguise": global Pauli-Z as a two-outcome parity POVM
- **Paper:** B
- **Candidate:** CTX
- **Matrix rows:** —
- **Claim category:** Global Pauli-Z estimation uses the two-element parity POVM {Π₊, Π₋}
- **Classification:** EXPLICIT
- **Section:** II. Framework
- **Subsection:** Polynomial POVMs in disguise
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 5 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); the global-Z paragraph is absent from v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Estimating ⟨⊗Z_i⟩ requires only the eigenvalue sector of each bitstring, so the relevant POVM is {Π₊, Π₋}: projectors onto even- and odd-parity subspaces.
- **Mathematical expression:** M = {Π₊, Π₋}
- **Assumptions:** —
- **Scope:** POVM bookkeeping.
- **Relation to Stage 7:** Matches the two-outcome parity estimator of the Stage 6 parity benchmark.
- **Does NOT establish:** Finite-shot gradient statistics for that POVM.

<a id="B-03"></a>
### B-03 · §III Definition 1 (outcome probability concentration), Eq. (8)
- **Paper:** B
- **Candidate:** F-A; F-F
- **Matrix rows:** 1, 6
- **Claim category:** Concentration at the level of POVM outcome probabilities
- **Classification:** EXPLICIT
- **Section:** III. Exponential concentration
- **Subsection:** Definition 1
- **Equation:** (8)
- **Figure:** Fig. 1
- **Appendix:** App. B (used throughout)
- **Page:** 5–7; Fig. 1 on p. 2 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); v1 has Definition 1/Eq. (8) without the explicit "drawn from D" qualifier and the following remark
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** A POVM's outcome probabilities concentrate with respect to α ~ D if, for every element, Pr(|p_k(α) − μ_k| ≥ δ) ≤ β/δ² with β ∈ O(exp(−n)) and α-independent μ_k. The mechanisms are those of expectation-value concentration, since p_k is the expectation of a POVM element.
- **Mathematical expression:** Pr_{α~D}(|p_k(α) − μ_k| ≥ δ) ≤ β/δ², β ∈ O(exp(−n))
- **Assumptions:** Distribution D over the variables.
- **Scope:** Any POVM.
- **Relation to Stage 7:** Stage 5–7 analyse exactly these outcome probabilities (F±, q±) at fixed θ and their distribution over θ.
- **Does NOT establish:** Finite-shot gradient laws or exponents.

<a id="B-04"></a>
### B-04 · Theorem 1 (informal) and Theorem 2 (formal), Eqs. (B1)–(B13)
- **Paper:** B
- **Candidate:** F-F; F-E
- **Matrix rows:** 5, 6
- **Claim category:** Concentrated polynomial-size POVM ⇒ samples indistinguishable from a fixed distribution under polynomial shots
- **Classification:** EXPLICIT
- **Section:** III. Exponential concentration; App. B
- **Subsection:** Theorem 1; Theorem 2
- **Equation:** (B1)–(B13)
- **Figure:** Fig. 1
- **Appendix:** App. B
- **Page:** 7; 19–20; Fig. 1 on p. 2 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); same statement and (B)-numbering in v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** With |M| ∈ O(poly(n)) and N ∈ O(poly(n)), with probability ≥ 1 − δ over α the samples from P_α cannot be told apart from samples of P_fixed with success above 1/2 + ε. Here δ = |M|√β and ε = N|M|β^(1/4)/4 are exponentially small.
- **Mathematical expression:** Pr[right decision] ≤ 1/2 + N|M|β^(1/4)/4 with prob. ≥ 1 − |M|√β
- **Assumptions:** Definition 1 for all outcomes; polynomial POVM and shots; 1-norm hypothesis-testing bound (App. A).
- **Scope:** Any procedure with polynomial POVMs.
- **Relation to Stage 7:** The general indistinguishability fact; Stage 7 does not claim it.
- **Does NOT establish:** Readout-specific exponents (the bound is 1-norm based), gradient zero/sign laws.

<a id="B-05"></a>
### B-05 · Corollary 1 (informal, Eq. 9) and Corollary 3 (formal)
- **Paper:** B
- **Candidate:** F-H
- **Matrix rows:** 26
- **Claim category:** No classical post-processing removes indistinguishability
- **Classification:** EXPLICIT
- **Section:** III. Exponential concentration; App. B
- **Subsection:** Corollary 1; Corollary 3
- **Equation:** (9)
- **Figure:** Fig. 1
- **Appendix:** App. B
- **Page:** 7; 20; Fig. 1 on p. 2 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); same in v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Applying any map Φ′ to concentrated measurement outcomes yields, with high probability, an estimate statistically indistinguishable from the α-independent random variable ℓ̂_fixed = Φ′(S_N,fixed).
- **Mathematical expression:** ℓ̂_fixed = Φ′(S_N,fixed)
- **Assumptions:** As Theorem 2.
- **Scope:** Arbitrary post-processing.
- **Relation to Stage 7:** A fact Stage 7 does not claim. Stage 7's gradient estimators are one such map.
- **Does NOT establish:** The specific form of the fixed-distribution gradient laws.

<a id="B-06a"></a>
### B-06a · Corollary 2 (Eq. 10), Corollary 4 (Eqs. B14–B15) and proof (B16)–(B30): random walk
- **Paper:** B
- **Candidate:** C4; F-G
- **Matrix rows:** 8
- **Claim category:** Polynomial-shot parameter-shift gradient descent on a concentrated loss is statistically a random walk
- **Classification:** EXPLICIT
- **Section:** III. Exponential concentration; App. B
- **Subsection:** Corollary 2; Corollary 4 and proof
- **Equation:** (10); (B14)–(B30)
- **Figure:** Fig. 3
- **Appendix:** App. B
- **Page:** 7; 20–23; Fig. 3 on p. 6 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); v1 has the same corollaries with wording "results in a random walk" (see Version differences V-05)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Setting: loss Σ_i c_i Tr[ρ(θ)O_i] with Pauli O_i, parameter-shift rule, random initialisation, polynomially many iterations and shots. With probability ≥ 1 − c, c ∈ O(exp(−n)), each update θ_new = θ_current + Δ_N is indistinguishable from one with parameter-independent components [Δ_N]_k = −(η/2) Σ_i c_i [Σ_j z_ijk/N − Σ_j z′_ijk/N], with z, z′ = ±1 equiprobable. A union bound over steps extends this to the whole trajectory.
- **Mathematical expression:** [Δ_N]_k = −(η/2) Σ_i c_i [Σ_{j=1}^N z_ijk/N − Σ_{j=1}^N z′_ijk/N], z, z′ ∈ {±1} equiprobable
- **Assumptions:** Pauli observables (two-outcome POVMs, ±1 outcomes); every POVM exponentially concentrated; N, N_ℓ, N_step ∈ O(poly(n)); union bound.
- **Scope:** Concentration point 1/2 for both outcomes (Pauli/SWAP-like). The Loschmidt projector POVM, whose fixed distribution is (0, 1) (B-09a), is not the case written in (B15).
- **Relation to Stage 7:** Stage 7 §17–18 lists SWAP-driven GD at n ≥ 10 matching a signal-free random walk as a replication of this corollary.
- **Does NOT establish:** Zero/sign probabilities, alignment, norm or trajectory metrics (B-06b–B-06e), or the Loschmidt "frozen" behaviour.

<a id="B-06b"></a>
### B-06b · Eqs. (B18), (B26): update written as a difference of two empirical means of ±1 outcomes
- **Paper:** B
- **Candidate:** C1
- **Matrix rows:** 12
- **Claim category:** Difference-of-binomials form of the finite-shot parameter-shift estimate
- **Classification:** PARTIAL / RELATED
- **Section:** App. B
- **Subsection:** Proof of Corollary 4, step (1)
- **Equation:** (B18), (B19), (B26)
- **Figure:** —
- **Appendix:** App. B
- **Page:** 22–23 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); same numbering in v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Each update component is −(η/2) Σ_i c_i [Σ_q λ_i1kq/N − Σ_q λ_i2kq/N], with λ = +1 w.p. (1 + ℓ_i(α))/2 and −1 otherwise. Each sum is an affine function of a binomial count (our rewriting; the word "binomial" does not appear in the source, which uses only ±1-outcome sums). In the concentrated limit both are replaced by z = ±1 equiprobable (B26). The distribution of the difference is not derived.
- **Mathematical expression:** (our rewriting) Σ_q λ_q/N = 2K/N − 1, K ~ Bin(N, (1 + ℓ)/2)
- **Assumptions:** As B-06a.
- **Scope:** Pauli ±1 outcomes.
- **Relation to Stage 7:** The SWAP gradient estimator ĝ_SWAP = (K₋ − K₊)/M has exactly this structure with ℓ = F (ancilla ⟨Z⟩ = F). Stage 5–7 derive its exact pmf-based P_zero/P_correct.
- **Does NOT establish:** The pmf of the difference, P(ĝ = 0), P_correct/P_wrong, tie probability, or the Loschmidt (0/1-outcome) version.

<a id="B-06c"></a>
### B-06c · Corollaries 2/4 read against gradient sign probabilities
- **Paper:** B
- **Candidate:** C1
- **Matrix rows:** 10, 11
- **Claim category:** Correct/wrong-sign probabilities of the finite-shot gradient
- **Classification:** PARTIAL / RELATED
- **Section:** III. Exponential concentration; App. B
- **Subsection:** Corollary 2; Corollary 4
- **Equation:** (10), (B15), (B26)
- **Figure:** —
- **Appendix:** App. B
- **Page:** 7; 21–23 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** The update is indistinguishable from a parameter-independent variable that is symmetric under sign flip. This implies the sign carries no usable information about the landscape with high probability, but no probability of the correct or wrong sign is stated or computed.
- **Mathematical expression:** —
- **Assumptions:** As B-06a.
- **Scope:** Pauli/±1 outcomes; asymptotic indistinguishability statement.
- **Relation to Stage 7:** Stage 6–7 give exact finite-M P_correct, P_wrong and P_zero (e.g. SWAP P_correct → (1 − P_zero)/2; Loschmidt P_correct → 0 through zeros). Neither the values nor the Loschmidt asymmetry appear in the source.
- **Does NOT establish:** Exact or asymptotic P_correct/P_wrong values; their M- or n-dependence.

<a id="B-06d"></a>
### B-06d · Corollaries 2/4 read against full-vector direction metrics
- **Paper:** B
- **Candidate:** C4
- **Matrix rows:** 20, 22, 23
- **Claim category:** Direction of the estimated gradient vector (cosine, ĝ·g > 0, component sign accuracy)
- **Classification:** PARTIAL / RELATED
- **Section:** III. Exponential concentration; App. B
- **Subsection:** Corollary 2; Corollary 4
- **Equation:** (10), (B14)–(B15)
- **Figure:** Fig. 3
- **Appendix:** App. B
- **Page:** 7; 21; Fig. 3 on p. 6 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** The whole update vector is indistinguishable from a parameter-independent random vector. The source states this at the level of trajectories (random walk); it does not compute any alignment measure (cosine, ĝ·g sign, fraction of correct component signs).
- **Mathematical expression:** —
- **Assumptions:** As B-06a.
- **Scope:** Trajectory-level statement.
- **Relation to Stage 7:** Stage 7 §14 reports these metrics directly: SWAP median cosine ≈ 0.009, P(ĝ·g > 0) ≈ 0.51; Loschmidt conditional cosine ≈ 0.74 at n = 12, M = 1024. "Optimizer behaves like a random walk" and "cosine ≈ 0" are related but not identical statements.
- **Does NOT establish:** Any alignment value, the Loschmidt "zero-or-aligned" pattern, or finite-n behaviour.

<a id="B-06e"></a>
### B-06e · Corollary 4 read against gradient-norm inflation
- **Paper:** B
- **Candidate:** C4
- **Matrix rows:** 21
- **Claim category:** Norm of the estimated gradient relative to the exact gradient
- **Classification:** PARTIAL / RELATED
- **Section:** App. B
- **Subsection:** Corollary 4
- **Equation:** (B15)
- **Figure:** —
- **Appendix:** App. B
- **Page:** 21 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** The null update (B15) has a parameter-independent magnitude set by η, N and the coefficients c_i. The source makes no statement comparing the estimated-gradient norm with the exact-gradient norm.
- **Mathematical expression:** (implied, not stated) E‖Δ_N‖² = (η²/4) Σ_k Σ_i c_i² (2/N)
- **Assumptions:** As B-06a; the expectation shown is our algebra on (B15) (B5_MATH_COMPARISON §6.6).
- **Scope:** Null (concentrated) update only.
- **Relation to Stage 7:** Stage 7 §14 measures SWAP median log₁₀‖ĝ‖/‖g‖ ≈ 4.5 at n = 12, M = 1024.
- **Does NOT establish:** Any norm-ratio statement or value.

<a id="B-07a"></a>
### B-07a · Fig. 3 and §III text: 15-qubit training with 150 / 2¹⁵ / infinite shots
- **Paper:** B
- **Candidate:** C4; F-G
- **Matrix rows:** 8, 28
- **Claim category:** Numerical random-walk behaviour of finite-shot training on a barren plateau
- **Classification:** EXPLICIT
- **Section:** III. Exponential concentration
- **Subsection:** Text following Corollary 2
- **Equation:** —
- **Figure:** Fig. 3 (a)–(c)
- **Appendix:** App. C (setup)
- **Page:** 6–7 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); v1 has the figure, but its caption lacks the definition of the plotted quantity
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** For n = 15, a single layer of X rotations and the global Pauli-Z observable: trajectories with 2¹⁵ and infinite shots converge, while trajectories with 150 shots wander randomly. The mean and variance of (1/N_p)‖θ^(t) − θ^(0)‖₁ over initialisations under 150 shots closely resemble a random walk.
- **Mathematical expression:** Plotted statistic: (1/N_p)‖θ^(t) − θ^(0)‖₁ (mean and variance over initialisations)
- **Assumptions:** Global-Z cost; "random initialization" (Cor. 2; the Fig. 3 caption says "different parameter initializations"); learning rate η (value and schedule not stated in the reviewed text).
- **Scope:** One system size, one cost (parity), displacement statistics.
- **Relation to Stage 7:** Same circuit family as Stage 3–7 but the parity cost (Stage 6's parity benchmark). Stage 7's random-walk diagnostic uses the fidelity cost with the SWAP readout.
- **Does NOT establish:** Fidelity/SWAP or Loschmidt trajectories, endpoint-fidelity comparisons, alignment metrics, or start matching (B-07c).

<a id="B-07b"></a>
### B-07b · Fig. 3 (b)–(c): "Random Walk" reference curve
- **Paper:** B
- **Candidate:** C4
- **Matrix rows:** 25
- **Claim category:** Signal-free random-walk control
- **Classification:** EXPLICIT
- **Section:** III. Exponential concentration
- **Subsection:** Text following Corollary 2
- **Equation:** —
- **Figure:** Fig. 3 (b), (c) — legend "Random Walk"
- **Appendix:** —
- **Page:** 6–7 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** A random-walk reference is plotted alongside the 150-shot and 2¹⁵-shot runs for the mean and variance of parameter displacement. How the reference curve is generated is not specified in the reviewed text.
- **Mathematical expression:** —
- **Assumptions:** As B-07a.
- **Scope:** Displacement statistics only; parity cost; n = 15.
- **Relation to Stage 7:** Stage 7's control replaces SWAP counts with zero-signal counts (q₊ = q₋ = 1/2) under the identical update rule and identical starts, and compares fidelity endpoints and alignment. The source's comparison is on displacement statistics.
- **Does NOT establish:** Endpoint (loss/fidelity) comparison with a control, matched starts, or the construction of the reference.

<a id="B-07c"></a>
### B-07c · Fig. 3 (a) and Fig. 4: trajectories at different shot budgets — start matching not stated
- **Paper:** B
- **Candidate:** C4
- **Matrix rows:** 24
- **Claim category:** Matched-start finite-shot optimisation trajectories
- **Classification:** PARTIAL / RELATED
- **Section:** III. Exponential concentration; IV. Practical step-by-step guidelines
- **Subsection:** Text following Corollary 2; discussion of Fig. 4
- **Equation:** —
- **Figure:** Fig. 3 (a); Fig. 4
- **Appendix:** App. C
- **Page:** 6–8 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Trajectories under different shot budgets are shown together (Fig. 3a, a PCA cut) and training curves are compared across budgets (Fig. 4). Neither the text nor the captions say whether initial parameters are identical across budgets. Fig. 3 (b)–(c) average over different initialisations.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** Parity / global-Z costs.
- **Relation to Stage 7:** Stage 7 pairs every arm (exact, LE, SWAP, random walk) from identical θ₀ by construction (Stage 6 found an unpaired comparison gave a false positive).
- **Does NOT establish:** That starts were matched; any paired statistic.

<a id="B-08a"></a>
### B-08a · Fig. 4, §IV text and App. C: training curves at 10n vs 2ⁿ vs infinite shots
- **Paper:** B
- **Candidate:** F-E; F-G
- **Matrix rows:** 5
- **Claim category:** Exponential shot budget needed for training on a barren plateau (numerics)
- **Classification:** EXPLICIT
- **Section:** IV. Practical step-by-step guidelines
- **Subsection:** Discussion of Fig. 4
- **Equation:** (C1)–(C11)
- **Figure:** Fig. 4 (a)–(d)
- **Appendix:** App. C
- **Page:** 6, 8; 23–25 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); also in v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** For quantum natural gradient, CVaR, classical-NN initialisation and the rescaled parameter-shift rule (n = 9–17), training succeeds with 2ⁿ shots but does not move meaningfully with 10 × n shots.
- **Mathematical expression:** —
- **Assumptions:** Single X-rotation layer (C1); global-Z observables (C8) or a sum of four global-Z terms (C9); uniform random initialisation for QNG, CVaR and the rescaled parameter-shift rule; classical-NN-output initialisation for the NN method.
- **Scope:** Global costs; numerical.
- **Relation to Stage 7:** General exponential-burden fact; not readout-specific.
- **Does NOT establish:** Readout-dependent exponents or gradient-level laws.

<a id="B-08b"></a>
### B-08b · App. C, Eqs. (C1), (C8), (C9): single X-rotation layer with global Pauli-Z costs
- **Paper:** B
- **Candidate:** CTX
- **Matrix rows:** 28
- **Claim category:** Numerical setup on the single-qubit-rotation product circuit
- **Classification:** EXPLICIT
- **Section:** App. C
- **Subsection:** Further details of numerical simulation
- **Equation:** (C1), (C8), (C9)
- **Figure:** Fig. 3, Fig. 4
- **Appendix:** App. C
- **Page:** 23–25; Figs. 3–4 on p. 6 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); same in v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** All numerics use U(θ) = ∏_i e^(−iθ_i X_i) with global observables: ⊗Z_i (QNG, NN initialisation, rescaled PS) or a sum of four global-Z strings (CVaR). Parameters are initialised uniformly at random for QNG, CVaR and the rescaled parameter-shift rule; the classical-NN method initialises them from a neural network's output.
- **Mathematical expression:** U(θ) = ∏_{i=1}^n e^(−iθ_i X_i); H = ⊗_i Z_i
- **Assumptions:** —
- **Scope:** Parity-type costs on the product circuit, not the |0ⁿ⟩ fidelity.
- **Relation to Stage 7:** Same circuit family as Stage 3–7, different cost. This is Stage 6's parity benchmark setup (STAGE6.md §19 notes it). Stage 7's fidelity cost and the Loschmidt/SWAP readouts are not used in the source's numerics.
- **Does NOT establish:** Fidelity-cost results on this circuit.

<a id="B-08c"></a>
### B-08c · App. C setup read against the Stage 3–7 fidelity landscape
- **Paper:** B
- **Candidate:** CTX
- **Matrix rows:** 27
- **Claim category:** Concentration of the product single-qubit-rotation fidelity landscape
- **Classification:** PARTIAL / RELATED
- **Section:** App. C; IV. Practical step-by-step guidelines
- **Subsection:** Further details of numerical simulation; Subtlety regarding the choice of POVM
- **Equation:** (C1), (C8)
- **Figure:** Fig. 3, Fig. 4
- **Appendix:** App. C
- **Page:** 9–10, 23–25; Figs. 3–4 on p. 6 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** The source's numerics use the same product circuit (one layer of single-qubit X rotations; random initialisation, uniform for QNG, CVaR and rescaled parameter shift), but with global Pauli-Z costs, citing the globality-induced barren plateau. Its fidelity discussion (Loschmidt vs SWAP) assumes a 2-design, not the product family. The concentration of the product-circuit |0ⁿ⟩ fidelity is not stated.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** Same circuit, different cost; or same cost, different (2-design) ensemble.
- **Relation to Stage 7:** Paper A's Proposition 3 (A-03) is the located explicit statement for the product-rotation fidelity family.
- **Does NOT establish:** Concentration statistics of the product-circuit fidelity or its gradients.

<a id="B-09a"></a>
### B-09a · §IV "Subtlety regarding the choice of POVM", Fig. 5: Loschmidt vs SWAP fixed distributions
- **Paper:** B
- **Candidate:** F-B; F-C; C3
- **Matrix rows:** 1, 2, 3, 14a
- **Claim category:** Same fidelity objective, two POVMs: zero estimate (LE) vs 50/50 outcomes (SWAP)
- **Classification:** EXPLICIT
- **Section:** IV. Practical step-by-step guidelines
- **Subsection:** Subtlety regarding the choice of POVM
- **Equation:** —
- **Figure:** Fig. 5 (a) Loschmidt echo test, (b) SWAP test
- **Appendix:** App. B (Theorem 2 invoked)
- **Page:** 9 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); **absent from v1**; published-version status unverified
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** For learning |φ⟩ = U₀|0⟩ with infidelity loss and a variational state forming a 2-design: the Loschmidt POVM {|0⟩⟨0|^⊗n, 𝟙 − |0⟩⟨0|^⊗n} has fixed distribution (0, 1), so with probability exponentially close to 1 the estimated fidelity is zero. The SWAP-test POVM {|0⟩⟨0|, |1⟩⟨1|} on the ancilla has fixed distribution (1/2, 1/2). Both approaches are said to suffer from concentration (the fidelity concentrates under the 2-design assumption).
- **Mathematical expression:** P_fixed^(LE) = (0, 1); P_fixed^(SWAP) = (1/2, 1/2)
- **Assumptions:** |ψ(θ)⟩ = U(θ)|0⟩ forms a unitary 2-design; Theorem 2.
- **Scope:** Fidelity/loss estimates; analytic, no numerics; no gradients.
- **Relation to Stage 7:** Stage 7 lists the zero-vs-50/50 fidelity-level contrast as prior work (§3, §19). The source states it for a 2-design ensemble; Stage 7's landscape is the product (non-2-design) family.
- **Does NOT establish:** Gradient-level comparison, exponents, zero/sign probabilities.

<a id="B-09b"></a>
### B-09b · §IV, Loschmidt fixed distribution (0, 1), read against gradient/vector zero probabilities
- **Paper:** B
- **Candidate:** C1; C4
- **Matrix rows:** 9, 19
- **Claim category:** Zero probability of the gradient component / full gradient vector
- **Classification:** PARTIAL / RELATED
- **Section:** IV. Practical step-by-step guidelines
- **Subsection:** Subtlety regarding the choice of POVM
- **Equation:** —
- **Figure:** Fig. 5 (a)
- **Appendix:** —
- **Page:** 9 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); absent from v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Only the fidelity estimate is said to be zero with high probability. Nothing is said about the parameter-shift difference of two such estimates or about all components simultaneously.
- **Mathematical expression:** —
- **Assumptions:** As B-09a.
- **Scope:** Fidelity level.
- **Relation to Stage 7:** Both shifted Loschmidt estimates being zero makes the gradient component zero. Stage 5–7 compute the exact P(ĝ = 0) (including equal nonzero counts) and the full-vector zero probability.
- **Does NOT establish:** Gradient-level or vector-level zero probabilities or their values.

<a id="B-10a"></a>
### B-10a · §IV: single-shot estimator variances Var^(SWAP) = 1 − F², Var^(LE) = F(1 − F)
- **Paper:** B
- **Candidate:** F-D; C3
- **Matrix rows:** 4
- **Claim category:** Different estimator variances for Loschmidt vs SWAP (same fidelity)
- **Classification:** EXPLICIT
- **Section:** IV. Practical step-by-step guidelines
- **Subsection:** Subtlety regarding the choice of POVM
- **Equation:** Inline, unnumbered (text after Eq. (12))
- **Figure:** —
- **Appendix:** —
- **Page:** 10 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); **absent from v1**; published-version status unverified
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** "These distinct forms of variance result in different statistical behaviors"
- **Source statement (paraphrase):** The landscape variance is exponentially small regardless of the measurement scheme, but the estimator variances differ: 1 − F_θ² for the SWAP test and F_θ(1 − F_θ) for the Loschmidt echo test.
- **Mathematical expression:** Var^(SWAP)_ρ(θ)[ℓ̂(θ)] = 1 − F_θ²; Var^(LE)_ρ(θ)[ℓ̂(θ)] = F_θ(1 − F_θ)
- **Assumptions:** Per-shot variance (the source writes Var_ρ(θ)[ℓ̂(θ)] without a 1/N factor); pure variational state |ψ(θ)⟩ and target |φ⟩ as in the source's example; the landscape-variance clause relies on the stated assumption that |ψ(θ)⟩ = U(θ)|0⟩ forms a unitary 2-design (p. 9).
- **Scope:** Fidelity (loss) estimate, not its parameter-shift gradient.
- **Relation to Stage 7:** These are the per-shot variances Stage 7 uses (Var F̂ = F(1 − F)/M for LE; (1 − F²)/M for SWAP). Stage 7's gradient variances follow by the parameter-shift difference with independent batches (B5_MATH_COMPARISON §6.2).
- **Does NOT establish:** The gradient-estimator variances, SNRs, zero/sign probabilities, or the exponents they imply.

<a id="B-10b"></a>
### B-10b · §IV, Eq. (12): resolution ratio ε_N and the exponential-shot requirement
- **Paper:** B
- **Candidate:** F-E
- **Matrix rows:** 5
- **Claim category:** Exponential measurement burden via the estimator-variance / landscape-variance ratio
- **Classification:** EXPLICIT
- **Section:** IV. Practical step-by-step guidelines
- **Subsection:** Subtlety regarding the choice of POVM
- **Equation:** (12)
- **Figure:** —
- **Appendix:** —
- **Page:** 9–10 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); absent from v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Define ε_N(α) = Var_ρ(α)[ℓ̂(α)]/(N Var_α[ℓ(α)]). Sufficient resolution needs ε_N ≲ 1, which under exponential concentration requires N ∈ Ω(exp(n)). The source offers this as a rule-of-thumb diagnostic.
- **Mathematical expression:** ε_N(α) = Var_ρ(α)[ℓ̂(α)] / (N Var_α[ℓ(α)]); require ε_N ≲ 1 ⇒ N ∈ Ω(exp(n))
- **Assumptions:** Quantities that are expectation values; exponential concentration of Var_α[ℓ].
- **Scope:** General, applied to fidelity.
- **Relation to Stage 7:** Stage 7 uses a different, per-θ criterion (SNR ≥ ρ, P_correct ≥ q at fixed θ; median over θ). The two criteria give different exponents on the heavy-tailed product landscape (B5_MATH_COMPARISON §6.3).
- **Does NOT establish:** Readout-specific exponents (B-10c) or gradient-level criteria.

<a id="B-10c"></a>
### B-10c · §IV, Eq. (12) with the two variances: readout-dependent exponents implied but not computed
- **Paper:** B
- **Candidate:** C3
- **Matrix rows:** 15, 16, 18
- **Claim category:** Measurement-dependent shot-complexity exponent
- **Classification:** PARTIAL / IMPLIED
- **Section:** IV. Practical step-by-step guidelines
- **Subsection:** Subtlety regarding the choice of POVM
- **Equation:** (12) + inline variances
- **Figure:** —
- **Appendix:** —
- **Page:** 9–10 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); absent from v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** "affect the degree to which the problem suffers from shot noise"
- **Source statement (paraphrase):** Changing the POVM does not change the landscape variance and is not expected to remove concentration. Different estimators instead change how badly shot noise affects the problem. The source supplies ε_N and the two variances but does not combine them into shot counts or exponents for either readout.
- **Mathematical expression:** (our algebra, not in source) 2-design: N_LE ~ F/Var_α ~ 2ⁿ, N_SWAP ~ 1/Var_α ~ 4ⁿ (fidelity level); per-point SNR: N_SWAP/N_LE ≈ 1/F (fidelity) or ≈ 2/A (gradient)
- **Assumptions:** For the implication: 2-design statistics (E F = 2^(−n), Var_α F ≈ 2^(−2n)) or a per-point SNR criterion; independent shots; for the gradient version, parameter shift with independent batches and the Stage 5 log-typical A.
- **Scope:** The source is at the fidelity level under a 2-design. Stage 7 is at the gradient level on the product landscape.
- **Relation to Stage 7:** Algebra in B5_MATH_COMPARISON §6.2–§6.3. The implication holds at the fidelity level under the source's 2-design assumption (2ⁿ vs 4ⁿ). Reaching Stage 7's 4ⁿ vs 16ⁿ additionally needs the parameter-shift step, a per-θ criterion, and the product-landscape log-typical A. With the source's own ε_N criterion on the product landscape, the result differs: (2/3)ⁿ at the log-typical F, or (4/3)ⁿ at the mean F, vs (8/3)ⁿ.
- **Does NOT establish:** Any exponent value stated by the authors; gradient-level statements; same-θ paired comparison.

<a id="B-11"></a>
### B-11 · §IV: purity example and the open question about entangled POVMs
- **Paper:** B
- **Candidate:** CTX; F-D
- **Matrix rows:** —
- **Claim category:** POVM choice and multi-copy measurements under concentration
- **Classification:** EXPLICIT
- **Section:** IV. Practical step-by-step guidelines
- **Subsection:** Subtlety regarding the choice of POVM
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 10 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); absent from v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Two-copy SWAP measurements estimate purity efficiently without concentration. Under a 2-design the landscape variance stays exponentially small, so the advantage vanishes. Whether some entangled POVM could change the indistinguishability conclusion is left open; analysis must use the POVMs employed in practice.
- **Mathematical expression:** —
- **Assumptions:** 2-design.
- **Scope:** Conceptual.
- **Relation to Stage 7:** Positioning context for the readout-dependence question (A4 / B2 belong to the principal and later tracks).
- **Does NOT establish:** Readout exponents.

<a id="B-12"></a>
### B-12 · §IV "Subtlety regarding measure-first-estimate-later approaches", Eq. (11)
- **Paper:** B
- **Candidate:** F-H
- **Matrix rows:** 26
- **Claim category:** Classical-shadow / measure-first schemes are POVM post-processing
- **Classification:** EXPLICIT
- **Section:** IV. Practical step-by-step guidelines
- **Subsection:** Subtlety regarding measure-first-estimate-later approaches
- **Equation:** (11)
- **Figure:** —
- **Appendix:** —
- **Page:** 8–9 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); **absent from v1**
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Post-processing a classical representation built from measurements (e.g. ρ̂_Z) to evaluate an observable is equivalent to implementing that observable's POVM. Concentration results therefore apply however the POVM is realised.
- **Mathematical expression:** ρ̂_Z = (1/N) Σ_i |b_i⟩⟨b_i|
- **Assumptions:** —
- **Scope:** Classical shadows / measure-first schemes.
- **Relation to Stage 7:** Background (post-processing limits).
- **Does NOT establish:** —

<a id="B-13"></a>
### B-13 · §II examples, §IV guidelines, §V: QNG, CVaR, NN-assisted initialisation, rescaled parameter shift
- **Paper:** B
- **Candidate:** F-H; F-G
- **Matrix rows:** 26
- **Claim category:** Optimisation/post-processing strategies do not overcome outcome-probability concentration
- **Classification:** EXPLICIT
- **Section:** II. Framework; IV. Practical step-by-step guidelines; V. Discussion
- **Subsection:** Guideline steps 1–3 and following text
- **Equation:** (6), (7)
- **Figure:** Fig. 4
- **Appendix:** App. C
- **Page:** 4–5, 8, 10; Fig. 4 on p. 6 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); also in v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** By the guidelines (polynomial POVM + concentrated outcome probabilities ⇒ no information), these methods still suffer from exponential concentration, though they may help training in other ways.
- **Mathematical expression:** —
- **Assumptions:** Polynomial POVMs; concentration.
- **Scope:** Named methods.
- **Relation to Stage 7:** Background.
- **Does NOT establish:** —

<a id="B-14"></a>
### B-14 · §I Introduction: the source's own description of the random-walk corollary
- **Paper:** B
- **Candidate:** F-G; C4
- **Matrix rows:** 8
- **Claim category:** Source's own positioning of its random-walk result (self-description)
- **Classification:** EXPLICIT
- **Section:** I. Introduction
- **Subsection:** Final paragraph
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 2 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); also in v1
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** "it had not been proven as far we are aware" (source's own wording about its Corollary 2)
- **Source statement (paraphrase):** The authors say random-walk behaviour of vanilla GD on barren plateaus under practical shot budgets was mentioned in passing earlier (their Ref. [38], Arrasmith et al. 2021) and prove it via Corollary 2 by taking the post-processing to be a gradient calculation.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** Self-description, quoted as the source's own claim; B5 makes no determination.
- **Relation to Stage 7:** Locates the random-walk fact in prior work (this source and its Ref. [38]).
- **Does NOT establish:** Anything beyond the source's own positioning.

<a id="B-15"></a>
### B-15 · §V Discussion and App. D (Eqs. D1–D13): scope limits (exponentially many outcomes)
- **Paper:** B
- **Candidate:** CTX
- **Matrix rows:** —
- **Claim category:** Exponentially-many-element POVMs are outside the framework (counterexample)
- **Classification:** EXPLICIT
- **Section:** V. Discussion; App. D
- **Subsection:** App. D 1 Counter example; App. D 2 Indistinguishable example
- **Equation:** (D1)–(D13)
- **Figure:** —
- **Appendix:** App. D
- **Page:** 10–11; 25–27 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); also in v1 (appendix title differs)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** With exponentially many outcomes, each probability can be exponentially close to its concentration point while the distributions remain distinguishable. A counterexample with an odd/even test is given.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** Scope boundary of the framework.
- **Relation to Stage 7:** Stage 7's two readouts are two-outcome POVMs, inside the framework.
- **Does NOT establish:** —

<a id="B-16"></a>
### B-16 · App. A: Lemmas 1–2, Proposition 1, Definitions 2–4 (Eqs. A1–A23)
- **Paper:** B
- **Candidate:** F-F
- **Matrix rows:** 6
- **Claim category:** Hypothesis-testing tools for statistical indistinguishability
- **Classification:** EXPLICIT
- **Section:** App. A
- **Subsection:** A 1 One sample; A 2 Many samples; A 3 Statistical indistinguishability
- **Equation:** (A1), (A12), (A19), (A23)
- **Figure:** —
- **Appendix:** App. A
- **Page:** 15–18 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); v1 numbering of App. A differs (no Product-distribution definition; A-equations end at (A20))
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** One-sample optimal success = 1/2 + ‖P − P′‖₁/4. For product distributions ‖P − P′‖₁ ≤ Σ‖P_i − P′_i‖₁. With N samples, success ≤ 1/2 + N‖P₀ − P′₀‖₁/4. ε-statistical indistinguishability is defined for distributions and outputs.
- **Mathematical expression:** Pr[right decision] ≤ 1/2 + N‖P₀ − P′₀‖₁/4
- **Assumptions:** Equal priors; independent samples.
- **Scope:** General.
- **Relation to Stage 7:** As A-11. These 1-norm bounds do not separate the two readouts' exponents (B5_MATH_COMPARISON §6.4).
- **Does NOT establish:** Hellinger/variance-based exponents.

### Paper B — not-located search log

All entries below: arXiv v2 read in full (27 pp., main text + Appendices A–D, including figure captions), the
LaTeX source of v2 and v1 read, and text searches of both versions. Common search terms: sign, direction,
conditional, tie, binomial, Skellam, cosine, angle, inner product, norm, exponent, 4^n, 16^n, SNR,
signal-to-noise, sample complexity, gradient variance.

<a id="B-NL13"></a>
### B-NL13 · Conditional Loschmidt sign law
- **Paper:** B
- **Candidate:** C2
- **Matrix rows:** 13
- **Claim category:** P(correct sign | nonzero estimate) for the Loschmidt readout
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–27 (arXiv v2); 1–24 (arXiv v1)
- **Source version:** arXiv:2507.22054v2 (2026-06-04) and v1 (2025-07-29)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed versions after searches for: conditional, given nonzero, sign, direction, single count, (1+|sin|)/2, success probability. The Loschmidt statements are the fixed distribution (0, 1) (B-09a), the per-shot variance F(1 − F) (B-10a) and the overlap-test POVM for kernels (§II p. 5). None concerns signs.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="B-NL14b"></a>
### B-NL14b · Same-objective Loschmidt vs SWAP comparison at the parameter-shift-gradient level
- **Paper:** B
- **Candidate:** C3
- **Matrix rows:** 14b
- **Claim category:** Same-θ, same-gradient comparison of two readouts
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–27 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04) and v1 (2025-07-29)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed versions after searches for: gradient + Loschmidt, gradient + SWAP, parameter shift + fidelity, same landscape. The Loschmidt/SWAP comparison is at the fidelity level under a 2-design (B-09a, B-10a). The parameter-shift analysis (B-06a) is for Pauli observables.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="B-NL17"></a>
### B-NL17 · Explicit 4ⁿ vs 16ⁿ comparison
- **Paper:** B
- **Candidate:** C3
- **Matrix rows:** 17
- **Claim category:** Explicit pair of shot exponents 4ⁿ (LE) and 16ⁿ (SWAP)
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–27 (arXiv v2)
- **Source version:** arXiv:2507.22054v2 (2026-06-04) and v1 (2025-07-29)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed versions after searches for: 4^n, 16^n, 4n, 16n, 2^{2n}, exponent, decades per qubit. The only base-specific shot budgets are the numerical regimes 10 × n, 2ⁿ (Fig. 4) and 150 vs 2¹⁵ (Fig. 3). The general statement is N ∈ Ω(exp(n)).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

---

## Version differences — Aghaei Saem et al., arXiv v1 (2025-07-29) → v2 (2026-06-04)

Method: paragraph-level diff of the two LaTeX sources (140 vs 159 paragraphs, 21 changed blocks) plus a comparison
of equation/figure numbering in both PDFs. Only differences relevant to B5 are listed.

| Id | Change | Where (v2) | Relevance |
|---|---|---|---|
| V-01 | **Inserted:** "Subtlety regarding the choice of POVM": Loschmidt vs SWAP fixed distributions, Eq. (12) ε_N, both estimator variances, purity example, Fig. 5. | §IV, pp. 9–10 | All B-09/B-10/B-11 evidence exists **only in v2**. |
| V-02 | **Inserted:** "Subtlety regarding measure-first-estimate-later approaches", Eq. (11). | §IV, pp. 8–9 | B-12 is v2-only. |
| V-03 | **Inserted:** global Pauli-Z parity POVM example {Π₊, Π₋}. | §II, p. 5 | B-02 is v2-only. |
| V-04 | Fig. 3 caption now defines the plotted quantity (1/N_p)‖θ^(t) − θ^(0)‖₁ over initialisations. | Fig. 3, p. 6 | Clarifies B-07a/B-07b; the random-walk comparison itself is in both versions. |
| V-05 | Corollary 2 (informal) and Corollary 4 (formal) wording: v1 "results in a random walk … the updated parameters … follow"; v2 "is statistically indistinguishable from a random walk … with high probability at least 1 − c … are statistically indistinguishable from the update rule". The sentence after (B26) also changed (v1: the update "does not incorporate information about the current parameter values"; v2: indistinguishable from a parameter-independent random variable "with probability at least exponentially close to 1"). | §III p. 7; App. B pp. 21, 23 | Same mathematical content (B-06a); v2 makes the indistinguishability framing and probability qualifier explicit. |
| V-06 | Definition 1 adds "(which are drawn from some distribution D over a certain domain)" and a following remark on D-dependence. | §III, pp. 5–6 | B-03; no change to the bound. |
| V-07 | App. A: added Definition 2 (Product distribution); "Statistical indistinguishability" definitions renamed "ε-statistical…" and renumbered (v1 Defs. 2–3 → v2 Defs. 3–4; v1 App. A equations end at (A20), v2 at (A23)). | App. A | Cite App. A numbers with the version. App. B–D equation numbers are identical in v1 and v2. |
| V-08 | QNG paragraph expanded (block-diagonal QGT); Appendix D title changed ("exponential support" → "exponentially many elements"). | §II p. 4; App. D | Not candidate-relevant. |

Main-text equations (1)–(10) and Figs. 1–4 have the same numbers in both versions. Eqs. (11)–(12) and Fig. 5 exist
only in v2.

## Open items (not resolved in B5)

1. **Published-version check for paper B.** The IOP version of record (online 2026-01-30) could not be retrieved
   (bot protection on every IOP URL; no repository copy listed by OpenAlex). Because arXiv v2 post-dates
   publication, it most likely reflects the accepted text, but this is **unverified**. In particular, whether the
   version of record contains the v2-only Loschmidt/SWAP passage (V-01) and with which section/equation numbers
   must be checked before any of B-02, B-09, B-10, B-11 or B-12 is cited in a paper.
   **Status after the follow-up audit (2026-10-04): resolved.** The version of record was retrieved through its DOI.
   It contains the V-01 passage in §4 (pp. 9–10; Fig. 5; Eq. (12); both variances on p. 10), V-02 in §4 (pp. 8–9,
   Eq. (11)) and V-03 in §2 (p. 5). Equation, figure, theorem and corollary numbers equal those of arXiv v2. Page
   crosswalk and text comparison: [`B5_VERSION_GAP.md`](B5_VERSION_GAP.md).
2. Paper A's arXiv versions were not compared (not required by the brief). All A locators are to the published
   article and its published SI.

---

# Follow-up audit additions (2026-10-04)

Entries below were added by the targeted follow-up audit ([`B5_FOLLOWUP_AUDIT.md`](B5_FOLLOWUP_AUDIT.md)). They use the
four-label vocabulary only. Matrix rows 29 (gradient-estimator MSE) and 30 (critical copy number) were added to the
matrix in this audit, so papers A and B received one entry each for those rows. No earlier entry was edited.

## Papers A and B — entries for matrix rows 29–30

<a id="A-NL29"></a>
### A-NL29 · Mean-squared error of a finite-shot gradient estimator
- **Paper:** A
- **Candidate:** C1; C3
- **Matrix rows:** 29
- **Claim category:** Mean-squared error (or variance) of a finite-shot gradient estimator
- **Classification:** NOT LOCATED
- **Section:** Whole article (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version (Nat. Commun. 15, 5200; online 2024-06-18) + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: mean squared error, MSE, gradient estimator, parameter shift, finite difference, derivative. The article estimates kernel values (fidelity and projected quantum kernels); it contains no gradient estimator. "Derivative" occurs only in a reference title and in an SI Taylor expansion. Searched in the follow-up audit.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** Stage 7's Var(ĝ_LE) and Var(ĝ_SWAP) are compared with Teo 2023 instead (D-02, D-03b).
- **Does NOT establish:** Absence from the wider literature.

<a id="A-NL30"></a>
### A-NL30 · Critical copy number (estimator crossover)
- **Paper:** A
- **Candidate:** C3
- **Matrix rows:** 30
- **Claim category:** Copy number at which two gradient estimators exchange accuracy
- **Classification:** NOT LOCATED
- **Section:** Whole article (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version (Nat. Commun. 15, 5200; online 2024-06-18) + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: critical, crossover, copy number, copies, finite difference, scaled parameter shift. "Copies" occurs only in multi-copy statements: the SI overview (SI p. 5), Supp. Prop. 4 on coherent multi-copy discrimination (SI pp. 27–28), a SWAP-trick derivation with "two copies of such subsystems" (SI p. 32) and the error-mitigation discussion (SI p. 42). None is an estimator crossover.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** Teo's N_* (D-06) has no counterpart in A.
- **Does NOT establish:** Absence from the wider literature.

<a id="B-17"></a>
### B-17 · App. C "Re-scaled Parameter Shift rule optimization", Eq. (C11): Teo's MSE-minimising factor used in training numerics
- **Paper:** B
- **Candidate:** C3; F-H
- **Matrix rows:** 29
- **Claim category:** Gradient-estimator mean-squared error (finite shots) — matrix row 29
- **Classification:** RELATED BUT DIFFERENT
- **Section:** App. C; IV. Practical step-by-step guidelines
- **Subsection:** Re-scaled Parameter Shift rule optimization; discussion of Fig. 4
- **Equation:** (C11)
- **Figure:** Fig. 4 (d)
- **Appendix:** App. C
- **Page:** 25; Fig. 4 on p. 6; discussion of Fig. 4 on p. 8 (arXiv v2). Version of record: p. 20; Fig. 4 on p. 9; discussion on p. 8
- **Source version:** arXiv:2507.22054v2 (2026-06-04); same text and equation number verified in the version of record (QST 11, 015049; 2026-01-30)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** "a scaling factor that minimizes the mean squared error"
- **Source statement (paraphrase):** B trains with the scaled parameter-shift rule of its ref. [87] (Teo 2023). It describes this rule as using a scaling factor that minimises the mean squared error of loss and gradient estimates, λ = dN/(2d² + Nd − 2), with N "the number of measurement shots" and d = 2ⁿ (Eq. C11). Fig. 4(d) shows that the method still fails to move with 10 × n shots on a global-Z barren-plateau landscape and succeeds with 2ⁿ shots. B writes no MSE expression.
- **Mathematical expression:** λ = dN/(2d² + Nd − 2), d = 2ⁿ
- **Assumptions:** Global Pauli-Z observable; single layer of X rotations; uniform initial parameters; empirical-average post-processing; learning rate η.
- **Scope:** Training numerics (Fig. 4 d). The MSE itself is not analysed in B.
- **Relation to Stage 7:** Identifies Teo 2023 as the source of the MSE-optimised estimator. The λ formula equals Teo's Eq. (22) with Teo's N_T (total copies for one gradient component) in the place of B's N; B does not say whether its N counts shots per shifted circuit or per component (B5_SHOT_CONVENTIONS.md).
- **Does NOT establish:** Any MSE formula, any readout-dependent statement, or Stage 7's per-θ variances.

<a id="B-NL30"></a>
### B-NL30 · Critical copy number (estimator crossover)
- **Paper:** B
- **Candidate:** C3
- **Matrix rows:** 30
- **Claim category:** Copy number at which two gradient estimators exchange accuracy
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–27 (arXiv v2); 1–24 (version of record)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); the version of record (QST 11, 015049) was also searched
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed versions after searches for: critical, crossover, copy number, copies, finite difference, scaled parameter shift. B uses Teo's scaled estimator (B-17) but does not mention Teo's critical copy number. "Copies" occurs only in the purity example (two copies with a SWAP test, B-11).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

---

## Paper C — Arrasmith, Cerezo, Czarnik, Cincio, Coles, Quantum 5, 558 (2021)

<a id="C-01"></a>
### C-01 · §2.3 Definition 1 (barren plateau), Eqs. (4)–(5)
- **Paper:** C
- **Candidate:** F-A
- **Matrix rows:** 1
- **Claim category:** Fidelity exponential concentration — matrix row 1
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 2 Theoretical Background
- **Subsection:** 2.3 Barren Plateaus — Definition 1
- **Equation:** (4), (5)
- **Figure:** —
- **Appendix:** —
- **Page:** 4
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** "the barren plateau phenomenon is a probabilistic statement"
- **Source statement (paraphrase):** A cost exhibits a barren plateau if, for every parameter, E_θ[∂_μC(θ)] = 0 and Var_θ[∂_μC(θ)] ≤ F(n) with F(n) ∈ O(1/bⁿ), b > 1; expectations are over θ. By Chebyshev, P(|∂_μC| ≥ c) ≤ Var_θ[∂_μC]/c², so a random initialisation lands, with high probability, in a region of exponentially small gradients.
- **Mathematical expression:** Var_θ[∂_μC(θ)] ≤ F(n), F(n) ∈ O(1/bⁿ); P(|∂_μC(θ)| ≥ c) ≤ Var_θ[∂_μC(θ)]/c²
- **Assumptions:** Cost C(θ) = Σ_x f_x(θ, ρ_x) (Eq. 1); m ∈ O(poly(n)) parameters, each entering through e^(−iθ_μH_μ) with H_μ having two distinct non-zero eigenvalues.
- **Scope:** Concentration of the exact gradient of a general cost; probability over θ, not over measurement outcomes. Fidelity is not singled out.
- **Relation to Stage 7:** The Stage 3–7 global fidelity cost satisfies this definition (Stage 3: Var_θ[∂_kC] = (1/8)(3/8)^(n−1)). The definition concerns the exact gradient's spread over θ, not finite-shot estimators.
- **Does NOT establish:** Fidelity-estimate behaviour, any finite-shot estimator law, or readout dependence.

<a id="C-02"></a>
### C-02 · §3.1 Proposition 1 and Corollary 1, Eqs. (6)–(12); App. A, Eqs. (16)–(25): exponentially suppressed cost differences
- **Paper:** C
- **Candidate:** F-A; C3
- **Matrix rows:** 1
- **Claim category:** Fidelity exponential concentration — matrix row 1
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 3 Main Results; App. A
- **Subsection:** 3.1 Exponentially suppressed cost differences — Proposition 1, Corollary 1; A Proof of Proposition 1
- **Equation:** (6)–(12); (16)–(25)
- **Figure:** —
- **Appendix:** App. A
- **Page:** 5–6; 11–12
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** "this is a direct consequence of the fact that the cost exhibits a barren plateau"
- **Source statement (paraphrase):** For θ_B = θ_A + Lℓ̂ with θ_A random, E_θA[ΔC] = 0 and Var_θA[ΔC] ≤ G(n) = m²L²F(n) ∈ Õ(1/bⁿ) (Prop. 1). For independent random θ_A, θ_B the same holds with Ĝ(n) = m²L̄²F(n) (Cor. 1). Chebyshev then gives P(|ΔC| ≥ c) ≤ G(n)/c² (Eq. 12). Proof: ΔC is a line integral of ∇C; covariances of gradient components are bounded by Cauchy–Schwarz (App. A).
- **Mathematical expression:** E[ΔC] = 0; Var[ΔC] ≤ G(n) = m²L²F(n); P(|ΔC| ≥ c) ≤ G(n)/c²
- **Assumptions:** Definition 1 holds; m ∈ O(poly(n)); L ∈ O(poly(n)) (on a torus L ≤ √m·π, Eq. 13).
- **Scope:** Exact (noise-free) cost values at random parameter points. No measurement model.
- **Relation to Stage 7:** Landscape-level reason why any finite-shot comparison of two cost values needs exponential precision. Stage 7's parameter-shift difference (F₋ − F₊ at shift π/2) is one such difference; Stage 7 derives its estimator distribution, which this proposition does not address.
- **Does NOT establish:** A shot-noise distribution, P(ĝ = 0), sign probabilities, or readout dependence.

<a id="C-03"></a>
### C-03 · Abstract, §1 and §3.2: exponential precision and exponentially scaling sampling requirements
- **Paper:** C
- **Candidate:** C3; F-E
- **Matrix rows:** 5
- **Claim category:** Exponential finite-shot (precision) burden for optimisation on a barren plateau
- **Classification:** EXPLICIT
- **Section:** Abstract; 1 Introduction; 3 Main Results
- **Subsection:** 3.2 Implications for gradient-free optimizers
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1, 6
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** "without exponential precision, gradient-free optimizers will not make progress in the optimization"
- **Source statement (paraphrase):** Exponentially suppressed gradients mean that exponential precision is needed to make progress (introduction). Because cost differences are exponentially suppressed (Prop. 1), gradient-free optimisers likewise need exponential precision, i.e. sampling requirements that scale exponentially (§3.2).
- **Mathematical expression:** —
- **Assumptions:** Barren plateau per Definition 1; m, L ∈ O(poly(n)).
- **Scope:** Gradient-free optimisers (Nelder–Mead, Powell, COBYLA); gradient-based ones in the introduction. The base of the exponential is not specified and no measurement model is given.
- **Relation to Stage 7:** General exponential-shot statement of the kind Stage 5 §13 and Stage 7 §19 already treat as known. No readout dependence.
- **Does NOT establish:** A base (4ⁿ, 16ⁿ), readout dependence, or a per-θ statistic.

<a id="C-04a"></a>
### C-04a · §4 Numerical Implementation, Eqs. (14)–(15), Fig. 3: median total shots to reach C = 0.4 grow exponentially
- **Paper:** C
- **Candidate:** C3; F-E
- **Matrix rows:** 5
- **Claim category:** Numerical exponential growth of the total shots needed to start training
- **Classification:** EXPLICIT
- **Section:** 4 Numerical Implementation; 5 Discussion
- **Subsection:** —
- **Equation:** (14), (15)
- **Figure:** Fig. 3
- **Appendix:** —
- **Page:** 6–8
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** "the total number of shots scales exponentially with n for the Powell method"
- **Source statement (paraphrase):** Quantum-compiling toy problem (U = 𝟙, target |0⟩^⊗n) with the local cost C = Tr[O_L V|0⟩⟨0|V†], O_L = 𝟙 − (1/n)Σ_i|0_i⟩⟨0_i| (Eqs. 14–15), a layered hardware-efficient ansatz with p = n layers, n = 5–11, random initialisation and 20 runs per setting. For each n the shots N per cost evaluation were scanned and the N that reaches C = 0.4 with the smallest median total shot count N_total was kept. Median N_total grows exponentially (Powell), super-exponentially (Nelder–Mead), at least exponentially but irregularly (COBYLA), and exponentially for a gradient-descent reference. The authors call the exponential scaling a lower bound on the asymptotics.
- **Mathematical expression:** C(θ) = Tr[O_L V(θ)|0⟩⟨0|V†(θ)], O_L = 𝟙 − (1/n) Σ_i |0_i⟩⟨0_i|
- **Assumptions:** Default optimiser hyper-parameters; the threshold C = 0.4 probes the initial stage of training; N optimised separately for each n.
- **Scope:** Numerical, n = 5–11; local cost; median over 20 runs; no fitted exponent reported.
- **Relation to Stage 7:** Same qualitative conclusion (exponentially many shots), but with a different cost (local, hardware-efficient ansatz), a different statistic (median total shots to a cost threshold) and unspecified estimator details for the gradient-descent reference.
- **Does NOT establish:** A per-θ required-shot statistic, a base of the exponential, or a readout comparison.

<a id="C-04b"></a>
### C-04b · Fig. 3 gradient-descent reference read against gradient-level shot exponents
- **Paper:** C
- **Candidate:** C3
- **Matrix rows:** 15, 16
- **Claim category:** Gradient-level shot-complexity exponent for a specific readout
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 4 Numerical Implementation
- **Subsection:** —
- **Equation:** (14), (15)
- **Figure:** Fig. 3 (black crosses, "gradient descent")
- **Appendix:** —
- **Page:** 7
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** "As expected, the total number of shots also scales exponentially in this case"
- **Source statement (paraphrase):** Fig. 3 includes a "custom gradient-descent optimizer" as a reference; its median N_total also grows exponentially for n = 5–11. The paper gives no gradient estimator, shift rule, per-component shot allocation or fitted exponent for it.
- **Mathematical expression:** —
- **Assumptions:** As C-04a.
- **Scope:** One gradient-based reference curve. The cost observable is built from single-qubit projectors |0_i⟩⟨0_i| (Eq. 15); the measurement circuit is not described (an efficient circuit is cited to ref. [12], p. 7). It is neither the Loschmidt (global projector) nor the SWAP readout.
- **Relation to Stage 7:** Exponential growth for a gradient-based optimiser is consistent with Stage 7, but readout, statistic (total shots to a threshold vs per-θ shots for SNR/sign targets) and cost all differ. No exponent is reported, so 4ⁿ/16ⁿ cannot be compared.
- **Does NOT establish:** A Loschmidt or SWAP exponent, or readout dependence.

<a id="C-05a"></a>
### C-05a · §3.2: shot-noise-driven decisions make optimisers random walks or random sampling (the remark cited "in passing")
- **Paper:** C
- **Candidate:** C4; F-G
- **Matrix rows:** 8
- **Claim category:** Parameter-shift random-walk behaviour — matrix row 8
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 3 Main Results
- **Subsection:** 3.2 Implications for gradient-free optimizers (opening paragraph)
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 6
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** "leading to many optimizers effectively becoming either random walks or random sampling"
- **Source statement (paraphrase):** When an optimiser's precision requirements are not met, each decision it makes is randomly chosen by shot noise, so many optimisers effectively become random walks or random sampling. It is a one-sentence remark, without proof or numerics, in the context of gradient-free optimisers. It is the only random-walk sentence in the paper, and the passage Aghaei Saem et al. cite ([38]) as mentioning random-walk behaviour in passing (B-14).
- **Mathematical expression:** —
- **Assumptions:** Precision requirement not met (implicitly: shot noise much larger than cost differences).
- **Scope:** Qualitative; gradient-free optimisers (simplex, line-search and trust-region methods).
- **Relation to Stage 7:** Qualitative precursor of Stage 7 §17's SWAP random-walk diagnostic. It concerns gradient-free methods and has no control or statistic; it is not about parameter-shift gradient descent.
- **Does NOT establish:** A proof, a parameter-shift statement, a matched-start comparison or a signal-free control.

<a id="C-05b"></a>
### C-05b · §3.2: distinguishing cost values at different parameters is the core of gradient-free optimisation
- **Paper:** C
- **Candidate:** C3; F-F
- **Matrix rows:** 6
- **Claim category:** Outcome-distribution distinguishability framework — matrix row 6
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 3 Main Results
- **Subsection:** 3.2 Implications for gradient-free optimizers (opening paragraph)
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 6
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** "the capability of distinguishing the cost function value at different sets of parameters"
- **Source statement (paraphrase):** The precision needed to tell cost values apart fundamentally limits gradient-free methods; smaller differences need greater precision. The argument uses variances of exact cost differences (Chebyshev), not outcome distributions or hypothesis tests.
- **Mathematical expression:** —
- **Assumptions:** As C-02.
- **Scope:** Exact cost differences; no measurement model.
- **Relation to Stage 7:** Related to the resolution view of Stage 7 §15 (information distances). Stage 7 compares the outcome distributions of two shifted circuits under a given readout, a different object.
- **Does NOT establish:** Outcome-level distinguishability bounds or readout dependence.

<a id="C-06"></a>
### C-06 · §5 Discussion: the choice of optimiser does not avoid the exponential scaling
- **Paper:** C
- **Candidate:** F-H; C4
- **Matrix rows:** 26
- **Claim category:** Limits of classical post-processing / mitigation (fact H) — matrix row 26
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 5 Discussion
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 8
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** "Our work casts doubt on the notion that the choice of optimizer could provide"
- **Source statement (paraphrase):** The choice of optimiser is unlikely to avoid barren plateaus, although a careful choice may extend the size limits of trainable problems. Neural-network or natural-evolution strategies may improve the constants, but all require comparing cost values at different points and are subject to the same scaling analysis. Powell probably scales better because statistical noise does not accumulate in its state.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** Optimisation strategies; not post-processing of outcomes or error mitigation.
- **Relation to Stage 7:** Background for fact H (limits of workarounds), at the level of optimisers rather than A's/B's post-processing theorems.
- **Does NOT establish:** Outcome-level or readout-level statements.

<a id="C-07"></a>
### C-07 · §2.2.1 Nelder–Mead: noisy comparisons cause premature shrink operations
- **Paper:** C
- **Candidate:** C1; C4
- **Matrix rows:** —
- **Claim category:** Exact gradient sign probabilities P_correct / P_wrong (C1 context; no matrix row)
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 2 Theoretical Background; 5 Discussion
- **Subsection:** 2.2.1 Nelder-Mead
- **Equation:** —
- **Figure:** Fig. 1 (a)
- **Appendix:** —
- **Page:** 3–4, 8
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** "this algorithm is vulnerable to performing shrink operations prematurely"
- **Source statement (paraphrase):** When errors in the cost values are large enough to cause mistakes in Nelder–Mead's comparisons, the algorithm may shrink prematurely, slowing optimisation and possibly giving a false appearance of convergence (citing Barton & Ivey 1991). The Discussion tentatively ("likely") attributes Nelder–Mead's super-exponential shot scaling to this effect (p. 8).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** Qualitative; simplex comparisons, not gradient signs.
- **Relation to Stage 7:** Qualitative analogue of a wrong-decision probability. Stage 7's P_wrong is an exact gradient-sign probability.
- **Does NOT establish:** Any probability of a wrong decision.

### Paper C — not-located search log

Paper C was read in full (12 pp. incl. App. A) and its LaTeX source was searched.

<a id="C-NL09"></a>
### C-NL09 · Exact finite-shot gradient distribution, P_zero, P_correct, P_wrong, full-vector zero probability
- **Paper:** C
- **Candidate:** C1
- **Matrix rows:** 9, 10, 11, 12, 19
- **Claim category:** Exact law of a finite-shot gradient estimator and its zero/sign probabilities
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + App. A)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–12
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: binomial, Bernoulli, distribution, probability, zero, tie, sign, correct, wrong, parameter shift, estimator, shot noise. The only probabilities are Chebyshev bounds over random parameters (Eqs. 5, 12), not over measurement outcomes. Qualitative decision-error remarks are recorded in C-05a and C-07.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="C-NL13"></a>
### C-NL13 · Conditional Loschmidt sign law
- **Paper:** C
- **Candidate:** C2
- **Matrix rows:** 13
- **Claim category:** P(correct | ĝ ≠ 0) → (1 + |sin θ_k|)/2 for the Loschmidt gradient
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + App. A)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–12
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: conditional, sign, direction, non-zero, single count, Loschmidt, projector, (1 + sin)/2. No Loschmidt readout and no gradient-sign statistic appear. "Conditional comparisons" refers to Nelder–Mead's operations (p. 3).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="C-NL02"></a>
### C-NL02 · Loschmidt/SWAP readouts, readout-dependent exponents, 4ⁿ vs 16ⁿ
- **Paper:** C
- **Candidate:** C3
- **Matrix rows:** 2, 3, 4, 14a, 14b, 17, 18
- **Claim category:** Readout-specific estimator behaviour and readout-dependent shot exponents
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + App. A)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–12
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: Loschmidt, echo, SWAP, swap test, fidelity, POVM, measurement scheme, readout, estimator variance, 4^n, 16^n, exponent, slope. "Fidelity" occurs only in reference titles. The only measured quantity is the local cost of Eqs. (14)–(15), and no exponent value is stated.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="C-NL20"></a>
### C-NL20 · Vector alignment, norm, dot-sign, component sign, matched starts, signal-free control
- **Paper:** C
- **Candidate:** C4
- **Matrix rows:** 20, 21, 22, 23, 24, 25
- **Claim category:** Full-vector reliability metrics and controlled trajectory comparisons
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + App. A)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–12
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: cosine, angle, alignment, inner product, norm, sign, trajectory, control, same initial, matched, random walk (numerics). Fig. 3 uses 20 random initialisations per setting; whether the same initial points are shared across optimisers or across N values is not stated. The random-walk statement is qualitative (C-05a).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="C-NL07"></a>
### C-NL07 · Parameter-shift analysis, product-rotation landscape, global-Z parity numerics, gradient MSE, critical copy number
- **Paper:** C
- **Candidate:** C1; C3; CTX
- **Matrix rows:** 7, 27, 28, 29, 30
- **Claim category:** Finite-shot parameter-shift statistics and related context items
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + App. A)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–12
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: parameter shift, gradient estimator, mean squared error, MSE, finite difference, critical, copies, product state, single layer, global Z, parity. "Mean squared-error" occurs only as an example cost (p. 2), and "finite differences" are exact cost differences (App. A, Eq. 19). The gradient-descent reference of Fig. 3 has no stated estimator (C-04b). The ansatz is a layered hardware-efficient circuit with CNOTs (Fig. 2), not a product of single-qubit rotations.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

---

## Paper D — Teo, Phys. Rev. A 107, 042421 (2023), reviewed as arXiv:2206.12643v3

All D locators (section, equation, figure, table, page) are arXiv v3 locators. The APS version of record was not
inspected (B5_VERSION_GAP.md). "TDS" = two-design-sandwich condition (Case I of the source's Fig. 7).

<a id="D-01"></a>
### D-01 · §II–§III, Eqs. (1)–(4), (7): measurement model and the circuit-averaged MSE figure of merit
- **Paper:** D
- **Candidate:** C1; C3
- **Matrix rows:** 7, 29
- **Claim category:** Finite-copy estimation model and mean-squared-error figure of merit for gradient estimators
- **Classification:** EXPLICIT
- **Section:** II. Background: variational quantum algorithms; III. Figure of merit: mean squared-error; IV A
- **Subsection:** —
- **Equation:** (1)–(4), (7)
- **Figure:** Fig. 2, Fig. 7
- **Appendix:** App. A 3 (conditions for circuit averaging)
- **Page:** 2–4; 13–14
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** "is sampled independently for the same set of PEPQC parameters"
- **Source statement (paraphrase):** f_Q(θ; x) = ⟨0|U†OU|0⟩ with O = Σ_k h_k O_k/‖h‖, O_k multiqubit Pauli operators (eigenvalues ±1). Each O_k is measured independently in its eigenbasis, giving multinomial counts with N clicks per measured function. Accuracy is the MSE averaged over sampling, over the circuit ensemble (⟨·⟩, Haar averages for two-design modules) and over the non-trainable inputs x (Eq. 2). Gradient errors split into a finite-copy part and an approximation (nonzero-ε) part (Eq. 7). Exact MSEs require the TDS condition; other cases of Fig. 7 give upper bounds.
- **Mathematical expression:** MSE(Y) = ⟨E[(Ŷ − Y)²]⟩ (also averaged over x); MSE(Y) = Σ_k h_k² MSE(Ŷ_k)/‖h‖² for unbiased Ŷ_k (p. 4)
- **Assumptions:** Pauli-encoded parametrized quantum circuits (PEPQCs); Pauli observables; independent sampling of each O_k; two-design trainable modules (TDS) for exact expressions.
- **Scope:** Circuit-averaged errors; Pauli observables; any n.
- **Relation to Stage 7:** Stage 7's statistic is per θ (no circuit average) on a product landscape that is not a two-design, and Stage 7's Loschmidt readout is a global projector, not a Pauli observable.
- **Does NOT establish:** Fixed-θ distributions, sign probabilities, or projector-readout statistics.

<a id="D-02"></a>
### D-02 · §IV B, Eqs. (11)–(13): the parameter-shift estimator and its finite-copy MSE
- **Paper:** D
- **Candidate:** C1; C3
- **Matrix rows:** 7, 29
- **Claim category:** Finite-copy MSE of the parameter-shift gradient estimator
- **Classification:** EXPLICIT
- **Section:** IV. Results: sampling errors in gradient and Hessian estimations
- **Subsection:** B. Parameter-shift rule
- **Equation:** (11)–(13)
- **Figure:** —
- **Appendix:** App. C 1–C 2 (sampling identities)
- **Page:** 4–5; 18–19
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** "The corresponding MSEs are therefore just finite-copy errors given by"
- **Source statement (paraphrase):** PS gradient estimator [f(θ+s) − f(θ−s)]/(2 sin s) (Eq. 11). Under TDS, MSE_PS(∂f) = d/(N_T(d+1) sin² s) ≥ d/(N_T(d+1)) (Eq. 13), minimised at s = π/2. N_T is the total-copy convention defined on p. 4 for FD approximators (N_T = 2N per gradient component per basis observable, split equally between the two functions). §IV B uses the same N_T for PS without redefining it; Eq. (13) is consistent with that split (our check).
- **Mathematical expression:** MSE_PS(∂f_Q) = d/(N_T(d+1) sin² s); at s = π/2, d/(N_T(d+1)) ≈ 1/N_T
- **Assumptions:** TDS; Pauli observable; independent sampling; equal copy split between the two shifted circuits.
- **Scope:** Circuit-averaged MSE (sampling plus two-design circuit average).
- **Relation to Stage 7:** With N_T = 2M this is d/(2M(d+1)) ≈ 1/(2M), the same value as Stage 7's SWAP variance deep in the plateau ([2 − A²(1+s²)/2]/(4M) → 1/(2M)), because both are averages of ±1-outcome variances (our comparison). Teo does not treat the Loschmidt (0/1 projector) readout, whose gradient variance is ≈ A/(4M).
- **Does NOT establish:** The per-θ variance on a non-two-design landscape (implied only, D-03b), distributions, or sign probabilities.

<a id="D-03a"></a>
### D-03a · Eqs. (4), (11) and App. C 1, Eq. (C1): estimator built from multinomial relative frequencies; moments only
- **Paper:** D
- **Candidate:** C1
- **Matrix rows:** 12
- **Claim category:** Structure of the finite-copy PS estimator (difference of two empirical means) vs its exact law
- **Classification:** RELATED BUT DIFFERENT
- **Section:** III; IV B; App. C
- **Subsection:** App. C 1 Multinomial sampling distribution
- **Equation:** (4), (11), (C1)
- **Figure:** —
- **Appendix:** App. C 1
- **Page:** 4–5; 18–19
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** —
- **Source statement (paraphrase):** f̂ = Σ_k (h_k/‖h‖) Σ_l o_kl ν_kl with multinomial relative frequencies ν_kl (Eq. 4); the PS estimator is the difference of two such estimates divided by 2 sin s (Eq. 11). App. C 1 states the moments of the ν_kl up to second order (Eq. C1). The finite-copy part of every MSE follows from these moments; the approximation part uses the circuit averages of App. B.
- **Mathematical expression:** E[ν_kl(θ)] = p_kl(θ); E[ν_kl(θ) ν_kl′(θ′)] = (1 − δ_θθ′δ_xx′) p_kl(θ) p_kl′(θ′) + (δ_θθ′δ_xx′/N)[δ_ll′ p_kl + (N − 1) p_kl p_kl′] (Eq. C1)
- **Assumptions:** Independent multinomial sampling; circuits with different parameters sampled independently.
- **Scope:** Moments up to second order only.
- **Relation to Stage 7:** Stage 5–7 use the full difference-of-binomials law of this kind of estimator. Teo's moments fix Var(ĝ) but not P(ĝ = 0), P_correct, P_wrong or the tie probability.
- **Does NOT establish:** The pmf, the tie probability, or zero/sign probabilities.

<a id="D-03b"></a>
### D-03b · App. C 1–C 2, Eqs. (C1)–(C2) with Eq. (13): per-θ ±1-outcome variance that reproduces Stage 7's SWAP gradient variance (implied)
- **Paper:** D
- **Candidate:** C3
- **Matrix rows:** 16
- **Claim category:** Gradient shot-complexity exponent for a ±1-outcome (SWAP-type) readout
- **Classification:** PARTIAL / IMPLIED
- **Section:** IV B; App. C
- **Subsection:** App. C 1 Multinomial sampling distribution; App. C 2 Function estimation
- **Equation:** (13), (C1), (C2)
- **Figure:** —
- **Appendix:** App. C 1–C 2
- **Page:** 5; 18–19
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** —
- **Source statement (paraphrase):** Eq. (C2) gives MSE(f_Q) = (1/N_T)(1 − ⟨f²⟩) for a Pauli observable: the circuit average of the per-θ ±1 variance (1 − f²)/N that follows from (C1). Teo writes only the averaged form, and Eq. (13) is its two-design average for the PS difference.
- **Mathematical expression:** Implied (our algebra), at Teo's shift π/2: Var[PS(θ)] = [2 − f(θ + (π/2)e_k)² − f(θ − (π/2)e_k)²]/(2N_T)
- **Assumptions:** Added by this audit: per-θ use of (C1); the SWAP-test ancilla Z (±1 outcomes, mean F) as the Pauli observable; N_T = 2M; Stage 7's product landscape (F± = A(1∓s)/2); a per-θ SNR or sign target; the median over θ with the log-typical A = 4^(−(n−1)).
- **Scope:** Implied only. Teo performs none of these steps (B5_TEO_DEEP_AUDIT.md §9; B5_MATH_COMPARISON.md §8). The label applies to the per-θ variance structure. The 16ⁿ base itself comes from Stage 7's landscape and median statistic (Teo's own ensemble implies 2ⁿ), so for the exponent alone RELATED BUT DIFFERENT would also be defensible.
- **Relation to Stage 7:** With these additions the expression equals Stage 7's Var(ĝ_SWAP) = [2 − A²(1+s²)/2]/(4M) exactly (checked numerically), and the median required M grows ≈ 16ⁿ. Under Teo's own two-design average a mean-square criterion gives N_T ≈ 2d (2ⁿ); on Stage 7's landscape a mean-square criterion gives (8/3)ⁿ. The 16ⁿ base needs the per-θ median statistic.
- **Does NOT establish:** The Loschmidt 4ⁿ (a projector readout lies outside Teo's Pauli model), the readout comparison, or any explicit exponent.

<a id="D-04"></a>
### D-04 · §V A, Eqs. (17)–(18), and §VIII: the average squared PS estimate stays at the sampling level 1/N_T
- **Paper:** D
- **Candidate:** C4; C3
- **Matrix rows:** 3, 21
- **Claim category:** SWAP estimator random / data-independent limit (row 3); gradient norm inflation (row 21)
- **Classification:** RELATED BUT DIFFERENT
- **Section:** V. Results: optimally-tuned numerical estimators; VIII. Conclusion
- **Subsection:** A. Optimal FD estimators
- **Equation:** (17), (18)
- **Figure:** —
- **Appendix:** Tab. I (App. B 5)
- **Page:** 6, 12, 18
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** "estimates gradients and Hessians with errors that are asymptotically independent of the circuit-qubit number"
- **Source statement (paraphrase):** In the large-d limit under TDS, the circuit-averaged squared magnitude of the optimal FD estimator tends to [sinc(ε_opt/2)]²/(2d) + 4/(N_T ε_opt²), whereas for PS ⟨E[(PS)²]⟩ → 1/(2d) + 1/N_T → 1/N_T (Eqs. 17–18). The PS estimate's average squared magnitude therefore stays at the n-independent sampling level while the true ⟨(∂f)²⟩ ≈ 1/(2d) vanishes. The conclusion (p. 12) restates that PS errors are asymptotically independent of the qubit number.
- **Mathematical expression:** PS: ⟨E[(∂f̂)²]⟩ → 1/(2d) + 1/N_T → 1/N_T
- **Assumptions:** TDS; large d; Pauli observable.
- **Scope:** Circuit-averaged, per component.
- **Relation to Stage 7:** Our algebra: the ratio of mean-square estimate to mean-square gradient is 1 + 2d/N_T. This is a circuit-averaged, component-wise analogue of Stage 7's SWAP norm inflation (‖ĝ‖/‖g‖ ≈ 10^4.5 at n = 12, M = 1024, a per-θ median of a full-vector ratio), and the ±1-outcome analogue of the SWAP null (estimates dominated by sampling noise). Teo states neither comparison.
- **Does NOT establish:** A vector norm ratio, a per-θ median, or the Loschmidt contrast (where estimates collapse to exactly 0 instead).

<a id="D-05a"></a>
### D-05a · §IV A, §IV C, §V A–C, Eqs. (8), (14)–(16), (19)–(23), Figs. 3–4: MSEs of FD, GD and SPS estimators and their optimisation
- **Paper:** D
- **Candidate:** C3
- **Matrix rows:** 29
- **Claim category:** Finite-copy MSE of tunable gradient estimators (finite difference, generalized difference, scaled PS)
- **Classification:** EXPLICIT
- **Section:** IV A; IV C; V A–C; VI A
- **Subsection:** —
- **Equation:** (8), (14)–(16), (19)–(23)
- **Figure:** Fig. 3, Fig. 4
- **Appendix:** App. C 3–C 5
- **Page:** 4–9; 19–22
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** "they decrease exponentially with the number of qubits n"
- **Source statement (paraphrase):** MSE_FD(∂f) = 4d/(N_T(d+1)ε²) + d²[1 − sinc(ε/2)]²/(2(d+1)(d²−1)) (Eq. 8); ε_opt ≅ (2304(d²−1)/(N_T d))^(1/6) (Eq. 15); MSE_FD,opt(∂f) ≅ (3/32)^(1/3) d^(4/3)/((d+1)(d²−1)^(1/3) N_T^(2/3)) (Eq. 16), which decreases exponentially in n at fixed N_T. SPS: MSE_SPS(∂f) = dλ²/(N_T(d+1) sin² s) + d²(1−λ)²/(2(d+1)(d²−1)) (Eq. 14); λ_opt = dN_T/(2d² + dN_T − 2) (Eq. 22); MSE_SPS,opt(∂f) = d²/((d+1)(2d² + dN_T − 1)) (Eq. 23, as printed [sic]: minimising Eq. 14 gives − 2, consistent with Eqs. 22 and C18; B5_TEO_DEEP_AUDIT.md §6). Monte Carlo checks for a supervised-learning task and an 8-qubit water-molecule Hamiltonian (Fig. 4).
- **Mathematical expression:** As in the paraphrase.
- **Assumptions:** TDS for the exact forms, upper bounds otherwise (App. C 3–C 5); N_T ≫ d for the approximations (15)–(16).
- **Scope:** Circuit-averaged MSE; estimator design.
- **Relation to Stage 7:** Stage 7 uses only the unscaled PS estimator at s = π/2. These results concern estimator choice at a fixed readout, not readout choice at a fixed estimator.
- **Does NOT establish:** Readout dependence or zero/sign probabilities.

<a id="D-05b"></a>
### D-05b · Eqs. (16)–(18), §V A and Fig. 6: the estimator choice changes the n-dependence of the gradient error at fixed copies
- **Paper:** D
- **Candidate:** C3
- **Matrix rows:** 18
- **Claim category:** Measurement scheme changing the gradient-resolution exponent — matrix row 18
- **Classification:** RELATED BUT DIFFERENT
- **Section:** V A; VII. Important remarks and potential pitfall
- **Subsection:** A. Optimal FD estimators
- **Equation:** (16), (17), (18)
- **Figure:** Fig. 6
- **Appendix:** —
- **Page:** 6, 10–11
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** —
- **Source statement (paraphrase):** At fixed N_T the optimal FD (and GD, SPS) MSEs fall exponentially with n, tracking the true ⟨(∂f)²⟩ ≤ O(1/d), while the PS MSE stays ≈ 1/N_T. ε_opt grows roughly exponentially with n (Fig. 6). The estimator, applied to the same Pauli measurements, changes how the gradient error scales with n.
- **Mathematical expression:** —
- **Assumptions:** TDS; Pauli observables.
- **Scope:** Estimator choice (classical processing of the same measurements); circuit-averaged.
- **Relation to Stage 7:** Stage 7 changes the readout (projector vs SWAP) with the PS estimator fixed, and finds different required-shot exponents. Teo changes the estimator with the readout fixed. Both compare statistics for one task, but along different axes.
- **Does NOT establish:** A readout comparison or a required-shot exponent.

<a id="D-06"></a>
### D-06 · §VI B, Eqs. (24)–(25), Fig. 5: critical copy number N_*
- **Paper:** D
- **Candidate:** C3
- **Matrix rows:** 30
- **Claim category:** Critical copy number below which optimised difference estimators beat the parameter shift
- **Classification:** EXPLICIT
- **Section:** Abstract; VI. Performance; VIII. Conclusion
- **Subsection:** B. Benefits of optimized numerical estimators for scalable NISQ devices
- **Equation:** (24), (25)
- **Figure:** Fig. 5
- **Appendix:** App. B, App. C (general cases)
- **Page:** 1, 9–10, 12
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** "this critical number grows exponentially with the circuit-qubit number"
- **Source statement (paraphrase):** N_* is the N_T at which MSE_FD/GD,opt = MSE_PS. Under TDS and for N_* ≫ d: N_* ≅ 32(d²−1)/(3d) for gradients, 81(d²−1)/(16d) for diagonal and 9(d²−1)²/d³ for off-diagonal Hessian components (Eq. 24), with loose lower bounds for GD (Eq. 25). Hence N_* ≳ O(2ⁿ); Fig. 5 shows exponential growth of N_* for n = 1–9. Below N_* the optimised difference estimator has the smaller average error.
- **Mathematical expression:** N_* ≅ 32(d² − 1)/(3d) ≈ (32/3)·2ⁿ (gradient components)
- **Assumptions:** TDS; N_* ≫ d; FD with the approximate ε_opt.
- **Scope:** A comparison of two estimators' circuit-averaged MSEs.
- **Relation to Stage 7:** Not a resolution threshold. Our algebra: at N_T = N_*, MSE_PS/⟨(∂f)²⟩ = 2(d²−1)/(N_* d) = 3/16, so the crossover lies where PS already resolves the gradient in mean square. In Stage 7's convention (N_T = 2M) N_* corresponds to M_* ≈ (16/3)·2ⁿ, a 2ⁿ base unrelated to the 4ⁿ/16ⁿ per-θ medians.
- **Does NOT establish:** Required shots for gradient resolution or sign reliability, or any readout dependence.

<a id="D-07a"></a>
### D-07a · §VII, Eq. (26): relative spread D_θ0 and the exponential copy requirement for trainability
- **Paper:** D
- **Candidate:** C3; F-E
- **Matrix rows:** 5
- **Claim category:** Exponential sampling-copy requirement to distinguish shifted function values
- **Classification:** EXPLICIT
- **Section:** VII. Important remarks and potential pitfall
- **Subsection:** —
- **Equation:** (26)
- **Figure:** —
- **Appendix:** —
- **Page:** 11
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** "N must thus at least be exponentially large in n for trainability"
- **Source statement (paraphrase):** Trainability needs a small D_θ0 = ⟨max{Var[f̂(θ ± θ0)]}/|f(θ+θ0) − f(θ−θ0)|²⟩, the worst-case average relative spread of two shifted estimates. For circuits of large d with two-design properties the numerator approaches O(1/N) and the denominator is at most O(1/poly d), so D_θ0 ≳ O(poly(d)/N) and N must be at least exponentially large in n.
- **Mathematical expression:** D_θ0 = ⟨max{Var[f̂(θ ± θ0)]}/|f(θ+θ0) − f(θ−θ0)|²⟩ ≳ O(poly(d)/N)
- **Assumptions:** Large d; two-design circuits; numerator O(1/N) (Pauli ±1 outcomes); order-of-magnitude argument.
- **Scope:** Resolution of a function difference in one direction; the base of the exponential is not given.
- **Relation to Stage 7:** The located statement closest to Stage 7's per-θ SNR criterion: D_θ0 is a circuit average of an inverse squared SNR of the shifted-value difference. Teo's O(1/N) numerator is the ±1 (SWAP-type) case; for the Loschmidt readout the numerator is O(F/N). Our algebra: on Stage 7's landscape the literal average diverges (E_θ[1/A] = ∞), so Stage 7 uses medians (B5_STATISTIC_COMPARISON.md).
- **Does NOT establish:** 4ⁿ or 16ⁿ, readout dependence, or sign probabilities.

<a id="D-07b"></a>
### D-07b · §VII, Eq. (26) read against outcome-level distinguishability frameworks
- **Paper:** D
- **Candidate:** C3; F-F
- **Matrix rows:** 6
- **Claim category:** Outcome-distribution distinguishability framework — matrix row 6
- **Classification:** RELATED BUT DIFFERENT
- **Section:** VII. Important remarks and potential pitfall
- **Subsection:** —
- **Equation:** (26)
- **Figure:** —
- **Appendix:** —
- **Page:** 11
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** —
- **Source statement (paraphrase):** D_θ0 quantifies the failure to distinguish f(θ+θ0) from f(θ−θ0) through sampling by a variance-to-squared-difference ratio. No hypothesis test, outcome distribution or distance between distributions is used.
- **Mathematical expression:** See D-07a.
- **Assumptions:** As D-07a.
- **Scope:** Variance-ratio criterion.
- **Relation to Stage 7:** Stage 7 §15 (TV/Hellinger) works with outcome distributions. Teo's variance ratio coincides with an SNR criterion, not with A's/B's 1-norm hypothesis tests.
- **Does NOT establish:** Hellinger/TV statements or readout dependence.

<a id="D-08a"></a>
### D-08a · §VII: a small MSE can still give many wrong update directions
- **Paper:** D
- **Candidate:** C1; C4
- **Matrix rows:** 10, 11, 23
- **Claim category:** Exact gradient P_correct, P_wrong and component sign accuracy — matrix rows 10, 11, 23
- **Classification:** RELATED BUT DIFFERENT
- **Section:** VII. Important remarks and potential pitfall
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 11
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** "could still lead to many wrong update directions"
- **Source statement (paraphrase):** For very large n, where the true gradient is tiny, even a very small gradient-estimation MSE could still lead to many wrong update directions from slight statistical fluctuations, so cost minimisation can be very slow on average; one should be strict about picking the right descent direction. Stated qualitatively; no probability is computed.
- **Mathematical expression:** —
- **Assumptions:** Very large n; tiny true gradient.
- **Scope:** Qualitative.
- **Relation to Stage 7:** Qualitative counterpart of Stage 7's exact P_correct/P_wrong and component sign accuracy (§9, §14). Teo gives no sign probability, no conditional law and no readout contrast.
- **Does NOT establish:** Any sign probability, the conditional Loschmidt sign law, or P(ĝ = 0).

<a id="D-08b"></a>
### D-08b · §VII: accurate estimation and trainability are separate problems
- **Paper:** D
- **Candidate:** F-H
- **Matrix rows:** 26
- **Claim category:** Limits of classical post-processing / mitigation (fact H) — matrix row 26
- **Classification:** RELATED BUT DIFFERENT
- **Section:** VII. Important remarks and potential pitfall
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 10–11
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** "These are clearly two separate problems"
- **Source statement (paraphrase):** Optimised estimators can boost estimation accuracy, but this does not necessarily improve trainability under barren plateaus, which the article does not address. In a hypothetical n → ∞ example, near-zero estimation error does not make an almost flat landscape trainable.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** Qualitative remark.
- **Relation to Stage 7:** Consistent with fact H. B's App. C describes Teo's method as claimed to improve training on barren-plateau landscapes (B-17), whereas Teo's §VII says estimation accuracy and trainability are separate problems. The audit records both statements and takes no position.
- **Does NOT establish:** An outcome-level impossibility statement.

<a id="D-09"></a>
### D-09 · §I and §VIII: optimised estimators avoid "random guesses"; PS errors do not shrink with n
- **Paper:** D
- **Candidate:** C4; F-G
- **Matrix rows:** 8
- **Claim category:** Parameter-shift random-walk behaviour — matrix row 8
- **Classification:** RELATED BUT DIFFERENT
- **Section:** I. Introduction; VIII. Conclusion
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–2, 12
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** "prevent the optimally-tuned estimators from effectively making random guesses"
- **Source statement (paraphrase):** Because the optimised estimators' errors scale with the exponentially small gradient magnitudes, they avoid "random guesses" about the components at a fixed copy number, in contrast to the unscaled PS estimator whose errors are asymptotically independent of n. No optimisation trajectory or random-walk analysis is given.
- **Mathematical expression:** —
- **Assumptions:** As D-04.
- **Scope:** Estimate level; qualitative wording.
- **Relation to Stage 7:** Related to the SWAP failure mode (random signs) at the estimate level. Stage 7's random-walk statement concerns trajectories with a matched control.
- **Does NOT establish:** Random-walk dynamics, a control, or trajectory statistics.

<a id="D-10"></a>
### D-10 · App. B, Tab. I and Eqs. (B19), (C3): circuit-averaged squared gradient components are at most O(1/d)
- **Paper:** D
- **Candidate:** F-A
- **Matrix rows:** 1
- **Claim category:** Fidelity exponential concentration — matrix row 1
- **Classification:** RELATED BUT DIFFERENT
- **Section:** App. B; V A
- **Subsection:** B 2 Averages of gradient components; B 5 Summary table
- **Equation:** (B19), (B20), (B24), (C3)
- **Figure:** Tab. I
- **Appendix:** App. B 2–B 5; App. C 2
- **Page:** 6, 16, 18–19
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** "manifestations of the so-called barren-plateau phenomenon"
- **Source statement (paraphrase):** ⟨(∂f)²⟩ = d²/(2(d+1)(d²−1)) under TDS (Case I) and at most O(1/d) in all cases (Tab. I); ⟨f²⟩ = 1/(d+1) (Eq. C3). The text calls these averages manifestations of the barren-plateau phenomenon.
- **Mathematical expression:** ⟨(∂f_Q,k)²⟩_I = d²/(2(d+1)(d²−1)); ⟨f_Q,k²⟩ = 1/(d+1)
- **Assumptions:** Haar two-design modules; Pauli observables.
- **Scope:** Two-design circuit averages.
- **Relation to Stage 7:** Gradient concentration under two-designs. Stage 7's landscape is a product (non-two-design) landscape with Var_θ[∂_kC] = (1/8)(3/8)^(n−1) and log-typical A = 4^(−(n−1)). Fidelity concentration is not discussed.
- **Does NOT establish:** Fidelity concentration or product-landscape statistics.

### Paper D — not-located search log

Paper D (arXiv v3) was read in full (24 pp., Apps. A–D) and its LaTeX source was searched.

<a id="D-NL09"></a>
### D-NL09 · Exact zero probabilities: P(ĝ = 0) and the full-vector zero probability
- **Paper:** D
- **Candidate:** C1; C4
- **Matrix rows:** 9, 19
- **Claim category:** Probability that a finite-shot gradient estimate (component or vector) is exactly zero
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–24 (arXiv v3)
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: zero, exactly zero, tie, equal counts, probability, binomial, Poisson, vanishing estimate. The results are MSEs (second moments) averaged over circuits; no probability of a zero estimate is written.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="D-NL13"></a>
### D-NL13 · Conditional Loschmidt sign law
- **Paper:** D
- **Candidate:** C2
- **Matrix rows:** 13
- **Claim category:** P(correct | ĝ ≠ 0) → (1 + |sin θ_k|)/2 for the Loschmidt gradient
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–24 (arXiv v3)
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: conditional, sign, direction, non-zero, single count, projector, Loschmidt, (1 + sin)/2. §VII mentions wrong update directions qualitatively (D-08a); there is no conditional law and no projector readout.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="D-NL02"></a>
### D-NL02 · Loschmidt and SWAP readouts, and comparisons between them
- **Paper:** D
- **Candidate:** C3
- **Matrix rows:** 2, 4, 14a, 14b, 15
- **Claim category:** Readout-specific estimator behaviour (Loschmidt projector, SWAP test) and their comparison
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–24 (arXiv v3)
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: Loschmidt, echo, SWAP test, swap (only the swap operator τ of the Haar integrals, Eq. A3), fidelity, projector, overlap, POVM, readout, measurement scheme. "Fidelity" refers only to hardware fidelities (p. 1). All observables are Pauli sums measured term by term in their eigenbases. A 0/1 projector readout, whose per-shot variance F(1−F) underlies Stage 7's Loschmidt 4ⁿ, does not appear.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="D-NL17"></a>
### D-NL17 · Explicit 4ⁿ vs 16ⁿ comparison
- **Paper:** D
- **Candidate:** C3
- **Matrix rows:** 17
- **Claim category:** Explicit pair of shot exponents 4ⁿ (Loschmidt) and 16ⁿ (SWAP)
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–24 (arXiv v3)
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: 4^n, 16^n, 2^{2n}, 2^{4n}, d², d⁴ (as copy scalings), exponent, decades. The stated growth laws are N_* ≳ O(2ⁿ) (Eq. 24, Fig. 5) and D_θ0 ≳ O(poly(d)/N) (Eq. 26).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="D-NL20"></a>
### D-NL20 · Vector alignment, dot-sign, matched starts, signal-free control
- **Paper:** D
- **Candidate:** C4
- **Matrix rows:** 20, 22, 24, 25
- **Claim category:** Full-vector reliability metrics and controlled trajectory comparisons
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–24 (arXiv v3)
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: cosine, angle, alignment, inner product, full gradient vector, trajectory, matched, same initial, random walk, control. Fig. 4 concerns the initial optimisation step; no trajectories are simulated.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="D-NL27"></a>
### D-NL27 · Product single-qubit-rotation landscape and global-Z parity numerics
- **Paper:** D
- **Candidate:** CTX
- **Matrix rows:** 27, 28
- **Claim category:** Stage 3–7 landscape family and the Stage 6 parity benchmark
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–24 (arXiv v3)
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: product state, single layer, tensor product, RX, global Z, parity. "Product state" refers only to the initial input state |0⟩ (p. 2). The numerics use hardware-efficient circuits taken as approximate two-designs, the observable Y ⊗ 1^(n−1) (supervised-learning task) and a 96-term water-molecule Hamiltonian (App. D, Tab. II).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

---

## Paper E — Gentinetta, Thomsen, Sutter, Woerner, Quantum 8, 1225 (2024)

Notation clash: in paper E, **M is the training-set size** and **R the shots per kernel entry or expectation value**.
In Stage 7, M is the shots per shifted circuit.

<a id="E-01"></a>
### E-01 · §1 Introduction: quantum-kernel concentration needs exponentially many measurements; the paper assumes it away
- **Paper:** E
- **Candidate:** F-A; F-E
- **Matrix rows:** 1, 5
- **Claim category:** Fidelity-kernel exponential concentration and exponential measurement burden (background)
- **Classification:** EXPLICIT
- **Section:** 1 Introduction; 5 Conclusion
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 2, 18
- **Source version:** Published version (Quantum 8, 1225; 2024-01-11) = arXiv:2203.00031v2 file
- **Source URL:** https://doi.org/10.22331/q-2024-01-11-1225
- **Short quote:** "an exponential number of measurements is necessary to distinguish the kernel evaluations"
- **Source statement (paraphrase):** Quantum kernels can suffer from exponential concentration if the feature map is not chosen carefully (citing Thanasilp et al. [9]); an exponential number of measurements is then needed to distinguish kernel values. The paper studies training and assumes a reasonably chosen feature map (the noisy-halfspace-learning assumption, Assumption 1). The conclusion repeats that the kernel must not suffer from exponential concentration.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** Background statement attributed to [9]; not analysed in this paper.
- **Relation to Stage 7:** Known territory (facts A and E), as in paper A.
- **Does NOT establish:** Any readout-level or gradient-level statement.

<a id="E-02"></a>
### E-02 · Fig. 1, Eq. (9), §4.2 and App. A.1, Eqs. (20)–(25): the all-zero-outcome kernel estimator and its Bernoulli statistics
- **Paper:** E
- **Candidate:** C1; C3; F-D
- **Matrix rows:** 4
- **Claim category:** Different Loschmidt / SWAP estimator variances — matrix row 4
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 2.3 Quantum support vector machines; 3.1 Dual optimization; 4.2 Dual optimization; App. A.1
- **Subsection:** Fig. 1 Quantum kernel estimation; A.1 Justification of (10)
- **Equation:** (9), (20)–(25)
- **Figure:** Fig. 1
- **Appendix:** App. A.1
- **Page:** 6–8, 12, 21–22
- **Source version:** Published version (Quantum 8, 1225; 2024-01-11) = arXiv:2203.00031v2 file
- **Source URL:** https://doi.org/10.22331/q-2024-01-11-1225
- **Short quote:** "the frequency of the all zero outcome approximates the kernel value"
- **Source statement (paraphrase):** The kernel k(x_i, x_j) = |⟨ψ(x_i)|ψ(x_j)⟩|² is estimated by preparing E(x_j)†E(x_i)|0⟩, measuring all qubits and taking the frequency of the all-zero bit string over R shots (Fig. 1, Eq. 9). Each shot is Bernoulli with mean k. E[(k_R − k)²] = (1/R²)[Rk + 2·C(R,2)k²] − k² ≤ k/R and the fourth moment is O(1/R²) (Eqs. 23–25). In the numerics, noisy entries are drawn from the binomial distribution B(R, K_ij) (§4.2). No SWAP-test estimator appears.
- **Mathematical expression:** E[|(E_R)_ij|²] = (1/R²)[R k_ij + 2 C(R,2) k_ij²] − k_ij² ≤ k_ij/R
- **Assumptions:** i.i.d. shots; exact Bernoulli model; no hardware noise.
- **Scope:** Fidelity (kernel) estimate; used only as input to a classical optimisation.
- **Relation to Stage 7:** This is the Loschmidt readout of Stages 5–7 at the fidelity level, and the written expression simplifies to k(1−k)/R (our algebra; the source writes the bound ≤ k/R): the variance of the R-shot mean, i.e. the Loschmidt per-shot variance k(1−k) divided by R. There is no SWAP comparison and no gradient.
- **Does NOT establish:** Different variances for two readouts of one quantity, or gradient-level statistics.

<a id="E-03"></a>
### E-03 · §3.1, Eqs. (10)–(11), App. A.2 Lemma 5, Eq. (37): shot complexity of the dual QSVM
- **Paper:** E
- **Candidate:** C3
- **Matrix rows:** —
- **Claim category:** Gradient shot-complexity exponent in n (C3 context; no matrix row)
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 3 Analytical complexity; 4.2 Dual optimization; 5 Conclusion; App. A
- **Subsection:** 3.1 Dual optimization; A.2 Justification of (11)
- **Equation:** (10), (11), (27), (37)
- **Figure:** Fig. 5, Fig. 6
- **Appendix:** App. A.1–A.2
- **Page:** 8–9, 12–14, 18, 23–26
- **Source version:** Published version (Quantum 8, 1225; 2024-01-11) = arXiv:2203.00031v2 file
- **Source URL:** https://doi.org/10.22331/q-2024-01-11-1225
- **Short quote:** "which entails a significant overhead over training a classical SVM due to shot noise"
- **Source statement (paraphrase):** E‖K_R − K‖₂ = O(√(M/R)) (Latała's theorem; Eqs. 10, 27). Under Assumption 1, R = O(M^(8/3)/ε²) shots per kernel entry give |h_R − h| ≤ ε with probability > 1/2 (Lemma 5, Eq. 37), so R_tot = O(M^4.67/ε²) over the O(M²) entries (Eq. 11). Empirically R ≈ ε^(−2) (fits −1.989 to −1.998; the text calls R = O(1/ε²) tight) and R_tot ∝ M^(4.5–4.8) (Figs. 5–6, Table 2). The quote is from the Conclusion (p. 18). M is the training-set size and ε the decision-function accuracy.
- **Mathematical expression:** R_tot = O(M^4.67/ε²)
- **Assumptions:** Noisy halfspace learning (Assumption 1); no exponential concentration; the quadratic program is solved classically.
- **Scope:** Kernel training complexity in M and ε at fixed n; no n-dependence and no parameter-shift gradients.
- **Relation to Stage 7:** A different quantity: it must not be read as a VQA gradient shot complexity. Notation clash: E's M is the data-set size, Stage 7's M the shots per shift.
- **Does NOT establish:** Any gradient-level or n-dependent shot exponent.

<a id="E-04"></a>
### E-04 · §3.2, Assumption 2, Eqs. (12)–(14), §4.3 and App. B: shot complexity of the primal (Pegasos) QSVM
- **Paper:** E
- **Candidate:** C3
- **Matrix rows:** —
- **Claim category:** Gradient shot-complexity exponent in n (C3 context; no matrix row)
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 2.2; 3 Analytical complexity; 4.3 Primal optimization via Pegasos; 5 Conclusion; App. B
- **Subsection:** 3.2 Primal optimization via Pegasos
- **Equation:** (12)–(14), (16), (17)
- **Figure:** Fig. 7, Fig. 8, Fig. 9
- **Appendix:** App. B.1–B.2
- **Page:** 3, 5–6, 9–10, 13–16, 18, 27–29
- **Source version:** Published version (Quantum 8, 1225; 2024-01-11) = arXiv:2203.00031v2 file
- **Source URL:** https://doi.org/10.22331/q-2024-01-11-1225
- **Short quote:** "provides a scaling that is independent of M"
- **Source statement (paraphrase):** Pegasos (stochastic sub-gradient descent on the kernelised primal) updates integer coefficients classically from noisy kernel entries (Algorithm 1). Under Assumption 2 (empirically supported in App. B.1) the total shots are O(min{M²/(λ³ε⁶), 1/(λ⁵ε¹⁰)}); empirically O(1/ε^(8.3±1.6)) (separable) and O(1/ε^(9.5±1.0)) (overlapping data) (Table 2). The quote is from the Conclusion (p. 18); the introduction (p. 3) makes the same point.
- **Mathematical expression:** R_tot = O(min{M²/(λ³ε⁶), 1/(λ⁵ε¹⁰)})
- **Assumptions:** Assumption 2 (convergence unaffected once the sum in line 14 of Algorithm 1 is δ-accurate); strong convexity (App. B.2).
- **Scope:** Classical optimisation of kernel coefficients; the gradient is a classical sub-gradient computed from estimated kernel values.
- **Relation to Stage 7:** Shot noise enters a classical gradient through kernel estimates, not through a parameter-shift rule on circuit parameters.
- **Does NOT establish:** VQA parameter-shift gradient statistics.

<a id="E-05"></a>
### E-05 · §2.4 and §4.4, Eqs. (7)–(8), (18)–(19), Figs. 2, 10–11: approximate QSVM trained with SPSA from finite-shot expectation values
- **Paper:** E
- **Candidate:** C3; C4
- **Matrix rows:** 28
- **Claim category:** Global-Z (parity) parameter-shift training numerics on a single rotation layer — matrix row 28
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 2.4 Approximate quantum support vector machines; 4.4 Heuristic training of approximate QSVMs; 5 Conclusion
- **Subsection:** —
- **Equation:** (7), (8), (18), (19)
- **Figure:** Fig. 2, Fig. 10, Fig. 11
- **Appendix:** —
- **Page:** 7–8, 14–18
- **Source version:** Published version (Quantum 8, 1225; 2024-01-11) = arXiv:2203.00031v2 file
- **Source URL:** https://doi.org/10.22331/q-2024-01-11-1225
- **Short quote:** "which ensures that the scaling is independent of d"
- **Source statement (paraphrase):** h_θ(x) = ⟨ψ(x)|W(θ)†Z^⊗q W(θ)|ψ(x)⟩ with trainable θ (Eq. 7), a global observable (p. 8 contrasts it with a local one). Each ±1 outcome Q gives (1+Q)/2 ~ Bernoulli(p) with σ_Q² ≤ 1, so R = O(1/ε²) shots per expectation value; with an assumed O(1/ε) convergence rate, R_tot = O(1/ε³) (Eq. 18, conjectured). Training uses SPSA with SGD on batches of 5 (cost independent of the number of parameters d) and Qiskit's shot-based simulator. Empirically R_tot = O(1/ε^(2.9±0.3)) (Table 2), from the 2-dimensional-data runs with 8 trainable parameters (Fig. 11: exponents 2.86 and 2.79); 8-dimensional data with 16 parameters gives exponents ≈ 2.2. No parameter-shift rule is mentioned; the statevector reference uses full gradient descent without stating how the gradient is computed.
- **Mathematical expression:** σ_Q² = 4p(1 − p) ≤ 1; R = O(1/ε²); R_tot = O(1/ε³)
- **Assumptions:** O(1/ε) convergence assumed (footnote 9). Model choice to avoid barren plateaus (§2.4, p. 8); loss function and initial parameters must not cause trainability problems (Conclusion, p. 18).
- **Scope:** The only part of the paper with variational parameters; two fixed problem sizes (2- and 8-dimensional data, one feature per qubit per §4.1), so no n-scaling.
- **Relation to Stage 7:** For row 28: a global Z^⊗q observable trained with finite shots, but with SPSA (not parameter shift) on ZZFeatureMap + RealAmplitudes circuits (not a single rotation layer), with ε-scaling at fixed size. Stage 6's parity benchmark and B-07a/B-08b use parameter shift on a single RX layer. A different estimator and statistic from Stage 7's n-scaling of parameter-shift gradient reliability.
- **Does NOT establish:** Parameter-shift statistics, readout dependence, or n-exponents.

<a id="E-06"></a>
### E-06 · §4.4, Eq. (19): the noiseless reference optimisation is started from the noisy-trained parameters
- **Paper:** E
- **Candidate:** C4
- **Matrix rows:** 24
- **Claim category:** Matched-start finite-shot optimisation trajectories — matrix row 24
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 4.4 Heuristic training of approximate QSVMs
- **Subsection:** —
- **Equation:** (19)
- **Figure:** Fig. 11
- **Appendix:** —
- **Page:** 16–17
- **Source version:** Published version (Quantum 8, 1225; 2024-01-11) = arXiv:2203.00031v2 file
- **Source URL:** https://doi.org/10.22331/q-2024-01-11-1225
- **Short quote:** "converged to given the initial parameters"
- **Source statement (paraphrase):** After 1000 shot-based training steps (giving θ_R), a full-gradient statevector optimisation starting from θ_R gives θ_∞, and ε = max_x |h_θR(x) − h_θ∞(x)| is recorded. This is repeated over random initialisations and several R.
- **Mathematical expression:** ε := max_x |h_θR(x) − h_θ∞(x)| (Eq. 19)
- **Assumptions:** —
- **Scope:** The reference run starts from the noisy endpoint, not from a shared initial point; the comparison uses decision-function distance, not fidelity endpoints.
- **Relation to Stage 7:** Stage 7 §17 runs SWAP-, Loschmidt- and exact-gradient descent and a signal-free random walk from identical starts and compares endpoints. Paper E's pairing is a warm-started reference without a signal-free control.
- **Does NOT establish:** Matched-start trajectory comparisons or random-walk controls.

### Paper E — not-located search log

Paper E was read in full (30 pp., Apps. A–C) and its LaTeX source was searched.

<a id="E-NL09"></a>
### E-NL09 · Exact gradient distribution and zero/sign probabilities
- **Paper:** E
- **Candidate:** C1
- **Matrix rows:** 9, 10, 11, 12, 19
- **Claim category:** Exact law of a finite-shot gradient estimator and its zero/sign probabilities
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–C)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–30
- **Source version:** Published version (Quantum 8, 1225; 2024-01-11) = arXiv:2203.00031v2 file
- **Source URL:** https://doi.org/10.22331/q-2024-01-11-1225
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: parameter shift, gradient estimator, zero, tie, sign, probability, difference of binomial, Skellam. The binomial law appears only for a single kernel entry (E-02). The only gradient-type objects are Pegasos sub-gradients (classical) and SPSA estimates, whose distributions are not analysed.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="E-NL13"></a>
### E-NL13 · Conditional Loschmidt sign law
- **Paper:** E
- **Candidate:** C2
- **Matrix rows:** 13
- **Claim category:** P(correct | ĝ ≠ 0) → (1 + |sin θ_k|)/2 for the Loschmidt gradient
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–C)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–30
- **Source version:** Published version (Quantum 8, 1225; 2024-01-11) = arXiv:2203.00031v2 file
- **Source URL:** https://doi.org/10.22331/q-2024-01-11-1225
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: conditional, sign, direction, non-zero, single count, Loschmidt, (1 + sin)/2. The all-zero-outcome kernel estimator is of Loschmidt type (E-02), but no gradient of it and no sign statistic is considered.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="E-NL02"></a>
### E-NL02 · Readout comparisons and gradient shot exponents in n
- **Paper:** E
- **Candidate:** C3
- **Matrix rows:** 2, 3, 14a, 14b, 15, 16, 17, 18
- **Claim category:** Readout-specific estimator behaviour and n-dependent gradient shot exponents
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–C)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–30
- **Source version:** Published version (Quantum 8, 1225; 2024-01-11) = arXiv:2203.00031v2 file
- **Source URL:** https://doi.org/10.22331/q-2024-01-11-1225
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: SWAP, swap test, Loschmidt, echo, projector, POVM, readout, measurement scheme, 4^n, 16^n, exponential in n, number of qubits, collapse. One kernel readout (all-zero frequency) is used. The approximate QSVM uses a second readout (±1 outcomes of Z^⊗q, σ_Q² ≤ 1, p. 15) for a different quantity, and the two are never compared. The complexities are polynomial in M and ε at fixed n (E-03 to E-05), so no n-exponent is stated, and exponential concentration is assumed away (E-01).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="E-NL08"></a>
### E-NL08 · Random walk, vector metrics, signal-free control
- **Paper:** E
- **Candidate:** C4
- **Matrix rows:** 8, 20, 21, 22, 23, 25
- **Claim category:** Random-walk behaviour, full-vector reliability metrics and signal-free controls
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–C)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–30
- **Source version:** Published version (Quantum 8, 1225; 2024-01-11) = arXiv:2203.00031v2 file
- **Source URL:** https://doi.org/10.22331/q-2024-01-11-1225
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: random walk, cosine, angle, alignment, norm, sign, control, random baseline. The closest item is the warm-started noiseless reference (E-06).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="E-NL06"></a>
### E-NL06 · Distinguishability framework, parameter-shift analysis, post-processing limits, product landscape, parity numerics, gradient MSE, critical copy number
- **Paper:** E
- **Candidate:** C1; C3; CTX
- **Matrix rows:** 6, 7, 26, 27, 29, 30
- **Claim category:** Outcome-level distinguishability, parameter-shift statistics and related context items
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–C)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–30
- **Source version:** Published version (Quantum 8, 1225; 2024-01-11) = arXiv:2203.00031v2 file
- **Source URL:** https://doi.org/10.22331/q-2024-01-11-1225
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: hypothesis test, distinguish (only in the background sentence of E-01), parameter shift, mean squared error, MSE, critical, crossover, copies, error mitigation, product, single-qubit rotations. Footnote 7 (p. 12) chooses very large R so that ‖K − K_R‖ < μ holds; this is a sufficient-shot condition, not an estimator crossover. The feature map (Fig. 3) is a ZZ-entangling circuit, not a product of rotations. The global Z^⊗q observable of the approximate QSVM is recorded under row 28 (E-05).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

---

# Closure audit additions (2026-10-05)

Entries below were added by the B5 closure audit ([`B5_CLOSURE_AUDIT.md`](B5_CLOSURE_AUDIT.md)). They use the
four-label vocabulary only. Matrix rows 31–33 were added for the principal track's candidate statements C5 and the
general form of C2 (`principal/QLO_Principal_Track.md` §3, upstream commit 8003375). Papers A–E received one or two
entries each for those rows. Papers F–H were added in this audit. No earlier entry was edited.

## Papers A–E — entries for matrix rows 31–33

<a id="A-19"></a>
### A-19 · Outcome models of both readouts read against the gradient-level shot-ratio identity and the exponent rule
- **Paper:** A
- **Candidate:** C5; C3
- **Matrix rows:** 31, 32
- **Claim category:** SWAP/Loschmidt shot-ratio identity for parameter-shift gradients and the exponent rule — matrix rows 31, 32
- **Classification:** PARTIAL / IMPLIED
- **Section:** Results; SI Note III
- **Subsection:** Why exponential concentration is problematic; SI III A 1 (Loschmidt Echo test), SI III A 2 (SWAP test)
- **Equation:** (12), (14); SI (17), (46)
- **Figure:** —
- **Appendix:** SI Note III A
- **Page:** 4; SI 6, 9
- **Source version:** Published version (Nat. Commun. 15, 5200; online 2024-06-18) + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Both outcome models are stated for one fidelity (kernel) value κ: the Loschmidt Echo test assigns outcome 1 to the all-zero bitstring, which occurs with probability κ (p. 4; SI Eq. 17), and the SWAP test gives +1 with probability p₊ = 1/2 + κ/2 (p. 4; SI Eq. 46). The source writes no per-shot variance (A-08b), no parameter-shift gradient, no shot ratio and no exponent relation. Searched in the closure audit.
- **Mathematical expression:** Implied (our algebra): per-shot variances κ(1 − κ) (Loschmidt) and 1 − κ² (SWAP estimate 2K/N − 1); at the two shifts R = [2 − F₊² − F₋²]/[F₊(1 − F₊) + F₋(1 − F₋)] → 2/S as S = F₊ + F₋ → 0; with median log-slopes b_S, b_r, b_SW − b_LE ≈ b_S (to leading order as S → 0)
- **Assumptions:** Added (ours): the kernel value replaced by a parametrised fidelity F(θ); parameter shift with one independent batch of M shots per shift; for row 32, an ensemble over θ in which S concentrates and the median log-slopes b_S and b_r exist (principal track §3 definitions); the medians of log₁₀S and log₁₀|r| must combine additively (e.g. linear trends in n with O(1) fluctuations), and the rule holds only to leading order as S → 0, so it is approximate.
- **Scope:** The source is at the kernel (fidelity-estimate) level; no gradients and no landscape slopes.
- **Relation to Stage 7:** These are the Stage 7 outcome models (B5_POTENTIAL_ISSUES numerical cross-check). The principal track's A2 proof cites the per-shot variances of paper B (B-18); A states the outcome models from which they follow in one line.
- **Does NOT establish:** The ratio identity, the exponent rule, the quantity r or b_r, or any gradient-level statement.

<a id="A-NL33"></a>
### A-NL33 · General conditional Loschmidt sign law (1 + |r|)/2
- **Paper:** A
- **Candidate:** C2
- **Matrix rows:** 33
- **Claim category:** P(correct | ĝ ≠ 0) → (1 + |r|)/2, r = (F₋ − F₊)/(F₊ + F₋), on arbitrary circuits — matrix row 33
- **Classification:** NOT LOCATED
- **Section:** Whole article (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** main 1–13; SI 1–51
- **Source version:** Published version (Nat. Commun. 15, 5200; online 2024-06-18) + Supplementary Information (MOESM1)
- **Source URL:** https://doi.org/10.1038/s41467-024-49287-w
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: conditional, non-zero estimate, single count, relative gradient, sign accuracy, Poisson thinning, (1 + |r|)/2. As for the product-circuit form (A-NL13), the article contains no gradient estimator. Searched in the closure audit.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="B-18"></a>
### B-18 · §IV per-shot variances read against the gradient-level shot-ratio identity and the exponent rule
- **Paper:** B
- **Candidate:** C5; C3
- **Matrix rows:** 31, 32
- **Claim category:** SWAP/Loschmidt shot-ratio identity for parameter-shift gradients and the exponent rule — matrix rows 31, 32
- **Classification:** PARTIAL / IMPLIED
- **Section:** IV. Practical step-by-step guidelines
- **Subsection:** Subtlety regarding the choice of POVM
- **Equation:** (12) + inline variances
- **Figure:** Fig. 5
- **Appendix:** —
- **Page:** 9–10 (arXiv v2). Version of record: §4, p. 10
- **Source version:** arXiv:2507.22054v2 (2026-06-04); the identical passage was verified in the version of record (QST 11, 015049; 2026-01-30)
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** "These distinct forms of variance result in different statistical behaviors"
- **Source statement (paraphrase):** Per-shot variances Var^(SWAP) = 1 − F² and Var^(LE) = F(1 − F) are stated for the same fidelity, next to the resolution ratio ε_N of Eq. (12). The source forms no shot ratio, does not apply the variances to parameter-shift gradients and states no exponent relation (B-NL14b, B-NL17). The principal track's A2 proof of the ratio identity applies exactly these variances at the two shifts. Searched in the closure audit.
- **Mathematical expression:** Implied (our algebra): R = [2 − F₊² − F₋²]/[F₊(1 − F₊) + F₋(1 − F₋)] → 2/S; b_SW − b_LE ≈ b_S (to leading order as S → 0) for median log-slopes
- **Assumptions:** Added (ours): parameter shift with one independent batch per shift; for row 32, an ensemble over θ with median log-slopes b_S and b_r; the medians of log₁₀S and log₁₀|r| must combine additively (e.g. linear trends in n with O(1) fluctuations), and the rule holds only to leading order as S → 0, so it is approximate.
- **Scope:** Fidelity level under a 2-design in the source; gradient level and slopes only via the added steps.
- **Relation to Stage 7:** Same implication as B-10c (rows 15, 16, 18), here for the general identity of the principal track rather than for the product-landscape bases.
- **Does NOT establish:** The identity or the rule as stated results; the quantity r; any conditional sign law.

<a id="B-NL33"></a>
### B-NL33 · General conditional Loschmidt sign law (1 + |r|)/2
- **Paper:** B
- **Candidate:** C2
- **Matrix rows:** 33
- **Claim category:** P(correct | ĝ ≠ 0) → (1 + |r|)/2 on arbitrary circuits — matrix row 33
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–27 (arXiv v2); 1–24 (version of record)
- **Source version:** arXiv:2507.22054v2 (2026-06-04); the version of record (QST 11, 015049) was also searched
- **Source URL:** https://arxiv.org/abs/2507.22054v2
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed versions after searches for: conditional, non-zero, single count, relative gradient, sign accuracy, Poisson thinning, (1 + |r|)/2. The Loschmidt fixed distribution (0, 1) is stated (B-09a); what a non-zero Loschmidt estimate implies about the sign is not discussed. Searched in the closure audit.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="C-NL31"></a>
### C-NL31 · Shot-ratio identity, exponent rule and general conditional sign law
- **Paper:** C
- **Candidate:** C5; C2
- **Matrix rows:** 31, 32, 33
- **Claim category:** Gradient-level readout shot ratio, exponent rule and general conditional sign law — matrix rows 31–33
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + App. A)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–12
- **Source version:** Published version (Quantum 5, 558; 2021-10-05) = arXiv:2011.12245v2 file
- **Source URL:** https://doi.org/10.22331/q-2021-10-05-558
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: ratio, readout, swap, Loschmidt, per-shot variance, slope, exponent, conditional, sign, relative gradient. The paper has no measurement model for its analytic result (C-02) and one local-cost readout in its numerics (C-04a). Searched in the closure audit.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="D-11"></a>
### D-11 · Teo's per-θ ±1 variance read against the shot-ratio identity and the exponent rule
- **Paper:** D
- **Candidate:** C5; C3
- **Matrix rows:** 31, 32
- **Claim category:** SWAP/Loschmidt shot-ratio identity for parameter-shift gradients and the exponent rule — matrix rows 31, 32
- **Classification:** RELATED BUT DIFFERENT
- **Section:** IV B; V A; App. C
- **Subsection:** App. C 1 Multinomial sampling distribution; App. C 2 Function estimation
- **Equation:** (13), (16)–(18), (C1), (C2)
- **Figure:** —
- **Appendix:** App. C 1–C 2
- **Page:** 5–6; 18–19
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** —
- **Source statement (paraphrase):** Teo's model contains only ±1 (Pauli) per-shot variances, which correspond to the SWAP side of the identity (D-03b); the 0/1 projector readout is absent (D-NL02), so no ratio between two readouts can be formed from the source. Its exponent comparisons concern estimators (FD/GD/SPS vs PS) applied to the same measurements (D-05b), not readouts. Searched in the closure audit.
- **Mathematical expression:** —
- **Assumptions:** Two-design (TDS) circuit averages; Pauli observables.
- **Scope:** Estimator comparison at a fixed readout.
- **Relation to Stage 7:** Supplies the SWAP-side gradient variance structure only (B5_MATH_COMPARISON §8.2–§8.3).
- **Does NOT establish:** The ratio identity, the exponent rule or the Loschmidt-side variance.

<a id="D-NL33"></a>
### D-NL33 · General conditional Loschmidt sign law (1 + |r|)/2
- **Paper:** D
- **Candidate:** C2
- **Matrix rows:** 33
- **Claim category:** P(correct | ĝ ≠ 0) → (1 + |r|)/2 on arbitrary circuits — matrix row 33
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–24 (arXiv v3)
- **Source version:** arXiv:2206.12643v3 (2022-11-20; journal-ref Phys. Rev. A 107, 042421); APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2206.12643v3
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: conditional, non-zero, single count, relative gradient, sign accuracy, Poisson thinning, (1 + |r|)/2. §VII mentions wrong update directions qualitatively (D-08a). Searched in the closure audit.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="E-NL31"></a>
### E-NL31 · Shot-ratio identity, exponent rule and general conditional sign law
- **Paper:** E
- **Candidate:** C5; C2
- **Matrix rows:** 31, 32, 33
- **Claim category:** Gradient-level readout shot ratio, exponent rule and general conditional sign law — matrix rows 31–33
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–C)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–30
- **Source version:** Published version (Quantum 8, 1225; 2024-01-11) = arXiv:2203.00031v2 file
- **Source URL:** https://doi.org/10.22331/q-2024-01-11-1225
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: ratio, readout, swap, Loschmidt, slope, exponent in n, conditional, sign, relative gradient. The kernel readout is the all-zero frequency only (E-02); the ±1 readout of the approximate QSVM estimates a different quantity and is never compared with it (E-NL02). Searched in the closure audit.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

---

## Paper F — Mari, Bromley, Killoran, Phys. Rev. A 103, 012405 (2021), reviewed as arXiv:2008.06517v2

All F locators are arXiv v2 locators (17 pp.). The arXiv v2 PDF is byte-identical to the open-access post-print in
the University of Camerino repository (IRIS, hdl:11581/475358). The APS version of record returned an access
challenge (HTTP 403) and is not open access; its page and equation numbers are unverified.

<a id="F-01"></a>
### F-01 · §IV C, Eqs. (43)–(50): finite-shot parameter-shift estimator and its per-θ variance
- **Paper:** F
- **Candidate:** C1; C3; C5
- **Matrix rows:** 7, 29
- **Claim category:** Finite-shot parameter-shift gradient estimator and its mean-squared error — matrix rows 7, 29
- **Classification:** EXPLICIT
- **Section:** IV. Statistical estimation of derivatives
- **Subsection:** C. Parameter-shift gradient estimators; 1. The parameter-shift rule with maximum shift (s = π/2)
- **Equation:** (25), (43)–(50)
- **Figure:** —
- **Appendix:** —
- **Page:** 5, 7
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** "justified only if Assumption 1 is valid"
- **Source statement (paraphrase):** Each expectation value is estimated from N shots as f̂ = f + ε̂ with zero-mean noise of variance σ₀²/N, where σ₀² is the single-shot variance (Eq. 25). The parameter-shift estimator ĝ^(s) = [f̂(θ + s) − f̂(θ − s)]/(2 sin s) is unbiased (Eqs. 43–44) with Var = [σ₀²(θ_j + s) + σ₀²(θ_j − s)]/(4N sin² s) (Eq. 45), approximated by σ₀²/(2N sin² s) only under Assumption 1 (Eqs. 46–47). Under Assumption 1, Eq. (47) is minimised at s = π/2, which gives the estimator and MSE of Eqs. (48)–(50). The statistic is the MSE at a fixed parameter point (expectation over measurement outcomes only), not a circuit average.
- **Mathematical expression:** Var(ĝ_j^(s)) = [σ₀²(θ_j + s) + σ₀²(θ_j − s)]/(4N sin² s) (Eq. 45); ≈ σ₀²/(2N sin² s) under Assumption 1
- **Assumptions:** Rotation-like gates with involutory generators (Eqs. 3–4); independent shot noise for the two shifted evaluations (implicit in Eq. 45); Assumption 1 only for the approximations (46), (47), (50).
- **Scope:** Any expectation value; per-θ (fixed parameter) MSE.
- **Relation to Stage 7:** Eq. (45) at s = π/2, with N = M per shift, is the general form of Stage 7's gradient variances: σ₀² = F(1 − F) gives Var(ĝ_LE) and σ₀² = 1 − F² gives Var(ĝ_SWAP) (our substitution; checked against STAGE7.md §5–§6). As printed, Eq. (49) has denominator 2N where Eqs. (45), (48) and (50) imply 4N (B5_MARI_AUDIT.md §6); Stage 7 uses 4M.
- **Does NOT establish:** Readout-specific single-shot variances, the estimator's distribution, zero or sign probabilities, or any n-scaling.

<a id="F-02"></a>
### F-02 · Eq. (45) with shift-dependent single-shot variances, and Assumption 1, read against the shot-ratio identity
- **Paper:** F
- **Candidate:** C5
- **Matrix rows:** 31
- **Claim category:** SWAP/Loschmidt shot-ratio identity for parameter-shift gradients — matrix row 31
- **Classification:** RELATED BUT DIFFERENT
- **Section:** IV. Statistical estimation of derivatives
- **Subsection:** Assumption 1 (§IV B); C. Parameter-shift gradient estimators
- **Equation:** (25), (35), (36), (45)
- **Figure:** —
- **Appendix:** —
- **Page:** 5–7
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** "depends on the specific details of the circuit and of the observable"
- **Source statement (paraphrase):** The single-shot variance σ₀² "depends on the specific details of the circuit and of the observable" (p. 5), and Eq. (45) keeps its values at the two shifts separate. Assumption 1 (p. 6) states that σ₀²(θ + x) + σ₀²(θ − x) ≈ 2σ₀² and notes that counter-examples exist for large shifts. No readout-specific σ₀² is given and no ratio between readouts is formed.
- **Mathematical expression:** Implied only with external input (our algebra): inserting σ₀² = F(1 − F) and σ₀² = 1 − F² (B-10a, H-01) into Eq. (45) at s = π/2 gives the principal track's ratio R
- **Assumptions:** As F-01.
- **Scope:** General per-θ variance structure; the readout dependence enters only through σ₀², which the source leaves unspecified.
- **Relation to Stage 7:** The identity's per-θ variance structure is printed here in general form. Our algebra: Assumption 1 is a sum condition. For the Loschmidt readout at small fidelity, σ₀²(θ_k + x) + σ₀²(θ_k − x) ≈ A(1 + cos θ_k cos x) while 2σ₀²(θ_k) ≈ A(1 + cos θ_k); at the parameter shift x = π/2 the sum is ≈ A, so the assumption fails by the factor (1 + cos θ_k) (a factor 2 at θ_k = 0) and holds only where cos θ_k ≈ 0. For the SWAP readout both sides are ≈ 2 and the assumption holds. Stage 7 uses Eq. (45)'s exact form.
- **Does NOT establish:** The ratio identity, readout-specific variances or the exponent rule.

<a id="F-03"></a>
### F-03 · §III C, p. 3: the survival probability can be measured with a swap test or as the all-zero bitstring probability
- **Paper:** F
- **Candidate:** C3; C5
- **Matrix rows:** 14a
- **Claim category:** Same-objective Loschmidt vs SWAP comparison at the fidelity level — matrix row 14a
- **Classification:** RELATED BUT DIFFERENT
- **Section:** III. Parameter-shift rules
- **Subsection:** C. Fubini-Study metric tensor
- **Equation:** (14)–(18)
- **Figure:** —
- **Appendix:** —
- **Page:** 3–4
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** "either with a swap-test, or more simply"
- **Source statement (paraphrase):** The metric tensor is written as a Hessian of the survival probability |⟨ψ(θ′)|ψ(θ)⟩|², whose parameter-shift rule is Eq. (16); the survival probability can be estimated either with a swap test or, more simply, as the probability of the 00…0 bitstring after measuring the state printed as U(θ′)U(θ)|0⟩ [sic, no dagger] (p. 3). The two readouts are named as alternatives; their statistics are not compared.
- **Mathematical expression:** f(θ) = |⟨ψ(θ′)|ψ(θ)⟩|² (Eq. 15); F_{j,j}(θ) = (1/4)[1 − |⟨ψ(θ)|ψ(θ + πe_j)⟩|²] (Eq. 17)
- **Assumptions:** Pure states; rotation-like gates.
- **Scope:** Metric-tensor estimation from fidelities at shifted parameters.
- **Relation to Stage 7:** The same two readouts of a parameter-shifted fidelity that Stage 7 compares, named here as alternatives without statistics.
- **Does NOT establish:** A comparison of the two readouts' variances, shots or failure modes.

<a id="F-04"></a>
### F-04 · Eq. (25): additive zero-mean noise model for a finite-shot expectation value
- **Paper:** F
- **Candidate:** C1
- **Matrix rows:** 12
- **Claim category:** Exact difference-of-binomials law of the finite-shot gradient — matrix row 12
- **Classification:** RELATED BUT DIFFERENT
- **Section:** IV. Statistical estimation of derivatives
- **Subsection:** —
- **Equation:** (25), (43)
- **Figure:** —
- **Appendix:** —
- **Page:** 5, 7
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** —
- **Source statement (paraphrase):** The finite-shot estimate is modelled as f̂ = f + ε̂ with ε̂ a zero-mean random variable of variance σ₀²/N (Eq. 25), and the gradient estimate as g + (ε̂₊ − ε̂₋)/(2 sin s) (Eq. 43). Only moments up to second order are used.
- **Mathematical expression:** f̂(θ) = f(θ) + ε̂, E ε̂ = 0, Var ε̂ = σ₀²/N
- **Assumptions:** —
- **Scope:** Moments only.
- **Relation to Stage 7:** Stage 5–7 use the exact law of the same estimator (difference of two binomial counts). F gives its moments only.
- **Does NOT establish:** The pmf, the tie probability, or zero/sign probabilities.

<a id="F-05"></a>
### F-05 · §VI C, pp. 12–13: on hardware the gradient direction remains a signal but is prone to error
- **Paper:** F
- **Candidate:** C1; C4
- **Matrix rows:** 10, 11, 23
- **Claim category:** Exact gradient P_correct, P_wrong and component sign accuracy — matrix rows 10, 11, 23
- **Classification:** RELATED BUT DIFFERENT
- **Section:** VI. Numerical and hardware experiments
- **Subsection:** C. Optimization
- **Equation:** —
- **Figure:** Fig. 4
- **Appendix:** —
- **Page:** 12–13
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** "the gradient direction is clearly still prone to error"
- **Source statement (paraphrase):** On hardware, the optimiser approaches the expected minimum even though the cost function available on the device is noisy, which the authors read as the gradient direction still being an accessible signal; the hardware paths differ from the ideal simulated path, so the direction is prone to error. The N = 10 run approaches the minimum with far fewer circuit evaluations but oscillates around it. Stated qualitatively; no probability is computed.
- **Mathematical expression:** —
- **Assumptions:** 5-qubit circuit (Fig. 1), two trainable parameters, ibmq_burlington and ibmq_valencia hardware, η = 0.4.
- **Scope:** Qualitative; one small problem with device noise; not a barren plateau.
- **Relation to Stage 7:** Qualitative counterpart of Stage 7's exact sign probabilities (§9, §14).
- **Does NOT establish:** Any sign probability, conditional sign law or readout dependence.

<a id="F-06"></a>
### F-06 · §VI C and Fig. 4: gradient descent with N = 10, 100, 1000 shots from one starting point, against the exact-gradient path
- **Paper:** F
- **Candidate:** C4
- **Matrix rows:** 24
- **Claim category:** Matched-start finite-shot optimisation trajectories — matrix row 24
- **Classification:** EXPLICIT
- **Section:** V. First- and second-order optimization (Eq. 63); VI. Numerical and hardware experiments
- **Subsection:** V A. Gradient descent optimizer; VI C. Optimization
- **Equation:** (63)
- **Figure:** Fig. 4 (A1), (A2)
- **Appendix:** App. A 4 (Fig. 9, simulator)
- **Page:** 9 (Eq. 63); 12–13; 15–17
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** "The starting point of the optimizer is"
- **Source statement (paraphrase):** Gradient descent runs with N = 10, 100 and 1000 shots per expectation value on hardware all start from (θ₁, θ₂) = (0.1, 0.15); Fig. 4 (A2) overlays their paths with the path of gradient descent using exact expectation values (dashed line), and (A1) plots cost against total circuit evaluations. The Newton and diagonal-Newton runs (row B) use the same start with N = 1000.
- **Mathematical expression:** θ^(t) = θ^(t−1) − η∇f(θ^(t−1)) (Eq. 63)
- **Assumptions:** η = 0.4; two trainable parameters; device noise present.
- **Scope:** One 2-parameter, 5-qubit problem; no barren plateau; one readout (σ_z on one qubit); no signal-free random-walk control; costs, not fidelity endpoints.
- **Relation to Stage 7:** Matched starts across shot budgets with an exact-gradient reference, as in Stage 7 §17, but without a signal-free control, a readout comparison or a barren plateau.
- **Does NOT establish:** Random-walk behaviour, a signal-free control, or barren-plateau trajectory statistics.

<a id="F-07"></a>
### F-07 · §VI A and App. A, Fig. 6: finite-difference vs parameter-shift crossover at N ≈ 50 shots
- **Paper:** F
- **Candidate:** C3
- **Matrix rows:** 30
- **Claim category:** Critical copy number (estimator crossover) — matrix row 30
- **Classification:** EXPLICIT
- **Section:** VI. Numerical and hardware experiments; App. A
- **Subsection:** A. Estimating the gradient; App. A 2 Estimating the gradient
- **Equation:** (38), (39)
- **Figure:** Fig. 2, Fig. 5, Fig. 6
- **Appendix:** App. A 2
- **Page:** 6, 11, 15
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** "the parameter-shift method has the lower MSE for N > 50 shots"
- **Source statement (paraphrase):** With the optimal finite-difference step h* ∝ N^(−1/6) (Eq. 38) the finite-difference MSE scales as N^(−2/3) (Eq. 39); in simulation of the Fig. 1 circuit the parameter-shift estimator has the lower MSE for N > 50 shots, and Fig. 6 marks the crossover point at N ≈ 50. For low shot numbers the scaled parameter-shift estimator can also be used (p. 11).
- **Mathematical expression:** h* = (9σ₀²/(f₃²N))^(1/6) ∝ N^(−1/6); Δ(ĝ^(h*)) ∝ N^(−2/3)
- **Assumptions:** Assumption 1; one fixed parameter point (Eq. A1); simulator with 1000 repetitions.
- **Scope:** One 5-qubit circuit at one θ; no n-dependence.
- **Relation to Stage 7:** The fixed-θ precursor of Teo's circuit-averaged N_* (D-06; Teo's ref. [61] is this paper). Not a resolution threshold and not readout dependent.
- **Does NOT establish:** An n-scaling of the crossover, a required-shot exponent or readout dependence.

<a id="F-08"></a>
### F-08 · §IV C 2, p. 7: the scaled parameter-shift estimator proposed for the noise-dominated barren-plateau regime
- **Paper:** F
- **Candidate:** F-H
- **Matrix rows:** 26
- **Claim category:** Limits of classical post-processing / mitigation (fact H) — matrix row 26
- **Classification:** RELATED BUT DIFFERENT
- **Section:** IV. Statistical estimation of derivatives
- **Subsection:** C 2. Scaled parameter-shift gradient estimator
- **Equation:** (51)–(57)
- **Figure:** —
- **Appendix:** —
- **Page:** 7
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** "could potentially be helpful when faced with the so-called barren plateau"
- **Source statement (paraphrase):** When the gradient is much smaller than the statistical error, the optimal scaling λ* = 1/(1 + Var/g²) (Eq. 55) is much smaller than 1, so the scaled estimator can reduce the MSE; the authors envisage that it could help on barren plateaus and note that λ* can be absorbed into the learning rate. It is a proposal, not a limit.
- **Mathematical expression:** λ* = 1/(1 + Var(ĝ^(s))/g²); Δ(ĝ^(λ*, s)) = (1 − λ*)g² (Eqs. 55, 57)
- **Assumptions:** λ* known (it depends on the unknown g).
- **Scope:** Estimator design; MSE only.
- **Relation to Stage 7:** Background to Teo 2023 (D-05a) and to the rescaled-gradient method that Aghaei Saem et al. examine (B-13, B-17). Stage 7 does not use scaled estimators.
- **Does NOT establish:** Any limit on post-processing, or that scaling improves trainability (contrast D-08b, B-13).

<a id="F-09"></a>
### F-09 · §IV C 2, p. 7: barren plateaus make the gradient small compared with the statistical error
- **Paper:** F
- **Candidate:** F-A; F-E
- **Matrix rows:** 1, 5
- **Claim category:** Fidelity exponential concentration (row 1); exponential finite-shot measurement burden (row 5)
- **Classification:** RELATED BUT DIFFERENT
- **Section:** IV. Statistical estimation of derivatives
- **Subsection:** C 2. Scaled parameter-shift gradient estimator
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 7
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** —
- **Source statement (paraphrase):** Citing McClean et al. [31], the typical gradient magnitude of a random circuit decays exponentially with the number of qubits; the text then discusses the regime where the gradient is much smaller than the statistical error (Var ≫ g). No shot count, base or fidelity concentration is stated.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** One-sentence background remark.
- **Relation to Stage 7:** Background only.
- **Does NOT establish:** Fidelity concentration, an exponential shot requirement or readout dependence.

<a id="F-10"></a>
### F-10 · §IV B–D, Eqs. (33)–(42), (51)–(62): MSEs of finite-difference and scaled parameter-shift estimators at fixed θ
- **Paper:** F
- **Candidate:** C3
- **Matrix rows:** 29
- **Claim category:** Gradient-estimator mean-squared error (finite shots) — matrix row 29
- **Classification:** EXPLICIT
- **Section:** IV. Statistical estimation of derivatives
- **Subsection:** B. Finite-difference gradient estimator; C 2. Scaled parameter-shift gradient estimator; D. Comparison between analytic and finite-difference gradient estimators
- **Equation:** (33)–(42), (51)–(62)
- **Figure:** Fig. 2, Fig. 6
- **Appendix:** App. A 2
- **Page:** 5–9; 11; 15–16
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** —
- **Source statement (paraphrase):** Central-difference MSE σ₀²/(2Nh²) + f₃²h⁴/36 (Eq. 37) with optimal h* and N^(−2/3) error (Eqs. 38–39), forward-difference analogues (Eqs. 40–42), scaled parameter-shift bias/variance/MSE and optimal λ* (Eqs. 51–57). Eqs. (58)–(60) compare the finite-difference and unscaled parameter-shift estimators, and Eqs. (61)–(62) show that the optimally scaled parameter-shift estimator has the smaller MSE of the three. All at a fixed parameter point.
- **Mathematical expression:** Δ(ĝ^(h)) ≃ σ₀²/(2Nh²) + f₃²h⁴/36 (Eq. 37); Δ(ĝ^(λ, s)) = λ²Var(ĝ^(s)) + (λ − 1)²g² (Eq. 54)
- **Assumptions:** Assumption 1 for Eqs. (36)–(42); λ* requires the unknown g.
- **Scope:** Per-θ MSE; estimator comparison at a fixed readout.
- **Relation to Stage 7:** The fixed-θ counterparts of Teo's circuit-averaged MSEs (D-05a). Stage 7 uses the unscaled estimator at s = π/2 only.
- **Does NOT establish:** Readout dependence, distributions or n-scaling.

<a id="F-11"></a>
### F-11 · Eq. (29) with unbiasedness (Eq. 44): mean-square norm of the estimated gradient vector
- **Paper:** F
- **Candidate:** C4
- **Matrix rows:** 21
- **Claim category:** Gradient norm inflation — matrix row 21
- **Classification:** RELATED BUT DIFFERENT
- **Section:** IV. Statistical estimation of derivatives
- **Subsection:** A. Quantifying the error of a statistical estimator; C. Parameter-shift gradient estimators
- **Equation:** (29), (44)
- **Figure:** —
- **Appendix:** —
- **Page:** 5, 7
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** —
- **Source statement (paraphrase):** The total error of the full gradient estimate is the sum of the component MSEs, Δ(ĝ) = E‖ĝ − g‖² (Eq. 29), and the parameter-shift estimator is unbiased (Eq. 44). The source states no norm comparison.
- **Mathematical expression:** Implied (our algebra): E‖ĝ‖² = ‖g‖² + Δ(ĝ)
- **Assumptions:** Unbiased components.
- **Scope:** Mean-square (expectation) statement at a fixed θ.
- **Relation to Stage 7:** A mean-square analogue of Stage 7's SWAP norm inflation (median ‖ĝ‖/‖g‖ ≈ 10^4.5 at n = 12, M = 1024), like Teo's circuit-averaged Eq. (18) (D-04); the source makes no barren-plateau norm statement.
- **Does NOT establish:** A per-θ median norm ratio, readout dependence or barren-plateau scaling.

### Paper F — not-located search log

Paper F (arXiv v2) was read in full (17 pp. incl. Appendix A) and its LaTeX source was searched.

<a id="F-NL02"></a>
### F-NL02 · Readout statistics: Loschmidt collapse, SWAP null, readout variances, readout comparisons and exponents
- **Paper:** F
- **Candidate:** C3
- **Matrix rows:** 2, 3, 4, 14b, 15, 16, 17, 18
- **Claim category:** Readout-specific estimator behaviour and readout-dependent shot exponents
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + App. A)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–17 (arXiv v2)
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: Loschmidt, echo, swap test (only the p. 3 alternative, F-03), bit string, zero estimate, coin, readout variance, F(1 − F), 1 − F², exponent, scaling with qubits, 4^n, 16^n. σ₀² is left unspecified (F-02).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="F-NL09"></a>
### F-NL09 · Zero probabilities and conditional sign laws
- **Paper:** F
- **Candidate:** C1; C2
- **Matrix rows:** 9, 13, 19, 33
- **Claim category:** P(ĝ = 0), full-vector zero probability, and conditional Loschmidt sign laws (product and general form)
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + App. A)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–17 (arXiv v2)
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: zero, exactly zero, tie, binomial, Poisson, probability, conditional, non-zero, sign, relative gradient. The analysis uses MSEs (second moments) only. "Exactly zero" occurs only for the fifth gradient component of the fixed example (p. 15), a property of the circuit, not of an estimate.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="F-NL20"></a>
### F-NL20 · Distinguishability framework, random walk, vector metrics, signal-free control
- **Paper:** F
- **Candidate:** C4
- **Matrix rows:** 6, 8, 20, 22, 25
- **Claim category:** Outcome-level distinguishability, random-walk behaviour, full-vector metrics and signal-free controls
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + App. A)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–17 (arXiv v2)
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: hypothesis test, distinguish, random walk, cosine, angle, alignment, norm of the estimate, random baseline, control. Eq. (29) defines the total MSE of the full gradient vector (a sum of component MSEs), not a direction statistic (its norm consequence is recorded in F-11); the N = 10 hardware run is said to oscillate around the minimum, without a random-walk analysis.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

<a id="F-NL27"></a>
### F-NL27 · Product-rotation landscape, global-Z parity numerics, exponent rule
- **Paper:** F
- **Candidate:** CTX; C5
- **Matrix rows:** 27, 28, 32
- **Claim category:** Stage 3–7 landscape family, Stage 6 parity benchmark, and the exponent rule b_SW = b_LE + b_S
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + App. A)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–17 (arXiv v2)
- **Source version:** arXiv:2008.06517v2 (2021-02-26; journal-ref Phys. Rev. A 103, 012405 (2021)); = IRIS post-print; APS version of record not inspected
- **Source URL:** https://arxiv.org/abs/2008.06517v2
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: product state, fidelity landscape, global Z, parity, slope, exponent, scaling with qubits. The Fig. 1 circuit has five R_X rotations, an entangling CNOT block and a σ_z measurement on one qubit; no n-dependence is studied. "Parity" occurs only as the parity of a shift vector in Eq. (21), and exponential scaling with qubits only in the background barren-plateau remark (F-09).
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

---

## Paper G — Miranskyy, arXiv:2510.22418 (2025), *The Cost of Certainty: Shot Budgets in Quantum Program Testing*

Reviewed: arXiv:2510.22418v1 (2025-10-25, 30 pp., single version; no journal reference), read in full; the LaTeX
source was also downloaded. Locators are arXiv v1 locators. The paper was listed in the principal track's
"Other papers" table with the note "Read before citing".

<a id="G-01"></a>
### G-01 · §3.1–§3.4: inverse test vs swap test shot counts for one fidelity target; ratio → 2 as F → 1
- **Paper:** G
- **Candidate:** C3; C5
- **Matrix rows:** 14a
- **Claim category:** Same-objective Loschmidt vs SWAP comparison at the fidelity level — matrix row 14a
- **Classification:** EXPLICIT
- **Section:** Abstract; 3 Practical shot estimates: inverse, swap, and chi-square tests; 4 Impact of noise on shot estimates for inverse and swap tests; 6.1 Summary of results; 7 Conclusions
- **Subsection:** 3.1.1 Ideal quantum computer (inverse); 3.2.1 Ideal quantum computer (swap); 3.4 Comparison of methods
- **Equation:** (8), (10), (11)
- **Figure:** Fig. 2
- **Appendix:** App. C, App. D
- **Page:** 1–2, 6–9, 13–15, 21–22, 28–30
- **Source version:** arXiv:2510.22418v1 (2025-10-25); single version, no journal reference
- **Source URL:** https://arxiv.org/abs/2510.22418v1
- **Short quote:** "the swap test requires about twice as many shots"
- **Source statement (paraphrase):** For distinguishing an actual from an expected pure state at error probability P_e, the inverse test needs N ≲ ln P_e / ln F (Eq. 8) and the swap test N ≲ ln P_e / ln[(1 + F)/2] (Eq. 11), from the quantum Chernoff bound with Q = F and Q = (1 + F)/2 (App. C, App. D). Their ratio ln F / ln[(1 + F)/2] = 2 − (F − 1)/2 + O((F − 1)²) → 2 as F → 1 (p. 9); Examples 3.3–3.4 give 9208 vs 4603 shots at F = 0.999 and 919 vs 458 at F = 0.99 (P_e = 0.01). The factor-of-two overhead is said to persist under noise (§4, p. 15).
- **Mathematical expression:** N_swap/N_inverse = ln F / ln[(1 + F)/2] ≈ 2 for F → 1
- **Assumptions:** Pure states; ideal device for §3.1.1/§3.2.1 (κ ∈ [1, 2] for noise); asymptotic QCB estimate; high-fidelity regime (F ∈ [0.9, 0.995] in Fig. 2).
- **Scope:** Detection (testing) shot counts near F = 1; not estimator variances, not gradients, not concentrated landscapes.
- **Relation to Stage 7:** The same two readouts compared on one fidelity, at the opposite end of the fidelity range from Stage 7 (F ≈ 1 vs F ≈ 0) and with a different statistic (detection error probability vs estimator variance). Our algebra: the detection ratio and the per-shot variance ratio (1 + F)/F agree at F → 1 (both 2) and differ elsewhere, e.g. 2.41 vs 3 at F = 0.5 and 3.85 vs 11 at F = 0.1 (B5_MATH_COMPARISON §9).
- **Does NOT establish:** Estimator-variance ratios, gradient-level ratios, exponents in n, or behaviour under concentration.

<a id="G-02"></a>
### G-02 · Outcome probabilities F (inverse test) and (1 + F)/2 (swap test) read against variances, the ratio identity and the exponent rule
- **Paper:** G
- **Candidate:** C5; C3
- **Matrix rows:** 4, 31, 32
- **Claim category:** Different Loschmidt / SWAP estimator variances (row 4); SWAP/Loschmidt shot-ratio identity and exponent rule (rows 31, 32)
- **Classification:** PARTIAL / IMPLIED
- **Section:** 3 Practical shot estimates: inverse, swap, and chi-square tests; App. C; App. D
- **Subsection:** 3.1 Inverse test; 3.2 Swap test
- **Equation:** (10), (30)
- **Figure:** —
- **Appendix:** App. C, App. D
- **Page:** 6, 8, 28–30
- **Source version:** arXiv:2510.22418v1 (2025-10-25); single version, no journal reference
- **Source URL:** https://arxiv.org/abs/2510.22418v1
- **Short quote:** "the probability of measuring the all-zero outcome equals the fidelity"
- **Source statement (paraphrase):** The inverse test returns the all-zero bitstring with probability equal to the fidelity (p. 6; App. C, Eq. 30) and the swap-test ancilla returns 0 with probability 1/2 + F/2 (Eq. 10; App. D). The source uses these only for detection bounds; it writes no estimator variance, no gradient and no n-scaling.
- **Mathematical expression:** Implied (our algebra): per-shot variances F(1 − F) and 1 − F² (for F̂ = 2K/N − 1); at the two shifts the ratio R of the principal track; R → 2/S as S → 0; with median log-slopes, b_SW − b_LE ≈ b_S (to leading order as S → 0)
- **Assumptions:** Added (ours): fidelity estimation (not detection); parameter shift with independent batches; for row 32, a concentrated ensemble over θ with median log-slopes; the medians of log₁₀S and log₁₀|r| must combine additively (e.g. linear trends in n with O(1) fluctuations), and the rule holds only to leading order as S → 0, so it is approximate.
- **Scope:** Outcome models only; testing context near F = 1.
- **Relation to Stage 7:** Same outcome models as Stage 7 §5–§6.
- **Does NOT establish:** The variances, the identity or the rule as stated results.

<a id="G-03"></a>
### G-03 · Footnotes 2–3: probabilities that all N shots accept, F^N (inverse test) and [(1 + F)/2]^N (swap test)
- **Paper:** G
- **Candidate:** C1
- **Matrix rows:** 9
- **Claim category:** Exact gradient P_zero — matrix row 9
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 3 Practical shot estimates: inverse, swap, and chi-square tests
- **Subsection:** 3.1.1 (footnote 2); 3.2.1 (footnote 3)
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 6, 8
- **Source version:** arXiv:2510.22418v1 (2025-10-25); single version, no journal reference
- **Source URL:** https://arxiv.org/abs/2510.22418v1
- **Short quote:** "We accept the test only if every trial yields a zero-string"
- **Source statement (paraphrase):** The probability that every one of N inverse-test shots returns the all-zero string is F^N, and that every swap-test shot returns ancilla 0 is [(1 + F)/2]^N; requiring these to be at most P_e gives N ≥ ln P_e / ln F and N ≥ ln P_e / ln[(1 + F)/2].
- **Mathematical expression:** P_accept,inverse = F^N; P_miss,swap = [(1 + F)/2]^N
- **Assumptions:** Pure states; independent shots.
- **Scope:** Exact finite-shot event probabilities at the fidelity level, for the event "every shot accepts" (the Loschmidt-estimate-equals-one event).
- **Relation to Stage 7:** The opposite event to Stage 7's Loschmidt zero estimate, whose probability is (1 − F)^M (Thanasilp A-06a). No gradient-level zero probability.
- **Does NOT establish:** P(ĝ = 0) or zero-estimate probabilities.

<a id="G-04"></a>
### G-04 · §2 and App. A–B: quantum Chernoff bound, fidelity and trace-distance bounds for shot counts
- **Paper:** G
- **Candidate:** C3
- **Matrix rows:** 6
- **Claim category:** Outcome-distribution distinguishability framework — matrix row 6
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 2 Theoretical foundations for shot estimation; App. A; App. B
- **Subsection:** 2.1 Quantum Chernoff bound; 2.2 Fidelity
- **Equation:** (1)–(7)
- **Figure:** Fig. 1
- **Appendix:** App. A, App. B
- **Page:** 3–5, 27–29
- **Source version:** arXiv:2510.22418v1 (2025-10-25); single version, no journal reference
- **Source URL:** https://arxiv.org/abs/2510.22418v1
- **Short quote:** —
- **Source statement (paraphrase):** Shot counts for distinguishing two states follow from the quantum Chernoff bound, P_e ∼ exp(−Nξ_QCB) with ξ_QCB = −ln Q(ρ, σ) (Eq. 1), giving N ∼ ln P_e / ln Q (Eq. 2); for pure or pure-mixed pairs Q = F (Eqs. 4–5), with bounds for mixed pairs (Eqs. 6–7).
- **Mathematical expression:** N ∼ ln P_e / ln Q(ρ, σ) (Eq. 2)
- **Assumptions:** Asymptotic (N → ∞) QCB estimate.
- **Scope:** State discrimination (testing), not concentration-induced indistinguishability over a landscape.
- **Relation to Stage 7:** A different distinguishability framework from A's and B's 1-norm hypothesis tests; Stage 7 §15 uses per-shot TV and Hellinger distances between the two shifted outcome distributions.
- **Does NOT establish:** Statements about concentration or gradients.

<a id="G-05"></a>
### G-05 · §3.2, p. 8: the swap test keeps a 0.5 acceptance probability even for orthogonal states
- **Paper:** G
- **Candidate:** F-C
- **Matrix rows:** 3
- **Claim category:** SWAP estimator random / data-independent limit — matrix row 3
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 3 Practical shot estimates: inverse, swap, and chi-square tests
- **Subsection:** 3.2 Swap test
- **Equation:** (10)
- **Figure:** —
- **Appendix:** —
- **Page:** 8
- **Source version:** arXiv:2510.22418v1 (2025-10-25); single version, no journal reference
- **Source URL:** https://arxiv.org/abs/2510.22418v1
- **Short quote:** "the swap test always retains a 0.5 baseline acceptance probability"
- **Source statement (paraphrase):** Unlike the inverse test, which rejects orthogonal states with certainty, the swap test accepts orthogonal states with probability 0.5.
- **Mathematical expression:** P(M_qa = 0) = 1/2 + F/2 (Eq. 10)
- **Assumptions:** —
- **Scope:** The F = 0 endpoint of the swap-test outcome model; no concentration or estimator statement.
- **Relation to Stage 7:** The ½-centred outcome probability behind Stage 7's SWAP failure mode, stated here for orthogonal states.
- **Does NOT establish:** Indistinguishability from a null, random signs or random-walk behaviour.

<a id="G-06"></a>
### G-06 · §2.2.1 and Fig. 1: detection shot counts diverge as F → 1
- **Paper:** G
- **Candidate:** F-E
- **Matrix rows:** 5
- **Claim category:** Exponential finite-shot measurement burden — matrix row 5
- **Classification:** RELATED BUT DIFFERENT
- **Section:** 2 Theoretical foundations for shot estimation
- **Subsection:** 2.2.1 Comparison of N_pure, N_pure-mixed, and N_mixed
- **Equation:** (5), (7)
- **Figure:** Fig. 1
- **Appendix:** —
- **Page:** 4–5
- **Source version:** arXiv:2510.22418v1 (2025-10-25); single version, no journal reference
- **Source URL:** https://arxiv.org/abs/2510.22418v1
- **Short quote:** "As F → 1, the required N grows exponentially"
- **Source statement (paraphrase):** The shot count needed to distinguish two states diverges as the fidelity approaches 1 (described as exponential growth, p. 5 and Fig. 1 caption) and approaches one shot as F → 0.
- **Mathematical expression:** N_pure ∼ ln P_e / ln F (Eq. 5); our algebra: ≈ ln(1/P_e)/(1 − F) as F → 1, a 1/(1 − F) divergence
- **Assumptions:** Pure or pure-mixed states; asymptotic QCB estimate.
- **Scope:** Detection near F = 1 as a function of F; no system-size dependence and no concentration.
- **Relation to Stage 7:** A different shot burden (resolving a fidelity close to 1) from Stage 7's (resolving exponentially small fidelity differences).
- **Does NOT establish:** An exponential shot requirement in the number of qubits or under concentration.

### Paper G — not-located search log

Paper G was read in full (30 pp. incl. Appendices A–D).

<a id="G-NL01"></a>
### G-NL01 · Concentration, gradients, sign laws, trajectories, gradient MSE, crossover, general sign law
- **Paper:** G
- **Candidate:** C1; C2; C3; C4; F-A; F-B; CTX
- **Matrix rows:** 1, 2, 7, 8, 10, 11, 12, 13, 14b, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 33
- **Claim category:** Remaining matrix items (concentration, gradient-level statistics, exponents, trajectories, context)
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Appendices A–D)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–30
- **Source version:** arXiv:2510.22418v1 (2025-10-25); single version, no journal reference
- **Source URL:** https://arxiv.org/abs/2510.22418v1
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: barren plateau, concentration, gradient, parameter shift, variance, zero estimate, sign, conditional, random walk, trajectory, exponent in n, qubits scaling, 4^n, 16^n, crossover, mean squared error. Shot counts are functions of F and P_e; their divergence as F → 1 is recorded under row 5 (G-06), the Bures-angle budget N_j = O(θ_j^(−2)) (§5) is not a concentration statement, and the paper studies no landscape or optimisation.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.

---

## Paper H — Zhan, Wang, Mi, Xie, Xu, Zhang, Zhang, Light Sci. Appl. 14, 83 (2025)

Reviewed: the published version (Light: Science & Applications 14, 83; open access, CC BY 4.0; received 2024-04-16,
accepted 2025-01-10, published 2025-02-12; 12 pp.) and its published Supplementary Information (MOESM1, 26 pp.,
equations S1–S119), both read in full. arXiv:2406.06810v1 (2024-06-10) was cross-checked for dating: it already
contains the two variances, the known-state projection law and the precision comparison. Main-text locators are
published-version numbers; "SI" locators use the published SI's numbering.

<a id="H-01"></a>
### H-01 · Projection (known target) and swap-type overlap estimators: per-copy variances c(1 − c)/N and (1 − c²)/N
- **Paper:** H
- **Candidate:** C3; C5; F-D
- **Matrix rows:** 4
- **Claim category:** Different Loschmidt / SWAP estimator variances — matrix row 4
- **Classification:** EXPLICIT
- **Section:** Results; Materials and methods; SI II F, III A, IV, V
- **Subsection:** Overlap-dependent precision of strategies; Precision of joint measurement strategies; SI V Overlap estimation with a known state
- **Equation:** (3), (9), (10); SI (S72), (S80), (S112)
- **Figure:** Fig. 2
- **Appendix:** SI III A, SI V
- **Page:** 4–5, 9; SI 14, 17, 23
- **Source version:** Published version (Light Sci. Appl. 14, 83; 2025-02-12) + published Supplementary Information (MOESM1); arXiv:2406.06810v1 cross-checked
- **Source URL:** https://doi.org/10.1038/s41377-025-01755-8
- **Short quote:** "The average variance through projection-based overlap estimation with a known state is given by"
- **Source statement (paraphrase):** With one state known, projecting N copies of the other onto it gives Bin(k, N, c) counts, estimator k/N and variance v_proj = c(1 − c)/N (SI p. 23; the same projection term appears as Eq. 3, p. 5, and SI Eq. S72). The Schur collective measurement (SCM) has p₋ = (1 − c)/2 (Eq. 9), estimator 1 − 2k/N and variance (1 − c²)/N (Eq. 10, p. 9; Table 1, p. 4); the ideal optical swap test has the same law and variance (SI Eq. S80, p. 17; SI p. 23). The paper calls SCM and OST two realisations of the destructive swap test (p. 5).
- **Mathematical expression:** v_proj(c, N) = c(1 − c)/N; v_scm(c, N) = (1 − c²)/N (ideal OST identical)
- **Assumptions:** Pure states; independent copies; asymptotic (large-N) unbiased estimators.
- **Scope:** Overlap (fidelity) estimation between two states; qubits in the experiment, general d in the SI; no gradients and no concentration.
- **Relation to Stage 7:** These are Stage 7's per-shot variances: the known-target projection is the Loschmidt readout (F(1 − F)) and the SCM/OST is the destructive form of the SWAP test (1 − F²), in a paper published 2025-02-12 (arXiv v1 2024-06-10), earlier than paper B's version of record (2026-01-30), which contains the same pair (B-10a).
- **Does NOT establish:** Gradient-level variances, shot ratios for gradients, or any statement under concentration.

<a id="H-02"></a>
### H-02 · Same-overlap comparison of strategies: the swap-type estimators are less precise at small overlap
- **Paper:** H
- **Candidate:** C3; C5
- **Matrix rows:** 14a
- **Claim category:** Same-objective Loschmidt vs SWAP comparison at the fidelity level — matrix row 14a
- **Classification:** EXPLICIT
- **Section:** Results; Discussion
- **Subsection:** Overlap-dependent precision of strategies; Adaptive overlap estimation strategy
- **Equation:** (1)–(3), (10)
- **Figure:** Fig. 2, Fig. 3, Fig. 4
- **Appendix:** SI II E, SI V
- **Page:** 1, 4–8; SI 23–24
- **Source version:** Published version (Light Sci. Appl. 14, 83; 2025-02-12) + published Supplementary Information (MOESM1); arXiv:2406.06810v1 cross-checked
- **Source URL:** https://doi.org/10.1038/s41377-025-01755-8
- **Short quote:** "they achieve lower precision for small c but higher precision for large c"
- **Source statement (paraphrase):** For the same overlap c, the four strategies (tomography–tomography, tomography–projection, SCM, optical swap test) are compared analytically and in a photonic experiment (N = 900 copies, 11 overlaps, Fig. 2). The joint (swap-type) strategies have lower precision at small c and higher precision at large c than the tomography-based ones; TP and SCM cross at c_t = 4/11 (p. 6), which motivates an adaptive TP/SCM strategy (Fig. 4). The TP variance includes a tomography term 2κc(1 − c)/N (Eq. 2) on top of the projection term.
- **Mathematical expression:** v_tp = (2κ + 1)c(1 − c)/N vs v_scm = (1 − c²)/N; crossover c_t = 4/11 (κ = 11/8, MUB tomography)
- **Assumptions:** Qubit pairs Haar-sampled at fixed overlap (Eq. 1); MUB tomography for TT/TP; experimental imperfections (Γ = 0.965) for OST.
- **Scope:** Overlap estimation; fixed c; no gradients, no landscape and no concentration.
- **Relation to Stage 7:** A fidelity-level comparison of a projection readout and swap-type readouts of the same overlap, with the swap-type variance larger at small overlap. With a known target (no tomography term), the variance ratio is (1 + c)/c ≥ 2 (our algebra).
- **Does NOT establish:** Gradient-level comparisons, exponents or failure modes under concentration.

<a id="H-03"></a>
### H-03 · The two per-copy variances read against the gradient-level shot-ratio identity and the exponent rule
- **Paper:** H
- **Candidate:** C5; C3
- **Matrix rows:** 31, 32
- **Claim category:** SWAP/Loschmidt shot-ratio identity for parameter-shift gradients and the exponent rule — matrix rows 31, 32
- **Classification:** PARTIAL / IMPLIED
- **Section:** Results; Materials and methods; SI V
- **Subsection:** Overlap-dependent precision of strategies; Precision of joint measurement strategies; SI V Overlap estimation with a known state
- **Equation:** (3), (10)
- **Figure:** —
- **Appendix:** SI V
- **Page:** 5, 9; SI 23
- **Source version:** Published version (Light Sci. Appl. 14, 83; 2025-02-12) + published Supplementary Information (MOESM1); arXiv:2406.06810v1 cross-checked
- **Source URL:** https://doi.org/10.1038/s41377-025-01755-8
- **Short quote:** —
- **Source statement (paraphrase):** The source gives the per-copy variances of the projection (known target) and swap-type estimators of one overlap (H-01) and compares their precision (H-02). It does not consider parameter shifts, gradients, shot ratios for gradients or scaling with system size under concentration.
- **Mathematical expression:** Implied (our algebra): at the two shifts, R = [2 − F₊² − F₋²]/[F₊(1 − F₊) + F₋(1 − F₋)] → 2/S; with median log-slopes, b_SW − b_LE ≈ b_S (to leading order as S → 0)
- **Assumptions:** Added (ours): parametrised fidelity F(θ) with known target; parameter shift with independent batches; for row 32, a concentrated ensemble over θ with median log-slopes; the medians of log₁₀S and log₁₀|r| must combine additively (e.g. linear trends in n with O(1) fluctuations), and the rule holds only to leading order as S → 0, so it is approximate.
- **Scope:** Overlap level in the source.
- **Relation to Stage 7:** One of four sources (with A, B and G) whose printed per-shot statistics supply the ingredients of the principal track's identity.
- **Does NOT establish:** The identity or the rule as stated results.

<a id="H-04"></a>
### H-04 · SI V and Eq. (S54): binomial law Bin(k, N, c) of the projection count
- **Paper:** H
- **Candidate:** C1
- **Matrix rows:** 12
- **Claim category:** Exact difference-of-binomials law of the finite-shot gradient — matrix row 12
- **Classification:** RELATED BUT DIFFERENT
- **Section:** SI II E; SI V
- **Subsection:** Numerical results of average variance for TT and TP strategies; Overlap estimation with a known state
- **Equation:** (S54)
- **Figure:** —
- **Appendix:** SI II D, SI V
- **Page:** SI 11, 23
- **Source version:** Published version (Light Sci. Appl. 14, 83; 2025-02-12) + published Supplementary Information (MOESM1); arXiv:2406.06810v1 cross-checked
- **Source URL:** https://doi.org/10.1038/s41377-025-01755-8
- **Short quote:** "follows a binomial distribution Bin(k, N, c)"
- **Source statement (paraphrase):** The number of successful projections onto the known state follows Bin(k, N, c) (SI p. 23); with a tomographic estimate the projection count law is Eq. (S54). The law of a single overlap estimate is written; no difference of two counts is considered.
- **Mathematical expression:** P_proj(k | N) = C(N, k) c^k (1 − c)^(N − k)
- **Assumptions:** Independent copies.
- **Scope:** Single overlap estimate.
- **Relation to Stage 7:** One of the two binomials whose difference is Stage 7's Loschmidt gradient estimator.
- **Does NOT establish:** The difference-of-binomials law, ties, or zero/sign probabilities.

<a id="H-05"></a>
### H-05 · Eq. (1) and SI Eqs. (S1), (S5): MSE of overlap estimators averaged over Haar-sampled pairs at fixed overlap
- **Paper:** H
- **Candidate:** C3
- **Matrix rows:** 29
- **Claim category:** Gradient-estimator mean-squared error (finite shots) — matrix row 29
- **Classification:** RELATED BUT DIFFERENT
- **Section:** Results; SI I
- **Subsection:** Overlap estimation strategy performance assessment
- **Equation:** (1); SI (S1), (S5)
- **Figure:** —
- **Appendix:** SI I
- **Page:** 2; SI 2
- **Source version:** Published version (Light Sci. Appl. 14, 83; 2025-02-12) + published Supplementary Information (MOESM1); arXiv:2406.06810v1 cross-checked
- **Source URL:** https://doi.org/10.1038/s41377-025-01755-8
- **Short quote:** —
- **Source statement (paraphrase):** Precision is the mean squared error of the overlap estimate, averaged over Haar-random qubit pairs with fixed overlap c and over the measurement outcomes; it scales as 1/N, so the scaled variance N v_s(c) is the figure of merit.
- **Mathematical expression:** v_s(c, N) = (1/2π) ∫∫ v_s(c, N | U, φ) dU dφ (Eq. 1)
- **Assumptions:** —
- **Scope:** Overlap estimators, not gradient estimators.
- **Relation to Stage 7:** A different object (overlap, not gradient); for the projection and swap-type strategies the variance depends only on c, so the average is per-overlap.
- **Does NOT establish:** Any gradient MSE.

<a id="H-06"></a>
### H-06 · The measurement strategy changes how overlap-estimation precision scales with dimension
- **Paper:** H
- **Candidate:** C3
- **Matrix rows:** 5, 18
- **Claim category:** Exponential finite-shot measurement burden (row 5); measurement scheme changing the resolution exponent (row 18)
- **Classification:** RELATED BUT DIFFERENT
- **Section:** Results; SI II F–G; SI V
- **Subsection:** Overlap estimation of high-dimensional states; Extending the SCM strategy to qudits
- **Equation:** (4), (8); SI (S71)–(S75), (S119)
- **Figure:** —
- **Appendix:** SI II F–G, SI V
- **Page:** 6–7, 9; SI 14–15, 25
- **Source version:** Published version (Light Sci. Appl. 14, 83; 2025-02-12) + published Supplementary Information (MOESM1); arXiv:2406.06810v1 cross-checked
- **Source URL:** https://doi.org/10.1038/s41377-025-01755-8
- **Short quote:** "maintaining precision independent of d"
- **Source statement (paraphrase):** For n-qubit states with only local measurements for tomography, the tomography-based strategies acquire a dimension-dependent average variance, while SCM and OST keep precision independent of d, v_scm = (1 − c²)/N (p. 7; SI p. 25, Eq. S119). The size of the dimension factor is stated inconsistently: SI Eq. (S75) and main-text Eq. (4) with κ_loc = O(4ⁿ n) give O(2ⁿ n c(1 − c)/N), while the main text on p. 7 writes O(4ⁿ n c(1 − c)/N) (our reading; no effect on the comparison).
- **Mathematical expression:** v_tt, v_tp ∼ O(2ⁿ n c(1 − c)/N) (local tomography, SI Eq. S75); v_scm = (1 − c²)/N independent of d
- **Assumptions:** Sufficient-copy regime N ≫ d; local-measurement tomography with κ_loc = O(4ⁿ n).
- **Scope:** The exponential factor comes from tomography of an unknown state, not from concentration; overlap level.
- **Relation to Stage 7:** A measurement-dependent dimension scaling of overlap precision, by a different mechanism from Stage 7's (tomography cost vs concentrated outcome probabilities).
- **Does NOT establish:** Shot exponents for gradients, or concentration-driven readout dependence.

<a id="H-07"></a>
### H-07 · Fisher information and Cramér–Rao bounds per strategy
- **Paper:** H
- **Candidate:** C3
- **Matrix rows:** 6
- **Claim category:** Outcome-distribution distinguishability framework — matrix row 6
- **Classification:** RELATED BUT DIFFERENT
- **Section:** Results; Materials and methods; SI III D
- **Subsection:** Overlap-dependent precision of strategies; Precision of joint measurement strategies
- **Equation:** (9)–(12); SI (S97), (S98)
- **Figure:** Fig. 2 (b)
- **Appendix:** SI III D
- **Page:** 5, 9; SI 21
- **Source version:** Published version (Light Sci. Appl. 14, 83; 2025-02-12) + published Supplementary Information (MOESM1); arXiv:2406.06810v1 cross-checked
- **Source URL:** https://doi.org/10.1038/s41377-025-01755-8
- **Short quote:** —
- **Source statement (paraphrase):** The normalised Fisher information per state pair is computed for each strategy (Fig. 2b); the SCM has I_scm = 1/(1 − c²), its estimator saturates the Cramér–Rao bound, and its Fisher information approaches the quantum Fisher information at large overlap.
- **Mathematical expression:** I_scm = 1/(1 − c²) (p. 9)
- **Assumptions:** Large-N (asymptotic) estimation.
- **Scope:** Local estimation precision of one overlap.
- **Relation to Stage 7:** Estimation-theoretic counterpart of the information-distance view of Stage 7 §15; not a hypothesis-testing or indistinguishability statement.
- **Does NOT establish:** Concentration-induced indistinguishability or gradient-level statements.

### Paper H — not-located search log

Paper H was read in full: main text (12 pp.) and published Supplementary Information (26 pp.).

<a id="H-NL01"></a>
### H-NL01 · Concentration, gradient-level statistics, exponents in n, trajectories, context items
- **Paper:** H
- **Candidate:** C1; C2; C3; C4; F-A; F-B; CTX
- **Matrix rows:** 1, 2, 3, 7, 8, 9, 10, 11, 13, 14b, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 33
- **Claim category:** Remaining matrix items (concentration, gradient-level statistics, exponents, trajectories, context)
- **Classification:** NOT LOCATED
- **Section:** Whole paper (main text + Supplementary Information)
- **Subsection:** —
- **Equation:** —
- **Figure:** —
- **Appendix:** —
- **Page:** 1–12; SI 1–26
- **Source version:** Published version (Light Sci. Appl. 14, 83; 2025-02-12) + published Supplementary Information (MOESM1); arXiv:2406.06810v1 cross-checked
- **Source URL:** https://doi.org/10.1038/s41377-025-01755-8
- **Short quote:** —
- **Source statement (paraphrase):** Not located in the reviewed version after searches for: barren plateau, concentration, gradient, parameter shift, zero estimate, sign, conditional, random walk, trajectory, crossover, exponent, 4^n, 16^n. The swap-type outcome probability p₋ = (1 − c)/2 tends to 1/2 as c → 0 (Eq. 9), but no null-distribution or indistinguishability statement is made; the projection estimate's zero event is not discussed. The terms "exponential", "4ⁿ" and "crossover" do occur in other senses: the exponential tomography cost in d (p. 7; SI p. 15, κ_loc = O(4ⁿ n)) and the TP/SCM crossover c_t = 4/11 (p. 6), recorded in H-06 and H-02; none matches these rows' targets.
- **Mathematical expression:** —
- **Assumptions:** —
- **Scope:** As above.
- **Relation to Stage 7:** —
- **Does NOT establish:** Absence from the wider literature.
