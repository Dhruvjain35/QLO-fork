"""Build every paper figure from committed results (Phase 8 I3).

    python -m qlo.paper.figures                 # -> paper/figures/*.pdf, png/*.png, FIGURE_SOURCES.md, manifest.json
    python -m qlo.paper.figures --out-dir DIR   # anywhere else (tests)

Rules: data come only from committed CSV / JSON files (qlo.paper.sources); the only numbers written here are exact
reference constants (log10 2, 4, 8, 16, the ratio 4/3) and the closed form of Proposition 6, each named where it is
used. No fit is recomputed except where a panel says so; every panel is listed in FIGURE_SOURCES.md. PDFs are written
without timestamps, so unchanged inputs give byte-identical files.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

import numpy as np

from qlo.paper import sources as S
from qlo.paper import style as ST

plt = ST.plt
OUT = S.ROOT / "paper" / "figures"
LOG2, LOG4, LOG8, LOG16 = (float(np.log10(v)) for v in (2, 4, 8, 16))
MS_SMALL = 1e-2          # the M*S <= 1e-2 "deep limit" cut used for the B1 sign-law summary (b1_entangling.phase_sign)
FIXED_N = 14             # deepest B2 fixed-budget n with exact enumeration for every estimator up to T = 2048
FIXED_T_MARK = 2048      # budget highlighted in Figure 6
PDF_META = {"Creator": None, "Producer": None, "CreationDate": None}
PNG_META = {"Software": None}

PANELS: list[dict] = []


def panel(fig: str, letter: str, **info) -> None:
    PANELS.append({"figure": fig, "panel": letter, **info})


def _fam_style(family: str) -> tuple[str, str]:
    return {"rx_product": ("o", ST.OKABE["black"]), "hea_ring": ("s", ST.OKABE["blue"]),
            "rxry_czbrick": ("^", ST.OKABE["vermillion"])}[family]


FAMILY_LABEL = {"rx_product": "RX product", "hea_ring": "HEA ring", "rxry_czbrick": "RX-RY CZ brickwork"}
REGIME_FACE = {"product": 1.0, "d2": 0.0, "d4": 0.5, "dn": 1.0}      # marker fill: hollow d = 2, half d = 4, filled d = n


def _face(color: str, regime: str):
    a = REGIME_FACE[regime]
    if a == 0.0:
        return "white"
    if a == 1.0:
        return color
    import matplotlib.colors as mc
    r, g, b = mc.to_rgb(color)
    return (1 - a * (1 - r), 1 - a * (1 - g), 1 - a * (1 - b))


# =================================================================================================================
def fig1():
    st, fits, iv = S.table("stage7_scaling"), S.doc("stage7_fits")["fits"], S.table("b3_stage7_intervals")
    fig = plt.figure(figsize=(ST.DOUBLE, 10.0 * ST.CM), layout="constrained")
    gs = fig.add_gridspec(2, 2, height_ratios=[0.5, 1])
    a = fig.add_subplot(gs[0, :])                       # placeholder until the Figure 1(a) schematic (Shravan) replaces it
    a.axis("off")
    ST.panel_label(a, "a", x=0.0, y=0.96)
    a.text(0.05, 0.97, r"$F(\theta)=\prod_j \cos^2(\theta_j/2)$,  target $|0^n\rangle$;   "
           r"$F_\pm = F(\theta \pm \frac{\pi}{2} e_k)$,  $g=\partial_k(1-F)=(F_- - F_+)/2$", transform=a.transAxes, va="top", fontsize=9)
    for x, est, lines in ((0.05, "loschmidt", [r"each shot $\sim$ Bernoulli$(F_\pm)$", r"$\hat g_{\rm LE} = (K_- - K_+)/(2M)$",
                                              r"per-shot variance of $\hat F$: $F(1-F)$"]),
                          (0.53, "swap", [r"each shot $\sim$ Bernoulli$((1+F_\pm)/2)$", r"$\hat g_{\rm SW} = (K_- - K_+)/M$",
                                          r"per-shot variance of $\hat F$: $1-F^2$"])):
        label, c = ST.EST[est][0], ST.EST[est][1]
        a.text(x, 0.3, "\n".join([label + " readout"] + lines), transform=a.transAxes, va="center", linespacing=1.35,
               bbox={"boxstyle": "round,pad=0.4", "fc": "white", "ec": c, "lw": 0.9})
    panel("1", "a", source="docs/stages/STAGE7.md §4-6 (definitions, no data)", columns="—", filters="—", aggregation="—",
          ci="—", function="fig1")

    b = fig.add_subplot(gs[1, 0])
    for sc in ("loschmidt", "swap"):
        g = st[st.scheme == sc].sort_values("n")
        label, c, m, ls, _ = ST.EST[sc]
        b.fill_between(g.n, g.snr1_log10M_q25, g.snr1_log10M_q75, color=c, alpha=0.18, lw=0)
        b.plot(g.n, g.snr1_log10M_median, m, color=c, label=label, ms=3.2)
        f = fits[f"{sc}_snr1"]
        x = np.array([g.n.min(), g.n.max()], dtype=float)
        b.plot(x, f["intercept"] + f["slope"] * x, ls, color=c, lw=0.8)
        xt = 11.0
        b.text(xt + 0.4, f["intercept"] + f["slope"] * xt - 0.6, f"slope {f['slope']:.3f}", color=c, ha="left", va="top",
               bbox={"fc": "white", "ec": "none", "pad": 0.5})
    b.set_xlabel(r"qubits $n$")
    b.set_ylabel(r"median $\log_{10} M$ for SNR $\geq 1$")
    b.set_xticks(range(2, 21, 4))
    b.legend(loc="upper left")
    ST.panel_label(b, "b")
    panel("1", "b", source="results/stage7/scaling_summary.csv; results/stage7/scaling_fits.json",
          columns="n, scheme, snr1_log10M_median, snr1_log10M_q25, snr1_log10M_q75; fits.{loschmidt,swap}_snr1.slope/intercept",
          filters="scheme in {loschmidt, swap}; n = 2..20 (100,000 theta per n, k = 0)", aggregation="committed medians and quartiles; committed OLS fit",
          ci="band = interquartile range over theta (not an uncertainty of the median)", function="fig1")

    c = fig.add_subplot(gs[1, 1])
    targets = [("snr1", r"SNR$\geq$1"), ("snr2", r"SNR$\geq$2"), ("dir0.75", r"$P_c\!\geq\!0.75$"), ("dir0.9", r"$P_c\!\geq\!0.9$")]
    p = iv[(iv.fit_range == "primary_2_20") & iv.metric.str.startswith("slope_")].set_index("metric")   # drops the two text summary rows
    p = p[["stage7_estimate", "seed_pct_lo", "seed_pct_hi", "theta_lo", "theta_hi"]].apply(lambda col: col.astype(float))
    for off, sc, ref in ((-0.14, "loschmidt", LOG4), (0.14, "swap", LOG16)):
        label, col, m, _, _ = ST.EST[sc]
        rows = [p.loc[f"slope_{sc}_{t}"] for t, _ in targets]
        x = np.arange(len(targets)) + off
        y = np.array([1e3 * (r.stage7_estimate - ref) for r in rows])
        lo = np.array([1e3 * (r.seed_pct_lo - ref) for r in rows])
        hi = np.array([1e3 * (r.seed_pct_hi - ref) for r in rows])
        tlo = np.array([1e3 * (r.theta_lo - ref) for r in rows])
        thi = np.array([1e3 * (r.theta_hi - ref) for r in rows])
        c.errorbar(x, y, yerr=[y - lo, hi - y], fmt=m, color=col, mfc=col, lw=1.0, label=label + (r" ($b_{\rm ref}=\log_{10}4$)" if sc == "loschmidt" else r" ($b_{\rm ref}=\log_{10}16$)"))
        c.errorbar(x + 0.07, y, yerr=[y - tlo, thi - y], fmt="none", color=col, lw=0.5, alpha=0.8)
    c.axhline(0, color="0.4", lw=0.5, ls=":")
    c.set_xticks(range(len(targets)), [t for _, t in targets])
    c.set_xlim(-0.5, len(targets) - 0.5)
    c.set_ylabel(r"$10^3\,(b - b_{\rm ref})$  [decades / qubit]")
    c.set_ylim(-11.5, 15.5)
    c.tick_params(axis="x", top=False)
    c.legend(loc="upper center")
    ST.panel_label(c, "c")
    panel("1", "c", source="results/b3_hardening/stage7_interval_check.csv",
          columns="fit_range, metric, stage7_estimate, seed_pct_lo, seed_pct_hi, theta_lo, theta_hi",
          filters="fit_range = primary_2_20; metric = slope_{loschmidt,swap}_{snr1,snr2,dir0.75,dir0.9} (the file's two text 'headline range' rows are excluded)",
          aggregation="Stage 7 point slope minus the reference log10 4 (Loschmidt) or log10 16 (SWAP), times 1000",
          ci="thick bar: B3 SEED 95% percentile interval over 20 seeds (B3 primary criterion); thin offset bar: B3 THETA bootstrap 95% CI",
          function="fig1")
    return fig


# =================================================================================================================
def stage7_sign_range(sl, stage7_M) -> tuple[float, float]:
    """Cancellation-free median P(correct | g_LE != 0) at n = 20 over the Stage 7 shot counts (B3 D2; Phase 8 I1)."""
    r = sl[(sl.n == 20) & sl.shots.isin(stage7_M)].reference_observed_median_accurate
    if len(r) != len(stage7_M):
        raise ValueError("B3 sign-law summary lacks a Stage 7 shot count at n = 20")
    return float(r.min()), float(r.max())


def fig2():
    d, sl, cfg7 = S.table("b1_sign"), S.table("b3_sign_law"), S.doc("stage7_config")
    if not np.allclose(d.error, d.p_correct_given_nonzero - d.predicted, rtol=0, atol=1e-9):
        raise ValueError("B1 conditional_sign_summary.error is not observed - predicted")
    if not (d.error > 0).all():
        raise ValueError("Figure 2b plots error on a log axis and needs error > 0 in every row")
    fig, ax = plt.subplots(1, 3, figsize=(ST.DOUBLE, 6.2 * ST.CM), layout="constrained", gridspec_kw={"wspace": 0.04})
    a, b, c = ax
    sc = a.scatter(d.predicted, d.p_correct_given_nonzero, c=np.log10(d.M_times_S), s=4, lw=0, cmap="cividis", rasterized=False)
    a.plot([0.5, 1], [0.5, 1], color="k", lw=0.6)
    a.set_xlabel(r"predicted $(1+|r|)/2$")
    a.set_ylabel(r"$P(\mathrm{correct\ sign} \mid \hat g_{\rm LE} \neq 0)$")
    cb = fig.colorbar(sc, ax=a, fraction=0.05, pad=0.02)
    cb.solids.set_rasterized(False)          # Matplotlib rasterizes colorbars with >= 50 levels (Colorbar.n_rasterize); keep it vector
    cb.set_label(r"$\log_{10}(M S)$")
    ST.panel_label(a, "a")
    panel("2", "a", source="results/b1_entangling/conditional_sign_summary.csv",
          columns="predicted, p_correct_given_nonzero, M_times_S", filters="all 720 rows: the 16 B1 entangling cells (2 families x depth regimes x positions) at n = 12, theta at 5 S quantiles, M = 1..65536",
          aggregation="none (exact per-theta probabilities)", ci="none (exact computation, no sampling)", function="fig2")

    b.loglog(d.M_times_S, d.error, ".", color="k", ms=2.2, alpha=0.6)
    b.axvspan(d.M_times_S.min() / 2, MS_SMALL, color="0.85", lw=0)
    b.text(d.M_times_S.min(), d.error.max() * 1.6, r"$M S \leq 10^{-2}$", va="top")
    b.set_xlabel(r"$M S$")
    b.set_ylabel("observed $-$ predicted")
    ST.panel_label(b, "b")
    panel("2", "b", source="results/b1_entangling/conditional_sign_summary.csv", columns="M_times_S, error",
          filters="all rows; error > 0 in every row (checked), so no row is dropped by the log axis",
          aggregation="none", ci="none (exact)", function="fig2")

    stage7_M = [int(m) for m in cfg7["paired_shots"]]
    pred = float(sl.prediction_fixed.iloc[0])
    marks = {12: "o", 16: "s", 20: "D", 24: "^"}
    for i, (n, m) in enumerate(marks.items()):
        g = sl[sl.n == n].sort_values("shots")
        col = plt.get_cmap("cividis")(i / (len(marks) - 1) * 0.85)
        c.errorbar(g.shots * (1.0 + 0.06 * (i - 1.5)), g.reference_observed_median_accurate,
                   yerr=[g.reference_observed_median_accurate - g.SEED_pct_lo, g.SEED_pct_hi - g.reference_observed_median_accurate],
                   fmt=m + "-", color=col, ms=3, lw=0.8, elinewidth=0.5, label=fr"$n={n}$")
    c.axhline(pred, color="k", ls="--", lw=0.7, label=r"$(1+1/\sqrt{2})/2$")
    c.set_xscale("log")
    c.set_xlabel(r"shots per shifted circuit $M$")
    c.set_ylabel(r"median $P(\mathrm{correct} \mid \hat g_{\rm LE} \neq 0)$")
    stage7_sign_range(sl, stage7_M)                     # fails if B3 lacks a Stage 7 M; the caption quotes this range
    c.legend(loc="upper left", handlelength=1.6)
    ST.panel_label(c, "c")
    panel("2", "c", source="results/b3_hardening/sign_law_summary.csv; results/stage7/config.json",
          columns="n, shots, reference_observed_median_accurate, SEED_pct_lo, SEED_pct_hi, prediction_fixed; paired_shots",
          filters="n in {12, 16, 20, 24}; all M = 16..65536 (B3 grid); the caption's range uses n = 20 at the Stage 7 M values (paired_shots)",
          aggregation="median over the regenerated Stage 7 theta population, computed without cancellation (B3 D2); the caption's n = 20 range is stage7_sign_range",
          ci="B3 SEED 95% percentile interval over 20 seeds", function="fig2")
    return fig


# =================================================================================================================
def fig3():
    m = S.table("b1_main")
    m = m[m.fit_range == "primary"].reset_index(drop=True)
    fig, ax = plt.subplots(2, 2, figsize=(ST.DOUBLE, 12.5 * ST.CM), layout="constrained", gridspec_kw={"wspace": 0.06, "hspace": 0.04})
    a, b, c, d = ax.ravel()

    def eb(axis, x, y, r, xc=None, yc=None, **kw):
        mk, col = _fam_style(r.family)
        xerr = None if xc is None else [[x - r[f"{xc}_ci_lo"]], [r[f"{xc}_ci_hi"] - x]]
        yerr = None if yc is None else [[y - r[f"{yc}_ci_lo"]], [r[f"{yc}_ci_hi"] - y]]
        axis.errorbar([x], [y], xerr=xerr, yerr=yerr, fmt=mk, color=col, mfc=_face(col, r.regime), mec=col, ms=3.4, lw=0.6, **kw)

    for _, r in m.iterrows():
        eb(a, r.b_S, r.gap_obs, r, "b_S", "gap_obs")
    lim = [m.b_S.min() - 0.02, m.b_S.max() + 0.02]
    a.plot(lim, lim, color="k", lw=0.6)
    a.set_xlabel(r"$b_S$")
    a.set_ylabel(r"$b_{\rm SWAP} - b_{\rm LE}$")
    for fam in ("rx_product", "hea_ring", "rxry_czbrick"):
        mk, col = _fam_style(fam)
        a.plot([], [], mk, color=col, mfc=col, label=FAMILY_LABEL[fam], ms=3.4)
    a.legend(loc="upper left", handlelength=1.0)
    ST.panel_label(a, "a")

    lab = []
    for i, r in m.iterrows():
        y = 100 * r.eps_gap / r.b_S
        mk, col = _fam_style(r.family)
        b.errorbar([i], [y], yerr=[[y - 100 * r.eps_gap_ci_lo / r.b_S], [100 * r.eps_gap_ci_hi / r.b_S - y]], fmt=mk, color=col,
                   mfc=_face(col, r.regime), mec=col, ms=3.0, lw=0.6)
        lab.append("RX" if r.family == "rx_product" else f"{'HEA' if r.family == 'hea_ring' else 'CZ'} {r.regime} {r.position[0]}")
    b.axhline(0, color="k", lw=0.6)
    b.set_xticks(range(len(m)), lab, rotation=90)
    b.set_ylabel(r"$100\,\varepsilon_{\rm gap}/b_S$  [%]")
    b.tick_params(axis="x", top=False)
    ST.panel_label(b, "b")

    pos_x = {"k=0": 0, "EARLY": 1, "MIDDLE": 2, "LATE": 3}
    jit = {("rx_product", "product"): 0.0, ("hea_ring", "d2"): -0.27, ("hea_ring", "d4"): -0.18, ("hea_ring", "dn"): -0.09,
           ("rxry_czbrick", "d2"): 0.09, ("rxry_czbrick", "d4"): 0.18, ("rxry_czbrick", "dn"): 0.27}
    for _, r in m.iterrows():
        mk, col = _fam_style(r.family)
        y = 1e3 * r.b_r
        c.errorbar([pos_x[r.position] + jit[(r.family, r.regime)]], [y], yerr=[[y - 1e3 * r.b_r_ci_lo], [1e3 * r.b_r_ci_hi - y]], fmt=mk,
                   color=col, mfc=_face(col, r.regime), mec=col, ms=3.4, lw=0.6)
    c.axhline(0, color="k", lw=0.6)
    c.set_xticks(range(4), ["RX $k{=}0$", "early", "middle", "late"])
    c.set_ylabel(r"$10^3\,b_r$  [decades / qubit]")
    c.tick_params(axis="x", top=False)
    ST.panel_label(c, "c")

    for _, r in m.iterrows():
        eb(d, r.ratio_pred, r.ratio_obs, r, "ratio_pred", "ratio_obs")
    lo, hi = min(m.ratio_obs_ci_lo.min(), m.ratio_pred_ci_lo.min()) - 0.005, max(m.ratio_obs_ci_hi.max(), m.ratio_pred_ci_hi.max()) + 0.005
    d.plot([lo, hi], [lo, hi], color="k", lw=0.6)
    d.set_xlim(lo, hi)
    d.set_ylim(lo, hi)
    d.set_xlabel(r"predicted ratio (from $b_S$, $b_r$)")
    d.set_ylabel(r"observed $b_{\rm SWAP}/b_{\rm LE}$")
    ST.panel_label(d, "d")
    common = dict(source="results/b1_entangling/main_table.csv", filters="fit_range = primary (each cell's full n grid); 17 rows: RX product + 2 families x 3 depth regimes x positions",
                  ci="bootstrap 95% CI of the 10-seed mean (columns *_ci_lo / *_ci_hi, as committed by B1)", function="fig3")
    panel("3", "a", columns="b_S, gap_obs (+ _ci_lo/_ci_hi)", aggregation="10-seed mean slopes as committed", **common)
    panel("3", "b", columns="eps_gap (+ _ci_lo/_ci_hi), b_S", aggregation="100 * eps_gap / b_S; the CI is the eps_gap CI divided by the b_S mean (b_S treated as fixed)", **common)
    panel("3", "c", columns="b_r (+ _ci_lo/_ci_hi), position", aggregation="1000 * b_r; horizontal jitter separates family and depth regime", **common)
    panel("3", "d", columns="ratio_pred, ratio_obs (+ _ci_lo/_ci_hi)", aggregation="as committed (ratio_pred from the measured b_S and b_r of the same cell)", **common)
    return fig


# =================================================================================================================
EST4 = ("loschmidt", "swap_ancilla", "swap_destructive", "hadamard_u")


def fig4():
    req, sl, fx = S.table("b2_required"), S.table("b2_slopes"), S.table("b2_fixed")
    r0 = req[(req.seed == 0) & (req.rho == 1.0)]
    fig, ax = plt.subplots(2, 3, figsize=(ST.DOUBLE, 12.0 * ST.CM), layout="constrained", gridspec_kw={"wspace": 0.04, "hspace": 0.06})
    a, b, c, d, e, f = ax.ravel()
    for est in EST4:
        g = r0[r0.estimator == est].sort_values("n")
        kw = ST.marker_kw(est, 4.2 if est == "swap_destructive" else 3.0)
        if est != "swap_destructive":
            a.fill_between(g.n, g.q25_log10_total, g.q75_log10_total, color=kw["color"], alpha=0.13, lw=0)
        a.plot(g.n, g.median_log10_total_executions, **kw, lw=0.8)
    a.set_xlabel(r"qubits $n$")
    a.set_ylabel("median log$_{10}$ total executions")
    a.set_xticks(range(2, 21, 4))
    fig.legend(*a.get_legend_handles_labels(), loc="outside upper center", ncol=4)
    ST.panel_label(a, "a")
    panel("4", "a", source="results/b2_estimators/required_shots_rx.csv",
          columns="seed, rho, estimator, n, median_log10_total_executions, q25_log10_total, q75_log10_total",
          filters="seed = 0 (the Stage 7 theta population, 100,000 theta per n), rho = 1 (SNR >= 1)",
          aggregation="committed medians and quartiles", ci="band = interquartile range over theta", function="fig4")

    s = sl[sl.quantity == "median_log10_total_executions"]
    ref = {"loschmidt": LOG4, "hadamard_u": LOG4, "swap_ancilla": LOG16, "swap_destructive": LOG16}
    for i, est in enumerate(EST4):
        for off, fr, filled in ((-0.12, "primary_2_20", True), (0.12, "n_ge_8", False)):
            r = s[(s.estimator == est) & (s.fit_range == fr)].iloc[0]
            kw = ST.marker_kw(est)
            y, lo, hi = (1e3 * (v - ref[est]) for v in (r.stage7_population_slope, r.replicate_pct_lo, r.replicate_pct_hi))
            b.errorbar([i + off], [y], yerr=[[y - lo], [hi - y]], fmt=kw["marker"], color=kw["color"], mfc=kw["color"] if filled else "white",
                       mec=kw["color"], ms=3.4, lw=0.7)
            if filled:
                b.text(i + off, hi + 0.6, f"{r.stage7_population_slope:.4f}", ha="center", va="bottom", rotation=90)
    b.axhline(0, color="0.4", lw=0.5, ls=":")
    b.set_xticks(range(4), ["LE", "anc.\nSWAP", "destr.\nSWAP", "Had."])
    b.tick_params(axis="x", top=False)
    b.set_xlim(-0.6, 3.6)
    b.set_ylim(-9, 20)
    b.set_ylabel(r"$10^3\,(b - b_{\rm ref})$  [decades / qubit]")
    b.plot([], [], "ko", ms=3, label="$n=2$–$20$")
    b.plot([], [], "ko", mfc="white", ms=3, label=r"$n \geq 8$")
    b.legend(loc="upper center", ncol=2, handlelength=0.8, columnspacing=0.8)
    ST.panel_label(b, "b")
    panel("4", "b", source="results/b2_estimators/slope_summary.csv",
          columns="estimator, fit_range, quantity, stage7_population_slope, replicate_pct_lo, replicate_pct_hi",
          filters="quantity = median_log10_total_executions; fit_range in {primary_2_20, n_ge_8}",
          aggregation="slope on the Stage 7 population minus b_ref (log10 4 for Loschmidt and Hadamard, log10 16 for both SWAPs), times 1000; the slope itself is printed above each primary point",
          ci="95% percentile interval over the 10 replicate seeds (12000-12009)", function="fig4")

    pv = r0.pivot_table(index="n", columns="estimator", values="median_log10_total_executions")
    c.plot(pv.index, 10 ** (pv.hadamard_u - pv.loschmidt), **{**ST.marker_kw("hadamard_u"), "label": "Hadamard / Loschmidt"})
    c.plot(pv.index, 10 ** (pv.swap_destructive - pv.swap_ancilla), **{**ST.marker_kw("swap_destructive", 4.0), "label": "destructive / ancilla SWAP"})
    c.set_ylim(0, 11)
    c.set_xticks(range(2, 21, 4))
    c.set_xlabel(r"qubits $n$")
    c.set_ylabel("ratio of median total executions")
    c.text(20, 8.4, "Hadamard / Loschmidt", ha="right", va="top", color=ST.EST["hadamard_u"][1])
    c.text(20, 2.0, "destructive / ancilla SWAP", ha="right", va="bottom", color=ST.EST["swap_destructive"][1])
    ST.panel_label(c, "c")
    panel("4", "c", source="results/b2_estimators/required_shots_rx.csv", columns="estimator, n, median_log10_total_executions",
          filters="seed = 0, rho = 1", aggregation="10**(difference of committed median log10 total executions) at each n",
          ci="none shown", function="fig4")

    g14 = fx[fx.n == FIXED_N]
    for axis, col, ylab, letter in ((d, "median_P_zero", r"median $P(\hat g = 0)$", "d"),
                                    (e, "median_P_correct_given_nonzero", r"median $P(\mathrm{correct} \mid \hat g \neq 0)$", "e"),
                                    (f, "median_P_correct", r"median $P(\mathrm{correct\ sign})$", "f")):
        for est in EST4:
            g = g14[g14.estimator == est].sort_values("total_executions")
            axis.plot(g.total_executions, g[col], **ST.marker_kw(est, 4.2 if est == "swap_destructive" else 3.0), lw=0.8)
        axis.set_xscale("log")
        axis.set_xlabel(r"total executions $T$")
        axis.set_ylabel(ylab)
        ST.panel_label(axis, letter)
        panel("4", letter, source="results/b2_estimators/fixed_budget_failure_modes.csv", columns=f"n, total_executions, estimator, method, {col}",
              filters=f"n = {FIXED_N}; T = 32..32768", aggregation="median over 2,000 theta (300 for Hadamard), as committed",
              ci="none (exact enumeration; Hadamard at T >= 8192 is Monte Carlo with 20,000 repetitions, method column)", function="fig4")
    e.axhline(0.5, color="0.4", lw=0.5, ls=":")
    d.set_ylim(-0.03, 1.03)
    return fig


# =================================================================================================================
def _prop6_bS(p: np.ndarray) -> np.ndarray:
    """Proposition 6 (docs/theory/A2_PROPOSITIONS.md): b_S' = -(2/ln 10) ln[(sqrt(1 - p/2) + sqrt(p/2)) / 2]."""
    return -(2.0 / np.log(10.0)) * np.log((np.sqrt(1.0 - p / 2.0) + np.sqrt(p / 2.0)) / 2.0)


