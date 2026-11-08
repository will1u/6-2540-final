"""NbN meander geometry shared by make_chip.py and make_test_die.py (Claude-authored; DESIGN_LOG step 24).

One function, meander(). Lines run along x (the trap axis). The line count is even, so both free
ends (signal = top line, return = bottom line) leave on the -x side.

turn="sharp"  the v3 drawing: 1-wire-wide straight bars at the line ends (square corners) and abrupt
              40 x 3 um tabs that step out from the outer lines. Kept for the test-die control.
turn="round"  v3.1: each 180-degree turn is a solid end block (p + w tall, `block` long) placed past
              the line ends, with the slot between the two arms closed by a semicircle (diameter =
              gap), not a square corner. The outer lines run past the end blocks and widen smoothly
              into their tabs (edge y = w + (H - w)(s/L)^2: tangent to the wire, no re-entrant
              corner), on the side that faces y = yc, so no NbN goes further from the axis than the
              outer lines. Turn crowding: Clem & Berggren, PRB 84, 174510 (2011), Secs. VII.4-VII.5;
              tapers: Sec. X.2 (research/reports/SNSPD geometry audit.md).

Units um. Returns (polygons on `layer`, signal-tab lead point, return-tab lead point). The lead
points are the tab centres; the Ti/Au lead starts there and covers the half of the tab towards -x.
"""

import gdstk

TAB_L, TAB_H = 40.0, 3.0               # tab length (x) and height (y)
TAPER_L = 6.0                          # length of the wire-to-tab flare (round turns only)
TAB_GAP = 0.5                          # clearance between the left end blocks and the start of a flare


def rect(x0, y0, x1, y1, layer):
    return gdstk.rectangle((min(x0, x1), min(y0, y1)), (max(x0, x1), max(y0, y1)), layer=layer)


def meander(xc, yc, lx, ly, w, p, turn="round", block=0.5, layer=20):
    """Meander of straight lines lx long, filling ly in y at pitch p with wire width w, centred on (xc, yc)."""
    n = int(round(ly / p))
    n += n % 2
    x0, x1 = xc - lx / 2, xc + lx / 2
    if turn == "sharp":                        # v3: lines start at yc - ly/2 (exactly as make_chip v3)
        y0 = yc - ly / 2
    else:                                      # centred: the outer edges sit at yc +- ((n-1)p + w)/2
        y0 = yc - ((n - 1) * p + w) / 2
    g = p - w
    polys = [rect(x0, y0 + k * p, x1, y0 + k * p + w, layer) for k in range(n)]
    for k in range(n - 1):                     # turn joining line k and line k+1
        y = y0 + k * p
        right = k % 2 == 0
        if turn == "sharp":
            xe = x1 if right else x0 - w
            polys.append(rect(xe, y, xe + w, y + p + w, layer))
        else:
            xa, xb = (x1, x1 + block) if right else (x0 - block, x0)
            cap = gdstk.ellipse((x1 if right else x0, y + w + g / 2), g / 2, tolerance=0.002)
            polys += gdstk.boolean(rect(xa, y, xb, y + p + w, layer), cap, "not", layer=layer)
    y_last = y0 + (n - 1) * p
    if turn == "sharp":                        # abrupt tabs stepping outwards (v3)
        polys.append(rect(x0 - TAB_L, y0 - TAB_H, x0, y0 + w, layer))                 # return end
        polys.append(rect(x0 - TAB_L, y_last, x0, y_last + w + TAB_H, layer))         # signal end
        return polys, (x0 - 20, y_last + TAB_H / 2), (x0 - 20, y0 - TAB_H / 2)
    # round: outer lines run on past the left end blocks, then flare inwards into the tabs
    xt = x0 - block - TAB_GAP                  # flare start
    xtab = xt - TAPER_L                        # tab starts here and runs TAB_L towards -x
    ends = {}
    for name, yo, s in (("ret", y0, +1), ("sig", y_last + w, -1)):   # yo = outer edge; s = inward direction
        polys.append(rect(xt, yo, x0, yo + s * w, layer))           # extension past the end blocks
        m = 40
        pts = [(xt - TAPER_L * j / m, yo + s * (w + (TAB_H - w) * (j / m) ** 2)) for j in range(m + 1)]
        polys.append(gdstk.Polygon([(xt, yo)] + pts + [(xtab, yo)], layer=layer))
        polys.append(rect(xtab - TAB_L, yo, xtab, yo + s * TAB_H, layer))
        ends[name] = (xtab - TAB_L / 2, yo + s * TAB_H / 2)
    return polys, ends["sig"], ends["ret"]


def straight(xc, yc, lx, w, layer=20):
    """Straight wire lx long (critical-current reference), widening smoothly into a tab at each end.

    Returns (polygons, left-tab lead point, right-tab lead point)."""
    x0, x1 = xc - lx / 2, xc + lx / 2
    polys = [rect(x0, yc - w / 2, x1, yc + w / 2, layer)]
    m, ends = 40, []
    for xe, s in ((x0, -1), (x1, +1)):                     # s: outward direction along x
        top = [(xe + s * TAPER_L * j / m, yc + w / 2 + (TAB_H - w) / 2 * (j / m) ** 2) for j in range(m + 1)]
        bot = [(x, 2 * yc - y) for x, y in reversed(top)]
        polys.append(gdstk.Polygon(top + bot, layer=layer))
        xt = xe + s * TAPER_L
        polys.append(rect(xt, yc - TAB_H / 2, xt + s * TAB_L, yc + TAB_H / 2, layer))
        ends.append((xt + s * TAB_L / 2, yc))
    return polys, ends[0], ends[1]
