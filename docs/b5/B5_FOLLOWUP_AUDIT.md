# B5 follow-up: targeted audit of high-priority gradient-estimation prior work

Branch `dhruv/b5-prior-work-extraction`, on top of the initial B5 round (commit dfd2c6b). This is evidence for the
principal novelty audit (A1). No Stage 1–7 code, report or result was changed.

## 1. Purpose

The initial B5 round reviewed Thanasilp et al. 2024 (A) and Aghaei Saem et al. 2026 (B) and listed three
high-priority follow-up sources (`B5_FOLLOWUP_SOURCES.md` H1–H3). This audit:
- reads those three papers in full, including appendices: Arrasmith 2021 (C), Teo 2023 (D) and Gentinetta 2024 (E);
- records what they explicitly contain about the four Stage 7 candidate contributions:
  - C1: exact finite-shot gradient distribution, P(ĝ = 0), P_correct, P_wrong, ties;
  - C2: the conditional Loschmidt sign law;
  - C3: the readout-dependent gradient shot exponent, ≈ 4ⁿ vs ≈ 16ⁿ;
  - C4: vector and trajectory consequences;
- retries the published version of paper B through legitimate routes.

Teo 2023 gets a deep audit because it analyses finite-copy parameter-shift gradient errors directly.

Classification vocabulary: `EXPLICIT`, `PARTIAL / IMPLIED`, `RELATED BUT DIFFERENT`, `NOT LOCATED`. The initial round's
`PARTIAL / RELATED` is kept unchanged on its A/B entries as a legacy equivalent of `RELATED BUT DIFFERENT`. NOT LOCATED
means only "not found in the reviewed version after the logged searches".

## 2. Papers reviewed

| Id | Paper | Version reviewed | Read | Supplement / appendix | Published version inspected |
|---|---|---|---|---|---|
| C | Arrasmith, Cerezo, Czarnik, Cincio, Coles, *Effect of barren plateaus on gradient-free optimization*, Quantum 5, 558 (2021), doi:10.22331/q-2021-10-05-558 | Published Quantum PDF (= arXiv:2011.12245v2 file) | In full, 12 pp.; LaTeX searched | No supplement; App. A read | Yes |
| D | Teo, *Optimized numerical gradient and Hessian estimation for variational quantum algorithms*, Phys. Rev. A 107, 042421 (2023), doi:10.1103/PhysRevA.107.042421 | **arXiv:2206.12643v3** (2022-11-20; journal-ref PRA 107, 042421); v1 and v2 compared | In full, 24 pp.; LaTeX read (Secs. II–VII, Apps. A–C) | Apps. A–D read; separate APS Supplemental Material could not be checked | **No** (APS: HTTP 403 challenge; not open access) |
| E | Gentinetta, Thomsen, Sutter, Woerner, *The complexity of quantum support vector machines*, Quantum 8, 1225 (2024), doi:10.22331/q-2024-01-11-1225 | Published Quantum PDF (= arXiv:2203.00031v2 file) | In full, 30 pp.; LaTeX searched | Apps. A–C read; Zenodo code not reviewed | Yes |
| B (re-check) | Aghaei Saem et al., QST 11, 015049 (2026) | Version of record retrieved; compared with arXiv v1 and v2 | Text comparison and crosswalk of all B entries | — | **Yes** (follow-up) |

Local copies are under the git-ignored `research_sources/b5_followup/`. Source URLs, dates and sha256 are in
`results/b5_prior_work/source_manifest.json`.

## 3. Why Teo matters most

