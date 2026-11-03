# Project status

Last updated: 31 October 2026.

## Decided

- **Framing (16 October 2026).** The paper is a measurement and gradient-resolvability paper with a new title.
  - The Langevin apparatus moves to its own track.
  - Stage 4 stays in the paper as the falsified hypothesis.
  - See [`principal/QLO_Principal_Track.md`](principal/QLO_Principal_Track.md) §1.
- **Novelty audit A1, generalisation A2, normalisation A3, positioning A4.** See the principal track, §§2–5.

## Complete

| Item | Owner | Report | Results |
|---|---|---|---|
| Stages 1–7 | Dhruv Jain | [docs/stages/](docs/stages/) | `results/stage2` … `stage7` |
| B3 statistical hardening | Dhruv Jain | [B3](docs/b3/B3_STATISTICAL_HARDENING.md) | `results/b3_hardening` |
| B5 prior-work extraction | Dhruv Jain | [B5 closure audit](docs/b5/B5_CLOSURE_AUDIT.md) | `results/b5_prior_work` |
| B1 entangling-ansatz sweeps | Dhruv Jain | [B1](docs/b1/B1_ENTANGLING_SWEEPS.md) | `results/b1_entangling` |
| B2 additional estimators | Dhruv Jain | [B2](docs/b2/B2_ADDITIONAL_ESTIMATORS.md) | `results/b2_estimators` |
| B4 depolarizing-noise overlay | Dhruv Jain | [B4](docs/b4/B4_NOISE_OVERLAY.md) | `results/b4_noise` |
| A2 propositions with proofs (draft for principal review) | Dhruv Jain | [theory](docs/theory/A2_PROPOSITIONS.md) | — |
| A1–A4 and the framing decision | Satyabrat Sahu | [principal](principal/QLO_Principal_Track.md) | `principal/a2_numerics` |

## Phase 8 (baseline `eaf0728`, 29 October 2026)

| Item | Owner | Record |
|---|---|---|
| I1 Stage 7 wording fixes (random-walk scope; cancellation-free sign-law median) | Dhruv Jain | [I1](docs/phase8/I1_STAGE7_CORRECTIONS.md) |
| I2 portability (repo-local caches, explicit UTF-8, Linux + Windows CI, `--fast` smoke runs) | Dhruv Jain | [reproduction status](docs/phase8/REPRODUCTION_STATUS.md) |

All results so far are classical simulations run on Dhruv's macOS machine. Independent full reproduction (P9 Tiers 2
and 3) and any hardware run are not done yet. See [REPRODUCTION_STATUS](docs/phase8/REPRODUCTION_STATUS.md). Venue
dates are in [VENUE_TRACKER](docs/phase8/VENUE_TRACKER.md); nothing has been submitted.

## Open

1. **Principal review of the propositions** in `docs/theory/A2_PROPOSITIONS.md`. They answer principal §6 item 4;
   the principal track decides the final wording.
2. **A5:** the update to QuIP Network, kept out of this public repo.
3. **Manuscript** under the decided framing. B4 adds a noise section: the identity and the slope rule survive, and
   doubling depends on the noise model.
4. **Optional extensions** (B4 §8): local noise on entangling circuits, other channels, two noisy SWAP copies.

## Known notes

- Principal §6, B1 bullet, writes b_SWAP = b_LE − b_S. §3 derives b_SWAP = b_LE + b_S. B1 tested the plus form, and
  the data agree (B1 §3).
- B5 remaining holes: APS versions of Teo 2023 and Mari 2021, a full read of Sulimov & Lehmann 2026, library
  databases (B5 closure audit §8).
