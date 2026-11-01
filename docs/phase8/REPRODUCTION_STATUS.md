# Reproduction status

Last updated: 31 October 2026 (Phase 8 I2).

This page separates four different kinds of evidence. They are easy to blur, and only the first two exist today.

| | Kind of evidence | Status |
|---|---|---|
| A | Original result generation (classical simulation, Dhruv's macOS machine) | **Done.** Every committed result. |
| B | Automated cross-platform testing (GitHub Actions) | **Done** for the test suite and smoke runs on Linux 3.12, Linux 3.13 and Windows 3.13 (first run on PR #8). |
| C | Independent full-experiment reproduction on another machine | **Not done.** Principal track P9, Tiers 2 and 3. |
| D | Quantum hardware | **Not done.** Every result so far is a simulation. |

**Do not describe any result in this repository as validated on quantum hardware, and do not describe the full
experiments as independently reproduced.** Neither has happened yet.

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

## C. Independent full-experiment reproduction

**Not yet done.** No full experiment (Stage 6, Stage 7, B1, B2, B3 or B4 at its frozen configuration) has been rerun
on a second machine.
- Satyabrat's Windows 11 machine (Python 3.13.5, PennyLane 0.45.1) has so far run only **Tier 1**, the test suite: on
  29 October 2026 it gave 264 passed, 3 failed and 1 skipped. The 3 failures were the cp1252 text-encoding issue that
  I2 fixes.
- **Tier 2** (Stage 6 and Stage 7 headline results) and **Tier 3** (B1, B2, B3, B4 at their frozen configurations) are
  principal-track item **P9** in the Phase 8 allocation (§6.2), not yet run.

After I2, Tier 3 no longer needs folder flags. Caches go to `.qlo_cache/<experiment>/`, or to
`%QLO_WORK_DIR%\<experiment>` if that variable is set. `--work-dir` / `--b1-work` still override both. To keep the
committed results untouched, `b2_estimators` and `b4_noise` now also accept `--out-dir`.

## D. Quantum hardware

**Not yet done.** Every number in this repository comes from classical simulation. Hardware noise is represented
only by the simulated depolarizing models of B4.
- Section 6.3 of the Phase 8 allocation is a **proposed** small hardware validation (RX product, n = 2–6, Loschmidt
  and destructive SWAP, about 2 million shots). It depends on QuIP Network (P6) and has not been requested, scheduled
  or run.
- Until it runs and its results are committed, the paper and any poster or abstract must say the results are from
  simulation.
