"""Frozen B2 configuration (mirrored verbatim as JSON in docs/b2/B2_CONFIG.md; the driver refuses to run if they differ)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

ESTIMATORS = ("loschmidt", "swap_ancilla", "swap_destructive", "hadamard_u")
EXECUTIONS_PER_M = {"loschmidt": 2, "swap_ancilla": 2, "swap_destructive": 2, "hadamard_u": 4}   # per gradient component


@dataclass(frozen=True)
class B2Config:
    estimators: tuple = ESTIMATORS
    rx_n: tuple = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
    stage7_seed: int = 0                       # the Stage 7 theta population (primary table)
    stage7_samples: int = 100_000              # = Stage 7 n_samples
    req_stream: int = 20                       # Stage 7 required-shots theta stream
    replicate_seeds: tuple = tuple(range(12_000, 12_010))   # slope uncertainty; disjoint from Stage 7, B3, B1
    replicate_samples: int = 25_000
    rho_primary: float = 1.0
    rho_secondary: float = 2.0
    fit_ranges: tuple = (("primary_2_20", 2, 20), ("n_ge_8", 8, 20))
    n_boot_seed: int = 10_000
    boot_seed: int = 2026
    # fixed-budget failure modes
    budgets_total_executions: tuple = (32, 128, 512, 2048, 8192, 32768)
    fixed_n: tuple = (6, 10, 14, 18)
    fixed_stream: int = 30                     # Stage 7 fixed-shot theta stream
    fixed_samples: int = 2_000                 # LE / SWAP / destructive SWAP (exact)
    fixed_samples_hadamard: int = 300          # first 300 of the same theta (exact enumeration / Monte Carlo)
    hadamard_exact_max_m: int = 512            # exact enumeration up to M_internal = 512, Monte Carlo above
    hadamard_mc_reps: int = 20_000
    mc_seed: int = 2027
    # validation
    circuit_tol: float = 1e-12
    swap_equality_tol: float = 1e-12
    variance_tol: float = 1e-12
    validation_shots: tuple = (64, 256, 1024)
    hadamard_validation_m: tuple = (2, 3, 4, 8, 16, 64, 256)
    hadamard_exact_validation_max_m: int = 256
    validation_mc_reps: int = 200_000
    # secondary entangling spot check (only after the RX analysis)
    spot_n: tuple = (6, 8, 10, 12)
    spot_samples: int = 2_000
    spot_seed: int = 13_000

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)

    def sha256(self) -> str:
        return hashlib.sha256(self.to_json().encode()).hexdigest()


def config_json_from_markdown(text: str) -> str:
    body = text.split("<!-- B2-CONFIG-JSON-BEGIN -->", 1)[1].split("<!-- B2-CONFIG-JSON-END -->", 1)[0]
    return body.strip().removeprefix("```json").removesuffix("```").strip()
