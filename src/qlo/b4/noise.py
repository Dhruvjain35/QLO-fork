"""Depolarizing-noise overlays (exact) and their density-matrix validation.

Global depolarizing after every layer commutes with the unitaries, so with q = (1 - p)^L the noisy state is
q rho + (1 - q) I / 2^n and every shifted fidelity maps exactly as F' = q F + (1 - q)/2^n.
Local depolarizing on the product circuit keeps the state a product, so F' is a product of per-qubit fidelities
f_j = (1 - p) cos^2(theta_j/2) + p/2. Both are checked against PennyLane default.mixed simulations.
"""

from __future__ import annotations

import itertools

import numpy as np
import pennylane as qml

from qlo.stage5.theory import log_a_k, s_k
from qlo.stage7 import analysis as AN


def global_q(p: float, layers: int) -> float:
    return (1.0 - p) ** layers


def global_overlay(F_plus, F_minus, n: int, q: float) -> tuple[np.ndarray, np.ndarray]:
    floor = (1.0 - q) / 2.0**n
    return q * np.asarray(F_plus) + floor, q * np.asarray(F_minus) + floor


def global_delta(F_plus, F_minus, q: float) -> np.ndarray:
    """Exact Delta' = q (F_- - F_+): the floor cancels analytically, not in floating point."""
    return q * (np.asarray(F_minus) - np.asarray(F_plus))


def rx_noiseless(n: int, n_samples: int, seed: int, stream: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Stage 7 RX-product theta and closed-form F_pm (k = 0), as in the B1 RX arm."""
    th = AN.sample_theta(n, n_samples, seed, stream)
    A, s = np.exp(log_a_k(th, 0)), s_k(th, 0)
    return th, A * (1 - s) / 2, A * (1 + s) / 2


def rx_local(theta: np.ndarray, p: float, k: int = 0, with_delta: bool = False):
    """Exact F_pm for single-qubit depolarizing (strength p) after every RX of the product circuit
    (and, if ``with_delta``, the exact Delta' = prod_{j != k} f_j (1 - p) sin theta_k)."""
    c = np.cos(theta / 2.0) ** 2
    f = (1.0 - p) * c + p / 2.0
    with np.errstate(divide="ignore"):
        log_rest = np.sum(np.log(np.delete(f, k, axis=-1)), axis=-1)
    s = np.sin(theta[..., k])
    rest = np.exp(log_rest)
    fp, fm = rest * ((1 - p) * (1 - s) / 2 + p / 2), rest * ((1 - p) * (1 + s) / 2 + p / 2)
    return (fp, fm, rest * (1 - p) * s) if with_delta else (fp, fm)


# ---- density-matrix validation ---------------------------------------------------------------------------------
def _paulis(n: int) -> list[np.ndarray]:
    P = [np.eye(2), np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.diag([1.0, -1.0])]
    out = []
    for idx in itertools.product(range(4), repeat=n):
        m = np.array([[1.0]])
        for i in idx:
            m = np.kron(m, P[i])
        out.append(m.astype(np.complex128))
    return out


def global_depolarizing_kraus(p: float, n: int) -> list[np.ndarray]:
    """Kraus operators of rho -> (1-p) rho + p I/d via the Pauli twirl: (1-p+p/d^2) rho + (p/d^2) sum_{P != I} P rho P."""
    d2 = 4.0**n
    ps = _paulis(n)
    return [np.sqrt(1 - p + p / d2) * ps[0]] + [np.sqrt(p / d2) * P for P in ps[1:]]


def dm_rx_global(theta: np.ndarray, p: float) -> float:
    n = theta.size
    dev = qml.device("default.mixed", wires=n)
    K = global_depolarizing_kraus(p, n)

    @qml.qnode(dev)
    def circ():
        for j in range(n):
            qml.RX(theta[j], wires=j)
        qml.QubitChannel(K, wires=range(n))
        return qml.probs(wires=range(n))

    return float(circ()[0])


def dm_rx_local(theta: np.ndarray, p: float) -> float:
    n = theta.size
    dev = qml.device("default.mixed", wires=n)

    @qml.qnode(dev)
    def circ():
        for j in range(n):
            qml.RX(theta[j], wires=j)
            qml.DepolarizingChannel(3.0 * p / 4.0, wires=j)        # PennyLane convention: p_PL = 3p/4
        return qml.probs(wires=range(n))

    return float(circ()[0])


def dm_hea_global(params: np.ndarray, p: float) -> float:
    """Repo-layout HEA (RY, RZ + CNOT ring), global depolarizing after every layer."""
    depth, n, _ = params.shape
    dev = qml.device("default.mixed", wires=n)
    K = global_depolarizing_kraus(p, n)
    pairs = [(q, q + 1) for q in range(n - 1)] + [(n - 1, 0)]

    @qml.qnode(dev)
    def circ():
        for l in range(depth):
            for q in range(n):
                qml.RY(params[l, q, 0], wires=q)
                qml.RZ(params[l, q, 1], wires=q)
            for c, t in pairs:
                qml.CNOT(wires=[c, t])
            qml.QubitChannel(K, wires=range(n))
        return qml.probs(wires=range(n))

    return float(circ()[0])


def pure_hea_fidelity(params: np.ndarray) -> float:
    depth, n, _ = params.shape
    dev = qml.device("default.qubit", wires=n)
    pairs = [(q, q + 1) for q in range(n - 1)] + [(n - 1, 0)]

    @qml.qnode(dev)
    def circ():
        for l in range(depth):
            for q in range(n):
                qml.RY(params[l, q, 0], wires=q)
                qml.RZ(params[l, q, 1], wires=q)
            for c, t in pairs:
                qml.CNOT(wires=[c, t])
        return qml.probs(wires=range(n))

    return float(circ()[0])
