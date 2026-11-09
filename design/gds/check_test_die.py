"""Independent checker for the 10 x 2.5 mm test-structure dies (Claude-authored).

Usage (from design/sim):
  ./run.sh ../gds/check_test_die.py test_die_v4
  ./run.sh ../gds/check_test_die.py test_die_v4_TRAP

Reads <stem>.gds only. The checks are derived from the test-die spec and from the GDS itself; this file does not
import make_test_die.py or any other generator. Units um. Every check prints one PASS or FAIL line; indented lines
under a FAIL give the offending coordinates. C9 prints INFO lines (not pass/fail). Exit code 1 if any check fails.

  C1  layers 24, 30, 31, 45 empty; die outline on layer 101 is 10 x 2.5 mm centred on (0, 0); nothing outside it
  C2  Au (50) conductors: count; >= 5 um spacing (grow each by 2.49 um, merge, count must not change)
  C3  Au ground fill is the largest conductor; every other conductor is >= 100 x 100 um or >= 10000 um^2
  C4  every layer-40 opening lies on Ti/Au (22), on Al (10), or at an alignment-mark cross
  C5  layer-40 openings on Al: covered by one Au conductor and inside the Al, both by >= 15 um
  C6  NbN (20) pieces: each overlaps >= 2 Ti/Au (22) leads; the T3 bar (the piece with the most leads) overlaps 4
  C7  each NbN meander (bbox > 15 um both ways): its bbox grown by 3 um lies inside one Al piece
  C8  named structures T10, T11, T12, T2v, T1, T6 (full die); T1 and T6 only on the TRAP die
  C9  INFO: merged area and polygon count per layer

TRAP die (file name contains "TRAP"): C1, C2, C3, T1, T6, C9, and layers 10, 20, 22, 40 empty.
Boolean operations use gdstk 1.0 (polygon results are simple outlines; holes are bridged into them).
"""

import os
import sys
from collections import Counter

import gdstk
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STEM = sys.argv[1] if len(sys.argv) > 1 else "test_die_v4"
TRAP = "TRAP" in STEM

PREC = 1e-6                                       # boolean / offset grid, um
EPS = 1e-4                                        # um^2: a remainder below this counts as empty
DIE = (-5000.0, -1250.0, 5000.0, 1250.0)          # 10 mm x 2.5 mm, centred on (0, 0)
MARKS = [(-1700.0, -1080.0), (-1700.0, 1080.0), (4300.0, -1080.0), (4300.0, 1080.0)]

N_FAIL = 0


def report(ok, msg):
    global N_FAIL
    if not ok:
        N_FAIL += 1
    print(("PASS " if ok else "FAIL ") + msg)


def detail(lines):
    for s in lines:
        print("     " + s)


def fmt(b):
    return "(%.1f, %.1f)-(%.1f, %.1f)" % b


def bbox(p):
    (x0, y0), (x1, y1) = p.bounding_box()
    return (x0, y0, x1, y1)


def centre(p):
    x0, y0, x1, y1 = bbox(p)
    return ((x0 + x1) / 2, (y0 + y1) / 2)


def bboxes_overlap(a, b, margin=0.0):
    return not (a[0] - margin > b[2] or b[0] - margin > a[2] or a[1] - margin > b[3] or b[1] - margin > a[3])


def merge(polys):
    """Union (gdstk 'or') of a set of polygons."""
    if not polys:
        return []
    return gdstk.boolean(list(polys), [], "or", precision=PREC)


def area_of(polys):
    return sum(p.area() for p in polys)


def leftover(a, b):
    """Area of a that is not covered by b. Zero means a lies inside b."""
    if not a:
        return 0.0
    if not b:
        return area_of(a)
    return area_of(gdstk.boolean(list(a), list(b), "not", precision=PREC))


def inside(a, b):
    return leftover(a, b) < EPS


def piece_at(pt, polys):
    """Index of the polygon in polys that contains pt, or None."""
    for i, p in enumerate(polys):
        if p.contain(pt):
            return i
    return None


def enclosure(p, region, dmax=100.0):
    """Largest distance d (um) such that p grown by d (miter) still lies inside region. -1 if p is not inside."""
    if not inside([p], [region]):
        return -1.0

    def grow(d):
        return gdstk.offset([p], d, join="miter", precision=PREC)

    if inside(grow(dmax), [region]):
        return dmax
    lo, hi = 0.0, dmax
    for _ in range(30):                           # bisection to ~1e-9 um
        mid = 0.5 * (lo + hi)
        if inside(grow(mid), [region]):
            lo = mid
        else:
            hi = mid
    return lo


