# B5 closure: audit of Mari, Bromley, Killoran 2021

**Source.** A. Mari, T. R. Bromley, N. Killoran, *Estimating the gradient and higher-order derivatives on quantum
hardware*, Phys. Rev. A **103**, 012405 (2021), doi:10.1103/PhysRevA.103.012405.

**Version reviewed.** arXiv:2008.06517**v2** (2021-02-26, 17 pp., journal-ref PRA 103, 012405), read in full,
including Appendix A; the LaTeX source was searched.
- The open-access copy in the University of Camerino institutional repository (IRIS, hdl:11581/475358, labelled
  "post-print") is **byte-identical** to arXiv v2 (same sha256).
- The APS version of record returned an HTTP 403 challenge page (not bypassed) and is not open access, so its page and
  equation numbers are **unverified**. Every locator below is an arXiv v2 locator.
- v1 (2020-08-14) was compared on the statistical-estimation section: Eqs. (43)–(50) are identical, including the
  Eq. (49) denominator noted in §6. The v2 arXiv comment reports an updated Fubini–Study metric definition and a
  corrected typo in the resulting equations.

**Why it was read.** It is Teo 2023's ref. [61], the origin of the scaled parameter-shift (SPS) estimator. Teo
describes its expressions as large-N forms that are not averaged over circuits (Teo pp. 1, 6–7). It was the
highest-priority remaining hole of the follow-up audit (`B5_FOLLOWUP_AUDIT.md` §18).

Evidence ids F-01 … F-NL27 refer to [`B5_EVIDENCE_LEDGER.md`](B5_EVIDENCE_LEDGER.md). Statements marked
*(our algebra)* are derived in this audit.

## 1. What the paper does

| Part | Content | Locator |
|---|---|---|
| Setting | f(θ) = ⟨0\|U(θ)†MU(θ)\|0⟩ with rotation-like gates U_j(θ_j) = exp(−iθ_jH_j/2), H_j² = 𝟙 | §II, Eqs. (1)–(4), p. 2 |
| Exact shift rules | Gradient for any shift s, Eq. (9); Hessian (10)–(13); Fubini–Study metric via the survival probability (14)–(18); arbitrary order (19)–(24) | §III, pp. 2–5 |
| Statistical model | f̂ = f + ε̂, zero-mean noise of variance σ₀²/N; σ₀² is the single-shot variance | §IV, Eq. (25), p. 5 |
| Figure of merit | MSE Δ = E[(ĝ − g)²] over measurement outcomes at a fixed parameter point; Δ = Var + Bias² | §IV A, Eqs. (28)–(32), p. 5 |
| Finite difference | MSE σ₀²/(2Nh²) + f₃²h⁴/36, optimal h* ∝ N^(−1/6), error ∝ N^(−2/3) | §IV B, Eqs. (33)–(42), pp. 5–6 |
| Parameter shift | Unbiased; Var = [σ₀²(θ+s) + σ₀²(θ−s)]/(4N sin² s); s = π/2 optimal under Assumption 1 | §IV C, Eqs. (43)–(50), p. 7 |
| Scaled parameter shift | λ·ĝ; λ* = 1/(1 + Var/g²); never worse than FD or PS (in MSE) | §IV C 2, Eqs. (51)–(57), p. 7; §IV D, Eqs. (58)–(62), p. 8 |
| Optimisers | GD, Newton, diagonal Newton, QNG, regularisation | §V, Eqs. (63)–(66), pp. 9–10 |
| Experiments | 5-qubit circuit (Fig. 1); MSE vs step size, simulator and ibmq_valencia (Fig. 2); Hessian on hardware (Fig. 3); optimisation on ibmq_burlington/valencia (Fig. 4) | §VI, pp. 10–13 |
| Appendix | Fixed θ (Eq. A1); optimal step vs N (Fig. 5); MSE vs N with the FD/PS crossover at N ≈ 50 (Fig. 6); Hessian MSE (Figs. 7–8); simulator optimisation (Figs. 9–10) | App. A, pp. 15–17 |

