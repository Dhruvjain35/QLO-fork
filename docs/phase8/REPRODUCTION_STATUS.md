# Reproduction status

Last updated: 11 November 2026 (Phase 8 P9 follow-ups).

This page separates four different kinds of evidence. They are easy to blur, and only the first three exist today.

| | Kind of evidence | Status |
|---|---|---|
| A | Original result generation (classical simulation, Dhruv's macOS machine) | **Done.** Every committed result. |
| B | Automated cross-platform testing (GitHub Actions) | **Done** for the test suite and smoke runs on Linux 3.12, Linux 3.13 and Windows 3.13 (first run on PR #8). |
| C | Full-experiment reproduction on a second machine | **Done** by a co-author on Windows 11 (P9, 9 November 2026). Not reproduced by anyone outside the team. |
| D | Quantum hardware | **Not done.** Every result so far is a simulation. |

**Do not describe any result in this repository as validated on quantum hardware.** That has not happened. The full
experiments may be described as reproduced on two machines in simulation; do not describe them as reproduced by an
outside group, because both runs were made by members of the team.

## A. Original result generation

The original scientific results were **actually executed** as classical simulations on Dhruv's macOS machine.
- **Hardware model.** The B1 run log (`results/b1_entangling/numerics_log.md`) specifically identifies that machine
  as an Apple M4. The historical logs and reports for the other experiments record macOS, but do not identify the
  hardware model.
- **Software.** Python with NumPy, SciPy and PennyLane (`default.qubit` and `default.mixed`), computing exact or
  sampled measurement statistics. These are not physical quantum-processor runs.

The run logs are committed next to the results:

| Task | Run log / record | What it records |
|---|---|---|
| B1 entangling sweeps | [`results/b1_entangling/numerics_log.md`](../../results/b1_entangling/numerics_log.md) | Timestamped runs on 7 October 2026 (17:18 to 19:54 CDT) at git `735a8df`, config sha256 `2b7306ae…`. The audit took 704 s. The sweep was restarted several times because the machine was under heavy external memory and load pressure (swap 9.4 / 10 GB, load about 125; logged at 17:44 and 17:56). The completed sweep had 400 tasks (313 computed, 87 cached), 5.03 CPU-hours of compute and 418 s final wall time. The identity check covers 6.74 million θ rows (max relative error 1.75 × 10⁻¹¹, 0 excluded). |
| B2 additional estimators | [`results/b2_estimators/numerics_log.md`](../../results/b2_estimators/numerics_log.md) | Timestamped validate, rx, fixed, spot and figures runs on 7 October 2026 (20:26 to 20:32 CDT), config sha256 `9dc965c2…`. Destructive-SWAP and Hadamard circuit validation is accurate to ≤ 7 × 10⁻¹⁶. The Stage 7 regression matches to 1.78 × 10⁻¹⁵ over 40 cells. The RX phase took 34 s and the entangling spot check 47 s. The log also notes one figure-budget change, made because of memory and recorded as illustration-only. |
| B3 statistical hardening | [`results/b3_hardening/run_meta.json`](../../results/b3_hardening/run_meta.json), [B3 report, Reproduce](../b3/B3_STATISTICAL_HARDENING.md) | The full computation took 3.2 h wall on 8 workers, on a heavily shared machine (load average 50 to 150). The final (cached) analysis pass took 1,383 s. Stage 7 is reproduced to 3.6 × 10⁻¹⁵ over 100 cells. Results committed 9 October 2026. B3 has no per-run timestamp log. |
| B4 noise overlay | [`results/b4_noise/numerics_log.md`](../../results/b4_noise/numerics_log.md) | Two timestamped runs on 26 October 2026 (18:16 and 18:17 CDT), config sha256 `77e9e93a…`. 204 density-matrix checks agree to 5.08 × 10⁻¹⁴. The B1 per-θ caches were read from an external drive. 41.2 million noisy θ settings were analysed (identity max relative error 1.75 × 10⁻¹¹, 0 excluded after the precision fix). p = 0 reproduces the B1 medians to 3.55 × 10⁻¹⁵ on 1,160 rows. Execution took 30 s and 28 s. |
| Stages 2–7 | each `docs/stages/STAGE*.md` and `results/stage*/` | Produced on the same machine. Configurations and seeds are committed with each result. |

## B. Automated cross-platform testing

GitHub Actions runs on independent machines, but it checks **code and formulas** (the pytest suite: estimators,
closed forms, frozen configurations, regressions against committed results, history guards). Before this PR it did
not rerun the full experiments.

| Run | Environment | Result |
|---|---|---|
| `main` at `eaf0728`, run 40870964156, 29 October 2026 | ubuntu-latest, Python 3.12.15 | 267 passed, 1 skipped |

**Matrix added by Phase 8 I2** (`.github/workflows/tests.yml`, no `PYTHONUTF8` setting anywhere):

| Job | ubuntu-latest / 3.12 | ubuntu-latest / 3.13 | windows-latest / 3.13 |
|---|---|---|---|
| `pytest`: full suite, `-W error::DeprecationWarning` | yes | yes | yes |
| `smoke`: `b1_entangling --fast`, `b2_estimators --fast`, `b3_hardening --fast` and `b4_noise --fast` exactly as written (no folder flags), then `git diff --exit-code` | yes | yes | yes |

The smoke runs use reduced, **unfrozen** configurations and write only under `.qlo_cache/<experiment>_fast/`. They
prove that the drivers start, find their folders, handle text as UTF-8 and finish on each platform. They do **not**
reproduce the scientific numbers. The B2 smoke run keeps the full 100,000-θ Stage 7 population at n = 2–10, so its
exact Stage 7 regression gate still runs. B4's smoke run checks p = 0 against the B1 smoke medians.

First run of this matrix: run 41246198763, PR #8 at `7d7826d`, 31 October 2026. All six jobs succeeded.

| Job | Environment | Result |
|---|---|---|
| pytest | ubuntu-latest, Python 3.12.15 | 279 passed, 1 skipped |
| pytest | ubuntu-latest, Python 3.13.17 | 279 passed, 1 skipped |
| pytest | windows-latest, Python 3.13.16 | 279 passed, 1 skipped (no `PYTHONUTF8`) |
| smoke | ubuntu-latest / 3.12, ubuntu-latest / 3.13, windows-latest / 3.13 | all four `--fast` runs finished; no committed file changed |

## C. Full-experiment reproduction on a second machine

**Done.** Satyabrat reran every frozen experiment (Stage 6, Stage 7, B1, B2, B3 and B4 at their frozen configurations
and seeds) on his own machine on 9 November 2026, and every number on the check sheet matched the committed results.
The full run log is [`P9_WINDOWS_REPRODUCTION.md`](P9_WINDOWS_REPRODUCTION.md).

| | Original runs (A) | Second machine (P9) |
|---|---|---|
| Machine | Dhruv's macOS machine | Windows 11, Intel Core i9-13980HX, 32 threads, 15.6 GB RAM |
| Python, PennyLane | as recorded in each run log | Python 3.13.5, PennyLane 0.45.1 (NumPy 2.5.4, pandas 3.1.1) |
| Code | the commit recorded with each result | `main` at `067c120` (zip, compared file by file) |
| Tests | n/a | 311 passed, 5 skipped, 0 failed, no `PYTHONUTF8` |

Wall times on the second machine: Stage 6 about 11 min, Stage 7 about 30 min, B1 1 h 19 min (5 workers), B4 33 s, B2
about 4 min, B3 3 h 8 min.

What the run log reports beyond the check sheet:
- **Stage 7 sign median.** The Stage 7 script still computes the conditional sign median with the original
  subtraction formula and prints 0.8533 to 0.8537 at n = 20. That printout and the
  `loschmidt_median_p_correct_given_nonzero` column of `results/stage7/paired_estimator_comparison.csv` are
  **superseded** by the cancellation-free median in `results/b3_hardening/sign_law_summary.csv`, 0.8527 to 0.8530 for
  M up to 16,384 (B3 D2, Phase 8 I1). The script now prints this note under the table. The old formula even differs
  between the two machines at M = 64 (0.85366 against 0.85372); the cancellation-free values agree to 3e-16.
- **B1 ratio range.** The 34 observed SWAP/Loschmidt exponent ratios run from 1.9692 to 2.0186 on both machines. The
  README and the B1 report now say 1.969–2.019 instead of the rounded 1.97–2.02.
- **Other differences** are all near-ties or float rounding (sample choice at a quantile, strict comparisons near 1,
  a zero-width interval flag); the run log lists each one with its cause. None changes a conclusion.

What this does and does not establish:
- The committed results of Stage 6, Stage 7 and B1 to B4 rest on two machines with different operating systems and
  library versions.
- Both runs use the same frozen configurations and seeds. This shows the code reproduces its results; it is not new
  statistical evidence. B3 remains the source of the seed-to-seed intervals.
- Both runs were made by members of the team. Nobody outside the team has rerun the experiments.

Caches go to `.qlo_cache/<experiment>/`, or to `%QLO_WORK_DIR%\<experiment>` if that variable is set (it must point to
a folder that exists or can be created). `--work-dir` / `--b1-work` override both. To keep the committed results
untouched, every driver accepts `--out-dir`.

## D. Quantum hardware

**Not yet done.** Every number in this repository comes from classical simulation. Hardware noise is represented
only by the simulated depolarizing models of B4.
- Section 6.3 of the Phase 8 allocation is a **proposed** small hardware validation (RX product, n = 2–6, Loschmidt
  and destructive SWAP, about 2 million shots). It depends on QuIP Network (P6) and has not been requested, scheduled
  or run.
- Until it runs and its results are committed, the paper and any poster or abstract must say the results are from
  simulation.
