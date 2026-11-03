"""Machine-neutral locations for per-theta caches and smoke-run output.

Resolution order for an experiment's work (cache) directory:
    1. an explicit path (the driver's --work-dir / --b1-work flag);
    2. $QLO_WORK_DIR/<experiment>/ when the QLO_WORK_DIR environment variable is set;
    3. <repo>/.qlo_cache/<experiment>/ (git-ignored).
Smoke (--fast) runs use the experiment name "<experiment>_fast", so their small caches never mix with full-run caches
(cache files are keyed by seed and n, not by sample count).
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENV_VAR = "QLO_WORK_DIR"
CACHE_DIRNAME = ".qlo_cache"


def default_work_root() -> Path:
    env = os.environ.get(ENV_VAR, "").strip()
    return Path(env).expanduser() if env else ROOT / CACHE_DIRNAME


def work_dir(experiment: str, explicit: Path | str | None = None) -> Path:
    return Path(explicit) if explicit is not None else default_work_root() / experiment


def fast_name(experiment: str) -> str:
    return f"{experiment}_fast"


def run_dirs(experiment: str, fast: bool, out: Path | str | None, work: Path | str | None, results: Path) -> tuple[Path, Path]:
    """(output dir, work dir) for a driver run. Full runs write to ``results``; --fast runs write under the fast work
    root so that a smoke run can never overwrite committed results. Explicit paths always win."""
    if fast:
        base = work_dir(fast_name(experiment))
        return Path(out) if out is not None else base / "out", Path(work) if work is not None else base / "work"
    return Path(out) if out is not None else results, work_dir(experiment, work)
