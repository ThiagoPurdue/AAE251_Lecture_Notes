from chapter_4.common import *  # noqa: F401,F403
"""Page 4.3, Multistage Rockets: figures and printed values.

Worked examples (invented vehicles on the missions the book has already priced):
  1. Two stages, one for each burn of the Hohmann transfer of page 2.2 (2.012 and 1.404 km/s), the
     payload, engine and inert mass fraction of page 4.2's single stage (1,750 kg, 323 s, 0.17).
  2. The launch of page 2.3 (8.833 km/s with its losses) with one, two, three and four identical
     stages (750 kg, 330 s, 0.08).
  3. The same launch with two different stages (stage 1: 310 s, 0.065; stage 2: 440 s, 0.13): an
     equal split, a split that gives stage 2 more, and the best split.
A real vehicle: the three Saturn V stages of Apollo 11 (AS-506), masses from Orloff, Apollo by the
Numbers (SP-2000-4029), specific impulse and cutoff velocity from the AS-506 flight evaluation report.

Every worked step on the page is computed here from the digits printed before it (`chain`), so the
printed chain closes; the figures use full precision.
"""

from matplotlib.patches import Rectangle  # noqa: E402  (the window of panel (b) of the split curve)

PAGE = "p43"

# ---------------------------------------------------------------- worked examples: the givens
EX1 = TRANSFER_STAGE                                        # page 4.2's transfer stage (links.py)
EX2 = dict(m_pay=750.0, isp=330.0, f=0.08)                  # the launch of page 2.3, identical stages
EX3 = dict(m_pay=750.0, s1=dict(isp=310.0, f=0.065), s2=dict(isp=440.0, f=0.13))
EX3_SPLIT_B = 3200.0                                        # m/s given to stage 1 in the second trial split
N_MAX = 4                                                   # identical stages compared: 1 to 4


km_printed = km_as_printed                                   # links.py

DV1 = km_printed(HOHMANN_22["dv1"])                          # 2,012 m/s
DV2 = km_printed(HOHMANN_22["dv2"])                          # 1,404 m/s
DV_HOH = km_printed(HOHMANN_22["dv_total"])                  # 3,416 m/s
DV_LAUNCH = km_printed(LAUNCH_23["total"])                   # 8,833 m/s


def num(s):
    """The value of a printed string ("3,168.6" -> 3168.6)."""
    return float(s.replace(",", ""))


P = printed                                                 # (text, value as printed): chapter_4.style


def ex1():
    """Two stages, one per Hohmann burn, stage 2 sized first. Full precision and the printed chain."""
    full = size_stages(EX1["m_pay"], [DV1, DV2], isps=[EX1["isp"]] * 2, fs=[EX1["f"]] * 2)
    one = size_stage(EX1["m_pay"], DV_HOH, isp=EX1["isp"], f_inert=EX1["f"])
    f = EX1["f"]
    c_s, c = P(c_from_isp(EX1["isp"]), 5)                   # 3,168.6 m/s
    ch = {"c": c_s}
    m_pay = EX1["m_pay"]
    for k, dv in ((2, DV2), (1, DV1)):
        x_s, x = P(dv / c, 5)
        e_s, e = P(math.exp(x), 5)
        n_s, n = P(m_pay * (e - 1.0) * (1.0 - f), 4)
        d_s, d = P(1.0 - f * e, 4)
        mp_s, mp = P(n / d, 4)
        mi_s, mi_ = P(f / (1.0 - f) * mp, 4)
        mf_s, mf = P(m_pay + mi_, 4)
        m0_s, m0 = P(mf + mp, 4)
        ch[k] = dict(x=x_s, e=e_s, num=n_s, den=d_s, m_prop=mp_s, m_inert=mi_s, m_f=mf_s, m_i=m0_s,
                     m_pay=fmt(m_pay), ratio=fmt(m0 / mf, 4))
        m_pay = m0
    return full, one, ch


def identical(n, m_pay=EX2["m_pay"], dv=DV_LAUNCH, isp=EX2["isp"], f=EX2["f"]):
    """n identical stages, equal shares: the sized stages (full precision)."""
    return size_stages(m_pay, [dv / n] * n, isps=[isp] * n, fs=[f] * n)


def ex2():
    """One to four identical stages for the launch: full precision and the printed chain."""
    c_s, c = P(c_from_isp(EX2["isp"]), 5)                   # 3,237.3 m/s (exact)
    f = EX2["f"]
    ch = {"c": c_s}
    x_s, x = P(DV_LAUNCH / c, 5)
    e_s, e = P(math.exp(x), 4)
    ch[1] = dict(x=x_s, e=e_s, inv_f=fmt(1.0 / f, 4), limit=fmt(single_stage_limit(c, f)))
    for n in (2, 3):
        share_s, share = (fmt_dec(DV_LAUNCH / n, 1), DV_LAUNCH / n)
        xs, xv = P(share / c, 6)                           # shown for reference; e^x from the full ratio
        es, ev = P(math.exp(share / c), 6)
        nn_s, nn = P(ev * (1.0 - f), 6)
        dd_s, dd = P(1.0 - f * ev, 6)
        fac_s, fac = P(nn / dd, 6)
        mi_s, mi = P(EX2["m_pay"] * fac ** n, 4)
        ch[n] = dict(share=share_s, x=xs, e=es, num=nn_s, den=dd_s, factor=fac_s, m_i=mi_s)
    full = {n: identical(n) for n in range(2, N_MAX + 1)}
    for n in (2, 3):
        assert fmt(full[n][0]["m_i"]) == ch[n]["m_i"], (n, full[n][0]["m_i"], ch[n]["m_i"])
    return full, ch


def ex3_trials():
    """The three splits of worked example 3: equal, stage 1 given EX3_SPLIT_B, and the best."""
    b = best_split(EX3["m_pay"], DV_LAUNCH, EX3["s1"], EX3["s2"])
    trials = [("equal", 0.5 * DV_LAUNCH), ("B", EX3_SPLIT_B), ("best", b["dv1"])]
    out = []
    for name, d1 in trials:
        st = size_stages(EX3["m_pay"], [d1, DV_LAUNCH - d1], isps=[EX3["s1"]["isp"], EX3["s2"]["isp"]],
                         fs=[EX3["s1"]["f"], EX3["s2"]["f"]])
        cond = split_condition(DV_LAUNCH, d1 / DV_LAUNCH, EX3["s1"], EX3["s2"])
        out.append(dict(name=name, dv1=d1, dv2=DV_LAUNCH - d1, share=d1 / DV_LAUNCH, stages=st, m_i=st[0]["m_i"],
                        cond=cond))
    return b, out


