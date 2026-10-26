"""B1: entangling-ansatz sweeps, an independent empirical test of the principal-track A2 scaling rule.

Modules:
    config      frozen B1 configuration (mirrored verbatim in docs/b1/B1_CONFIG.md)
    circuits    batched numpy statevector simulator for the two entangling families
    quantities  per-theta F_+-, S, Delta, r, g, Q, M_LE, M_SWAP, R, R_identity (log space, explicit flags)
    rx_product  Family 0: the frozen Stage 7 RX-product benchmark run through the B1 per-theta pipeline
    audit       structural-zero audit (independent re-simulation, analytic derivative, PennyLane autograd)
    fits        per-seed slope fits, prediction residuals, concentration and outcome classification
    sign_law    conditional sign-law spot check (exact binomial differences)
    figures     plain scientific figures
"""
