"""Phase 8 (Shravan section 5, Appendix B): the LaTeX appendix is generated from the committed appendix tables."""

from __future__ import annotations

from qlo.paper import appendix_tex as AT


def test_committed_appendix_b_is_what_the_generator_builds():
    assert AT.OUT.read_text(encoding="utf-8").replace("\r\n", "\n") == AT.build()


def test_every_column_except_provenance_is_typeset():
    for stem in {t[0] for t in AT.TABLES}:
        header = set(AT.read(stem)[0])
        shown = {c for s, _, _, cols in AT.TABLES if s == stem for c, _, _ in cols}
        assert shown == header - {"provenance"}, (stem, sorted(header - {"provenance"} - shown))


def test_every_row_and_cell_appears():
    out = AT.build()
    for stem, _, _, cols in AT.TABLES:
        for r in AT.read(stem):
            line = " & ".join(AT.tex(r[c]) for c, _, _ in cols) + r" \\"
            assert line in out, (stem, r[cols[0][0]])


def test_output_is_ascii_and_braces_balance():
    out = AT.build()
    assert out.isascii()
    body = out.replace(r"\{", "").replace(r"\}", "")
    assert body.count("{") == body.count("}")
    assert out.count("$") % 2 == 0


def test_tex_conversion():
    assert AT.tex("|0^n⟩") == r"$|0^n\rangle$"
    assert AT.tex("θ_j iid U[−π, π]") == r"$\theta_j$ iid U[$-$$\pi$, $\pi$]".replace("$$", "")
    assert AT.tex("V(θ) = ⊗_j RX(θ_j)") == r"V($\theta$) = $\bigotimes_j$ RX($\theta_j$)"
    assert AT.tex("100000 per n; seeds 11000–11009") == r"100\,000 per n; seeds 11000--11009"
    assert AT.tex("n ≥ 8, 50%") == r"n $\ge$ 8, 50\%"