# ---------------------------------------------------------------- the Saturn V of Apollo 11
SV_NAMES = ("S-IC", "S-II", "S-IVB")


def saturn():
    """The three stages of the Apollo 11 Saturn V: mass at ignition and at burnout from the ground
    ignition weights (SP-2000-4029), ideal delta-V with each stage's specific impulse (AS-506 flight
    evaluation report). The interstage between the first two stages and the launch escape tower drop
    early in the second-stage burn: they are taken off at second-stage ignition."""
    W = SATURN_V_AS506
    tot = SATURN_V_AS506_TOTAL_LB
    stage_total = {k: W[k]["dry_lb"] + W[k]["ox_lb"] + W[k]["fuel_lb"] + W[k]["other_lb"] for k in SV_NAMES}
    les = SATURN_V_AS506_LES_LB
    ign = {"S-IC": tot}
    ign["S-II"] = tot - stage_total["S-IC"] - SATURN_V_AS506_INTERSTAGES_LB["S-IC/S-II"] - les
    ign["S-IVB"] = ign["S-II"] - stage_total["S-II"] - SATURN_V_AS506_INTERSTAGES_LB["S-II/S-IVB"]
    out = []
    for k in SV_NAMES:
        dry, prop = saturn_stage_kg(k)
        m0 = ign[k] * LB_KG
        m1 = m0 - prop
        c = c_from_isp(W[k]["isp"])
        out.append(dict(name=k, dry=dry, prop=prop, isp=W[k]["isp"], f=inert_mass_fraction(dry, prop), m_i=m0, m_f=m1,
                        ratio=m0 / m1, dv=delta_v(c, m0, m1), c=c, above=m0 - dry - prop - W[k]["other_lb"] * LB_KG,
                        v_cutoff=W[k]["v_cutoff"]))
    # the masses add up: the stage, its "other" items and everything above it make its ignition mass
    for s, k in zip(out, SV_NAMES):
        close_to(s["above"] + s["dry"] + s["prop"] + W[k]["other_lb"] * LB_KG, s["m_i"], 1e-9, "ignition mass", rel=True)
    return out




# ================================================================= figures
def _mass_rect(ax, x0, y0, w, h, kind, z=3.0, ghost=False):
    """One mass segment in the MASS_STYLE look of the chapter's mass bars (drawing4.fill_region: the hatch
    in HATCH_INK, a black outline), or a dashed empty outline for mass that is gone."""
    xy = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    if ghost:
        return ax.add_patch(Polygon(xy, closed=True, fc="none", ec=GRAY, lw=LW_THIN, ls=(0, (3.0, 2.0)), zorder=z))
    fp, ed = fill_region(ax, xy, MASS_STYLE[kind], z=z)
    return ed



def _key_axes(fig, rect, kinds=MASS_ORDER):
    """A small frameless equal-aspect axes at `rect` (figure fraction) holding the mass key, for a data plot."""
    W, H = fig.get_size_inches()
    axk = fig.add_axes(rect)
    w_in, h_in = rect[2] * W, rect[3] * H
    axk.set_xlim(0.0, w_in)
    axk.set_ylim(0.0, h_in)
    axk.set_aspect("equal")
    axk.axis("off")
    mass_key(axk, (0.05, 0.5 * h_in), kinds=kinds)
    return axk


