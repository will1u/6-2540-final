"""23 - RF coupling onto the DC electrodes, and what a filter capacitor does about it (Claude-authored; follows 10c).

Question: 53 V at 28 MHz on the RF rails couples into each DC electrode through a rail-to-electrode capacitance.
How much RF voltage is left on each DC electrode for a filter capacitor C_f to ground, and how far does that
move the RF null (gds2itvg, as sim 12)?

Model
  Part A  2-D electrostatics of the v4 stack (solver copied from 10c, not imported). Two cross-sections:
          'slot'  = lead, centre-DC half (12.5-20 um), rail (25-109), outer DC (114 um to the edge), Al mirror
                    (0-20 um, 100 nm, inlaid), grounded box;
          'plain' = centre DC solid (0-20 um), rail, outer DC, box (no lead, no mirror).
          Stack: SiO2 cap 0.160 um, spacer 0.238 um, NbN 7 nm, Al 0.100 um inlaid in 0.90 um thermal SiO2
          (10c's al100_inlaid). Au 6.0 um (E2) and 0.35 um (E1). Each conductor is set to 1 V in turn, the others
          at 0 V, and the charge on every conductor (box included) is integrated.
  Part B  Capacitance per electrode [team calc]: centre DC (electrode 2) to the rails and to ground; one outer
          DC segment to the rails; its ground capacitance from the pad estimates in pad_electrical_effects.md.
  Part C  Divider V_el = 53 V * C_c / (C_c + C_g + C_f) and filter current I = omega C_f V_el.
  Part D  RF null shift with gds2itvg (layout ../gds/trap_die_v4_A30_sim.json, as sim 12): d = -(V_el/53) H^-1 g,
          radial (x, z) components only.

Conventions
  The solver works on the half domain x >= 0 with a symmetry (Neumann) plane at x = 0. Q[i, j] (fF/um) is the
  charge per unit length on conductor i, half domain, when conductor j is at 1 V. cap(i, j) = -Q[i, j] for i != j.
  The centre DC, the mirror and the box straddle x = 0: their full-geometry value is 2 x the half-domain value.
  The rails, the leads and an outer DC conductor are one copy each on the x > 0 side, so cap(rail, electrode)
  is the coupling of that one electrode to both rails (both rails are at 1 V in the half-domain solve).

Inputs: design/gds/trap_die_v4_A30_sim.json (and its layer-50 GDS), the pad estimates in
  research/research_notes/Bond pad sizing for ion traps/pad_electrical_effects.md (lines 29-31).
Outputs: out/23_dc_rf_coupling/summary.json and table.md.
Run: ./run.sh 23_dc_rf_coupling.py

Limits: 2-D, no segment ends, no lead tracks crossing near the rails, ideal conductors. The bond wire and
  lead inductance between an electrode and its filter capacitor are ignored [inference]. The pad estimates
  in pad_electrical_effects.md assume 10 um SiO2 over a buried Al plane (not the v4 stack) and do not
  include lateral coupling to neighbours [verify for this stack]. Outer DC lead lengths were not measured
  from the GDS; the 5 mm and 8 mm lead values from that note are used as a bracket [verify].
"""

import json
import os
import time
from math import pi

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from gds2itvg import Layout, build_electrodes
from gds2itvg.analysis import rf_null

import trapcalc as tc      # shared physics helpers (taylor_all, sum_taylor); not a numbered script

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "23_dc_rf_coupling")
os.makedirs(OUT, exist_ok=True)
JS = os.path.join(HERE, "..", "gds", "trap_die_v4_A30_sim.json")

