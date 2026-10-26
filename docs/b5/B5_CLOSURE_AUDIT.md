# B5 closure audit

Branch `dhruv/b5-prior-work-extraction`, on top of the follow-up audit (commit 75fe5f3). This is evidence for the
principal novelty audit (A1). It records what prior papers contain. It does not classify the candidates and does not
revisit A1 or A2. No Stage 1–7 code, report or result was changed.

## 1. Scope

This closure was run after the principal track was merged on the canonical repository (`upstream/main` 8003375,
`principal/QLO_Principal_Track.md`). A separate written closure brief was not available in this working session, so the
scope was taken from three places:
1. the remaining holes listed in `B5_FOLLOWUP_AUDIT.md` §18:
   - Mari et al. 2021, the highest-priority untraced reference;
   - "no systematic search was performed";
2. the request to complete the closure "including Mari 2021 and the targeted search";
3. the principal track's B5 items:
   - line-check its prior-work map against the PDFs (§0, §6 item 3);
   - add Aghaei Saem §IV/Fig. 5 and Thanasilp Props. 1–2 as required rows (§6);
   - evidence for its candidate statements C5 (shot-ratio identity, exponent rule) and the general form of C2 (§3).

Classification vocabulary as before: `EXPLICIT`, `PARTIAL / IMPLIED`, `RELATED BUT DIFFERENT`, `NOT LOCATED`.
NOT LOCATED means only "not found in the reviewed version after the logged searches".

## 2. Deliverables

| File | Content |
|---|---|
| [`B5_MARI_AUDIT.md`](B5_MARI_AUDIT.md) | Full audit of Mari et al. 2021 (paper F) |
| [`B5_CLOSURE_SEARCH.md`](B5_CLOSURE_SEARCH.md) | Targeted search: protocol, queries, counts, screening of 1,060 records, results, limits |
| [`B5_PRINCIPAL_LINE_CHECK.md`](B5_PRINCIPAL_LINE_CHECK.md) | Line check of the principal track's 31 prior-work pointers and statements |
| `B5_EVIDENCE_LEDGER.md` | 38 entries added (154 in total): papers F, G, H, and rows 31–33 for papers A–E |
| `B5_PRIOR_WORK_MATRIX.md` | Rows 31–33; part 2 with columns for F, G, H; the principal-track required-rows crosswalk |
| `B5_MATH_COMPARISON.md` §9 | The identity's ingredients by source; estimation vs detection readout ratios |
| `B5_STATISTIC_COMPARISON.md`, `B5_SHOT_CONVENTIONS.md`, `B5_VERSION_GAP.md` §4 | Closure rows |
| `B5_POTENTIAL_ISSUES.md` | PI-6 (attribution of the per-shot variances) |
| `tools/b5_closure_search.py`, `results/b5_prior_work/closure_search_*.{csv,json}` | Reproducible search and screening record |

## 3. Papers added

| Id | Paper | Version reviewed | Read |
|---|---|---|---|
| F | Mari, Bromley, Killoran, *Estimating the gradient and higher-order derivatives on quantum hardware*, Phys. Rev. A 103, 012405 (2021) | arXiv:2008.06517v2, byte-identical to the institutional-repository post-print; APS version not inspected (HTTP 403) | In full, 17 pp. incl. App. A |
| G | Miranskyy, *The Cost of Certainty: Shot Budgets in Quantum Program Testing*, arXiv:2510.22418 (2025) | v1, the only version (preprint) | In full, 30 pp. incl. App. A–D |
| H | Zhan, Wang, Mi, Xie, Xu, Zhang, Zhang, *Experimental benchmarking of quantum state overlap estimation strategies with photonic systems*, Light Sci. Appl. 14, 83 (2025) | Published version + published SI; arXiv v1 checked for dating | In full, 12 + 26 pp. |

Sources are in the git-ignored `research_sources/b5_closure/`, with sha256 in
`results/b5_prior_work/source_manifest.json`.

## 4. Key content of the added papers