def fig5():
    w, pr, cx = S.table("b4_window"), S.table("b4_pred"), S.table("b4_crossover")
    ps = sorted(S.doc("b4_config")["global_p"])
    cmap = plt.get_cmap("cividis")
    pcol = {p: cmap(0.9 * i / (len(ps) - 1)) for i, p in enumerate(ps)}
    pmark = dict(zip(ps, "ovsD^"))
    fig, ax = plt.subplots(2, 2, figsize=(ST.DOUBLE, 12.5 * ST.CM), layout="constrained", gridspec_kw={"wspace": 0.06, "hspace": 0.04})
    a, b, c, d = ax.ravel()
    rx = w[(w.family == "rx_product") & (w.model == "global")]
    for p in ps:
        g = rx[rx.p == p].sort_values("n_mid")
        lab = "$p=0$" if p == 0 else f"$10^{{{int(np.log10(p))}}}$"
        a.plot(g.n_mid, g.b_LE, pmark[p] + "-", color=pcol[p], ms=3.0, lw=0.9, label=lab)
        a.plot(g.n_mid, g.b_SWAP, pmark[p] + "--", color=pcol[p], mfc="white", ms=3.0, lw=0.8)
    for v, t in ((LOG4, r"$\log_{10}4$"), (LOG8, r"$\log_{10}8$"), (LOG16, r"$\log_{10}16$")):
        a.axhline(v, color="0.5", lw=0.5, ls=":")
        a.text(1.01, v, t, transform=a.get_yaxis_transform(), va="center")
    a.set_xlabel(r"window centre $n$ (3-point windows)")
    a.set_ylabel("local slope [decades / qubit]")
    a.plot([], [], "-", color="0.3", lw=0.9, label=r"$b_{\rm LE}$")
    a.plot([], [], "--", color="0.3", lw=0.8, label=r"$b_{\rm SWAP}$")
    a.set_ylim(0.55, 1.72)
    a.legend(loc="upper center", ncol=3, handlelength=1.4, columnspacing=0.8)
    ST.panel_label(a, "a")
    panel("5", "a", source="results/b4_noise/window_slopes.csv; results/b4_noise/config.json", columns="model, p, family, n_mid, b_LE, b_SWAP; global_p",
          filters="model = global, family = rx_product", aggregation="committed local slopes over 3 consecutive n of the 10-seed mean medians",
          ci="none shown (window slopes of seed means)", function="fig5")

    xs = {p: i for i, p in enumerate(ps)}
    ent = pr[(pr.model == "global") & (pr.family != "rx_product") & (pr.fit_range == "secondary_n_ge_8")]
    b.plot([xs[p] + 0.15 for p in ent.p], ent.measured_ratio_obs, ".", color="0.6", ms=2.5, label="entangling, global")
    for fr, mfc, lab in (("secondary_n_ge_8", "k", r"RX global, $n\geq 8$"), ("primary", "white", r"RX global, $n=2$–$20$")):
        g = pr[(pr.model == "global") & (pr.family == "rx_product") & (pr.fit_range == fr)].sort_values("p")
        b.plot([xs[p] for p in g.p], g.measured_ratio_obs, "o-", color="k", mfc=mfc, ms=3.2, lw=0.8, label=lab)
    g = pr[(pr.model == "global") & (pr.family == "rx_product") & (pr.fit_range == "secondary_n_ge_8")].sort_values("p")
    b.plot([xs[p] - 0.15 for p in g.p], g.asym_ratio, "_", color=ST.OKABE["blue"], ms=8, mew=1.2, label="Prop. 5 (RX)")
    lo = pr[(pr.model == "local") & (pr.family == "rx_product") & (pr.fit_range == "secondary_n_ge_8")].sort_values("p")
    b.plot([xs[p] for p in lo.p], lo.measured_ratio_obs, "s--", color=ST.OKABE["vermillion"], ms=3.2, lw=0.8, label=r"RX local, $n\geq 8$")
    b.axhline(2.0, color="0.5", lw=0.5, ls=":")
    b.axhline(4.0 / 3.0, color="0.5", lw=0.5, ls=":")
    b.text(1.01, 2.0, "2", transform=b.get_yaxis_transform(), va="center")
    b.text(1.01, 4.0 / 3.0, "4/3", transform=b.get_yaxis_transform(), va="center")
    b.set_xticks(range(len(ps)), ["0" if p == 0 else f"$10^{{{int(np.log10(p))}}}$" for p in ps])
    b.set_xlabel("depolarizing strength $p$")
    b.set_ylabel(r"exponent ratio $b_{\rm SWAP}/b_{\rm LE}$")
    b.set_ylim(0.7, 2.08)
    b.legend(loc="lower left", handlelength=1.6)
    ST.panel_label(b, "b")
    panel("5", "b", source="results/b4_noise/predictions_vs_measured.csv",
          columns="model, p, family, fit_range, measured_ratio_obs, asym_ratio",
          filters="RX product: global (both fit ranges) and local (n >= 8); entangling cells: global, n >= 8 (16 cells)",
          aggregation="10-seed mean slopes as committed; asym_ratio is the committed Proposition 5 prediction", ci="none shown", function="fig5")

    loc = pr[(pr.model == "local") & (pr.family == "rx_product")]
    pp = np.logspace(np.log10(loc.p.min()) - 0.3, np.log10(loc.p.max()) + 0.3, 200)
    c.plot(pp, _prop6_bS(pp), color="k", lw=0.8, label="Proposition 6")
    for fr, mfc, lab in (("secondary_n_ge_8", ST.OKABE["vermillion"], r"measured ($n\geq 8$)"), ("primary", "white", r"measured ($n=2$–$20$)")):
        g = loc[loc.fit_range == fr].sort_values("p")
        c.plot(g.p, g.measured_b_S, "s", color=ST.OKABE["vermillion"], mfc=mfc, ms=3.4, label=lab)
    c.set_xscale("log")
    c.set_xlabel("local depolarizing strength $p$")
    c.set_ylabel(r"$b_S'$  [decades / qubit]")
    c.legend(loc="lower left")
    ST.panel_label(c, "c")
    panel("5", "c", source="results/b4_noise/predictions_vs_measured.csv; docs/theory/A2_PROPOSITIONS.md (Proposition 6 closed form)",
          columns="model, p, family, fit_range, measured_b_S", filters="model = local, family = rx_product",
          aggregation="10-seed mean b_S as committed; curve evaluated from the closed form", ci="none shown", function="fig5")

    cc = cx[cx.n_star.notna()]
    r = cc[cc.family == "rx_product"].sort_values("p")
    e = cc[cc.family != "rx_product"]
    d.plot(e.p * 1.08, e.n_star, ".", color="0.55", ms=3, label="B1 entangling cells")
    d.plot(r.p, r.n_star, "o-", color="k", ms=3.2, lw=0.8, label="RX product")
    d.set_xscale("log")
    d.set_xlabel("global depolarizing strength $p$")
    d.set_ylabel(r"crossover $n^*$")
    d.legend(loc="upper right")
    ST.panel_label(d, "d")
    panel("5", "d", source="results/b4_noise/crossover.csv", columns="family, p, n_star, note",
          filters="rows with a crossover inside the tested n range (note = 'inside range'); NaN rows ('signal dominates throughout') are not plotted",
          aggregation="as committed (log-linear interpolation of q * median S against the floor)", ci="none", function="fig5")
    return fig


