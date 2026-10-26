# B5 follow-up sources

Works cited **by the two reviewed papers** that may bear on the Stage 7 candidates. None of these was reviewed in
B5. The citations are copied as printed in the citing source and their contents have **not** been checked. This list
is **not exhaustive** and is not a literature search. Choosing which, if any, to read belongs to the principal audit
(A1).

Citing-source keys:
- **A** = Thanasilp et al., Nat. Commun. 15, 5200 (2024). "ref." = main-text reference list; "SI ref." =
  Supplementary Information reference list.
- **B** = Aghaei Saem et al., arXiv:2507.22054v2, cited as "[n]".

Candidates:
- C1 exact zero/sign probabilities;
- C2 conditional Loschmidt sign law;
- C3 readout-dependent gradient shot exponent;
- C4 vector/trajectory consequences;
- F-x the "already prior" facts.

**Follow-up status (2026-10-04).** H1 (Arrasmith 2021), H2 (Teo 2023, reviewed as arXiv v3) and H3 (Gentinetta
2024, published Quantum version) were reviewed in full in the targeted follow-up audit:
[`B5_FOLLOWUP_AUDIT.md`](B5_FOLLOWUP_AUDIT.md), ledger entries C-xx, D-xx and E-xx. The MEDIUM and BACKGROUND items
remain unreviewed.

## HIGH priority — could directly contain one of the candidate results

| # | Citation (as printed in the citing source) | Cited by / where | Why it may matter | Candidates |
|---|---|---|---|---|
| H1 | A. Arrasmith, M. Cerezo, P. Czarnik, L. Cincio, P. J. Coles, *Effect of barren plateaus on gradient-free optimization*, Quantum 5, 558 (2021). | B [38], §I p. 2 (named as having mentioned random-walk behaviour "in passing"); B §I p. 1 (exponential resources to resolve flat regions); A ref. 31. | Shot cost of resolving loss differences on barren plateaus, and random-walk remarks. Gradient-free methods rely on finite-shot loss differences. | C3, C4, F-G |
| H2 | Y. S. Teo, *Optimized numerical gradient and hessian estimation for variational quantum algorithms*, Physical Review A 107, 10.1103/physreva.107.042421 (2023). | B [87]; B App. C Eq. (C11) (rescaled parameter-shift factor λ = dN/(2d² + Nd − 2)). | A finite-shot parameter-shift gradient estimator whose scaling factor minimises mean-squared error, so it contains finite-shot gradient-estimator statistics. Whether it treats different readouts or zero/sign events is unknown. | C1, C3 |
| H3 | G. Gentinetta, A. Thomsen, D. Sutter, S. Woerner, *The complexity of quantum support vector machines*, arXiv:2203.00031 (2022). | A ref. 16 and SI ref. [10]; A p. 2 ("rigorous study of the number of measurement shots required to successfully train the fidelity kernel"); A SI Note I.D. | Shot-complexity analysis of fidelity-kernel estimation. It may treat estimator variance for specific fidelity measurements. | C3 |

### Added by the follow-up audit (cited by the follow-up sources; not reviewed)

| # | Citation (as printed in the citing source) | Cited by / where | Why it may matter | Candidates |
|---|---|---|---|---|
| H4 | A. Mari, T. R. Bromley, and N. Killoran, *Estimating the gradient and higher-order derivatives on quantum hardware*, Phys. Rev. A 103, 012405 (2021). | Teo 2023 (D) ref. [61]: origin of the scaled parameter-shift estimator. Teo says [61]'s expressions are not circuit-averaged (p. 1) and are large-N forms (pp. 6–7). Not cited by A, B, C or E. | **Reviewed in the closure audit** (paper F, arXiv v2; B5_MARI_AUDIT.md): per-θ finite-shot PS/FD/SPS MSEs, Eq. (45). | C1, C3, C5 |

### Added by the closure audit (targeted search; B5_CLOSURE_SEARCH.md)

| # | Citation | Found by | Status | Candidates |
|---|---|---|---|---|
| H5 | A. Miranskyy, *The Cost of Certainty: Shot Budgets in Quantum Program Testing*, arXiv:2510.22418 (2025). | Principal-track "Other papers" table; arXiv search | **Reviewed** (paper G) | C3, C5 |
| H6 | H. Zhan et al., *Experimental benchmarking of quantum state overlap estimation strategies with photonic systems*, Light Sci. Appl. 14, 83 (2025). | Search (OpenAlex/arXiv, swap test + variance) | **Reviewed** (paper H) | C3, C5 |
| H7 | P. Sulimov, C. Lehmann, *Certification cost of quantum models: measurement correlation, not parameter count*, arXiv:2609.14424 (2026). | Search (arXiv, parameter shift + shots) | Screened only; accounting identity for shot-cost exponents (Eq. 2, p. 7); full read recommended | C5 (exponent rule) |
| M7 | Y. S. Teo, *Robustness of optimized numerical estimation schemes for noisy variational quantum algorithms*, Phys. Rev. A 109, 012620 (2024). | Forward citations of D | Not reviewed (noise; B4 territory) | C3 |

## MEDIUM priority — relevant to measurement-dependent finite-shot gradients / estimates

