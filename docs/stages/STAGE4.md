# Stage 4 — Does finite-shot stochasticity help escape a verified barren plateau?

## 1. Purpose
Test, on the Stage 3 global benchmark whose barren plateau is independently verified
(`Var_θ[∂C/∂θ_k] = (1/8)(3/8)^(n−1)`), whether the stochasticity of finite-shot gradient
estimates gives a reproducible optimization / escape advantage over noiseless gradient
descent, and if so whether the effect is specific to the finite-shot (binomial)
distribution or is reproduced by classical Gaussian noise with the same covariance.

## 2. Why falsification-first
Beneficial stochasticity for *saddle* escape is already in the literature, and
shot-noise-leveraging optimizers already exist (§14). Saddle escape and barren-plateau
escape are not the same thing, and the 2026 saddle-escape result explicitly does not claim
to circumvent barren plateaus. The naive QLO premise — that shot noise is useful
exploration *inside* a genuine plateau — is therefore the hypothesis at risk, and Stage 4
is designed to give it every chance to fail: predeclared tuning score, strict
tuning/evaluation seed separation, held-out seeds, paired comparisons, matched-covariance
Gaussian and noise-only controls.

## 3. Projector finite-shot estimator
Benchmark: `|ψ(θ)> = ⊗_j RX(θ_j)|0^n>`, `θ_j ~ U[−π,π]`, `F = |<0^n|ψ>|² = ∏ cos²(θ_j/2)`, `C = 1 − F`,
`∂C/∂θ_k = ½ sin θ_k ∏_{j≠k} cos²(θ_j/2)`.
Measuring the projector `|0^n><0^n|` M times gives `K ~ Binomial(M, F)`, `Ĉ = 1 − K/M`
(`qlo.stage4.shots.BinomialProjectorShots`). Parameter shift
`ĝ_k = ½[Ĉ(θ+π/2 e_k) − Ĉ(θ−π/2 e_k)]` with an independent M-shot batch for every
(k, ±), iteration and replicate; conditional variance
`Var(ĝ_k|θ) = [F₊(1−F₊) + F₋(1−F₋)]/(4M)` (`conditional_shot_variance`). With one batch per
(k, ±) the conditional covariance is diagonal *by construction of this measurement
strategy* — not a universal statement. Randomness: one Generator per trajectory from an
explicit `SeedSequence([4, 200, method_id, n, start_seed, replicate, config_id])`; methods
have distinct ids so draws are never shared. The estimator never sees the exact gradient
(tested by source inspection and by monkey-patching).

## 4. PennyLane / binomial validation (`crosscheck_pennylane_vs_binomial.csv`)
n ∈ {3,4,6} × 2 θ seeds × θ-scale ∈ {1.0 (Stage-3-distributed), 0.4 (moderate F)} ×
M ∈ {64,256,1024} × k ∈ {0, n−1}, 400 repetitions of the parameter-shift component each way.
Over the 66 non-degenerate cells (F > 1e-4): PennyLane-vs-binomial mean difference
max |z| = 2.34 (3.0 % of cells beyond 1.96, as expected); both means agree with the exact
gradient (max |z| 2.1 / 2.4); PennyLane/binomial variance ratio 0.80–1.26, mean 0.998
(expected SD ≈ 0.10); PennyLane/theory 0.83–1.17 (mean 0.976), binomial/theory
0.81–1.16 (mean 0.985). Six low-F cells (F ≤ 1e-4) are in the small-count regime (counts
mostly 0) — one is fully degenerate (all K = 0 in both simulators, an exact but trivial
agreement) and the rest have noisy ratios 0.5–1.5, as expected when the variance is
carried by a handful of non-zero counts. The Binomial simulator reproduces the
measurement statistics of the ideal PennyLane simulator.

## 5. Initial signal-to-noise scaling (`snr_summary.csv`, `snr_scaling.csv`)
5000 Stage-3-distributed θ per n; `Σ_shot` from the analytic conditional variance.

| n | median F₀ | median ‖g‖ | median √trΣ/‖g‖ at M=16 / 64 / 256 / 1024 | frac. NSR>1 at M=1024 |
|---|---|---|---|---|
| 4 | 7.9e-3 | 3.9e-2 | 1.47 / 0.74 / 0.37 / 0.18 | 0.20 |
| 6 | 5.5e-4 | 4.2e-3 | 5.67 / 2.83 / 1.42 / 0.71 | 0.44 |
| 8 | 3.4e-5 | 3.5e-4 | 22.5 / 11.3 / 5.6 / 2.8 | 0.69 |
| 10 | 1.9e-6 | 2.7e-5 | 95 / 48 / 24 / 12 | 0.86 |
| 12 | 1.2e-7 | 2.1e-6 | 370 / 185 / 93 / 46 | 0.94 |

