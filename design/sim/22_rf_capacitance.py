"""22 - RF capacitance of the v4 trap chip, its dielectric loss, and what it means for the resonator (Claude-authored).

Questions answered:
  1. How much capacitance does the RF conductor have to ground on each v4 die (A30, NODET; E1 and E2 Au)?
  2. How much of the field energy sits in Si and in SiO2 (participation, by +/-5 % permittivity)?
  3. What Q does the chip dielectric allow (room temperature: Si lossy; cold: Si lossless)?
  4. What is the RF heating bound of sim 18 at this capacitance?
  5. What do the chip capacitance and extra loads give for the resonator (L, drive power, frequency error)?
  6. What does the electrical test a10 (LCR, 1 MHz, room temperature) read for this chip? Two limits.

Model: the 2-D finite-volume electrostatics of sim 10c (copied, not imported: its grid helpers, laplacian, solve,
charge and geometry). Each section of the RF conductor is one cross-section perpendicular to the trap axis:
  slot   lead slot, Al mirror under |x| <= 20 um (A30 only, 2240 um)
  plain  rails and centre DC, no mirror, no leads (A30 1760 um; NODET 4000 um)
  ubar   the U-bar joining the two rails (75 um)
  feed   RF feed lead, 60 um wide with a 10 um gap to the ground fill (2525 um)
  pad    RF pad, 200 um wide with a 30 um gap to the ground fill (200 um)
RF at 1 V, every other conductor at 0 V. Stack (z = 0 at the Au top, as 10c): Au 6 um (E2) or 0.35 um (E1);
SiO2 cap 0.160 um, SiO2 spacer 0.238 um, thermal SiO2 1.0 um (the 7 nm NbN is kept as SiO2 in slot, as 10c does);
slot only: 0.100 um Al inlaid in the top of the thermal SiO2 under |x| <= 20 um (thermal SiO2 under it 0.90 um), as
10c's al100_inlaid case. HR Si eps 11.7; grounded back side at z = -516 um (10c's value; the Si is ~508 to 515 um
deep, not exactly 500 um); grounded box 400 um above and 400 um to the side.
Non-slot sections: full stack (cap + spacer + thermal) or thermal SiO2 only (NODET).

Section total (pF) = 2 x (half-domain value, pF/mm) x length. The half domain holds one rail (slot, plain) or half
the strip (ubar, feed, pad). Per-unit values are per rail for slot and plain and for the full strip otherwise.

Limits: 2-D (end effects, rail ends, corners and the pad's far edge are neglected [inference]); ideal conductors;
B60 taken equal to A30 [inference]; Si loss and tan_d of SiO2 are first-order [inference]; the a10 limits are for
the chip alone (no carrier, no bond wires) [inference].

Outputs (design/sim/out/22_rf_capacitance/): summary.json, table.md, sections.png.
Run: cd design/sim && ./run.sh 22_rf_capacitance.py
"""

import json
import os
import sys
from math import pi, sqrt

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.special import ellipk
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "22_rf_capacitance")
REF_10C = os.path.join(HERE, "out", "10c_mirror_thickness", "summary.json")
REF_10B = os.path.join(HERE, "out", "10b_rf_pickup_v4", "summary.json")
REF_18 = os.path.join(HERE, "out", "18_e1_vs_e2", "summary.json")
os.makedirs(OUT, exist_ok=True)

EPS0 = 8.8541878128e-12
V_RF, F_RF = 53.0, 28e6
OMEGA = 2 * pi * F_RF
EPS_OX, EPS_SI = 3.9, 11.7
RHO_SI = 200.0                                  # Ohm m, the 20 kOhm cm lower spec (design/CLAUDE.md)
X_SLOT, X_LEAD0, X_LEAD1 = 12.5, 2.5, 7.5       # slot cut, as 10c
X_C, X_RF0, X_RF1, X_OUT, X_MAX, X_MIR = 20.0, 25.0, 109.0, 114.0, 400.0, 20.0
Z_TOP, Z_BACK = 400.0, -516.0                   # as 10c
T_NBN = 0.007
PAD_HALF, PAD_GAP = 100.0, 30.0                 # measured (see MEASURED_GAPS): pad RF |y| <= 100, ground from |y| = 130
FEED_HALF, FEED_GAP = 30.0, 10.0                # measured: feed RF |y| <= 30, ground from |y| = 40

