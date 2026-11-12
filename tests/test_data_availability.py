"""Phase 8 (Shravan section 8 item 4): the data availability statement, and the data behind every figure and table is public."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
STATEMENT = ROOT / "paper" / "drafts" / "data_availability.tex"


def _live(tex: str) -> str:
    return "\n".join(l for l in tex.splitlines() if not l.lstrip().startswith("%"))


def _paper_sources() -> set[str]:
    """Every repository file a paper figure or appendix table is built from."""
    man = json.loads((ROOT / "paper" / "figures" / "manifest.json").read_text(encoding="utf-8"))
    paths = {s["path"] for f in man["figures"] for s in f["sources"]}
    prov = (ROOT / "paper" / "appendix" / "PROVENANCE.md").read_text(encoding="utf-8")
    paths |= set(re.findall(r"<- ((?:docs|results|paper|src)/[^\s:;]+)", prov))
    return paths


def test_statement_names_the_public_repository_and_the_archive():
    s = _live(STATEMENT.read_text(encoding="utf-8"))
    repo = re.search(r'repository-code: "([^"]+)"', (ROOT / "CITATION.cff").read_text(encoding="utf-8")).group(1)
    assert f"\\url{{{repo}}}" in s
    assert "openly available" in s and "FIGURE_SOURCES.md" in s and "classical simulation" in s
    assert "[Zenodo DOI from I7]" in s or re.search(r"10\.5281/zenodo\.\d+", s), "the archive DOI (I7) is missing"


def test_every_figure_and_table_source_is_in_the_repository():
    paths = _paper_sources()
    assert len(paths) > 20
    missing = sorted(p for p in paths if not (ROOT / p).is_file())
    assert not missing, missing


def test_every_figure_and_table_source_is_tracked_not_ignored():
    if not (ROOT / ".git").exists():
        pytest.skip("not a git checkout (for example a source zip)")
    tracked = set(subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                                 check=True).stdout.splitlines())
    untracked = sorted(_paper_sources() - tracked)
    assert not untracked, f"would not be public on publication: {untracked}"
