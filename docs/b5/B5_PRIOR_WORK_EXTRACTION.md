# B5: Prior-work extraction for the Stage 7 candidate contributions

Delegated-track task B5 (Satyabrat work allocation). Baseline: `main` at `ba51866` (Stage 7, 180 tests). This branch
(`dhruv/b5-prior-work-extraction`) is cut from `main`, not from the B3 branch. No scientific code, result or stage
report was modified.

## 1. Purpose

Build a source-traceable evidence packet for the principal novelty audit (A1). It records exactly what the two closest
prior papers do and do not explicitly establish about the four Stage 7 candidate contributions and about the facts
Stage 7 already treats as prior work. **B5 does not judge novelty.** "Not located" means only "not found in the
reviewed version after the logged searches".

Deliverables:
- `B5_PRIOR_WORK_MATRIX.md` — claim × paper matrix.
- `B5_EVIDENCE_LEDGER.md` — 67 evidence entries with exact locators.
- `B5_MATH_COMPARISON.md` — formula-by-formula comparison and separately labelled derived algebra.
- `B5_FOLLOWUP_SOURCES.md`.
- `B5_POTENTIAL_ISSUES.md`.
- `results/b5_prior_work/evidence.csv` — generated from the ledger by `tools/b5_evidence.py`.
- `results/b5_prior_work/source_manifest.json`.
- `tests/test_b5_evidence.py`.

## 2. Papers reviewed

| Id | Paper | Version reviewed | Read |
|---|---|---|---|
| A | S. Thanasilp, S. Wang, M. Cerezo, Z. Holmes, *Exponential concentration in quantum kernel methods*, Nat. Commun. **15**, 5200 (2024), doi:10.1038/s41467-024-49287-w | **Published** article (online 2024-06-18) + published Supplementary Information (MOESM1) | In full: main text pp. 1–13, SI pp. 1–51 |
| B | R. Aghaei Saem, B. Tafreshi, Z. Holmes, S. Thanasilp, *Pitfalls when tackling the exponential concentration of parameterized quantum models*, QST **11**, 015049 (2026), doi:10.1088/2058-9565/ae2202 | **arXiv:2507.22054v2** (2026-06-04), compared with v1 (2025-07-29). The IOP version of record (online 2026-01-30) could **not** be retrieved. | In full: v2 main text + Appendices A–D (27 pp.) and the v2 LaTeX source; v1 compared |

Paper A's author list includes M. Cerezo (the B5 brief's "et al."). Both papers are CC BY 4.0 per Crossref.

**Access limitation (paper B).** Every IOP URL (article, `/pdf`, legacy path, DOI redirect) returned a bot-protection
captcha to scripted requests. The browser extension was not connected. OpenAlex lists no repository copy of the
published version, and there is no Wayback snapshot. arXiv was therefore used, as the brief permits when the published
text is inaccessible. Every B locator is labelled arXiv v2 and none is presented as a published-version locator.

## 3. Review method

1. Downloaded the sources into the git-ignored `research_sources/b5/` (sha256 in the manifest).
2. Read every page:
   - Paper A: main-text and SI pages viewed directly; text extraction was used only for searching and for the
     equation-light projected-kernel and proof pages.
   - Paper B: the full LaTeX source, plus PDF pages viewed to fix compiled section, equation and figure numbers.
3. Concept searches beyond keywords, with surrounding derivations read. Terms: 4ⁿ/16ⁿ, exponent, sample/measurement
   complexity, shots, fidelity, Loschmidt, SWAP, parameter shift, gradient variance/estimation, SNR, statistical
   distinguishability, trainability, sign, direction, conditional, tie, binomial, Skellam, cosine, angle, inner
   product, norm, random walk, trajectory.
4. One ledger entry per (location, claim). Where one passage supports two claims at different strengths it is split
   (e.g. A-06a EXPLICIT for the fidelity-level zero probability, A-06b PARTIAL for the gradient-level question).
5. Matrix cells use only `EXPLICIT`, `PARTIAL / RELATED`, `PARTIAL / IMPLIED` (candidate-3 rows, as requested) and
   `NOT LOCATED`. `tests/test_b5_evidence.py` checks that every cell links to ledger entries of the same
   classification, in both directions.
