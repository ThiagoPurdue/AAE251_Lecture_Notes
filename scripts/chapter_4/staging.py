"""Multistage rockets (page 4.3): stages sized from the payload down, identical stages, and the split
of the delta-V between two stages. SI units: kg, m/s.

Stage numbering as the pages write it: stage 1 is the lowest, the first to burn; the payload of
stage k is everything above it. Every list in this module is in stage order, stage 1 first, and the
sizing runs from the top stage down, because the top stage's payload is the only mass known first.

The initial mass is the payload times one factor per stage,
    m_i = m_pay * prod_k e^(x_k) (1 - f_k) / (1 - f_k e^(x_k)),   x_k = dV_k / c_k,
and for two stages ln m_i is smallest where its slope against dV_1 is zero, which gives
    c_1 (1 - f_1 e^(x_1)) = c_2 (1 - f_2 e^(x_2)).
Sources: Sutton and Biblarz, Rocket Propulsion Elements, Chapter 4 (multistage vehicles); Humble,
Henry and Larson, Space Propulsion Analysis and Design (1995), Chapter 3 (staging).

Run this file for its unit checks:  python3 -B scripts/chapter_4/staging.py
"""
import math
import sys
from pathlib import Path

import numpy as np

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from chapter_4.rocket import size_stage, stage_factor, single_stage_limit, c_from_isp, StageLimitError  # noqa: E402

__all__ = ["size_stages", "identical_stages", "identical_limit", "split_mass", "split_sweep", "best_split",
           "split_condition"]


def _cs(cs=None, isps=None):
    if cs is not None:
        return [float(c) for c in cs]
    return [c_from_isp(i) for i in isps]


def size_stages(m_pay, dvs, cs=None, fs=None, isps=None):
    """Size n stages from the top down. dvs, cs (m/s; or isps in s) and fs (inert mass fractions) are
    lists in stage order, stage 1 (the lowest) first. Returns a list of per-stage dicts, stage 1 first,
    each the result of rocket.size_stage for that stage plus `stage` (its number) and `above` (the mass
    above it: its payload). The vehicle's initial mass is result[0]["m_i"]. Raises StageLimitError when
    a stage is past its limit.
    Example: size_stages(1750.0, [2012.0, 1404.0], isps=[323.0, 323.0], fs=[0.17, 0.17])[0]["m_i"] -> 7,095"""
    cs = _cs(cs, isps)
    n = len(dvs)
    if not (len(cs) == len(fs) == n):
        raise ValueError("dvs, cs (or isps) and fs must have one entry per stage")
    out = [None] * n
    above = float(m_pay)
    for k in range(n - 1, -1, -1):                       # the top stage first
        s = size_stage(above, float(dvs[k]), c=cs[k], f_inert=float(fs[k]))
        s["stage"], s["above"] = k + 1, above
        out[k] = s
        above = s["m_i"]
    return out


def identical_stages(m_pay, dv, n, c=None, f=None, isp=None):
    """n identical stages sharing the delta-V equally: m_i = m_pay * factor(dV/n)^n (kg).
    Raises StageLimitError past n c ln(1/f). Example: identical_stages(750.0, 8833.0, 2, isp=330.0, f=0.08) -> 20,594"""
    c = c if c is not None else c_from_isp(isp)
    return m_pay * stage_factor(dv / n, c, f) ** n


def identical_limit(n, c=None, f=None, isp=None):
    """The largest delta-V of n identical stages, n c ln(1/f) (m/s). Example: identical_limit(2, isp=330.0, f=0.08) -> 16,354"""
    c = c if c is not None else c_from_isp(isp)
    return n * single_stage_limit(c, f)


def split_mass(m_pay, dv, share1, stage1, stage2):
    """Initial mass (kg) of a two-stage vehicle when stage 1 gives the share `share1` of dv (0 to 1).
    stage1, stage2: dicts with c (m/s) or isp (s), and f (the inert mass fraction). nan when a stage
    is past its limit. Example: split_mass(750.0, 8833.0, 0.5, dict(isp=330.0, f=0.08), dict(isp=330.0, f=0.08)) -> 20,594"""
    c1 = stage1.get("c") or c_from_isp(stage1["isp"])
    c2 = stage2.get("c") or c_from_isp(stage2["isp"])
    try:
        return m_pay * stage_factor(share1 * dv, c1, stage1["f"]) * stage_factor((1.0 - share1) * dv, c2, stage2["f"])
    except StageLimitError:
        return float("nan")


def split_sweep(m_pay, dv, stage1, stage2, shares):
    """Initial mass (kg) against the share of stage 1 for an array of shares; nan where a stage is past
    its limit (draw the regions with nan as shaded). Example: split_sweep(750.0, 8833.0, s1, s2, np.linspace(0, 1, 401))"""
    return np.array([split_mass(m_pay, dv, float(a), stage1, stage2) for a in np.asarray(shares, float)])


def split_condition(dv, share1, stage1, stage2):
    """The two sides of the best-split condition, (c_1 (1 - f_1 e^(x_1)), c_2 (1 - f_2 e^(x_2))): equal at the
    best split. Example: split_condition(8833.0, 0.5, s, s) -> (a, a) for identical stages"""
    c1 = stage1.get("c") or c_from_isp(stage1["isp"])
    c2 = stage2.get("c") or c_from_isp(stage2["isp"])
    x1, x2 = share1 * dv / c1, (1.0 - share1) * dv / c2
    return c1 * (1.0 - stage1["f"] * math.exp(x1)), c2 * (1.0 - stage2["f"] * math.exp(x2))