# ---------------------------------------------------------------- load
lib = gdstk.read_gds(os.path.join(HERE, STEM + ".gds"))
tops = lib.top_level()
polys = tops[0].get_polygons() if tops else []
L = {}
for p in polys:
    L.setdefault(p.layer, []).append(p)
print(f"== {STEM}: {len(polys)} polygons, top cells {[c.name for c in tops]}, TRAP die: {TRAP}")

# ---------------------------------------------------------------- C1
print("-- C1 layers, die outline")
report(len(tops) == 1, f"C1 single top cell ({[c.name for c in tops]})")
empty = {n: len(L.get(n, [])) for n in (24, 30, 31, 45)}
report(not any(empty.values()), f"C1 layers 24, 30, 31, 45 empty (polygon counts {empty})")
outline = [bbox(p) for p in L.get(101, [])]
report(len(outline) == 1 and all(abs(a - b) < 1e-3 for a, b in zip(outline[0], DIE)),
       f"C1 die outline on layer 101 is {DIE} (found {outline})")
outside = [(n, bbox(p)) for n, ps in L.items() for p in ps
           if bbox(p)[0] < DIE[0] - 1e-6 or bbox(p)[2] > DIE[2] + 1e-6
           or bbox(p)[1] < DIE[1] - 1e-6 or bbox(p)[3] > DIE[3] + 1e-6]
report(not outside, f"C1 no polygon outside the die ({len(outside)} outside)")
detail([f"layer {n} bbox {fmt(b)}" for n, b in outside[:20]])

# ---------------------------------------------------------------- C2
print("-- C2 Au spacing")
au = merge(L.get(50, []))                         # Au conductors (merged, one polygon per conductor)
n_au = len(au)
grown = [gdstk.offset([p], 2.49, join="miter", precision=PREC) for p in au]
n_grown = len(merge([g for gi in grown for g in gi]))
close_pairs = []
for i in range(n_au):
    for j in range(i + 1, n_au):
        if not bboxes_overlap(bbox(au[i]), bbox(au[j]), 5.0):
            continue
        if area_of(gdstk.boolean(grown[i], grown[j], "and", precision=PREC)) > EPS:
            close_pairs.append((i, j))
report(n_grown == n_au and not close_pairs,
       f"C2 {n_au} Au conductors; grown by 2.49 um they merge to {n_grown} (must stay {n_au}); "
       f"{len(close_pairs)} pair(s) closer than 5 um")
detail([f"conductor {i} bbox {fmt(bbox(au[i]))}  <->  conductor {j} bbox {fmt(bbox(au[j]))}"
        for i, j in close_pairs[:30]])

# ---------------------------------------------------------------- C3
print("-- C3 floating Au")
if n_au:
    fill_i = max(range(n_au), key=lambda i: au[i].area())
    odd = []
    for i in range(n_au):
        if i == fill_i:
            continue
        x0, y0, x1, y1 = bbox(au[i])
        big = (x1 - x0 >= 100 - 1e-6 and y1 - y0 >= 100 - 1e-6) or au[i].area() >= 10000
        if not big:
            odd.append(i)
    report(not odd, f"C3 ground fill is the largest Au conductor (area {au[fill_i].area():.0f} um^2, bbox "
                    f"{fmt(bbox(au[fill_i]))}); {len(odd)} other conductor(s) smaller than 100 x 100 um / 10000 um^2")
    detail([f"conductor {i}: bbox {fmt(bbox(au[i]))}, area {au[i].area():.1f} um^2" for i in odd])
else:
    report(False, "C3 no Au conductors found")