Median ‖g‖ shrinks by ×0.29 per qubit, median trΣ by ×0.33 per qubit, so the median
noise/signal ratio **doubles per qubit** (×2.00) at every M, i.e. NSR ∝ 2ⁿ/√M. The
"stochastic update scale" `η√trΣ` is 1e-4…1e-5 at n ≥ 10 (η=0.1): shot noise is
relatively enormous but absolutely tiny. This is characterization, not a success criterion.

## 6. Tuning protocol
Predeclared. Tuning start seeds 0–39, n ∈ {6,8,10}, 2000 iterations, one trajectory per
(config, n, start). Score = `log10((F_best+1e-300)/(F0+1e-300))` with exact offline F.
Selection: (1) highest median score pooled over all 120 tuning runs; (2) tie → higher rate
of `F_best ≥ 0.1`; (3) shot SGD only → fewer total shots; (4) smaller η. Grids as
specified: GD η ∈ {0.01,0.03,0.1,0.3,1.0}; SGD η ∈ {0.01,0.03,0.1,0.3} × M ∈ {16,64,256,1024};
Langevin η ∈ {0.03,0.1,0.3} × σ ∈ {0.01,0.03,0.1,0.3}. Matched Gaussian and noise-only
inherit SGD's (η, M) untuned. Evaluation seeds 1000–1099 were never used for selection
(tested disjoint). All 3 960 tuning runs are in `tuning_results.csv`.

## 7. Selected hyperparameters (`selected_hyperparameters.json`)
| method | selected | median score | rate F_best ≥ 0.1 |
|---|---|---|---|
| A exact GD | η = 1.0 | 2.47 | 0.72 |
| B finite-shot SGD | η = 0.3, M = 64 | 2.25 | 0.67 |
| D constant Langevin | η = 0.3, σ = 0.1 (D = σ²/2η = 0.0167) | 3.21 | 0.77 |
| C, E | η = 0.3, M = 64 (inherited) | — | — |

Two facts from the grid matter for interpretation. (i) Shot SGD's score is flat in M
(2.22 / 2.25 / 2.18 / 2.18 at η=0.3) and equals exact GD at the same η (2.18): on the
tuning set, shot noise changes nothing. (ii) The GD grid extends to η = 1.0 but the SGD
grid stops at 0.3 (as specified), so the *primary* B-vs-A comparison confounds noise with
learning rate. Two secondary controls were therefore added to the held-out evaluation
without altering the protocol: **exact GD at η = 0.3** (matched η) and **pure diffusion**
(Langevin σ = 0.1 with η = 0, no gradient) to separate D's exploration from its capture.

## 8. Held-out results (`evaluation_summary.csv`, `evaluation_runs.csv.gz`; seeds 1000–1099, 2000 iterations)
A: 1 trajectory / seed; B, C, D, E and the controls: 5 replicates / seed (500 runs per cell).

