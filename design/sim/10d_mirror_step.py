"""10d - RF null shift from a step or a sideways misalignment of the local Al mirror (Claude-authored; follows 10c).

Same 2-D electrostatic solver as 10c (finite-volume Laplace on a graded grid, copied, not imported). The cross-section
is the full domain in x (both signs) through the lead slot. The local Al mirror under the centre DC is either inlaid in
the thermal SiO2 (100 nm Al, no step) or raised on the SiO2 by s (100 nm or 450 nm). The SiO2 spacer and cap and the
Au electrodes above the mirror rise by s. The mirror can also be shifted sideways by d. For each case the script solves
the RF potential (1 V on the RF rails, every other conductor at 0 V), finds the RF null from the local field gradient,
and reports how far the null moves against the inlaid, centred reference, and the micromotion that shift would give if
the DC fields were not re-tuned.

Model: the null position is found from a linear fit of the field over a 1 um x 2 um box around the field minimum. The
pseudopotential gradient G gives the Mathieu q. Materials: Au electrodes, Al mirror, SiO2 (spacer, cap and thermal) and
high-resistivity Si, with vacuum above the surface.
Limits: 2-D cross-section through the lead slot (no window, no mirror end); ideal conductors; SiO2 drawn with vertical
steps; leads and DC electrodes at RF ground; static fields (no DC re-tuning); micromotion uses the local linear field.
Outputs: out/10d_mirror_step/summary.json and table.md.
Run:     ./run.sh 10d_mirror_step.py
"""

import json
import os
import sys
import time
from math import sqrt

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "10d_mirror_step")
os.makedirs(OUT, exist_ok=True)

EPS0 = 8.8541878128e-12
V_RF, F_RF = 53.0, 28e6
OMEGA = 2 * np.pi * F_RF
EPS_OX, EPS_SI = 3.9, 11.7                     # SiO2, HR Si
X_MAX, Z_TOP, Z_BACK = 400.0, 400.0, -516.0
T_STACK = 0.40                                 # SiO2 spacer + cap between the Al top and the surface, um
T_D1 = 1.0                                     # thermal SiO2 under the Al, um
INLAID_AL = 0.10                               # inlaid Al thickness (100 nm Al let into the thermal SiO2), um
MIRROR_HALF = 20.0                             # Al mirror |x - d| <= 20 um
E_CHARGE = 1.602176634e-19                     # C
M_ION = 138 * 1.66053906660e-27                # kg, 138Ba+
AU_OPTIONS = (("E2", 6.0), ("E1", 0.35))       # Au thickness, um
S_CASES = (0.0, 0.10, 0.45)                    # step of the Al mirror top, um
D_CASES = (0.0, 2.0, 5.0)                      # sideways misalignment of the mirror, um
LABEL = {0.0: "inlaid", 0.10: "raised 100 nm", 0.45: "raised 450 nm"}
RF_RAILS = [(25.0, 109.0)]                     # Au, um (mirrored to negative x)
DC_OUTER = [(114.0, 400.0)]
DC_CENTRE = [(12.5, 20.0)]
LEADS = [(2.5, 7.5)]

POS_KNOTS = [(0.0, 0.1), (30.0, 0.1), (45.0, 1.0), (100.0, 1.0), (109.0, 0.2), (114.0, 0.2),
             (150.0, 2.0), (400.0, 25.0)]       # x, positive half (mirrored below); lighter grid
Z_KNOTS = [(-516.0, 40.0), (-30.0, 2.0), (-1.5, 0.05), (-0.6, 0.01), (0.9, 0.01), (1.5, 0.05), (7.0, 0.05),
           (10.0, 0.5), (70.0, 0.5), (400.0, 25.0)]
X_MUST = [2.5, 7.5, 12.5, 15.0, 18.0, 20.0, 22.0, 25.0, 109.0, 114.0]   # each also negative
# z = -1.4 (thermal SiO2 bottom) is not a node on this grid; materials are assigned per cell centre
Z_MUST = [-0.5, -0.4, -0.3, 0.0, 0.1, 0.35, 0.45, 0.8, 6.0, 6.1, 6.45]