## 2. Estimator, statistic and shot convention

- **Estimator.** The same two-term parameter-shift estimator as Stage 7 (s = π/2), built from two independent
  N-shot estimates.
- **Statistic.** The MSE at a **fixed parameter point**: the expectation is over measurement outcomes only (Eq. 28). It
  is not averaged over circuits (contrast Teo, `B5_TEO_DEEP_AUDIT.md` §3) or over θ. This makes Mari's formulas
  per-θ statements, like Stage 7's.
- **Shot convention.** N shots per expectation value, i.e. per shifted circuit, so **N ↔ Stage 7's M** exactly. A
  gradient component costs 2N shots.
- **Single-shot variance.** σ₀² "depends on the specific details of the circuit and of the observable" (p. 5). The
  paper does not evaluate it for any particular readout.

## 3. The per-θ variance formula and the readouts (C5, C3)

- **Explicit (F-01).** Var(ĝ^(s)) = [σ₀²(θ_j + s) + σ₀²(θ_j − s)]/(4N sin² s) (Eq. 45, p. 7). This is the general
  per-θ variance of the parameter-shift estimator, with the single-shot variance kept separate at the two shifts.
- **Readouts named, not compared (F-03).** For the metric tensor, the survival probability |⟨ψ(θ′)|ψ(θ)⟩|² can be
  estimated "either with a swap-test, or more simply" as the probability of the 00…0 bit string after
  U(θ′)†U(θ) (§III C, p. 3). These are the two readouts Stage 7 compares. No variance, shot count or failure mode is
  given for either.
- **Our substitution (F-02, RELATED BUT DIFFERENT for row 31).** At s = π/2 with N = M, put σ₀²(θ±) = F±(1 − F±)
  (Loschmidt) or 1 − F±² (SWAP) into Eq. (45). This gives exactly Stage 7's Var(ĝ_LE) and Var(ĝ_SWAP) and the
  principal track's ratio identity R. The source supplies the variance structure; the readout-specific σ₀² come from
  paper B (B-10a) or Zhan et al. (H-01).
- **Assumption 1 (p. 6)** says σ₀²(θ + x) + σ₀²(θ − x) ≈ 2σ₀². The authors note that it can fail for large shifts.
  *(Our algebra:)* it is a condition on the **sum** of the two single-shot variances.
  - **Loschmidt readout, small fidelity:** σ₀²(θ_k + x) + σ₀²(θ_k − x) ≈ A(1 + cos θ_k cos x), while
    2σ₀²(θ_k) ≈ A(1 + cos θ_k). At the parameter shift x = π/2 the sum is ≈ A, so the assumption fails by the factor
    (1 + cos θ_k): a factor 2 at θ_k = 0. It holds only where cos θ_k ≈ 0 (numerically, at A = 0.01 the ratio of the
    two sides is 0.50 at θ_k = 0, 1.0 at θ_k = π/2 and 3.4 at θ_k = 3π/4).
  - **SWAP readout, small fidelity:** both sides are ≈ 2 and the assumption holds.
  - Where it fails, the approximations (46), (47) and (50) are off, while the exact Eq. (45) still holds. Stage 7 uses
    the exact form.

## 4. Relation to the candidates

