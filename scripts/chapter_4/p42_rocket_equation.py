from chapter_4.common import *  # noqa: F401,F403
"""Figures and values of 4.2 Rocket Equation (notes/chapter-4/rocket-equation.md).

One function per figure, make_all() for the runner, and values() for every number the page
prints. Run through the runner from the book folder:

    FIG_PREVIEW=<folder> python3 -B scripts/make_chapter_4_figures.py p42

Helpers that the shared code lacks are defined here (prefixed with an underscore).

Worked examples (inputs; everything else is computed):
  1. The lectures' Jupiter orbit insertion: a 4,000 kg spacecraft slows by 2.1 km/s with an engine of
     360 s (vacuum). Final mass and propellant.
  2. One stage does both burns of the Hohmann transfer of page 2.2 (3.416 km/s, converted as
     printed to 3,416 m/s): payload 1,750 kg, 323 s, inert mass fraction 0.17.
  3. The Ariane 5 core stage of page 1.3 (14,700 kg dry, 170,000 kg of propellant; Vulcain 2,
     432 s in vacuum and 960 kN at sea level, Ariane 5 User's Manual, p. 1-7) against the launch
     budget of page 2.3 (8.833 km/s, losses included).
Every printed step is computed from the digits printed before it (check_chains.py), so the
chains use the printed, rounded operands; full precision is only kept where nothing is printed.
"""

PAGE = "p42"

# ------------------------------------------------------------------ worked example inputs
EX1 = dict(m_i=4000.0, dv_kms=2.1, isp=360.0)                 # the lectures' example
EX2 = TRANSFER_STAGE                                          # links.py: shared with page 4.3
A5 = dict(dry=ARIANE5_CORE["dry_kg"], prop=ARIANE5_CORE["prop_kg"], isp=VULCAIN2["isp_vac"],
          F_sl=1e3 * VULCAIN2["F_sl_kN"])                     # page 1.3 masses; A5UM p. 1-7 engine

# Inert mass fractions of real stages drawn and tabulated (AVUM left out: its dry mass carries the
# avionics of the whole launcher, so its fraction says nothing about tanks and engines)
STAGE_ROWS = [s for s in STAGES if s[0] != "AVUM"]

# Curves of the payload-fraction figure: the Ariane 5 core stage, worked example 2, the Ariane 5
# upper stage (ESC-A), each computed from its masses or given
def _f_of(name):
    for n, veh, kind, dry, prop, src in STAGES:
        if n == name:
            return inert_mass_fraction(dry, prop)
    raise KeyError(name)


def P(x, sig=4):
    """Printed value of x back as a float: chains use the printed digits."""
    return printed(x, sig)[1]


# ------------------------------------------------------------------ the examples, computed as printed
def ex1():
    dv = 1000.0 * EX1["dv_kms"]
    c = EX1["isp"] * G0                                   # 3,531.6 exactly
    x = P(dv / P(c), 5)
    ex = P(math.exp(x), 5)
    m_f = EX1["m_i"] / ex
    m_prop = EX1["m_i"] - P(m_f)
    return dict(dv=dv, c=c, x=x, ex=ex, m_f=m_f, m_prop=m_prop, share=m_prop / EX1["m_i"])


def ex2():
    dv = km_as_printed(HOHMANN_22["dv_total"])            # 3,416 m/s
    c = EX2["isp"] * G0                                   # 3,168.63 exactly
    f = EX2["f"]
    x = P(dv / c, 6)                                      # six figures: the denominator 1 - f e^x magnifies rounding
    ex = P(math.exp(x), 6)
    num = P(EX2["m_pay"] * (ex - 1.0) * (1.0 - f), 6)
    den = P(1.0 - f * ex, 6)
    m_prop = P(num / den, 5)
    m_inert = P(f / (1.0 - f) * m_prop, 5)
    m_f = EX2["m_pay"] + m_inert
    m_i = m_f + m_prop
    full = size_stage(EX2["m_pay"], dv, c=c, f_inert=f)
    close_to(m_i, full["m_i"], 0.1, "example 2: the printed chain stays with the full-precision sizing")
    check = c * math.log(P(m_i, 5) / P(m_f, 5))
    return dict(dv=dv, c=c, f=f, x=x, ex=ex, num=num, den=den, m_prop=m_prop, m_inert=m_inert, m_f=m_f, m_i=m_i,
                ratio=P(m_i, 5) / P(m_f, 5), check=check, full=full)