| n | method | median log10(F_best/F0) [IQR] | median F_final | P(F ≥ 0.01) | P(F ≥ 0.1) | P(F ≥ 0.5) | P(≥10×F0) |
|---|---|---|---|---|---|---|---|
| 6 | A exact GD η=1 | 2.60 [1.49, 3.93] | 1.000 | 0.78 | 0.81 | 0.82 | 0.86 |
| 6 | A′ exact GD η=0.3 | 2.26 [1.14, 3.46] | 1.000 | 0.71 | 0.74 | 0.75 | 0.80 |
| 6 | B shot SGD | 2.26 [1.17, 3.51] | 0.999 | 0.71 | 0.75 | 0.75 | 0.80 |
| 6 | C matched Gaussian | 2.26 [1.18, 3.51] | 0.999 | 0.70 | 0.74 | 0.75 | 0.80 |
| 6 | D Langevin | 3.45 [2.23, 4.59] | 0.950 | 1.00 | 1.00 | 1.00 | 1.00 |
| 6 | D′ pure diffusion | 2.74 [1.56, 3.86] | 4.1e-4 | 1.00 | 0.79 | 0.10 | 0.90 |
| 6 | E noise-only | 0.17 [0.07, 0.40] | 2.6e-4 | 0.13 | 0.03 | 0.00 | 0.04 |
| 8 | A exact GD η=1 | 2.77 [0.57, 3.71] | 1.000 | 0.66 | 0.67 | 0.68 | 0.70 |
| 8 | A′ exact GD η=0.3 | 1.57 [0.15, 3.10] | 1.000 | 0.48 | 0.51 | 0.52 | 0.56 |
| 8 | B shot SGD | 1.56 [0.17, 3.14] | 0.997 | 0.48 | 0.51 | 0.52 | 0.57 |
| 8 | C matched Gaussian | 1.56 [0.19, 3.10] | 0.997 | 0.48 | 0.51 | 0.52 | 0.57 |
| 8 | D Langevin | 3.78 [2.78, 5.91] | 0.924 | 0.94 | 0.87 | 0.86 | 0.99 |
| 8 | D′ pure diffusion | 2.93 [1.68, 4.75] | 2.5e-5 | 0.92 | 0.34 | 0.01 | 0.90 |
| 8 | E noise-only | 0.08 [0.02, 0.22] | 5.5e-5 | 0.04 | 0.00 | 0.00 | 0.02 |
| 10 | A exact GD η=1 | 1.94 [0.06, 4.19] | 1.000 | 0.51 | 0.51 | 0.52 | 0.57 |
| 10 | A′ exact GD η=0.3 | 0.36 [0.02, 2.95] | 2.3e-5 | 0.33 | 0.34 | 0.35 | 0.41 |
| 10 | B shot SGD | 0.51 [0.03, 2.94] | 2.1e-5 | 0.33 | 0.33 | 0.35 | 0.41 |
| 10 | C matched Gaussian | 0.50 [0.04, 2.98] | 2.5e-5 | 0.33 | 0.34 | 0.35 | 0.41 |
| 10 | D Langevin | 4.20 [2.72, 5.71] | 0.803 | 0.74 | 0.51 | 0.51 | 0.97 |
| 10 | D′ pure diffusion | 3.18 [2.15, 4.97] | 4.0e-6 | 0.60 | 0.07 | 0.00 | 0.93 |
| 10 | E noise-only | 0.04 [0.01, 0.13] | 8.8e-6 | 0.01 | 0.00 | 0.00 | 0.02 |
| 12 | A exact GD η=1 | 0.015 [0.000, 0.42] | 9.7e-8 | 0.19 | 0.19 | 0.19 | 0.20 |
| 12 | A′ exact GD η=0.3 | 0.004 [0.000, 0.11] | 9.5e-8 | 0.12 | 0.12 | 0.12 | 0.12 |
| 12 | B shot SGD | 0.008 [0.000, 0.15] | 9.3e-8 | 0.12 | 0.12 | 0.11 | 0.13 |
| 12 | C matched Gaussian | 0.014 [0.002, 0.19] | 9.4e-8 | 0.12 | 0.12 | 0.12 | 0.14 |
| 12 | D Langevin | 5.13 [3.25, 7.01] | 9.5e-7 | 0.39 | 0.19 | 0.19 | 0.98 |
| 12 | D′ pure diffusion | 4.69 [3.03, 6.65] | 1.9e-7 | 0.27 | 0.01 | 0.00 | 0.96 |
| 12 | E noise-only | 0.007 [0.002, 0.04] | 8.9e-8 | 0.00 | 0.00 | 0.00 | 0.01 |

Wilson 95 % CIs for all success probabilities are in the CSV (half-widths ≈ 0.03–0.09).
Outcomes are bimodal (a run either converges to F ≈ 1 or stays at F ≈ F0), which is why
paired *median* differences below are ≈ 0 while means and success rates differ.

## 9. Exact GD vs finite-shot SGD (`paired_comparisons.json`, paired by start seed, 10 000-sample bootstrap)
Primary (A at η=1 vs B at η=0.3, M=64): B is **worse** at every n — mean Δlog10(F_best/F0)
= −0.31 [−0.51, −0.15], −0.71 [−1.02, −0.42], −0.74 [−1.03, −0.46], −0.37 [−0.61, −0.16]
for n = 6, 8, 10, 12; ΔP(F ≥ 0.1) = −0.07, −0.16, −0.18, −0.07 (all CIs exclude 0); B never
beats A on a single seed (frac B > A = 0.00–0.10).
Matched η (A′ at η=0.3 vs B): **no difference** — mean Δ = +0.03 [+0.00, +0.06], +0.04
[−0.04, +0.10], +0.04 [−0.01, +0.09], +0.01 [−0.02, +0.03]; ΔP(F ≥ 0.1) = +0.006, 0.000,
−0.004, −0.004 with CIs inside ±0.025; 96–99 % of seeds tie exactly on success.
The primary deficit is entirely the learning rate; the shot noise itself neither helps
nor hurts the escape statistics at any tested n or M.