def payload_of_a_stage():
    """Lesson: each stage carries everything above it as its payload: stage 1 carries stage 2 (with its
    engine), the fairing and the payload; stage 2 carries the payload."""
    F = FALCON9
    z_sep = F["stage1_len"] + F["interstage_len"]            # the separation plane: top of the interstage
    z_f0 = F["height"] - F["fairing_len"]                    # base of the fairing
    R, Rf = 0.5 * F["d"], 0.5 * F["fairing_d"]
    plain = two_stage_vehicle(payload="hidden", orientation="horizontal")
    cut = two_stage_vehicle(payload="hidden", cutaway=True, orientation="horizontal")
    # the outline of the plain vehicle; from the cut-open one, the interstage (open, its walls in section),
    # the second-stage engine inside it and the three first-stage engines in the section plane (plain bells)
    keep = ("first_stage", "second_stage", "fairing", "stage1_joint")
    full = {k: plain[k] for k in keep}
    full["interstage"] = cut["interstage"]
    for k in ("engine_1", "engine_2", "engine_3", "vacuum_engine"):
        full[k] = cut[k]
    full["vacuum_engine"].z = 2.9                            # behind stage 2: its top sits inside the stage
    dy = -16.0                                               # the second row: the upper piece alone
    upper_names = ("second_stage", "fairing", "vacuum_engine")
    upper = {}
    for k in upper_names:
        src = full[k]
        upper[k] = Part(k, np.asarray(src.xy, float) + np.array([0.0, dy]), src.kind, z=src.z,
                        inside=(src.inside[0], src.inside[1] + dy))
    fig, ax = canvas(6.5, xlim=(-1.0, 71.5), ylim=(-26.0, 9.4))
    P1 = draw_parts(ax, full, highlight=("second_stage", "fairing", "vacuum_engine"))
    P2 = draw_parts(ax, upper)
    for P in (P1, P2):                                       # engines as plain bells in thin line
        for k, pa in P.items():
            if k.startswith("engine_") or k == "vacuum_engine":
                pa.set_linewidth(LW_DETAIL)
    # the payload on its adapter, drawn solid in both rows (what rides inside the fairing)
    pay0, ada0 = plain["payload"].xy, plain["adapter"].xy
    for yoff in (0.0, dy):
        pay = pay0 + np.array([0.0, yoff])
        p0, p1 = float(pay[:, 0].min()), float(pay[:, 0].max())
        q0, q1 = float(pay[:, 1].min()), float(pay[:, 1].max())
        _mass_rect(ax, p0, q0, p1 - p0, q1 - q0, "payload", z=6.0)
        ax.add_patch(Polygon(ada0 + np.array([0.0, yoff]), closed=True, fc="white", ec=INK, lw=LW_DETAIL, zorder=6.0))
    x_nose = float(full["fairing"].xy[:, 0].max())
    x_tail = float(min(p.xy[:, 0].min() for k, p in full.items() if k.startswith("engine_")))
    x_mvac = float(full["vacuum_engine"].xy[:, 0].min())     # the exit of the second-stage engine
    # names inside the stages
    ax.text(0.5 * (5.0 + F["stage1_len"]), 0.0, "stage 1", ha="center", va="center", fontsize=FS_SMALL, color=INK,
            zorder=8)
    for y in (0.0, dy):
        ax.text(0.5 * (z_sep + z_f0), y, "stage 2", ha="center", va="center", fontsize=FS_SMALL, color=INK, zorder=8)
    # the separation plane: short marks outside the body, level with the joint
    for y in (0.0, dy):
        for s in (1, -1):
            ax.plot([z_sep, z_sep], [y + s * (R + 0.3), y + s * (R + 1.3)], color=INK, lw=LW_THIN, zorder=7)
    text(ax, (z_sep, R + 1.3), "stages separate", direction=90.0, dist=3.0, fs=FS_SMALL, backing=False)
    # the interstage, the second-stage engine and the payload adapter, named once each
    # the interstage leader ends on its lower wall between the bell's lip and the separation plane, where the
    # bell has narrowed well clear of the wall (it must not seem to name the bell)
    x_is = F["stage1_len"] + 1.0
    x_lead = x_mvac + 0.75 * (z_sep - x_mvac)
    vac = np.asarray(full["vacuum_engine"].xy, float)
    near = vac[np.abs(vac[:, 0] - x_lead) < 0.3]
    assert float(near[:, 1].min()) - (-R + F["wall"]) > 1.0, "the bell lies far inside the wall at the leader's end"
    label_part(ax, P1, full, "interstage", "interstage, stays\nwith stage 1", at=(x_is - 9.0, -R - 3.4),
               fs=FS_SMALL, ha="center", target=(x_lead, -R + 0.5 * F["wall"]))
    label_part(ax, P2, upper, "vacuum_engine", "stage 2 engine", at=(x_mvac - 6.5, dy + R + 3.2), fs=FS_SMALL,
               ha="center", target=(x_mvac + 1.2, dy + 0.9))
    ada = ada0 + np.array([0.0, dy])
    label_part(ax, P2, upper, "fairing", "payload adapter", at=(float(ada[:, 0].mean()), dy + Rf + 3.0),
               fs=FS_SMALL, ha="center", target=tuple(ada.mean(axis=0)))
    # row titles
    text(ax, (-0.8, 8.4), "while stage 1 burns", ha="left", va="center", backing=False, fs=FS_LABEL,
         fontweight="bold")
    text(ax, (-0.8, dy + 5.0), "while stage 2 burns", ha="left", va="center", backing=False, fs=FS_LABEL,
         fontweight="bold")
    # braces: the payload of each stage (stage 1's starts at the exit of the second-stage engine)
    yb = -Rf - 0.5
    brace(ax, (x_nose, yb), (x_mvac, yb), "payload of stage 1:\nstage 2, fairing and payload", side=1, fs=FS_SMALL)
    pay = pay0 + np.array([0.0, dy])
    p0, p1 = float(pay[:, 0].min()), float(pay[:, 0].max())
    yb2 = dy - Rf - 0.5
    brace(ax, (p1, yb2), (p0, yb2), "payload of stage 2", side=1, fs=FS_SMALL)
    # asserts: the vehicle keeps its published length; stage 2's engine sits inside the interstage, aft
    # of the separation plane; the payload lies inside the fairing
    close_to(x_nose - x_tail, F["height"], 1e-6, "the vehicle is 70 m long")
    assert x_tail < F["stage1_len"] < x_mvac < z_sep < z_f0 < p0 < p1 < x_nose, \
        "stage 1, the interstage holding stage 2's engine, stage 2, then the payload under the fairing"
    close_to(float(upper["second_stage"].xy[:, 0].min()), z_sep, 1e-9, "the upper piece starts at the separation plane")
    trim_canvas(fig)
    save_figure(fig, "p43-payload-of-a-stage")



def staging_sequence():
    """Lesson: dropping the empty first stage removes mass that the second burn would otherwise have to push."""
    full, one, ch = ex1()
    s1, s2 = full[0], full[1]
    m_pay = EX1["m_pay"]
    L = 7.6                                                  # drawn length of the full vehicle
    sc = L / s1["m_i"]
    fig, ax = canvas(6.5, xlim=(-3.9, 9.6), ylim=(-5.3, 1.95))
    h = 0.62
    seg_kinds = [("payload", m_pay), ("inert", s2["m_inert"]), ("propellant", s2["m_prop"]),
                 ("inert", s1["m_inert"]), ("propellant", s1["m_prop"])]
    starts = np.cumsum([0.0] + [m for _, m in seg_kinds])
    rows = [("first burn starts", [0, 1, 2, 3, 4], []),
            ("first burn ends", [0, 1, 2, 3], [4]),
            ("stage 1 dropped", [0, 1, 2], [3]),
            ("second burn ends", [0, 1], [2])]
    ys = [0.0, -1.4, -2.8, -4.2]
    x_tot = L + 0.25
    totals = []
    for i, ((name, keep, ghost), y) in enumerate(zip(rows, ys)):
        for j in keep:
            _mass_rect(ax, starts[j] * sc, y, seg_kinds[j][1] * sc, h, seg_kinds[j][0])
        for j in ghost:
            _mass_rect(ax, starts[j] * sc, y, seg_kinds[j][1] * sc, h, None, ghost=True)
        m = sum(seg_kinds[j][1] for j in keep)
        totals.append(m)
        step_marker(ax, (-3.6, y + 0.5 * h), i + 1)
        text(ax, (-3.2, y + 0.5 * h), name, ha="left", va="center", backing=False, fs=FS_SMALL)
        text(ax, (x_tot, y + 0.5 * h), f"{fmt(m)} kg", ha="left", va="center", backing=False, fs=FS_SMALL)
    # what is gone, named with its mass in or under its outline
    text(ax, ((starts[4] + 0.5 * seg_kinds[4][1]) * sc, ys[1] + 0.5 * h), f"burned, {fmt(seg_kinds[4][1])} kg",
         backing=False, fs=FS_SMALL, color=GRAY)
    text(ax, ((starts[3] + 0.5 * seg_kinds[3][1]) * sc, ys[2]), f"dropped, {fmt(seg_kinds[3][1])} kg", direction=-90.0,
         dist=4.0, fs=FS_SMALL, color=GRAY, backing=False)
    text(ax, ((starts[2] + 0.5 * seg_kinds[2][1]) * sc, ys[3]), f"burned, {fmt(seg_kinds[2][1])} kg", direction=-90.0,
         dist=4.0, fs=FS_SMALL, color=GRAY, backing=False)
    # the stages named above the first bar
    yt = h + 0.1
    for (a, b, lab) in ((0, 1, "payload"), (1, 3, "stage 2"), (3, 5, "stage 1")):
        brace(ax, (starts[a] * sc, yt), (starts[b] * sc, yt), lab, side=1, fs=FS_SMALL)
    mass_key(ax, (-3.75, -5.2))
    # asserts: the bars are to one scale; each row is the row above less what left
    close_to(totals[0], s1["m_i"], 1e-9, "row 1 is the initial mass", rel=True)
    close_to(totals[1], s1["m_f"], 1e-9, "row 2 is stage 1's final mass", rel=True)
    close_to(totals[2], s2["m_i"], 1e-9, "row 3 is stage 2's initial mass", rel=True)
    close_to(totals[3], s2["m_f"], 1e-9, "row 4 is stage 2's final mass", rel=True)
    for k, j in ((0, 4), (1, 3), (2, 2)):
        close_to(totals[k] - totals[k + 1], seg_kinds[j][1], 1e-9, "what leaves is the named segment", rel=True)
    trim_canvas(fig)
    save_figure(fig, "p43-staging-sequence")