Teo 2023 is the only reviewed paper that **computes the error (MSE) of finite-copy parameter-shift gradient estimators**:
- Eq. (13), MSE_PS = d/(N_T(d+1) sin² s);
- that analysis is the basis for the scaled estimator later used in paper B (Eq. C11 = Teo's Eq. 22; B-17).

Its per-θ multinomial identity (Eq. C1), applied to a ±1 observable, reproduces Stage 7's SWAP gradient variance
**exactly** (our algebra, checked numerically). So Teo is the closest located prior work to C3's SWAP side and to the
second-moment part of C1. It also contains:
- the statement that PS errors are independent of n at fixed copies (Eq. 18);
- an exponential copy requirement for distinguishing shifted values (Eq. 26);
- a qualitative remark on wrong update directions (§VII).

All of these are circuit-averaged statements under a two-design (TDS) ensemble with Pauli observables. Full audit:
[`B5_TEO_DEEP_AUDIT.md`](B5_TEO_DEEP_AUDIT.md).

## 4. Candidate 1 overlap

**Candidate 1:** the exact finite-shot gradient distribution, i.e. the PS pmf, the difference-of-binomials law,
P(ĝ = 0), P_correct, P_wrong and the tie probability.

| Item | Arrasmith | Teo | Gentinetta |
|---|---|---|---|
| Gradient MSE (second moment) | Not located (C-NL07) | **EXPLICIT**, circuit-averaged (D-01, D-02, D-05a) | Not located (E-NL06) |
| Exact law / difference of binomials (row 12) | Not located (C-NL09) | Related but different: difference of multinomial means; moments only (D-03a) | Not located (E-NL09); a single-entry binomial law B(R, K_ij) at the kernel level (E-02) |
| P(ĝ = 0) (row 9) | Not located (C-NL09) | Not located (D-NL09) | Not located (E-NL09) |
| P_correct, P_wrong (rows 10–11) | Not located (C-NL09); qualitative decision errors only (C-07) | Related but different: "many wrong update directions", qualitative (D-08a) | Not located (E-NL09) |
| Tie probability | Not located (C-NL09) | Not located (D-NL09) | Not located (E-NL09) |

**Status.**
- Variance and MSE results are located (Teo), but variance is not the full distribution.
- No reviewed paper (A–E) gives the pmf, P(ĝ = 0) with equal-count terms, P_correct, P_wrong or the tie probability of a
  finite-shot parameter-shift gradient.

## 5. Candidate 2 overlap

**Candidate 2:** the conditional Loschmidt sign law P(correct | ĝ ≠ 0) → (1 + |sin θ_k|)/2.

- **Not located** in Arrasmith, Teo or Gentinetta (C-NL13, D-NL13, E-NL13).
- Concepts searched: conditional on a non-zero estimate, single count, sign, direction, Loschmidt/projector,
  (1 + sin)/2.
- Neither Teo nor Arrasmith has a Loschmidt readout. Gentinetta has a Loschmidt-type kernel estimator but no gradient
  of it.
- Teo's qualitative "wrong update directions" (D-08a) is not an equivalent formula. Per the brief, nothing was inferred
  from an MSE bound.

**Status:** not located in any of the five reviewed papers.

## 6. Candidate 3 overlap

**Candidate 3:** a measurement-dependent gradient shot exponent on one landscape, ≈ 4ⁿ (Loschmidt) vs ≈ 16ⁿ (SWAP).

| Item | Arrasmith | Teo | Gentinetta |
|---|---|---|---|
| Exponential shot burden (row 5) | EXPLICIT (C-03, C-04a) | EXPLICIT: D_θ0, base unspecified (D-07a) | EXPLICIT, background attributed to A (E-01) |
| Loschmidt gradient exponent (row 15) | Related but different: gradient-descent reference curve, local-projector cost (readout circuit not described), no exponent (C-04b) | Not located: no projector readout (D-NL02) | Not located (E-NL02) |
| SWAP gradient exponent (row 16) | Related but different (C-04b) | **PARTIAL / IMPLIED** (D-03b) | Not located (E-NL02) |
| Readout changes the exponent (row 18) | Not located (C-NL02) | Related but different: the estimator, not the readout, changes the n-scaling (D-05b) | Not located (E-NL02) |
| Explicit 4ⁿ vs 16ⁿ (row 17) | Not located (C-NL02) | Not located (D-NL17) | Not located (E-NL02) |
| Critical copy number (row 30) | Not located (C-NL07) | EXPLICIT: N_* ≅ 32(d²−1)/(3d), an estimator crossover (D-06) | Not located (E-NL06) |

**The single implied overlap (Teo → SWAP 16ⁿ), five-part write-out** (detail in B5_TEO_DEEP_AUDIT.md §11;
B5_MATH_COMPARISON.md §8.2):
1. **Original equation:** Eq. (C1) (per-θ multinomial moments), averaged in Eq. (C2) and specialised in Eq. (13).
2. **Ensemble and assumptions:** two-design modules (TDS); traceless Pauli observables (±1); independent sampling;
   equal copy split.
3. **Statistic:** circuit-averaged MSE.
4. **Extra algebra:**
   - per-θ use of (C1);
   - PS difference at π/2;
   - f = F± for the SWAP ancilla;
   - N_T = 2M;
   - shift identities, giving Var(ĝ_SWAP) = [2 − A²(1+s²)/2]/(4M);
   - SNR inversion.
5. **Extra Stage 7 assumptions:** product RX landscape (not a two-design); SWAP readout; independent batches; per-θ
   target; median over θ ~ U[−π, π]ⁿ with log-typical A = 4^(−(n−1)).

**Status.**
- The exponential burden is known.
- The SWAP-side 16ⁿ is implied by Teo only with the five steps above.
- The Loschmidt-side 4ⁿ is not implied by Teo. It needs the projector variance from B (B-10a) or E (E-02).
- The same-landscape readout comparison and the explicit 4ⁿ/16ⁿ pair are not located in any of the five papers.

## 7. Candidate 4 overlap

**Candidate 4:** vector alignment, random-walk optimisation, matched starts, signal-free control.

| Item | Arrasmith | Teo | Gentinetta |
|---|---|---|---|
| Random-walk optimisation (row 8) | Related but different: one qualitative sentence for gradient-free optimisers, §3.2, p. 6 (C-05a) | Related but different: "random guesses" wording (D-09) | Not located (E-NL08) |
| Vector alignment / cosine, dot-sign (rows 20, 22) | Not located (C-NL20) | Not located (D-NL20) | Not located (E-NL08) |
| Norm inflation (row 21) | Not located (C-NL20) | Related but different: component-wise mean-square, Eq. 18 (D-04) | Not located (E-NL08) |
| Component sign accuracy (row 23) | Not located (C-NL20) | Related but different, qualitative (D-08a) | Not located (E-NL08) |
| Matched starts (row 24) | Not located (C-NL20) | Not located (D-NL20) | Related but different: noiseless reference warm-started from the noisy endpoint (E-06) |
| Signal-free control (row 25) | Not located (C-NL20) | Not located (D-NL20) | Not located (E-NL08) |

**Status.**
- Random-walk behaviour is known: proven in B (Corollaries 2/4); remarked qualitatively in C.
- Cosine/dot-sign metrics, matched-start comparisons with a signal-free random-walk control, and fidelity endpoints
  are not located in any of the five papers.

## 8. Teo vs Stage 7 mathematics

| Stage 7 | Teo (arXiv v3) | Relation |
|---|---|---|
| ĝ = (Ĉ₊ − Ĉ₋)/2, M per shift | PS (Eq. 11), N_T = 2N per component | Same estimator; N_T = 2M |
| Var(ĝ_SWAP) = [2 − A²(1+s²)/2]/(4M) | Per θ from (C1): [2 − f₊² − f₋²]/(2N_T); average d/(N_T(d+1)) (Eq. 13) | Identical per θ after f = F±, N_T = 2M (our algebra, verified numerically and by Monte Carlo); both ≈ 1/(2M) deep in the plateau |
| Var(ĝ_LE) = [A − A²(1+s²)/2]/(4M) | Not in the model (Pauli ±1 only) | Not located. Teo's term-by-term sampling of the projector would give an O(1)-per-copy (SWAP-like) estimator; shared samples recover Loschmidt (our algebra) |
| P_zero, P_correct, conditional law | None / qualitative | Not located / related but different |
| Required shots: per-θ medians ≈ 4ⁿ, 16ⁿ | N_* ∝ 2ⁿ (crossover); D_θ0 exponential, base not given | Different objects and statistics (§9) |
| Norm inflation ‖ĝ‖/‖g‖ | Mean-square ratio 1 + 2d/N_T (Eq. 18) | Component-wise mean-square analogue |

- **Consistency check.** No Teo formula contradicts a Stage 7 result. Teo's n-independent PS noise matches Stage 7's
  SWAP sd ≈ 1/√(2M) at every n.
- **Arithmetic observation (no Stage 7 impact).** Teo's printed Eq. (23), gradient line, has "−1" where minimising
  Eq. (14) gives "−2", consistent with his Eqs. (22) and (C18) (B5_TEO_DEEP_AUDIT.md §6).

## 9. Statistic-definition differences

From [`B5_STATISTIC_COMPARISON.md`](B5_STATISTIC_COMPARISON.md):
- **Stage 7:** per-θ exact laws, then the **median** of required M over θ.
- **Teo:** **circuit means** (and a mean of a ratio).
- **Aghaei Saem:** **probabilities over initialisations** of indistinguishability, and a per-point/landscape-variance
  ratio ε_N.
- **Thanasilp:** fidelity-level probabilities and fractions, at the mean scale 2^(−n).
- **Arrasmith:** median total shots per run.
- **Gentinetta:** data-size and accuracy complexities at fixed n.

On Stage 7's landscape, with Stage 7's per-shot variances, the statistic alone yields different bases:

| Statistic | Loschmidt | SWAP |
|---|---|---|
| Median | 4ⁿ | 16ⁿ |
| Mean-square (ratio of means) | (4/3)ⁿ | (8/3)ⁿ |
| Teo's two-design average | — | 2ⁿ |
| Average of per-θ requirements, or Teo's D_θ0 | ∞ | ∞ (E_θ[1/A] = ∞) |

Stage 7's 16ⁿ is specific to the per-θ median. Averaged statements cannot be cited for or against it.

## 10. Shot-convention differences

From [`B5_SHOT_CONVENTIONS.md`](B5_SHOT_CONVENTIONS.md):
- **Teo.** N_T is a per-component **total** (2 × per-shift). In Stage 7 units the PS MSE is d/(2M(d+1)) and
  M_* = N_*/2 ≈ (16/3)·2ⁿ.
- **Aghaei Saem.** N is per POVM per quantity (= M), except Eq. (C11), whose N is ambiguous relative to Teo's N_T.
- **Thanasilp.** N is per kernel entry (= M at the fidelity level).
- **Arrasmith.** N is per cost evaluation and N_total per run; not convertible to per-component shots.
- **Gentinetta.** **M is the data-set size** and R the shots. Its R_tot values are run totals.

No exponent or constant was compared numerically before this alignment.

## 11. Arrasmith relationship

See [`B5_ARRASMITH_AUDIT.md`](B5_ARRASMITH_AUDIT.md).
- **The main result** (Prop. 1, Cor. 1) concerns exact cost differences over random parameter points: a landscape
  statistic without a measurement model. It is not a parameter-shift estimator result. It covers the shift pair only as
  exact values (L = π).
- **Explicit content:** exponential precision and exponentially growing shots, numerically via median N_total to C = 0.4
  for n = 5–11, including a gradient-descent reference with an unspecified estimator.
- **The "in passing" random-walk remark** cited by Aghaei Saem (their [38], version of record p. 2) is a single precise
  sentence: §3.2, opening paragraph, last sentence, p. 6. It is qualitative and in the gradient-free context, and it is
  the paper's only random-walk sentence.

## 12. Gentinetta relationship

See [`B5_GENTINETTA_AUDIT.md`](B5_GENTINETTA_AUDIT.md).
- **Estimator.** The kernel estimator is the Loschmidt-type all-zero frequency (Fig. 1, Eq. 9), with Bernoulli variance
  written as (1/R²)[Rk + 2C(R,2)k²] − k² ≤ k/R (Eq. 24), which simplifies to k(1−k)/R (our algebra). SWAP is absent.
- **No variational gradients in the main models.** The dual/primal QSVMs use the quantum device only for kernel
  entries, which feed a classical QP or classical sub-gradients.
- **The approximate QSVM** has variational parameters but trains with SPSA, not parameter shift.
- **Complexities** (O(M^4.67/ε²), O(min{M²/ε⁶, 1/ε¹⁰}), empirical O(1/ε^2.9)) are kernel/model training complexities
  in data size and accuracy at fixed n, with concentration assumed away. They are not VQA parameter-shift gradient
  complexities and are not compared with Stage 7's exponents.

## 13. Updated known-prior-work territory

Now located explicitly in at least one reviewed paper:
- **Finite-copy parameter-shift gradient MSE** (circuit-averaged, Pauli observables, two-design): Teo D-01, D-02,
  D-05a. This is matrix row 29.
- **Critical copy number** for optimised difference estimators vs PS, N_* ≳ O(2ⁿ): Teo D-06 (row 30).
- **PS errors independent of n at fixed copies**, with the mean-square estimate → 1/N_T: Teo D-04 (related to rows 3
  and 21).
- **Exponential copy requirement for gradient-direction resolution**, base unspecified: Teo D-07a; Arrasmith C-03,
  C-04a (row 5).
- **The Loschmidt per-shot (Bernoulli) variance at the fidelity level:** Gentinetta E-02, in addition to B-10a.
- **The random-walk remark** antecedent to B's corollaries: Arrasmith C-05a (qualitative).

## 14. Updated partial/implied territory

- **Stage 7's per-θ SWAP gradient variance, and with Stage 7's landscape and median statistic its ≈ 16ⁿ:** PARTIAL /
  IMPLIED from Teo (D-03b, row 16), in addition to the earlier B-10c (rows 15, 16, 18).
- **Matched-start comparisons** (row 24): Gentinetta's warm-started noiseless reference is related but different
  (E-06), alongside B-07c.
- **Global-Z parity training numerics** (row 28): Gentinetta trains a global Z^⊗q observable with finite shots, but
  with SPSA on ZZFeatureMap + RealAmplitudes circuits (E-05, related but different), alongside B-07a/B-08b.
- **Wrong-direction and noise-dominated estimates** (rows 8, 10, 11, 21, 23): qualitative or averaged counterparts in Teo
  (D-04, D-08a, D-09).

## 15. Updated not-located items

Not located in any of the five reviewed papers (A–E) after the logged searches:
- the exact finite-shot gradient pmf and tie probability; P(ĝ = 0) including equal non-zero counts; exact P_correct and
  P_wrong (rows 9–12; C1);
- the conditional Loschmidt sign law (row 13; C2);
- the same-θ Loschmidt vs SWAP comparison at the gradient level (row 14b);
- the Loschmidt gradient-level shot exponent as a stated result (row 15);
- a readout-dependent gradient exponent as a stated result (row 18);
- the explicit 4ⁿ vs 16ⁿ pair (row 17; C3);
- gradient cosine similarity, P(ĝ·g > 0) and exact component sign accuracy (rows 20, 22, 23);
- matched-start trajectory comparisons with a signal-free random-walk control on fidelity endpoints (rows 24–25 as
  combined in Stage 7; C4).

These are statements about five papers only.

## 16. Aghaei Saem published-version status

**Resolved** ([`B5_VERSION_GAP.md`](B5_VERSION_GAP.md) §1).
- **Retrieval.** One plain request to the DOI was served the IOPscience open-access full text, and its PDF link served
  the version of record (CC BY 4.0). No challenge was bypassed.
- **Dates:** received 2025-08-01; revised 2025-10-23; **accepted 2025-11-20**; **published online 2026-01-30**; print
  issue 2026-03-01; Figure 2 corrected 2026-04-07.
- **arXiv versions.** v1 is 2025-07-29. v2 is **2026-06-04, after publication**. The arXiv record shows the journal-ref
  and DOI, but no statement that v2 is the published text.
- **Text comparison.** 95.6% / 91.0% shingle coverage in the two directions; only publisher boilerplate and affiliations
  differ.
- **Numbering** of equations, figures, theorems and corollaries is identical; sections are arabic.
- **Every B entry** was mapped to a version-of-record locator. Quotes were verified, and the not-located items were
  re-searched (still not located).
- PI-1 is resolved.

## 17. Evidence most important for A1

1. **Teo D-03b (PARTIAL / IMPLIED):** the SWAP gradient variance is reproduced exactly from Teo's per-θ ±1 identity, and
   16ⁿ needs Stage 7's landscape and median statistic. B5_TEO_DEEP_AUDIT.md §9, §11.
2. **Teo D-02 / D-04 / D-07a (EXPLICIT):** the finite-copy PS gradient MSE; PS noise independent of n; an exponential
   copy requirement with an O(1/N) (±1) numerator. Together with B-10a/b/c, these are the located prior formulas behind
   C3.
3. **Teo D-NL02 and §9 of the deep audit:** the Loschmidt (projector) side is outside Teo's model. Term-by-term Pauli
   sampling of the projector would behave like SWAP.
4. **The statistic dependence** (B5_STATISTIC_COMPARISON.md §2): (8/3)ⁿ, 2ⁿ or ∞ vs 16ⁿ for the same variances.
5. **Arrasmith C-05a:** the exact location and qualitative nature of the "in passing" random-walk remark.
6. **Gentinetta E-02 / E-03:** the Loschmidt-type estimator variance at the kernel level, and the fact that its
   complexities are not gradient complexities.
7. **Version of record of B:** all initial-round B evidence holds in the version of record.
8. **PI-4 and PI-5** (B5_POTENTIAL_ISSUES.md): Stage 7's §19 boundary omits Teo 2023, and two summary sentences omit the
   "median" qualifier.

## 18. Remaining literature holes

- **Teo's APS version of record** is not inspected. Locators are arXiv v3, and the Eq. (23) typo status in print is
  unknown.
- **MEDIUM-priority follow-up sources** were not reviewed: Cerezo & Coles 2021; Wang et al. 2024; Huang et al. 2022;
  Rudolph et al. 2024; Liu et al. 2021; Xiong et al.
- **Works cited by C, D or E were not traced.** In particular:
  - **Mari, Bromley, Killoran, PRA 103, 012405 (2021)** (Teo's ref. [61], the origin of SPS) is the highest-priority
    remaining hole. Teo says its expressions are not circuit-averaged (p. 1) and are "large-N forms that are not
    averaged over quantum circuits" (pp. 6–7). So it may contain fixed-θ finite-shot statistics of PS/FD/SPS gradient
    estimators relevant to C1 and C3.
  - van Straaten & Koczor, PRX Quantum 2, 030324 (2021) (Teo's ref. [58]; measurement cost of metric-aware VQAs).
  - Stage 5 §13's Wang et al. 2021 and Qin 2026.
- **No systematic search** (keyword or citation-graph) for exact finite-shot parameter-shift distributions, sign
  probabilities or readout-dependent exponents was performed. B5 is a targeted extraction, not a literature search.
- **Arrasmith v1 and Gentinetta v1** were not compared (their v2 files are the published versions).

## 19. What this audit CAN say

- Exactly where Arrasmith 2021, Teo 2023 (arXiv v3) and Gentinetta 2024 state, or do not state, each candidate-related
  item, under which assumptions and statistics: 49 follow-up ledger entries, each with a page locator; matrix columns
  for all 30 rows.
- That Teo's per-θ ±1 variance identity reproduces Stage 7's SWAP gradient variance exactly, and which additional
  assumptions turn it into 16ⁿ.
- That Teo's model does not contain the Loschmidt readout, so 4ⁿ is not implied by Teo.
- That the reported exponents depend on the statistic, and how the papers' shot conventions convert.
- That the published version of paper B matches arXiv v2, with an entry-by-entry crosswalk.
- That every quote, equation, figure and table number in the ledger (116 entries) is found in the local source texts.
  `tools/b5_evidence.py --verify-sources` checks this, and so does `tests/test_b5_evidence.py` when the local copies
  are present.
- **Quality control.** An independent read-only review checked all 49 follow-up entries against the PDFs, extracted
  text and LaTeX. It confirmed all 26 short quotes as verbatim and ≤ 15 words, every transcribed formula, and the
  Eq. (23) typo. It found:
  - **1 error, corrected.** E-NL06 listed row 28 as not located, but Gentinetta's approximate QSVM uses a global Z^⊗q
    observable. Row 28 moved to E-05 as RELATED BUT DIFFERENT (SPSA, not parameter shift; not a single rotation
    layer). This is the only classification changed by the review.
  - **12 minor issues, corrected:** the Fig. 5 range (n = 1–9); the missing qualifiers "unbiased", "large d" and
    "likely"; the N_T convention for PS; the readout wording for Arrasmith's cost; three page/section fields; the
    exponent precision; Gentinetta's problem sizes; a fuller "copies" search log.
  - **1 systematic wording issue, corrected.** 19 claim categories were reworded to name the target claim, following
    the initial-round convention.
  - Optional notes were also applied: the [sic] on Eq. (23), the s-notation clash, "our algebra" tags, and fuller
    search logs.

## 20. What this audit CANNOT say

- Whether any candidate has precedent elsewhere in the literature. Five papers were reviewed; "not located" is not "absent".
- What the APS version of Teo 2023 contains at any locator.
- Whether the algebra connecting Teo or B to Stage 7 (D-03b; MATH_COMPARISON §6, §8) would be regarded as routine or
  substantive. That judgment belongs to A1.
- Anything about the MEDIUM-priority sources or the untraced references in §18.

*AI assistance:*
- Source acquisition, reading, extraction, derivation checks and document drafting were done with Claude Code, with
  the source copies listed in `results/b5_prior_work/source_manifest.json`.
- The algebra marked "ours" was checked numerically: exact identities, Monte Carlo, and sample checks of the divergent
  averages.
- The packet still needs review by the author and the principal investigator before use in A1.

This remains an evidence extraction for A1 and does not make the novelty decision.
