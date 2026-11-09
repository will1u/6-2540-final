"""10b - RF pickup for the v4 local-mirror die: 2-D electrostatics (Claude-authored; DESIGN_LOG step 26).

Same physics and solver as 10_rf_pickup_2d.py (quasi-static, finite volumes, RF rails at 1 V, every other
conductor at 0 V; I = omega V_RF C as an upper bound on the peak induced current). The grid helpers,
Laplacian, solver and charge function are copied from 10 (10 runs its whole study at import).

v4 stack (z = 0 at the Au top): Au electrodes z in [-T_AU, 0] (E2: 6 um, E1: 0.35 um); vacuum above the
Au and in the gaps and window down to the cap; SiO2 cap 80 nm / NbN 7 nm / SiO2 spacer 238 nm / Al 150 nm
only for |x| <= 20 um (the local mirror, grounded) / thermal SiO2 1 um / high-resistivity Si (eps 11.7,
insulating at the 4-6 K detector temperature) with the chip back side grounded 500 um down. No ground
plane under the RF rails.

Two cross-sections perpendicular to the trap axis:
  window  through the readout zone: centre-DC rim 15..20 um, 30 um window, v3.1 wires (130 nm on a 200 nm
          pitch) out to |x| = 16 um. Gives C_RN (wires held at 0 V) and C between the wires and the
          mirror (mirror at 1 V, everything else 0 V).
  slot    through the lead slot (x < 235 um in GDS): centre-DC halves 12.5..20, Au leads 2.5..7.5 (held at
          0 V), no wires. Gives C from the RF rails to each lead and to the mirror strip, per unit length.

Reference: the v3.1 baseline (10 um D2 over a die-wide Al plane) gives C_RN 0.18 fF, I_pk 1.67 uA for the
130 nm / 16 um meander (10, summary_v31_scan.json, key W130_x16_dc0, same detector length 30 um).

Mirror ground path: the strip is grounded by one via ~2.75 mm away (DESIGN_LOG step 25). The RF charge the
rails induce on the strip flows along it to the via, so the detector end sits at
    V_m = omega V_RF C'_rf-mirror R' (L^2/2 + L L2)
with L = 2240 um of strip between the RF rails, L2 = 140 um from the rail ends to the via (step 28), and
R' = R_s / 40 um. The wires then pick up an extra omega V_m C_wires-mirror.

Limitations: 2-D (no window ends, no lead tips, no slot end); ideal conductors; omega V C is an upper bound.
Outputs: sim/out/10b_rf_pickup_v4/summary.json
Run:     ./run.sh 10b_rf_pickup_v4.py
"""

import json
import os

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "10b_rf_pickup_v4")
os.makedirs(OUT, exist_ok=True)

EPS0 = 8.8541878128e-12
V_RF, F_RF = 53.0, 28e6
OMEGA = 2 * np.pi * F_RF
EPS_OX, EPS_SI = 3.9, 11.7
L_DET = 30.0                                   # um, as in 10 (comparison with the v3.1 scan)
X_WIN, X_C, X_RF0, X_RF1, X_OUT, X_MAX = 15.0, 20.0, 25.0, 109.0, 114.0, 400.0
X_SLOT, X_LEAD0, X_LEAD1 = 12.5, 2.5, 7.5      # slot cut: centre-DC halves from 12.5, leads 2.5..7.5
X_MIR = 20.0
Z_TOP, Z_BACK = 400.0, -516.0
T_CAP, T_NBN, T_SP, T_AL, T_D1 = 0.080, 0.007, 0.238, 0.150, 1.0
WIRE_W, WIRE_P, X_NW = 0.130, 0.200, 16.0
# step 28: readout at x = 240 (480 um zones) and the via at x = -2140, so 2240 um of strip between the RF rails and
# 140 um from the rail ends to the via (step 26 used 2300 / 450)
L_STRIP, L_TAIL, W_STRIP = 2240.0, 140.0, 40.0
# Ohm/sq for Al-1%Cu at 3-4 uOhm cm [team calc]: 150 nm (as drawn) and 450 nm (proposed, step 28)
RS_AL = {"150nm": (0.20, 0.27), "450nm": (0.067, 0.089)}


# ------------------------------------------------------------------ grid helpers (copied from 10)
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
    lu = spla.splu(K[free][:, free].tocsc())
    Kfc = K[free][:, f]
    out = []
    for vals in values_list:
        phi = vals.ravel().astype(float).copy()
        phi[free] = lu.solve(-Kfc @ phi[f])
        out.append(phi)
    return out


def charge(K, phi, mask):
    """Charge per unit length (C/m) on the nodes in mask, half domain x >= 0."""
    return EPS0 * float((K @ phi)[mask.ravel()].sum())