def top_down():
    """Lesson: the sizing starts from the only mass known, the real payload, and works down: each stage
    multiplies the mass above it by its own factor, and its initial mass is the payload of the stage below."""
    full, one, ch = ex1()
    s1, s2 = full[0], full[1]
    m_pay = EX1["m_pay"]
    L = 7.6                                                  # the scale of p43-staging-sequence
    sc = L / s1["m_i"]
    fig, ax = canvas(6.5, xlim=(-3.9, 9.6), ylim=(-5.2, 0.9))
    h = 0.62
    seg_kinds = [("payload", m_pay), ("inert", s2["m_inert"]), ("propellant", s2["m_prop"]),
                 ("inert", s1["m_inert"]), ("propellant", s1["m_prop"])]
    starts = np.cumsum([0.0] + [m for _, m in seg_kinds])
    rows = [(3, "start at the top:\nthe real payload", [0]),
            (5, "its initial mass is\nthe payload of stage 1", [0, 1, 2]),
            (6, "gross liftoff mass", [0, 1, 2, 3, 4])]
    ys = [0.0, -1.6, -3.2]
    x0 = 0.35                                                # bars start clear of the step names
    totals = []
    for (n, name, keep), y in zip(rows, ys):
        for j in keep:
            _mass_rect(ax, x0 + starts[j] * sc, y, seg_kinds[j][1] * sc, h, seg_kinds[j][0])
        m = sum(seg_kinds[j][1] for j in keep)
        totals.append(m)
        step_marker(ax, (-3.6, y + 0.5 * h), n)
        text(ax, (-3.2, y + 0.5 * h), name, ha="left", va="center", backing=False, fs=FS_SMALL)
        text(ax, (x0 + m * sc + 0.2, y + 0.5 * h), f"{fmt(m)} kg", ha="left", va="center", backing=False, fs=FS_SMALL)
    # the steps between the rows: size the next stage down ("leads to" arrows, with step 4 of the method)
    r = 9.0 * data_per_pt(ax)[1]                            # the radius of a step marker, in data units
    factors = []
    for k, (stage, dv) in enumerate(((2, DV2), (1, DV1))):
        y_a, y_b = ys[k] + 0.5 * h - r - 0.04, ys[k + 1] + 0.5 * h + r + 0.04
        arrow(ax, (-3.6, y_a), (-3.6, y_b), lw=LW_THIN, head="small")
        ym = 0.5 * (ys[k] + ys[k + 1] + h)
        fac = num(fmt(totals[k + 1])) / num(fmt(totals[k]))
        factors.append(fac)
        step_marker(ax, (-3.0, ym), 4)
        text(ax, (-2.6, ym), f"size stage {stage} for $\\Delta V_{stage}$ = {fmt(dv)} m/s: × {fmt(fac, 4)}",
             ha="left", va="center", backing=False, fs=FS_SMALL)
    # the parts of the last bar
    yb = ys[2] - 0.1
    for (a, b, lab) in ((0, 1, "payload"), (1, 3, "stage 2"), (3, 5, "stage 1")):
        brace(ax, (x0 + starts[b] * sc, yb), (x0 + starts[a] * sc, yb), lab, side=1, fs=FS_SMALL)
    mass_key(ax, (-3.75, -4.6))
    # asserts: one scale; each row is the row above times the factor of the stage added
    close_to(totals[0], m_pay, 1e-12, "row 1 is the payload")
    close_to(totals[1], s2["m_i"], 1e-9, "row 2 is stage 2's initial mass, the payload of stage 1", rel=True)
    close_to(totals[2], s1["m_i"], 1e-9, "row 3 is the gross liftoff mass", rel=True)
    c = c_from_isp(EX1["isp"])
    for dv, fac in zip((DV2, DV1), factors):
        close_to(fac, stage_factor(dv, c, EX1["f"]), 2e-3, "the printed factor is the stage factor", rel=True)
    trim_canvas(fig)
    save_figure(fig, "p43-top-down")


