"""Phase 8 I7: one command rebuilds every paper asset from committed results and finds it unchanged."""

from __future__ import annotations

from qlo.paper import reproduce as R


def test_one_command_rebuild_matches_the_committed_paper_assets(tmp_path):
    assert R.run(tmp_path) == []
    assert len(list((tmp_path / "figures").glob("*.pdf"))) == 6
    assert (tmp_path / "appendix_b.tex").is_file()


def test_rebuild_reports_a_changed_table(tmp_path, monkeypatch):
    real = R.MT.build

    def tampered(out):
        tables = real(out)
        (out / "validation_table.csv").write_text("changed\n", encoding="utf-8")
        return tables

    monkeypatch.setattr(R.MT, "build", tampered)
    assert any("validation_table.csv" in p for p in R.run(tmp_path))


def test_text_comparison_ignores_windows_line_endings(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.write_bytes(b"x\r\ny\r\n")
    b.write_bytes(b"x\ny\n")
    assert R._same_text(a, b)
