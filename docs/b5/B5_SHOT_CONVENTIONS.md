# B5 follow-up: shot conventions and their conversion to Stage 7

**Reference convention (Stage 7).**
- **M** = measurement shots **per shifted circuit** for one gradient component k, with one independent batch per
  (k, ±). So one component costs **2M** shots, and a full n-component gradient costs 2nM.
- Loschmidt: one shot = one preparation of the n-qubit variational state, read in the computational basis.
- SWAP: one shot = one run of the (2n + 1)-qubit SWAP-test circuit, consuming one copy of the variational state and one
  of the target. Stage 7 counts this as 2 state copies per shot (STAGE7.md §23).

Exponents or constants from different papers may be compared only after this conversion **and** only when the statistic
also matches ([`B5_STATISTIC_COMPARISON.md`](B5_STATISTIC_COMPARISON.md)). Where a conversion is impossible, that is
stated.

## 1. Per-paper symbols

| Paper | Symbol | Meaning in the source | Locator | Stage 7 equivalent | Conversion status |
|---|---|---|---|---|---|
| Stage 7 | M | Shots per shifted circuit, per component | STAGE7.md §5–§7 | M | Reference |
| Teo 2023 | N | Copies ("clicks") recorded when measuring one function f_{Q,k} (one Pauli term) at fixed parameters | p. 4; App. C 1 (Eq. C1) | M (per shifted circuit, per Pauli term) | Exact |
| Teo 2023 | N_T | **Total** copies for one estimator per circuit-observable basis operator O_k, split equally over its functions: 2N (gradient), 3N (diagonal Hessian), 4N (off-diagonal Hessian). Defined for FD approximators and used unchanged for PS/SPS (Eq. 13 is consistent with an equal split; our check); in App. C 2, N_T = N for one function estimate | p. 4; p. 5 (GD); p. 19 | 2M per gradient component (one Pauli term) | Exact: N_T = 2M |
| Teo 2023 | N (in D_θ0) | "N sampling copies" of each shifted function | §VII, p. 11 | M | Exact |
| Aghaei Saem 2026 | N | Shots per POVM measurement, i.e. per estimated quantity ℓ_i at one parameter point (S_N^(i) = {λ_j}_{j=1..N}) | §2, Eq. (1)–(2); App. B, Eqs. (B16)–(B18) | M (each shifted loss term gets N shots) | Exact for single-term losses; per term otherwise |
| Aghaei Saem 2026 | 150, 2¹⁵ (Fig. 3); 10 × n, 2ⁿ (Fig. 4) | Shot budgets per loss estimate in the numerics | Figs. 3–4, pp. 6–8 (v2) / 7, 9 (version of record) | M | As above |
| Aghaei Saem 2026 | N in Eq. (C11) | "the number of measurement shots" in λ = dN/(2d² + Nd − 2), taken from Teo | App. C, p. 25 (v2) / p. 20 (version of record) | Ambiguous: Teo's formula uses N_T (= 2M) | **Ambiguous** (see §2) |
| Thanasilp 2024 | N | Shots per kernel entry (one fidelity estimate) | Main p. 4; SI Notes II–III | M for one fidelity estimate F̂± (fidelity level only) | Exact at the fidelity level; no gradients |
| Thanasilp 2024 | N_s | Training-set size (number of data points), not shots | Main p. 4; SI | — | Not a shot count |
| Arrasmith 2021 | N | Shots per **cost-function evaluation** | §4, p. 7 | Not defined per component | Partial: equals M only if one evaluation were one shifted circuit |
| Arrasmith 2021 | N_total | Total shots used in one optimisation run until C = 0.4 (or a cap) | §4, Fig. 3 | — | **Not convertible**: depends on the number of evaluations, optimiser and N tuning; the gradient-descent reference's estimator is unspecified |
| Gentinetta 2024 | R | Shots per kernel entry (dual, Pegasos) or per expectation value (approximate QSVM) | Eq. (9), p. 8; §4.4, p. 14 | M for one fidelity or expectation estimate | Exact at the estimate level; no parameter-shift gradients |
| Gentinetta 2024 | R_tot | Total shots (dual: R·M(M+1)/2; Pegasos ≈ T·R); for SPSA, Fig. 10 counts circuit evaluations as 5·2·T | Eqs. (11), (18); Figs. 6, 10 | — | Not a per-component count |
| Gentinetta 2024 | **M** | **Training-set size**, not shots | Throughout | — | **Notation clash with Stage 7's M** |

### Closure-audit sources

| Paper | Symbol | Meaning in the source | Locator | Stage 7 equivalent | Conversion status |
|---|---|---|---|---|---|
| Mari 2021 | N | Shots per expectation value, i.e. per shifted circuit; σ₀² is the single-shot variance | Eq. (25), p. 5; Eqs. (43)–(50), p. 7 | M | Exact: Eq. (45) at s = π/2 with N = M has Stage 7's 4M denominator (Eq. 49 as printed has 2N, a typo) |
| Miranskyy 2025 | N | Shots (circuit executions) of the inverse or swap test needed to detect a deviation at error probability P_e | Eqs. (8), (11), pp. 6–9 | — | Not a per-component estimation budget; detection statistic |
| Zhan 2025 | N | Copies of the state (projection) or of the state pair (joint strategies: SCM, swap test) | Eq. (1), p. 2; Table 1, p. 4 | M for one fidelity estimate | Exact at the overlap level; the swap-type strategies consume one copy of each state per shot (Stage 7 counts this as 2 state copies per shot, STAGE7.md §23) |