def ex3():
    c = A5["isp"] * G0                                    # 4,237.92 exactly
    m0 = A5["dry"] + A5["prop"]                           # 184,700
    f = inert_mass_fraction(A5["dry"], A5["prop"])
    ratio0 = m0 / A5["dry"]
    dv0 = c * math.log(P(ratio0, 5))
    dv_req = km_as_printed(LAUNCH_23["total"])            # 8,833 m/s
    x = P(dv_req / c, 6)
    ex = P(math.exp(x), 5)
    inv_f = 1.0 / P(f)
    fe = P(f) * ex
    num = P(A5["prop"] * (1.0 - P(fe, 5)), 5)
    den = P((ex - 1.0) * (1.0 - P(f)), 5)
    m_pay = num / den
    mi = m0 + P(m_pay)
    mf = A5["dry"] + P(m_pay)
    W = m0 * G0
    return dict(c=c, m0=m0, f=f, ratio0=ratio0, dv0=dv0, dv_req=dv_req, x=x, ex=ex, inv_f=inv_f, fe=fe, num=num,
                den=den, m_pay=m_pay, mi=mi, mf=mf, back=c * math.log(mi / mf), W=W, FW=A5["F_sl"] / W)


# ------------------------------------------------------------------ drawing helpers of this page
def _vehicle(origin, angle_deg, length):
    """Chapter 1's Falcon 9 outline (proportions after the Falcon User's Guide), no payload, scaled to
    `length` data units, its tail (the base of the first stage) at `origin` and its nose pointing at
    `angle_deg` (screen degrees, counterclockwise from the right). Returns the parts and the unit vector
    along the axis, the nose point and the tail point."""
    from chapter_1.geometry import Part
    parts = two_stage_vehicle(payload=False)
    k = length / FALCON9["height"]
    a = math.radians(angle_deg - 90.0)
    Rm = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    o = np.asarray(origin, float)
    out = {}
    for n_, p in parts.items():
        out[n_] = Part(p.name, (p.xy * k) @ Rm.T + o, p.kind, p.z, p.hidden, (p.inside * k) @ Rm.T + o,
                       on=getattr(p, "on", None))
    u = np.array([math.cos(math.radians(angle_deg)), math.sin(math.radians(angle_deg))])
    z_all = np.vstack([p.xy for p in parts.values()])
    nose = o + u * k * z_all[:, 1].max()
    tail = o + u * k * z_all[:, 1].min()
    return out, u, nose, tail


# ------------------------------------------------------------------ 1. momentum before and after
def fig_momentum_exchange():
    """Lesson: the rocket gains the forward momentum that the small exhaust mass carries backward."""
    fig, ax = new_axes(6.5, 3.9)
    ax.set_xlim(-0.2, 10.4)
    ax.set_ylim(-0.6, 5.3)
    L = 4.6                                   # drawn length of the vehicle
    V, dV, Ve = 1.2, 0.45, 2.6                # drawn speeds (data units); dV exaggerated
    y1, y2 = 3.95, 1.0
    x_tail = 3.85
    xc = x_tail + 0.5 * L
    rows = []
    for y in (y1, y2):
        parts, u, nose, tail = _vehicle((x_tail, y), 0.0, L)
        draw_parts(ax, parts, details=False)
        rows.append((nose, tail))
    # row 1: at time t
    text(ax, (-0.1, y1 + 0.95), "at time $t$", ha="left", va="center", fontweight="bold")
    n1, t1 = rows[0]
    kind_arrow(ax, (n1[0] + 0.15, y1), (n1[0] + 0.15 + V, y1), "velocity", "$V$", label_dir=0.0)
    text(ax, (xc, y1), "mass $m$", direction=-90.0, dist=10.0)
    text(ax, (-0.1, y1 - 1.2), "momentum at $t$:  $mV$", ha="left", va="center")
    # row 2: at time t + dt
    text(ax, (-0.1, y2 + 0.95), "at time $t + dt$", ha="left", va="center", fontweight="bold")
    n2, t2 = rows[1]
    kind_arrow(ax, (n2[0] + 0.15, y2), (n2[0] + 0.15 + V + dV, y2), "velocity", "$V + dV$", label_dir=0.0)
    text(ax, (xc, y2), "mass $m - dm_\\text{prop}$", direction=-90.0, dist=10.0)
    text(ax, (-0.1, y2 - 1.2), "momentum at $t + dt$:  $(m - dm_\\text{prop})(V + dV) + dm_\\text{prop}(V - V_e)$",
         ha="left", va="center")
    # the small exhaust mass behind the nozzle, moving backward at V - Ve (Ve > V here)
    xp = 2.35
    ax.add_patch(Circle((xp, y2), 0.12, fc=MASS_STYLE["propellant"]["fill"], ec=INK, lw=LW_DETAIL, zorder=6))
    kind_arrow(ax, (xp - 0.2, y2), (xp - 0.2 - (Ve - V), y2), "velocity")
    text(ax, (xp - 0.45, y2), "$V - V_e$", direction=90.0, dist=7.0, color=TEXT_KIND["velocity"])
    text(ax, (xp, y2), "mass $dm_\\text{prop}$", direction=-90.0, dist=10.0)
    # sign convention: velocities measured from the ground, positive forward
    kind_arrow(ax, (8.6, 5.05), (9.6, 5.05), "axis")
    text(ax, (8.6, 5.05), "velocities seen from the ground, positive", direction=180.0, dist=4.0, fs=FS_SMALL)
    text(ax, (9.6, 4.62), "a velocity to the left is negative", ha="right", va="center", fs=FS_SMALL)
    close_to(n2[0] - t2[0], n1[0] - t1[0], 1e-12, "the same vehicle in both rows")
    assert xp < t2[0] and (V - Ve) < 0 < V < V + dV, "the exhaust is behind the rocket and moves backward: V < V_e"
    save_figure(fig, "p42-momentum-exchange")


