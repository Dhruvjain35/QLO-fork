# B5 potential issues

Issues noticed while reading the two prior papers. **Nothing here was fixed.** No Stage 1–7 file was modified.

## Outcome of the numerical cross-check

**No numerical or code issue found.** The Stage 7 outcome models and per-shot variances match the sources exactly:

| Stage 7 (code / STAGE7.md) | Source |
|---|---|
| Loschmidt: one shot ~ Bernoulli(F); `estimators.fidelity_estimate("loschmidt", K, M) = K/M`; `fidelity_estimate_variance` = F(1 − F)/M | A main Eq. (12) and p. 4; A SI Eq. (17); B §IV Var^(LE) = F(1 − F) per shot (B-10a†) |
| SWAP: ancilla +1 w.p. q = (1 + F)/2; `fidelity_estimate("swap", K, M) = 2K/M − 1`; variance (1 − F²)/M | A main p. 4 (p₊ = 1/2 + κ/2); A SI Eq. (46); B §IV Var^(SWAP) = 1 − F² per shot (B-10a†) |
| Fidelity-level Loschmidt zero probability (1 − F)^M (`analysis.prior_work_replication`: `p0 = exp(M log1p(−F))`) | A SI Eqs. (26)–(27), conditional factor (1 − s)^N |

The structural statements Stage 7 lists as prior work (§3, §18, §19) are present in the sources:
- Loschmidt estimates collapse to zero: A Prop. 1, SI Supp. Prop. 2; B §IV†.
- SWAP estimates become data-independent: A Prop. 2, SI Supp. Lemma 3; B §IV†.
- Global-Pauli parameter-shift GD is a random walk: B Corollaries 2/4.

## Items for the principal audit (documentation / wording, not code)

### PI-1 · Version provenance of the Loschmidt/SWAP statements attributed to Aghaei Saem et al.
- **Suspected issue:**
  - STAGE7.md §3, §19 and §22 attribute to *Aghaei Saem et al., QST 11, 015049 (2026)*:
    - that Loschmidt and SWAP give different fixed distributions for the same fidelity;
    - that different POVMs for the same quantity have different estimator variances.
  - In the arXiv record these statements appear in **v2 (2026-06-04)**, §IV "Subtlety regarding the choice of
    POVM", and are **absent from v1 (2025-07-29)**.
  - The published (IOP) version of record could not be retrieved in B5, so whether it contains this passage, and
    under which section/equation numbers, is unverified.
- **Source evidence:** B5_EVIDENCE_LEDGER.md entries B-09a, B-10a, B-10b, B-10c; version table V-01.
- **Why it might matter:** A paper citing the QST article for these points needs the version-of-record locator.
  Citing arXiv v1 for them would be wrong.
- **Stage 7 location potentially affected:** `STAGE7.md` §3, §19, §22 (prose only). No code.
- **Follow-up status (2026-10-04): resolved.**
  - The version of record was retrieved through its DOI, and its text matches arXiv v2.
  - The attributed statements are in §4 "Subtlety regarding the choice of POVM", pp. 9–10: Fig. 5, Eq. (12), and
    Var^(SWAP) = 1 − F² and Var^(LE) = F(1 − F) on p. 10.
  - Equation and figure numbers equal v2's; sections are arabic-numbered.
  - Crosswalk: [`B5_VERSION_GAP.md`](B5_VERSION_GAP.md). When citing, use the version-of-record pages.

### PI-2 · Arithmetic-mean vs log-typical scales when positioning against Thanasilp et al.
- **Suspected issue:**
  - Paper A states its shot requirements in terms of the mean kernel value μ = 2^(−n) (e.g. "N ∈ Ω(2ⁿ)" for a fixed
    non-zero fraction of Loschmidt estimates, SI Fig. 4a).
  - Stage 5/7 express medians through the log-typical A = 4^(−(n−1)) (≈ 4ⁿ for Loschmidt).
  - Both are consistent (Ω(2ⁿ) is a lower bound), but a side-by-side quotation could look like a conflict unless
    the two scales are named explicitly.
- **Source evidence:** A-10a, A-10b; B5_MATH_COMPARISON §1, §6.3.
- **Why it might matter:** Positioning text (A4) comparing exponents.
- **Stage 7 location potentially affected:** `STAGE5.md` §7, `STAGE7.md` §11–§12 wording when cited against A. No
  code.

### PI-3 · Probabilistic qualifier on the random-walk statement
- **Suspected issue:**
  - Paper B's Corollaries 2/4 hold "with high probability" over the random initialisation (probability ≥ 1 − c,
    c ∈ O(exp(−n))).
  - STAGE7.md §17 and the README Stage 7 paragraph state that SWAP-driven GD at n ≥ 10 "is indistinguishable from a
    signal-free random walk" without that qualifier.
  - Yet Stage 7's own table shows non-zero success for SWAP at n = 10: P(F_final ≥ 0.5) between 0.04 and 0.14
    across variants, against 0 for the random walk.
- **Source evidence:** B-06a (assumptions and scope); B-14 (source's own positioning).
- **Why it might matter:** The prior-work statement is probabilistic over initialisations. Matching its scope avoids
  over-generalising Stage 7's diagnostic. (This point was examined numerically on the separate B3 branch; B5 does not
  use or depend on that work.)
- **Stage 7 location potentially affected:** `STAGE7.md` §17, §18, §20 F, §21; `README.md` Stage 7 paragraph (prose
  only). Function `qlo.stage7.analysis.optimization_diagnostic` is **not** suspected of any error.

## Items added by the follow-up audit (2026-10-04)

