# B5 closure: line check of the principal-track prior-work pointers

**Source checked.** `principal/QLO_Principal_Track.md` on the canonical repository, `upstream/main` at merge commit
8003375 (Satyabrat2005/QLO---Quantum-Langevin-Optimisation).

**Why.** The principal track says its pointers into Thanasilp et al. and Aghaei Saem et al. were read through a
summarising fetch of the arXiv HTML. It describes them as "a map, not a citation" and asks for each to be confirmed
against the PDFs, adding that this is what B5 is for (preamble "Two things to know before reading", item 2; §6,
item 3). Its §6 also asks B5 to carry Aghaei
Saem et al. §IV and Fig. 5, and Thanasilp et al. Propositions 1 and 2, as required rows.

**Scope.**
- This file checks prior-work pointers, quotations and factual statements about sources against the PDFs.
- It does not evaluate the principal track's candidate classifications, framing, A2 derivations or numerics, and it
  does not re-derive A1 or A2.
- Locators refer to the versions reviewed in B5:
  - Thanasilp: published Nat. Commun. article and SI.
  - Aghaei Saem: version of record (QST 11, 015049), with arXiv v2 locators in the ledger (`B5_VERSION_GAP.md` §1.4).
  - Teo: arXiv v3.
  - Mari: arXiv v2.
  - Miranskyy: arXiv v1.
  - Zhan: published version and SI.

**Result labels:**
- `CONFIRMED` — the pointer and statement match the source.
- `CONFIRMED, LOCATOR UPDATED` — the content matches; the locator should be given in the version-of-record form.
- `PARTLY CONFIRMED` — part of the statement matches; the rest needs a qualifier, which is given.
- `NOT CHECKED` — outside B5's scope or not a prior-work statement.
- `CONSISTENT` — a negative search claim that B5's own documented search agrees with (B5 cannot confirm absence).

## 1. Thanasilp et al. 2024 (principal track §2)

| # | Principal-track pointer or statement | B5 evidence | Result |
|---|---|---|---|
| L1 | "Section II.2" sets up the Loschmidt Echo test (+1 for the all-zero bitstring) and the SWAP test (±1, p₊ = 1/2 + κ/2) | The published article has unnumbered sections. Both tests are introduced in Results, "Why exponential concentration is problematic", p. 4 (A-05, A-08); the outcome models are SI Eqs. (17) and (46). The arXiv numbering was not checked. | CONFIRMED, LOCATOR UPDATED |
| L2 | Proposition 1 (around Eq. 13): polynomial shots and a concentrated kernel make the Loschmidt Gram matrix the identity with probability 1 − O(c^(−n)) | Proposition 1, Eq. (13), p. 4: Pr[K̂ = 𝟙] ≥ 1 − δ′ with δ′ ∈ O(c^(−n)); formal version SI Supp. Prop. 2, SI pp. 7–8 (A-05, A-06a). The proposition assumes concentration towards an exponentially small value (p. 4). | CONFIRMED, with the qualifier |
| L3 | Mechanism stated in the text: (1 − μ)^N ≈ 1 − Nμ | p. 4 (A-05) | CONFIRMED |
| L4 | Proposition 2 (Eq. 14): the SWAP Gram matrix is statistically indistinguishable from one built from fair ±1 coin flips | Proposition 2, Eq. (14), p. 4; SI Eqs. (46)–(54), SI pp. 9–13 (A-08). Indistinguishability is defined at success probability ≤ 0.51 (SI Def. 2) and holds with probability ≥ 1 − δ_κ over input pairs; concentration towards an exponentially small value is assumed. | CONFIRMED, with the qualifiers |
| L5 | Scope: kernel values; no parameter-shift gradients | No gradient estimator in the article or SI (A-NL07, A-NL29) | CONFIRMED |
| L6 | "no exact zero probability theorem" | No gradient-level zero-probability result (row 9: A-06b is related only). The **exact** fidelity-level conditional zero probability (1 − s)^N appears inside the proof of SI Supp. Prop. 2 (SI Eqs. 26–27; A-06a, EXPLICIT for row 2). | PARTLY CONFIRMED: true at the gradient level; an exact fidelity-level factor is in the SI |
| L7 | "no sign probabilities" | A-NL10, A-NL11, A-NL13, A-NL33 | CONFIRMED |
| L8 | "no comparison of shot counts between the two tests" | No ratio and no fitted exponents (A-NL17). But SI Note III A 3 and SI Supplementary Fig. 4 report, on the same product-R_y kernels (n = 5–40), the shots each test needs: Loschmidt "N ∈ Ω(2ⁿ)" for a fixed non-zero fraction, SWAP "at least exponentially" (A-10a, A-10b; SI pp. 13–14). Main-text Fig. 3 compares training with the two tests' estimates at N = 1000 shots on a 40-qubit example (Fig. 2 is a schematic) (A-09a). | PARTLY CONFIRMED: no stated ratio, but a numerical same-kernel shot study of both tests exists in the SI |