# ------------------------------------------------------------------ 2. the mass ratio grows exponentially
MR_MARKS = (1.0, 2.0, 3.0)                    # delta-V of c, 2c and 3c


def fig_mass_ratio():
    """Lesson: each extra c of delta-V multiplies the mass ratio by e, while the propellant share only
    creeps toward 100 percent."""
    fig, (a1, a2) = data_axes(6.5, 5.0, nrows=2, sharex=True, gridspec_kw=dict(hspace=0.22))
    x = np.linspace(0.0, 3.2, 400)
    a1.plot(x, np.exp(x), **line_kw(0))
    a2.plot(x, 100.0 * (1.0 - np.exp(-x)), **line_kw(0))
    a1.set_xlim(0.0, 3.2)
    a1.set_ylim(0.0, 25.0)
    a2.set_ylim(0.0, 100.0)
    a1.set_ylabel("Mass ratio, $m_i/m_f$")
    a2.set_ylabel("Propellant share\nof $m_i$, percent")
    a2.set_xlabel("Delta-V over effective exhaust velocity, $\\Delta V/c$")
    a1.yaxis.set_major_locator(mticker.FixedLocator([0, 5, 10, 15, 20, 25]))
    a2.yaxis.set_major_locator(mticker.FixedLocator([0, 20, 40, 60, 80, 100]))
    a2.xaxis.set_major_locator(mticker.FixedLocator([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]))
    for k in MR_MARKS:
        r = math.exp(k)
        sh = 100.0 * (1.0 - math.exp(-k))
        point(a1, (k, r), None, ms=7)
        point(a2, (k, sh), None, ms=7)
        text(a1, (k, r), f"{fmt(r)}", direction=135.0, dist=8.0, fs=FS_SMALL)
        text(a2, (k, sh), f"{fmt(sh, 2)}%", direction=-60.0, dist=9.0, fs=FS_SMALL)
    text(a1, (0.12, 21.0), "each added $c$ of delta-V multiplies\nthe mass ratio by $e$ = 2.718", ha="left", va="center",
         fs=FS_SMALL)
    text(a2, (2.05, 40.0), "the share creeps\ntoward 100 percent", ha="left", va="center", fs=FS_SMALL)
    xs = a1.get_lines()[0].get_xdata()
    ys = a1.get_lines()[0].get_ydata()
    for k in MR_MARKS[:-1]:
        close_to(float(np.interp(k + 1.0, xs, ys)) / float(np.interp(k, xs, ys)), math.e, 2e-3,
                 "one more c multiplies the drawn mass ratio by e")
    save_figure(fig, "p42-mass-ratio")


