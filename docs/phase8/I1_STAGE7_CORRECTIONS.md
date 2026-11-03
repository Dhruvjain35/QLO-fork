# Phase 8 I1: Stage 7 wording corrections

- **Task:** I1 of the Phase 8 work allocation (baseline `main` at `eaf0728`, 29 October 2026).
- **What changed:** two corrections that B3 and B5 had flagged but Stage 7 never applied.
- **What did not change:** no Stage 7 experiment was rerun or altered. The Stage 7 code (`src/qlo/stage7/`), results
  (`results/stage7/`) and every other number in `docs/stages/STAGE7.md` are unchanged.

## 1. Random-walk statement: scope added

**Original** (`STAGE7.md` §18, with the same claim in §17 and §20 F):

> Trajectory level (§17): SWAP-estimated GD at n ≥ 10 is statistically indistinguishable from a signal-free random walk
> under polynomial shots.

**Corrected:**

> Trajectory level (§17): for the typical start (initial fidelity below the median), SWAP-estimated GD at n ≥ 10 is
> statistically indistinguishable from a signal-free random walk under polynomial shots. Starts in the high-fidelity
> tail keep a small but resolved directional signal (B3 D1, B5 PI-3; scope added in Phase 8 I1).

The random-walk finding stays in the report. Only its scope is narrowed.

| Location in `STAGE7.md` | Change |
|---|---|
| §17, n ≥ 10 bullet | Added a *Scope* sub-bullet after "SWAP GD moves but is a random walk". |
| §18, "Trajectory level" paragraph | Qualified as above. |
| §20 F | "SWAP a random walk (control-matched)" is now limited to the typical start, with the high-fidelity-tail exception. |

**Evidence:**
- [B3 §13](../b3/B3_STATISTICAL_HARDENING.md) (1,000 paired starts per n), stratified by starting fidelity:
  - starts with F₀ below the median are consistent with the signal-free walk;
  - starts above the median keep a resolved residual signal;
  - in the top 10% of F₀, SWAP tracks exact GD.
- [B3 §16 D1](../b3/B3_STATISTICAL_HARDENING.md): the discrepancy as recorded.
- [B5 PI-3](../b5/B5_POTENTIAL_ISSUES.md): the prior-work statement is probabilistic over initialisations, while Stage 7
  stated it without that qualifier.

**Left as they were:**
- §3 and §19. They describe what prior work (Aghaei Saem et al.) shows, not a Stage 7 result.
- `README.md`. The README paragraph that PI-3 flagged ("SWAP-driven GD at n ≥ 10 is indistinguishable from a
  signal-free random walk", in `README.md` at `00c8550`) was removed when PR #5 rewrote the README. The current
  `README.md` and `STATUS.md` make no random-walk statement, so they needed no change.

## 2. Conditional sign-law median at n = 20: cancellation-free value

**Original** (`STAGE7.md` §9):

> **Observed at n = 20: 0.8533–0.8537 for every M.**

**Corrected:**

> **Observed at n = 20: 0.8527–0.8530 for every M.**

A correction note directly below it gives the original value and the reason for the change.

**Evidence:** [B3 §16 D2](../b3/B3_STATISTICAL_HARDENING.md).
- Stage 7 computed P(correct | ĝ ≠ 0) by subtracting from about 1. Deep in the dead zone that keeps only a few digits.
- B3 reproduces 0.8533–0.8537 exactly with the Stage 7 formula, and gets 0.8527–0.8530 when both tails are summed
  directly.
- The conclusion is unchanged. B3 §10 shows that the cancellation-free median equals the same sample's median of
  (1 + |s|)/2 to five digits.

**For the principal (not changed here).** §20 C still says the sign law is "matched to 4 digits (§9)" against the
population value 0.8536. With the corrected median, the agreement with 0.8536 is about 3 digits. The tighter match in
B3 §10 compares against the same sample's prediction instead. I1 is limited to the two corrections above, so the
wording of §20 C is left for the principal track to decide.

## 3. Files modified

| File | Change |
|---|---|
| `docs/stages/STAGE7.md` | The four text edits above. Nothing else. |
| `docs/phase8/i1_stage7_patch.json` | The exact edits, as (old, new) text pairs against `STAGE7.md` at `00c8550`. |
| `tests/test_b1_entangling.py` | The history guard now accepts `STAGE7.md` only if it equals the base file with exactly these edits applied. STAGE2–6 are still compared byte for byte. |
| `docs/phase8/I1_STAGE7_CORRECTIONS.md` | This record. |

## 4. Statement

No underlying Stage 7 experiment was rerun, re-seeded or altered for I1. Both corrections are documentation-only.
They apply results already committed in B3 (`results/b3_hardening/`) and evidence already recorded in B5. The guard
test (`test_historical_files_untouched_since_b1_base`) still requires every Stage 7 result file and every Stage 5–7 /
B3 source file to be byte-identical to `00c8550`.
