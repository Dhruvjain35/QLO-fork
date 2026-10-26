# QLO — measurement cost and gradient resolvability on barren plateaus

[![tests](https://github.com/Satyabrat2005/QLO---Quantum-Langevin-Optimisation/actions/workflows/tests.yml/badge.svg)](https://github.com/Satyabrat2005/QLO---Quantum-Langevin-Optimisation/actions/workflows/tests.yml)

Variational quantum algorithms estimate gradients from a finite number of measurement shots. On a barren plateau
the true gradient is exponentially small, so the question that decides whether training is possible at all is:
**how many shots does a usable gradient cost, and how does that cost depend on the way the fidelity is measured?**

The project began as *Quantum Langevin Optimisation*, which asked whether shot noise could act as useful
Langevin-style exploration on a barren plateau. Stage 4 falsified that hypothesis. Shot noise gave no escape
advantage over exact gradient descent or matched Gaussian noise. The work then turned to the mechanism, finite-shot
gradient resolvability.

On 16 October 2026 the project adopted the measurement framing for the paper
([`principal/QLO_Principal_Track.md`](principal/QLO_Principal_Track.md) §1). The Langevin apparatus moves to a
separate track. The repository name is unchanged.

## Main results

| | Result | Report |
|---|---|---|
| Stage 4 | Finite-shot SGD gives **no** barren-plateau escape advantage over exact GD or covariance-matched Gaussian noise (falsified hypothesis) | [STAGE4](docs/stages/STAGE4.md) |
| Stage 5 | The projector estimator fails by *count starvation*: both shifted counts are usually zero, ĝ ≡ 0, and a resolvable gradient needs ~4^(n−1) shots | [STAGE5](docs/stages/STAGE5.md) |
| Stage 6 | A global-parity cost fails differently, by *random signs* rather than exact zeros, at a similar shot exponent | [STAGE6](docs/stages/STAGE6.md) |
| Stage 7 | **Same landscape, same gradient, different readout:** typical gradient shots grow ~4ⁿ with the Loschmidt / projector readout and ~16ⁿ with the SWAP test | [STAGE7](docs/stages/STAGE7.md) |
| B3 | The Stage 7 slopes survive 20 independent seeds and a θ bootstrap (LE ≈ 0.605, SWAP ≈ 1.20 decades/qubit) | [B3](docs/b3/B3_STATISTICAL_HARDENING.md) |
| A2 (principal) | Exact identity M_SWAP/M_LE = (2−Q)/(S−Q) for any circuit, giving the slope rule b_SWAP = b_LE + b_S; the exponent doubles when the relative gradient does not concentrate | [principal §3](principal/QLO_Principal_Track.md) |
| B1 | Independent test of the A2 rule on two entangling ansätze, depths 2 / 4 / n, early / middle / late parameters. The identity holds on all 6.74 M θ; b_r ≈ 0 everywhere; the exponent ratio is 1.97–2.02; the gap rule holds to ~1% of b_S | [B1](docs/b1/B1_ENTANGLING_SWEEPS.md) |
| B2 | Destructive SWAP reproduces ancilla SWAP exactly. An unbiased Hadamard-test estimator scales like Loschmidt (~4ⁿ) at ~9.5× the executions and fails by random signs | [B2](docs/b2/B2_ADDITIONAL_ESTIMATORS.md) |
| B4 | Depolarizing noise: the exact identity and the general slope rule survive. Global depolarizing breaks exponent doubling: on the product benchmark Loschmidt rises from 4ⁿ to 8ⁿ, SWAP stays at 16ⁿ, and the ratio falls to 4/3. Local depolarizing preserves doubling | [B4](docs/b4/B4_NOISE_OVERLAY.md) |
| Theory | The A2 results as propositions with proofs (identity, slope rule under explicit hypotheses, doubling condition, sign law with O(MS) error), plus noise propositions written before B4 | [theory](docs/theory/A2_PROPOSITIONS.md) |
| B5 | Prior-work evidence audit: 8 papers line-checked, 154 ledger entries, 1,060-record targeted search. Evidence only; the novelty decisions are the principal track's (A1) | [B5](docs/b5/B5_CLOSURE_AUDIT.md) |

Every stage report separates what is established from what is not. Claims are scoped to the circuits and n ranges
actually tested.

## Repository layout

```
principal/            principal track: framing decision, novelty audit (A1), generalisation (A2),
                      normalisation (A3), positioning (A4), standalone A2 numerics
docs/stages/          Stage 1-7 reports (STAGE1_STATUS.md ... STAGE7.md)
docs/b1 ... b5/       task reports and frozen design documents (B1_CONFIG.md, B2_CONFIG.md, B4_CONFIG.md)
docs/theory/          the A2 results as propositions with proofs
src/qlo/
  circuits/ costs/ gradients/ analysis/ benchmarks/   Stage 1-3 foundation (ansatz, costs, verified gradients)
  stage4/ ... stage7/                                  per-stage estimators and analysis
  hardening/                                           B3 interval and seed-replicate utilities
  b1/                                                  B1 entangling-circuit simulator, audit, fits
  b2/                                                  B2 destructive SWAP and Hadamard-test estimators
  b4/                                                  B4 depolarizing-noise overlays and density-matrix checks
  experiments/                                         one driver per stage / task (python -m qlo.experiments.<name>)
tools/                B5 evidence tooling and the reproducible literature search
tests/                pytest suite (all stages and tasks)
results/              committed summary tables and figures per stage / task (no raw arrays)
```

## Setup

Python ≥ 3.12.

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest -W error::DeprecationWarning
```

`research_sources/` (local copies of third-party papers used by the B5 source check) is git-ignored. Without it,
one B5 test is skipped.

## Reproducing results

Every driver writes to `results/<name>/`. The B1 and B2 drivers refuse to run unless their configuration equals the
JSON frozen in `docs/b1/B1_CONFIG.md` / `docs/b2/B2_CONFIG.md`.

| Command | Output | Cost |
|---|---|---|
| `python -m qlo.experiments.stage4` … `stage7` | `results/stage4` … `stage7` | see each stage report |
| `python -m qlo.experiments.b3_hardening --workers 8` | `results/b3_hardening` | ~3 h |
| `python -m qlo.experiments.b1_entangling --workers 6` | `results/b1_entangling` | ~5 CPU-h; caches go to an external disk (`--work-dir`) |
| `python -m qlo.experiments.b2_estimators` | `results/b2_estimators` | ~10 min |
| `python -m qlo.experiments.b4_noise` | `results/b4_noise` | ~30 s (reads the B1 per-θ caches) |
| `python tools/b5_evidence.py --check` | verifies `results/b5_prior_work/evidence.csv` against the ledger | seconds |

## Status

See [STATUS.md](STATUS.md) for what is complete and what is still open.

## Contributors

- **Satyabrat Sahu**: principal track (framing, novelty audit A1, A2 generalisation, A3 normalisation, A4
  positioning).
- **Dhruv Jain**: Stages 1–7 and the delegated track (B1 entangling sweeps, B2 additional estimators, B3
  statistical hardening, B5 prior-work extraction), B4 noise overlay and the propositions write-up.

Parts of the code and reports were produced with an AI coding assistant (Claude). Every numerical claim is backed
by committed code, frozen configurations and tests. See [CITATION.cff](CITATION.cff) to cite the repository.

## License

MIT. See [LICENSE](LICENSE).