# ------------------------------------------------------------------ 3. the three masses and the inert mass fraction
def fig_three_masses():
    """Lesson: the inert mass fraction is measured against the stage (inert plus propellant), not
    against the whole vehicle."""
    e = ex2()
    fig, ax = new_axes(6.5, 3.5)
    ax.set_xlim(-0.6, 10.2)
    ax.set_ylim(-1.9, 3.9)
    sc = 9.6 / e["m_i"]
    h = 1.15
    b = mass_bar(ax, (0.0, 0.0), [("payload", EX2["m_pay"], "payload", "$m_\\text{pay}$"),
                                  ("inert", e["m_inert"], "", ""),
                                  ("propellant", e["m_prop"], "propellant", "$m_\\text{prop}$")], sc, h,
                 two_lines=True)
    (i0, i1) = b["spans"][1]
    # leader into the hatched segment, ending on a small dot as in fig_example_stage (mass_bar's callouts)
    c_in = (0.5 * (i0 + i1), 0.5 * h)
    an = callout(ax, c_in, "inert mass, $m_\\text{inert}$", at=(0.5 * (i0 + i1), h + 0.62), ha="center", gap=1.5)
    an.arrow_patch.set_gid("leader")
    ax.plot(*c_in, "o", ms=2.6, color=INK, zorder=12, gid="grp:lead-inert")
    mass_braces(ax, b, [(0, 1, "final mass, $m_f$"), (0, 2, "initial mass, $m_i$")], side=-1, step=30.0)
    # the stage: inert plus propellant, above the bar, with the definition
    a1_ = b["spans"][2][1]
    yb = h + 1.25
    brace(ax, (i0, yb), (a1_, yb), None, side=1)
    text(ax, (0.5 * (i0 + a1_), yb), "the stage: $m_\\text{inert} + m_\\text{prop}$\n"
         "$f_\\text{inert} = m_\\text{inert}/(m_\\text{inert} + m_\\text{prop})$", direction=90.0, dist=9.0,
         linespacing=1.4)
    close_to(b["end"][0], e["m_i"] * sc, 1e-9, "bar length is the initial mass")
    close_to((i1 - i0) / (a1_ - i0), EX2["f"], 1e-4, "inert over the stage, as drawn, is f_inert")
    save_figure(fig, "p42-three-masses")


# ------------------------------------------------------------------ 4. inert mass fractions of real stages
def fig_inert_fractions():
    """Lesson: real stages carry about 6 to 23 percent of their own loaded mass as inert mass; the large
    liquid stages are lightest, the small upper stage heaviest."""
    fig, ax = data_axes(6.5, 3.9)
    pts = []
    for name, veh, kind, dry, prop, src in STAGE_ROWS:
        f = inert_mass_fraction(dry, prop)
        solid = kind.startswith("solid")
        pts.append((name, veh, prop / 1000.0, f, solid))
        ax.plot(prop / 1000.0, f, "s" if solid else "o", ms=7.5, mfc="white" if solid else INK, mec=INK, mew=1.4,
                zorder=6)
    log_axis(ax, "x", 4.0, 5000.0, "comma", "Propellant mass of the stage, t (logarithmic scale)")
    ax.set_ylim(0.0, 0.25)
    ax.yaxis.set_major_locator(mticker.MultipleLocator(0.05))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.2f}"))
    ax.set_ylabel("Inert mass fraction, $f_\\text{inert}$")
    # the trend of the liquid stages: a thin dashed gray guide through them in order of size (a guide, not a
    # model to interpolate on), named beside its steep part
    liq = sorted((p for p in pts if not p[4]), key=lambda p: p[2])
    ax.plot([p[2] for p in liq], [p[3] for p in liq], color=STEEL, lw=LW_THIN, ls=(0, (4.0, 2.5)), zorder=3)
    text(ax, (40.0, 0.19), "liquid stages:\nthe larger, the lighter", ha="left", va="center", fs=FS_SMALL,
         color=STEEL, linespacing=1.2)
    # short names (the caption pairs each with its vehicle), each beside its own marker
    NAMES = {"S-IC": ("S-IC", 0.0), "S-II": ("S-II", 90.0), "S-IVB": ("S-IVB", 45.0),
             "EPC": ("Ariane 5 core", -90.0), "ESC-A": ("Ariane 5 upper", 20.0),
             "EAP": ("Ariane 5 booster", -90.0), "Shuttle SRB": ("Shuttle booster", 0.0),
             "P80": ("P80", 180.0), "Zefiro 23": ("Zefiro 23", 180.0), "Zefiro 9": ("Zefiro 9", 90.0)}
    for name, veh, x, f, solid in pts:
        nm, d = NAMES[name]
        text(ax, (x, f), nm, direction=d, dist=9.0 if d % 90.0 else 7.0, fs=FS_SMALL)
    legend_pts = [("o", INK, "liquid stage"), ("s", "white", "solid motor")]
    for k, (m, fc, nm) in enumerate(legend_pts):
        ax.plot(1500.0, 0.235 - 0.018 * k, m, ms=7.5, mfc=fc, mec=INK, mew=1.4)
        text(ax, (1500.0, 0.235 - 0.018 * k), nm, direction=0.0, dist=7.0, fs=FS_SMALL)
    fs_ = [p[3] for p in pts]
    assert 0.05 < min(fs_) and max(fs_) < 0.25, fs_
    assert max(pts, key=lambda p: p[2])[3] == min(fs_), "the largest stage has the smallest fraction"
    drawn = ax.get_lines()[len(pts)]
    assert all(np.diff(drawn.get_ydata()) < 0) and all(np.diff(drawn.get_xdata()) > 0), \
        "the drawn liquid-stage line falls with every step in size"
    save_figure(fig, "p42-inert-fractions")