def one_against_two():
    """Lesson: for the same payload and the same delta-V, two stages need 17% less initial mass than one."""
    full, one, ch = ex1()
    s1, s2 = full[0], full[1]
    m_pay = EX1["m_pay"]
    L = 8.4
    sc = L / one["m_i"]
    fig, ax = canvas(6.5, xlim=(-2.4, 11.0), ylim=(-3.2, 2.0))
    h = 0.7
    y1, y2 = 0.55, -0.95
    b1 = mass_bar(ax, (0.0, y1), [("payload", m_pay), ("inert", one["m_inert"]), ("propellant", one["m_prop"])],
                  sc, h, total=one["m_i"], labels=False)
    b2 = mass_bar(ax, (0.0, y2), [("payload", m_pay), ("inert", s2["m_inert"]), ("propellant", s2["m_prop"]),
                                  ("inert", s1["m_inert"]), ("propellant", s1["m_prop"])],
                  sc, h, total=s1["m_i"], labels=False)

    def inside(bar, i, s):
        a, b = bar["spans"][i]
        x0, y0 = bar["origin"]
        st = MASS_STYLE[bar["segments"][i]["kind"]]
        ax.text(x0 + 0.5 * (a + b), y0 + 0.5 * h, s, ha="center", va="center", fontsize=FS_SMALL, color=INK, zorder=8,
                bbox=dict(boxstyle="square,pad=0.12", fc=st["fill"], ec="none"))
    inside(b1, 0, "payload")
    inside(b1, 2, "propellant")
    inside(b2, 0, "payload")
    inside(b2, 4, "stage 1 propellant")
    text(ax, (0.0, y1 + 0.5 * h), f"one stage\n{fmt(one['m_i'])} kg", direction=180.0, dist=6.0, fs=FS_SMALL,
         backing=False)
    text(ax, (0.0, y2 + 0.5 * h), f"two stages\n{fmt(s1['m_i'])} kg", direction=180.0, dist=6.0, fs=FS_SMALL,
         backing=False)
    # stage 2 and stage 1 named with braces below their segments
    a, b = b2["spans"][1][0], b2["spans"][2][1]
    brace(ax, (b, y2 - 0.1), (a, y2 - 0.1), "stage 2", side=1, fs=FS_SMALL)
    a1, b1_ = b2["spans"][3][0], b2["spans"][4][1]
    brace(ax, (b1_, y2 - 0.1), (a1, y2 - 0.1), "stage 1", side=1, fs=FS_SMALL)
    # the difference, from the end of the two-stage bar to the end of the single-stage bar
    x_a, x_b = b2["end"][0], b1["end"][0]
    ax.plot([x_b, x_b], [y1, y2 - 0.05], color=GRAY, lw=LW_THIN, ls=(0, (2.0, 2.0)), zorder=2)
    dimension(ax, (x_a, y2 + 0.5 * h), (x_b, y2 + 0.5 * h), None)
    d = num(fmt(one["m_i"])) - num(fmt(s1["m_i"]))
    text(ax, (x_b, y2 + 0.5 * h), f"{fmt(d)} kg less\n({fmt(100.0 * d / num(fmt(one['m_i'])), 2)}%)", direction=0.0,
         dist=6.0, fs=FS_SMALL, backing=False)
    mass_key(ax, (0.0, -2.4))
    close_to(b1["end"][0], one["m_i"] * sc, 1e-9, "bar length is the initial mass")
    close_to(b2["end"][0], s1["m_i"] * sc, 1e-9, "bar length is the initial mass")
    assert b2["end"][0] < b1["end"][0], "two stages are lighter"
    trim_canvas(fig)
    save_figure(fig, "p43-one-against-two")


def number_of_stages():
    """Lesson: each added stage moves the limit to the right, and each helps less than the one before."""
    c = c_from_isp(EX2["isp"])
    f = EX2["f"]
    fig, ax = data_axes(6.5, 4.0)
    xmax = 18.0
    for n, st in ((1, 0), (2, 1), (3, 2)):
        lim = identical_limit(n, c=c, f=f)
        dv = np.linspace(0.0, min(lim * 0.99995, xmax * 1000.0), 1200)
        r = np.array([identical_stages(1.0, v, n, c=c, f=f) for v in dv])
        ax.plot(dv / 1000.0, r, **line_kw(st))
        if lim < xmax * 1000.0:
            ax.axvline(lim / 1000.0, **line_kw("boundary"))
    log_axis(ax, "y", 1.0, 1000.0, "comma", "Initial mass per kilogram\nof payload, $m_i/m_\\text{pay}$")
    ax.set_xlim(0, xmax)
    ax.set_xlabel("Delta-V, $\\Delta V$, km/s")
    lim1, lim2 = identical_limit(1, c=c, f=f) / 1000.0, identical_limit(2, c=c, f=f) / 1000.0
    text(ax, (lim1, 1.9), f"limit of\none stage:\n{fmt(lim1)} km/s", direction=180.0, dist=5.0, fs=FS_SMALL,
         backing=False)
    text(ax, (lim2, 6.0), f"limit of\ntwo stages:\n{fmt(lim2)} km/s", direction=180.0, dist=5.0, fs=FS_SMALL,
         backing=False)
    text(ax, (5.2, 22.0), "1 stage", color=text_color(0), backing=False)
    text(ax, (11.2, 330.0), "2 stages", color=text_color(1), backing=False)
    text(ax, (13.6, 45.0), "3 stages", color=text_color(2), backing=False)
    dv0 = DV_LAUNCH / 1000.0
    y2, y3 = identical_stages(1.0, DV_LAUNCH, 2, c=c, f=f), identical_stages(1.0, DV_LAUNCH, 3, c=c, f=f)
    ax.axvline(dv0, color=GRAY, lw=LW_THIN, ls=(0, (1.0, 2.0)), zorder=1.5)
    text(ax, (dv0, 1.9), f"launch of page 2.3:\n{fmt(dv0)} km/s", direction=0.0, dist=5.0, fs=FS_SMALL,
         backing=False)
    # the two readings of worked example 2, small markers (open circle, filled square) labeled directly
    point(ax, (dv0, y2), None, ms=4.5, color=text_color(1), kind="open", zorder=9)
    point(ax, (dv0, y3), None, ms=4.0, color=text_color(2), kind="square", zorder=8.5)
    callout(ax, (dv0, y2), fmt(y2), at=(9.9, 110.0), gap=3.0, fs=FS_SMALL, ha="center", backing=False)
    callout(ax, (dv0, y3), fmt(y3), at=(10.2, 12.0), gap=3.0, fs=FS_SMALL, ha="center", backing=False)
    # asserts: each limit is n c ln(1/f); the curves are ordered; the gain shrinks
    close_to(lim2, 2.0 * lim1, 1e-12, "the limit of two identical stages is twice that of one")
    assert lim1 < dv0 < lim2 and y2 > y3, "one stage cannot do the launch; three are lighter than two"
    for v in (2000.0, 6000.0, 8000.0):
        r1, r2, r3 = (identical_stages(1.0, v, n, c=c, f=f) for n in (1, 2, 3))
        assert r1 > r2 > r3 and (r1 - r2) > (r2 - r3), "more stages lighter, by less each time"
    save_figure(fig, "p43-number-of-stages")



