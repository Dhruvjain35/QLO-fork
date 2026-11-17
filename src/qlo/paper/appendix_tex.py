"""Appendix B of the manuscript as LaTeX, generated from the committed appendix tables.

    python -m qlo.paper.appendix_tex      # paper/appendix/*.csv -> paper/drafts/appendix_b.tex

Every cell comes from a CSV that `python -m qlo.paper.methods_tables` builds from committed reports and result files;
PROVENANCE.md gives the source of each cell. Nothing here computes or rounds a number: it only selects columns, splits
wide tables and converts text to LaTeX. Every column except `provenance` appears in some table.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
APPENDIX = ROOT / "paper" / "appendix"
OUT = ROOT / "paper" / "drafts" / "appendix_b.tex"

# (csv stem, label, caption, [(column, header, width in cm)]); widths sum to about 22 cm (landscape text width).
TABLES = [
    ("configuration_table", "tab:config-circuits", "Experiment configurations (1 of 3): circuits and gradient component.", [
        ("experiment", "Experiment", 1.6), ("circuit_family", "Circuit family", 5.0), ("target", "Target", 1.2),
        ("n_range", "$n$", 3.4), ("depth", "Depth", 2.0), ("parameter_position", "Parameter position", 4.4),
        ("gradient_component", "Gradient component", 4.0)]),
    ("configuration_table", "tab:config-samples", "Experiment configurations (2 of 3): parameter samples, seeds and shots.", [
        ("experiment", "Experiment", 1.6), ("theta_distribution", "$\\theta$ distribution", 3.4),
        ("number_of_theta", "Number of $\\theta$", 4.0), ("number_of_seeds", "Seeds", 4.0),
        ("shot_budgets", "Shot budgets", 6.6), ("optimizer_iterations", "Optimizer iterations", 2.2)]),
    ("configuration_table", "tab:config-fits", "Experiment configurations (3 of 3): purpose, fits, intervals and sources.", [
        ("experiment", "Experiment", 1.6), ("purpose", "Purpose", 5.0), ("fit_range", "Fit range", 4.4),
        ("CI_method", "Interval method", 5.0), ("config_source", "Configuration", 3.0),
        ("result_source", "Results", 2.8)]),
    ("validation_table", "tab:validation", "Validation checks.", [
        ("check", "Check", 3.4), ("quantity", "Quantity", 5.0), ("reference", "Reference", 3.0),
        ("observed_error", "Observed error", 3.4), ("tolerance", "Tolerance", 1.4), ("status", "Status", 1.4),
        ("source_file", "Source", 2.8), ("source_location", "Location", 1.8)]),
    ("regime_of_validity", "tab:regime", "Regime of validity of each result.", [
        ("result", "Result", 2.4), ("mathematical_scope", "Mathematical scope", 4.0),
        ("tested_scope", "Tested scope", 3.6), ("assumptions", "Assumptions", 4.2),
        ("known_exclusions", "Known exclusions", 3.6), ("source", "Source", 4.4)]),
    ("reproduction_table", "tab:repro-runs", "Reproduction and compute cost (1 of 2): runs.", [
        ("experiment", "Experiment", 2.0), ("command", "Command", 3.8), ("platform_actually_run", "Platform", 3.6),
        ("python_version", "Python", 2.4), ("workers", "Workers", 2.8), ("wall_time", "Wall time", 3.0),
        ("cpu_time", "CPU time", 2.0), ("peak_memory", "Peak memory", 2.6)]),
    ("reproduction_table", "tab:repro-checks", "Reproduction and compute cost (2 of 2): caches, outputs and checks.", [
        ("experiment", "Experiment", 2.0), ("cache_requirement", "Cache", 4.6),
        ("output_directory", "Output", 3.0), ("expected_headline_check", "Headline check", 5.0),
        ("source_log", "Source log", 5.0), ("physical_hardware", "Quantum hardware", 2.0)]),
    ("estimator_resources", "tab:estimators", "Estimator resources and access requirements.", [
        ("estimator", "Estimator", 1.8), ("measured_quantity", "Measured quantity", 3.4), ("qubits", "Qubits", 1.1),
        ("copies", "Copies", 1.1), ("controlled_unitary_requirement", "Controlled unitary", 2.4),
        ("target_inverse_requirement", "Target inverse", 2.4), ("executions_convention", "Executions", 2.2),
        ("failure_behavior", "Failure behaviour", 4.4), ("rx_exponent", "RX exponent", 3.0)]),
]

_SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
            "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
_UNICODE = {"–": "--", "−": "$-$", "θ": r"$\theta$", "π": r"$\pi$", "⟩": r"$\rangle$", "ĝ": r"$\hat g$",
            "≤": r"$\le$", "ⁿ": r"$^{n}$", "≠": r"$\neq$", "±": r"$\pm$", "≥": r"$\ge$", "†": r"$^\dagger$",
            "≈": r"$\approx$", "·": r"$\cdot$", "→": r"$\to$", "§": r"\S{}", "Δ": r"$\Delta$", "⊗": r"$\otimes$",
            "ρ": r"$\rho$", "σ": r"$\sigma$", "ε": r"$\varepsilon$", "ä": r"\"a", "×": r"$\times$"}


def tex(s: str) -> str:
    """Plain-text cell -> ASCII LaTeX. |0^n⟩ becomes a ket; '/' and '_' get break points so paths wrap."""
    out = []
    for part in re.split(r"(\|0\^n⟩)", s):
        if part == "|0^n⟩":
            out.append(r"$|0^n\rangle$")
            continue
        for ch in part:
            if ch in _SPECIAL:
                out.append(_SPECIAL[ch] + (r"\allowbreak{}" if ch == "_" else ""))
            elif ch in _UNICODE:
                out.append(_UNICODE[ch])
            elif ord(ch) > 127:
                raise ValueError(f"no LaTeX mapping for {ch!r} in {s!r}")
            else:
                out.append(ch + (r"\allowbreak{}" if ch == "/" else ""))
    return "".join(out).replace("$$", "")


def code(path: str) -> str:
    """A file path in typewriter type that can break after each '/'."""
    return r"\texttt{" + tex(path) + "}"


def read(stem: str, appendix: Path = APPENDIX) -> list[dict]:
    with open(appendix / f"{stem}.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def table(stem: str, label: str, caption: str, cols: list[tuple[str, str, float]], appendix: Path = APPENDIX) -> str:
    spec = "".join(f">{{\\raggedright\\arraybackslash}}p{{{w:.1f}cm}}" for _, _, w in cols)
    head = " & ".join(h for _, h, _ in cols) + r" \\"
    L = [r"\begin{longtable}{" + spec + "}",
         r"\caption{" + caption + " Generated from " + code(f"paper/appendix/{stem}.csv") + "; the source of every cell"
         " is listed in " + code("paper/appendix/PROVENANCE.md") + r".}\label{" + label + r"} \\",
         r"\toprule", head, r"\midrule", r"\endfirsthead", r"\toprule", head, r"\midrule", r"\endhead",
         r"\bottomrule", r"\endfoot"]
    L += [" & ".join(tex(r[c]) for c, _, _ in cols) + r" \\" for r in read(stem, appendix)]
    L.append(r"\end{longtable}")
    return "\n".join(L)


def build(appendix: Path = APPENDIX) -> str:
    """The appendix as LaTeX, from the CSVs in `appendix` (default: the committed paper/appendix)."""
    L = ["% Appendix B: configuration, validation and reproduction tables (Phase 8 guidance, section 5: Dhruv drafts B).",
         "% GENERATED by `python -m qlo.paper.appendix_tex` from paper/appendix/*.csv; do not edit by hand.",
         "% Needs \\usepackage{longtable,booktabs,array,pdflscape}. The tables are typeset landscape at \\scriptsize.",
         "", r"\section{Configuration, validation and reproduction}", r"\label{app:tables}", "",
         r"These tables give every circuit, estimator, parameter range, shot budget, fit range and interval method used,"
         r" the checks each computation passed, the scope in which each result holds, and what it took to run. Every"
         r" entry is copied from a committed report or result file; " + code("paper/appendix/PROVENANCE.md") + r" names the"
         r" file and line or computation behind each cell. NOT RECORDED marks a value that was not logged; none is"
         r" estimated. All computations are classical simulations; no quantum hardware was used.", "",
         r"\begin{landscape}", r"\scriptsize", r"\setlength{\tabcolsep}{3pt}"]
    for t in TABLES:
        L += ["", table(*t, appendix=appendix)]
    L += ["", r"\end{landscape}", ""]
    return "\n".join(L)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args(argv)
    a.out.write_text(build(), encoding="utf-8", newline="\n")
    print(f"{len(TABLES)} tables -> {a.out}")


if __name__ == "__main__":
    main()