# Section lengths along the trap axis (um), from the GDS layout (brief)
LEN_A30 = [("slot", 2240.0), ("plain", 1760.0), ("ubar", 75.0), ("feed", 2525.0), ("pad", 200.0)]
LEN_NODET = [("plain", 4000.0), ("ubar", 75.0), ("feed", 2525.0), ("pad", 200.0)]
# RF interval (half domain) and 0 V conductor intervals (x0, x1, name) per section
RF_IV = {"slot": (X_RF0, X_RF1), "plain": (X_RF0, X_RF1), "ubar": (0.0, X_RF1),
         "feed": (0.0, FEED_HALF), "pad": (0.0, PAD_HALF)}
ZERO_IV = {"slot": [("dc", X_SLOT, X_C), ("lead", X_LEAD0, X_LEAD1), ("gnd", X_OUT, X_MAX)],
           "plain": [("dc", 0.0, X_C), ("gnd", X_OUT, X_MAX)],
           "ubar": [("gnd", X_OUT, X_MAX)],
           "feed": [("gnd", FEED_HALF + FEED_GAP, X_MAX)],
           "pad": [("gnd", PAD_HALF + PAD_GAP, X_MAX)]}
# Extra x knots (mesh nodes exactly on the conductor edges that are not already knots)
XEXTRA = {"feed": [(30.0, 1.0), (40.0, 1.0)], "pad": [(130.0, 0.2)]}

# Measured on gds/trap_die_v4_A30.gds and gds/trap_die_v4_NODET.gds, layer 50, union of polygons, vertical lines
# (script run 2026-11-10, read-only): y-intervals of Au that are the RF strip and the ground fill
MEASURED_GAPS = {
    "A30 x=3000 (feed)": [[-30.0, 30.0], [40.0, 324.0]],
    "A30 x=4500 (feed)": [[-30.0, 30.0], [40.0, 4900.0]],
    "A30 x=4700 (pad)": [[-100.0, 100.0], [130.0, 4900.0]],
    "NODET x=3000 (feed)": [[-30.0, 30.0], [40.0, 324.0]],
    "NODET x=4500 (feed)": [[-30.0, 30.0], [40.0, 4900.0]],
    "NODET x=4700 (pad)": [[-100.0, 100.0], [130.0, 4900.0]],
}

# Sim 18 constants (copied; same formula and resistances)
RHO_RT = {"bulk": 2.44e-8, "film": 4.0e-8}
RRR = [2, 5, 10]
SQ_RAIL = 4000.0 / 84.0                                  # one rail: 4000 um long, 84 um wide, as 18
SQ_FEED = (4700.0 - (2000.0 + 60.0)) / 60.0              # 2640 / 60, as 18
C_OTHER = [3.0, 7.0, 17.0]                               # pF, resonator loads
TAN_SIO2 = [1e-4, 1e-3, 1e-2]                            # [verify]: no measured value in the repo
Q_LOAD = [50, 100, 200, 500]

# Citations for the extra loads (repo-relative; line numbers checked by grep)
C_OTHER_SRC = {
    3.0: "design/research/research_notes/Bond pad sizing for ion traps/ion_trap_pad_literature.md line 97 "
         "(Zhao et al.: RF-to-ground 3 pF after wire-bond pads removed; a trap-die value, used as a size reference [inference])",
    7.0: "design/research/research_notes/Bond pad sizing for ion traps/ion_trap_pad_literature.md line 95 "
         "(Stick et al.: 7 pF RF-to-ground, trap and CPGA package)",
    17.0: "design/research/research_notes/Bond pad sizing for ion traps/pad_electrical_effects.md line 20 "
          "(Siverns et al.: 17 +/- 2 pF, ion trap plus vacuum system)",
}


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