## 10. Finite-shot SGD vs matched Gaussian
B and C are statistically indistinguishable: mean Δlog10 gain = +0.01, −0.00, −0.01,
−0.02 (n = 6…12), ΔP(F ≥ 0.1) within ±0.005, identical IQRs, and representative
trajectories overlay (figure 2). The only reproducible difference is at n = 12:
Δ = −0.023 [−0.042, −0.006] against B, tiny in effect but real in mechanism — with F± ≈ 1e-7
and M = 64, every shot batch usually returns K = 0, so ĝ is *exactly zero* and the
optimizer does not move at all in 44 % of runs (54 % at M = 16, 29 % at M = 1024), versus
0.6 % for the Gaussian surrogate. *(Erratum, Stage 5: these fractions used
`log10(F_best/F0) < 1e-12` and so also counted runs that moved only downhill; the exact
never-moved fractions are 50.0 / 39.8 / 29.8 / 24.2 % at M = 16 / 64 / 256 / 1024, and
STAGE5.md §12 retrodicts them from the exact zero-gradient probability with no free parameter.)* Binomial shot noise is quantized to zero on a deep
plateau; Gaussian noise of the same variance is not. Neither produces escape.

## 11. Constant Langevin control
D (η = 0.3, σ = 0.1, D_coef = 0.0167) beats every other method on F_best at every n and
also on F_final for n ≤ 10 (median F_final 0.95, 0.92, 0.80 at n = 6, 8, 10; success
P(F ≥ 0.5) = 1.00, 0.86, 0.51). Versus A: ΔP(F ≥ 0.1) = +0.18 [+0.11, +0.26] at n=6,
+0.19 [+0.10, +0.29] at n=8, **0.00 [−0.10, +0.11] at n=10, 0.00 [−0.08, +0.08] at n=12**.
Versus pure diffusion (same σ, no gradient): D wins on F_final by 3.6, 4.3, 3.1, 1.5
decades, so the benefit is exploration-then-capture, not random-walk luck; but pure
diffusion alone already reaches F ≥ 0.01 in 100 %, 92 %, 60 %, 27 % of runs (n = 6…12),
which shows how much of the F_best metric is exploration. D's per-step noise scale
(σ = 0.1) is 10²–10⁴ times larger than the shot-noise update scale (§5); it is a generic
exploration control, not a model of shot noise, and no FDT/temperature relation is implied.
Its advantage vanishes by n = 10–12 as the target basin shrinks.

## 12. Resource accounting (finite-shot SGD only; controls use analytic oracles and are not hardware-comparable)
Per iteration: 2n circuit evaluations, 2nM shots (verified independently for all 8 000 B
runs: totals and at-hit values equal 2n·M·iteration exactly). Success is independent of M
at every n (P(F ≥ 0.1) at M = 16/64/256/1024: 0.75/0.75/0.75/0.75 at n=6; 0.51/0.51/0.51/0.51
at n=8; 0.34/0.33/0.34/0.34 at n=10; 0.11/0.12/0.12/0.12 at n=12), so the cheapest budget
minimizes shots-to-target:

| n | M | hits F≥0.1 / eligible | median shots to F ≥ 0.1 [IQR] | median circuit evals |
|---|---|---|---|---|
| 6 | 16 | 363/485 | 2.6e4 [7.9e3, 1.3e5] | 1.6e3 |
| 8 | 16 | 251/490 | 6.6e4 [2.5e4, 1.1e5] | 4.1e3 |
| 10 | 16 | 164/490 | 2.1e5 [9.4e4, 4.3e5] | 1.3e4 |
| 12 | 16 | 55/500 | 2.2e5 [1.3e5, 4.3e5] | 1.4e4 |
| 6 | 64 | 363/485 | 1.1e5 [3.2e4, 4.9e5] | 1.7e3 |
| 12 | 64 | 58/500 | 9.1e5 [5.6e5, 1.8e6] | 1.4e4 |

The runs that succeed at n = 12 are those whose *starting* fidelity is already large
enough for the gradient to be resolvable (the same 11–12 % that exact GD at η = 0.3
escapes); shots do not buy escape, they buy resolution of a gradient that is already there.