# ------------------------------------------------------------------ v4 geometry
def build(cut, t_au):
    z_cap = -t_au
    z_nw_top, z_nw_bot = z_cap - T_CAP, z_cap - T_CAP - T_NBN
    z_al_top = z_nw_bot - T_SP
    z_al_bot = z_al_top - T_AL
    z_d1_bot = z_al_bot - T_D1
    h_fine, x_fine = (0.005, 17.5) if cut == "window" else (0.05, 19.0)
    xs = axis([(0.0, h_fine), (x_fine, h_fine), (X_C, 0.1), (X_RF0, 0.1), (45.0, 1.0), (100.0, 1.0),
               (X_RF1, 0.2), (X_OUT, 0.2), (150.0, 2.0), (X_MAX, 25.0)])
    top = [(z_cap, 0.01), (z_cap + 0.06, 0.02), (-t_au / 2, 0.3), (0.0, 0.1)] if t_au > 1 else [(z_cap, 0.01), (0.0, 0.02)]
    zs = axis([(Z_BACK, 40.0), (-30.0, 2.0), (z_d1_bot, 0.1), (z_al_bot, 0.02), (z_al_top, 0.01),
               (z_nw_bot, T_NBN / 2), (z_nw_top, T_NBN / 2)] + top + [(20.0, 1.0), (Z_TOP, 25.0)])
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    xc, zc = 0.5 * (xs[1:] + xs[:-1]), 0.5 * (zs[1:] + zs[:-1])
    XC, ZC = np.meshgrid(xc, zc, indexing="ij")
    tol = 1e-9

    def box(x0, x1, z0, z1):
        return (X >= x0 - tol) & (X <= x1 + tol) & (Z >= z0 - tol) & (Z <= z1 + tol)

    eps = np.ones_like(XC)                      # vacuum above the cap (gaps, window)
    eps[ZC < z_cap] = EPS_OX                    # cap, spacer, thermal SiO2 (Al cells unused)
    eps[ZC < z_d1_bot] = EPS_SI                 # HR Si
    cond = dict(rf=box(X_RF0, X_RF1, z_cap, 0.0), dc=box(X_OUT, X_MAX, z_cap, 0.0),
                mirror=box(0.0, X_MIR, z_al_bot, z_al_top),
                gnd=(Z <= Z_BACK + tol) | (Z >= Z_TOP - tol) | (X >= X_MAX - tol))
    if cut == "window":
        cond["dcc"] = box(X_WIN, X_C, z_cap, 0.0)
        w = np.zeros_like(X, bool)
        for k in range(int(round(X_NW / WIRE_P))):
            x0 = k * WIRE_P + (WIRE_P - WIRE_W) / 2
            w |= box(x0, x0 + WIRE_W, z_nw_bot, z_nw_top)
        cond["wires"] = w
    else:
        cond["dcc"] = box(X_SLOT, X_C, z_cap, 0.0)
        cond["lead"] = box(X_LEAD0, X_LEAD1, z_cap, 0.0)
    return xs, zs, eps, cond


def run(cut, t_au):
    xs, zs, eps, cond = build(cut, t_au)
    K = laplacian(xs, zs, eps)
    fixed = np.zeros((len(xs), len(zs)), bool)
    for m in cond.values():
        fixed |= m
    v_rf = np.where(cond["rf"], 1.0, 0.0)
    v_mir = np.where(cond["mirror"], 1.0, 0.0)
    phi_rf, phi_m = solve(K, fixed, [v_rf, v_mir])
    r = dict(cut=cut, t_au=t_au)
    # both halves (x2), per um of length along the trap axis
    r["C_rf_mirror_fF_per_um"] = -2 * charge(K, phi_rf, cond["mirror"]) * 1e15 * 1e-6
    r["C_rf_per_rail_pF_per_mm"] = charge(K, phi_rf, cond["rf"]) * 1e12 * 1e-3
    if cut == "window":
        r["C_RN_fF"] = -2 * charge(K, phi_rf, cond["wires"]) * 1e15 * 1e-6 * L_DET
        r["I_pk_uA"] = OMEGA * V_RF * r["C_RN_fF"] * 1e-15 * 1e6
        r["C_wires_mirror_fF"] = -2 * charge(K, phi_m, cond["wires"]) * 1e15 * 1e-6 * L_DET
    else:
        r["C_rf_lead_fF_per_um"] = -charge(K, phi_rf, cond["lead"]) * 1e15 * 1e-6      # one lead (half domain)
        r["I_lead_uA_per_mm"] = OMEGA * V_RF * r["C_rf_lead_fF_per_um"] * 1e-15 * 1e3 * 1e6
        r["I_lead_in_trap_uA"] = r["I_lead_uA_per_mm"] * L_STRIP / 1e3
    return r


v31 = json.load(open(os.path.join(os.path.dirname(OUT), "10_rf_pickup_2d", "summary_v31_scan.json")))["runs"]["W130_x16_dc0"]
res = dict(reference_v31_baseline=dict(C_RN_fF=v31["C_RN_fF"], I_pk_uA=v31["I_pk_uA"]))
for t_au, name in ((6.0, "E2"), (0.35, "E1")):
    for cut in ("window", "slot"):
        r = run(cut, t_au)
        res[f"{name}_{cut}"] = r
        print(f"{name} {cut:6s}: " + ", ".join(f"{k} {v:.4g}" for k, v in r.items() if isinstance(v, float) and k != "t_au"))
    # mirror ground path: voltage at the detector end and the extra wire current it drives
    cp = res[f"{name}_slot"]["C_rf_mirror_fF_per_um"] * 1e-15 / 1e-6          # F/m
    for t_al, rss in RS_AL.items():
        for rs in rss:
            rp = rs / (W_STRIP * 1e-6)                                        # Ohm/m
            vm = OMEGA * V_RF * cp * rp * ((L_STRIP * 1e-6) ** 2 / 2 + L_STRIP * L_TAIL * 1e-12)
            i_extra = OMEGA * vm * res[f"{name}_window"]["C_wires_mirror_fF"] * 1e-15 * 1e6
            res[f"{name}_mirror_path_{t_al}_Rs{rs}"] = dict(V_mirror_mV=vm * 1e3, I_extra_uA=i_extra)
            print(f"{name} mirror path, Al {t_al}, Rs {rs} Ohm/sq: V at the detector end {vm * 1e3:.3g} mV, "
                  f"extra wire current <= {i_extra:.3g} uA")
print(f"reference v3.1 baseline: C_RN {v31['C_RN_fF']:.4g} fF, I_pk {v31['I_pk_uA']:.3g} uA")
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(res, fh, indent=1)
