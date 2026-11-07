"""Parametric five-wire trap geometry, shared by the simulation scripts and gds/make_chip.py
(Claude-authored).

One function, build(P), returns the top-metal (Au electrode) polygons plus gds2itvg seed points,
so the GDS that is simulated and the GDS that is fabricated come from the same code.

GDS frame (um): trap axis along x, y in-plane radial, chip centre at (0, 0).
gds2itvg frame (quarter_turns=1): ITVG y = GDS x (axis), ITVG x = -GDS y, z = height.

Layout (top half shown; bottom half is the mirror image):

    y
    |  [ end L ][ s1 ][ s2 ] ... [ sN ][ end R ]   outer DC segments (depth P["dc_depth"])
    |  ======================================      RF rail, width a
    |  --------------------------------------      centre DC, width c  (window cut here)
    +------------------------------------------ x

Electrode numbers (= gds2itvg grid-file numbers):
    1          RF (both rails, one electrode)
    2          centre DC
    3 .. N+2   top outer segments, left to right
    N+3..2N+2  bottom outer segments, left to right
    2N+3, 2N+4 top end caps (left, right); 2N+5, 2N+6 bottom end caps (left, right)
    ground     surrounding Au ground plane (not an output electrode)
"""

import gdstk
import numpy as np

LAYER_AU = 50     # top Au electrodes (see gds/layer_map.md)

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
)


def rect(x0, y0, x1, y1):
    return gdstk.rectangle((x0, y0), (x1, y1), layer=LAYER_AU, datatype=0)


def build(P=None):
    """Return (polygons, seeds, ground_seeds, info) for parameter dict P (defaults: BASE)."""
    P = {**BASE, **(P or {})}
    c, a, g, L = P["c"], P["a"], P["g"], P["half_len"]
    y_rf0, y_rf1 = c / 2 + g, c / 2 + g + a
    y_dc0, y_dc1 = y_rf1 + g, y_rf1 + g + P["dc_depth"]
    polys, seeds, ground = [], {}, {}

    # centre DC (with optional window hole)
    centre = rect(-L, -c / 2, L, c / 2)
    w = P["window"]
    if w and w.get("kind") == "open":
        hole = rect(w["x"] - w["wx"] / 2, -w["wy"] / 2, w["x"] + w["wx"] / 2, w["wy"] / 2)
        centre = gdstk.boolean(centre, hole, "not", layer=LAYER_AU, datatype=0)
        # seed must sit on metal: put it well away from the hole
        seeds["2"] = [[w["x"] + w["wx"] / 2 + 50.0, 0.0]]
    else:
        centre = [centre]
        seeds["2"] = [[0.0, 0.0]] if not w else [[w["x"] + 100.0, 0.0]]
    polys += centre

    # RF rails (one electrode)
    polys.append(rect(-L, y_rf0, L, y_rf1))
    polys.append(rect(-L, -y_rf1, L, -y_rf0))
    seeds["1"] = [[0.0, (y_rf0 + y_rf1) / 2], [0.0, -(y_rf0 + y_rf1) / 2]]

    # outer DC segments + end caps
    N, sw, x0 = P["n_seg"], P["seg_w"], P["seg_x0"]
    xs = [x0 + k * (sw + g) for k in range(N)]
    seg_centres = [x + sw / 2 for x in xs]
    for side, (ya, yb), first in ((+1, (y_dc0, y_dc1), 3), (-1, (-y_dc1, -y_dc0), 3 + N)):
        for k, xl in enumerate(xs):
            polys.append(rect(xl, ya, xl + sw, yb))
            seeds[str(first + k)] = [[xl + sw / 2, (ya + yb) / 2]]
    xl_end = xs[0] - g
    xr_end = xs[-1] + sw + g
    caps = {}
    for side, (ya, yb), (nl, nr) in ((+1, (y_dc0, y_dc1), (2 * N + 3, 2 * N + 4)),
                                     (-1, (-y_dc1, -y_dc0), (2 * N + 5, 2 * N + 6))):
        polys.append(rect(-L, ya, xl_end, yb))
        polys.append(rect(xr_end, ya, L, yb))
        seeds[str(nl)] = [[(-L + xl_end) / 2, (ya + yb) / 2]]
        seeds[str(nr)] = [[(xr_end + L) / 2, (ya + yb) / 2]]
        caps[side] = (nl, nr)

    # surrounding ground frame
    G = P["guard"]
    outer = gdstk.rectangle((-L - g - G, -y_dc1 - g - G), (L + g + G, y_dc1 + g + G))
    inner = gdstk.rectangle((-L - g, -y_dc1 - g), (L + g, y_dc1 + g))
    polys += gdstk.boolean(outer, inner, "not", layer=LAYER_AU, datatype=0)
    ground["99"] = [[0.0, y_dc1 + g + G / 2]]

    info = dict(P=P, y_rf=(y_rf0, y_rf1), y_dc=(y_dc0, y_dc1), seg_centres=seg_centres,
                top=list(range(3, 3 + N)), bottom=list(range(3 + N, 3 + 2 * N)), caps=caps,
                roi_box=[-L, -y_dc1 - g - G, L, y_dc1 + g + G])
    return polys, seeds, ground, info


def write(path_stem, P=None, gap_model="profile", ground_depth=10.0, metal_thickness=6.0,
          epsilon_r=3.9, outer_ground_depth=None, cell="TRAP"):
    """Write <stem>.gds and <stem>.json (gds2itvg layout). Returns (gds, json, info).

    Defaults describe our stack: ~6 um plated Au on ~10 um SiO2 over the Al ground plane.
    outer_ground_depth=None grounds the surface outside the ROI (the chip is covered in
    grounded Au/Al around the trap, so this matches the real chip better than a floating edge).
    """
    from gds2itvg import Layout
    from gds2itvg.frame import Frame
    polys, seeds, ground, info = build(P)
    lib = gdstk.Library(unit=1e-6, precision=1e-9)
    top = lib.new_cell(cell)
    for p in polys:
        top.add(p)
    lib.write_gds(path_stem + ".gds")
    lay = Layout(layer=LAYER_AU, datatype=0, roi_box=tuple(info["roi_box"]),
                 frame=Frame(origin=(0.0, 0.0), quarter_turns=1, mirror=False),
                 electrodes=seeds, ground=ground, max_gap=30.0, gap_model=gap_model,
                 metal_thickness=metal_thickness, ground_depth=ground_depth,
                 epsilon_r=epsilon_r, outer_ground_depth=outer_ground_depth)
    lay.to_json(path_stem + ".json", comment="generated by design/sim/trapgeom.py")
    return path_stem + ".gds", path_stem + ".json", info


def itvg(x_gds, y_gds=0.0, z=50.0):
    """GDS (x, y) + height -> ITVG point."""
    return np.array([-y_gds, x_gds, z])