# ------------------------------------------------------------------ 5. payload fraction against delta-V
PF_CURVES = (("EPC", "Ariane 5 core stage"), (None, "worked example 2"), ("ESC-A", "Ariane 5 upper stage"))


def fig_payload_fraction():
    """Lesson: one stage has a hard limit: the payload fraction falls to zero at dV/c = ln(1/f_inert)."""
    fig, ax = data_axes(6.5, 3.9)
    e2 = ex2()
    ax.set_xlim(0.0, 2.8)
    ax.set_ylim(0.0, 1.0)
    key_y = 0.93
    KX = 1.10                                        # key inside the axes, clear of the curves (all below 0.28 here)
    # worked example 2 first, at the top of the key, so its open-circle glyph sits far from the real point
    pf2 = EX2["m_pay"] / e2["m_i"]
    x2 = e2["dv"] / e2["c"]
    point(ax, (x2, pf2), None, ms=7.5, kind="open", color=SERIES_STYLE[1]["color"])
    ax.plot(KX + 0.075, key_y, "o", ms=7.5, mfc="white", mec=SERIES_STYLE[1]["color"], mew=1.4)
    text(ax, (KX + 0.15, key_y), f"worked example 2: $\\Delta V/c$ = {fmt(x2)},\npayload {fmt(100.0 * pf2, 3)}% of $m_i$",
         direction=0.0, dist=5.0, color=text_color(1), va="center", linespacing=1.25)
    assert key_y - pf2 > 0.6, "the key's glyph sits far above the real point"
    key_y -= 0.18
    for k, (name, label) in enumerate(PF_CURVES):
        f = _f_of(name) if name else EX2["f"]
        lim = math.log(1.0 / f)
        x = np.linspace(0.0, lim, 400)
        ex_ = np.exp(x)
        pf = (1.0 - f * ex_) / (ex_ * (1.0 - f))          # m_pay / m_i, the inverse of the stage factor
        ax.plot(x, pf, **line_kw(k))
        # the end of each curve on the axis: a whole dot, drawn over the spine
        ax.plot(lim, 0.0, "o", ms=6.5, color=SERIES_STYLE[k]["color"], mec=SERIES_STYLE[k]["color"], mew=0.8,
                clip_on=False, zorder=9)
        close_to(float(pf[-1]), 0.0, 1e-9, "the curve reaches zero payload at ln(1/f)")
        close_to(float(pf[0]), 1.0, 1e-12, "no delta-V: all payload")
        # key entry: line sample, then the stage, its fraction and where its payload reaches zero
        ax.plot([KX, KX + 0.15], [key_y, key_y], **line_kw(k))
        fs_txt = fmt(f, 3) if name else fmt(f, 2)
        text(ax, (KX + 0.15, key_y), f"{label}, $f_\\text{{inert}}$ = {fs_txt}\nno payload left at $\\Delta V/c$ = {fmt(lim)}",
             direction=0.0, dist=5.0, color=text_color(k), va="center", linespacing=1.25)
        key_y -= 0.18
    ends = [ln for ln in ax.get_lines() if not ln.get_clip_on()]
    assert len(ends) == 3 and all(float(ln.get_ydata()[0]) == 0.0 for ln in ends), "three whole end dots on the axis"
    ax.set_xlabel("Delta-V over effective exhaust velocity, $\\Delta V/c$")
    ax.set_ylabel("Payload fraction, $m_\\text{pay}/m_i$")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}"))
    save_figure(fig, "p42-payload-fraction")


# ------------------------------------------------------------------ 6. forces along the flight path
GAMMA = 40.0                                  # drawn flight-path angle, deg


