"""10c - Al mirror thickness and inlaid thermal SiO2 for the v4 local-mirror die (Claude-authored; follows 10b).

Same 2-D electrostatics and solver as 10b (copied, not imported: 10b runs its study at import). Each case changes
three layer thicknesses of the v4 stack: the SiO2 cap over the NbN (t_cap), the Al local mirror (t_al) and the
thermal SiO2 under the Al (t_d1). The script has two inlaid cases: 0.45 um Al over 0.55 um of thermal SiO2, and
0.10 um Al over 0.90 um of thermal SiO2. Each puts the HR Si 1.0 um below the SiO2 spacer everywhere. For each case and Au option (E2 6 um, E1 0.35 um) it runs
the window cut (wire pickup, wire-to-mirror capacitance) and the slot cut (RF-to-mirror capacitance per um,
lead-to-mirror capacitance per um). From the slot capacitance it then estimates the RF swing on the Al strip
(V_m, 10b's formula), the strip current, its dissipation, the extra nanowire current, the lead common mode from the
mirror swing, and a small-patch micromotion amplitude for two window areas.

Case al100_cap110 is the slot cross-section of the final stack (decided 2026-11-12): a raised 100 nm Al mirror on
1.0 um of base SiO2, with only the 110 nm blanket PECVD SiO2 cap (plus the 238 nm spacer) between the Au leads and the
Al, because HSQ stays on the NbN wires only. Use its mirror current, mirror swing, strip dissipation, lead currents and
lead-to-mirror capacitance. Its direct nanowire current is NOT representative: over the wires the SiO2 is 160 nm, so
use the al100 row for that.

Limits: 2-D model; ideal conductors; omega V C is an upper bound on induced current; room-temperature Al resistivity
(3 and 4 uOhm cm); no thermal model; micromotion is a small-patch estimate (uniform field over one window area),
not a trap-wide value.
Outputs: sim/out/10c_mirror_thickness/summary.json (nested by case, then Au option) and table.md.
Run:     ./run.sh 10c_mirror_thickness.py
"""

import json
import os
import sys
import time
from math import pi

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "10c_mirror_thickness")
REF_JSON = os.path.join(HERE, "out", "10b_rf_pickup_v4", "summary.json")
os.makedirs(OUT, exist_ok=True)

EPS0 = 8.8541878128e-12
V_RF, F_RF = 53.0, 28e6
OMEGA = 2 * np.pi * F_RF
EPS_OX, EPS_SI = 3.9, 11.7                     # SiO2, HR Si
L_DET = 30.0                                   # um, as in 10
X_WIN, X_C, X_RF0, X_RF1, X_OUT, X_MAX = 15.0, 20.0, 25.0, 109.0, 114.0, 400.0
X_SLOT, X_LEAD0, X_LEAD1 = 12.5, 2.5, 7.5      # slot cut: centre-DC halves from 12.5, Au leads 2.5..7.5
X_MIR = 20.0                                   # Al local mirror, |x| <= 20 um
Z_TOP, Z_BACK = 400.0, -516.0
T_NBN, T_SP = 0.007, 0.238                     # NbN and SiO2 spacer, um
WIRE_W, WIRE_P, X_NW = 0.130, 0.200, 16.0
L_STRIP, L_TAIL, W_STRIP = 2240.0, 140.0, 40.0  # um (strip between the RF rails, rail end to via, strip width)

RHO = (3e-8, 4e-8)                             # Ohm m: room-temperature Al, 3 and 4 uOhm cm
RS_CHECK = 0.27                                # Ohm/sq, 10b's 150 nm check value
T10_PER_RS = 62.75                             # Ohm per (Ohm/sq), T10 resistance factor from the brief
AU_OPTIONS = (("E2", 6.0), ("E1", 0.35))       # Au thickness, um
# name, t_cap (SiO2 cap over the NbN), t_al (Al mirror), t_d1 (thermal SiO2 under Al); all um
CASES = (
    ("reference", 0.080, 0.150, 1.0),
    ("al50", 0.160, 0.050, 1.0),
    ("al100", 0.160, 0.100, 1.0),
    ("al150", 0.160, 0.150, 1.0),
    ("al450", 0.160, 0.450, 1.0),
    ("al450_inlaid", 0.160, 0.450, 0.55),
    ("al100_inlaid", 0.160, 0.100, 0.90),
    # slot cross-section of the final stack (2026-11-12): raised 100 nm Al on 1.0 um base SiO2, 110 nm cap only
    # (HSQ on the NbN wires only). Not representative for the nanowire current; see the docstring.
    ("al100_cap110", 0.110, 0.100, 1.0),
)