6. Paper B version check: paragraph-level diff of the v1 and v2 LaTeX sources, plus numbering comparison in both PDFs.
7. Quality control:
   - every EXPLICIT entry was re-checked against its page, number and assumptions;
   - one quote longer than 15 words was removed;
   - one assumption not stated by the source was removed;
   - a script confirmed that every short quote is verbatim and every cited equation/figure number appears on the
     cited page (10 page fields extended to include the page of a cited figure);
   - an independent read-only review of all 67 entries found 18 minor discrepancies (dropped qualifiers, missing
     assumptions, two locators, an axis generalisation, search-log wording), all verified against the sources and
     corrected. No classification label changed, and no NOT LOCATED entry was contradicted.

## 4. What Thanasilp 2024 explicitly establishes (relevant to Stage 7)

- **Fidelity (kernel) concentration**, including the **product single-qubit-rotation family** (Prop. 3, Eq. (26);
  SI Eqs. (207)–(216)): Var ≤ E[κ²] = (3/8)ⁿ, mean 2^(−n), for uniform angles. The per-factor law equals Stage 3–7's
  cos²(θ_j/2) (A-03).
- **Loschmidt estimates collapse to zero** (Prop. 1, Eq. (13); SI Supp. Prop. 2), with the exact single-estimate
  factor (1 − s)^N (SI Eqs. (26)–(27)) and the joint all-zero Gram-matrix probability as a product (SI Eqs. (33)–(36))
  (A-05, A-06a, A-07).
- **SWAP estimates become data-independent**: p₊ = 1/2 + κ/2; null κ̂^(rand) = mean of ±1 equiprobable outcomes
  (Prop. 2, Eq. (14); SI Eqs. (46)–(54)) (A-08).
- **A same-kernel Loschmidt-vs-SWAP comparison**, analytic (Fig. 1, Corollary 1) and numerical, including SI Fig. 4
  on product-R_y kernels for n = 5–40. For Loschmidt it states "N ∈ Ω(2ⁿ)" for a fixed non-zero fraction; for SWAP,
  "at least exponentially" (A-09a, A-10a).
- **Exponential shot burden**, with a range-based (Hoeffding) shot count Ω(b^(2n)/ε̃²) that is the same for both
  readouts (SI Supp. Prop. 5). The source frames it as required; its Gram-matrix corollary assumes per-outcome
  fluctuations stay constant, which holds for ±1 but not for 0/1 Loschmidt outcomes at small F (A-12a, A-13).
- **Binary hypothesis-testing / indistinguishability tools** (SI Note II) and **limits of post-processing,
  multi-copy processing and error mitigation** (SI Notes III C, VIII) (A-11, A-14–A-16).

## 5. What Aghaei Saem 2026 explicitly establishes (arXiv v2)

- **Outcome-probability concentration** for POVMs (Def. 1, Eq. (8)) ⇒ samples **indistinguishable** from a fixed
  distribution with polynomial shots (Theorems 1–2), and **no post-processing** removes this (Corollaries 1, 3)
  (B-03–B-05).
- **Random walk**: polynomial-shot parameter-shift gradient descent on a concentrated Pauli-observable loss is
  statistically indistinguishable from a random walk with explicit null update (B15). Fig. 3 shows displacement
  statistics vs a "Random Walk" reference at n = 15 on a single X-rotation layer with a global-Z cost (B-06a,
  B-07a, B-07b).
- **Exponential budgets in training numerics**: 2ⁿ shots train, 10 × n shots do not, for QNG, CVaR, NN
  initialisation and rescaled parameter shift (Fig. 4, App. C) (B-08a, B-08b).
- **v2 only:**
  - The same fidelity objective under Loschmidt vs SWAP POVMs: fixed distributions (0, 1) vs (1/2, 1/2) (Fig. 5).
  - Per-shot estimator variances F(1 − F) vs 1 − F².
  - The resolution ratio ε_N (Eq. (12)) and the statement that different estimators change how badly shot noise hurts.
  - Classical shadows are POVM post-processing.

  (B-09a, B-10a, B-10b, B-12.)