EPS0 = 8.8541878128e-12
EPS_OX, EPS_SI = 3.9, 11.7                       # SiO2, HR Si
V_RF, F_RF = 53.0, 28e6
OMEGA = 2 * pi * F_RF
T_NBN, T_CAP, T_SP, T_AL, T_D1 = 0.007, 0.160, 0.238, 0.100, 0.90   # um, al100_inlaid stack
X_SLOT, X_LEAD0, X_LEAD1, X_C, X_MIR = 12.5, 2.5, 7.5, 20.0, 20.0
X_RF0, X_RF1, X_OUT, X_MAX = 25.0, 109.0, 114.0, 400.0
Z_TOP, Z_BACK = 400.0, -516.0
AU = (("E2", 6.0), ("E1", 0.35))                 # Au thickness, um
L_SLOT, L_PLAIN = 2240.0, 1760.0                 # um, A30: slot section and plain section of the rails
L_NODET = 4000.0                                 # um, NODET die: plain for the whole rail length
L_SEG = 120.0                                    # um, DC segment pitch (design/CLAUDE.md)
L_MIRROR_NOTE = 2730.0                           # um, centre-DC length used in fab/variants/LOCAL_MIRROR.md
# pad_electrical_effects.md, table in section 1, eps_r = 3.9 column (team estimates of that note)
CG_PAD_PF = 0.101                                # line 29: DC pad 120 x 200 um
CG_LEAD5_PF = 0.30                               # line 30: DC lead 6 um x 5 mm
CG_LEAD8_PF = 0.48                               # line 31: DC lead 6 um x 8 mm
CG_SEG5_PF = CG_PAD_PF + CG_LEAD5_PF
CG_SEG8_PF = CG_PAD_PF + CG_LEAD8_PF
C_FILTER_PF = [0.0, 100.0, 1000.0, 10000.0]     # 0, 100 pF, 1 nF, 10 nF
TOP = [str(n) for n in range(3, 18)]            # electrodes 3-17: top segments (left to right)
BOT = [str(n) for n in range(18, 33)]           # electrodes 18-32: bottom segments
GEO_AUDIT_PF = 0.5                               # geometry audit, line 312 (team estimate there)


# ------------------------------------------------------------------ grid helpers (copied from 10c)
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