- **Mari 2021 (F).**
  - Prints the per-θ variance of the finite-shot parameter-shift estimator with a separate single-shot variance at
    each shift: Var = [σ₀²(θ + s) + σ₀²(θ − s)]/(4N sin² s) (Eq. 45, p. 7; F-01). The statistic is an MSE at a fixed
    parameter point.
  - Names both fidelity readouts (swap test, or the 00…0 bitstring) for one survival probability without comparing
    them (p. 3; F-03).
  - Leaves σ₀² unspecified (F-02).
  - Shows a numerical FD/PS crossover at N ≈ 50 shots (F-07) and matched-start trajectories against an exact-gradient
    path on a 2-parameter hardware problem (F-06).
  - Proposes the scaled estimator for noise-dominated barren plateaus (F-08).
  - Printed Eq. (49) has 2N where Eqs. (45), (48) and (50) imply 4N.
- **Miranskyy 2025 (G).**
  - Compares inverse-test and swap-test **detection** shot counts for one fidelity: N ≲ ln P_e / ln F vs
    ln P_e / ln[(1 + F)/2], ratio → 2 as F → 1 (p. 9; G-01).
  - Prints both outcome models (G-02) and the all-accept probabilities F^N and ((1 + F)/2)^N (G-03).
  - Notes that the swap test accepts orthogonal states with probability 0.5 (G-05).
  - Covers detection near F = 1 only: no estimation variances, no gradients, no concentration.
- **Zhan 2025 (H).**
  - Prints the per-copy variances of projection onto a known state, c(1 − c)/N (SI p. 23; Eq. 3), and of the
    swap-type estimators (Schur collective measurement, ideal swap test), (1 − c²)/N (Eq. 10; SI p. 17) (H-01).
  - Compares them for the same overlap, with swap-type estimators less precise at small overlap (p. 5; H-02).
  - The statements date from arXiv v1 (2024-06-10); the paper was published 2025-02-12.
  - Overlap level only: no gradients and no concentration.

## 5. Candidate evidence after the closure

| Candidate | Rows | Change from the follow-up audit |
|---|---|---|
| C1 (exact gradient law, P_zero, P_correct, P_wrong, ties) | 9–12, 19 | Still not located in A–H. Closest items added in the closure: Mari's noise moments (F-04), Miranskyy's all-accept probabilities (G-03), Zhan's single-estimate binomial law (H-04) — all related but different |
| C2 (conditional sign law; product form row 13, general form row 33) | 13, 33 | Not located in A–H; the targeted search found no record stating it (B5_CLOSURE_SEARCH.md §5) |
| C3 (readout-dependent exponent, 4ⁿ vs 16ⁿ) | 4, 14a, 15–18 | Fidelity-level readout comparisons are now explicit in two further sources: Zhan (estimation precision) and Miranskyy (detection near F = 1). The gradient-level exponents and the explicit 4ⁿ/16ⁿ pair are still not located |
| C4 (vector / trajectory) | 8, 20–25 | Mari: matched starts across shot budgets with an exact-gradient reference on a toy problem (F-06, EXPLICIT for row 24); no signal-free control or barren plateau. Vector metrics still not located |
| C5 (shot-ratio identity; exponent rule) | 31, 32 | Not stated in A–H. Implied (PARTIAL / IMPLIED) by the per-shot statistics of A, B, G and H applied at the two shifts; Mari prints the general per-θ variance structure (RELATED BUT DIFFERENT); Teo has the SWAP side only. The exponent rule's accounting structure appears in a different setting in Sulimov & Lehmann 2026 (screened; full read recommended) |

## 6. Line check of the principal track

Of the principal track's 31 prior-work pointers and statements:
- 24 are confirmed: two need a version-of-record locator update, five a qualifier, and four are confirmed at metadata or
  abstract level only;
- 3 are partly confirmed;
- 3 are outside B5's scope;
- 1 is consistent with the documented search.