## 2. Conversions of the formulas used in this audit

- **Teo, Eq. (13), PS MSE at s = π/2.** d/(N_T(d+1)) becomes **d/(2M(d+1)) ≈ 1/(2M)** in Stage 7 units.
  - This equals the deep-plateau value of Stage 7's SWAP variance, [2 − A²(1+s²)/2]/(4M) → 1/(2M). The prefactors are
    consistent after conversion.
  - Without the conversion (reading N_T as M) the two would differ by a factor 2.
- **Teo, Eq. (24), critical copy number.** N_* ≅ 32(d²−1)/(3d) becomes **M_* = N_*/2 ≈ (16/3)·2ⁿ** shots per shifted
  circuit. Its base 2 comes from the two-design average, not from the readout. It is not comparable to Stage 7's
  per-θ medians (B5_TEO_DEEP_AUDIT.md §7).
- **Teo, Eq. (26).** D_θ0 ≳ poly(d)/N with N = M per shifted function. No base is given, so there is nothing to convert
  numerically.
- **Teo, Eq. (22), and B, Eq. (C11).** Teo's λ_opt = dN_T/(2d² + dN_T − 2) uses the total copies N_T per component. B
  writes the same formula with N, "the number of measurement shots".
  - If B's N is per shifted circuit, as in the rest of B, the factor Teo prescribes would be λ = 2dN/(2d² + 2dN − 2).
  - B does not say which N it uses.
  - This does not affect any Stage 7 result, because Stage 7 does not use SPS. It matters only if B's Fig. 4(d) is
    re-run or cited quantitatively.
- **Aghaei Saem, Var^(LE), Var^(SWAP) per shot** (B-10a): divide by M for one fidelity estimate. For the gradient,
  Var(ĝ) = [Var₊ + Var₋]/(4M) with M per shift (B5_MATH_COMPARISON §6.2).
- **Aghaei Saem, Corollary 4 null update** (B15): [Δ_N]_k = −(η/2)Σ_i c_i(Z̄_ik − Z̄′_ik), with N shots per mean, so
  N ↔ M. The per-component null variance (η²/4)·(2/N)·Σ_i c_i² matches Stage 7's SWAP null sd ≈ 1/√(2M) for one term
  with c = 1, after including the factor η/2 (B5_MATH_COMPARISON §6.6).
- **Thanasilp, (1 − s)^N:** N ↔ M for one Loschmidt fidelity estimate. Stage 7's P(ĝ_LE = 0) involves two such counts,
  each with M shots (B5_MATH_COMPARISON §6.1).
- **Thanasilp, "N ∈ Ω(2ⁿ)" (SI Fig. 4):** shots per kernel entry, i.e. per fidelity estimate. The Stage 7 analogue is M
  per shifted circuit, but the statistic differs: a fraction of entries at the mean scale vs a median required M
  (B5_STATISTIC_COMPARISON.md).
- **Arrasmith, Fig. 3:** no conversion is possible. N_total aggregates many cost evaluations whose number is set by the
  optimiser, and N was tuned per n. The fitted slope of median N_total against n is not reported. The plotted range
  (roughly 10²–10¹² shots for n = 5–11) must not be compared with Stage 7's slopes.
- **Gentinetta:** R ↔ M only for a single kernel or expectation estimate. All of the paper's complexities are in the
  data-set size M and the accuracy ε at fixed n. No conversion to a per-component, n-dependent gradient budget exists.

## 3. Findings

1. **Teo's N_T is a per-component total** (2 × per-shift copies). Reading it as Stage 7's M overstates Teo's error by
   a factor 2. After conversion, Teo's average PS error and Stage 7's SWAP variance agree in the deep plateau.
2. **Teo's N_* is in copies per component;** in Stage 7 units M_* ≈ (16/3)·2ⁿ. Its exponent (base 2) reflects the
   two-design average and the FD/PS crossover. It is not a required-shot exponent and is not comparable to 4ⁿ or 16ⁿ.
3. **Aghaei Saem's N** is per POVM per quantity (per shifted loss term), which aligns with Stage 7's M. The exception is
   Eq. (C11), whose N is ambiguous relative to Teo's N_T.
4. **Gentinetta's M is the data-set size.** Any cross-reading with Stage 7's M is a notation error. Gentinetta's R is
   the shot count.
5. **Arrasmith's N_total and Gentinetta's R_tot are run-level totals.** They cannot be converted to per-component
   budgets without the optimiser's evaluation counts, which are not reported per component.
6. **Copies vs shots for SWAP.** Teo counts copies of the measured circuit state; Stage 7 counts shots and, separately,
   state copies (SWAP = 2 per shot). The factor 2 is a constant and does not change any exponent.

This document is evidence for A1 and does not make the novelty decision.