H_ION = 50e-6                                  # ion height, m
A30 = 30e-6 * 30e-6                            # window area, m^2
B60 = 60e-6 * 30e-6
E_CHARGE = 1.602176634e-19                     # C
M_ION = 138 * 1.66053906660e-27                # kg, 138Ba+


# ------------------------------------------------------------------ grid helpers (copied from 10b)
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


# ------------------------------------------------------------------ v4 geometry (build changed: thicknesses are arguments)
def build(cut, t_au, t_cap, t_al, t_d1):
    z_cap = -t_au
    z_nw_top, z_nw_bot = z_cap - t_cap, z_cap - t_cap - T_NBN
    z_al_top = z_nw_bot - T_SP
    z_al_bot = z_al_top - t_al
    z_d1_bot = z_al_bot - t_d1
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
    eps[ZC < z_cap] = EPS_OX                    # SiO2 cap, spacer, thermal SiO2 (Al cells are fixed or unused)
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


def run(cut, t_au, t_cap, t_al, t_d1):
    xs, zs, eps, cond = build(cut, t_au, t_cap, t_al, t_d1)
    K = laplacian(xs, zs, eps)
    fixed = np.zeros((len(xs), len(zs)), bool)
    for m in cond.values():
        fixed |= m
    v_rf = np.where(cond["rf"], 1.0, 0.0)
    v_mir = np.where(cond["mirror"], 1.0, 0.0)
    phi_rf, phi_m = solve(K, fixed, [v_rf, v_mir])
    r = dict(cut=cut, t_au=t_au, t_cap=t_cap, t_al=t_al, t_d1=t_d1)
    # both halves (x2), per um of length along the trap axis
    r["C_rf_mirror_fF_per_um"] = -2 * charge(K, phi_rf, cond["mirror"]) * 1e15 * 1e-6
    if cut == "window":
        r["C_RN_fF"] = -2 * charge(K, phi_rf, cond["wires"]) * 1e15 * 1e-6 * L_DET
        r["I_pk_uA"] = OMEGA * V_RF * r["C_RN_fF"] * 1e-15 * 1e6
        r["C_wires_mirror_fF"] = -2 * charge(K, phi_m, cond["wires"]) * 1e15 * 1e-6 * L_DET
    else:
        r["C_rf_lead_fF_per_um"] = -charge(K, phi_rf, cond["lead"]) * 1e15 * 1e-6      # one lead (half domain)
        r["I_lead_uA_per_mm"] = OMEGA * V_RF * r["C_rf_lead_fF_per_um"] * 1e-15 * 1e3 * 1e6
        r["I_lead_in_trap_uA"] = r["I_lead_uA_per_mm"] * L_STRIP / 1e3
        # common-mode coupling of one lead to the Al mirror, with the mirror at 1 V
        r["C_lead_mirror_fF_per_um"] = -charge(K, phi_m, cond["lead"]) * 1e15 * 1e-6
    return r


# ------------------------------------------------------------------ derived quantities
def micromotion_nm(v_m, area):
    """Small-patch estimate: uniform field E = V_m * area / (pi h^3) over one window, amplitude e E / (m omega^2)."""
    e_field = v_m * area / (pi * H_ION ** 3)                     # V/m
    return E_CHARGE * e_field / (M_ION * OMEGA ** 2) * 1e9       # nm


