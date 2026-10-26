# Project status

Last updated: 26 October 2026.

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
| A1–A4 and the framing decision | Satyabrat Sahu | [principal](principal/QLO_Principal_Track.md) | `principal/a2_numerics` |

## Open

From the principal track §6 and the task reports:

1. **A2 as a proposition with proof.** The identity is two lines; the slope rule needs its stated regime (principal §6
   item 4). B1 supplies the empirical regime check: the gap rule holds to ~1% of b_S, and the residual decomposes
   into an O(S) term plus a difference-of-medians term (B1 §17).
2. **A5:** the update to QuIP Network, kept out of this public repo (principal §6 item 5).
3. **B4: depolarising-noise overlay.** Not started. The A2 regime statement and the B1/B2 reports list noise as
   uncovered.
4. **Manuscript** under the decided framing.

## Known notes

- Principal §6, B1 bullet, writes b_SWAP = b_LE − b_S. §3 derives b_SWAP = b_LE + b_S. B1 tested the plus form, and
  the data agree (B1 §3).
- B5 remaining holes: APS versions of Teo 2023 and Mari 2021, a full read of Sulimov & Lehmann 2026, library
  databases (B5 closure audit §8).