# =================================================================================================================
def fig6():
    sl, fx = S.table("b2_slopes"), S.table("b2_fixed")
    s = sl[(sl.quantity == "median_log10_total_executions") & (sl.fit_range == "primary_2_20")].set_index("estimator")
    g14 = fx[fx.n == FIXED_N]
    fig, ax = plt.subplots(1, 2, figsize=(ST.DOUBLE, 6.5 * ST.CM), layout="constrained", gridspec_kw={"wspace": 0.06})
    for axis, col, ylab, letter in ((ax[0], "median_P_zero", r"median $P(\hat g = 0)$", "a"),
                                    (ax[1], "median_P_correct_given_nonzero", r"median $P(\mathrm{correct} \mid \hat g \neq 0)$", "b")):
        for est in EST4:
            g = g14[g14.estimator == est]
            x = float(s.loc[est, "stage7_population_slope"])
            kw = ST.marker_kw(est, 5.0 if est == "swap_destructive" else 3.6)
            axis.vlines(x, g[col].min(), g[col].max(), color=kw["color"], lw=2.2, alpha=0.35)
            y = float(g[g.total_executions == FIXED_T_MARK][col].iloc[0])
            axis.errorbar([x], [y], xerr=[[x - s.loc[est, "replicate_pct_lo"]], [s.loc[est, "replicate_pct_hi"] - x]],
                          fmt=kw["marker"], color=kw["color"], mfc=kw["markerfacecolor"], mec=kw["color"], ms=kw["markersize"], lw=0.6,
                          label=kw["label"])
        axis.set_xlabel("shot-cost exponent [decades / qubit]")
        axis.set_ylabel(ylab)
        axis.set_xlim(0.45, 1.35)
        axis.set_ylim(-0.04, 1.04)
        ST.panel_label(axis, letter)
        panel("6", letter, source="results/b2_estimators/slope_summary.csv; results/b2_estimators/fixed_budget_failure_modes.csv",
              columns=f"estimator, stage7_population_slope, replicate_pct_lo/hi; n, total_executions, {col}",
              filters=f"slopes: quantity = median_log10_total_executions, fit_range = primary_2_20; failure: n = {FIXED_N}",
              aggregation=f"marker: value at T = {FIXED_T_MARK} total executions; shaded bar: range over T = 32..32768",
              ci="horizontal bar: 95% percentile interval of the slope over 10 replicate seeds", function="fig6")
    ax[1].axhline(0.5, color="0.4", lw=0.5, ls=":")
    ax[0].legend(loc="center left")
    return fig


