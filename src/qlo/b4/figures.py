"""B4 figures (plain matplotlib, read from the result CSVs)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

L2, L4, L8, L16 = (float(np.log10(v)) for v in (2, 4, 8, 16))


def _plt():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    return plt


def _save(fig, path, plt):
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def _pcolor(ps):
    cmap = __import__("matplotlib").colormaps["viridis"]
    return {p: cmap(i / max(1, len(ps) - 1)) for i, p in enumerate(ps)}


def all_figures(out: Path, cfg) -> None:
    plt = _plt()
    figs = out / "figures"
    med = pd.read_csv(out / "sample_summary.csv")
    win = pd.read_csv(out / "window_slopes.csv")
    pr = pd.read_csv(out / "predictions_vs_measured.csv")
    gp = list(cfg.global_p)
    col = _pcolor(gp)

    # 1 RX global: shot scaling
    rx = med[(med.family == "rx_product") & (med.model == "global")]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for ax, c, title in ((axes[0], "median_log10_M_LE", "Loschmidt"), (axes[1], "median_log10_M_SWAP", "SWAP")):
        for p in gp:
            g = rx[rx.p == p].groupby("n")[c].mean()
            ax.plot(g.index, g.values, "o-", ms=3, color=col[p], label=f"p = {p:g}")
        ax.set_title(f"RX product, global depolarizing: {title}", fontsize=10)
        ax.set_xlabel("n")
    axes[0].set_ylabel("median log10 M (SNR 1, seed mean)")
    axes[0].legend(fontsize=8)
    _save(fig, figs / "rx_global_shot_scaling.png", plt)

    # 2 transition profile
    w = win[(win.family == "rx_product") & (win.model == "global")]
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for ax, m, refs in ((axes[0], "b_LE", (L4, L8)), (axes[1], "b_SWAP", (L16,)), (axes[2], "b_r", (0.0, L2))):
        for p in gp:
            g = w[w.p == p]
            ax.plot(g.n_mid, g[m], "o-", ms=3, color=col[p], label=f"p = {p:g}")
        for v in refs:
            ax.axhline(v, color="0.5", ls=":", lw=0.8)
        ax.set_title(f"local slope of {m} (3-point windows)", fontsize=10)
        ax.set_xlabel("window centre n")
    axes[0].legend(fontsize=7)
    axes[0].text(0.02, 0.02, "dotted: log10 4 and log10 8", transform=axes[0].transAxes, fontsize=7)
    _save(fig, figs / "transition_profile_rx_global.png", plt)

    # 3 exponent ratio vs p
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for ax, rname in zip(axes, ("primary", "secondary_n_ge_8")):
        d = pr[(pr.fit_range == rname) & (pr.model == "global")]
        for (fam, reg, pos), g in d.groupby(["family", "regime", "position"], sort=False):
            g = g.sort_values("p")
            x = np.where(g.p > 0, g.p, 1e-5)
            ax.semilogx(x, g.measured_ratio_obs, "o-" if fam == "rx_product" else ".-", lw=1.5 if fam == "rx_product" else 0.6,
                        color="k" if fam == "rx_product" else None, alpha=1 if fam == "rx_product" else 0.5)
        l = pr[(pr.fit_range == rname) & (pr.model == "local")].sort_values("p")
        ax.semilogx(np.where(l.p > 0, l.p, 1e-5), l.measured_ratio_obs, "s--", color="C3", label="RX product, local noise")
        ax.axhline(2.0, color="0.5", ls=":", lw=0.8)
        ax.axhline(4 / 3, color="0.5", ls="--", lw=0.8)
        ax.set_title(f"b_SWAP / b_LE ({rname}); black = RX global, thin = B1 cells; p = 0 drawn at 1e-5", fontsize=8)
        ax.set_xlabel("p")
    axes[0].set_ylabel("exponent ratio")
    axes[0].legend(fontsize=7)
    _save(fig, figs / "exponent_ratio_vs_noise.png", plt)

    # 4 b_r measured vs asymptotic prediction
    fig, ax = plt.subplots(figsize=(5.6, 5))
    d = pr[(pr.p > 0) & (pr.fit_range == "secondary_n_ge_8")]
    for model, mk in (("global", "o"), ("local", "s")):
        g = d[d.model == model]
        ax.scatter(g.asym_b_r, g.measured_b_r, c=np.log10(g.p), marker=mk, s=18, label=model, cmap="viridis")
    lim = [min(d.asym_b_r.min(), d.measured_b_r.min()) - 0.01, max(d.asym_b_r.max(), d.measured_b_r.max()) + 0.01]
    ax.plot(lim, lim, "k-", lw=0.8, label="measured = asymptote")
    ax.axhline(0, color="0.6", lw=0.5)
    ax.set_xlabel("asymptotic b_r' (Prop. 5 / 6)")
    ax.set_ylabel("measured b_r' (n >= 8)")
    ax.set_title("relative-gradient exponent under noise (colour = log10 p)", fontsize=9)
    ax.legend(fontsize=7)
    _save(fig, figs / "br_measured_vs_asymptote.png", plt)

    # 5 local noise: b_S vs formula
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    for rname, mk in (("primary", "o"), ("secondary_n_ge_8", "s")):
        g = pr[(pr.model == "local") & (pr.fit_range == rname)].sort_values("p")
        ax.semilogx(g.p, g.measured_b_S, mk, label=f"measured b_S' ({rname})")
    pp = np.logspace(-3.2, -0.9, 100)
    ax.semilogx(pp, -(2 / np.log(10)) * np.log((np.sqrt(1 - pp / 2) + np.sqrt(pp / 2)) / 2), "k-", lw=0.8, label="Prop. 6 formula")
    ax.set_xlabel("local depolarizing p")
    ax.set_ylabel("b_S'")
    ax.legend(fontsize=7)
    ax.set_title("RX product, local depolarizing", fontsize=9)
    _save(fig, figs / "local_noise_bS_vs_formula.png", plt)

    # 6 gap rule under noise
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    for rname, ls in (("primary", "-"), ("secondary_n_ge_8", "--")):
        d = pr[(pr.fit_range == rname) & (pr.model == "global")]
        q = d.groupby("p").measured_eps_gap.agg(["min", "max", "median"])
        x = np.where(q.index > 0, q.index, 1e-5)
        ax.fill_between(x, q["min"], q["max"], alpha=0.2)
        ax.semilogx(x, q["median"], ls, label=f"global, {rname}: median and range over cells")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel("p (p = 0 at 1e-5)")
    ax.set_ylabel("eps_gap = (b_SWAP - b_LE) - b_S")
    ax.legend(fontsize=7)
    ax.set_title("general slope rule under global depolarizing", fontsize=9)
    _save(fig, figs / "gap_rule_under_noise.png", plt)
