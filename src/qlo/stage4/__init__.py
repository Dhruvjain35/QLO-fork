"""Stage 4: falsification-first test of finite-shot stochastic escape on the verified
Cerezo-2021 global barren plateau. See docs/stages/STAGE4.md.

Modules
-------
landscape   exact fidelity / cost / gradient / shifted fidelities / wrapping (NumPy only)
shots       exact finite-shot projector estimator (Binomial draws) + conditional shot variance
methods     update rules A-E (exact GD, finite-shot SGD, matched Gaussian, constant Langevin, noise-only)
trajectory  harness: runs a method, records OFFLINE exact metrics the optimizer never sees
seeds       tuning / evaluation start-seed sets and noise-seed derivation
"""