# ------------------------------------------------------------------ solver (copied from 10c, unchanged)
def graded(a, b, ha, hb):
    if ha == hb:
        return np.linspace(a, b, int(round((b - a) / ha)) + 1)
    pts, x = [a], a
    while x < b - 1e-12:
        x += ha + (hb - ha) * (x - a) / (b - a)
        pts.append(x)
    pts = np.array(pts)
    return a + (pts - a) * (b - a) / (pts[-1] - a)


def axis(knots):
    parts = [graded(p0, p1, h0, h1)[:-1] for (p0, h0), (p1, h1) in zip(knots[:-1], knots[1:])]
    return np.concatenate(parts + [np.array([knots[-1][0]])])


def laplacian(xs, zs, eps):
    nx, nz = len(xs), len(zs)
    dx, dz = np.diff(xs), np.diff(zs)
    idx = np.arange(nx * nz).reshape(nx, nz)
    A = eps * dz[None, :] / 2
    wx = np.zeros((nx - 1, nz))
    wx[:, 1:] += A
    wx[:, :-1] += A
    wx /= dx[:, None]
    B = eps * dx[:, None] / 2
    wz = np.zeros((nx, nz - 1))
    wz[1:, :] += B
    wz[:-1, :] += B
    wz /= dz[None, :]
    p = np.concatenate([idx[:-1, :].ravel(), idx[:, :-1].ravel()])
    q = np.concatenate([idx[1:, :].ravel(), idx[:, 1:].ravel()])
    w = np.concatenate([wx.ravel(), wz.ravel()])
    return sp.coo_matrix((np.concatenate([w, w, -w, -w]), (np.concatenate([p, q, p, q]), np.concatenate([p, q, q, p]))),
                         shape=(nx * nz, nx * nz)).tocsr()


def solve(K, fixed, values_list):
    f = fixed.ravel()
    free = ~f
    # MMD_AT_PLUS_A: fill-reducing ordering only (speed); the solution is the same
    lu = spla.splu(K[free][:, free].tocsc(), permc_spec="MMD_AT_PLUS_A")
    Kfc = K[free][:, f]
    out = []
    for vals in values_list:
        phi = vals.ravel().astype(float).copy()
        phi[free] = lu.solve(-Kfc @ phi[f])
        out.append(phi)
    return out


# ------------------------------------------------------------------ grid and geometry
def build_grid():
    pos = axis(POS_KNOTS)
    xs = np.concatenate([-pos[::-1][:-1], pos])          # full domain, both signs of x
    zs = axis(Z_KNOTS)
    for v in X_MUST:
        for vv in (v, -v):
            assert np.min(np.abs(xs - vv)) < 1e-9, f"x node {vv} missing"
    for v in Z_MUST:
        assert np.min(np.abs(zs - v)) < 1e-9, f"z node {v} missing"
    return xs, zs


def surf_height(x, s, d):
    """Top of the SiO2 stack: s over the Al mirror (inclusive ends), 0 elsewhere."""
    inside = (x >= -MIRROR_HALF + d - 1e-9) & (x <= MIRROR_HALF + d + 1e-9)
    return np.where(inside, s, 0.0)


def sym(intervals):
    return list(intervals) + [(-b, -a) for a, b in intervals]


def find_null(xs, zs, Ex, Ez):
    """Null from the field minimum in |x| <= 10, 40 <= z <= 62, then a linear fit of E over the box around it."""
    XX, ZZ = np.meshgrid(xs, zs, indexing="ij")
    box = (np.abs(XX) <= 10.0) & (ZZ >= 40.0) & (ZZ <= 62.0)
    e2 = np.where(box, Ex ** 2 + Ez ** 2, np.inf)
    i, j = np.unravel_index(np.argmin(e2), e2.shape)
    xn, zn = xs[i], zs[j]
    fit = (np.abs(XX - xn) <= 0.5 + 1e-9) & (np.abs(ZZ - zn) <= 1.0 + 1e-9)
    dxf, dzf = XX[fit] - xn, ZZ[fit] - zn
    A = np.column_stack([np.ones_like(dxf), dxf, dzf])
    a0, a1, a2 = np.linalg.lstsq(A, Ex[fit], rcond=None)[0]
    b0, b1, b2 = np.linalg.lstsq(A, Ez[fit], rcond=None)[0]
    J = np.array([[a1, a2], [b1, b2]])                  # 1/um^2
    p0 = np.array([xn, zn]) - np.linalg.solve(J, np.array([a0, b0]))
    G = sqrt(abs(np.linalg.det(J)))                     # 1/um^2
    return p0, J, G