# ---------------------------------------------------------------- C4 to C7 (full die only)
if not TRAP:
    print("-- C4 layer-40 openings")
    L22 = merge(L.get(22, []))
    L10 = merge(L.get(10, []))
    kinds = {"a": [], "b": [], "c": [], "x": []}
    for p in L.get(40, []):
        c = centre(p)
        if inside([p], L22):
            kinds["a"].append(p)
        elif inside([p], L10):
            kinds["b"].append(p)
        elif any(np.hypot(c[0] - mx, c[1] - my) <= 100 for mx, my in MARKS):
            kinds["c"].append(p)
        else:
            kinds["x"].append(p)
    report(not kinds["x"],
           f"C4 layer-40 openings: {len(kinds['a'])} on Ti/Au (22), {len(kinds['b'])} on Al (10), "
           f"{len(kinds['c'])} mark crosses, {len(kinds['x'])} other")
    detail([f"opening bbox {fmt(bbox(p))}" for p in kinds["x"]])

    print("-- C5 openings on Al covered by Au")
    enc_au, enc_al, bad5 = [], [], []
    for p in kinds["b"]:
        c = centre(p)
        ia = piece_at(c, au)
        ib = piece_at(c, L10)
        if ia is None or ib is None:
            bad5.append(f"opening {fmt(bbox(p))}: no Au or no Al at its centre")
            continue
        ea = enclosure(p, au[ia])
        eb = enclosure(p, L10[ib])
        enc_au.append(ea)
        enc_al.append(eb)
        if ea < 15 - 1e-3 or eb < 15 - 1e-3:
            bad5.append(f"opening {fmt(bbox(p))}: enclosure by Au {ea:.2f} um, by Al {eb:.2f} um")
    min_au = min(enc_au) if enc_au else float("nan")
    min_al = min(enc_al) if enc_al else float("nan")
    report(not bad5, f"C5 {len(kinds['b'])} openings on Al: minimum enclosure by Au {min_au:.2f} um, "
                     f"by Al {min_al:.2f} um (need >= 15)")
    detail(bad5)

    print("-- C6 NbN connectivity")
    NB_all = merge(L.get(20, []))
    leads = merge(L.get(22, []))
    nb, ignored = [], 0
    for p in NB_all:
        c = centre(p)
        near_mark = any(np.hypot(c[0] - mx, c[1] - my) <= 100 for mx, my in MARKS)
        if p.area() < 20 and near_mark:
            ignored += 1
            continue
        nb.append(p)
    lead_hits = []
    for p in nb:
        hits = []
        for j, q in enumerate(leads):
            if not bboxes_overlap(bbox(p), bbox(q)):
                continue
            if area_of(gdstk.boolean([p], [q], "and", precision=PREC)) > 1e-6:
                hits.append(j)
        lead_hits.append(len(hits))
    if nb:
        t3i = max(range(len(nb)), key=lambda i: lead_hits[i])
        t3_ok = lead_hits[t3i] == 4 and lead_hits.count(4) == 1
    else:
        t3i, t3_ok = None, False
    others = [lead_hits[i] for i in range(len(nb)) if i != t3i]
    hist = dict(sorted(Counter(others).items()))
    report(t3_ok and all(c >= 2 for c in others),
           f"C6 {len(nb)} NbN pieces (ignored {ignored} overlay squares); leads touched by the other pieces: "
           f"histogram {hist}; T3 bar {fmt(bbox(nb[t3i])) if nb else 'none'} touches {lead_hits[t3i] if nb else 0} leads")
    detail([f"NbN piece {fmt(bbox(p))} touches {n} lead(s)" for p, n in zip(nb, lead_hits) if n < 2 and p is not nb[t3i]])

    print("-- C7 local Al mirror under each meander")
    checked, narrow, bad7 = 0, 0, []
    for i, p in enumerate(nb):
        if i == t3i:
            continue
        x0, y0, x1, y1 = bbox(p)
        if x1 - x0 <= 15 or y1 - y0 <= 15:
            narrow += 1
            continue
        checked += 1
        g = gdstk.rectangle((x0 - 3, y0 - 3), (x1 + 3, y1 + 3))
        if not any(inside([g], [al]) for al in L10):
            bad7.append(f"NbN piece {fmt((x0, y0, x1, y1))}: grown bbox not inside one Al piece")
    report(not bad7, f"C7 {checked} meanders checked (bbox grown 3 um inside one Al piece); {narrow} narrow NbN "
                     f"pieces skipped (straight references); T3 bar skipped")
    detail(bad7)

# ---------------------------------------------------------------- C8 named structures
print("-- C8 named structures")
au_at = lambda pt: piece_at(pt, au)
L10_m = merge(L.get(10, []))
al_at = lambda pt: piece_at(pt, L10_m)