The factual additions ([`B5_PRINCIPAL_LINE_CHECK.md`](B5_PRINCIPAL_LINE_CHECK.md) §7) are:
- Thanasilp's SI has a numerical same-kernel shot study of both tests (L8);
- the per-shot variance pair appears earlier in Zhan et al. 2025 (L10, L17; PI-6);
- Mari Eq. (45) prints the general per-θ variance used in the A2 proof (L17);
- "The Cost of Certainty" factor of two is a near-F = 1 detection statistic (L21–L22);
- the principal track's §6 B1 acceptance check writes b_SWAP = b_LE − b_S, the opposite sign to the rule derived in
  its §3 (b_SW = b_LE + b_S) (line check §6b).

## 7. Version status

| Paper | Status |
|---|---|
| Aghaei Saem 2026 (B) | Version of record reviewed (follow-up audit) |
| Teo 2023 (D) | APS version not inspected (HTTP 403); arXiv v3 locators |
| Mari 2021 (F) | APS version not inspected (HTTP 403); arXiv v2 = institutional post-print |
| Miranskyy 2025 (G) | Preprint only |
| Zhan 2025 (H) | Version of record and published SI reviewed |

## 8. Remaining holes

- **APS versions of Teo 2023 and Mari 2021.** These need institutional access. Their equation numbers are unverified,
  and so is whether the printed typos (Teo Eq. 23, Mari Eq. 49) persist.
- **Sulimov & Lehmann 2026 (arXiv:2609.14424).** Screened only; a full read is recommended before the exponent rule is
  positioned.
- **Library databases** (Scopus, Web of Science, INSPEC) were not searched, and Semantic Scholar answered only 2 of 17
  queries.
- **Medium-priority sources** in `B5_FOLLOWUP_SOURCES.md` are still unreviewed, as are backward references of F, G
  and H.
- **Teo 2024** (noise extension) was not reviewed (B4 territory).

## 9. What this closure can and cannot say

- **Can:**
  - where eight papers state, or do not state, each candidate-related item, with page locators (154 ledger entries,
    every quote and equation, figure and table number checked against the local sources by
    `tools/b5_evidence.py --verify-sources`);
  - which printed formulas supply the ingredients of the principal track's identity;
  - how fidelity-level estimation and detection comparisons differ from the gradient-level statements;
  - which principal-track pointers needed qualifiers.
- **Cannot:**
  - whether any candidate has precedent elsewhere in the literature — eight papers and a targeted open-database search were reviewed,
    and "not located" is not "absent";
  - what the APS versions of Teo and Mari contain;
  - whether the algebra from printed variances to the identity or the rule is routine or substantive. That is A1's
    judgment, already made by the principal track and not revisited here.

**Quality control.** An independent read-only review checked all 36 closure entries and the line check against the
PDFs, LaTeX and extracted text:
- It confirmed every short quote and every transcribed formula, and re-ran the not-located searches without
  contradiction.
- **1 error, corrected.** My Assumption 1 statement (F-02, B5_MARI_AUDIT §3, B5_MATH_COMPARISON §9.1) had the
  condition backwards. Corrected and checked numerically: for the Loschmidt readout at small fidelity it fails by the
  factor (1 + cos θ_k) and holds only where cos θ_k ≈ 0.
- **Minor items, all corrected:**
  - locator fixes in A-19, F-06, G-01, G-02, H-01, H-04;
  - wording in F-03 and F-05;
  - stated approximations for the exponent rule in A-19, B-18, G-02, H-03;
  - two entries added for consistent treatment (F-11 for row 21, G-06 for row 5);
  - fuller search logs;
  - line-check fixes: qualifiers on L2/L4, the figure in L8, labels for L23/L28, the citation mapping in L29, removal
    of an evaluative sentence from L20, and a new item L31.
- The review also spotted the principal track's sign inconsistency recorded above.

*AI assistance:*
- Source acquisition, the search, reading, extraction and drafting were done with Claude Code, using the sources listed
  in `results/b5_prior_work/source_manifest.json`.
- Algebra marked "ours" was checked numerically.
- The packet still needs review by the author and the principal investigator.

This remains an evidence extraction for A1 and does not make the novelty decision.
