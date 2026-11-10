"""Parametric five-wire trap geometry, used by sims 02, 03, 04 and 05 only (make_chip.py does not import it)
(Claude-authored).

One function, build(P), returns the top-metal (Au electrode) polygons plus gds2itvg seed points,
so the GDS that is simulated and the GDS that is fabricated come from the same code.

GDS frame (um): trap axis along x, y in-plane radial, chip centre at (0, 0).
gds2itvg frame (quarter_turns=1): ITVG y = GDS x (axis), ITVG x = -GDS y, z = height.

Layout (top half shown; bottom half is the mirror image unless a_top / a_bot differ):

    y
    |  [ end L ][ s1 ][ s2 ] ... [ sN ][ end R ]   outer DC segments (depth P["dc_depth"])
    |  ======================================      RF rail, width a (a_top on +y, a_bot on -y)
    |  --------------------------------------      centre DC, width c  (window cut here)
    +------------------------------------------ x

Electrode numbers (= gds2itvg grid-file numbers):
    1          RF (both rails, one electrode)
    2          centre DC (the top half if c_split_gap is set)
    3 .. N+2   top outer segments, left to right
    N+3..2N+2  bottom outer segments, left to right
    2N+3, 2N+4 top end caps (left, right); 2N+5, 2N+6 bottom end caps (left, right)
    2N+7       bottom half of the centre DC, only with c_split_gap
    2N+8, 2N+9 c_split_x range 1: top and bottom island; 2N+10, 2N+11 range 2; and so on
    97, 98     SNSPD lead strips (ground), only with c_split_leads
    99         ground (surrounding Au ground plane; not an output electrode)

Optional keys (all off by default; sims 02-05 use the defaults, so their output does not change):
    a_top, a_bot     RF rail width on the +y and -y side (None = a)
    c_split_gap      cut the centre DC along its whole length with a gap of this width at y = 0
    c_split_leads    inside that gap, two grounded strips (electrodes 97, 98) at y = +-5 um
    c_split_x        list of (x0, x1): replace the centre DC there by two islands
"""

import json
import os

import gdstk
import numpy as np

LAYER_AU = 50     # top Au electrodes (see gds/layer_map.md)
LEAD_W = 5.0      # width of the SNSPD lead strips (um)
LEAD_Y = 5.0      # their centre |y| (um)
V4_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gds", "trap_die_v4_UNIFORM_sim.json")

# Baseline parameters (see DESIGN_LOG.md, steps 1-3). All um.
BASE = dict(
    c=40.0,            # centre DC width
    a=84.0,            # RF rail width
    g=5.0,             # gap
    half_len=2500.0,   # half length of rails used for simulation (chip uses its own)
    dc_depth=400.0,    # radial extent of the outer DC segments
    seg_w=95.0,        # outer segment width along the axis (pitch = seg_w + g)
    n_seg=16,          # segments per side
    seg_x0=-1300.0,    # x of the left edge of the first segment
    guard=200.0,       # width of the surrounding ground frame (simulation only)
    window=None,       # dict(x=..., wx=..., wy=..., kind='open'|'none') hole in centre DC
    a_top=None,        # RF rail width on the +y side (None: a)
    a_bot=None,        # RF rail width on the -y side (None: a)
    c_split_gap=None,     # gap width cut along the whole centre DC (None: no cut)
    c_split_leads=False,  # grounded lead strips inside that gap (needs c_split_gap >= 15)
    c_split_x=None,       # list of (x0, x1) ranges where the centre DC becomes two islands
)


def rect(x0, y0, x1, y1):
    return gdstk.rectangle((x0, y0), (x1, y1), layer=LAYER_AU, datatype=0)


def _overlaps(a, b):
    """True if boxes (x0, y0, x1, y1) a and b overlap."""
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def _seed_point(w, box):
    """Seed on metal for a centre piece box (x0, y0, x1, y1), kept away from the window hole."""
    x0, y0, x1, y1 = box
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    if not w:
        return [xm, ym]
    if x0 < w["x"] < x1:
        # piece contains the window: seed beyond the hole, as the unsplit code always did
        if w.get("kind") == "open":
            xs = w["x"] + w["wx"] / 2 + 50.0
        else:
            xs = w["x"] + 100.0
        if not x0 < xs < x1:
            raise ValueError("no seed on metal for piece %s" % (box,))
        return [xs, ym]
    return [xm, ym]