def best_split(m_pay, dv, stage1, stage2, tol=1e-12):
    """The share of stage 1 that gives the smallest initial mass, found numerically (golden-section
    search on ln m_i between the two limits). Asserts that the result satisfies the condition
    c_1 (1 - f_1 e^(x_1)) = c_2 (1 - f_2 e^(x_2)). Returns a dict: share1, dv1, dv2, m_i.
    Example: best_split(750.0, 8833.0, dict(isp=330.0, f=0.08), dict(isp=330.0, f=0.08))["share1"] -> 0.5000"""
    c1 = stage1.get("c") or c_from_isp(stage1["isp"])
    c2 = stage2.get("c") or c_from_isp(stage2["isp"])
    lo = max(0.0, 1.0 - single_stage_limit(c2, stage2["f"]) / dv)      # stage 2 at its limit
    hi = min(1.0, single_stage_limit(c1, stage1["f"]) / dv)            # stage 1 at its limit
    if not lo < hi:
        raise StageLimitError(f"no split of {dv:g} m/s works for these two stages")
    eps = 1e-9 * (hi - lo)
    a, b = lo + eps, hi - eps
    g = (math.sqrt(5.0) - 1.0) / 2.0

    def F(s):
        return math.log(split_mass(m_pay, dv, s, stage1, stage2))
    x1, x2 = b - g * (b - a), a + g * (b - a)
    f1, f2 = F(x1), F(x2)
    while b - a > tol:
        if f1 < f2:
            b, x2, f2 = x2, x1, f1
            x1 = b - g * (b - a)
            f1 = F(x1)
        else:
            a, x1, f1 = x1, x2, f2
            x2 = a + g * (b - a)
            f2 = F(x2)
    s = 0.5 * (a + b)
    left, right = split_condition(dv, s, stage1, stage2)
    assert abs(left - right) <= 1e-5 * max(abs(left), abs(right)), \
        f"best split does not satisfy c1(1 - f1 e^x1) = c2(1 - f2 e^x2): {left} vs {right}"
    return dict(share1=s, dv1=s * dv, dv2=(1.0 - s) * dv, m_i=split_mass(m_pay, dv, s, stage1, stage2))


# ===================================================================== unit checks
if __name__ == "__main__":
    from chapter_4.rocket import delta_v

    def close(a, b, tol, what):
        assert abs(a - b) <= tol * max(1.0, abs(b)), f"{what}: {a!r} vs {b!r}"

    c = c_from_isp(323.0)
    # n = 1: the stage list is the single stage
    one = size_stages(1750.0, [3416.0], cs=[c], fs=[0.17])
    close(one[0]["m_i"], size_stage(1750.0, 3416.0, c=c, f_inert=0.17)["m_i"], 1e-12, "one stage = size_stage")
    close(identical_stages(1750.0, 3416.0, 1, c=c, f=0.17), one[0]["m_i"], 1e-12, "n = 1 identical")
    # two stages: each stage's payload is the mass above it; the delta-Vs add up; product of factors
    two = size_stages(1750.0, [2012.0, 1404.0], cs=[c, c], fs=[0.17, 0.17])
    close(two[0]["above"], two[1]["m_i"], 1e-12, "payload of stage 1 = initial mass of stage 2")
    close(sum(delta_v(s["c"], s["m_i"], s["m_f"]) for s in two), 3416.0, 1e-12, "stage delta-Vs add up")
    close(two[0]["m_i"], 1750.0 * stage_factor(2012.0, c, 0.17) * stage_factor(1404.0, c, 0.17), 1e-12, "factors")
    assert two[0]["m_i"] < one[0]["m_i"], "two stages are lighter than one for the same job"
    # identical stages: the factor to the power n; equal stages through size_stages agree
    for n in (2, 3):
        st = size_stages(750.0, [8833.0 / n] * n, cs=[c_from_isp(330.0)] * n, fs=[0.08] * n)
        close(st[0]["m_i"], identical_stages(750.0, 8833.0, n, isp=330.0, f=0.08), 1e-12, f"{n} identical stages")
    # more stages are always lighter in this model, by less each time
    m = [identical_stages(750.0, 8833.0, n, isp=330.0, f=0.08) for n in (2, 3, 4)]
    assert m[0] > m[1] > m[2] and m[0] - m[1] > m[1] - m[2], m
    # the best split of identical stages is equal; it satisfies the condition; the sweep's minimum agrees
    S = dict(isp=330.0, f=0.08)
    b = best_split(750.0, 8833.0, S, S)
    close(b["share1"], 0.5, 1e-6, "identical stages: equal split")
    A, B = dict(isp=305.0, f=0.065), dict(isp=355.0, f=0.12)
    b = best_split(750.0, 8833.0, A, B)
    sh = np.linspace(0.0, 1.0, 20001)
    sw = split_sweep(750.0, 8833.0, A, B, sh)
    close(sh[np.nanargmin(sw)], b["share1"], 1e-4, "best split = minimum of the sweep")
    assert np.isnan(sw[0]) or np.isnan(sw[-1]), "a stage past its limit gives nan"
    print("staging.py: all unit checks passed")
