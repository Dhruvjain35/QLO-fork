"""Frozen B4 configuration (mirrored as JSON in docs/b4/B4_CONFIG.md; the driver refuses to run if they differ)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class B4Config:
    # same theta populations as B1 (RX arm: Stage 7 stream 20; entangling cells: B1 per-theta caches)
    seeds: tuple = tuple(range(11_000, 11_010))
    rx_n: tuple = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
    rx_samples: int = 25_000
    rx_stream: int = 20
    # noise models and strengths (p = 0 is the noiseless regression control)
    global_p: tuple = (0.0, 1e-4, 1e-3, 1e-2, 1e-1)          # global depolarizing after every layer: q = (1-p)^L
    local_p_rx: tuple = (0.0, 1e-3, 1e-2, 1e-1)                # single-qubit depolarizing after every RX (product circuit)
    rho: float = 1.0
    secondary_n_min: int = 8
    window: int = 3                                           # points per local-slope window (transition profile)
    n_boot_seed: int = 10_000
    boot_seed: int = 2026
    # validation (density-matrix simulation, small n)
    validate_n: tuple = (2, 3)
    validate_local_n: tuple = (2, 3, 4)
    validate_theta: int = 6
    validate_tol: float = 1e-12
    regression_tol: float = 1e-12                             # p = 0 must reproduce the B1 medians
    identity_rel_tol: float = 1e-10

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)

    def sha256(self) -> str:
        return hashlib.sha256(self.to_json().encode()).hexdigest()


def config_json_from_markdown(text: str) -> str:
    body = text.split("<!-- B4-CONFIG-JSON-BEGIN -->", 1)[1].split("<!-- B4-CONFIG-JSON-END -->", 1)[0]
    return body.strip().removeprefix("```json").removesuffix("```").strip()