# ------------------------------------------------------------------ geometry
def xknots(sec, hs):
    base = [(0.0, 0.05), (19.0, 0.05), (X_C, 0.1), (X_RF0, 0.1), (45.0, 1.0), (100.0, 1.0),
            (X_RF1, 0.2), (X_OUT, 0.2), (150.0, 2.0), (X_MAX, 25.0)]
    return [(x, h * hs) for x, h in sorted(base + XEXTRA.get(sec, []))]


def zknots(p, z_cap, z_nw_bot, z_nw_top, z_al_bot, z_al_top, z_d1_bot, hs):
    zk = [(Z_BACK, 40.0), (-30.0, 2.0), (z_d1_bot, 0.1)]
    if p["t_al"] > 0:
        zk += [(z_al_bot, 0.02), (z_al_top, 0.01)]
    if p["nbn"]:
        zk += [(z_nw_bot, T_NBN / 2), (z_nw_top, T_NBN / 2)]
    top = [(z_cap, 0.01), (z_cap + 0.06, 0.02), (-p["t_au"] / 2, 0.3), (0.0, 0.1)] if p["t_au"] > 1 \
        else [(z_cap, 0.01), (0.0, 0.02)]
    return [(z, h * hs) for z, h in zk + top + [(20.0, 1.0), (Z_TOP, 25.0)]]


def build(sec, p, eps_si, eps_ox, si_ground, hs):
    z_cap = -p["t_au"]
    z_nw_top = z_cap - p["t_cap"]
    z_nw_bot = z_nw_top - (T_NBN if p["nbn"] else 0.0)
    z_al_top = z_nw_bot - p["t_sp"]
    z_al_bot = z_al_top - p["t_al"]
    z_d1_bot = z_al_bot - p["t_d1"]
    xs = axis(xknots(sec, hs))
    zs = axis(zknots(p, z_cap, z_nw_bot, z_nw_top, z_al_bot, z_al_top, z_d1_bot, hs))
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    xc, zc = 0.5 * (xs[1:] + xs[:-1]), 0.5 * (zs[1:] + zs[:-1])
    XC, ZC = np.meshgrid(xc, zc, indexing="ij")
    tol = 1e-9

    def box(x0, x1, z0, z1):
        return (X >= x0 - tol) & (X <= x1 + tol) & (Z >= z0 - tol) & (Z <= z1 + tol)

    eps = np.ones_like(XC)                       # vacuum above the Au and in the gaps
    eps[ZC < z_cap] = eps_ox                     # SiO2 cap, spacer, thermal SiO2
    eps[ZC < z_d1_bot] = eps_si                  # HR Si
    rf = box(RF_IV[sec][0], RF_IV[sec][1], z_cap, 0.0)
    zero = {name: box(x0, x1, z_cap, 0.0) for name, x0, x1 in ZERO_IV[sec]}
    if p["t_al"] > 0:
        zero["mirror"] = box(0.0, X_MIR, z_al_bot, z_al_top)
    if si_ground:
        zero["si"] = Z <= z_d1_bot + tol         # Si replaced by a grounded conductor (a10 limit)
    fixed = (X >= X_MAX - tol) | (Z <= Z_BACK + tol) | (Z >= Z_TOP - tol) | rf
    for m in zero.values():
        fixed = fixed | m
    return xs, zs, eps, rf, zero, fixed


