"""Phase 8 I2: portable cache paths, explicit UTF-8 text I/O, smoke-mode path handling, and guards showing that no
committed result or frozen configuration changed."""

from __future__ import annotations

import ast
import json
import subprocess
from dataclasses import asdict
from pathlib import Path

import pytest

from qlo import paths as P
from qlo.b1 import config as B1CF
from qlo.b2 import config as B2CF
from qlo.b4 import config as B4CF
from qlo.experiments import b1_entangling as D1
from qlo.experiments import b2_estimators as D2
from qlo.experiments import b3_hardening as D3
from qlo.experiments import b4_noise as D4
from qlo.experiments.stage7 import Stage7Config

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "eaf0728"      # upstream main when Phase 8 started (29 October 2026)
ODD = "work dir with spaces ü"   # spaces (as on the old external drive) and a non-ASCII character


@pytest.fixture
def no_env(monkeypatch):
    monkeypatch.delenv(P.ENV_VAR, raising=False)


# 1-3. resolution order -----------------------------------------------------------------------------------------------
def test_default_work_dir_is_repo_local_and_platform_neutral(no_env):
    w = P.work_dir("b1_entangling")
    assert w == P.ROOT / ".qlo_cache" / "b1_entangling"
    assert w.parts[-2:] == (".qlo_cache", "b1_entangling")
    assert P.ROOT == ROOT
    assert ".qlo_cache/" in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()


def test_env_var_overrides_default(monkeypatch, tmp_path):
    monkeypatch.setenv(P.ENV_VAR, str(tmp_path / ODD))
    assert P.work_dir("b3_hardening") == tmp_path / ODD / "b3_hardening"
    assert P.run_dirs("b2_estimators", True, None, None, ROOT / "results" / "b2_estimators") == (
        tmp_path / ODD / "b2_estimators_fast" / "out", tmp_path / ODD / "b2_estimators_fast" / "work")


def test_explicit_path_overrides_env_and_default(monkeypatch, tmp_path):
    monkeypatch.setenv(P.ENV_VAR, str(tmp_path / "env"))
    explicit = tmp_path / "explicit"
    assert P.work_dir("b1_entangling", explicit) == explicit
    res = ROOT / "results" / "b1_entangling"
    assert P.run_dirs("b1_entangling", False, None, explicit, res) == (res, explicit)
    assert P.run_dirs("b1_entangling", True, tmp_path / "o", explicit, res) == (tmp_path / "o", explicit)


def test_fast_runs_never_default_to_committed_results(no_env):
    for exp in ("b1_entangling", "b2_estimators", "b3_hardening", "b4_noise"):
        res = ROOT / "results" / exp
        out, work = P.run_dirs(exp, True, None, None, res)
        assert res not in (out, *out.parents) and work != P.work_dir(exp)
        assert P.run_dirs(exp, False, None, None, res)[0] == res


# 6. drivers resolve their folders through qlo.paths (phases stubbed; a path with spaces and a non-ASCII character) -----
def test_b1_driver_folders(monkeypatch, tmp_path):
    seen = []
    monkeypatch.setattr(D1, "phase_audit", lambda cfg, out, work, workers, log: seen.append((out, work)))
    monkeypatch.setenv(P.ENV_VAR, str(tmp_path / ODD))
    D1.main(["--fast", "--phase", "audit"])
    D1.main(["--fast", "--phase", "audit", "--work-dir", str(tmp_path / "w")])
    monkeypatch.delenv(P.ENV_VAR)
    monkeypatch.setattr(P, "ROOT", tmp_path)
    D1.main(["--phase", "audit", "--out-dir", str(tmp_path / "full")])
    fast = tmp_path / ODD / "b1_entangling_fast"
    assert seen == [(fast / "out", fast / "work"), (fast / "out", tmp_path / "w"), (tmp_path / "full", tmp_path / ".qlo_cache" / "b1_entangling")]
    cfg = json.loads((fast / "out" / "config.json").read_text(encoding="utf-8"))
    assert cfg["config_sha256"] == "smoke (not frozen)" and (fast / "out" / "numerics_log.md").exists()


def test_b2_driver_folders(monkeypatch, tmp_path):
    monkeypatch.setattr(D2, "OUT", D2.OUT)
    monkeypatch.setattr(D2, "phase_validate", lambda cfg: None)
    monkeypatch.setenv(P.ENV_VAR, str(tmp_path / ODD))
    D2.main(["--fast", "--phase", "validate"])
    assert D2.OUT == tmp_path / ODD / "b2_estimators_fast" / "out"
    assert "## run" in (D2.OUT / "numerics_log.md").read_text(encoding="utf-8")
    D2.main(["--phase", "validate", "--out-dir", str(tmp_path / "full")])          # full run: frozen-config check passes
    assert D2.OUT == tmp_path / "full"
    assert json.loads((D2.OUT / "config.json").read_text(encoding="utf-8"))["config_sha256"] == B2CF.B2Config().sha256()


