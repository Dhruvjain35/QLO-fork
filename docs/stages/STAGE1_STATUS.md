# Stage 1 Status

> Stage 2 (finite-shot noise characterization) is complete — see `STAGE2.md`.

## Environment

| component  | version                                  |
|------------|------------------------------------------|
| Python     | 3.12.13 (`/opt/homebrew/opt/python@3.12`, via `uv venv`) |
| PennyLane  | 0.45.1 (installed cleanly; no fallback needed) |
| NumPy      | 2.5.3                                    |
| SciPy      | 1.18.1                                   |
| pandas     | 3.0.6                                    |
| matplotlib | 3.11.2                                   |
| pytest     | 9.1.1                                    |
| device     | `default.qubit`, `shots=None`, interface `autograd` |
| OS         | macOS (Darwin 25.4.0, arm64)             |

System `python3` is 3.14.5; 3.12 was chosen for wheel compatibility.

## Implemented

- [x] `HardwareEfficientAnsatz(n_qubits, depth, entangler)` — RY·RZ rotation
      layer + ring/chain CNOT layer per depth; params shape `(depth, n, 2)`,
      `p = 2·n·depth`; frozen dataclass, no mutable state.
- [x] Global cost `Z_0…Z_{n-1}` and local cost `(1/n)ΣZ_i` via one accessor.
- [x] Analytic scalar cost `C(θ)` on `default.qubit` (`shots=None`).
- [x] Gradients: autograd/backprop, parameter-shift, central finite-difference.
- [x] Centralized seeding (`make_rng`, `random_params`); legacy global NumPy
      RNG untouched (tested).
- [x] `bp_smoke` experiment: per-init gradient stats → tidy DataFrame → CSV
      (+ per-qubit aggregate CSV), CLI with `--qubits --depth --n-init --cost
      --seed --entangler --gradient --out`.
- [x] 47 tests across circuit / costs / gradients / reproducibility+smoke.
- [ ] Finite-shot devices, QLO optimizer, FDT analysis, chemistry, GPU,
      hardware — **deliberately not implemented**.

## Verification

`python -m pytest -v -W error::DeprecationWarning` → **47 passed, 0 failed, 0 warnings** (1.8 s).

Gradient agreement, n=2, depth=1, 5 seeds × 2 costs:

| comparison                                   | max abs diff |
|----------------------------------------------|--------------|
| autograd vs parameter-shift                  | 4.4e-16      |
| autograd vs central finite-diff (h=1e-5)     | 6.8e-11      |
| autograd vs hand-rolled π/2 shift rule (test) | < 1e-10     |

Also tested at (3,2,ring), (3,2,chain), (4,3,ring) with the same tolerances.
Independent cost checks: global cost = parity-weighted probability sum;
local cost = mean of individually measured `<Z_i>`; observable matrices match
explicit Kronecker constructions.

## Smoke Experiment

Config: `qubits=(2,4,6), depth=2, n_init=3, seed=0, entangler=ring, gradient=autograd`.
Per-qubit aggregates (mean over 3 inits). Full per-init rows in `results/`.

**global cost** (`results/bp_smoke_global_seed0.csv`)

| n | p  | mean_grad | mean_abs_grad | within_gradient_entry_var | ‖g‖ mean | ‖g‖ std |
|---|----|-----------|---------------|----------|----------|---------|
| 2 |  8 | -0.0581   | 0.1374        | 0.0521   | 0.717    | 0.125   |
| 4 | 16 |  0.0032   | 0.0745        | 0.0316   | 0.684    | 0.321   |
| 6 | 24 | -0.0076   | 0.0417        | 0.0122   | 0.539    | 0.166   |

**local cost** (`results/bp_smoke_local_seed0.csv`)

| n | p  | mean_grad | mean_abs_grad | within_gradient_entry_var | ‖g‖ mean | ‖g‖ std |
|---|----|-----------|---------------|----------|----------|---------|
| 2 |  8 |  0.0004   | 0.1132        | 0.0248   | 0.458    | 0.126   |
| 4 | 16 | -0.0012   | 0.0534        | 0.0064   | 0.317    | 0.054   |
| 6 | 24 | -0.0065   | 0.0155        | 0.0007   | 0.129    | 0.045   |

**These numbers demonstrate only that the pipeline runs and produces finite
output.** With 3 initializations, depth 2, and n ≤ 6 they carry no statistical
weight and must not be read as evidence for or against a barren plateau in
either cost.

## Known Limitations

- Analytic simulation only; no finite-shot path yet (by design for Stage 1).
- Smoke sample sizes are tiny; `var_first_partial` over 3 inits is essentially
  noise.
- (Fixed in Stage 2) the smoke statistic formerly named `var_grad` is the
  variance over the *entries of one gradient vector*; it is now named
  `within_gradient_entry_var`, and the real Var_θ[∂_k C] across initializations
  lives in `qlo.analysis.bp_variance`.
- Only one ansatz family (RY·RZ + CNOT ring/chain); no claim it is representative.
- Parameter-shift is evaluated on an analytic device, so its agreement with
  backprop tests correctness of the estimator, not its finite-shot variance.
- `Hamiltonian` for the local cost is the legacy-named constructor in
  PennyLane 0.45.1 (maps to `LinearCombination`); no deprecation warning is
  emitted, but this is the most likely thing to break on a future upgrade.
- No git repository was initialized (per instructions, no commits).

## Next Scientific Step

**Not implemented yet.** The next step is empirical finite-shot gradient-noise
characterization: for fixed θ, evaluate the parameter-shift gradient on a
seeded `default.qubit` with `shots=N` many times, and compare the estimator's
mean and covariance against the analytic gradient from this stage across
`N`, `n_qubits`, `depth`, and local vs. global cost. That characterization is a
prerequisite for any later statement about "useful" noise, and it must be done
before touching QLO, FDT analogies, or plateau-escape claims.