def solve_case(xs, zs, t_au, s, d):
    t0 = time.time()
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    xc, zc = 0.5 * (xs[1:] + xs[:-1]), 0.5 * (zs[1:] + zs[:-1])
    XC, ZC = np.meshgrid(xc, zc, indexing="ij")
    tol = 1e-9
    # permittivity per cell: vacuum above the surface, SiO2 up to the surface, HR Si below the thermal SiO2
    eps = np.ones_like(XC)
    eps[(ZC < surf_height(XC, s, d)) & (ZC > -T_STACK - T_D1)] = EPS_OX
    eps[ZC < -T_STACK - T_D1] = EPS_SI
    K = laplacian(xs, zs, eps)
    # Al mirror at 0 V: raised on the SiO2 by s, or inlaid in the thermal SiO2
    if s > 0:
        z_al0, z_al1 = -T_STACK, -T_STACK + s
    else:
        z_al0, z_al1 = -T_STACK - INLAID_AL, -T_STACK
    mirror = ((X >= -MIRROR_HALF + d - tol) & (X <= MIRROR_HALF + d + tol)
              & (Z >= z_al0 - tol) & (Z <= z_al1 + tol))
    # Au electrodes: from the local surface up to surface + t_au (surface evaluated per node)
    surf_n = surf_height(X, s, d)

    def on_surface(intervals, t):
        m = np.zeros(X.shape, bool)
        for a, b in intervals:
            m |= (X >= a - tol) & (X <= b + tol)
        return m & (Z >= surf_n - tol) & (Z <= surf_n + t + tol)

    rf = on_surface(sym(RF_RAILS), t_au)
    dc = on_surface(sym(DC_OUTER) + sym(DC_CENTRE), t_au)
    leads = on_surface(sym(LEADS), t_au)
    gnd = (Z <= Z_BACK + tol) | (Z >= Z_TOP - tol) | (np.abs(X) >= X_MAX - tol)
    fixed = rf | dc | leads | mirror | gnd
    v_rf = np.where(rf, 1.0, 0.0)
    (phi,) = solve(K, fixed, [v_rf])
    phi2 = phi.reshape(len(xs), len(zs))
    gx, gz = np.gradient(phi2, xs, zs)
    p0, J, G = find_null(xs, zs, -gx, -gz)
    G_SI = G * 1e12                                     # 1/m^2
    q = 2 * E_CHARGE * V_RF * G_SI / (M_ION * OMEGA ** 2)
    return dict(x0=float(p0[0]), z0=float(p0[1]), p0=p0, J=J, G_um2=float(G), q=float(q),
                solve_s=time.time() - t0)


def micromotion_nm(J, p_from, p_to):
    """Field per volt at p_to from the linear field of this case (centred at p_from's null), amplitude in nm."""
    E = J @ (p_from - p_to)                             # 1/um per volt
    E_SI = np.linalg.norm(E) * 1e6                      # 1/m per volt
    return E_CHARGE * V_RF * E_SI / (M_ION * OMEGA ** 2) * 1e9