def fig_flight_path_forces():
    """Lesson: along the path, the thrust must first pay for drag and for the part of the weight that
    pulls back along the path; only what is left speeds the vehicle up."""
    fig, ax = new_axes(6.5, 4.1)
    ax.set_xlim(-0.6, 11.6)
    ax.set_ylim(-0.7, 6.6)
    g = GAMMA
    L = 5.4
    parts, u, nose, tail = _vehicle((1.7, 1.2), g, L)
    draw_parts(ax, parts, details=False)
    nrm = np.array([-u[1], u[0]])
    cg = tail + 0.45 * L * u
    # forces where they act: thrust on the engines, drag on the nose, weight at the center of mass
    kind_arrow(ax, tail - 1.6 * u, tail - 0.08 * u, "force")
    text(ax, tail - 1.6 * u, "thrust, $F$", direction=g + 180.0, dist=7.0)
    kind_arrow(ax, nose + 1.2 * u, nose + 0.08 * u, "force")
    text(ax, nose + 1.2 * u, "drag, $D$", direction=g, dist=7.0)
    ax.plot(*cg, "o", ms=5, color=INK, zorder=9)
    kind_arrow(ax, cg, cg + np.array([0.0, -1.8]), "force")
    text(ax, cg + np.array([0.0, -1.8]), "weight, $mg$", direction=-90.0, dist=4.0)
    # velocity along the path, beside the vehicle, with the flight-path angle from the local horizontal
    q = cg + 1.45 * nrm - 1.1 * u
    kind_arrow(ax, q, q + 1.9 * u, "velocity", "velocity, $V$", label_dir=g + 90.0, label_at="mid")
    ax.plot(*np.c_[q, q + np.array([1.5, 0.0])], color=STEEL, lw=LW_THIN, zorder=2)
    text(ax, q, "horizontal", direction=180.0, dist=4.0, fs=FS_SMALL)
    angle_arc(ax, q, 1.0, 0.0, g, "$\\gamma$", dist=6.0)
    # the weight split along and across the path (inset, right)
    o = np.array([9.4, 4.6])
    W = 2.4
    kind_arrow(ax, o, o + np.array([0.0, -W]), "force")
    text(ax, o + np.array([0.0, -W]), "$mg$", direction=-90.0, dist=4.0)
    along = -W * math.sin(math.radians(g)) * u
    across = -W * math.cos(math.radians(g)) * nrm
    # construction: the two parts are the sides of a rectangle whose diagonal is the weight
    for a_, b_ in ((o + along, o + along + across), (o + across, o + along + across)):
        ax.plot(*np.c_[a_, b_], color=STEEL, lw=LW_THIN, ls=(0, (4.0, 2.5)), zorder=3)
    s_ = 0.34                                            # right-angle mark between the two parts
    ua, uc = along / np.linalg.norm(along), across / np.linalg.norm(across)
    ax.plot(*np.c_[o + s_ * ua, o + s_ * (ua + uc), o + s_ * uc], color=INK, lw=LW_THIN, zorder=4)
    close_to(float(np.dot(ua, uc)), 0.0, 1e-12, "the two parts are drawn at a right angle")
    close_to(float(np.linalg.norm(o + along + across - (o + np.array([0.0, -W])))), 0.0, 1e-12,
             "the rectangle closes on the tip of the weight")
    kind_arrow(ax, o, o + along, "force", lw=1.4)
    text(ax, o + along, "$mg\\,\\sin\\gamma$,\nbackward along\nthe path", direction=g + 180.0, dist=4.0)
    kind_arrow(ax, o, o + across, "force", lw=1.4)
    text(ax, o + across, "$mg\\,\\cos\\gamma$\nacross it", direction=-20.0, dist=4.0)
    angle_arc(ax, o, 0.9, -90.0, g - 90.0, "$\\gamma$", dist=6.0)
    text(ax, o + np.array([0.0, 0.5]), "the weight, split", fs=FS_SMALL)
    close_to(float(np.dot(along + across, along + across)), W * W, 1e-9, "the two parts add up to the weight")
    close_to(float(np.dot(along, along)), (W * math.sin(math.radians(g))) ** 2, 1e-9, "along-path part is mg sin(gamma)")
    close_to(float(np.dot(along, u)), -W * math.sin(math.radians(g)), 1e-9, "the along-path part points backward")
    save_figure(fig, "p42-flight-path-forces")


