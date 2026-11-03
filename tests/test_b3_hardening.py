"""B3 statistical hardening tests: deterministic properties only (no statistical pass/fail thresholds)."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from qlo.experiments import b3_hardening as B3
from qlo.experiments.stage7 import Stage7Config, fit_table
from qlo.hardening import bootstrap as BS
from qlo.hardening import intervals as IV
from qlo.hardening import numerics as NUM
from qlo.hardening import seed_replicates as SR
from qlo.stage5.theory import log_a_k, s_k
from qlo.stage6.directional import direction_probabilities
from qlo.stage7 import analysis as AN
from qlo.stage7 import required_shots as R
from qlo.stage7.estimators import pair

STAGE7 = Path(__file__).resolve().parents[1] / "results" / "stage7"


# 1, 2: seeds
def test_seed_list_unique_and_disjoint_from_stage7():
    assert len(set(SR.B3_SEEDS)) == len(SR.B3_SEEDS) >= 20
    assert SR.STAGE7_SEED == Stage7Config().seed
    assert SR.STAGE7_SEED not in SR.B3_SEEDS
    assert SR.check_seeds(SR.B3_SEEDS) == SR.B3_SEEDS
    with pytest.raises(ValueError):
        SR.check_seeds((10000, 10001, 10000))
    with pytest.raises(ValueError):
        SR.check_seeds((10000, SR.STAGE7_SEED))
    assert B3.B3Config().seeds == SR.B3_SEEDS and SR.STAGE7_SEED not in B3.B3Config().seeds


# 3: LE and SWAP on exactly the same theta within a seed; different seeds give different theta
def test_schemes_paired_within_seed():
    res = SR.required_shots_per_theta(6, 300, 10003)
    th = AN.sample_theta(6, 300, 10003, SR.REQ_STREAM)
    assert np.array_equal(res["logA"], log_a_k(th, 0)) and np.array_equal(res["s"], s_k(th, 0))
    for sc in ("loschmidt", "swap"):   # every series is a function of the ONE (logA, s) array
        i = SR.SERIES.index((sc, "snr1"))
        assert np.array_equal(res["vals"][i], R.snr_shots(sc, res["logA"], res["s"], 1.0))
    other = AN.sample_theta(6, 300, 10004, SR.REQ_STREAM)
    assert not np.allclose(th, other)
    fx = SR.fixed_shot_per_theta(6, (64,), 200, 10003)
    th_f = AN.sample_theta(6, 200, 10003, SR.FIXED_STREAM)
    assert np.array_equal(fx["s"], s_k(th_f, 0))
    assert fx["loschmidt"].shape == fx["swap"].shape == (1, 3, 200)


# 4: theta bootstrap applies the same resampled indices to LE and SWAP
def test_bootstrap_keeps_pairing():
    rng = np.random.default_rng(1)
    base = rng.normal(size=(1, 501))
    pop = {n: np.vstack([base + n, base + n + 7.25]) for n in (2, 4, 6)}
    meds = BS.theta_bootstrap(pop, (2, 4, 6), 50, 3)
    assert np.allclose(meds[:, 1, :] - meds[:, 0, :], 7.25, atol=1e-12)
    assert meds[:, 0, 0].std() > 0   # it does resample
    b = BS.bootstrap_fixed_medians({"le": base, "sw": base * 2.0}, 40, 5)
    assert np.allclose(b["sw"], 2.0 * b["le"])


def test_count_median_equals_numpy_median():
    rng = np.random.default_rng(2)
    v = rng.normal(size=(3, 400))
    v[1, ::7] = np.nan
    cm = BS.CountMedian(v)
    for _ in range(25):
        idx = rng.integers(0, 400, 400)
        got = cm.medians(np.bincount(idx, minlength=400))
        want = [np.median(r[idx][np.isfinite(r[idx])]) for r in v]
        assert np.allclose(got, want, rtol=0, atol=1e-14)


# 5: per-theta pipeline and seed-level fit reproduce the Stage 7 implementation on the same data
def test_seed_fit_reproduces_stage7_implementation():
    rows, res = [], []
    for n in (2, 4, 6):
        res = SR.required_shots_per_theta(n, 250, SR.STAGE7_SEED)
        st7 = AN.required_shots_for_n(n, 250, SR.STAGE7_SEED)
        ours = {(r["scheme"], r["target"]): r["median_log10M"] for r in SR.medians_and_methods(res)}
        for row in st7["rows"]:
            for tag, _, _ in SR.TARGETS:
                assert ours[(row["scheme"], tag)] == row[f"{tag}_log10M_median"]
        rows += st7["rows"]
    st7_fits = fit_table(pd.DataFrame(rows))
    for sc, tag in SR.SERIES:
        d = pd.DataFrame(rows)
        d = d[d.scheme == sc].sort_values("n")
        f = SR.fit_series(d.n.values, d[f"{tag}_log10M_median"].values)
        assert abs(f["slope"] - st7_fits[f"{sc}_{tag}"]["slope"]) < 1e-13
        s_vec, _ = IV.ols_slopes(d.n.values, d[f"{tag}_log10M_median"].values[None, :])
        assert abs(s_vec[0] - f["slope"]) < 1e-12


# 6: the RX-product baseline point estimates are reproduced (closed-form targets at the full Stage 7 size)
def test_rx_baseline_snr_reproduced():
    summ = pd.read_csv(STAGE7 / "scaling_summary.csv")
    fits = json.loads((STAGE7 / "scaling_fits.json").read_text(encoding="utf-8"))["fits"]
    for sc in ("loschmidt", "swap"):
        for tag, rho in (("snr1", 1.0), ("snr2", 2.0)):
            meds = []
            for n in SR.PRIMARY_N:
                th = AN.sample_theta(n, Stage7Config().n_samples, SR.STAGE7_SEED, SR.REQ_STREAM)
                m = SR.finite_median(R.snr_shots(sc, log_a_k(th, 0), s_k(th, 0), rho))
                ref = float(summ[(summ.n == n) & (summ.scheme == sc)][f"{tag}_log10M_median"].iloc[0])
                assert abs(m - ref) < 1e-12
                meds.append(m)
            assert abs(SR.fit_series(SR.PRIMARY_N, meds)["slope"] - fits[f"{sc}_{tag}"]["slope"]) < 1e-12


# 7: interval helpers
def test_intervals_ordered_and_finite():
    x = np.random.default_rng(4).normal(0.6, 0.01, 20)
    lo, hi = IV.percentile_interval(x)
    s = IV.summarize(x, 2000, 1)
    assert np.isfinite([lo, hi]).all() and lo <= hi
    assert s["min"] <= s["pct_lo"] <= s["median"] <= s["pct_hi"] <= s["max"]
    assert s["boot_lo"] <= s["mean"] <= s["boot_hi"] and s["q25"] <= s["q75"]
    assert np.isnan(IV.percentile_interval([np.nan, np.nan])[0])


# 8: exponent-gap CI uses seed-paired values
def test_gap_is_seed_paired():
    with pytest.raises(ValueError):
        IV.paired_gap([1.0, 2.0], [1.0])
    rng = np.random.default_rng(5)
    seeds = SR.B3_SEEDS[:6]
    le = rng.normal(0.6, 0.01, 6)
    sw = le + 0.6 + rng.normal(0, 1e-4, 6)    # strongly correlated with le within a seed
    rows = []
    for sd, a, b in zip(seeds, le, sw):
        for sc, v in (("loschmidt", a), ("swap", b)):
            for tag, _, _ in SR.TARGETS:
                rows.append({"seed": sd, "scheme": sc, "target": tag, "fit_range": "primary_2_20", "slope": v,
                             "r2": 1.0, "ols_slope_se_diagnostic": 0.0})
    fits = pd.DataFrame(rows).sample(frac=1.0, random_state=0)   # shuffled: pairing must come from the seed key
    cfg = B3.B3Config(seeds=seeds, n_boot_seed=500)
    g = B3.seed_summary(fits, cfg)
    row = g[g.metric == "gap_swap_minus_le_snr1"].iloc[0]
    assert abs(row["mean"] - np.mean(sw - le)) < 1e-12
    assert row["sd"] < 1e-3   # an unpaired difference would carry the 0.01 between-seed spread


# 9: bootstrap determinism
def test_bootstrap_deterministic():
    pop = {n: np.random.default_rng(n).normal(size=(2, 300)) for n in (2, 4)}
    a = BS.theta_bootstrap(pop, (2, 4), 20, 11)
    b = BS.theta_bootstrap(pop, (2, 4), 20, 11)
    c = BS.theta_bootstrap(pop, (2, 4), 20, 12)
    assert np.array_equal(a, b) and not np.array_equal(a, c)
    pops = {sd: pop for sd in (1, 2, 3)}
    assert np.array_equal(BS.hierarchical_bootstrap(pops, (1, 2, 3), (2, 4), 10, 4), BS.hierarchical_bootstrap(pops, (1, 2, 3), (2, 4), 10, 4))
    assert IV.bootstrap_mean_ci([1, 2, 3, 4], 300, 7) == IV.bootstrap_mean_ci([1, 2, 3, 4], 300, 7)


# 10: n-extension rejects invalid points instead of accepting them
def test_extension_rejects_invalid_points():
    res = SR.required_shots_per_theta(8, 120, 10001)
    assert NUM.validate_required_point(res)["accepted"]
    bad = {**res, "vals": res["vals"].copy()}
    bad["vals"][SR.SERIES.index(("swap", "dir0.9")), 3] = np.nan
    assert not NUM.validate_required_point(bad)["accepted"]
    under = {**res, "logA": res["logA"].copy()}
    under["logA"][0] = -800.0      # exp underflows to 0
    c = NUM.validate_required_point(under)
    assert not c["no_underflow"] and not c["accepted"]
    wrong = {**res, "vals": res["vals"].copy()}
    i = SR.SERIES.index(("loschmidt", "dir0.9"))
    ex = np.flatnonzero(res["meth"][i] == R.METHOD["exact"])
    wrong["vals"][i, ex] -= 0.5     # a mis-inverted (too small) budget
    assert not NUM.validate_required_point(wrong)["accepted"]


# 11: fixed-shot probabilities stay in [0, 1]
def test_fixed_shot_probabilities_in_unit_interval():
    fx = SR.fixed_shot_per_theta(20, (16, 1024, 65536), 150, 10002)
    for key in ("loschmidt", "swap", "loschmidt_cond_accurate"):
        v = fx[key][np.isfinite(fx[key])]
        assert v.size and v.min() >= 0.0 and v.max() <= 1.0
    th = AN.sample_theta(4, 50, 10002, 1)
    A, s = np.exp(log_a_k(th, 0)), s_k(th, 0)
    p_pos, p_neg, _ = pair("loschmidt", A, s)
    acc = SR.direction_accurate(p_pos, p_neg, 64.0)
    ref = direction_probabilities(p_pos, p_neg, 64.0)   # no cancellation at n = 4: the two must agree
    assert np.allclose(acc["p_correct"], ref["p_correct"], atol=1e-12)
    assert np.allclose(acc["p_nonzero"], 1 - ref["p_zero"], atol=1e-12)


# 12: every compared arm starts from the identical theta
def test_paired_starts_identical():
    variants = [("exact", None, 0), ("SWAP M=64", "swap", 64), ("SWAP-noise random walk M=64", "swap_null", 64), ("LE M=64", "loschmidt", 64)]
    runs, _ = AN.optimization_diagnostic((6,), variants, 5, 3, 0.3, 10007)
    f0 = runs.pivot(index="seed", columns="variant", values="F0")
    assert (f0.nunique(axis=1) == 1).all()
    x, y = runs[runs.variant == "SWAP M=64"].copy(), runs[runs.variant == "exact"].copy()
    B3._pair_stats(x, y)
    y.loc[y.index[0], "F0"] += 1e-9
    with pytest.raises(AssertionError):
        B3._pair_stats(x, y)


def test_vector_reliability_schemes_share_theta(monkeypatch):
    seen = {}
    orig = AN.sample_gradient

    def spy(scheme, th, M, rng):
        seen.setdefault(scheme, th.copy())
        return orig(scheme, th, M, rng)

    monkeypatch.setattr(AN, "sample_gradient", spy)
    AN.vector_reliability((6,), (64,), 10, 2, 10011)
    assert set(seen) == {"loschmidt", "swap"} and np.array_equal(seen["loschmidt"], seen["swap"])