## 13. Outcome classification
**CASE 4 for the shot-noise hypothesis, with a CASE 3 component and a CASE 5 mechanism,
and NOT CASE 1 or 2.**
- B vs A at matched η: no benefit and no harm (CASE 4). B vs A at protocol η: worse, but
  because of η, not noise.
- B ≈ C: the finite-shot distribution has no advantage over covariance-matched Gaussian
  noise (rules out CASE 2). The one difference (zero-quantization at n=12) is a
  resolvability *deficit* of shot noise (CASE 5 in mechanism, negligible in effect).
- D helps at n ≤ 8 and not at n ≥ 10 (CASE 3, limited): generic diffusion 10²–10⁴× larger
  than shot noise can find the basin while it is not yet exponentially small; naturally
  occurring shot noise at any tested M cannot.
- E: shot-scale displacement alone does nothing (median gain ≤ 0.17 decades).

## 14. Relation to prior work
- Stochastic and shot noise have prior literature showing benefits for saddle-point /
  local-landscape optimization: J. Liu et al., "Stochastic noise can be helpful for
  variational quantum algorithms," Phys. Rev. A 111, 052441 (2025),
  doi:10.1103/PhysRevA.111.052441; E. Kaminishi et al., "Impact of measurement noise on
  escaping saddles in variational quantum algorithms," Sci. Rep. 16, 9390 (2026).
- Shot-noise-leveraging optimizers already exist: K. Ito and K. Fujii, "SantaQlaus: A
  resource-efficient method to leverage quantum shot-noise for optimization of variational
  quantum algorithms," arXiv:2312.15791.
- Stage 4 tests behaviour specifically inside an independently verified barren-plateau
  benchmark. Beneficial saddle escape and barren-plateau escape are not equivalent, and
  the 2026 saddle-escape paper states that its result does not establish circumvention of
  barren plateaus. Nothing here claims novelty beyond this experiment.

## 15. What the experiment establishes (for this benchmark, n ≤ 12, 2000 iterations, tested grids)
- The Binomial projector simulator reproduces PennyLane's finite-shot statistics.
- Finite-shot parameter-shift SGD does not improve, and at matched η does not degrade,
  escape statistics relative to exact GD; the effect is null within ±0.02 in success
  probability at every n.
- Covariance-matched Gaussian noise reproduces finite-shot SGD's behaviour; the only
  distinction is that binomial noise is quantized to exactly zero deep in the plateau.
- Large constant diffusion (σ = 0.1 ≫ shot scale) with an exact gradient helps at n ≤ 8
  and not at n ≥ 10.
- Success of shot SGD is independent of M from 16 to 1024; shots-to-target is minimized
  by the smallest M.
- The noise/signal ratio of shot gradients doubles per qubit.

## 16. What it does NOT establish
Anything about other ansätze, costs or initializations; about QNG, SPSA, Adam, SantaQlaus,
annealed or adaptive shot schedules, or injected Langevin noise on top of shot noise
(none implemented); about longer horizons than 2000 iterations or η > 0.3 for SGD; about
hardware noise; about FDT; about polynomial escape times; about quantum advantage. The
Langevin result is on an analytic-gradient oracle and says nothing about hardware cost.

## 17. Recommended next scientific step (conditional on this result)
Do **not** build a full QLO optimizer on the premise that shot noise is useful
exploration in a genuine plateau — Stage 4 falsifies that premise at the tested scales.
Two defensible directions remain, in order:
1. **Quantify the CASE 3 window.** The Langevin control shows that exploration with a
   *large* diffusion scale plus capture works while the basin is not yet exponentially
   small (n ≤ 8) and fails after. Measure how the required diffusion scale and the
   iterations-to-capture scale with n for the *cheapest hardware-realizable* version of
   that idea (exact-gradient Langevin is an oracle; the realizable analogue is
   finite-shot SGD with deliberately injected, decaying classical noise). If the
   crossover n grows only polynomially with budget, that is a result; if it is fixed, the
   idea is dead for plateaus.
2. **Resolvability, not exploration, is the binding constraint.** Since success is
   M-independent and the failure mode at n = 12 is ĝ ≡ 0, the relevant quantity is the
   shot budget at which the gradient becomes resolvable, which scales like 1/Var_θ[∂C] —
   exponential. A shot-schedule study (M growing with iteration or with a resolvability
   test) would characterize that cost honestly rather than hide it.
Either way, the next stage should keep this benchmark, these controls and the paired
held-out protocol.