def _centre_pieces(P, L, c, g, N):
    """Centre DC before the window cut: (pieces, leads, split_names).

    pieces: list of (name, x0, y0, x1, y1). leads: ground strips (names 97, 98).
    """
    gap, xs = P["c_split_gap"], P["c_split_x"]
    if gap is not None and xs is not None:
        raise ValueError("c_split_gap and c_split_x together are not supported")
    if P["c_split_leads"] and (gap is None or gap < 15.0):
        raise ValueError("c_split_leads needs c_split_gap >= 15")
    if gap is None and xs is None:
        return [("2", -L, -c / 2, L, c / 2)], [], []

    if gap is not None:
        h = gap / 2
        if not 0 < h < c / 2:
            raise ValueError("c_split_gap must be between 0 and c")
        bot = str(2 * N + 7)
        pieces = [("2", -L, h, L, c / 2), (bot, -L, -c / 2, L, -h)]
        leads = []
        if P["c_split_leads"]:
            for name, yc in (("97", LEAD_Y), ("98", -LEAD_Y)):
                leads.append((name, -L, yc - LEAD_W / 2, L, yc + LEAD_W / 2))
        return pieces, leads, [bot]

    # c_split_x: solid centre DC with a gap g at each end of every range, islands inside the ranges
    rngs = sorted((float(p), float(q)) for p, q in xs)
    for p, q in rngs:
        if not (-L < p < q < L):
            raise ValueError("c_split_x range (%g, %g) outside the centre DC" % (p, q))
    for (p0, p1), (q0, q1) in zip(rngs, rngs[1:]):
        if q0 - g <= p1 + g:
            raise ValueError("c_split_x ranges too close")
    pieces, cur = [], -L
    for p, q in rngs:
        if p - g > cur:
            pieces.append(("2", cur, -c / 2, p - g, c / 2))
        cur = q + g
    if cur < L:
        pieces.append(("2", cur, -c / 2, L, c / 2))
    split = []
    for k, (p, q) in enumerate(rngs):
        top, bot = str(2 * N + 8 + 2 * k), str(2 * N + 9 + 2 * k)
        pieces.append((top, p, g / 2, q, c / 2))
        pieces.append((bot, p, -c / 2, q, -g / 2))
        split += [top, bot]
    return pieces, [], split


def build(P=None):
    """Return (polygons, seeds, ground_seeds, info) for parameter dict P (defaults: BASE)."""
    P = {**BASE, **(P or {})}
    c, g, L, N = P["c"], P["g"], P["half_len"], P["n_seg"]
    sw, x0, dc, G = P["seg_w"], P["seg_x0"], P["dc_depth"], P["guard"]
    a_t = P["a"] if P["a_top"] is None else P["a_top"]
    a_b = P["a"] if P["a_bot"] is None else P["a_bot"]
    w = P["window"]
    polys, seeds, ground = [], {}, {}

    # RF rails and outer DC rows on each side (y ranges as (low, high))
    yr = c / 2 + g
    y_rf_top = (yr, yr + a_t)
    y_dc_top = (yr + a_t + g, yr + a_t + g + dc)
    y_rf_bot = (-(yr + a_b), -yr)
    y_dc_bot = (-(yr + a_b + g + dc), -(yr + a_b + g))

    # centre DC (with optional split and window hole); the window hole is cut from each piece it overlaps
    pieces, leads, split_names = _centre_pieces(P, L, c, g, N)
    hole = None
    if w and w.get("kind") == "open":
        hole = (w["x"] - w["wx"] / 2, -w["wy"] / 2, w["x"] + w["wx"] / 2, w["wy"] / 2)
    for name, xa, ya, xb, yb in pieces + leads:
        box = (xa, ya, xb, yb)
        if hole is not None and _overlaps(hole, box):
            parts = gdstk.boolean(rect(*box), rect(*hole), "not", layer=LAYER_AU, datatype=0)
        else:
            parts = [rect(*box)]
        polys += parts
        pt = _seed_point(w, box)
        if hole is not None and abs(pt[0] - w["x"]) < w["wx"] / 2 and abs(pt[1]) < w["wy"] / 2:
            raise ValueError("seed for %s lies in the window" % name)
        target = ground if name in ("97", "98") else seeds
        target.setdefault(name, []).append(pt)
    centre_names = []
    for name, *_ in pieces:
        if name not in centre_names:
            centre_names.append(name)

    # RF rails (one electrode)
    polys.append(rect(-L, y_rf_top[0], L, y_rf_top[1]))
    polys.append(rect(-L, y_rf_bot[0], L, y_rf_bot[1]))
    seeds["1"] = [[0.0, (y_rf_top[0] + y_rf_top[1]) / 2], [0.0, (y_rf_bot[0] + y_rf_bot[1]) / 2]]

    # outer DC segments + end caps
    xs = [x0 + k * (sw + g) for k in range(N)]
    seg_centres = [x + sw / 2 for x in xs]
    for (ya, yb), first in ((y_dc_top, 3), (y_dc_bot, 3 + N)):
        for k, xl in enumerate(xs):
            polys.append(rect(xl, ya, xl + sw, yb))
            seeds[str(first + k)] = [[xl + sw / 2, (ya + yb) / 2]]
    xl_end = xs[0] - g
    xr_end = xs[-1] + sw + g
    caps = {}
    for side, (ya, yb), (nl, nr) in ((+1, y_dc_top, (2 * N + 3, 2 * N + 4)),
                                     (-1, y_dc_bot, (2 * N + 5, 2 * N + 6))):
        polys.append(rect(-L, ya, xl_end, yb))
        polys.append(rect(xr_end, ya, L, yb))
        seeds[str(nl)] = [[(-L + xl_end) / 2, (ya + yb) / 2]]
        seeds[str(nr)] = [[(xr_end + L) / 2, (ya + yb) / 2]]
        caps[side] = (nl, nr)

    # surrounding ground frame
    ymin, ymax = y_dc_bot[0], y_dc_top[1]
    outer = gdstk.rectangle((-L - g - G, ymin - g - G), (L + g + G, ymax + g + G))
    inner = gdstk.rectangle((-L - g, ymin - g), (L + g, ymax + g))
    polys += gdstk.boolean(outer, inner, "not", layer=LAYER_AU, datatype=0)
    ground["99"] = [[0.0, ymax + g + G / 2]]

    info = dict(P=P, y_rf=y_rf_top, y_dc=y_dc_top, seg_centres=seg_centres,
                top=list(range(3, 3 + N)), bottom=list(range(3 + N, 3 + 2 * N)), caps=caps,
                roi_box=[-L, ymin - g - G, L, ymax + g + G],
                y_rf_top=y_rf_top, y_rf_bot=y_rf_bot, y_dc_top=y_dc_top, y_dc_bot=y_dc_bot,
                centre_names=centre_names, split_names=split_names)
    return polys, seeds, ground, info