## 2. Aghaei Saem et al. 2026 (principal track §2)

| # | Principal-track pointer or statement | B5 evidence | Result |
|---|---|---|---|
| L9 | "Section IV" ("Subtlety regarding the choice of POVM", Fig. 5): Loschmidt POVM concentrates to (0, 1), SWAP POVM to (1/2, 1/2) | Version of record: §4 (arabic numbering), pp. 9–10, Fig. 5 on p. 10; arXiv v2 §IV p. 9 (B-09a) | CONFIRMED, LOCATOR UPDATED (use "§4" and the version-of-record pages) |
| L10 | Same section states the per-shot variances Var^SWAP = 1 − F² and Var^LE = F(1 − F), with the remark that the different forms give different statistical behaviour | Version of record p. 10; arXiv v2 p. 10 (B-10a; quote verified in both) | CONFIRMED. For completeness: the same pair of per-copy variances (projection onto a known state, c(1 − c)/N; SWAP-type, (1 − c²)/N) is printed in Zhan et al., Light Sci. Appl. 14, 83 (published 2025-02-12; arXiv v1 2024-06-10), earlier than this paper's version of record (H-01, H-02; PI-6) |
| L11 | "they do not turn this into a shot ratio, and do not apply it to gradients" | Full text of arXiv v1, v2 and the version of record: no shot ratio, no gradient-level variance, no exponent (B-NL14b, B-NL17, B-NL30; B-10c and B-18 record the implication) | CONFIRMED (no longer limited to "as far as the fetch shows") |
| L12 | Eq. 12: resolution ratio ε_N = Var_ρ[ℓ̂]/(N Var_α[ℓ]), requiring ε_N ≲ 1 and hence exponential N | Eq. (12), version of record p. 10; arXiv v2 pp. 9–10 (B-10b). The source calls it a rule-of-thumb diagnostic. | CONFIRMED |
| L13 | Eq. 6 and Corollary 2: parameter-shift updates under concentrated outcome probabilities are indistinguishable from parameter-independent random variables, so the trajectory is a random walk | Eq. (6), §2, version of record p. 4 (B-01); Corollary 2, Eq. (10), p. 7; Corollary 4, p. 16 (B-06a). Stated for Pauli observables (two-outcome POVMs), random initialisation, polynomial shots and iterations, with probability ≥ 1 − c, c ∈ O(exp(−n)) (PI-3). | CONFIRMED, with the qualifiers |
| L14 | Fig. 3: 15 qubits, one layer of single-qubit X rotations, global Z cost (the Stage 6 parity benchmark circuit); 150-shot trajectories look like a random walk (PCA plot, displacement mean and variance) | Version of record Fig. 3, p. 7; legend "Random Walk" checked on the page image (B-07a, B-07b) | CONFIRMED |
| L15 | C4 determination: random-walk trajectories "on the same RX circuit with global Z" | Same circuit family as Stages 3–7 (single R_X layer), but the cost is the global-Z parity of Stage 6, not the Stage 7 fidelity (B-07a, B-08b; matrix row 28). The principal track's §2 already states this for Fig. 3. | CONFIRMED (same circuit family; different cost from Stage 7) |
| L16 | A4 draft: Aghaei Saem et al. give "the per shot variances F(1−F) and 1−F²" and show that finite-shot parameter-shift training "then resembles a random walk" | B-10a; B-06a, B-07a. The random-walk results are proven for Pauli observables (±1 outcomes); the Loschmidt POVM's fixed distribution (0, 1) is not the case written in Eq. (B15) (B5_MATH_COMPARISON §6.7). | CONFIRMED, with the observable qualifier |

## 3. Statements about the A2 ingredients (principal track §3)