## 6. Evidence relevant to candidate 1 (exact finite-shot gradient zero/sign probabilities)

- **Zero probability:** both papers give it only at the fidelity-estimate level. A gives the exact (1 − s)^N; B
  states that the Loschmidt estimate is zero w.h.p. (†). The gradient-level P(ĝ = 0) = Σ_r Bin(r; M, F₊)Bin(r; M, F₋),
  including equal nonzero counts, is **not located**. A's factor reproduces only its r = 0 term (MATH_COMPARISON §6.1).
  → Row 9: PARTIAL / RELATED (A, B).
- **P_correct / P_wrong:** **not located** in A. B's random-walk indistinguishability bears on the sign but gives no
  probability. → Rows 10–11: A NOT LOCATED; B PARTIAL / RELATED.
- **Difference-of-binomials law:** B writes the Pauli update as a difference of two ±1 means (B18, B26) without
  deriving its distribution or tie probability. → Row 12: A NOT LOCATED; B PARTIAL / RELATED.

## 7. Evidence relevant to candidate 2 (conditional Loschmidt sign law)

**Not located in either reviewed source** after concept searches (conditional probability, given nonzero, sign,
direction, single count, success probability, (1+|sin|)/2). No located formula from which it follows was found.
→ Row 13: NOT LOCATED (A, B).

## 8. Evidence relevant to candidate 3 (same-landscape readout-dependent gradient shot scaling)

- **Located:**
  - B: the per-shot fidelity-estimator variances and ε_N (†). B states that estimator choice affects shot-noise
    impact but computes **no exponent**.
  - A: same-kernel two-readout comparisons, analytic and numerical (SI Fig. 4). Its only exponent statements are
    Ω(2ⁿ) (Loschmidt, kernel level, numerical) and "at least exponentially" (SWAP). Its resolution bound is
    range-based and therefore identical for both readouts; the constant-fluctuation assumption behind it is the
    property that differs between readouts, a link the source does not make (MATH_COMPARISON §6.8).
- **Not located** in either source:
  - a parameter-shift gradient sample complexity for either readout;
  - any 4ⁿ or 16ⁿ statement or fitted exponent;
  - a same-θ gradient-level comparison.
- **Implied (B):** B's formulas imply a readout-dependent exponent only after added algebra and assumptions
  (MATH_COMPARISON §6.2–§6.3):
  - under B's own 2-design setting and ε_N criterion, at the fidelity level: ≈2ⁿ (Loschmidt) vs ≈4ⁿ (SWAP);
  - Stage 7's 4ⁿ vs 16ⁿ (gradient level, product landscape) additionally needs the parameter-shift step, the
    product-landscape shift identities, a per-θ SNR/sign criterion (B's ε_N gives (2/3)ⁿ, or (4/3)ⁿ at the mean F,
    vs (8/3)ⁿ there) and the
    log-typical A, none of which is in either source.
- → Rows 4, 14a–18: 14a EXPLICIT (fidelity level, A and B†); 14b NOT LOCATED (A, B); 15–16 A PARTIAL / RELATED,
  B PARTIAL / IMPLIED; 17 NOT LOCATED (A, B); 18 A NOT LOCATED, B PARTIAL / IMPLIED.

## 9. Evidence relevant to candidate 4 (full-vector / trajectory consequences)

- **Random walk:** explicit in B (Corollaries 2/4, Fig. 3) for Pauli/±1 outcomes, with probability ≥ 1 − c over
  initialisation. B's random-walk curve is a displacement-statistics reference whose construction is not stated.
  Whether starts are matched across shot budgets is not stated.
- **Separate metrics:** cosine, norm ratio, P(ĝ·g > 0) and component sign accuracy are **not computed** in either
  source. "Optimizer behaves like a random walk" (B) is related to these but is not the same statement.
- **Full-vector zero probability:** A has a product-form joint all-zero probability for Gram matrices, not gradient
  vectors.