# ------------------------------------------------------------------ geometry (10c's build, conductors as masks)
def build(section, t_au):
    z_cap = -t_au
    z_nw_top = z_cap - T_CAP
    z_nw_bot = z_nw_top - T_NBN
    z_al_top = z_nw_bot - T_SP
    z_al_bot = z_al_top - T_AL
    z_d1_bot = z_al_bot - T_D1
    xs = axis([(0.0, 0.05), (19.0, 0.05), (X_C, 0.1), (X_RF0, 0.1), (45.0, 1.0), (100.0, 1.0),
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

    eps = np.ones_like(XC)                       # vacuum above the Au top surface
    eps[ZC < z_cap] = EPS_OX                     # SiO2 cap, NbN (as SiO2), spacer, thermal SiO2
    eps[ZC < z_d1_bot] = EPS_SI                  # HR Si
    cond = {}
    cond["rf"] = box(X_RF0, X_RF1, z_cap, 0.0)
    gnd = (Z <= Z_BACK + tol) | (Z >= Z_TOP - tol) | (X >= X_MAX - tol)
    cond["dc"] = box(X_OUT, X_MAX, z_cap, 0.0) & ~gnd     # the x = 400 column is the grounded box, not DC
    if section == "slot":
        cond["lead"] = box(X_LEAD0, X_LEAD1, z_cap, 0.0)
        cond["dcc"] = box(X_SLOT, X_C, z_cap, 0.0)
        cond["mirror"] = box(0.0, X_MIR, z_al_bot, z_al_top)
    else:
        cond["dcc"] = box(0.0, X_C, z_cap, 0.0)
    cond["gnd"] = gnd
    return xs, zs, eps, cond


def matrix(section, t_au):
    """Half-domain charge matrix Q (fF/um): Q[i, j] = charge on conductor i with conductor j at 1 V."""
    xs, zs, eps, cond = build(section, t_au)
    names = list(cond.keys())
    K = laplacian(xs, zs, eps)
    fixed = np.zeros((len(xs), len(zs)), bool)
    for m in cond.values():
        fixed |= m
    vals = [np.where(cond[n], 1.0, 0.0) for n in names]
    phis = solve(K, fixed, vals)
    Q = np.zeros((len(names), len(names)))
    for j, phi in enumerate(phis):
        for i, n in enumerate(names):
            Q[i, j] = charge(K, phi, cond[n]) * 1e9   # C/m -> fF/um (1 F/m = 1e9 fF/um)
    return names, Q


def cap(names, Q, a, b):
    """Half-domain coupling (fF/um) between conductors a and b, a != b (positive)."""
    return -Q[names.index(a), names.index(b)]


def pF(per_um_fF, length_um):
    return per_um_fF * length_um / 1000.0


def divider(c_c_pF, c_g_pF, c_f_pF):
    """V_el = 53 V * C_c / (C_c + C_g + C_f); pF in, V out."""
    return V_RF * c_c_pF / (c_c_pF + c_g_pF + c_f_pF)


def shift_nm(T, H2, names, v_el):
    """Radial (x, z) null shift in nm: d = -(V_el/53) inv(H_rf) g_n, electrodes in names summed (same V_el each)."""
    g = np.zeros(2)
    for n in names:
        g += T[n][1][[0, 2]]
    d_um = -(v_el / V_RF) * np.linalg.solve(H2, g)
    return d_um * 1000.0


def main():
    t_all = time.time()
    mats, pul = {}, {}
    print("Part A: capacitance matrices (half domain, fF/um)")
    for section in ("slot", "plain"):
        for au, t_au in AU:
            t0 = time.time()
            names, Q = matrix(section, t_au)
            mats[(section, au)] = (names, Q)
            c_rf_dcc = cap(names, Q, "dcc", "rf")
            # full-geometry parts of the centre-DC total: x2 because the centre DC straddles x = 0
            parts = {n: 2 * cap(names, Q, n, "dcc") for n in names if n not in ("dcc", "rf")}
            d = dict(
                names=names,
                C_rf_dcc_half=c_rf_dcc,
                C_rf_dc_half=cap(names, Q, "dc", "rf"),
                C_centre_rails_full=2 * c_rf_dcc,
                Cg_parts_full=parts,
                Cg_full=sum(parts.values()) - 0.0,
                diag_dcc_half=Q[names.index("dcc"), names.index("dcc")],
            )
            if section == "slot":
                d["C_rf_lead_half"] = cap(names, Q, "lead", "rf")
                d["C_rf_mirror_full"] = 2 * cap(names, Q, "mirror", "rf")
                d["C_lead_mirror_half"] = cap(names, Q, "lead", "mirror")
            pul[(section, au)] = d
            print(f"  {section:5s} {au}: solve {time.time() - t0:.1f} s; C'(rf->dcc) {c_rf_dcc:.5f}, "
                  f"C'(rf->dc) {d['C_rf_dc_half']:.5f}, C'(rf->lead) {d.get('C_rf_lead_half', float('nan')):.7f}")

    # ---------------- acceptance: 10c reproduction and reciprocity / charge conservation on the matrices
    recip_max, cons_max = 0.0, 0.0
    for key, (names, Q) in mats.items():
        for i, a in enumerate(names):
            for j, b in enumerate(names):
                if i >= j:
                    continue
                c_ab, c_ba = -Q[i, j], -Q[j, i]
                denom = max(abs(c_ab), abs(c_ba))
                if denom > 1e-6:
                    recip_max = max(recip_max, abs(c_ab - c_ba) / denom)
        for j in range(len(names)):
            cons_max = max(cons_max, abs(Q[:, j].sum()) / abs(Q[j, j]))

    # ---------------- Part B: per electrode
    print("Part B: capacitance per electrode")
    el = {}
    for au, _ in AU:
        s_names, s_Q = mats[("slot", au)]
        p_names, p_Q = mats[("plain", au)]
        s, p = pul[("slot", au)], pul[("plain", au)]
        # centre DC, A30: slot section over 2240 um, plain over 1760 um
        c_c_a30 = pF(s["C_centre_rails_full"], L_SLOT) + pF(p["C_centre_rails_full"], L_PLAIN)
        c_g_a30 = pF(s["Cg_full"], L_SLOT) + pF(p["Cg_full"], L_PLAIN)
        mirror_a30 = pF(s["Cg_parts_full"]["mirror"], L_SLOT)
        # centre DC, NODET: plain for the whole 4000 um
        c_c_nodet = pF(p["C_centre_rails_full"], L_NODET)
        c_g_nodet = pF(p["Cg_full"], L_NODET)
        # outer segment: slot-section coupling to the rails over one 120 um segment (A30 die)
        c_c_seg = pF(s["C_rf_dc_half"], L_SEG)
        c_c_seg_plain = pF(p["C_rf_dc_half"], L_SEG)
        el[au] = dict(
            centre_A30=dict(C_c_pF=c_c_a30, C_g_pF=c_g_a30, C_g_mirror_pF=mirror_a30),
            centre_NODET=dict(C_c_pF=c_c_nodet, C_g_pF=c_g_nodet),
            outer_seg=dict(C_c_pF=c_c_seg, C_c_plain_section_pF=c_c_seg_plain,
                           C_g_pF_bracket=[CG_SEG5_PF, CG_SEG8_PF]),
            mirror_to_centre_2240_pF=pF(s["Cg_parts_full"]["mirror"], L_SLOT),
            mirror_to_centre_2730_pF=pF(s["Cg_parts_full"]["mirror"], L_MIRROR_NOTE),
        )
        # full C_g parts for the slot section, A30 (fF/um, full geometry, per unit length)
        el[au]["centre_slot_Cg_parts_fF_per_um"] = s["Cg_parts_full"]
        el[au]["centre_slot_Cg_parts_fF_per_um"] = {k: float(v) for k, v in s["Cg_parts_full"].items()}
        print(f"  {au}: centre DC A30 C_c {c_c_a30:.4f} pF, C_g {c_g_a30:.4f} pF (mirror {mirror_a30:.4f} pF); "
              f"NODET C_c {c_c_nodet:.4f} pF, C_g {c_g_nodet:.4f} pF; outer segment C_c {c_c_seg:.5f} pF; "
              f"mirror-to-centre 2240 um {el[au]['mirror_to_centre_2240_pF']:.3f} pF, 2730 um "
              f"{el[au]['mirror_to_centre_2730_pF']:.3f} pF")

    # ---------------- Part C: divider
    print("Part C: divider V_el (V) and filter current I (uA)")
    div_rows = []
    for au, _ in AU:
        rows = [
            ("centre DC (A30)", el[au]["centre_A30"]["C_c_pF"], el[au]["centre_A30"]["C_g_pF"]),
            ("centre DC (NODET)", el[au]["centre_NODET"]["C_c_pF"], el[au]["centre_NODET"]["C_g_pF"]),
            ("outer segment, 5 mm lead", el[au]["outer_seg"]["C_c_pF"], CG_SEG5_PF),
            ("outer segment, 8 mm lead", el[au]["outer_seg"]["C_c_pF"], CG_SEG8_PF),
        ]
        for label, c_c, c_g in rows:
            for c_f in C_FILTER_PF:
                v_el = divider(c_c, c_g, c_f)
                i_ua = OMEGA * (c_f * 1e-12) * v_el * 1e6
                div_rows.append(dict(electrode=label, Au=au, C_c_pF=c_c, C_g_pF=c_g, C_f_pF=c_f,
                                     V_el_V=v_el, I_uA=i_ua))
                print(f"  {au} {label:26s} C_c {c_c:.4f} C_g {c_g:.4f} C_f {c_f:>8.0f} pF: "
                      f"V_el {v_el:.5g} V, I {i_ua:.4g} uA")

    # ---------------- Part D: null shifts with gds2itvg (as sim 12)
    print("Part D: RF null shift (gds2itvg, A30 layout)")
    LAYOUT = json.load(open(JS))
    GDS = os.path.join(os.path.dirname(JS), LAYOUT["_gds"]) if "_gds" in LAYOUT else JS.replace("_sim.json", ".gds")
    lay = Layout.from_json(JS)
    els, _ = build_electrodes(GDS, lay, ion_box=(-20, 20, -900, 350), ion_z=(25, 90), return_ground=True)
    null_rows = []
    zone_out = {}
    for zname, y in (("readout", LAYOUT["_zones"]["readout_itvg_y"]), ("loading", LAYOUT["_zones"]["loading_itvg_y"])):
        r = rf_null(els, ["1"], y=float(y), z_range=(15, 150))
        p = np.array([r["x"], y, r["z"]])
        T = tc.taylor_all(els, p)
        _, _, Hrf = tc.sum_taylor(T, {"1": 1.0})
        H2 = Hrf[np.ix_([0, 2], [0, 2])]
        top_near = max(TOP, key=lambda n: abs(T[n][0]))
        bot_near = max(BOT, key=lambda n: abs(T[n][0]))
        zone_out[zname] = dict(y_itvg=y, null_x=float(r["x"]), null_z=float(r["z"]), top_nearest=top_near,
                               bottom_nearest=bot_near, H_rf_radial_V_per_um2=H2.tolist())
        print(f"  {zname} y={y:.0f}: null x {r['x']:.3f}, z {r['z']:.3f} um; nearest top {top_near}, bottom {bot_near}")
        for au, _ in AU:
            for c_f in C_FILTER_PF:
                v_c = divider(el[au]["centre_A30"]["C_c_pF"], el[au]["centre_A30"]["C_g_pF"], c_f)
                v5 = divider(el[au]["outer_seg"]["C_c_pF"], CG_SEG5_PF, c_f)
                v8 = divider(el[au]["outer_seg"]["C_c_pF"], CG_SEG8_PF, c_f)
                d_c = shift_nm(T, H2, ["2"], v_c)
                d_t5 = shift_nm(T, H2, [top_near], v5)
                d_tb5 = shift_nm(T, H2, [top_near, bot_near], v5)
                d_t8 = shift_nm(T, H2, [top_near], v8)
                d_tb8 = shift_nm(T, H2, [top_near, bot_near], v8)
                row = dict(zone=zname, Au=au, C_f_pF=c_f, V_el_centre_V=v_c, V_el_outer5_V=v5,
                           V_el_outer8_V=v8,
                           centre_nm=[float(d_c[0]), float(d_c[1])], centre_abs_nm=float(np.linalg.norm(d_c)),
                           top5_abs_nm=float(np.linalg.norm(d_t5)), top_bottom5_abs_nm=float(np.linalg.norm(d_tb5)),
                           top_bottom5_xz_nm=[float(d_tb5[0]), float(d_tb5[1])],
                           top8_abs_nm=float(np.linalg.norm(d_t8)), top_bottom8_abs_nm=float(np.linalg.norm(d_tb8)))
                null_rows.append(row)
                print(f"    {au} C_f {c_f:>8.0f} pF: centre |d| {row['centre_abs_nm']:.4g} nm; top |d| "
                      f"{row['top5_abs_nm']:.4g}; top+bottom |d| {row['top_bottom5_abs_nm']:.4g} nm")
        if zname == "readout":
            # acceptance: doubling V_el doubles the shift
            d1 = shift_nm(T, H2, ["2"], 0.7)
            d2 = shift_nm(T, H2, ["2"], 1.4)
            lin_ok = bool(np.allclose(d2, 2 * d1, rtol=1e-9, atol=1e-12))
    electrodes_used = dict(centre="2", outer_top_readout=zone_out["readout"]["top_nearest"],
                           outer_bottom_readout=zone_out["readout"]["bottom_nearest"],
                           outer_top_loading=zone_out["loading"]["top_nearest"],
                           outer_bottom_loading=zone_out["loading"]["bottom_nearest"])

    # ---------------- acceptance
    s_e2, s_e1 = pul[("slot", "E2")], pul[("slot", "E1")]
    lead_e2 = s_e2["C_rf_lead_half"]
    lead_e1 = s_e1["C_rf_lead_half"]
    mir_rf_e2 = s_e2["C_rf_mirror_full"]
    lead_mir_e2 = s_e2["C_lead_mirror_half"]
    acceptance = dict(
        reproduces_10c_lead=bool(abs(lead_e2 - 0.0021322) <= 1e-5 and abs(lead_e1 - 0.0013698) <= 1e-5),
        reproduces_10c_mirror=bool(abs(mir_rf_e2 - 0.15294) <= 0.0005 and abs(lead_mir_e2 - 0.48883) <= 0.002),
        reciprocity_within_2pct=bool(recip_max < 0.02),
        charge_conserved=bool(cons_max < 0.01),
        null_shift_is_linear=lin_ok,
    )
    numbers = dict(
        C_rf_lead_E2=lead_e2, C_rf_lead_E1=lead_e1, C_rf_mirror_E2=mir_rf_e2, C_lead_mirror_E2=lead_mir_e2,
        reciprocity_max_rel=recip_max, charge_conservation_max_rel=cons_max,
    )

    print("ACCEPTANCE (numbers):")
    for k, v in numbers.items():
        print(f"  {k}: {v:.8g}")
    print("ACCEPTANCE (checks):")
    for k, v in acceptance.items():
        print(f"  {k}: {v}")

    # ---------------- outputs
    summary = dict(
        units="fF/um (per unit length along the trap axis), half domain unless stated",
        conventions=dict(
            half_domain="cap(i,j) = -Q[i,j], i != j; centre DC, mirror and box straddle x=0 (full = 2 x half)",
            rails_and_leads="one copy each on x > 0; cap(rail, electrode) = coupling of that electrode to both rails",
            pad_estimates="pad_electrical_effects.md lines 29-31 (eps_r 3.9, 10 um SiO2 over buried Al: not the v4 stack)",
        ),
        matrix_half_domain_fF_per_um={f"{sec}_{au}": dict(names=mats[(sec, au)][0],
                                                       Q=mats[(sec, au)][1].tolist())
                                      for sec in ("slot", "plain") for au, _ in AU},
        per_unit_length_fF_per_um={f"{sec}_{au}": {k: (v if not isinstance(v, dict) else
                                                    {kk: float(vv) for kk, vv in v.items()})
                                                   for k, v in pul[(sec, au)].items() if k != "names"}
                                   for sec in ("slot", "plain") for au, _ in AU},
        per_electrode=el,
        divider=div_rows,
        null_shifts=null_rows,
        null_zones=zone_out,
        electrodes_used_for_null_shift=electrodes_used,
        numbers=numbers,
        acceptance=acceptance,
    )
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)

    write_table(el, div_rows, null_rows, electrodes_used, numbers, mats, pul)
    print(f"whole run {time.time() - t_all:.1f} s")


def write_table(el, div_rows, null_rows, electrodes_used, numbers, mats, pul):
    L = ["> **Claude-authored.** Written by sim/23_dc_rf_coupling.py: RF coupling onto the DC electrodes and the "
         "filter-capacitor divider, 2026-11-10.", ""]
    L += ["## Per-electrode capacitance [team calc]", "",
          "| Electrode | Au | C_c, rails to electrode (pF) | C_g, to ground (pF) | of which Al mirror (pF) |",
          "|---|---|---|---|---|"]
    for au, _ in AU:
        a = el[au]["centre_A30"]
        n = el[au]["centre_NODET"]
        o = el[au]["outer_seg"]
        L.append(f"| centre DC, A30 (2240 um slot + 1760 um plain) | {au} | {a['C_c_pF']:.4f} | {a['C_g_pF']:.4f} "
                 f"| {a['C_g_mirror_pF']:.4f} |")
        L.append(f"| centre DC, NODET (4000 um plain) | {au} | {n['C_c_pF']:.4f} | {n['C_g_pF']:.4f} | - |")
        L.append(f"| outer DC segment, 120 um (C_g from pad estimates, 5 / 8 mm lead) | {au} | {o['C_c_pF']:.5f} | "
                 f"{CG_SEG5_PF:.3f} / {CG_SEG8_PF:.3f} | - |")
    L += ["", "Mirror to centre DC: " + "; ".join(
        f"{au} {el[au]['mirror_to_centre_2240_pF']:.3f} pF over 2240 um, {el[au]['mirror_to_centre_2730_pF']:.3f} pF "
        f"over 2730 um (LOCAL_MIRROR.md quotes about 12 pF at 318 nm gap, 2.73 mm)" for au, _ in AU) + ".", ""]
    L += ["## Divider and RF on the electrode, and filter current [team calc]", "",
          "| Electrode | Au | C_f (pF) | V_el (V) | I = omega C_f V_el (uA) |", "|---|---|---|---|---|"]
    for r in div_rows:
        L.append(f"| {r['electrode']} (C_c {r['C_c_pF']:.4f} pF, C_g {r['C_g_pF']:.3f} pF) | {r['Au']} | "
                 f"{r['C_f_pF']:.0f} | {r['V_el_V']:.4g} | {r['I_uA']:.4g} |")
    L += ["", "## RF null shift (gds2itvg, A30 layout) [team calc]", "",
          f"Electrodes used: centre 2; outer segments nearest the ion (by unit potential) at readout: top "
          f"{electrodes_used['outer_top_readout']}, bottom {electrodes_used['outer_bottom_readout']}; at loading: top "
          f"{electrodes_used['outer_top_loading']}, bottom {electrodes_used['outer_bottom_loading']}.", "",
          "| Zone | Au | C_f (pF) | centre DC shift (nm) | top segment, 5 mm lead (nm) | top + bottom, 5 mm (nm) | top + bottom, 8 mm (nm) |",
          "|---|---|---|---|---|---|---|"]
    for r in null_rows:
        L.append(f"| {r['zone']} | {r['Au']} | {r['C_f_pF']:.0f} | {r['centre_abs_nm']:.4g} | {r['top5_abs_nm']:.4g} | "
                 f"{r['top_bottom5_abs_nm']:.4g} | {r['top_bottom8_abs_nm']:.4g} |")
    L += ["", "Limits: 2-D capacitance, ideal conductors, no segment ends, no lead tracks near the rails; bond wire and "
          "lead inductance ignored; C_g for the outer segment is the pad note's estimate (10 um SiO2 over buried Al), "
          "not a value for this stack."]
    with open(os.path.join(OUT, "table.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
