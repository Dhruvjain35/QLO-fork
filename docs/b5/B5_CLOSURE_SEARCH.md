# B5 closure: targeted literature search

**Purpose.** The principal track lists three searches that "came up empty" and asks for them to be repeated before
submission (`principal/QLO_Principal_Track.md` §2):
- the exact zero probability of a finite-shot parameter-shift gradient;
- the conditional sign probability of a non-zero finite-shot gradient;
- a SWAP vs Loschmidt shot ratio for gradients.

The follow-up audit also recorded that "no systematic search … was performed" (`B5_FOLLOWUP_AUDIT.md` §18). This file
documents a targeted, reproducible search for those items and for the other candidate statements (C1–C5). It is a
targeted search, not a systematic review. A hit that is "not located" here is still only "not found by these
queries".

**Run date:** 2026-10-05.
**Script:** [`tools/b5_closure_search.py`](tools/b5_closure_search.py).
**Committed outputs:**
- [`results/b5_prior_work/closure_search_queries.json`](results/b5_prior_work/closure_search_queries.json) — queries and
  counts.
- [`results/b5_prior_work/closure_search_screen.csv`](results/b5_prior_work/closure_search_screen.csv) — 1,060 unique
  records, each with a decision and reason.

Raw API responses and abstracts stay in the git-ignored `research_sources/b5_closure/search/`.

## 1. Targets

| Target | Statement searched for | Candidate | Matrix rows |
|---|---|---|---|
| T1 | Exact law of a finite-shot parameter-shift gradient (difference of binomials, Skellam), P(ĝ = 0), ties | C1 | 9, 12, 19 |
| T2 | Sign statistics of finite-shot gradients, including the conditional law for non-zero estimates | C1, C2 | 10, 11, 13, 33 |
| T3 | Loschmidt/inversion/compute-uncompute vs SWAP-test fidelity estimation: variances, shot counts, comparisons | C3, C5 | 4, 14a, 14b, 31 |
| T4 | A measurement-dependent shot exponent; a shot ratio between readouts; an exponent rule | C3, C5 | 15–18, 32 |
| T5 | Vector alignment, random walks, matched-start trajectories under shot noise on barren plateaus | C4 | 8, 20–25 |

## 2. Sources and queries