def stage_bars():
    """Lesson: for the launch, a third identical stage saves about 3 t of 21; a fourth saves only about 1 t."""
    full, ch = ex2()
    fig, ax = data_axes(6.5, 4.6)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.08, top=0.85)
    ax.grid(False, axis="x")
    w = 0.46
    tops = []
    ns = list(range(2, N_MAX + 1))
    named = []
    for k, n in enumerate(ns):
        st = full[n]
        x0 = k - 0.5 * w
        y = 0.0
        for s in st:                                       # stage 1 at the bottom, as on the pad
            mid = (y + 0.5 * s["m_prop"]) / 1000.0
            _mass_rect(ax, x0, y / 1000.0, w, s["m_prop"] / 1000.0, "propellant")
            if s["m_prop"] / 1000.0 > 1.2:                 # the name fits inside the propellant
                ax.text(k, mid, f"stage {s['stage']}", ha="center", va="center", fontsize=FS_SMALL, color=INK, zorder=8)
            else:                                          # a thin top stage: named to the right of its bar
                callout(ax, (k + 0.5 * w, mid), f"stage {s['stage']}", at=(k + 0.5 * w + 0.12, mid), gap=1.0,
                        fs=FS_SMALL, ha="left", backing=False)
            named.append((n, s["stage"]))
            y += s["m_prop"]
            _mass_rect(ax, x0, y / 1000.0, w, s["m_inert"] / 1000.0, "inert")
            y += s["m_inert"]
        _mass_rect(ax, x0, y / 1000.0, w, EX2["m_pay"] / 1000.0, "payload")
        y += EX2["m_pay"]
        close_to(y, st[0]["m_i"], 1e-9, "the bar adds up to the initial mass", rel=True)
        tops.append(num(fmt(y)))
        text(ax, (k, y / 1000.0), f"{fmt(y)} kg", direction=90.0, dist=4.0, fs=FS_SMALL, backing=False)
    ax.set_xticks(range(len(ns)), [f"{n} stages" for n in ns])
    ax.tick_params(axis="x", labelsize=FS_LABEL)
    ax.set_xlim(-0.55, len(ns) - 0.2)
    ax.set_ylim(0, 22.0)
    ax.set_yticks([0, 5, 10, 15, 20])
    ax.set_ylabel("Initial mass, t")
    # the saving from one bar to the next: a level line from the taller bar and a drop beside the shorter one
    for k in range(len(ns) - 1):
        d = tops[k] - tops[k + 1]
        xl = k + 0.5
        ax.plot([k + 0.5 * w, xl + 0.04], [tops[k] / 1000.0] * 2, color=GRAY, lw=LW_THIN, ls=(0, (2.0, 2.0)), zorder=2)
        ax.plot([xl - 0.04, k + 1 - 0.5 * w], [tops[k + 1] / 1000.0] * 2, color=GRAY, lw=LW_THIN, ls=(0, (2.0, 2.0)),
                zorder=2)
        ax.annotate("", xy=(xl, tops[k + 1] / 1000.0), xytext=(xl, tops[k] / 1000.0),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=LW_THIN, shrinkA=0, shrinkB=0), zorder=6)
        text(ax, (xl, tops[k + 1] / 1000.0), f"{fmt(d, 3)} kg\nless", direction=-90.0, dist=4.0,
             fs=FS_SMALL, backing=False)
    _key_axes(fig, [0.12, 0.905, 0.80, 0.075])
    assert tops[0] - tops[1] > tops[1] - tops[2] > 0, "each added stage saves less"
    assert all((n, k) in named for n in ns for k in range(1, n + 1)), "every stage of every bar is named"
    save_figure(fig, "p43-stage-bars")



def split_curve():
    """Lesson: there is a best split; near it the initial mass changes little, and it grows without
    bound as either stage nears its limit. The right panel enlarges the bottom of the curve, where the
    three splits of the worked example differ by a few hundred kilograms."""
    b, trials = ex3_trials()
    sh = np.linspace(0.0, 1.0, 4001)
    mi = split_sweep(EX3["m_pay"], DV_LAUNCH, EX3["s1"], EX3["s2"], sh) / 1000.0
    hi = single_stage_limit(c_from_isp(EX3["s1"]["isp"]), EX3["s1"]["f"]) / DV_LAUNCH
    fig, (ax, az) = data_axes(6.5, 3.9, ncols=2, gridspec_kw=dict(width_ratios=[1.25, 1.0]))
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.15, top=0.90, wspace=0.42)
    eq, tb, best = trials
    marks = [(best, "dot", "best split"), (tb, "square", "trial split"), (eq, "open", "equal split")]
    # (a) the whole range
    ax.axvspan(hi, 1.0, fc="#EDEDED", ec="none", zorder=0.5)
    ax.plot(sh, mi, **line_kw(0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 40)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0], ["0.00", "0.25", "0.50", "0.75", "1.00"])   # panel (b)'s style
    ax.text(0.5 * (1 + hi), 20.0, "stage 1 past its limit", rotation=90, ha="center", va="center", fontsize=FS_SMALL)
    for t, kind, _ in marks:
        point(ax, (t["share"], t["m_i"] / 1000.0), None, ms=5.0, kind=kind)
    text(ax, (best["share"], best["m_i"] / 1000.0), "best split", direction=-90.0, dist=6.0, fs=FS_SMALL,
         backing=False)
    ax.set_xlabel("Share of stage 1, $\\Delta V_1/\\Delta V$")
    ax.set_ylabel("Initial mass, $m_i$, t")
    ax.set_title("(a) all splits", fontsize=FS_SMALL, loc="left")
    # (b) near the best split, enlarged; its window is outlined in panel (a) and named "(b)"
    lo_, hi_ = 0.30, 0.54
    y_lo, y_hi = 14.85, 16.0
    ax.add_patch(Rectangle((lo_, y_lo), hi_ - lo_, y_hi - y_lo, fc="none", ec=STEEL, lw=LW_THIN, zorder=2.5))
    text(ax, (0.5 * (lo_ + hi_), y_hi), "(b)", direction=90.0, dist=9.0, fs=FS_SMALL, color=STEEL, backing=False)
    sel = (sh >= lo_) & (sh <= hi_)
    az.plot(sh[sel], mi[sel], **line_kw(0))
    az.set_xlim(lo_, hi_)
    az.set_ylim(y_lo, y_hi)
    az.set_xticks([0.30, 0.35, 0.40, 0.45, 0.50])
    az.set_yticks([15.0, 15.25, 15.5, 15.75, 16.0], ["15.00", "15.25", "15.50", "15.75", "16.00"])
    for t, kind, name in marks:
        point(az, (t["share"], t["m_i"] / 1000.0), None, ms=6.0, kind=kind)
    text(az, (best["share"], best["m_i"] / 1000.0), f"best split:\n{fmt(best['m_i'] / 1000.0)} t", direction=-90.0,
         dist=6.0, fs=FS_SMALL, backing=False)
    callout(az, (tb["share"], tb["m_i"] / 1000.0), f"trial split:\n{fmt(tb['m_i'] / 1000.0)} t", at=(0.398, 15.5),
            gap=4.0, fs=FS_SMALL, ha="center", backing=False)
    callout(az, (eq["share"], eq["m_i"] / 1000.0), f"equal split:\n{fmt(eq['m_i'] / 1000.0)} t", at=(0.44, 15.8),
            gap=4.0, fs=FS_SMALL, ha="center", backing=False)
    az.set_xlabel("Share of stage 1, $\\Delta V_1/\\Delta V$")
    az.set_ylabel("Initial mass, $m_i$, t")
    az.set_title("(b) near the best split", fontsize=FS_SMALL, loc="left")
    i = int(np.nanargmin(mi))
    close_to(float(sh[i]), b["share1"], 1e-3, "minimum of the drawn curve at the best split")
    assert best["m_i"] < tb["m_i"] < eq["m_i"], "the best split is lightest"
    assert np.nanmax(mi[sh < 0.05]) > 3 * best["m_i"] / 1000.0 and np.nanmax(mi[(sh > 0.85) & (sh < hi)]) > 100.0, \
        "the curve blows up near both ends"
    assert all(lo_ < t["share"] < hi_ and 15.0 < t["m_i"] / 1000.0 < 16.0 for t, _, _ in marks), \
        "the three splits lie inside the enlarged panel"
    save_figure(fig, "p43-split-curve")