- **A signal-free control:** exists in A for kernel models (random Gram matrix), not for trajectories.
- → Rows 8, 19–25: 8 B EXPLICIT; 19 PARTIAL (A, B†); 20–23 A NOT LOCATED, B PARTIAL / RELATED; 24 A NOT LOCATED,
  B PARTIAL; 25 A PARTIAL, B EXPLICIT.

## 10. Known prior-work territory (facts the final paper should not claim)

| Brief fact | Status | Where |
|---|---|---|
| A. Exponential concentration of fidelity/kernel quantities | EXPLICIT (A, B) | A Def. 1, Thm 1, Prop. 3 (product family); B Def. 1 |
| B. Loschmidt estimates collapsing toward zero | EXPLICIT (A, B†) | A Prop. 1, SI Supp. Prop. 2; B §IV |
| C. SWAP estimates becoming data-independent / random | EXPLICIT (A, B†) | A Prop. 2, SI Eqs. (46)–(54); B §IV |
| D. Different POVMs having different estimator variances | EXPLICIT (B†); PARTIAL (A: outcome models only) | B §IV p. 10 |
| E. Exponential measurement/sample burden | EXPLICIT (A, B) | A SI Supp. Prop. 5, SI Fig. 4; B Thm 2, Fig. 4, Eq. (12)† |
| F. Outcome distributions / distinguishability as the finite-shot object | EXPLICIT (A, B) | A SI Note II; B Def. 1, Thm 2, App. A |
| G. Polynomial-shot optimisation random-walk-like | EXPLICIT (B); not located (A) | B Cor. 2/4, Fig. 3 |
| H. Limits of post-processing / mitigation | EXPLICIT (A, B) | A SI Def. 3, Notes III C, VIII; B Cor. 1/3, §IV |

Also located: the single X-rotation layer + global-Z (parity) training setup of Stage 6 is B's numerical setup
(row 28; already noted in STAGE6.md §19).

## 11. Partial / implied overlaps

- Row 4: A gives the outcome models from which the variances follow in one line (B states them, †).
- Row 9: fidelity-level zero probabilities (A exact, B qualitative †) vs gradient-level P(ĝ = 0).
- Rows 10–12: B's ±1 difference structure and random-walk indistinguishability vs exact sign probabilities and the
  difference-of-binomials pmf.
- Rows 15–16, 18: A's kernel-level numerics; B's variances + ε_N imply readout-dependent exponents only after
  §6.2–§6.3 algebra (PARTIAL / IMPLIED).
- Row 19: A's product-form Gram-matrix all-zero probability; B's fidelity-level zero.
- Rows 20–23: B's random-walk statement vs specific alignment/norm/sign metrics.
- Row 24: B's multi-budget trajectories without stated start matching.
- Row 25: A's random-matrix model control vs a trajectory control.
- Row 27: B uses the same circuit with a different cost.

## 12. Items not located in the reviewed sources

Not located after the logged searches (ledger entries A-NL07 … A-NL28, B-NL13, B-NL14b, B-NL17):
- the conditional Loschmidt sign law (both papers);
- a same-θ gradient-level Loschmidt-vs-SWAP comparison (both);
- an explicit 4ⁿ vs 16ⁿ statement or any fitted exponent (both);
- in A: parameter-shift analysis, random walk, gradient P_correct/P_wrong, the difference-of-binomials law, a
  readout-dependent exponent, cosine, norm, ĝ·g, component sign accuracy, matched-start trajectories, global-Z
  training numerics.

"Not located" is limited to these two reviewed versions. It is not a statement about the wider literature.

## 13. Version differences (Aghaei Saem, arXiv v1 → v2)

- **Inserted in v2:**
  - the entire Loschmidt-vs-SWAP passage ("Subtlety regarding the choice of POVM": Fig. 5, Eq. (12) ε_N, both
    estimator variances, purity example);
  - the measure-first/classical-shadow passage (Eq. (11));
  - the global-Z parity-POVM example.
- **Reworded:** Corollary 4 ("results in" → "is statistically indistinguishable from a random walk").
- **Clarified:** the Fig. 3 caption now defines the plotted statistic.
- **Renumbered:** App. A (v2 adds Definition 2); main-text Eqs. (1)–(10), Figs. 1–4 and App. B–D equation numbers
  are unchanged.