def test_b4_driver_folders(monkeypatch, tmp_path):
    for name in ("OUT", "B1_RESULTS", "B1"):
        monkeypatch.setattr(D4, name, getattr(D4, name))
    seen, b1_runs = [], []
    monkeypatch.setattr(D4, "phase_validate", lambda cfg: None)
    monkeypatch.setattr(D4, "phase_rx", lambda cfg: ([], []))
    monkeypatch.setattr(D4, "phase_ent", lambda cfg, b1_work: seen.append(b1_work) or ([], []))
    monkeypatch.setattr(D4, "phase_analyse", lambda cfg, m, i: None)
    monkeypatch.setattr(D1, "main", lambda argv=None: b1_runs.append(argv))
    monkeypatch.setenv(P.ENV_VAR, str(tmp_path / ODD))
    D4.main(["--fast"])
    assert b1_runs == [["--fast", "--workers", "2"]]                               # no B1 smoke caches yet -> runs B1 --fast
    assert seen[-1] == tmp_path / ODD / "b1_entangling_fast" / "work"
    assert D4.OUT == tmp_path / ODD / "b4_noise_fast" / "out" and D4.B1_RESULTS == tmp_path / ODD / "b1_entangling_fast" / "out"
    D4.main(["--out-dir", str(tmp_path / "full")])
    assert seen[-1] == tmp_path / ODD / "b1_entangling" and D4.OUT == tmp_path / "full"
    assert D4.B1 == B1CF.B1Config() and D4.B1_RESULTS == D4.B1_RESULTS_DIR
    D4.main(["--out-dir", str(tmp_path / "full"), "--b1-work", str(tmp_path / "b1")])
    assert seen[-1] == tmp_path / "b1"


# 4. no machine-specific defaults ---------------------------------------------------------------------------------------
def test_no_hard_coded_external_drive_paths_in_runtime_source():
    hits = [str(p.relative_to(ROOT)) for p in (ROOT / "src").rglob("*.py")
            if "/Volumes/" in p.read_text(encoding="utf-8") or "SSD Disk" in p.read_text(encoding="utf-8")]
    assert hits == []
    for mod in (D1, D3, D4):
        assert not hasattr(mod, "DEFAULT_WORK") and not hasattr(mod, "DEFAULT_B1_WORK")


# 5. every text-mode open() / read_text() / write_text() in this repository's code names its encoding --------------------
def _unencoded_text_io(path: Path) -> list[str]:
    out = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if not isinstance(node, ast.Call):
            continue
        f, kws = node.func, {k.arg for k in node.keywords}
        name = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None
        if "encoding" in kws:
            continue
        if name == "open":
            mode = node.args[1].value if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) else next(
                (k.value.value for k in node.keywords if k.arg == "mode" and isinstance(k.value, ast.Constant)), "r")
            if "b" not in mode:
                out.append(f"{path.name}:{node.lineno} open")
        elif (name == "read_text" and not node.args) or (name == "write_text" and len(node.args) == 1):
            out.append(f"{path.name}:{node.lineno} {name}")
    return out


def test_text_io_names_utf8_explicitly():
    files = [p for d in ("src", "tests", "tools") for p in (ROOT / d).rglob("*.py")]
    assert len(files) > 50
    assert [hit for p in files for hit in _unencoded_text_io(p)] == []


def test_utf8_scan_catches_a_missing_encoding(tmp_path):
    bad = tmp_path / "bad.py"
    bad.write_text('open("a.md").read()\nPath("b").read_text()\nPath("c").write_text("x")\nopen("d.npz", "rb")\n'
                   'Path("e").read_text(encoding="utf-8")\n', encoding="utf-8")
    assert sorted(_unencoded_text_io(bad)) == ["bad.py:1 open", "bad.py:2 read_text", "bad.py:3 write_text"]


# 7-8. no committed result and no frozen configuration changed since the Phase 8 baseline --------------------------------
def _git_diff_quiet(*paths: str) -> int:
    try:
        ok = subprocess.run(["git", "cat-file", "-e", f"{BASELINE}^{{commit}}"], cwd=ROOT, capture_output=True).returncode == 0
        r = subprocess.run(["git", "diff", "--quiet", BASELINE, "--", *paths], cwd=ROOT, capture_output=True)
    except OSError:
        pytest.skip("git not available")
    if not ok or r.returncode not in (0, 1):
        pytest.skip("Phase 8 baseline commit not available in this clone")
    return r.returncode


def test_committed_results_unchanged_since_phase8_baseline():
    assert _git_diff_quiet("results", "principal/a2_numerics") == 0


def test_frozen_configurations_unchanged():
    assert _git_diff_quiet("docs/b1/B1_CONFIG.md", "docs/b2/B2_CONFIG.md", "docs/b4/B4_CONFIG.md",
                           "src/qlo/b1/config.py", "src/qlo/b2/config.py", "src/qlo/b4/config.py") == 0
    assert B1CF.B1Config().sha256() == "2b7306ae18f9f6caf833670faf6ab55d48d11dcbb394d13930ab70bc5d77e497"
    assert B2CF.B2Config().sha256() == "9dc965c2ede0a00145b75827382fd47333de4b6b11d17f5749cf3e4e0c58cf4a"
    assert B4CF.B4Config().sha256() == "77e9e93a7e21d5ef1b9ad8015caa03b6a77af7b89ed0f69c8c7e8c3cc746ce38"
    # B3 and Stage 7 defaults equal the configuration recorded with their committed results
    for cfg, path in ((D3.B3Config(), "results/b3_hardening/config.json"), (Stage7Config(), "results/stage7/config.json")):
        committed = json.loads((ROOT / path).read_text(encoding="utf-8"))
        assert {k: committed[k] for k in asdict(cfg)} == json.loads(json.dumps(asdict(cfg), default=str))