FIGURES = {"fig1_same_landscape": fig1, "fig2_conditional_sign_law": fig2, "fig3_b1_scaling_rule": fig3,
           "fig4_four_estimators": fig4, "fig5_noise": fig5, "fig6_empirical_estimator_comparison": fig6}


# =================================================================================================================
def _git_head() -> str:
    try:
        h = subprocess.run(["git", "rev-parse", "HEAD"], cwd=S.ROOT, capture_output=True, text=True, encoding="utf-8").stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "src", "results"], cwd=S.ROOT, capture_output=True, text=True,
                               encoding="utf-8").stdout.strip()
        return h + ("+dirty" if dirty else "")
    except OSError:
        return "unknown"


def sources_md() -> str:
    L = ["# Figure sources", "", "Generated by `python -m qlo.paper.figures`. One row per panel; every plotted number comes from the file",
         "and columns listed. CI = the uncertainty drawn in the panel.", ""]
    for p in PANELS:
        L += [f"## Figure {p['figure']}{p['panel'].upper()}", "",
              f"- **Source:** {p['source']}", f"- **Columns:** {p['columns']}", f"- **Filters:** {p['filters']}",
              f"- **Aggregation:** {p['aggregation']}", f"- **CI:** {p['ci']}", f"- **Function:** `qlo.paper.figures.{p['function']}`",
              f"- **Output:** `paper/figures/{p['output']}`", ""]
    return "\n".join(L)