# ------------------------------------------------------------------ 7. worked example 2 as a mass bar
def fig_example_stage():
    """Lesson: to carry 1,750 kg through 3,416 m/s, the stage burns more than three times the payload
    in propellant."""
    e = ex2()
    fig, ax = new_axes(6.5, 2.8)
    ax.set_xlim(-0.4, 10.2)
    ax.set_ylim(-1.75, 2.6)
    sc = 9.6 / e["m_i"]
    b = mass_bar(ax, (0.0, 0.0), [("payload", EX2["m_pay"]), ("inert", e["m_inert"]), ("propellant", e["m_prop"])],
                 sc, 0.9, total=e["m_i"])
    mass_braces(ax, b, [(0, 1, f"final mass, $m_f$ = {fmt(e['m_f'])} kg"),
                        (0, 2, f"initial mass, $m_i$ = {fmt(e['m_i'])} kg")], side=-1, step=30.0)
    i0, a1_ = b["spans"][1][0], b["spans"][2][1]
    yb = 0.9 + 1.05
    brace(ax, (i0, yb), (a1_, yb), f"the stage, inert mass and propellant: {fmt(100.0 * EX2['f'], 2)}% of it is inert",
          side=1)
    close_to(e["m_inert"] / (e["m_inert"] + e["m_prop"]), EX2["f"], 1e-4, "the drawn stage has f_inert = 0.17")
    assert e["m_prop"] > 3.0 * EX2["m_pay"]
    save_figure(fig, "p42-example-stage")


def make_all():
    fig_momentum_exchange()
    fig_mass_ratio()
    fig_three_masses()
    fig_inert_fractions()
    fig_payload_fraction()
    fig_flight_path_forces()
    fig_example_stage()