| # | Citation (as printed) | Cited by / where | Why it may matter | Candidates |
|---|---|---|---|---|
| M1 | M. Cerezo, P. J. Coles, *Higher order derivatives of quantum neural networks with barren plateaus*, Quantum Science and Technology 6, 035006 (2021). | B [101] (§V; cited with B [29], [38] as "standard methods"). | Finite-shot resolvability of derivatives on barren plateaus. | C3, C4 |
| M2 | S. Wang, P. Czarnik, A. Arrasmith, M. Cerezo, L. Cincio, P. J. Coles, *Can error mitigation improve trainability of noisy variational quantum algorithms?*, Quantum 8, 1287 (2024). | A SI ref. [18] (source of A's Supplemental Theorem 1); A ref. 32. | Resolvability / shot cost under mitigation; A quotes it for "can impair resolvability". | F-E, F-H |
| M3 | H.-Y. Huang, M. Broughton, J. Cotler, S. Chen, J. Li, M. Mohseni, H. Neven, R. Babbush, R. Kueng, J. Preskill, J. R. McClean, *Quantum advantage in learning from experiments*, Science 376, 1182 (2022). | B [100] (§IV purity example: two-copy SWAP measurement advantage). | Multi-copy/entangled POVMs changing estimation cost: the "different POVM" question B leaves open. | C3, F-D |
| M4 | M. S. Rudolph, S. Lerch, S. Thanasilp, O. Kiss, O. Shaya, S. Vallecorsa, M. Grossi, Z. Holmes, *Trainability barriers and opportunities in quantum generative modeling*, npj Quantum Information 10, 116 (2024). | B [79] (§V: only polynomially many bitstrings receive non-zero estimates). | Count-starvation-type effects (unsampled outcomes estimated as zero), related in mechanism to Loschmidt zero estimates. | C1 |
| M5 | Y. Liu, S. Arunachalam, K. Temme, *A rigorous and robust quantum speed-up in supervised machine learning*, Nat. Phys. 17, 1013–1017 (2021). | A ref. 8 and SI ref. [9]; A p. 2, SI Note I.D. | Shot-noise robustness of fidelity-kernel estimation without concentration. | C3 (contrast case) |
| M6 | W. Xiong et al., *On fundamental aspects of quantum extreme learning machines*, arXiv:2312.15124 (2023); W. Xiong et al., *Role of scrambling and noise in temporal information processing with quantum systems*, arXiv:2505.10080 (2025). | B [34], [35]. | Finite-shot concentration in reservoir / extreme-learning models (outcome-level analyses by overlapping authors). | F-A, F-F |

## BACKGROUND — general barren-plateau / concentration context

| # | Citation (as printed) | Cited by | Use |
|---|---|---|---|
| G1 | M. Cerezo, A. Sone, T. Volkoff, L. Cincio, P. J. Coles, *Cost function dependent barren plateaus in shallow parametrized quantum circuits*, Nature Communications 12, 1 (2021). | B [41]; A ref. 21; A SI ref. [31] | Source of the Stage 3 global/local benchmark. |
| G2 | A. Arrasmith, Z. Holmes, M. Cerezo, P. J. Coles, *Equivalence of quantum barren plateaus to cost concentration and narrow gorges*, Quantum Science and Technology 7, 045015 (2022). | B [37]; A ref. 65 | Positioning against cost concentration / narrow gorges (A4). |
| G3 | M. Larocca, S. Thanasilp, S. Wang, K. Sharma, J. Biamonte, P. J. Coles, L. Cincio, J. R. McClean, Z. Holmes, M. Cerezo, *A review of barren plateaus in variational quantum computing*, Nature Reviews Physics 3, 625–644 (2025) [volume/pages as printed in B]. | B [28] | Review. |
| G4 | J. R. McClean, S. Boixo, V. N. Smelyanskiy, R. Babbush, H. Neven, *Barren plateaus in quantum neural network training landscapes*, Nature Communications 9, 1 (2018). | B [29]; A ref. 20 | Background. |
| G5 | S. Wang et al., *Noise-induced barren plateaus in variational quantum algorithms*, Nat. Commun. 12, 1 (2021). | A ref. 28; A SI ref. [16] | Background (noise; B4 is Satyabrat's). |
| G6 | J. Stokes, J. Izaac, N. Killoran, G. Carleo, *Quantum natural gradient*, Quantum 4, 269 (2020). | B [72] | Method examined by B. |
| G7 | H.-Y. Huang, R. Kueng, J. Preskill, *Predicting many properties of a quantum system from very few measurements*, Nature Physics 16, 1050 (2020). | A SI ref. [12]; B [98] | Classical shadows (B §IV measure-first discussion). |
| G8 | H.-Y. Huang et al., *Power of data in quantum machine learning*, Nature Communications 12, 1 (2021); J. Kübler, S. Buchholz, B. Schölkopf, *The inductive bias of quantum kernels*, NeurIPS 34, 12661 (2021). | A SI refs. [1], [3] | Earliest fidelity-kernel concentration observations (A SI Note I). |

Not included: works cited only for methods unrelated to finite-shot readout statistics (generic VQA/QML reviews,
architecture or initialisation proposals, reservoir computing beyond M6, symmetry-based ansätze).

This list feeds the principal novelty audit. It does not make the novelty decision.