def build(out: Path, png: bool = True) -> dict:
    ST.apply()
    PANELS.clear()
    out.mkdir(parents=True, exist_ok=True)
    if png:
        (out / "png").mkdir(exist_ok=True)
    manifest = {"entrypoint": "python -m qlo.paper.figures", "git_commit": _git_head(),
                "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "figures": []}
    for name, fn in FIGURES.items():
        S.USED.clear()
        n0 = len(PANELS)
        fig = fn()
        bad = ST.check(fig)
        if bad:
            raise ValueError(f"{name} breaks the journal figure rules: " + "; ".join(bad[:5]))
        pdf = out / f"{name}.pdf"
        fig.savefig(pdf, metadata=PDF_META)
        files = [pdf]
        if png:
            fig.savefig(out / "png" / f"{name}.png", dpi=200, metadata=PNG_META)
            files.append(out / "png" / f"{name}.png")
        plt.close(fig)
        for p in PANELS[n0:]:
            p["output"] = pdf.name
        manifest["figures"].append({"name": name, "function": fn.__name__,
                                    "files": [{"filename": str(f.relative_to(out)), "sha256": S.sha256(f)} for f in files],
                                    "panels": [p["panel"] for p in PANELS[n0:]],
                                    "sources": [{"path": k, "sha256": v} for k, v in sorted(S.USED.items())]})
    (out / "FIGURE_SOURCES.md").write_text(sources_md(), encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", type=Path, default=OUT)
    ap.add_argument("--no-png", action="store_true")
    a = ap.parse_args(argv)
    m = build(a.out_dir, png=not a.no_png)
    print(f"{len(m['figures'])} figures, {sum(len(f['panels']) for f in m['figures'])} panels -> {a.out_dir}")


if __name__ == "__main__":
    main()