a1, b1 = au_at((-4300, 350)), au_at((-3600, 600))
report(a1 is not None and b1 is not None and a1 != b1,
       f"C8 T1 comb: Au at (-4300,350) and (-3600,600) are different conductors ({a1}, {b1})")
a6, b6 = au_at((3500, 300)), au_at((4255, 300))
report(a6 is not None and a6 == b6, f"C8 T6 loop: Au at (3500,300) and (4255,300) are one conductor ({a6}, {b6})")

if not TRAP:
    pts = [(-4570, -100), (-1920, -100), (-4455, -220), (-1945, -220), (-3000, -100)]
    ids = [al_at(p) for p in pts]
    report(ids[0] is not None and all(i == ids[0] for i in ids),
           f"C8 T10 strip: the five points lie in one Al piece ({ids})")
    s_in = [al_at((-3000, y)) == ids[0] for y in (-119, -81)]
    s_out = [al_at((-3000, y)) != ids[0] for y in (-121, -79)]
    report(all(s_in) and all(s_out),
           f"C8 T10 strip 40 um wide at x=-3000: inside at y=-119 and -81 {s_in}, outside at y=-121 and -79 {s_out}")
    taps = (-1945) - (-4455)
    report(taps == 2510 and al_at((-4455, -150)) == ids[0] and al_at((-1945, -150)) == ids[0],
           f"C8 T10 tap stubs at x=-4455 and x=-1945 on the strip, {taps} um apart")

    b_a, b_b = al_at((2000, -100)), al_at((2600, -100))
    report(b_a is not None and b_b is not None and b_a != b_b,
           f"C8 T11 Al: (2000,-100) and (2600,-100) in two different Al pieces ({b_a}, {b_b})")
    c3 = [au_at((1750, -100)), au_at((2300, -100)), au_at((2900, -100))]
    report(None not in c3 and len(set(c3)) == 3, f"C8 T11 Au: x=1750, 2300, 2900 are three different conductors {c3}")
    centres40 = [centre(p) for p in L.get(40, [])]
    has = [any(abs(cx - xv) < 0.5 and abs(cy + 100) < 0.5 for cx, cy in centres40) for xv in (1900, 2150, 2500, 2750)]
    report(all(has), f"C8 T11 layer-40 openings centred at x=1900, 2150, 2500, 2750 (y=-100): {has}")

    d1, d2 = au_at((-1550, -45)), au_at((1050, -45))
    report(d1 is not None and d1 == d2, f"C8 T12 upper lead: (-1550,-45) and (1050,-45) one conductor ({d1}, {d2})")
    e1, e2 = au_at((-1550, -155)), au_at((1050, -155))
    report(e1 is not None and e1 == e2 and e1 != d1,
           f"C8 T12 lower lead: (-1550,-155) and (1050,-155) one conductor, different from the upper ({e1}, {e2})")
    report(al_at((0, -100)) is not None, "C8 T12 Al strip under (0,-100)")

    f1, f2 = au_at((-2700, 400)), au_at((-2400, 400))
    report(f1 is not None and f2 is not None and f1 != f2,
           f"C8 T2v: Au at (-2700,400) and (-2400,400) are different conductors ({f1}, {f2})")
    g1, g2 = al_at((-2700, 400)), al_at((-2400, 400))
    report(g1 is not None and g1 == g2, f"C8 T2v: Al at (-2700,400) and (-2400,400) is one Al piece ({g1}, {g2})")
    plate_in = f1 is not None and g1 is not None and inside([au[f1]], [L10_m[g1]])
    report(plate_in, "C8 T2v: the Au plate at (-2700,400) lies inside the Al")

# ---------------------------------------------------------------- C9 info
print("-- C9 per-layer summary (info, not pass/fail)")
for n in sorted(L):
    print(f"INFO C9 layer {n:3d}: merged area {area_of(merge(L[n])):12.1f} um^2, polygons {len(L[n]):5d}")

# ---------------------------------------------------------------- TRAP-only rule
if TRAP:
    cnt = {n: len(L.get(n, [])) for n in (10, 20, 22, 40)}
    report(not any(cnt.values()), f"TRAP layers 10, 20, 22, 40 empty (polygon counts {cnt})")

print("ALL CHECKS PASS" if N_FAIL == 0 else f"{N_FAIL} CHECK(S) FAILED")
sys.exit(0 if N_FAIL == 0 else 1)
