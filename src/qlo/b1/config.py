"""Frozen B1 configuration. ``docs/b1/B1_CONFIG.md`` embeds ``B1Config().to_json()`` verbatim; the driver refuses to run if
the two differ, so the committed config document is the configuration that produced the results."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

import numpy as np

REGIMES = ("d2", "d4", "dn")                     # depth 2, depth 4, depth = n
REGIME_CODE = {"d2": 2, "d4": 4, "dn": 0}        # SeedSequence word; 0 = depth equals n
FAMILY_CODE = {"hea_ring": 1, "rxry_czbrick": 2}
POSITIONS = ("EARLY", "MIDDLE", "LATE")
B1_TAG = 0xB1
AUDIT_TAG = 0xA0D17


def depth_of(regime: str, n: int) -> int:
    return {"d2": 2, "d4": 4, "dn": int(n)}[regime]


def position_layer(label: str, depth: int) -> int:
    """EARLY = first layer, MIDDLE = floor(depth/2), LATE = final layer (qubit 0, first rotation of the layer)."""
    return {"EARLY": 0, "MIDDLE": depth // 2, "LATE": depth - 1}[label]


def position_map(depth: int) -> dict:
    """label -> (layer, qubit, rotation index). At depth 2 MIDDLE and LATE are the SAME parameter (layer 1)."""
    return {lab: (position_layer(lab, depth), 0, 0) for lab in POSITIONS}


def distinct_positions(depth: int) -> dict:
    """label -> position with duplicates removed (the later label of a coincident pair is kept: LATE at depth 2)."""
    out, seen = {}, {}
    for lab, p in position_map(depth).items():
        if p in seen:
            del out[seen[p]]
        out[lab], seen[p] = p, lab
    return out


def control_positions(family: str, depth: int) -> dict:
    """Audit-only positive control: the final-layer RZ on qubit 0 of the repo HEA (expected structural zero)."""
    return {"CONTROL_FINAL_RZ": (depth - 1, 0, 1)} if family == "hea_ring" else {}


@dataclass(frozen=True)
class B1Config:
    # --- seeds (independent of Stage 7 seed 0 and B3 seeds 10000..10019) ---
    seeds: tuple = tuple(range(11_000, 11_010))
    # --- entangling families / depth regimes / n grids ---
    families: tuple = ("hea_ring", "rxry_czbrick")
    regimes: tuple = REGIMES
    n_grid_d2: tuple = (4, 6, 8, 10, 12, 14, 16)
    n_grid_d4: tuple = (4, 6, 8, 10, 12, 14, 16)
    n_grid_dn: tuple = (4, 6, 8, 10, 12, 14)
    samples_per_cell: int = 4_000                 # theta per (family, regime, n, seed); shared by all positions
    positions: tuple = POSITIONS
    rotation_index: int = 0                       # theta[l, 0, 0]: RY (hea_ring), RX (rxry_czbrick)
    # --- structural-zero audit ---
    audit_samples: int = 200
    audit_zero_tol_r: float = 1e-10               # |r| <= tol counts as a numerical zero
    audit_valid_max_zero_fraction: float = 0.01
    audit_min_var_r: float = 1e-20
    audit_agreement_tol: float = 1e-9             # |difference| / S for every gradient / fidelity cross-check
    audit_pennylane: bool = True                  # PennyLane autograd on every audited (family, regime, n)
    # --- RX product regression arm (exact Stage 7 benchmark) ---
    rx_n: tuple = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
    rx_samples: int = 25_000                      # = B3 seed_samples
    rx_stream: int = 20                           # Stage 7 required-shots theta stream (qlo.stage7.analysis.sample_theta)
    rx_component: int = 0
    b3_seeds: tuple = tuple(range(10_000, 10_020))
    b3_regeneration_tol: float = 1e-12
    rx_sanity_tol_bS_bLE_br: float = 0.02         # secondary "approximately" checks only
    rx_sanity_tol_bSWAP: float = 0.04
    # --- per-theta exact shot-ratio identity (implementation check; STOP if violated) ---
    identity_rel_tol: float = 1e-10
    # --- slope fits ---
    rho: float = 1.0                              # SNR target (primary). SNR 2 adds log10 4 to every theta: same slopes
    secondary_n_min: int = 8                      # secondary fit range: n >= 8 of each grid
    # --- intervals (B3 utilities and B3 settings) ---
    n_boot_seed: int = 10_000
    boot_seed: int = 2026
    equivalence_margin: float = 0.02              # decades/qubit, secondary practical-equivalence check
    br_small_fraction: float = 0.10               # doubling test only if |mean b_r| <= 0.10 mean b_S and b_r CI has 0
    # --- concentration classification ---
    conc_r2_min: float = 0.99
    conc_curvature_max: float = 0.25              # |b_S(upper half) - b_S(lower half)| <= 0.25 b_S
    conc_median_S_max: float = 0.1                # median S <= 0.1 at every n for CLEARLY CONCENTRATED
    # --- theta bootstrap (secondary, limited subset) ---
    theta_boot_regime: str = "d4"
    theta_boot_seed_index: int = 0
    theta_boot_reps: int = 2_000
    # --- conditional sign-law spot check (secondary) ---
    sign_n: int = 12
    sign_seed_index: int = 0
    sign_S_quantiles: tuple = (0.10, 0.25, 0.50, 0.75, 0.90)
    sign_shots: tuple = tuple(4**k for k in range(9))     # 1 .. 65536

    def n_grid(self, regime: str) -> tuple:
        return {"d2": self.n_grid_d2, "d4": self.n_grid_d4, "dn": self.n_grid_dn}[regime]

    def fit_ranges(self, n_values) -> dict:
        n_values = tuple(int(n) for n in n_values)
        return {"primary": n_values, "secondary_n_ge_8": tuple(n for n in n_values if n >= self.secondary_n_min)}

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    def sha256(self) -> str:
        return hashlib.sha256(self.to_json().encode()).hexdigest()


def theta_seed(family: str, regime: str, n: int, seed: int) -> np.random.SeedSequence:
    return np.random.SeedSequence([B1_TAG, FAMILY_CODE[family], REGIME_CODE[regime], int(n), int(seed)])


def sample_theta(family: str, regime: str, n: int, seed: int, n_samples: int) -> np.ndarray:
    """theta ~ iid U[-pi, pi], shape (n_samples, depth, n, 2); one stream per (family, regime, n, master seed)."""
    rng = np.random.default_rng(theta_seed(family, regime, n, seed))
    return rng.uniform(-np.pi, np.pi, (int(n_samples), depth_of(regime, n), int(n), 2))


def audit_theta(family: str, regime: str, n: int, n_samples: int) -> np.ndarray:
    rng = np.random.default_rng(np.random.SeedSequence([B1_TAG, AUDIT_TAG, FAMILY_CODE[family], REGIME_CODE[regime], int(n)]))
    return rng.uniform(-np.pi, np.pi, (int(n_samples), depth_of(regime, n), int(n), 2))


def config_json_from_markdown(text: str) -> str:
    """The JSON block between the B1-CONFIG-JSON markers of docs/b1/B1_CONFIG.md."""
    start, end = "<!-- B1-CONFIG-JSON-BEGIN -->", "<!-- B1-CONFIG-JSON-END -->"
    body = text.split(start, 1)[1].split(end, 1)[0]
    return body.strip().removeprefix("```json").removesuffix("```").strip()
