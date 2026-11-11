# Phase 8 P9: Windows reproduction run

- **Task:** P9 of the Phase 8 allocation (section 6.2), following Dhruv's check sheet of 2 November 2026.
- **Run by:** Satyabrat Sahu, on 9 November 2026, on his own Windows machine.
- **Result:** every frozen experiment (Stage 6, Stage 7, B1, B2, B3, B4) reran and matched the committed results. Four
  differences from the check sheet are listed in section 5. None of them changes a conclusion.
- **What did not change:** nothing under `results/` was touched. All outputs went to a scratch folder `check\`, which is
  not committed.

## 1. Setup

| Item | Value |
|---|---|
| Code | GitHub zip of `main`. On 9 November its `src`, `tests`, `docs`, `tools`, `configs`, `principal`, `paper`, `pyproject.toml`, `README.md` and `STATUS.md` were compared file by file with `main` at `067c120` (merge of PR #10) and found identical. It is not a git checkout. |
| Machine | Windows 11 Home Single Language (10.0.26300), Intel Core i9-13980HX, 32 threads, 15.6 GB RAM |
| Python | 3.13.5, in a fresh `.venv`, installed with `pip install -e ".[dev]"` |
| Packages | PennyLane 0.45.1, pennylane-lightning 0.45.0, NumPy 2.5.4, SciPy 1.18.1, pandas 3.1.1, matplotlib 3.11.2, pytest 9.2.0 |
| `PYTHONUTF8` | Not set |
| `QLO_WORK_DIR` | Not set for the B runs, so caches went to `.qlo_cache\` (see note 4) |

## 2. Commands and wall times

| Run | Command | Wall time |
|---|---|---|
| Tests | `.venv\Scripts\python -m pytest -W error::DeprecationWarning` | 76.5 s |
| Stage 6 | `... -m qlo.experiments.stage6 --workers 8 --out-dir check\stage6` | about 11 min |
| Stage 7 | `... -m qlo.experiments.stage7 --workers 8 --out-dir check\stage7` | about 30 min |
| B1 | `... -m qlo.experiments.b1_entangling --workers 5 --out-dir check\b1` | 1 h 19 min (sweep 4,041 s, 5.60 CPU h) |
| B4 | `... -m qlo.experiments.b4_noise --out-dir check\b4` | 33 s |
| B2 | `... -m qlo.experiments.b2_estimators --out-dir check\b2` | about 4 min |
| B3 | `... -m qlo.experiments.b3_hardening --workers 8 --out-dir check\b3` | 3 h 8 min (11,303 s, from `run_meta.json`) |

The Stage 6, Stage 7 and B2 times are from the first and last output file times, so they are approximate. B1 ran on 5
workers instead of 12 because only about 4 GB of RAM was free at the time. No result depends on the worker count.

## 3. Numbers on the check sheet

| Run | Expected | Got | Status |
|---|---|---|---|
| Tests | 279 passed, 1 skipped | 311 passed, 5 skipped, 0 failed | Differs, note 1 |
| Stage 6 | Parity P_zero levels off at 1/√(πM) = 0.0176 at M = 1024; projector P_zero goes to 1 | 0.01763; projector goes to 1 | Match |
| Stage 7 | Slopes 0.6059 (Loschmidt) and 1.2025 (SWAP), R² ≥ 0.9999 | 0.6059 (R² 0.99994) and 1.2025 (R² 0.99999) | Match |
| Stage 7 | Conditional sign median at n = 20: 0.8527 to 0.8530 | Script prints 0.8533 to 0.8537 (old formula); B3 gives 0.85266 to 0.85299 | Note 2 |
| B1 | Identity error ≤ 1.75e-11; ratio 1.97 to 2.02 in every cell; b_r near 0 | 1.75e-11; ratio 1.9692 to 2.0186; b_r between −0.0029 and +0.0008 | Match, note 3 |
| B4 | Global noise: local Loschmidt slope 0.90, ratio 1.334; local noise b_S = 0.5834, 0.5451, 0.4451 | 0.9016 and 1.3340 (n 16 to 20, p = 0.1); 0.5834, 0.5451, 0.4451 | Match |
| B2 | Loschmidt 0.6059, both SWAPs 1.2025, Hadamard 0.6066 | Same | Match |
| B3 | 20-seed means: Loschmidt about 0.605, SWAP about 1.201 | 0.6053 and 1.2014 | Match |

## 4. Comparison with the committed result files

Every output table was compared with the committed file of the same name. Unless listed here, all numbers agree to
about 1e-10 relative or better, and every text column is identical.

| Run | Differences found | Why |
|---|---|---|
| Stage 6 | `direction_probability_validation.csv`: 6 of 90 rows use a different sample at the "median abs(g)" label | Most likely a near tie in choosing the median sample. Coverage is unchanged: P_zero 83/90 and P_correct 81/90 in the Wilson CI, max abs(z) 2.88, as in the committed run. |
| Stage 7 | `paired_estimator_comparison.csv`: the `paired_frac_swap_higher_*` columns differ by up to 0.0036 in 11 of 30 rows | These count θ where one probability is strictly above another; where both are about 1, rounding decides the comparison. |
| Stage 7 | Same file: `loschmidt_median_p_correct_given_nonzero` differs by up to 5.8e-5 in 3 rows | The old subtraction formula of note 2. |
| Stage 7 | `paired_required_shots_subsample.csv.gz`: 4 of 20,000 values differ by up to 3.3e-7 relative | Rounding in the root search |
| B1 | `ratio_identity_validation.csv`: `max_abs_err` 2.56e18 at RX n = 20 (committed: 296) | An absolute error on a value above 1e32. The relative error is unchanged at 1.75e-11. |
| B1 | `conditional_sign_summary.csv`: 63 of 720 rows use a different θ at a predeclared S quantile | The code takes the θ closest to the quantile, so near ties can resolve differently. The summary errors are identical (4.84e-4 where M·S ≤ 0.01, 0.328 overall). |
| B2 | `fixed_budget_failure_modes.csv`: 1 of 96 rows differs by 3.3e-4 in the Loschmidt P(correct given nonzero) | Precision of the conditional probability, not traced further |
| B3 | `fixed_shot_summary.csv` and `sign_law_summary.csv`: the Stage 7 method conditional sign values differ by up to 3.4e-4 | Old subtraction formula. The cancellation-free values agree to 3e-16. |
| B3 | `stage7_interval_check.csv`: the SWAP P_nz slope flips to "outside" | Its interval has zero width, so the flag depends on float equality in the last digit. B3 §16 already notes this. |
| B3 | `numerical_nonmonotone_rows.csv`: 98 rows (committed: 99) | Diagnostic list of rounding cases |
| B4 | None beyond 2.2e-13 absolute | With p = 0 it reproduces this run's B1 medians to 5.68e-14 |

Files present in the committed folders but not written by these runs: `results/b1_entangling/fused_kernel_validation.csv`
and `results/b3_hardening/CI_METHODS.md`. Both are committed documentation, not outputs of the frozen runs.

## 5. The four notes sent to Dhruv

1. **Test count.** 311 passed and 5 skipped instead of 279 and 1, because the code is a newer commit than the sheet's
   `3c54801`. Four of the five skips need git history, which a zip download does not have (B1 base commit, methods
   tables baseline, two Phase 8 portability checks). The fifth needs the prior-work PDFs, as on the sheet.
2. **Stage 7 sign median.** The Stage 7 script still computes the conditional sign median with the old subtraction
   formula and prints 0.8533 to 0.8537. The cancellation-free median from B3 at n = 20 is 0.85266 to 0.85299 for M up
   to 16,384, which matches the corrected 0.8527 to 0.8530. The old formula even differs between machines at M = 64:
   0.85366 here against 0.85372 committed.
3. **B1 ratio range.** 3 of the 32 B1 ratios sit just under 1.97 (lowest 1.9692), exactly as in the committed results.
   The range is 1.969 to 2.02, not 1.97 to 2.02.
4. **Cache folder.** This machine has no D: drive, so `QLO_WORK_DIR = "D:\qlo"` made B1 stop when it tried to create the
   folder. With the variable unset, the caches went to `.qlo_cache\` and B4 found the B1 caches there automatically.

## 6. What this does and does not establish

- The committed results of Stage 6, Stage 7 and B1 to B4 now rest on two machines: Dhruv's macOS machine and this
  Windows 11 machine, with different operating systems and newer NumPy and pandas versions.
- Both runs use the same frozen configurations and seeds. This shows the code reproduces its results; it is not new
  statistical evidence. B3 remains the source of the seed-to-seed intervals.
- Every run is a classical simulation. Nothing has run on quantum hardware.
- The `check\` outputs (143 files, 17.1 MB) are kept on the run machine and are not committed.