def main():
    t_all = time.time()
    xs, zs = build_grid()
    print(f"grid: {len(xs)} x {len(zs)} = {len(xs) * len(zs)} nodes")
    # --one: time a single solve (E2 or the --au option, inlaid, no misalignment) and stop
    # --au E1|E2: solve only that Au option and save it to out/10d_mirror_step/part_<au>.json
    # Outputs are written only once both part files exist, so the two Au options can run in separate commands.
    args = sys.argv[1:]
    sel = args[args.index("--au") + 1] if "--au" in args else None
    aus = [a for a in AU_OPTIONS if sel is None or a[0] == sel]
    if "--merge" in args:                          # no solves: build outputs from the saved part files
        aus = []
    if "--one" in args:
        au, t_au = aus[0]
        r1 = solve_case(xs, zs, t_au, 0.0, 0.0)
        print(f"one solve {au} inlaid d=0: {r1['solve_s']:.1f} s, grid {len(xs)} x {len(zs)}")
        return
    for au, t_au in aus:
        part = {}
        for s in S_CASES:
            for d in D_CASES:
                r = solve_case(xs, zs, t_au, s, d)
                part[f"{s:.2f}|{d:.1f}"] = dict(x0=r["x0"], z0=r["z0"], p0=r["p0"].tolist(), J=r["J"].tolist(),
                                                G_um2=r["G_um2"], q=r["q"], solve_s=r["solve_s"])
        with open(os.path.join(OUT, f"part_{au}.json"), "w", encoding="utf-8") as fh:
            json.dump(part, fh, indent=1)
        print(f"solved {au}: 9 cases, {sum(v['solve_s'] for v in part.values()):.1f} s")
    res = {}
    for au, t_au in AU_OPTIONS:
        path = os.path.join(OUT, f"part_{au}.json")
        if not os.path.exists(path):
            print(f"partial run: {path} missing; run --au for the other Au option to finish")
            return
        with open(path, encoding="utf-8") as fh:
            part = json.load(fh)
        for s in S_CASES:
            for d in D_CASES:
                v = part[f"{s:.2f}|{d:.1f}"]
                res[(au, s, d)] = dict(x0=v["x0"], z0=v["z0"], p0=np.array(v["p0"]), J=np.array(v["J"]),
                                       G_um2=v["G_um2"], q=v["q"], solve_s=v["solve_s"])
    # ---- derived, relative to the inlaid centred reference of each Au option
    rec = {}
    for au, t_au in AU_OPTIONS:
        ref = res[(au, 0.0, 0.0)]
        for s in S_CASES:
            for d in D_CASES:
                r = res[(au, s, d)]
                st = res[(au, 0.0, d)]
                e = dict(au=au, t_au_um=t_au, s_um=s, d_um=d, label=LABEL[s],
                         x0_um=r["x0"], z0_um=r["z0"], h_um=r["z0"] - (t_au + s),
                         q=r["q"], G_um2=r["G_um2"],
                         f_sec_MHz=r["q"] * F_RF / (2 * sqrt(2)) / 1e6,
                         dx_nm=(r["x0"] - ref["x0"]) * 1e3, dz_nm=(r["z0"] - ref["z0"]) * 1e3,
                         dx_step_nm=(r["x0"] - st["x0"]) * 1e3, dz_step_nm=(r["z0"] - st["z0"]) * 1e3,
                         dq_percent=100 * (r["q"] / ref["q"] - 1),
                         micromotion_nm=micromotion_nm(r["J"], ref["p0"], r["p0"]),
                         J=r["J"].tolist(), solve_s=r["solve_s"])
                rec[(au, s, d)] = e
                print(f"{au} {LABEL[s]:<15s} s={s:.2f} d={d:.1f} x0={e['x0_um']:.4f} um z0={e['z0_um']:.4f} um "
                      f"h={e['h_um']:.2f} um q={e['q']:.4f} f_sec={e['f_sec_MHz']:.3f} MHz "
                      f"dx={e['dx_nm']:.1f} nm dz={e['dz_nm']:.1f} nm dx_step={e['dx_step_nm']:.1f} nm "
                      f"dz_step={e['dz_step_nm']:.1f} nm dq={e['dq_percent']:.2f} % "
                      f"micromotion={e['micromotion_nm']:.1f} nm solve={e['solve_s']:.1f} s")

    # ---------------- acceptance checks
    checks = []

    def check(label, ok, detail):
        checks.append(ok)
        print(f"{'PASS' if ok else 'FAIL'}  {label}: {detail}")

    for (au, s, d), e in rec.items():
        if d == 0.0:
            check(f"A1 {au} {LABEL[s]} d=0 symmetry", abs(e["x0_um"]) < 0.005, f"|x0| = {abs(e['x0_um']):.6f} um (limit 0.005)")
    e1 = rec[("E1", 0.0, 0.0)]
    e2 = rec[("E2", 0.0, 0.0)]
    check("A2 E1 reference q", 0.25 < e1["q"] < 0.35, f"q = {e1['q']:.4f} (0.25 to 0.35)")
    check("A2 E1 reference h", 45 < e1["h_um"] < 53, f"h = {e1['h_um']:.2f} um (45 to 53)")
    check("A3 E2 reference q", 0.22 < e2["q"] < 0.35, f"q = {e2['q']:.4f} (0.22 to 0.35)")
    check("A3 E2 reference h", 43 < e2["h_um"] < 53, f"h = {e2['h_um']:.2f} um (43 to 53)")
    for au, t_au in AU_OPTIONS:
        ratio = rec[(au, 0.45, 0.0)]["dz_nm"] / rec[(au, 0.10, 0.0)]["dz_nm"]
        if t_au > 0.45:
            check(f"A4 {au} linearity dz(450)/dz(100)", 3.8 <= ratio <= 5.2, f"ratio = {ratio:.3f} (3.8 to 5.2)")
        else:
            # a 0.45 um step is taller than the 0.35 um Au, so the raised Au no longer overlaps the rails in height:
            # the shift is not expected to stay linear in the step, and the ratio is printed for information only
            print(f"INFO A4 {au} dz(450)/dz(100) = {ratio:.3f} (not checked: the 450 nm step exceeds the {t_au} um Au)")
    for (au, s, d), e in rec.items():
        r_nm = sqrt(e["dx_nm"] ** 2 + e["dz_nm"] ** 2)
        if r_nm > 5:
            target = e["q"] / 2 * r_nm
            ok = abs(e["micromotion_nm"] - target) <= 0.25 * target
            check(f"A5 {au} {LABEL[s]} d={d:.1f} micromotion vs (q/2) r", ok,
                  f"micromotion {e['micromotion_nm']:.2f} nm, (q/2) r {target:.2f} nm (within 25 %)")
    print(f"INFO dz at s=0.10 d=0: E2 {rec[('E2', 0.10, 0.0)]['dz_nm']:.1f} nm, E1 {rec[('E1', 0.10, 0.0)]['dz_nm']:.1f} nm; "
          f"hand estimate: magnitude about 70 nm (information only)")
    n_fail = checks.count(False)
    print(f"ACCEPTANCE: {len(checks) - n_fail} of {len(checks)} PASS")

    # ---------------- outputs
    summary = dict(grid=dict(nx=len(xs), nz=len(zs)), cases={})
    for (au, s, d), e in rec.items():
        summary["cases"][f"{au}|s={s:.2f}|d={d:.1f}"] = {k: (float(v) if isinstance(v, (float, np.floating)) else v)
                                                       for k, v in e.items()}
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)

    lines = ["> **Claude-authored.** Written by sim/10d_mirror_step.py.", ""]
    for au, t_au in AU_OPTIONS:
        lines += [f"## {au} (Au {t_au} µm)", "",
                  "| mirror | misalignment d (µm) | null shift sideways dx (nm) | null shift in height dz (nm) "
                  "| of which from the step: dx_step / dz_step (nm) | change in q (%) "
                  "| micromotion if nothing is re-tuned (nm) |",
                  "|---|---|---|---|---|---|---|"]
        for s in S_CASES:
            for d in D_CASES:
                e = rec[(au, s, d)]
                lines.append(f"| {LABEL[s]} | {d:.1f} | {e['dx_nm']:.1f} | {e['dz_nm']:.1f} "
                             f"| {e['dx_step_nm']:.1f} / {e['dz_step_nm']:.1f} | {e['dq_percent']:.2f} "
                             f"| {e['micromotion_nm']:.1f} |")
        lines.append("")
    lines.append("Reference: inlaid mirror, no misalignment. Limits: 2-D cross-section through the lead slot "
                 "(no window, no mirror end), ideal conductors, SiO2 drawn with vertical steps, leads and DC "
                 "electrodes at RF ground.")
    with open(os.path.join(OUT, "table.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"whole run {time.time() - t_all:.1f} s")
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
