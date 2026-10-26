# B5 follow-up: version gaps (Aghaei Saem 2026; Teo 2023)

The initial B5 round reviewed Aghaei Saem et al. as arXiv:2507.22054v2 because the IOP version of record was not
retrievable (potential issue PI-1). This follow-up retried the published version **through legitimate routes only**:
- DOI landing page;
- publisher PDF link;
- Crossref, OpenAlex and Semantic Scholar metadata;
- arXiv metadata;
- the authors' institutional repository.

No bot check or access control was bypassed: no captcha was solved, no challenge was evaded, no browser automation was
used, and no credentials were entered. The same was done for Teo 2023, the other paper reviewed from arXiv.

## 1. Aghaei Saem et al., QST 11, 015049 (2026) — status: **resolved**

### 1.1 Routes tried

| Route | Date | Result |
|---|---|---|
| `https://doi.org/10.1088/2058-9565/ae2202` (DOI → iopscience.iop.org), initial B5 round | 2026-10-04 | Radware bot-manager captcha page; not bypassed |
| Same DOI URL, single plain request, follow-up | 2026-10-04 | **HTTP 200: the IOPscience article page with the open-access full text** (CC BY 4.0). No challenge was presented. The page embeds the publisher's bot-manager configuration script, but the content was served |
| `citation_pdf_url` from that page (`…/ae2202/pdf`), single plain request | 2026-10-04 | **HTTP 200: the version-of-record PDF**, 25 PDF pages (IOP cover page + 24 journal pages). The PDF carries a per-download stamp, so its sha256 (in the manifest) is download-specific |
| Crossref API (`api.crossref.org/works/10.1088/2058-9565/ae2202`) | 2026-10-04 | Dates (§1.2). The `am` and `vor` links both point to IOP URLs |
| OpenAlex | 2026-10-04 | OA status hybrid; locations: the DOI and the arXiv record only (no institutional-repository copy); `publication_date` 2025-11-20 (= the Crossref `created` date at acceptance, not the publication date) |
| Semantic Scholar | 2026-10-04 | `openAccessPdf` = the DOI URL (HYBRID, CC BY); `publicationDate` 2025-07-29 (= arXiv v1) |
| arXiv abstract page and API (`2507.22054`) | 2026-10-04 | v1 2025-07-29; v2 2026-06-04. Journal-ref "Quantum Science and Technology, Volume 11, 015049 (2026)"; DOI linked; comment "11+13 pages, 5 figures" |
| EPFL Infoscience search (authors' institution) | 2026-10-04 | The returned page contained captcha markup; not pursued (not needed once the version of record was obtained) |
| Wayback Machine (initial round) | 2026-10-04 | No snapshot of the PDF |

### 1.2 Dates

| Event | Date | Source |
|---|---|---|
| arXiv v1 posted | 2025-07-29 | arXiv |
| Received by QST | 2025-08-01 | Crossref assertion `date_received`; article page |
| Revised | 2025-10-23 | Article page and PDF title block |
| **Accepted** | **2025-11-20** | Crossref assertion `date_accepted`; article page; PDF ("Accepted for publication") |
| DOI registered (Crossref `created`) | 2025-11-20 | Crossref |
| **Published online** | **2026-01-30** | Crossref `published-online`, assertion `date_epub`; article page |
| Print issue | 2026-03-01 | Crossref `published-print` |
| Post-publication change | 2026-04-07 | Article page: Figure 2 had been replaced by a duplicate of Figure 3 during final file creation and was restored. The retrieved PDF shows the correct Figure 2 |
| **arXiv v2 posted** | **2026-06-04** | arXiv |

- **Order of versions.** v2 was posted **after** publication: 125 days after online publication, and after the
  2026-04-07 correction. v1 was posted 3 days before the journal received the manuscript.
- **Does v2 claim to match the published version?** No.
  - The arXiv record carries the journal-ref and DOI, but these fields identify the article. They do not state that v2
    is the published or accepted text.
  - The only comment is "11+13 pages, 5 figures".
  - The match was therefore checked directly (§1.3).

### 1.3 Text comparison: version of record vs arXiv v2 (and v1)

- **Method.**
  - Version-of-record full text taken from the article HTML (TeX math preserved; split into paragraphs) and from the PDF.
  - v1 and v2 taken from their LaTeX sources (math removed; appendices included).
  - Coverage measured with 5-word shingles, in both directions, overall and per paragraph (paragraphs ≥ 25 words).
- **Version of record vs v2.**
  - 95.6% of version-of-record shingles occur in v2, and 91.0% of v2 shingles occur in the version of record.
  - Of 125 version-of-record paragraphs, only 3 lack a v2 counterpart: the licence notice, the post-publication-change
    note and the data-availability statement.
  - Of 108 v2 paragraphs, only 3 lack a version-of-record counterpart: the author-affiliation blocks.
- **Version of record vs v1.** 78.5% coverage. The v1-absent passages V-01 to V-03 (ledger) are present in the version
  of record:
  - "Subtlety regarding the choice of POVM", §4, pp. 9–10;
  - "Subtlety regarding measure-first-estimate-later approaches", §4, pp. 8–9;
  - the global Pauli-Z parity POVM example, §2, p. 5.
- **Numbering.**
  - Identical in the version of record and v2: Eqs. (1)–(12), (A1)–(A23), (B1)–(B30), (C1)–(C11) and (D1)–(D13);
    Figs. 1–5; Theorems 1–2; Corollaries 1–4; Lemmas 1–2; Proposition 1; Definitions 1–4.
  - Sections use arabic numerals (1–5, App. A–D with A.1–A.3, D.1–D.2) instead of v2's roman numerals.
- **Pages.** Journal pages 1–24 (PDF page = journal page + 1).
- **Quotes.** The B-ledger quotes (B-10a, B-10c, B-14, B-17) occur verbatim in the version of record.
- **Not located, re-checked.** The B "not located" items (B-NL13, B-NL14b, B-NL17, B-NL30) were searched again in the
  version-of-record text. They remain not located. Searches: conditional, 4^n, 16^n, decades, Skellam, cosine, inner
  product, matched, same/identical initial.

### 1.4 Crosswalk: every B entry, arXiv v2 locator → version-of-record locator

| Entry | arXiv v2 locator (as in the ledger) | Version of record (QST 11, 015049) |
|---|---|---|
| B-01 | §II Framework, "Gradient-based and non-gradient based training"; Eqs. (1)–(4), (6); Fig. 2; (B17); pp. 3–4 | §2, same paragraph heading; Eqs. (1)–(4), (6); Fig. 2 (as restored); (B17); pp. 3–4, 17 |
| B-02 | §II "Polynomial POVMs in disguise"; p. 5 | §2, same heading; p. 5 |
| B-03 | §III Definition 1, Eq. (8); Fig. 1; pp. 5–7 | §3 Definition 1, Eq. (8), p. 6; Fig. 1, p. 2 |
| B-04 | Theorem 1 (§III), Theorem 2 (App. B), (B1)–(B13); pp. 7, 19–20 | Theorem 1, §3 p. 6; App. B pp. 14–16, Theorem 2 p. 15, (B1)–(B13) pp. 15–16 |
| B-05 | Corollary 1 (Eq. 9), Corollary 3; pp. 7, 20 | Corollary 1, Eq. (9), p. 7; Corollary 3, p. 16 |
| B-06a | Corollary 2 (Eq. 10), Corollary 4, (B14)–(B30); pp. 7, 20–23; Fig. 3 | Corollary 2, Eq. (10), p. 7; Corollary 4, p. 16; (B14)–(B30) pp. 16–18; Fig. 3, p. 7 |
| B-06b | (B18), (B19), (B26); pp. 22–23 | (B18), (B19) p. 17; (B26) p. 18 |
| B-06c | (10), (B15), (B26); pp. 7, 21–23 | pp. 7, 16, 18 |
| B-06d | (10), (B14)–(B15); Fig. 3; pp. 7, 21 | pp. 7, 16; Fig. 3, p. 7 |
| B-06e | (B15); p. 21 | p. 16 |
| B-07a | §III text after Corollary 2; Fig. 3 (a)–(c); App. C; pp. 6–7 | §3, p. 7; Fig. 3, p. 7; App. C pp. 19–20 |
| B-07b | Fig. 3 (b), (c), legend "Random Walk"; pp. 6–7 | Fig. 3 (b), (c), legend "Random Walk", p. 7 (checked on the page image) |
| B-07c | §III and §IV; Fig. 3 (a); Fig. 4; pp. 6–8 | pp. 7–9; Fig. 3, p. 7; Fig. 4, p. 9 |
| B-08a | §IV discussion of Fig. 4; (C1)–(C11); pp. 6, 8, 23–25 | §4, p. 8; Fig. 4, p. 9; (C1)–(C11) pp. 19–20 |
| B-08b | App. C (C1), (C8), (C9); pp. 23–25 | App. C, pp. 19–20; Figs. 3–4, pp. 7, 9 |
| B-08c | App. C; §IV POVM subtlety; (C1), (C8); pp. 9–10, 23–25 | pp. 9–10, 19–20 |
| B-09a | §IV "Subtlety regarding the choice of POVM"; Fig. 5; Theorem 2; p. 9 | §4 pp. 9–10; Fig. 5, p. 10; Theorem 2, p. 15 |
| B-09b | §IV; Fig. 5 (a); p. 9 | §4 pp. 9–10; Fig. 5 (a), p. 10 |
| B-10a | §IV; variances inline after Eq. (12); p. 10 | §4, p. 10 |
| B-10b | §IV; Eq. (12); pp. 9–10 | Eq. (12), p. 10 |
| B-10c | §IV; Eq. (12) + inline variances; pp. 9–10 | p. 10 |
| B-11 | §IV purity example and open question; p. 10 | §4, p. 10 |
| B-12 | §IV "Subtlety regarding measure-first-estimate-later approaches"; Eq. (11); pp. 8–9 | §4, pp. 8–9; Eq. (11), p. 9 |
| B-13 | §II examples, §IV guidelines, §V; (6), (7); Fig. 4; App. C; pp. 4–5, 8, 10 | §2 pp. 3–5 ((6) p. 4, (7) p. 5); §4 p. 8; §5 pp. 10–11; Fig. 4, p. 9; App. C pp. 19–20 |
| B-14 | §I final paragraph; p. 2 | §1, p. 2 |
| B-15 | §V; App. D (D1)–(D13); pp. 10–11, 25–27 | §5 pp. 10–11; App. D pp. 20–22 |
| B-16 | App. A, Lemmas 1–2, Proposition 1, Definitions 2–4, (A1)–(A23); pp. 15–18 | App. A: Lemma 1 p. 12, Proposition 1 p. 13, Definitions 3–4 p. 14; (A1)–(A23) pp. 12–14 |
| B-17 | App. C (C11); Fig. 4 (d); p. 25 | p. 20; Fig. 4, p. 9 |
| B-NL13, B-NL14b, B-NL17, B-NL30 | Whole paper, pp. 1–27 | Re-searched in the version of record (pp. 1–24): still not located |

### 1.5 Consequence

- PI-1 (`B5_POTENTIAL_ISSUES.md`) is resolved. The Loschmidt/SWAP statements that STAGE7.md §3, §19 and §22 attribute
  to the QST article are in the version of record: §4, pp. 9–10, Fig. 5, Eq. (12), and both variances on p. 10.
- When citing, use the version-of-record section numbers (arabic) and pages. Equation and figure numbers carry over
  unchanged.
- The B ledger entries keep their arXiv v2 locators, which the crosswalk maps one to one.

## 2. Arrasmith 2021 and Gentinetta 2024 — status: no gap

Both Quantum PDFs are the arXiv v2 files themselves:
- **Arrasmith 2021:** margin stamp "arXiv:2011.12245v2 … 30 Sep 2021"; comment "Updated to final publication version".
- **Gentinetta 2024:** margin stamp "arXiv:2203.00031v2 … 7 Jan 2024"; comment "v2: published version".

Quantum publishes the arXiv version, so the reviewed text is the version of record.

## 3. Teo 2023, Phys. Rev. A 107, 042421 — status: **not resolved**

| Route | Date | Result |
|---|---|---|
| `https://doi.org/10.1103/PhysRevA.107.042421` → `link.aps.org` | 2026-10-04, retried once in the follow-up | HTTP 403 challenge page; not bypassed |
| `journals.aps.org` abstract and PDF URLs | 2026-10-04 | HTTP 403 challenge page |
| Crossref | 2026-10-04 | Published 2023-04-17; licence `aps-default-license` (version of record, not open access); no received/accepted assertions |
| OpenAlex | 2026-10-04 | Published version listed as not open access; open copy = arXiv (`submittedVersion`) |
| Semantic Scholar | 2026-10-04 | `openAccessPdf` = arXiv (GREEN) |
| arXiv | 2026-10-04 | v1 2022-06-25, v2 2022-06-28, v3 2022-11-20; journal-ref PRA 107, 042421 (2023) |

- **Order of versions.** v3 predates publication by 148 days. Whether further changes were made after 2022-11-20
  (proofs, referee rounds) is unknown.
- **Claim of equivalence.** The arXiv comment describes the changes from v2 but does not claim v3 is the published text.
- **Consequence.**
  - Every Teo locator in this audit is an arXiv v3 locator, and published equation and page numbers are unverified.
  - The arithmetic observation on Eq. (23) (B5_TEO_DEEP_AUDIT.md §6) also refers to v3.
  - Before Teo is cited with equation numbers, the PRA version should be checked through legitimate access (for
    example an institutional subscription).

## 4. Closure-audit sources

| Paper | Version reviewed | Version of record | Status |
|---|---|---|---|
| Mari, Bromley, Killoran, PRA 103, 012405 (2021) | arXiv:2008.06517v2 (2021-02-26), read in full | APS: DOI → link.aps.org returned HTTP 403 (2026-10-05), not bypassed; not open access. The open-access copy in the University of Camerino repository (IRIS, hdl:11581/475358, labelled post-print) is byte-identical to arXiv v2 (same sha256). | **Not resolved** for the APS version; locators are arXiv v2. v1 vs v2: same statistical-estimation section (Eqs. 43–50) |
| Miranskyy, arXiv:2510.22418 (2025) | v1 (2025-10-25), the only version | None (arXiv record has no journal reference) | Preprint only |
| Zhan et al., Light Sci. Appl. 14, 83 (2025) | Published PDF and published SI (MOESM1), via the DOI landing page (open access, CC BY 4.0) | Same | **Resolved**: the version of record was reviewed. Dates: received 2024-04-16, accepted 2025-01-10, published 2025-02-12. arXiv v1 (2024-06-10) already contains the cited statements |

This document records version provenance for A1 and does not make the novelty decision.