Prior work reviewed in the follow-up (Teo 2023; Arrasmith 2021; Gentinetta 2024) raised the two interpretation points
below. As before, **nothing was fixed** and no Stage 1–7 file was modified. The numerical cross-check found no conflict:
- Teo's per-θ ±1 variance, applied to the SWAP ancilla, equals Stage 7's Var(ĝ_SWAP) exactly.
- Teo's averaged PS error ≈ 1/N_T = 1/(2M) matches Stage 7's deep-plateau SWAP variance.
- Teo's n-independent PS noise matches Stage 7 §7's SWAP sd ≈ 1/√(2M) at every n.

### PI-4 · Stage 7's prior-work boundary omits finite-copy parameter-shift error analyses
- **Suspected issue.** STAGE7.md §19 lists the prior work Stage 7 does not claim (Thanasilp 2024; Aghaei Saem 2026),
  then says Stage 7 "focuses more narrowly on the finite-shot *parameter-shift gradient* distributions …". The section
  does not mention the following.
  - **Teo 2023** analyses the finite-copy error of parameter-shift gradients:
    - MSE_PS = d/(N_T(d+1) sin² s) (Eq. 13);
    - PS errors asymptotically independent of n (Eq. 18; conclusion);
    - an exponential copy requirement for distinguishing shifted values (Eq. 26);
    - a qualitative remark that small MSEs can still give "many wrong update directions" (§VII).

    Its per-θ ±1 variance identity (Eq. C1) gives Stage 7's SWAP gradient variance exactly (D-02, D-03b).
  - **Arrasmith 2021** contains the qualitative random-walk sentence that Aghaei Saem et al. cite as "mentioned in
    passing" (§3.2, p. 6; C-05a), and exponential-shot numerics for optimisation (C-03, C-04a).
  - Neither contains Stage 7's exact zero/sign probabilities, the conditional sign law, the Loschmidt variance or a
    readout comparison (D-NL02, D-NL09, D-NL13, C-NL02, C-NL09, C-NL13).
- **Source evidence:** D-02, D-03b, D-04, D-07a, D-08a; C-05a; B5_TEO_DEEP_AUDIT.md §10–§11.
- **Why it might matter.** Positioning text (A4) that describes Stage 7's gradient-variance or SNR results without Teo
  2023 would omit the closest located finite-copy parameter-shift error analysis. STAGE7.md §22 already notes that D
  "follows directly from the per-shot variances". Teo adds that the SWAP-side variance structure is located at the
  gradient level (per θ only by implication). The Loschmidt side is still not located in Teo.
- **Stage 7 location potentially affected:** `STAGE7.md` §3, §19, §22 (prose only). No code.

### PI-5 · The 4ⁿ/16ⁿ statement depends on the statistic; some summary sentences omit the qualifier
- **Suspected issue.**
  - Stage 7's exponents are slopes of **median** required shots over θ ~ U[−π, π]ⁿ, explained by the log-typical
    A = 4^(−(n−1)). STAGE7.md §12 and §21 and the README Stage 7 paragraph say "median".
  - Two summary sentences do not: the README file-map line for `STAGE7.md` ("4^n vs 16^n gradient shots") and the
    parenthesis in STAGE7.md §23 ("already 16ⁿ vs 4ⁿ in shots").
  - The follow-up audit shows that the same per-shot variances give other bases under other statistics: mean-square
    criteria give (8/3)ⁿ vs (4/3)ⁿ on the same landscape, Teo's two-design ensemble gives 2ⁿ, and averages of per-θ
    requirements are infinite (E_θ[1/A] = ∞).
- **Source evidence:** B5_STATISTIC_COMPARISON.md §2 and §4; D-02, D-07a; B5_TEO_DEEP_AUDIT.md §9.
- **Why it might matter.** A reader comparing Stage 7 with Teo (circuit means) or with Aghaei Saem's ε_N (landscape
  variance) could see an apparent contradiction unless the statistic is named. The measured medians themselves are not
  in question.
- **Stage 7 location potentially affected:** `README.md` file map (STAGE7.md line); `STAGE7.md` §23 (prose only).
  No code, no numbers.

## Item added by the closure audit (2026-10-05)

### PI-6 · The per-shot variances are attributed to Aghaei Saem et al. alone
- **Suspected issue.** STAGE7.md §19 lists among the things Aghaei Saem et al. (2026) "already show" that "different
  POVMs for the same quantity can have different estimator variances". The same Loschmidt-type and SWAP-type per-copy
  variances appear in an earlier source:
  - **Zhan et al.**, Light Sci. Appl. 14, 83 (published 2025-02-12; arXiv v1 2024-06-10). It gives v_proj = c(1 − c)/N
    for projection onto a known state (SI p. 23; Eq. 3) and v_scm = (1 − c²)/N for the destructive swap test (Eq. 10;
    SI p. 17).
  - It also explicitly compares their precision as a function of overlap ("lower precision for small c", p. 5)
    (H-01, H-02).
  - Aghaei Saem et al.'s version of record is dated 2026-01-30, and the passage is absent from their arXiv v1.
- **Source evidence:** H-01, H-02; B-10a; B5_VERSION_GAP.md §1 and §4; B5_PRINCIPAL_LINE_CHECK.md L10, L17.
- **Why it might matter.** Positioning text that credits the variance pair only to Aghaei Saem et al. would omit the
  earlier source. The principal track's A2 proof and A4 draft use the same attribution; that document is outside this
  file's scope, and the point is recorded in the line check.
- **Stage 7 location potentially affected:** `STAGE7.md` §19 (prose only). No code, no numbers.

This file records observations for the principal audit and does not make the novelty decision.