def run(sec, p, eps_si=EPS_SI, eps_ox=EPS_OX, si_ground=False, hs=1.0):
    """Half-domain capacitance of the RF conductor to everything else (pF/mm), plus mirror and lead for slot."""
    xs, zs, eps, rf, zero, fixed = build(sec, p, eps_si, eps_ox, si_ground, hs)
    K = laplacian(xs, zs, eps)
    phi = solve(K, fixed, [np.where(rf, 1.0, 0.0)])[0]
    out = dict(half=charge(K, phi, rf) * 1e9)    # F/m -> pF/mm
    if "mirror" in zero:
        out["C_mirror_fF_um"] = -2 * charge(K, phi, zero["mirror"]) * 1e9   # F/m -> fF/um; both halves
    if "lead" in zero:
        out["C_lead_fF_um"] = -charge(K, phi, zero["lead"]) * 1e9           # one lead, half domain
    return out


def params(sec, t_au, stack):
    if sec == "slot":                            # 10c al100_inlaid
        return dict(t_au=t_au, t_cap=0.160, t_sp=0.238, nbn=True, t_al=0.100, t_d1=0.90)
    if stack == "full":
        return dict(t_au=t_au, t_cap=0.160, t_sp=0.238, nbn=False, t_al=0.0, t_d1=1.0)
    return dict(t_au=t_au, t_cap=0.0, t_sp=0.0, nbn=False, t_al=0.0, t_d1=1.0)


def section(sec, L, p):
    nom = run(sec, p)
    c0 = 2 * nom["half"] * L / 1000.0            # pF, both halves, length in mm
    sip = 2 * run(sec, p, eps_si=EPS_SI * 1.05)["half"] * L / 1000.0
    sim = 2 * run(sec, p, eps_si=EPS_SI * 0.95)["half"] * L / 1000.0
    oxp = 2 * run(sec, p, eps_ox=EPS_OX * 1.05)["half"] * L / 1000.0
    oxm = 2 * run(sec, p, eps_ox=EPS_OX * 0.95)["half"] * L / 1000.0
    gsi = 2 * run(sec, p, si_ground=True)["half"] * L / 1000.0
    r = dict(L_um=L,
             unit_pF_per_mm=nom["half"] if sec in ("slot", "plain") else 2 * nom["half"],
             unit_basis="per rail" if sec in ("slot", "plain") else "full strip",
             C_pF=c0, p_Si=(sip - sim) / (0.10 * c0), p_SiO2=(oxp - oxm) / (0.10 * c0),
             C_groundSi_pF=gsi, _sip=sip, _sim=sim, _oxp=oxp, _oxm=oxm)
    if sec == "slot":
        r["C_rf_mirror_fF_per_um"] = nom["C_mirror_fF_um"]
        r["C_rf_lead_fF_per_um"] = nom["C_lead_fF_um"]
    return r


def config(name, die, t_au, stack):
    secs = LEN_A30 if die == "A30" else LEN_NODET
    res = {}
    for sec, L in secs:
        res[sec] = section(sec, L, params(sec, t_au, stack))
        print(f"{name:18s} {sec:6s} L {L:6.0f} um: C {res[sec]['C_pF']:.4f} pF, p_Si {res[sec]['p_Si']:.4f}, "
              f"p_SiO2 {res[sec]['p_SiO2']:.4f}, C with grounded Si {res[sec]['C_groundSi_pF']:.4f} pF", flush=True)
    C = sum(r["C_pF"] for r in res.values())
    L_tot = sum(r["L_um"] for r in res.values())
    chip = dict(
        C_chip_pF=C,
        C_chip_groundSi_pF=sum(r["C_groundSi_pF"] for r in res.values()),
        p_Si_length_weighted=sum(r["p_Si"] * r["L_um"] for r in res.values()) / L_tot,
        p_SiO2_length_weighted=sum(r["p_SiO2"] * r["L_um"] for r in res.values()) / L_tot,
        p_Si_C_weighted=(sum(r["_sip"] for r in res.values()) - sum(r["_sim"] for r in res.values())) / (0.1 * C),
        p_SiO2_C_weighted=(sum(r["_oxp"] for r in res.values()) - sum(r["_oxm"] for r in res.values())) / (0.1 * C),
    )
    for r in res.values():
        for k in [k for k in r if k.startswith("_")]:
            del r[k]
    return dict(die=die, t_au_um=t_au, stack=stack, sections=res, chip=chip)