def derived(win, slot, t_al, rho):
    t = t_al * 1e-6                                              # m
    rs = rho / t                                                 # Ohm/sq
    rp = rs / (W_STRIP * 1e-6)                                   # Ohm/m
    cp = slot["C_rf_mirror_fF_per_um"] * 1e-15 / 1e-6            # F/m
    clm = slot["C_lead_mirror_fF_per_um"] * 1e-15 / 1e-6         # F/m
    cw = win["C_wires_mirror_fF"] * 1e-15                        # F
    L = L_STRIP * 1e-6
    L2 = L_TAIL * 1e-6
    i_m = OMEGA * V_RF * cp * L                                  # A, current the strip carries to ground
    v_m = OMEGA * V_RF * cp * rp * (L ** 2 / 2 + L * L2)         # V, swing at the detector end (10b)
    i_w = OMEGA * v_m * cw                                       # A, extra nanowire current bound
    p = 0.5 * rp * i_m ** 2 * (L / 3 + L2)                       # W, time-averaged dissipation in the Al strip
    i_l = OMEGA * clm * OMEGA * V_RF * cp * rp * (L ** 3 / 3 + L ** 2 * L2)   # A, common-mode current per lead
    return dict(
        rs_ohm_sq=rs, rp_ohm_per_m=rp, t10_ohm=T10_PER_RS * rs,
        i_mirror_mA=i_m * 1e3, v_m_mV=v_m * 1e3, i_wire_upper_uA=i_w * 1e6,
        p_uW=p * 1e6, i_lead_mirror_uA=i_l * 1e6,
        micromotion_A30_nm=micromotion_nm(v_m, A30), micromotion_B60_nm=micromotion_nm(v_m, B60),
    )


def pair(vals, fmt):
    return f"{vals[0]:{fmt}}–{vals[1]:{fmt}}"


