"""Controlled literature benchmarks with known gradient-variance scaling.

These are deliberately separate from the Stage 1 hardware-efficient ansatz,
which has structurally-zero gradient components (see docs/stages/STAGE3.md) and is
therefore not a clean barren-plateau benchmark.
"""

from qlo.benchmarks import cerezo2021

__all__ = ["cerezo2021"]