| Candidate | Status in Mari 2021 | Entries |
|---|---|---|
| C1 exact law, P(ĝ = 0), P_correct, P_wrong | Moments only (zero-mean noise, Eq. 25); qualitative hardware remark that the gradient direction is "prone to error" (p. 13); no probabilities | F-04, F-05, F-NL09 |
| C2 conditional sign law (product and general) | Not located | F-NL09 |
| C3 readout-dependent exponent | Not located; no n-dependence anywhere; no readout statistics | F-NL02 |
| C4 vector / trajectory | Matched starts across shot budgets with an exact-gradient reference path (Fig. 4) on a 2-parameter, 5-qubit hardware problem, no barren plateau, no signal-free control; a mean-square norm relation follows from Eqs. (29) and (44); no direction metrics or random walk | F-06, F-11, F-NL20 |
| C5 shot-ratio identity | General per-θ variance (Eq. 45) with unspecified σ₀²; both readouts named for one fidelity; no ratio | F-01, F-02, F-03 |
| C5 exponent rule | Not located | F-NL27 |
| Gradient MSE (row 29) | Explicit per-θ MSEs of PS, FD and SPS | F-01, F-10 |
| Critical copy number (row 30) | Explicit numerical FD/PS crossover at N ≈ 50 shots for one circuit (Fig. 6; p. 11) | F-07 |

## 5. Relation to Teo 2023 and Aghaei Saem 2026

- **Teo 2023** (D) takes Mari's SPS estimator and FD/PS comparison and averages them over two-design circuits.
  - Mari's per-θ crossover (N ≈ 50, one circuit) becomes Teo's circuit-averaged N_* ∝ 2ⁿ (D-06).
  - Mari's per-θ MSEs become Teo's circuit-averaged MSEs (D-05a).
- **Aghaei Saem et al.** (B) examine the "rescaled gradient approach" of their ref. [87] (Teo) and argue it remains
  prone to exponential concentration (B-13, B-17).
  - Mari's own motivation for the scaled estimator is the noise-dominated barren-plateau regime: "could potentially
    be helpful when faced with the so-called barren plateau" (p. 7; F-08).
  - B5 records both statements and takes no position.

## 6. Arithmetic observation (no Stage 7 impact)

- **Eq. (49) as printed** (p. 7) reads [σ₀²(θ_j + π/2) + σ₀²(θ_j − π/2)]/(**2N**).
- **What the paper's own equations imply** is 4N:
  - Eq. (45) at s = π/2 gives denominator 4N sin²(π/2) = 4N;
  - the estimator of Eq. (48) has variance [σ₀²(θ₊)/N + σ₀²(θ₋)/N]/4;
  - Eq. (50), σ₀²/(2N), follows from 4N under Assumption 1 (sum ≈ 2σ₀²), not from 2N.
- The same text appears in arXiv v1 (LaTeX line 679 in v2). Whether the APS version differs is unverified.
- **Stage 7 is not affected:** it uses 4M (STAGE7.md §5–§6), consistent with Eq. (45).

## 7. What is explicit, implied, different, not located

- **Explicit:**
  - the finite-shot PS estimator and its per-θ variance (rows 7, 29);
  - per-θ FD and SPS MSEs (row 29);
  - a numerical FD/PS crossover (row 30);
  - matched-start trajectories on a toy problem (row 24).
- **Implied only with external input:** Stage 7's two gradient variances and the principal track's ratio identity,
  after inserting readout-specific σ₀² from B or H.
- **Related but different:**
  - the noise model (row 12);
  - qualitative direction errors (rows 10, 11, 23);
  - both readouts named for one fidelity (row 14a);
  - the SPS proposal for barren plateaus (row 26);
  - a background barren-plateau remark (rows 1, 5);
  - the mean-square norm relation E‖ĝ‖² = ‖g‖² + Δ(ĝ) (row 21; our algebra from Eqs. 29 and 44).
- **Not located:**
  - readout statistics and readout comparisons (rows 2–4, 14b, 15–18);
  - zero and sign laws (rows 9, 13, 19, 33);
  - distinguishability, random walk, direction metrics, signal-free control (rows 6, 8, 20, 22, 25);
  - the product landscape, parity numerics and the exponent rule (rows 27, 28, 32).

`NOT LOCATED` means only: not found in arXiv:2008.06517v2 after the logged searches. This audit is evidence for A1 and
does not make the novelty decision.