- **Consequence:** all paper-B evidence on rows 2–4, 9, 14a–16, 18 and 19 rests on v2 text. Whether the published
  version (2026-01-30, before v2 was posted) contains it, and at which locators, is **unverified** (ledger "Open
  items"; B5_POTENTIAL_ISSUES PI-1).

## 14. Follow-up papers identified

Only works the two sources cite near candidate-relevant claims (B5_FOLLOWUP_SOURCES.md; not exhaustive, not reviewed):
- **HIGH:**
  - Arrasmith et al., Quantum 5, 558 (2021) — random-walk remark, shot cost of loss differences;
  - Teo, PRA 107, 042421 (2023) — finite-shot parameter-shift gradient estimator statistics;
  - Gentinetta et al., arXiv:2203.00031 — shot complexity of fidelity-kernel estimation.
- **MEDIUM:** Cerezo & Coles QST 2021; Wang et al. Quantum 2024; Huang et al. Science 2022; Rudolph et al. npj QI 2024;
  Liu et al. Nat. Phys. 2021; Xiong et al. 2023/2025.
- **BACKGROUND:** barren-plateau and cost-concentration references, plus the Stage 3 benchmark source.

## 15. What this extraction CAN say

- Exactly where each of the two papers states (or does not state) each candidate-related item, under which
  assumptions, and at which locator (published version for A; arXiv v2 for B).
- That facts A–H of the brief are explicitly established in these sources (G only in B; D explicitly only in B v2).
- That several candidate items have only fidelity-level, structural or implied counterparts in these sources, and what
  extra steps would connect them (MATH_COMPARISON §6).
- That the Stage 7 outcome models and per-shot variances match the sources exactly (B5_POTENTIAL_ISSUES).

## 16. What this extraction CANNOT say

- Whether any candidate has precedent elsewhere in the literature. Only two papers were reviewed, and "not located" is not "absent".
- What the published version of paper B contains at any locator (not inspected).
- What the follow-up works contain.
- Whether the implied algebra in MATH_COMPARISON §6 would be regarded as an obvious consequence or as a substantive
  step. That judgment belongs to A1.

## 17. Follow-up audit (2026-10-04)

The three HIGH-priority follow-up sources were reviewed in a targeted follow-up audit on this branch:
- Arrasmith 2021;
- Teo 2023 (as arXiv v3);
- Gentinetta 2024.

The version of record of paper B was also retrieved, and it matches arXiv v2. Summary:
[`B5_FOLLOWUP_AUDIT.md`](B5_FOLLOWUP_AUDIT.md). Detail files:
- `B5_TEO_DEEP_AUDIT.md`, `B5_ARRASMITH_AUDIT.md`, `B5_GENTINETTA_AUDIT.md`;
- `B5_STATISTIC_COMPARISON.md`, `B5_SHOT_CONVENTIONS.md`, `B5_VERSION_GAP.md`;
- ledger entries C-xx, D-xx, E-xx and the row 29–30 entries; matrix columns for the three papers;
- `B5_MATH_COMPARISON.md` §8; `B5_POTENTIAL_ISSUES.md` PI-4 and PI-5.

§16's second bullet (the published version of paper B) no longer applies.

## 18. Closure audit (2026-10-05)

The closure audit added three papers and a targeted search: Mari et al. 2021 (F), Miranskyy 2025 (G) and Zhan et al.
2025 (H). It also added matrix rows 31–33 for the principal track's C5 statements and the general form of C2, and a
line check of the principal track's prior-work pointers. Summary: [`B5_CLOSURE_AUDIT.md`](B5_CLOSURE_AUDIT.md).

*AI assistance:* source acquisition, reading, extraction and cross-checking were done with Claude Code (including an
independent read-only review pass). Every locator was verified against the local source files listed in
`results/b5_prior_work/source_manifest.json`. The packet still needs review by the author and the principal
investigator before it is used in the A1 audit.

This document is evidence for the principal novelty audit. It does not make the novelty decision.