| Source | What was run | Records |
|---|---|---|
| arXiv API (`export.arxiv.org`) | 17 field-restricted queries (T1a–T5b), e.g. `abs:"parameter shift" AND abs:shot`, `abs:Skellam AND cat:quant-ph`, `abs:"swap test" AND abs:"inversion test"`; then 10 supplemental queries (S1–S10) for C5/C2 terms, e.g. `abs:"destructive swap test" AND abs:variance`, `abs:"relative gradient" AND cat:quant-ph AND abs:shots` | 50 (first pass) + 9 (supplemental) |
| OpenAlex search (`api.openalex.org/works?search=`) | The same 17 targets as free-text queries, up to 50 results each | 817 |
| Semantic Scholar graph API | The same 17 free-text queries | 51 (2 of 17 queries answered; the other 15 returned no response under the API's rate limit, HTTP 429, and were not retried with a key) |
| OpenAlex forward citations (`filter=cites:`) | All works citing Thanasilp 2024 (A), Aghaei Saem 2026 (B), Teo 2023 (D), Mari 2021 (F) | 131 + 3 + 3 + 155 |
| Web search | 6 natural-language queries for the three principal-track targets and the readout comparison (listed in the JSON) | — |
| Direct lookups | arXiv `id_list` for the 35 shortlisted records and for the principal track's "Other papers" citations | — |

- **Deduplication:** 1,210 raw hits became 1,042 unique records after title normalisation. Supplemental and direct
  lookups bring the total to 1,060.
- Exact query strings and per-query counts are in `closure_search_queries.json`.

## 3. Screening

1. **Automatic flagging** (`P1`/`P2`/`P3`) from title and abstract keywords, combining:
   - parameter shift with shots and a distribution or sign term;
   - swap test with inversion/Loschmidt/compute-uncompute;
   - swap test with a ratio or exponent term and shots;
   - vector or random-walk terms with shots and barren plateaus.
2. **Manual title/abstract reading** of all P1/P2 records and of every record from the arXiv field queries, the
   forward-citation lists (titles filtered for shot, sampling, measurement, swap, gradient, sign, estimator, fidelity,
   echo, overlap, precision or noise) and the web searches.
3. **Full-text keyword search** of nine downloaded candidates: Skellam, binomial, difference of binomials, sign, swap
   test, inversion/compute-uncompute, Loschmidt, F(1−F), ratio, exponent, parameter shift.
4. **Full reading** of the three records that bear directly on the targets. They became ledger papers F, G and H.

## 4. Results

| Decision | Records |
|---|---|
| Included and read in full (ledger papers F, G, H) | 3 |
| Screened, related, not added to the matrix | 4 |
| Screened, context only (principal-track citations, framing) | 5 |
| Screened, not reviewed (relevant mainly to B4) | 1 |
| Screened and excluded after title/abstract or full-text search | 42 |
| Excluded at the automatic keyword screen | 1,005 |

**Included** (full audits: [`B5_MARI_AUDIT.md`](B5_MARI_AUDIT.md) and [`B5_CLOSURE_AUDIT.md`](B5_CLOSURE_AUDIT.md) §4):
- **F — Mari, Bromley, Killoran, PRA 103, 012405 (2021).**
  - Per-θ parameter-shift variance with shift-dependent single-shot variance (Eq. 45).
  - Both readouts named for one survival probability (p. 3).
  - FD/PS crossover at N ≈ 50.
  - Matched-start trajectories.
- **G — Miranskyy, arXiv:2510.22418 (2025).** Inverse-test vs swap-test detection shot counts for one fidelity, with
  ratio ln F / ln[(1 + F)/2] → 2 as F → 1.
- **H — Zhan et al., Light Sci. Appl. 14, 83 (2025).** Per-copy variances c(1 − c)/N (projection onto a known state)
  and (1 − c²)/N (SCM / ideal swap test) for one overlap, with an explicit comparison: swap-type estimators are less
  precise at small overlap. These statements are present in arXiv v1 (2024-06-10).

**Screened, related, not added** (exact locators so that A1 can follow up):
- **Sulimov & Lehmann, arXiv:2609.14424 (2026-09-13), *Certification cost of quantum models*.**
  - An "accounting identity": the fitted shot-cost exponent equals 2 + d log(nV)/d log n − d log(nG)/d log n, with V
    the readout variance and G the squared gradient norm (Eq. 2, p. 7; Fig. 4, pp. 6–7).
  - Structurally the same accounting as the principal track's exponent rule (shots ∝ variance / signal²).
  - Differences: Fisher-matrix certification, polynomial exponents in the register size, no readout comparison, no
    Loschmidt or SWAP test.
  - Related to matrix row 32. **A full read is recommended before the exponent rule is positioned.**
- **Ali, Scala, Lupo, Mandarino, arXiv:2603.18211 (2026).** SWAP-test-only fidelity-kernel estimation with variance
  (1 − k²)/S and Chebyshev shot bounds for symmetric spin models. One readout, kernel level.
- **Miranskyy, Campos, Mjeda, Zhang, García Rodríguez de Guzmán, arXiv:2507.17235 (2025).** Empirical shot counts of
  inverse vs swap tests for program testing (near F = 1); the empirical study behind paper G.
- **arXiv:2010.13186 (2020), *A Unified Framework for Quantum Supervised Learning*.** Swap vs inversion test accuracy on
  noisy hardware (qubit count, c-SWAP gates), not shot statistics.

**Context only:**
- Kaminishi, Mori, Sugawara, Yamamoto, arXiv:2406.09780. Now published as *Impact of measurement noise on escaping
  saddles in variational quantum algorithms*, Sci. Rep. (2026), doi:10.1038/s41598-026-40123-3.
- Kang, arXiv:2605.01319.
- Li, Thapa, Alpcan, Parampalli, arXiv:2607.11095.
- Arrasmith, Holmes, Cerezo, Coles, QST 7, 045015 (2022).

These are the principal track's "Other papers" entries; their metadata were verified (`B5_PRINCIPAL_LINE_CHECK.md`).

**Not reviewed:** Teo, *Robustness of optimized numerical estimation schemes for noisy variational quantum algorithms*,
PRA 109, 012620 (2024). The abstract shows it extends Teo 2023 to hardware noise (B4 territory).

## 5. Answers to the three principal-track searches

| Principal-track search | Result of this search |
|---|---|
| Exact zero probability of a finite-shot parameter-shift gradient | Not located in any screened or read record. Closest: the fidelity-level single-estimate factor (1 − s)^N inside a proof (Thanasilp A-06a); the all-accept probabilities F^N and ((1 + F)/2)^N for testing (Miranskyy G-03); the binomial law of one projection estimate (Zhan H-04). |
| Conditional sign probability of a non-zero finite-shot gradient | Not located. Closest: qualitative remarks that noisy gradients point the wrong way (Teo D-08a; Mari F-05). |
| SWAP vs Loschmidt shot ratio for gradients | Not located as a gradient-level statement. Implied (PARTIAL / IMPLIED) by per-shot statistics printed in four sources: Thanasilp (outcome models), Aghaei Saem (variances), Miranskyy (outcome models), Zhan (variances). Fidelity-level comparisons are explicit in Zhan (estimation precision) and Miranskyy (detection shots near F = 1). |

## 6. Limitations

- **No subscription databases** (Scopus, Web of Science, INSPEC) were used; the principal track recommends a library
  database before submission.
- **Semantic Scholar answered only 2 of 17 queries** (rate limit); its coverage is largely missing.
- **Shallow screening for most records:** title/abstract keyword screening, full reading only for F, G and H.
- **Forward citations one hop only,** from A, B, D and F. Backward references of F, G and H were not traced.
- **No full-text search** beyond the downloaded candidates.
- Records after 2026-10-05 are not covered.

This document records evidence for A1 and does not make the novelty decision.