def saturn_v():
    """Lesson: the three Saturn V stages share about 12.5 km/s of ideal delta-V; none gives more than 4.8 km/s,
    and the ideal total is more than the speed the vehicle reached: the gap is what the climb cost."""
    S = saturn()
    dvs = [s["dv"] / 1000.0 for s in S]
    total = sum(dvs)
    fig, ax = data_axes(6.5, 3.9)
    ax.grid(False, axis="x")
    labels = ["first stage\nS-IC", "second stage\nS-II", "third stage\nS-IVB\n(both burns)", "sum of\nthe three"]
    bottoms = [0.0, dvs[0], dvs[0] + dvs[1], 0.0]
    vals = dvs + [total]
    cont = bars(ax, labels, vals, styles=[0, 1, 2, 4], bottoms=bottoms, value_text=[fmt(v) for v in vals], fs=FS_SMALL)
    for x0, x1, yv in ((0, 1, dvs[0]), (1, 2, dvs[0] + dvs[1]), (2, 3, total)):
        ax.plot([x0 + 0.31, x1 - 0.31], [yv, yv], color=GRAY, lw=LW_THIN, ls=(0, (2, 2)), zorder=2)
    v_tli = SATURN_V_AS506_TLI_V / 1000.0
    ax.plot([-0.5, 3.31], [v_tli, v_tli], color=INK, lw=1.2, ls=(0, (6.0, 3.0)), zorder=4)
    text(ax, (-0.45, v_tli), f"speed reached at\ntranslunar injection:\n{fmt(v_tli)} km/s", direction=90.0, dist=3.0,
         ha="left", fs=FS_SMALL, backing=False)
    # the gap between the ideal sum and the speed reached, marked beside the sum bar
    gap = num(fmt(total, 4)) - num(fmt(v_tli))
    xg = 3.0 + 0.31 + 0.12
    dimension(ax, (xg, v_tli), (xg, total), None, extension=False, ticks=False)
    text(ax, (xg, 0.5 * (v_tli + total)), f"{fmt(gap, 3)} km/s:\nlosses, less Earth's\nrotation, plus\nunburned propellant",
         direction=0.0, dist=5.0, fs=FS_SMALL, backing=False)
    ax.set_ylabel("Ideal delta-V, km/s")
    ax.set_ylim(0, 14.5)
    # the axis stops just past the sum bar; the gap's label sits in the right margin, not in an empty slot
    ax.set_xlim(-0.5, 3.5)
    fig.subplots_adjust(left=0.10, right=0.70)
    tops = [p.get_y() + p.get_height() for p in cont.patches]
    close_to(tops[3], tops[2], 1e-9, "the total bar ends where the third stage ends")
    assert max(dvs) < 0.5 * total and total > v_tli, "no stage gives half; the ideal total exceeds the speed reached"
    close_to(gap, (total - v_tli), 6e-3, "the marked gap is the sum less the speed reached")
    save_figure(fig, "p43-saturn-v")



def make_all():
    payload_of_a_stage()
    staging_sequence()
    top_down()
    one_against_two()
    number_of_stages()
    stage_bars()
    split_curve()
    saturn_v()