def values():
    r = lambda k, v: record(PAGE, k, v)                       # noqa: E731
    r("g0", fmt(G0, 3))
    # what the equation says: delta-V of c, 2c, 3c
    for k in MR_MARKS:
        r(f"mr-{k:g}", fmt(math.exp(k)))
        r(f"share-{k:g}", fmt(100.0 * (1.0 - math.exp(-k)), 2))
    r("e", fmt(math.e))
    # worked example 1 (the lectures' Jupiter orbit insertion)
    e1 = ex1()
    r("ex1-mi", fmt(EX1["m_i"]))
    r("ex1-dv-kms", fmt(EX1["dv_kms"], 2))
    r("ex1-dv", fmt(e1["dv"]))
    r("ex1-isp", fmt(EX1["isp"], 3))
    r("ex1-c", fmt(e1["c"]))
    r("ex1-x", fmt(e1["x"], 5))
    r("ex1-ex", fmt(e1["ex"], 5))
    r("ex1-mf", fmt(e1["m_f"]))
    r("ex1-mprop", fmt(e1["m_prop"]))
    r("ex1-share", fmt(100.0 * e1["share"], 2))
    close_to(e1["m_f"], final_mass(EX1["m_i"], e1["dv"], c_from_isp(EX1["isp"])), 0.5, "example 1 against full precision")
    # inert mass fractions of real stages (table and figure)
    for name, veh, kind, dry, prop, src in STAGE_ROWS:
        r(f"st-{name}-dry", fmt(dry / 1000.0))
        r(f"st-{name}-prop", fmt(prop / 1000.0))
        r(f"st-{name}-f", fmt(inert_mass_fraction(dry, prop), 3))
    fs_ = {n: inert_mass_fraction(d, p_) for n, v, k, d, p_, s_ in STAGE_ROWS}
    r("st-f-min", fmt(min(fs_.values()), 2))
    r("st-f-max", fmt(max(fs_.values()), 2))
    # worked example 2: one stage for the Hohmann transfer of page 2.2
    e2 = ex2()
    r("ex2-pay", fmt(EX2["m_pay"]))
    r("ex2-isp", fmt(EX2["isp"], 3))
    r("ex2-f", fmt(EX2["f"], 2))
    r("ex2-dv-kms", fmt(HOHMANN_22["dv_total"]))
    r("ex2-dv1-kms", fmt(HOHMANN_22["dv1"]))
    r("ex2-dv2-kms", fmt(HOHMANN_22["dv2"]))
    r("ex2-dv", fmt(e2["dv"]))
    r("ex2-c", fmt(e2["c"], 6))
    r("ex2-x", fmt(e2["x"], 6))
    r("ex2-ex", fmt(e2["ex"], 6))
    r("ex2-1-f", fmt(1.0 - EX2["f"], 2))
    r("ex2-ex-1", fmt(e2["ex"] - 1.0, 6))
    r("ex2-num", fmt(e2["num"], 6))
    r("ex2-den", fmt(e2["den"], 6))
    r("ex2-mprop", fmt(e2["m_prop"], 5))
    r("ex2-minert", fmt(e2["m_inert"], 5))
    r("ex2-mf", fmt(e2["m_f"], 5))
    r("ex2-mi", fmt(e2["m_i"], 5))
    r("ex2-mprop-r", fmt(e2["m_prop"]))
    r("ex2-minert-r", fmt(e2["m_inert"]))
    r("ex2-mf-r", fmt(e2["m_f"]))
    r("ex2-mi-r", fmt(e2["m_i"]))
    r("ex2-ratio", fmt(e2["ratio"], 5))
    r("ex2-check", fmt(e2["check"]))
    r("ex2-prop-over-pay", fmt(e2["m_prop"] / EX2["m_pay"], 2))
    r("ex2-pf", fmt(100.0 * EX2["m_pay"] / e2["m_i"], 3))
    r("ex2-x-fig", fmt(e2["dv"] / e2["c"]))                   # the worked-example point of fig-p42-payload-fraction
    # how far one stage can go: the limit of the example-2 stage against the launch of page 2.3
    lim2 = single_stage_limit(e2["c"], EX2["f"])
    r("ex2-ln1f", fmt(math.log(1.0 / EX2["f"])))
    r("ex2-limit", fmt(lim2))
    r("launch-kms", fmt(LAUNCH_23["total"]))
    r("launch", fmt(km_as_printed(LAUNCH_23["total"])))
    r("launch-losses", fmt(LAUNCH_23["losses"], 2))
    for name, label in PF_CURVES:
        f = _f_of(name) if name else EX2["f"]
        r(f"pf-lim-{name or 'ex2'}", fmt(math.log(1.0 / f)))
        r(f"pf-f-{name or 'ex2'}", fmt(f, 3) if name else fmt(f, 2))
    # worked example 3: the Ariane 5 core stage alone
    e3 = ex3()
    r("ex3-dry", fmt(A5["dry"]))
    r("ex3-prop", fmt(A5["prop"]))
    r("ex3-m0", fmt(e3["m0"]))
    r("ex3-f", fmt(e3["f"]))
    r("ex3-isp", fmt(A5["isp"], 3))
    r("ex3-c", fmt(e3["c"], 6))
    r("ex3-ratio0", fmt(e3["ratio0"], 5))
    r("ex3-ln0", fmt(math.log(P(e3["ratio0"], 5)), 5))
    r("ex3-dv0", fmt(e3["dv0"]))
    r("ex3-spare", fmt(P(e3["dv0"]) - e3["dv_req"]))
    r("ex3-x", fmt(e3["x"], 6))
    r("ex3-ex", fmt(e3["ex"], 5))
    r("ex3-fe", fmt(e3["fe"], 5))
    r("ex3-num", fmt(e3["num"], 5))
    r("ex3-den", fmt(e3["den"], 5))
    r("ex3-mpay", fmt(e3["m_pay"]))
    r("ex3-mi", fmt(e3["mi"]))
    r("ex3-mf", fmt(e3["mf"]))
    r("ex3-back", fmt(e3["back"]))
    r("ex3-W-N", fmt(e3["W"], 7))
    r("ex3-W", fmt(e3["W"] / 1000.0))
    r("ex3-Fsl", fmt(A5["F_sl"] / 1000.0, 3))
    r("ex3-FW", fmt(e3["FW"], 2))
    r("ex3-isp-sl", fmt(VULCAIN2["isp_sl"], 3))
    r("ex3-pf", fmt(100.0 * P(e3["m_pay"]) / e3["mi"], 2))
    r("ex3-ex-1", fmt(e3["ex"] - 1.0, 5))
    r("ex3-1-f", fmt(1.0 - P(e3["f"]), 5))
    r("ex3-mpay-t", fmt(e3["m_pay"] / 1000.0, 2))
    r("a5-eap-share", fmt(ARIANE5_FLIGHT["eap_thrust_share"], 2))
    r("h1", fmt(HOHMANN_22["h1"], 3))
    r("h2", fmt(HOHMANN_22["h2"]))
    r("ex2-f-pct", fmt(100.0 * EX2["f"], 2))
    close_to(e3["back"], e3["dv_req"], 1.0, "example 3: the largest payload gives back the requirement")
    close_to(e3["dv0"], single_stage_limit(e3["c"], e3["f"]), 1.0, "no payload: the stage's own limit")
