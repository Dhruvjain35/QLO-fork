"""Rebuild every paper asset from committed results with one command and compare it with what is committed (I7).

    python -m qlo.paper.reproduce                  # build into .qlo_cache/reproduce/ and compare
    python -m qlo.paper.reproduce --out-dir DIR    # build somewhere else

It rebuilds the six figures, the appendix tables and provenance, Appendix B in LaTeX, and checks the bibliography.
Nothing under paper/ or results/ is overwritten: to update the committed files, run each builder on its own
(see paper/README.md). The experiments themselves are not rerun here; each has its own driver (README).

Exit status 1 if any figure source differs from the one the committed figures were built from, any rebuilt table or
LaTeX file differs from the committed one, or the bibliography check fails. Figure PDFs are compared byte for byte
and reported, but a byte difference only fails the run with --strict-pdf, because the bytes depend on the
matplotlib version (the plotted data are already checked through the source hashes).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from qlo.paper import appendix_tex as AT
from qlo.paper import figures as FIG
from qlo.paper import methods_tables as MT
from qlo.paper import sources as S

ROOT = S.ROOT
PAPER = ROOT / "paper"
DEFAULT_OUT = ROOT / ".qlo_cache" / "reproduce"


def _same_text(a: Path, b: Path) -> bool:
    return a.read_bytes().replace(b"\r\n", b"\n") == b.read_bytes().replace(b"\r\n", b"\n")


def run(out: Path, strict_pdf: bool = False) -> list[str]:
    """Rebuild into `out`; return the list of problems (empty means everything matches)."""
    problems: list[str] = []
    committed = json.loads((PAPER / "figures" / "manifest.json").read_text(encoding="utf-8"))
    built = FIG.build(out / "figures", png=False)
    old = {f["name"]: f for f in committed["figures"]}
    for f in built["figures"]:
        c = old.get(f["name"])
        if c is None:
            problems.append(f"figure {f['name']}: not in the committed manifest")
            continue
        if f["sources"] != c["sources"]:
            problems.append(f"figure {f['name']}: its source files differ from the ones the committed figure was built from")
        pdf_now, pdf_then = f["files"][0]["sha256"], c["files"][0]["sha256"]
        same = pdf_now == pdf_then
        print(f"  {f['name']}.pdf: {'identical to the committed PDF' if same else 'rebuilt; bytes differ from the committed PDF'}")
        if strict_pdf and not same:
            problems.append(f"figure {f['name']}: PDF bytes differ (--strict-pdf)")
    if set(old) - {f["name"] for f in built["figures"]}:
        problems.append(f"committed figures not rebuilt: {sorted(set(old) - {f['name'] for f in built['figures']})}")

    MT.build(out / "appendix")
    for f in sorted((out / "appendix").iterdir()):
        if not _same_text(f, PAPER / "appendix" / f.name):
            problems.append(f"paper/appendix/{f.name}: rebuilt file differs from the committed one")
    tex = out / "appendix_b.tex"
    tex.write_text(AT.build(out / "appendix"), encoding="utf-8", newline="\n")
    if not _same_text(tex, AT.OUT):
        problems.append("paper/drafts/appendix_b.tex: rebuilt file differs from the committed one")

    bib = subprocess.run([sys.executable, str(ROOT / "tools" / "check_bib.py")], cwd=ROOT, capture_output=True,
                         text=True, encoding="utf-8")
    if bib.returncode != 0:
        problems.append("bibliography check failed: " + (bib.stdout + bib.stderr).strip().splitlines()[-1])
    return problems


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--strict-pdf", action="store_true", help="also fail when a rebuilt PDF is not byte-identical")
    a = ap.parse_args(argv)
    print(f"Rebuilding the paper assets into {a.out_dir}")
    problems = run(a.out_dir, a.strict_pdf)
    if problems:
        print("\nFAILED:\n" + "\n".join(f"  - {p}" for p in problems))
        raise SystemExit(1)
    print("\nOK: 6 figures, the appendix tables, Appendix B and the bibliography rebuild from committed results and match"
          " what is committed.")


if __name__ == "__main__":
    main()