def heat(C_pF, t_au_um, rho_lab, n):
    """Sim 18's formula (same resistances). Returns current amplitude (A), sim 18 bound (W), linear-fall line (W)."""
    t = t_au_um * 1e-6
    rs4 = RHO_RT[rho_lab] / n / t
    I = OMEGA * C_pF * 1e-12 * V_RF
    p18 = 0.5 * I * I * SQ_FEED * rs4 + I * I * (SQ_RAIL * rs4) / 12.0
    plin = 0.5 * I * I * SQ_FEED * rs4 + (1.0 / 3.0) * I * I * (SQ_RAIL * rs4) / 12.0
    return I, p18, plin


def main():
    # ---------------- configurations
    CONF = [("A30_E2", "A30", 6.0, "full"), ("A30_E1", "A30", 0.35, "full"),
            ("NODET_E2_full", "NODET", 6.0, "full"), ("NODET_E2_thermal", "NODET", 6.0, "thermal"),
            ("NODET_E1_full", "NODET", 0.35, "full"), ("NODET_E1_thermal", "NODET", 0.35, "thermal")]
    cfg = {}
    for name, die, t_au, stack in CONF:
        cfg[name] = config(name, die, t_au, stack)
        c = cfg[name]["chip"]
        print(f"CHIP {name}: C_chip {c['C_chip_pF']:.4f} pF, grounded-Si {c['C_chip_groundSi_pF']:.4f} pF, "
              f"p_Si {c['p_Si_length_weighted']:.4f}, p_SiO2 {c['p_SiO2_length_weighted']:.4f}", flush=True)

    # ---------------- convergence (halved spacing, plain and feed, A30 E2 full stack)
    conv = {}
    for sec in ("plain", "feed"):
        a = run(sec, params(sec, 6.0, "full"))["half"]
        b = run(sec, params(sec, 6.0, "full"), hs=0.5)["half"]
        conv[sec] = dict(coarse_pF_per_mm=a, fine_pF_per_mm=b, rel_change=abs(b - a) / a)
        print(f"convergence {sec}: coarse {a:.6f}, half spacing {b:.6f}, change {abs(b - a) / a:.4%}", flush=True)

    # ---------------- check 10c (slot, al100_inlaid, E2)
    with open(REF_10C) as fh:
        ref10c = json.load(fh)["al100_inlaid"]["E2"]["slot"]
    s = run("slot", params("slot", 6.0, "full"))
    mir, lead = s["C_mirror_fF_um"], s["C_lead_fF_um"]
    ok10c = abs(mir - ref10c["C_rf_mirror_fF_per_um"]) <= 5e-4 and abs(lead - ref10c["C_rf_lead_fF_per_um"]) <= 1e-5
    print(f"10c slot E2: mirror {mir:.6f} fF/um (10c {ref10c['C_rf_mirror_fF_per_um']:.6f}), "
          f"lead {lead:.7f} fF/um (10c {ref10c['C_rf_lead_fF_per_um']:.7f})", flush=True)

    # ---------------- check 10b (rail, 10b parameters, E2 slot)
    with open(REF_10B) as fh:
        ref10b = json.load(fh)["E2_slot"]["C_rf_per_rail_pF_per_mm"]
    p10b = dict(t_au=6.0, t_cap=0.080, t_sp=0.238, nbn=True, t_al=0.150, t_d1=1.0)
    rail = run("slot", p10b)["half"]
    ok10b = abs(rail - ref10b) <= 5e-4
    print(f"10b rail E2: {rail:.6f} pF/mm per rail (10b {ref10b:.6f})", flush=True)

    # ---------------- check 18 (1 pF row, all six resistance cases, both options)
    with open(REF_18) as fh:
        rows18 = {r["quantity"]: r for r in json.load(fh)["rows"]}
    rep18 = {}
    ok18 = True
    for lab in ("bulk", "film"):
        for n in RRR:
            q = f"P upper bound, C_rf = 1 pF, {lab} rho, RRR = {n}"
            for opt, t_au in (("E1", 0.35), ("E2", 6.0)):
                _, p18, _ = heat(1.0, t_au, lab, n)
                mine = f"{p18 * 1e6:.2f}"
                want = rows18[q][opt]
                rep18[f"{q} {opt}"] = dict(mine_uW=mine, sim18_uW=want)
                ok18 = ok18 and (mine == want)
    print("sim 18 1 pF row reproduced:", ok18, flush=True)

    # ---------------- feed sanity (textbook CPW, full strip per length)
    k = 30.0 / 40.0
    kp = sqrt(1 - k * k)
    eps_eff = (1 + 11.7) / 2
    cpw = 4 * EPS0 * eps_eff * ellipk(k ** 2) / ellipk(kp ** 2) * 1e9       # pF/mm
    feed_solver = cfg["A30_E2"]["sections"]["feed"]["unit_pF_per_mm"]
    ratio = feed_solver / cpw
    okfeed = (1 / 1.5) <= ratio <= 1.5
    print(f"feed sanity: solver {feed_solver:.5f} pF/mm (full strip), CPW textbook {cpw:.5f} pF/mm, ratio {ratio:.3f}",
          flush=True)

    # ---------------- heating (sim 18 formula, per config with its own C_chip and Au)
    heating = {}
    for name in cfg:
        c = cfg[name]
        heating[name] = {}
        for lab in ("bulk", "film"):
            for n in RRR:
                I, p18, plin = heat(c["chip"]["C_chip_pF"], c["t_au_um"], lab, n)
                heating[name][f"{lab}_RRR{n}"] = dict(I_mA=I * 1e3, P18_mW=p18 * 1e3, P_linear_mW=plin * 1e3)

    # ---------------- loss
    tan_si = 1.0 / (OMEGA * EPS0 * EPS_SI * RHO_SI)
    tan_si_1MHz = 1.0 / (2 * pi * 1e6 * EPS0 * EPS_SI * RHO_SI)
    print(f"tan_d Si at 28 MHz (200 Ohm m): {tan_si:.4f}; at 1 MHz: {tan_si_1MHz:.3f}", flush=True)
    Q = {}
    for name in cfg:
        ch = cfg[name]["chip"]
        Q[name] = {}
        for t in TAN_SIO2:
            q_room = 1.0 / (ch["p_Si_length_weighted"] * tan_si + ch["p_SiO2_length_weighted"] * t)
            q_cold = 1.0 / (ch["p_SiO2_length_weighted"] * t)
            Q[name][f"tan_SiO2_{t:g}"] = dict(Q_room=q_room, Q_cold=q_cold)

    # ---------------- resonator table
    res_rows = []
    for name in ("A30_E2", "A30_E1"):
        C_chip = cfg[name]["chip"]["C_chip_pF"]
        for C_o in C_OTHER:
            C_tot = C_chip + C_o
            Ctot_F = C_tot * 1e-12
            L_uH = 1.0 / (OMEGA ** 2 * Ctot_F) * 1e6
            P_mW = {int(Qv): OMEGA * Ctot_F * V_RF ** 2 / (2 * Qv) * 1e3 for Qv in Q_LOAD}
            df_pct = -1.0 / (2 * C_tot) * 100.0
            res_rows.append(dict(chip=name, C_chip_pF=C_chip, C_other_pF=C_o, C_tot_pF=C_tot, L_uH=L_uH,
                                 P_mW=P_mW, df_over_f_pct_per_pF=df_pct, source=C_OTHER_SRC[C_o]))

    # ---------------- acceptance
    acc = {
        "reproduces_10c_slot_E2": bool(ok10c),
        "reproduces_10b_rail": bool(ok10b),
        "grid_converged": bool(max(conv["plain"]["rel_change"], conv["feed"]["rel_change"]) < 0.01),
        "reproduces_sim18_1pF_row": bool(ok18),
        "feed_sanity": bool(okfeed),
    }

    summary = dict(
        measured_gaps_um=MEASURED_GAPS,
        inputs=dict(V_RF=V_RF, F_RF=F_RF, EPS_OX=EPS_OX, EPS_SI=EPS_SI, RHO_SI=RHO_SI, Z_BACK=Z_BACK,
                    SQ_RAIL=SQ_RAIL, SQ_FEED=SQ_FEED, PAD_GAP=PAD_GAP, FEED_GAP=FEED_GAP,
                    B60="taken equal to A30 [inference]"),
        configs=cfg,
        convergence=conv,
        checks=dict(ref10c=dict(mirror_fF_um=mir, lead_fF_um=lead,
                                ref_mirror=ref10c["C_rf_mirror_fF_per_um"], ref_lead=ref10c["C_rf_lead_fF_per_um"]),
                    ref10b=dict(rail_pF_mm=rail, ref=ref10b),
                    sim18_1pF=rep18,
                    feed_sanity=dict(solver_pF_mm=feed_solver, textbook_pF_mm=cpw, ratio=ratio)),
        loss=dict(tan_d_Si_28MHz=tan_si, tan_d_Si_1MHz=tan_si_1MHz, Q=Q, tan_SiO2_values_verify=TAN_SIO2),
        heating=heating,
        resonator=res_rows,
        acceptance=acc,
    )
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)

    # ---------------- table.md
    L = ["> **Claude-authored.** Written by design/sim/22_rf_capacitance.py (regenerate, do not edit), 2026-11-10.", "",
         "## Section table", "",
         "Per unit: pF/mm per rail (slot, plain) or for the full strip (ubar, feed, pad). "
         "Section pF = both halves x length. [team calc]", "",
         "| Config | Section | Length (um) | Per unit (pF/mm) | Section (pF) | p_Si | p_SiO2 | Section with grounded Si (pF) |",
         "|---|---|---|---|---|---|---|---|"]
    for name in cfg:
        for sec, r in cfg[name]["sections"].items():
            L.append(f"| {name} | {sec} | {r['L_um']:.0f} | {r['unit_pF_per_mm']:.5f} ({r['unit_basis']}) | "
                     f"{r['C_pF']:.4f} | {r['p_Si']:.4f} | {r['p_SiO2']:.4f} | {r['C_groundSi_pF']:.4f} |")
    L += ["", "## Chip totals [team calc]", "",
          "Chip = sum of sections; end effects neglected [inference]. p values are length-weighted means "
          "(as the brief asks); the C-weighted values are in summary.json.", "",
          "| Config | C_chip (pF), Si lossless | C_chip (pF), Si as grounded conductor | p_Si (length-wt) | p_SiO2 (length-wt) |",
          "|---|---|---|---|---|"]
    for name in cfg:
        c = cfg[name]["chip"]
        L.append(f"| {name} | {c['C_chip_pF']:.3f} | {c['C_chip_groundSi_pF']:.3f} | "
                 f"{c['p_Si_length_weighted']:.4f} | {c['p_SiO2_length_weighted']:.4f} |")
    L += ["", "## Loss and Q [inference: first-order, small-loss]", "",
          f"tan_d Si at 28 MHz with rho = 200 Ohm m: {tan_si:.4f} (not small: order-of-magnitude only). "
          "At 5 K the Si is treated as lossless (carriers frozen out, as 10b). "
          f"tan_d Si at 1 MHz, room temperature: {tan_si_1MHz:.2f} (the Si conducts more than it stores).", "",
          "| Config | tan_d SiO2 [verify] | Q (room temperature, Si lossy) | Q (cold, Si lossless) |",
          "|---|---|---|---|"]
    for name in cfg:
        for t in TAN_SIO2:
            qq = Q[name][f"tan_SiO2_{t:g}"]
            L.append(f"| {name} | {t:g} | {qq['Q_room']:.1f} | {qq['Q_cold']:.1f} |")
    L += ["", "## RF heating bound (sim 18 formula) [team calc]", "",
          "Sim 18 bound: 0.5 I^2 R_feed + I^2 R_rail / 12, I = omega C V. Linear-fall line: rail term / 3 "
          "(brief's sensitivity line; sim 18's 1/12 already assumes a linear fall along the rail). "
          "Upper bound: the full current through the whole resistance, as sim 18.", "",
          "| Config | C_chip (pF) | I (mA) | P, bulk, RRR 2 (mW) | P linear, bulk, RRR 2 (mW) | P, film, RRR 2 (mW) | P linear, film, RRR 2 (mW) |",
          "|---|---|---|---|---|---|---|"]
    for name in cfg:
        h = heating[name]
        L.append(f"| {name} | {cfg[name]['chip']['C_chip_pF']:.3f} | {h['bulk_RRR2']['I_mA']:.3f} | "
                 f"{h['bulk_RRR2']['P18_mW']:.4f} | {h['bulk_RRR2']['P_linear_mW']:.4f} | "
                 f"{h['film_RRR2']['P18_mW']:.4f} | {h['film_RRR2']['P_linear_mW']:.4f} |")
    L += ["", "## Resonator table [team calc; C_other sources cited per row]", "",
          "P = omega C_tot V^2 / (2 Q) at V = 53 V; L = 1/(omega^2 C_tot); df/f = -dC/(2 C_tot) per pF of error.", "",
          "| Chip | C_chip (pF) | C_other (pF) | C_tot (pF) | L (uH) | P at Q 50 / 100 / 200 / 500 (mW) | df/f per pF (%) | Source of C_other |",
          "|---|---|---|---|---|---|---|---|"]
    for r in res_rows:
        pq = " / ".join(f"{r['P_mW'][q]:.1f}" for q in Q_LOAD)
        L.append(f"| {r['chip']} | {r['C_chip_pF']:.3f} | {r['C_other_pF']:g} | {r['C_tot_pF']:.3f} | {r['L_uH']:.3f} | "
                 f"{pq} | {r['df_over_f_pct_per_pF']:.3f} | {r['source']} |")
    L += ["", "## Acceptance", ""]
    L += [f"- {'PASS' if v else 'FAIL'}: {k}" for k, v in acc.items()]
    L += ["", "Limits: 2-D; ideal conductors; B60 = A30 [inference]; end effects neglected [inference]; "
          "a10 limits are for the chip alone, not the packaged device [inference]."]
    with open(os.path.join(OUT, "table.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    # ---------------- sections.png (stacked bars, no title)
    secs = ["slot", "plain", "ubar", "feed", "pad"]
    dies = ["A30_E2", "A30_E1", "NODET_E2_full", "NODET_E1_full"]
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    bottom = np.zeros(len(dies))
    for sec in secs:
        vals = np.array([cfg[d]["sections"][sec]["C_pF"] if sec in cfg[d]["sections"] else 0.0 for d in dies])
        ax.bar(dies, vals, bottom=bottom, label=sec)
        bottom += vals
    ax.set_xlabel("Die and Au option")
    ax.set_ylabel("RF capacitance to ground (pF)")
    ax.legend(title="Section")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "sections.png"), dpi=150)
    plt.close(fig)

    # ---------------- print
    print("\nACCEPTANCE")
    for k, v in acc.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    n_fail = sum(1 for v in acc.values() if not v)
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
