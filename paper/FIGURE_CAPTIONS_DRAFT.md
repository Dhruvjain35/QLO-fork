# Figure captions (draft)

These are draft captions for the figures built by `python -m qlo.paper.figures`. They state what is plotted and its
limits. They make no novelty statement. The claim list and framing are decided by the principal track (P2, P5), so
the wording here may change. Every number below is taken from the committed result files named in
[`figures/FIGURE_SOURCES.md`](figures/FIGURE_SOURCES.md). All results come from classical simulation; none is from
quantum hardware ([`docs/phase8/REPRODUCTION_STATUS.md`](../docs/phase8/REPRODUCTION_STATUS.md) once PR #8 is merged).

---

**Figure 1. One landscape, two readouts.**

- **(a) Setting.** The Stage 7 benchmark:
  - an RX product state on n qubits with target |0ⁿ⟩ and fidelity F(θ) = ∏ⱼ cos²(θⱼ/2), θⱼ ~ U[−π, π];
  - the parameter-shift gradient of C = 1 − F with respect to θ_k (k = 0);
  - the two shifted fidelities are estimated either by a Loschmidt (projector) readout or by an ancilla SWAP test.

  Both readouts estimate the same F± and the same exact gradient g. They differ only in the per-shot statistics,
  F(1 − F) for Loschmidt and 1 − F² for SWAP.
- **(b) Required shots.** Median log₁₀ of the shots per shifted circuit, M, needed for SNR ≥ 1. The data are 100,000 θ
  per n, n = 2–20, the same θ for both readouts.
  - Shaded bands are the interquartile range over θ.
  - Lines are the committed least-squares fits: slope 0.606 (Loschmidt) and 1.203 (SWAP) decades per qubit, close to
    log₁₀ 4 and log₁₀ 16.
- **(c) Slope stability.** For four targets (SNR ≥ 1, SNR ≥ 2, sign accuracy ≥ 0.75, sign accuracy ≥ 0.9), the
  Stage 7 slope minus its reference (log₁₀ 4 for Loschmidt, log₁₀ 16 for SWAP), in units of 10⁻³ decades per qubit.
  - Thick bars: B3 95% percentile interval over 20 independent seeds of 25,000 θ.
  - Thin bars: the B3 θ-bootstrap 95% CI.

**Limitation.** The bases 4ⁿ and 16ⁿ belong to this RX-product benchmark, where the median shifted-fidelity sum
decays as 4⁻ⁿ. They are not universal. Other circuits have other base rates (Figure 3). Only one parameter
position (k = 0) and noiseless circuits are shown.

---

**Figure 2. Conditional sign accuracy of the Loschmidt gradient.**

- **(a) Exact probability against the prediction.** The exact probability that a nonzero Loschmidt gradient estimate
  has the correct sign, plotted against the prediction (1 + |r|)/2, where r = (F₋ − F₊)/(F₋ + F₊).
  - The 720 points cover the 16 B1 entangling cells at n = 12, θ at five quantiles of S = F₊ + F₋, and M = 1 to 65,536
    shots per shifted circuit.
  - Colour is log₁₀(M S).
- **(b) Deviation against M S.** Observed minus predicted. It is positive in every row and falls with M S. For
  M S ≤ 10⁻² (shaded) the largest deviation is 4.8 × 10⁻⁴.
- **(c) Population medians.** The median over θ of the same probability on the regenerated Stage 7 RX-product
  population, computed without cancellation (B3 D2), for n = 12–24 and M = 16–65,536.
  - Error bars: B3 95% percentile interval over 20 seeds.
  - Dashed line: (1 + 1/√2)/2 = 0.8536, the population median of the prediction.
  - At n = 20 and the Stage 7 shot counts (M = 64, 1,024, 16,384) the median is 0.8527–0.8530.

**Limitation.** The prediction is a limit for M·S → 0. Departures at large M·S, visible at n = 12 for M ≥ 1,024,
are expected and are not refitted. Panel (a) is exact (no sampling). Panel (c) uses the cancellation-safe values
that replace the earlier Stage 7 figure (Phase 8 I1).

---

**Figure 3. The slope rule across entangling circuits (B1).**

The data are slopes of median log₁₀ quantities against n for 17 cells:
- the RX-product regression arm, n = 2–20;
- a hardware-efficient ring ansatz (RY, RZ, CNOT ring);
- an RX-RY CZ brickwork ansatz.

The two entangling ansätze are run at depth 2, depth 4 and depth n, with the differentiated parameter in the early,
middle or late layer, on n = 4–16 (depth 2 and 4) or n = 4–14 (depth n). Each cell uses 10 seeds of 4,000 θ per n.
Marker shape is the family; marker fill is the depth (hollow: 2, half: 4, filled: n). Error bars are bootstrap 95%
CIs of the 10-seed mean.

- **(a)** The measured gap b_SWAP − b_LE against b_S, the slope of the shifted-fidelity sum. The line is equality.
- **(b)** The residual ε_gap = (b_SWAP − b_LE) − b_S as a percentage of b_S. It ranges from −1.28% to −0.48%.
- **(c)** b_r, the slope of the relative gradient |r|, by parameter position. Every |b_r| ≤ 3 × 10⁻³ decades per qubit.
  Six cells have CIs that exclude zero. The largest is the brickwork depth-n middle cell (−2.9 × 10⁻³).
- **(d)** The observed exponent ratio b_SWAP/b_LE against the ratio predicted from the same cell's b_S and b_r. The
  observed ratios (1.969–2.010) lie 0.5–1.6% below the prediction.

**Limitation.** Two ansatz families, one target state, noiseless circuits and n ≤ 16. The sub-percent residual is
reported, not removed.

---

**Figure 4. Four fidelity-gradient estimators on the RX-product landscape (B2).**

The estimators are Loschmidt, ancilla SWAP, destructive SWAP (two copies, no ancilla) and a Hadamard-test U-statistic.

- **(a) Required executions.** Median log₁₀ total circuit executions per gradient component for SNR ≥ 1. The data
  are the Stage 7 population of 100,000 θ per n, n = 2–20. Bands are interquartile ranges. The destructive and
  ancilla SWAP medians agree to 2 × 10⁻¹³.
- **(b) Fitted slopes.** Each slope minus its reference (log₁₀ 4 for Loschmidt and Hadamard, log₁₀ 16 for the SWAPs),
  in 10⁻³ decades per qubit, for n = 2–20 (filled) and n ≥ 8 (open). Error bars are 95% percentile intervals over 10
  replicate seeds of 25,000 θ. Printed values are the n = 2–20 slopes.
- **(c) Execution ratios.** Ratio of median total executions: Hadamard to Loschmidt is 9.0 at n = 2 and 9.4–9.55 for
  n ≥ 4; destructive to ancilla SWAP is 1.
- **(d–f) Fixed budgets.** At n = 14 and a fixed budget of T total executions:
  - (d) the median probability of an exactly zero estimate;
  - (e) the median probability of the correct sign given a nonzero estimate;
  - (f) the median probability of the correct sign.

  These are exact enumerations, except Hadamard at T ≥ 8,192, which is Monte Carlo with 20,000 repetitions.

**Limitation.** Executions are counted per gradient component. Qubit number, circuit depth, ancillas and the number
of state copies differ between readouts (B2 resource table), so equal execution counts do not mean equal hardware
cost. Noiseless simulation only.

---

**Figure 5. Depolarizing noise (B4).**

Global depolarizing noise acts after every layer, which is exactly equivalent to F' = qF + (1 − q)/2ⁿ with
q = (1 − p)^L. It is applied to the RX product (L = 1) and to the 16 B1 entangling cells. Local single-qubit
depolarizing noise is applied to the RX product only. The data reuse the B1 θ populations (10 seeds).

- **(a) Local slopes.** Three-point local slopes of the seed-mean medians for the RX product under global noise:
  Loschmidt b_LE (filled) and SWAP b_SWAP (open), for p = 0 to 10⁻¹. With noise, b_LE rises from log₁₀ 4 toward log₁₀ 8
  (0.90 at the largest window for p ≥ 10⁻²). b_SWAP stays at 1.20.
- **(b) Exponent ratio.** b_SWAP/b_LE against p:
  - RX product under global noise, fits over n = 2–20 (open) and n ≥ 8 (filled);
  - the committed Proposition 5 asymptote for the RX product (bars);
  - the RX product under local noise (squares);
  - the 16 entangling cells under global noise (gray, n ≥ 8).
- **(c) Local noise.** Measured b_S' for the RX product, with the closed form of Proposition 6 (line).
- **(d) Crossover.** The crossover n*, where the noise floor equals the noiseless signal scale, for the RX product
  (n* = 15.4, 12.1, 8.7 and 5.2 at p = 10⁻⁴ to 10⁻¹) and for the 13 entangling cells whose crossover lies inside the
  tested range (all at p = 10⁻¹). Cells where the signal dominates throughout are not plotted.

**Limitation.** Simulated depolarizing channels only, with an ideal SWAP target copy. Other noise channels, local
noise on entangling circuits, and hardware are not covered. The fixed-depth entangling cells are mostly
pre-asymptotic at n ≤ 16.

---

**Figure 6. Empirical estimator comparison (not a theorem or a complete taxonomy).**

For the four estimators of Figure 4, the horizontal axis is the fitted shot-cost exponent (median total executions,
n = 2–20, with the 95% replicate interval). The vertical axis is a finite-shot failure statistic at n = 14:
- (a) the median probability of an exactly zero estimate;
- (b) the median probability of the correct sign given a nonzero estimate.

Markers are the values at T = 2,048 total executions. The shaded bars show the range over T = 32–32,768.
- Loschmidt combines the lower exponent with exact-zero estimates.
- Both SWAP readouts combine the higher exponent with nonzero estimates whose sign is correct half the time.
- The Hadamard U-statistic combines the lower exponent with nonzero estimates whose sign is correct half the time.

**Limitation.** One landscape (RX product), one n and the B2 budget grid. Whether exponent and failure type are
independent properties in general is the open principal-track question P4. This figure shows measured values only.