def write(path_stem, P=None, gap_model="profile", ground_depth=10.0, metal_thickness=6.0,
          epsilon_r=3.9, outer_ground_depth=None, cell="TRAP", stack=None, max_gap=30.0):
    """Write <stem>.gds and <stem>.json (gds2itvg layout). Returns (gds, json, info).

    Defaults describe our stack: ~6 um plated Au on ~10 um SiO2 over the Al ground plane.
    outer_ground_depth=None grounds the surface outside the ROI (the chip is covered in
    grounded Au/Al around the trap, so this matches the real chip better than a floating edge).

    stack=None: the keyword arguments above are used as given (old behaviour).
    stack="v4": gap_model, metal_thickness, ground_depth, epsilon_r, outer_ground_depth and max_gap
    are read from design/gds/trap_die_v4_UNIFORM_sim.json instead, and the keyword arguments
    above are IGNORED (the v4 values win).
    """
    from gds2itvg import Layout
    from gds2itvg.frame import Frame
    if stack is None:
        stack_kw = dict(gap_model=gap_model, metal_thickness=metal_thickness, ground_depth=ground_depth,
                        epsilon_r=epsilon_r, outer_ground_depth=outer_ground_depth, max_gap=max_gap)
    elif stack == "v4":
        with open(V4_JSON) as f:
            ref = json.load(f)
        stack_kw = {k: ref[k] for k in ("gap_model", "metal_thickness", "ground_depth", "epsilon_r",
                                        "outer_ground_depth", "max_gap")}
    else:
        raise ValueError("stack must be None or 'v4'")
    polys, seeds, ground, info = build(P)
    lib = gdstk.Library(unit=1e-6, precision=1e-9)
    top = lib.new_cell(cell)
    for p in polys:
        top.add(p)
    lib.write_gds(path_stem + ".gds")
    lay = Layout(layer=LAYER_AU, datatype=0, roi_box=tuple(info["roi_box"]),
                 frame=Frame(origin=(0.0, 0.0), quarter_turns=1, mirror=False),
                 electrodes=seeds, ground=ground, **stack_kw)
    lay.to_json(path_stem + ".json", comment="generated by design/sim/trapgeom.py")
    return path_stem + ".gds", path_stem + ".json", info


def itvg(x_gds, y_gds=0.0, z=50.0):
    """GDS (x, y) + height -> ITVG point."""
    return np.array([-y_gds, x_gds, z])