def main():
    t_all = time.time()
    with open(REF_JSON) as fh:
        ref = json.load(fh)
    summary = {}
    raw = {}
    solve_s = []
    for name, t_cap, t_al, t_d1 in CASES:
        entry = dict(t_cap_um=t_cap, t_al_um=t_al, t_d1_um=t_d1,
                     step_nm=0.0 if name.endswith("inlaid") else t_al * 1e3)
        for au, t_au in AU_OPTIONS:
            t0 = time.time()
            win = run("window", t_au, t_cap, t_al, t_d1)
            t1 = time.time()
            slot = run("slot", t_au, t_cap, t_al, t_d1)
            t2 = time.time()
            solve_s.append((name, au, t1 - t0, t2 - t1))
            raw[(name, au)] = (win, slot)
            au_entry = dict(t_au_um=t_au, window=win, slot=slot, rho={})
            for rho in RHO:
                d = derived(win, slot, t_al, rho)
                au_entry["rho"][f"{rho:.0e}"] = d
                print(f"{au} {name:<13s} rho {rho:.0e}: step {entry['step_nm']:.0f} nm, R_s {d['rs_ohm_sq']:.3f} Ohm/sq, "
                      f"T10 {d['t10_ohm']:.1f} Ohm, I_mirror {d['i_mirror_mA']:.3f} mA, V_m {d['v_m_mV']:.2f} mV, "
                      f"I_wire <= {d['i_wire_upper_uA']:.3f} uA (direct I_pk {win['I_pk_uA']:.3f} uA), "
                      f"P {d['p_uW']:.2f} uW, I_lead from mirror {d['i_lead_mirror_uA']:.3g} uA "
                      f"(direct I_lead {slot['I_lead_in_trap_uA']:.3g} uA), "
                      f"micromotion A30 {d['micromotion_A30_nm']:.2f} nm, B60 {d['micromotion_B60_nm']:.2f} nm")
            entry[au] = au_entry
        summary[name] = entry
    print(f"solve times (window, slot) s: " + ", ".join(f"{n}/{a} {w:.1f}, {s:.1f}" for n, a, w, s in solve_s))

    # ---------------- acceptance checks
    checks = []

    def check(label, got, want, tol):
        rel = abs(got - want) / abs(want)
        ok = rel < tol
        checks.append(ok)
        print(f"{'PASS' if ok else 'FAIL'}  {label}: got {got:.6g}, expected {want:.6g} (rel diff {rel:.2%}, tol {tol:.1%})")

    ref_win, ref_slot = raw[("reference", "E2")]
    r_b, r_s, r_m = ref["E2_window"], ref["E2_slot"], ref["E2_mirror_path_150nm_Rs0.27"]
    check("A  E2 window C_RN_fF", ref_win["C_RN_fF"], r_b["C_RN_fF"], 0.005)
    check("A  E2 window I_pk_uA", ref_win["I_pk_uA"], r_b["I_pk_uA"], 0.005)
    check("A  E2 slot C_rf_mirror_fF_per_um", ref_slot["C_rf_mirror_fF_per_um"], r_s["C_rf_mirror_fF_per_um"], 0.005)
    check("A  E2 window C_wires_mirror_fF", ref_win["C_wires_mirror_fF"], r_b["C_wires_mirror_fF"], 0.005)
    rp27 = RS_CHECK / (W_STRIP * 1e-6)
    cp_ref = ref_slot["C_rf_mirror_fF_per_um"] * 1e-15 / 1e-6
    L, L2 = L_STRIP * 1e-6, L_TAIL * 1e-6
    v27 = OMEGA * V_RF * cp_ref * rp27 * (L ** 2 / 2 + L * L2)
    i27 = OMEGA * v27 * ref_win["C_wires_mirror_fF"] * 1e-15
    check("A  E2 reference V_m at R_s 0.27 (mV)", v27 * 1e3, r_m["V_mirror_mV"], 0.005)
    check("A  E2 reference I_wire at R_s 0.27 (uA)", i27 * 1e6, r_m["I_extra_uA"], 0.005)

    al450 = summary["al450"]["E2"]["rho"]
    al50 = summary["al50"]["E2"]["rho"]
    check("B  E2 al450 I_mirror (mA)", al450["3e-08"]["i_mirror_mA"], 3.15, 0.10)
    check("B  E2 al450 rho 4e-8 P (uW)", al450["4e-08"]["p_uW"], 9.8, 0.10)
    check("B  E2 al50 rho 4e-8 P (uW)", al50["4e-08"]["p_uW"], 88.0, 0.10)
    check("B  micromotion formula, V_m 0.080 V, A30 (nm)", micromotion_nm(0.080, A30), 4.1, 0.10)
    n_fail = checks.count(False)
    print(f"ACCEPTANCE: {len(checks) - n_fail} of {len(checks)} PASS")

    # ---------------- outputs
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)

    lines = ["> **Claude-authored.** Written by sim/10c_mirror_thickness.py.", ""]
    for au, t_au in AU_OPTIONS:
        lines += [f"## {au} (Au {t_au} µm)", "",
                  "| case | step (nm) | R_s (Ohm/sq) | T10 (Ohm) | I_mirror (mA) | V_m (mV) | I_wire upper bound (µA) "
                  "| direct I_pk (µA) | P (µW) | I_lead from mirror (µA) | direct I_lead (µA) "
                  "| micromotion A30 (nm) | micromotion B60 (nm) |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for name, _, _, _ in CASES:
            e = summary[name][au]
            d = [e["rho"][f"{rho:.0e}"] for rho in RHO]
            col = lambda k: [x[k] for x in d]
            lines.append("| " + " | ".join([
                name,
                f"{summary[name]['step_nm']:.0f}",
                pair(col("rs_ohm_sq"), ".3f"),
                pair(col("t10_ohm"), ".1f"),
                f"{d[0]['i_mirror_mA']:.3f}",
                pair(col("v_m_mV"), ".2f"),
                pair(col("i_wire_upper_uA"), ".3f"),
                f"{e['window']['I_pk_uA']:.3f}",
                pair(col("p_uW"), ".2f"),
                pair(col("i_lead_mirror_uA"), ".3g"),
                f"{e['slot']['I_lead_in_trap_uA']:.3g}",
                pair(col("micromotion_A30_nm"), ".2f"),
                pair(col("micromotion_B60_nm"), ".2f"),
            ]) + " |")
        lines.append("")
    lines.append("Limits: 2-D model, ideal conductors, omega V C upper bounds, room-temperature Al resistivity, "
                 "no thermal model; micromotion is a small-patch estimate.")
    with open(os.path.join(OUT, "table.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"whole run {time.time() - t_all:.1f} s")
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
