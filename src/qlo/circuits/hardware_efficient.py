"""A minimal, configurable hardware-efficient ansatz (HEA).

Structure (for ``depth`` layers):

    for each layer l in 0..depth-1:
        for each qubit q:  RY(theta[l, q, 0]) RZ(theta[l, q, 1])      # rotation sub-layer
        entangling sub-layer of CNOTs                                  # ring or chain

Parameter tensor shape:  ``(depth, n_qubits, 2)``
Parameter count:         ``p(n, depth) = 2 * n * depth``

Entangling topology:
    * ``"ring"``  : CNOT(q, q+1) for q = 0..n-2, then CNOT(n-1, 0). For n == 2 the
      closing CNOT(1, 0) is still applied (so a 2-qubit ring has two CNOTs).
      For n == 1 no entangler is applied.
    * ``"chain"`` : CNOT(q, q+1) for q = 0..n-2 (open nearest-neighbour line).

This is *one* simple HEA. Nothing here asserts that it exhibits a barren plateau
for any particular (n, depth); that is an empirical question for later stages.

NOTE (Stage 2/3 finding): with the global cost ``Z⊗...⊗Z`` some parameters have an
identically-zero gradient for *all* theta — every last-layer RZ (it commutes with any
Z-product) and last-layer RYs on qubits dropped when the observable is pushed back
through the final CNOT ring. These are structural zeros, not gradient concentration,
so this ansatz is NOT used as the controlled barren-plateau benchmark; see
``qlo.benchmarks.cerezo2021`` and docs/stages/STAGE3.md.
The class holds only immutable configuration — it has no mutable state, and all
randomness for parameter initialization comes from an explicitly passed RNG.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pennylane as qml

ROTATIONS_PER_QUBIT = 2  # RY then RZ


def param_shape(n_qubits: int, depth: int) -> tuple[int, int, int]:
    """Shape of the parameter tensor: ``(depth, n_qubits, 2)``."""
    if n_qubits < 1 or depth < 1:
        raise ValueError("n_qubits and depth must both be >= 1")
    return (depth, n_qubits, ROTATIONS_PER_QUBIT)


def n_params(n_qubits: int, depth: int) -> int:
    """Total number of trainable parameters, ``p(n, depth) = 2 * n * depth``."""
    return int(np.prod(param_shape(n_qubits, depth)))


@dataclass(frozen=True)
class HardwareEfficientAnsatz:
    """Immutable description of the ansatz. Call :meth:`apply` inside a QNode."""

    n_qubits: int
    depth: int
    entangler: str = "ring"

    def __post_init__(self) -> None:
        if self.entangler not in ("ring", "chain"):
            raise ValueError(f"entangler must be 'ring' or 'chain', got {self.entangler!r}")
        param_shape(self.n_qubits, self.depth)  # validates ranges

    # ----- static description -------------------------------------------------
    @property
    def param_shape(self) -> tuple[int, int, int]:
        return param_shape(self.n_qubits, self.depth)

    @property
    def n_params(self) -> int:
        return n_params(self.n_qubits, self.depth)

    @property
    def wires(self) -> list[int]:
        return list(range(self.n_qubits))

    def entangling_pairs(self) -> list[tuple[int, int]]:
        """Ordered list of (control, target) CNOT pairs for one entangling sub-layer."""
        n = self.n_qubits
        if n == 1:
            return []
        pairs = [(q, q + 1) for q in range(n - 1)]
        if self.entangler == "ring":
            pairs.append((n - 1, 0))
        return pairs

    # ----- circuit body ---------------------------------------------------------
    def apply(self, params) -> None:
        """Queue the ansatz gates. ``params`` must have shape ``self.param_shape``.

        Must be called inside a QNode / tape context. Accepts any array-like the
        active PennyLane interface understands (numpy / autograd arrays).
        """
        shape = tuple(qml.math.shape(params))
        if shape != self.param_shape:
            raise ValueError(f"params has shape {shape}, expected {self.param_shape}")
        for layer in range(self.depth):
            for q in range(self.n_qubits):
                qml.RY(params[layer, q, 0], wires=q)
                qml.RZ(params[layer, q, 1], wires=q)
            for c, t in self.entangling_pairs():
                qml.CNOT(wires=[c, t])

    def init_params(self, rng: np.random.Generator) -> np.ndarray:
        """Uniform ``[0, 2π)`` initialization from an explicit RNG (see ``utils.seeding``)."""
        from qlo.utils.seeding import random_params

        return random_params(self.param_shape, rng)