| # | Principal-track statement | B5 evidence | Result |
|---|---|---|---|
| L17 | Result 1 proof: "Two independent binomials; the per shot variances are those of Aghaei Saem et al. Section IV, applied at the two shifts" | B-10a (variances). Additional printed sources of the ingredients: the general per-θ parameter-shift variance with shift-dependent single-shot variance, [σ₀²(θ + s) + σ₀²(θ − s)]/(4N sin² s), in Mari et al. 2021 Eq. (45), p. 7 (F-01, F-02); both per-copy variances in Zhan et al. 2025 (H-01); both outcome models in Thanasilp et al. (A-19) and Miranskyy 2025 (G-02). | CONFIRMED. The citation could include Mari Eq. (45) and Zhan et al. for the ingredients (B5 records sources; it takes no position on citation choice) |
| L18 | C5 is "not stated in either paper" | Not stated in A or B (A-19 and B-18 are PARTIAL / IMPLIED). Also not stated in C–H: D-11 related but different; F-02 related but different; G-02 and H-03 PARTIAL / IMPLIED; C-NL31, E-NL31, F-NL27 not located. | CONFIRMED for A and B; extended to C–H |
| L19 | C2: neither paper has the conditional sign law, and searches found nothing | Not located in A–H for either the product form (row 13) or the general form (row 33). Targeted search: [`B5_CLOSURE_SEARCH.md`](B5_CLOSURE_SEARCH.md) §5. | CONSISTENT (B5 search scope and limits are documented) |
| L20 | C3: a referee can derive 4ⁿ against 16ⁿ from Aghaei Saem §IV "in two lines" | B5 records the steps from B's variances to the product-landscape bases: per-θ variances, the parameter-shift difference with independent batches, the shift identities, a per-θ criterion, and the log-typical A (B5_MATH_COMPARISON §6.3, §8.2; B-10c). | NOT CHECKED (a judgment about effort; B5 lists the steps and takes no position) |
| L21 | "The Cost of Certainty" (arXiv:2510.22418): the inverse test is the most sample-efficient and the SWAP test costs about a factor of two more, in the near-identity regime of program testing | Read in full (paper G). Abstract p. 1; ratio ln F / ln[(1 + F)/2] → 2 − (F − 1)/2 + … ≈ 2 as F → 1 (p. 9); Examples 3.3–3.4 at F = 0.999 and 0.99 (G-01). The statistic is a quantum-Chernoff-bound **detection** shot count at error probability P_e for pure states, not an estimator variance. Single author, preprint (no journal reference). | CONFIRMED, with the statistic named |
| L22 | With both shifted fidelities equal to F, the identity gives a ratio (1 + F)/F: 2 at F = 1, growing like 1/F as F → 0 | The (1 + F)/F expression is the principal track's own algebra; paper G does not state it. *(Our algebra:)* G's detection ratio and (1 + F)/F coincide at F → 1 but differ elsewhere, e.g. 2.41 vs 3 at F = 0.5 and 3.85 vs 11 at F = 0.1 (B5_MATH_COMPARISON §9). | NOT CHECKED (principal-track algebra); difference in statistics recorded |

## 4. "Other papers found during the search" (principal track §2 table)

| # | Entry | B5 check | Result |
|---|---|---|---|
| L23 | Kaminishi et al., arXiv:2406.09780 (2024) | Authors Kaminishi, Mori, Sugawara, Yamamoto (arXiv v1); the arXiv abstract supports the η/N_s scaling and shorter escape times with more noise. A published version with the same title appears to be *Impact of measurement noise on escaping saddles in variational quantum algorithms*, Sci. Rep. (2026), doi:10.1038/s41598-026-40123-3 (matched on title and DOI in OpenAlex; author list not in that record; not read in B5). | CONFIRMED (metadata; abstract level) |
| L24 | Arrasmith et al., QST 7, 045015 (2022), arXiv:2104.05868 | Crossref: QST 7, 045015, published 2022-08-09; authors Arrasmith, Holmes, Cerezo, Coles. Not read in B5. | CONFIRMED (metadata) |
| L25 | *The Cost of Certainty*, arXiv:2510.22418 ("Read before citing") | Read in full (paper G; L21). | CONFIRMED; reading done |
| L26 | Kang, arXiv:2605.01319 (2026): sign organisation of gradient terms, not finite-shot estimators | Abstract: a term-resolved decomposition of the exact gradient's second moment into activity, sign organisation and coupling; no finite-shot estimator (screened). | CONFIRMED (abstract level) |
| L27 | Li et al., arXiv:2607.11095 (2026): measurement cost of gradient-based attacks on quantum classifiers | Abstract: shot budgets for attacks scaling as d^(5/2) and d³ in the input dimension; no readout comparison (screened). Authors Li, Thapa, Alpcan, Parampalli. | CONFIRMED (abstract level) |
| L28 | "Searches that came up empty (worth repeating with a library database before submission)" | Repeated with arXiv, OpenAlex, partial Semantic Scholar, forward citations and web searches ([`B5_CLOSURE_SEARCH.md`](B5_CLOSURE_SEARCH.md)); none of the three statements was located. No library database (Scopus, Web of Science, INSPEC) was used. | PARTLY CONFIRMED: the open-database searches also came up empty; the library-database search is still open |