# ================================================================= printed values
def values():
    R = lambda key, s: record(PAGE, key, s)                 # noqa: E731
    # the inputs as the page prints them
    R("dv1", fmt(DV1))
    R("dv2", fmt(DV2))
    R("dv-launch", fmt(DV_LAUNCH))
    R("dv1-km", fmt(HOHMANN_22["dv1"]))
    R("dv2-km", fmt(HOHMANN_22["dv2"]))
    R("dv-hoh-km", fmt(HOHMANN_22["dv_total"]))
    R("dv-launch-km", fmt(LAUNCH_23["total"]))
    # worked example 1
    full, one, ch = ex1()
    R("ex1-c", ch["c"])
    for k in (2, 1):
        for key, s in ch[k].items():
            R(f"ex1-s{k}-{key}", s)
    R("ex1-one-mi", fmt(one["m_i"]))
    R("ex1-one-mprop", fmt(one["m_prop"]))
    R("ex1-one-minert", fmt(one["m_inert"]))
    assert ch[1]["m_i"] == fmt(full[0]["m_i"]) and ch[2]["m_i"] == fmt(full[1]["m_i"]), (ch, full)
    d = num(ch["1"]["m_i"] if "1" in ch else ch[1]["m_i"])
    one_s = num(fmt(one["m_i"]))
    R("ex1-saving", fmt(one_s - d))
    R("ex1-saving-pct", fmt(100.0 * (one_s - d) / one_s, 2))
    R("ex1-saving-pct-fig", fmt(100.0 * (one["m_i"] - full[0]["m_i"]) / one["m_i"], 2))
    R("ex1-prop-total", fmt(num(ch[1]["m_prop"]) + num(ch[2]["m_prop"])))
    R("ex1-inert-total", fmt(num(ch[1]["m_inert"]) + num(ch[2]["m_inert"])))
    for k in (2, 1):                                        # each stage's factor, from the printed masses
        R(f"ex1-factor{k}", fmt(num(ch[k]["m_i"]) / num(ch[k]["m_pay"]), 4))
    # what the second burn pushes: the single stage's inert mass rides to the end
    # worked example 2
    full2, ch2 = ex2()
    R("ex2-c", ch2["c"])
    for key, s in ch2[1].items():
        R(f"ex2-n1-{key}", s)
    for n in (2, 3):
        for key, s in ch2[n].items():
            if key != "x":                                # the exponent is printed as a ratio, not as x
                R(f"ex2-n{n}-{key}", s)
    m2, m3 = num(ch2[2]["m_i"]), num(ch2[3]["m_i"])
    m4 = full2[4][0]["m_i"]
    R("ex2-n4-mi", fmt(m4))
    R("ex2-save23", fmt(m2 - m3))
    R("ex2-save34", fmt(m3 - num(fmt(m4)), 3))
    e2 = num(ch2[2]["e"])
    R("ex2-n2-fe", fmt(EX2["f"] * e2, 4))
    R("ex2-save23-pct", fmt(100.0 * (m2 - m3) / m2, 2))
    R("ex2-n2-per-kg", fmt(full2[2][0]["m_i"] / EX2["m_pay"]))
    R("ex2-n3-per-kg", fmt(full2[3][0]["m_i"] / EX2["m_pay"]))
    R("ex2-lim2", fmt(identical_limit(2, isp=EX2["isp"], f=EX2["f"]) / 1000.0))
    R("ex2-lim1-km", fmt(identical_limit(1, isp=EX2["isp"], f=EX2["f"]) / 1000.0))
    # worked example 3
    b, trials = ex3_trials()
    c1, c2 = c_from_isp(EX3["s1"]["isp"]), c_from_isp(EX3["s2"]["isp"])
    R("ex3-c1", fmt(c1, 5))
    R("ex3-c2", fmt(c2, 5))
    R("ex3-lim1", fmt(single_stage_limit(c1, EX3["s1"]["f"])))
    R("ex3-lim2", fmt(single_stage_limit(c2, EX3["s2"]["f"])))
    R("ex3-lim2-share", fmt(1.0 - single_stage_limit(c2, EX3["s2"]["f"]) / DV_LAUNCH, 1))
    R("ex3-lim1-share", fmt(single_stage_limit(c1, EX3["s1"]["f"]) / DV_LAUNCH, 3))
    for t in trials:
        p = t["name"]
        R(f"ex3-{p}-dv1", fmt_dec(t["dv1"], 1) if p == "equal" else fmt(t["dv1"]))
        R(f"ex3-{p}-dv2", fmt_dec(t["dv2"], 1) if p == "equal" else fmt(t["dv2"]))
        R(f"ex3-{p}-share", fmt(t["share"], 3))
        for s in t["stages"]:
            k = s["stage"]
            R(f"ex3-{p}-s{k}-e", fmt(s["exp"], 4))
            R(f"ex3-{p}-s{k}-mprop", fmt(s["m_prop"]))
            R(f"ex3-{p}-s{k}-minert", fmt(s["m_inert"]))
            R(f"ex3-{p}-s{k}-mi", fmt(s["m_i"]))
        R(f"ex3-{p}-mi", fmt(t["m_i"]))
        R(f"ex3-{p}-mi-t", fmt(t["m_i"] / 1000.0))
        R(f"ex3-{p}-cond1", fmt(t["cond"][0]))
        R(f"ex3-{p}-cond2", fmt(t["cond"][1]))
    eq, tb, best = trials
    R("ex3-eq-over-pct", fmt(100.0 * (eq["m_i"] - best["m_i"]) / best["m_i"], 2))
    R("ex3-b-over-pct", fmt(100.0 * (tb["m_i"] - best["m_i"]) / best["m_i"], 2))
    R("ex3-best-share2-pct", fmt(100.0 * (1.0 - best["share"]), 2))
    # the curve is flat: a share 0.05 away from the best costs little
    for dsh in (0.05, 0.1):
        m_lo = split_mass(EX3["m_pay"], DV_LAUNCH, best["share"] - dsh, EX3["s1"], EX3["s2"])
        m_hi = split_mass(EX3["m_pay"], DV_LAUNCH, best["share"] + dsh, EX3["s1"], EX3["s2"])
        R(f"ex3-flat-{dsh:g}", fmt(100.0 * (max(m_lo, m_hi) - best["m_i"]) / best["m_i"], 2))
    # the Saturn V
    S = saturn()
    for s in S:
        k = s["name"]
        R(f"sv-{k}-prop-t", fmt(s["prop"] / 1000.0))
        R(f"sv-{k}-dry-t", fmt(s["dry"] / 1000.0))
        R(f"sv-{k}-isp", fmt(s["isp"]) if s["isp"] >= 1000 else (f"{s['isp']:g}"))
        R(f"sv-{k}-f", fmt(s["f"], 3))
        R(f"sv-{k}-mi-t", fmt(s["m_i"] / 1000.0))
        R(f"sv-{k}-mf-t", fmt(s["m_f"] / 1000.0))
        R(f"sv-{k}-dv-km", fmt(s["dv"] / 1000.0))
        R(f"sv-{k}-vcut-km", fmt(s["v_cutoff"] / 1000.0))
    tot = sum(s["dv"] for s in S)
    R("sv-total-km", fmt(tot / 1000.0, 3))
    R("sv-total-km4", fmt(tot / 1000.0))
    R("sv-tli-km", fmt(SATURN_V_AS506_TLI_V / 1000.0))
    R("sv-diff-km", fmt((tot - SATURN_V_AS506_TLI_V) / 1000.0, 3))
    s2 = S[1]
    R("sv-sii-limit-km", fmt(single_stage_limit(s2["c"], s2["f"]) / 1000.0))
    # the S-IC value is the highest of the five engines' values reduced to sea level (the flight report's range)
    lo, hi = (float(v) for v in re.findall(r"\d+\.\d", SATURN_V_AS506["S-IC"]["isp_kind"]))
    assert lo < hi == SATURN_V_AS506["S-IC"]["isp"], "the S-IC value is the top of the engines' range"
    R("sv-sic-isp-lo", f"{lo:.1f}")
    R("sv-sic-isp-hi", f"{hi:.1f}")
    R("sv-liftoff-t", fmt(S[0]["m_i"] / 1000.0))
    rp1 = SP125_PROPERTIES["RP-1"][2][0]                     # g/cc, the low end of 0.80 to 0.82
    R("rp1-lh2-ratio", fmt(rp1 / SP125_PROPERTIES["liquid hydrogen"][2], 2))