## 5. A4 draft citations (principal track §5)

| # | Statement | B5 check | Result |
|---|---|---|---|
| L29 | "concentration forces an exponential number of measurement shots to resolve the cost or its gradient [Cerezo et al. 2021; Wang et al. 2021; Larocca et al. 2025]" | These three works were not read in B5. They appear to correspond to B5_FOLLOWUP_SOURCES G1 (Cerezo et al., Nat. Commun. 2021), G5 (Wang et al., noise-induced barren plateaus, Nat. Commun. 2021) and G3 (Larocca et al., review); the mapping is inferred from author and year. Reviewed B5 sources stating the exponential shot burden: Arrasmith 2021 (C-03, C-04a), Teo 2023 (D-07a), Thanasilp 2024 (A-12a, A-13), Aghaei Saem 2026 (B-04, B-10b). | NOT CHECKED (cited works not reviewed); reviewed alternatives listed |
| L30 | Thanasilp et al.: Loschmidt estimates collapse to zero, SWAP estimates become indistinguishable from fair coin flips | A-05, A-06a, A-08 | CONFIRMED |

## 5b. Additional item (principal track §2, C1 determination)

| # | Principal-track statement | B5 evidence | Result |
|---|---|---|---|
| L31 | C1 determination: the exact zero and sign probabilities of the parameter-shift estimator are not written down for gradients in either paper | Not located at the gradient level in A or B (A-06b and B-09b are fidelity-level and related only; A-NL10, A-NL11, A-NL12; B-06b, B-06c are related only); also not located in C–H (C-NL09, D-NL09, E-NL09, F-NL09, G-NL01, H-NL01; closest related items F-04, G-03, H-04). | CONFIRMED |

## 6. Required rows (principal track §6, "B5" item)

Aghaei Saem §IV and Fig. 5, and Thanasilp Propositions 1 and 2, are carried as required rows through the crosswalk in
[`B5_PRIOR_WORK_MATRIX.md`](B5_PRIOR_WORK_MATRIX.md) ("Principal-track required rows"): matrix rows 2, 3, 4, 9, 14a,
15, 16, 18, 31 and 32, with entries A-05, A-06a, A-06b, A-08, A-09a, B-09a, B-09b, B-10a, B-10b, B-10c, B-11 and B-18.

## 6b. Internal consistency note (outside the prior-work scope)

The principal track states the exponent rule as b_SW = b_LE + b_S in §3 (and its §3 table's "predicted b_SW" column is
b_LE + b_S), but its §6 B1 acceptance check writes "b_SWAP = b_LE − b_S" (upstream/main 8003375, line 250). The two
signs disagree; the §3 form is the one derived there. B5 only records the discrepancy.

## 7. Summary

- **Of 31 items:**
  - 24 are confirmed: L1–L5, L7, L9–L18, L21, L23–L27, L30, L31. Of these, L1 and L9 need the version-of-record
    locator, L2, L4, L13, L16 and L21 need the stated qualifier or the statistic named, and L23, L24, L26 and L27 are
    confirmed at metadata or abstract level only.
  - 3 are partly confirmed: L6, L8, L28.
  - 3 are not checked, as judgments, principal-track algebra or works B5 did not read: L20, L22, L29.
  - 1 is consistent with B5's documented search: L19.
- **Substantive factual additions for A1:**
  - Thanasilp's SI does contain a numerical same-kernel shot study of both tests (L8).
  - The two per-copy variances appear in Zhan et al. 2025, earlier than Aghaei Saem's version of record (L10, L17).
  - Mari et al. 2021 print the general per-θ parameter-shift variance used in the A2 proof (L17).
  - "The Cost of Certainty" factor of two is a near-F = 1 detection statistic (L21–L22).
  - The principal track's §6 B1 check states the exponent rule with the opposite sign to §3 (§6b).

This document records evidence for A1 and does not make the novelty decision.
