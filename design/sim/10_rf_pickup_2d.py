"""10 - RF pickup of the NbN SNSPD in the readout zone: 2-D electrostatics (Claude-authored).

Physics
  The trap RF (V_RF = 53 V at 28 MHz, step 1) couples capacitively into the nanowire meander. At
  28 MHz the wavelength is ~10 m, so the field near the chip is quasi-static: solve Laplace's
  equation div(eps grad phi) = 0 with the RF rails at 1 V and every other conductor at 0 V (DC
  electrodes are RF-grounded through their filter capacitors). Everything scales linearly with V.

  Induced current (Todaro et al., PRL 126, 010501 (2021), Supplement "SNSPD pulses and induced rf
  currents", Fig. S4, Eq. S1): each piece of nanowire has a capacitance C_RN to the RF electrode;
  since |Z_C| >> |Z_L| of the wire, the meander sits near RF ground and the displacement current
  i = j omega C_RN V_RF flows along the wire to the terminations, adding to the DC bias. We compute
  C_RN by holding all nanowires at 0 V and reading off the charge induced on them per volt of RF.
  The peak induced current is then at most I = omega V_RF C_RN (all of it leaving through one end;
  a symmetric termination halves the worst-case current). Todaro measured I1 = 3.5(2) uA spatially
  varying (+0.9 uA uniform) at 8.8 V, 67 MHz on MoSi with Isw ~ 8.9 uA and no ground plane.

  2-D model: an x-z cross-section perpendicular to the trap axis through the readout zone,
  infinitely long along y (worst case for a window: the real window is ~30 um long). Charges are
  per unit length along y; the meander's total C_RN = C'_RN x 30 um (detector length along y).
  Symmetric about x = 0, so only x >= 0 is solved (Neumann at x = 0).

  Numerics: finite volumes on a non-uniform tensor grid (3.5 nm steps across the 7 nm NbN, 25 nm
  across the 30 um window so every 100 nm wire is resolved, growing to 25 um far away). Each node
  carries a potential; each cell carries a permittivity. The flux between two neighbouring nodes is
  eps_face (phi_i - phi_k) x (control-volume face length) / (node spacing). The sum of these
  fluxes out of a node is Q/eps0 there, which gives the charge on any conductor directly (Gauss).

Geometry (um; z = 0 at the Au top, as in 04_window_validation.py):
  Au electrodes z in [-6, 0]: centre DC |x| <= 20 with a 30 um window (|x| < 15 has no Au),
  RF rails 25 <= |x| <= 109, outer DC |x| >= 114. D2 PECVD SiO2 (eps 3.9) z in [-16, -6].
  Under D2: ITO (t_ito) / SiO2 cap / NbN wires (100 nm wide, 200 nm pitch, 7 nm thick) / SiO2
  spacer / Al ground plane (whole chip, also the optical mirror). Thicknesses from step 9.
Cases:
  a   no Al, no ITO; a grounded plane 1 um below the nanowire (as specified; crude "Si as ground")
  a2  no Al, no ITO; 1 um SiO2 then high-resistivity Si (eps 11.7, insulating at 5 K) with the
      chip back side grounded 500 um down - the realistic "no mirror" case (Todaro-like)
  b   Al ground plane/mirror only (grounded)
  c1  Al + grounded buried ITO, |x| <= 25 um (window floor + under the centre DC, not under RF)
  c2  Al + grounded buried ITO, |x| <= 114 um (also under the RF rails and gaps)
  d   Al + buried ITO |x| <= 25 um left floating
  e   "ITO on D2": D2 not etched; ITO patch on top of D2 at the bottom of the Au window
      (z = -6, |x| <= 15), tied to the centre DC electrode; no buried ITO; Al below
  Cases a-d have the window etched through D2 (vacuum in |x| < 15 down to the ITO / cap).

Limitations (read before trusting small numbers):
  - 2-D: no field enters from the window ends along y, from the SNSPD leads, or through openings in
    the ITO (vias, lead exits). With grounded ITO above and Al below, the field leaks into the thin
    sandwich only from its edge and decays like exp(-pi x / gap) (gap ~0.3 um), so cases c1/c2
    come out numerically zero. In the real device the lead routing and the ITO openings set the
    floor; this model cannot estimate it.
  - Conductors are ideal (equipotential). For grounded ITO at 40-400 Ohm/sq the RC to its contacts is
    ps (notes Q2), so this holds for C_RN; the I^2 R loss in ITO under the RF rails is computed
    separately from the induced charge.
  - omega V C_RN is an upper bound on the peak current (all current out of one end); the real
    spatial distribution depends on the termination (Todaro Supp. Fig. S4).
  - Grid check (halving every spacing) changes E and C_RN of cases b and e by < 0.5 %.

Outputs: sim/out/10_rf_pickup_2d/rf_pickup.png, potential.png, summary.json
Run:     ./run.sh 10_rf_pickup_2d.py
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "10_rf_pickup_2d")
os.makedirs(OUT, exist_ok=True)

EPS0 = 8.8541878128e-12
V_RF, F_RF = 53.0, 28e6          # step 1 / DESIGN_LOG
OMEGA = 2 * np.pi * F_RF
EPS_OX, EPS_SI = 3.9, 11.7
L_DET = 30.0                     # um, detector length along the trap axis
RAIL_LEN = 5000.0                # um, RF rail length (rails run +/-2.5 mm, step 2)
I_SW = (15.0, 20.0)              # uA, estimated NbN switching current (notes nbn_process.md Q5)
TODARO = dict(I1_uA=3.5, I0_uA=0.9, V=8.8, f=67.03e6, Isw_uA=8.9)

# electrode edges (um, x >= 0)
X_WIN, X_C, X_RF0, X_RF1, X_OUT, X_MAX = 15.0, 20.0, 25.0, 109.0, 114.0, 400.0
Z_AU, Z_D2, Z_TOP, Z_BACK = -6.0, -16.0, 400.0, -516.0
# stack from step 9 (um): ITO 60 nm, cap 80 nm, NbN 7 nm; spacer 234 nm (2nd order) by default
STACK = dict(t_ito=0.060, t_cap=0.080, t_nbn=0.007, t_sp=0.234)
WIRE_W, WIRE_P = 0.100, 0.200


# ------------------------------------------------------------------ grid helpers
def graded(a, b, ha, hb):
    """Points from a to b whose spacing changes linearly from ha (at a) to hb (at b)."""
    if ha == hb:                                  # uniform: exact multiples of the step
        return np.linspace(a, b, int(round((b - a) / ha)) + 1)
    pts, x = [a], a
    while x < b - 1e-12:
        x += ha + (hb - ha) * (x - a) / (b - a)
        pts.append(x)
    pts = np.array(pts)
    return a + (pts - a) * (b - a) / (pts[-1] - a)


def axis(knots):
    """knots: [(position, local spacing), ...] in increasing position."""
    parts = [graded(p0, p1, h0, h1)[:-1] for (p0, h0), (p1, h1) in zip(knots[:-1], knots[1:])]
    return np.concatenate(parts + [np.array([knots[-1][0]])])


def layers(st):
    """z positions of the buried stack for a parameter set."""
    z_ito_bot = Z_D2 - st["t_ito"]
    z_nw_top = z_ito_bot - st["t_cap"]
    z_nw_bot = z_nw_top - st["t_nbn"]
    z_al = z_nw_bot - st["t_sp"]
    z_gnd_a = z_nw_bot - 1.0
    return dict(z_ito_bot=z_ito_bot, z_nw_top=z_nw_top, z_nw_bot=z_nw_bot, z_al=z_al, z_gnd_a=z_gnd_a,
                z_nw=0.5 * (z_nw_top + z_nw_bot))


def make_grid(st):
    L = layers(st)
    xs = axis([(0.0, 0.025), (15.5, 0.025), (X_C, 0.1), (X_RF0, 0.1), (45.0, 1.0), (100.0, 1.0),
               (X_RF1, 0.2), (X_OUT, 0.2), (150.0, 2.0), (X_MAX, 25.0)])
    zs = axis([(Z_BACK, 40.0), (-30.0, 2.0), (L["z_gnd_a"], 0.05), (L["z_al"], 0.01),
               (L["z_nw_bot"], st["t_nbn"] / 2), (L["z_nw_top"], st["t_nbn"] / 2), (L["z_ito_bot"], 0.01),
               (Z_D2, 0.01), (-11.0, 0.4), (Z_AU, 0.02), (Z_AU + 0.06, 0.02), (-3.0, 0.3), (0.0, 0.1),
               (20.0, 1.0), (Z_TOP, 25.0)])
    return xs, zs, L


# ------------------------------------------------------------------ geometry of one case
def build_case(case, st, wires_on):
    """Return grid, cell permittivity, fixed-node mask/values and named conductor masks."""
    xs, zs, L = make_grid(st)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    xc, zc = 0.5 * (xs[1:] + xs[:-1]), 0.5 * (zs[1:] + zs[:-1])
    XC, ZC = np.meshgrid(xc, zc, indexing="ij")
    tol = 1e-9

    def box(Xa, Za, x0, x1, z0, z1):
        return (Xa >= x0 - tol) & (Xa <= x1 + tol) & (Za >= z0 - tol) & (Za <= z1 + tol)

    etched = case in ("a", "a2", "b", "c1", "c2", "d")
    has_al = case not in ("a", "a2")
    ito_x = {"c1": X_RF0, "c2": X_OUT, "d": X_RF0}.get(case)

    # permittivity of every cell
    eps = np.ones_like(XC)
    eps[ZC < Z_AU] = EPS_OX                    # D2, cap, spacer (cells inside conductors are unused)
    if etched:
        eps[(XC < X_WIN) & (ZC > Z_D2) & (ZC < Z_AU)] = 1.0                    # window etched to ITO/cap
    if case == "a2":
        eps[ZC < L["z_gnd_a"]] = EPS_SI                                        # Si below 1 um SiO2

    cond = {}
    cond["rf"] = box(X, Z, X_RF0, X_RF1, Z_AU, 0.0)
    cond["dc"] = box(X, Z, X_WIN, X_C, Z_AU, 0.0) | box(X, Z, X_OUT, X_MAX, Z_AU, 0.0)
    if case == "e":
        cond["dc"] |= box(X, Z, 0.0, X_WIN, Z_AU, Z_AU + 0.06)                 # ITO on D2, tied to centre DC
    if has_al:
        cond["gnd"] = Z <= L["z_al"] + tol
    elif case == "a":
        cond["gnd"] = Z <= L["z_gnd_a"] + tol
    else:
        cond["gnd"] = Z <= Z_BACK + tol
    cond["gnd"] |= (Z >= Z_TOP - tol) | (X >= X_MAX - tol)                      # far boundary at 0 V
    if ito_x is not None:
        cond["ito"] = box(X, Z, 0.0, ito_x, L["z_ito_bot"], Z_D2)
    if wires_on:
        w = np.zeros_like(X, bool)
        for k in range(int(X_WIN / WIRE_P)):
            x0 = k * WIRE_P + (WIRE_P - WIRE_W) / 2
            w |= box(X, Z, x0, x0 + WIRE_W, L["z_nw_bot"], L["z_nw_top"])
        cond["wires"] = w
    return xs, zs, L, eps, cond


def laplacian(xs, zs, eps):
    """Finite-volume matrix K with (K phi)_p = sum_q w_pq (phi_p - phi_q) = Q_p / eps0 (per unit length)."""
    nx, nz = len(xs), len(zs)
    dx, dz = np.diff(xs), np.diff(zs)
    idx = np.arange(nx * nz).reshape(nx, nz)
    A = eps * dz[None, :] / 2                    # half cell heights x eps, for x-directed faces
    wx = np.zeros((nx - 1, nz))
    wx[:, 1:] += A
    wx[:, :-1] += A
    wx /= dx[:, None]
    B = eps * dx[:, None] / 2                    # half cell widths x eps, for z-directed faces
    wz = np.zeros((nx, nz - 1))
    wz[1:, :] += B
    wz[:-1, :] += B
    wz /= dz[None, :]
    p = np.concatenate([idx[:-1, :].ravel(), idx[:, :-1].ravel()])
    q = np.concatenate([idx[1:, :].ravel(), idx[:, 1:].ravel()])
    w = np.concatenate([wx.ravel(), wz.ravel()])
    K = sp.coo_matrix((np.concatenate([w, w, -w, -w]), (np.concatenate([p, q, p, q]), np.concatenate([p, q, q, p]))),
                      shape=(nx * nz, nx * nz)).tocsr()
    return K


def solve(K, fixed, values_list):
    """Solve for the free nodes for one or more sets of fixed-node values (one factorisation)."""
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
    """Charge per unit length (C/m) on the nodes in mask, for the half domain x >= 0."""
    return EPS0 * float((K @ phi)[mask.ravel()].sum())


def run_case(case, st=STACK):
    """Field at the nanowire plane (no wires) and charge on the wires, both per volt on the RF."""
    res = dict(case=case)
    for wires_on in (False, True):
        xs, zs, L, eps, cond = build_case(case, st, wires_on)
        K = laplacian(xs, zs, eps)
        fixed = np.zeros((len(xs), len(zs)), bool)
        for m in cond.values():
            fixed |= m
        v_rf = np.where(cond["rf"], 1.0, 0.0)
        if case == "d":                        # floating ITO: superpose RF=1 and ITO=1 solutions
            phi_a, phi_b = solve(K, fixed, [v_rf, np.where(cond["ito"], 1.0, 0.0)])
            v_f = -charge(K, phi_a, cond["ito"]) / charge(K, phi_b, cond["ito"])
            phi = phi_a + v_f * phi_b
            res["V_ITO_float_per_V" + ("_wires" if wires_on else "")] = v_f
        else:
            (phi,) = solve(K, fixed, [v_rf])
        P = phi.reshape(len(xs), len(zs))
        if not wires_on:
            j = int(np.argmin(np.abs(zs - L["z_nw"])))
            Ez = (P[:, j + 1] - P[:, j - 1]) / (zs[j + 1] - zs[j - 1])
            Ex = np.gradient(P[:, j], xs)
            E = np.hypot(Ex, Ez) * 1e6           # V/m per V
            inwin = xs <= X_WIN
            res.update(E_max=float(E[inwin].max()), E_mean=float(E[inwin].mean()), E_x0=float(E[0]),
                       E_profile=(xs[xs <= 30], E[xs <= 30]))
            res["C_rf_per_rail_pF_per_mm"] = charge(K, phi, cond["rf"]) * 1e12 * 1e-3
            if "ito" in cond:
                q_ito = charge(K, phi, cond["ito"])            # (negative) charge on ITO, C/m per V
                res["C_rf_to_ito_per_rail_pF_per_mm"] = -q_ito * 1e12 * 1e-3
                # lateral current in the ITO sheet if it is grounded at x = 0..X_C (vias under the
                # centre DC): K(x) = omega V * (charge on ITO beyond x); P' = 1/2 R_s int K^2 dx
                node_q = EPS0 * (K @ phi).reshape(len(xs), len(zs)) * cond["ito"]
                qx = -node_q.sum(axis=1)                       # C/m per V at each x column
                beyond = np.cumsum(qx[::-1])[::-1]             # charge between x and the ITO edge
                Ksheet = OMEGA * V_RF * beyond                 # A per metre of trap length
                Ksheet[xs <= X_C] = 0.0
                integral = np.sum(0.5 * (Ksheet[1:] ** 2 + Ksheet[:-1] ** 2) * np.diff(xs) * 1e-6)
                res["ito_P_per_mm_per_Rs_W"] = float(0.5 * integral * 1e-3)   # W per mm per (Ohm/sq)
            if case in ("b", "c1"):
                res["phi_map"] = (xs, zs, P)
        else:
            q = charge(K, phi, cond["wires"])                  # half domain, per V
            res["C_RN_per_um_fF"] = -2 * q * 1e15 * 1e-6       # both halves, fF per um of length
            res["C_RN_fF"] = res["C_RN_per_um_fF"] * L_DET
            res["I_pk_uA"] = OMEGA * V_RF * res["C_RN_fF"] * 1e-15 * 1e6
            res["I_todaro_conditions_uA"] = 2 * np.pi * TODARO["f"] * TODARO["V"] * res["C_RN_fF"] * 1e-15 * 1e6
            # charge on each wire (fF/um per V) to show where pickup comes from
            node_q = EPS0 * (K @ phi).reshape(len(xs), len(zs)) * cond["wires"]
            colq = -node_q.sum(axis=1) * 1e15 * 1e-6
            centres = np.arange(int(X_WIN / WIRE_P)) * WIRE_P + WIRE_P / 2
            per_wire = [colq[(xs > c - WIRE_P / 2) & (xs < c + WIRE_P / 2)].sum() for c in centres]
            res["wire_profile"] = (centres, np.array(per_wire))
    return res


# ------------------------------------------------------------------ run all cases
CASES = ["a", "a2", "b", "c1", "c2", "d", "e"]
LABEL = {"a": "a: no Al, gnd 1 um below", "a2": "a2: no Al, Si substrate", "b": "b: Al only",
         "c1": "c1: Al + ITO |x|<=25 gnd", "c2": "c2: Al + ITO under RF gnd", "d": "d: Al + ITO floating",
         "e": "e: Al + ITO on D2 (no etch)"}
res = {c: run_case(c) for c in CASES}
st66 = dict(STACK, t_sp=0.066)
res66 = {c: run_case(c, st66) for c in ("b", "c1", "e")}

# ------------------------------------------------------------------ figures
fig, axs = plt.subplots(1, 3, figsize=(16, 4.6))
for c in CASES:
    x, E = res[c]["E_profile"]
    axs[0].semilogy(x, np.maximum(E, 1e-1), label=LABEL[c])
    xw, qw = res[c]["wire_profile"]
    axs[1].semilogy(xw, np.maximum(qw, 1e-9), ".", ms=3, label=LABEL[c])
axs[0].axvline(X_WIN, color="0.5", lw=0.8, ls="--")
axs[0].set(xlabel="x (um)", ylabel="|E| at the nanowire plane (V/m per V of RF)",
           title="RF field at the NbN plane (no wires; floor 0.1)")
axs[1].set(xlabel="wire position x (um)", ylabel="charge on wire per V (fF/um)", title="pickup per wire (floor 1e-9)")
names = [c for c in CASES]
I = [res[c]["I_pk_uA"] for c in names]
axs[2].bar(range(len(names)), np.maximum(I, 1e-4), color="C0")  # shielded cases are numerically zero; drawn at the floor
axs[2].set_yscale("log")
axs[2].set_ylim(1e-4, 100)
axs[2].axhspan(*I_SW, color="C3", alpha=0.15, label="NbN Isw estimate 15-20 uA")
axs[2].axhline(TODARO["I1_uA"], color="k", ls="--", lw=0.8, label="Todaro I1 = 3.5 uA")
axs[2].set_xticks(range(len(names)), names)
axs[2].set(ylabel="upper bound on induced RF current (uA)", title=f"omega V C_RN, {V_RF:g} V at {F_RF/1e6:g} MHz")
for a_ in axs:
    a_.grid(alpha=0.3, which="both")
axs[0].legend(fontsize=7)
axs[2].legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "rf_pickup.png"), dpi=150)

fig, axs = plt.subplots(1, 2, figsize=(12, 4.2))
for a_, c in zip(axs, ("b", "c1")):
    xs, zs, P = res[c]["phi_map"]
    m = (xs <= 35)
    k = (zs >= -17.5) & (zs <= 2)
    im = a_.pcolormesh(xs[m], zs[k], np.log10(np.maximum(P[m][:, k].T, 1e-6)), shading="auto", vmin=-5, vmax=0)
    a_.set(xlabel="x (um)", ylabel="z (um)", title=f"log10 phi (RF = 1 V), case {LABEL[c]}")
    fig.colorbar(im, ax=a_)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "potential.png"), dpi=150)

# ------------------------------------------------------------------ summary
def clean(r):
    return {k: v for k, v in r.items() if k not in ("E_profile", "wire_profile", "phi_map")}


summary = dict(inputs=dict(V_RF=V_RF, f_RF=F_RF, stack_um=STACK, L_det_um=L_DET, rail_len_um=RAIL_LEN,
                           Isw_estimate_uA=I_SW, todaro=TODARO),
               cases={c: clean(res[c]) for c in CASES}, spacer_66nm={c: clean(r) for c, r in res66.items()})
# RF capacitance and ITO dissipation for the whole rail length (two rails)
cb, ca2, cc2 = (res[c]["C_rf_per_rail_pF_per_mm"] for c in ("b", "a2", "c2"))
summary["rf_capacitance"] = dict(
    per_rail_pF_per_mm=dict(with_Al=cb, without_Al_Si=ca2, ITO_under_rail=cc2),
    both_rails_total_pF=dict(with_Al=2 * cb * RAIL_LEN / 1e3, without_Al_Si=2 * ca2 * RAIL_LEN / 1e3),
    displacement_current_both_rails_mA=dict(with_Al=OMEGA * V_RF * 2 * cb * RAIL_LEN / 1e3 * 1e-12 * 1e3,
                                           without_Al_Si=OMEGA * V_RF * 2 * ca2 * RAIL_LEN / 1e3 * 1e-12 * 1e3),
    c2_rail_to_ITO_pF_per_mm=res["c2"]["C_rf_to_ito_per_rail_pF_per_mm"],
    c1_rail_to_ITO_pF_per_mm=res["c1"]["C_rf_to_ito_per_rail_pF_per_mm"],
    ITO_dissipation_mW_per_mm_both_rails={f"Rs={rs}": 2 * res[c]["ito_P_per_mm_per_Rs_W"] * rs * 1e3
                                          for c in ("c2",) for rs in (40, 400)},
    ITO_dissipation_c1_mW_per_mm_both_rails={f"Rs={rs}": 2 * res["c1"]["ito_P_per_mm_per_Rs_W"] * rs * 1e3
                                             for rs in (40, 400)})
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(summary, fh, indent=1)

print(f"V_RF = {V_RF} V at {F_RF/1e6} MHz; stack {STACK}; detector length {L_DET} um")
print(f"{'case':30s} {'E_max V/m/V':>12s} {'E(x=0)':>10s} {'C_RN fF':>10s} {'I_pk uA':>10s} {'I@Todaro':>9s}")
for c in CASES:
    r = res[c]
    print(f"{LABEL[c]:30s} {r['E_max']:12.3g} {r['E_x0']:10.3g} {r['C_RN_fF']:10.3g} {r['I_pk_uA']:10.3g} "
          f"{r['I_todaro_conditions_uA']:9.3g}")
print("spacer 66 nm instead of 234 nm:")
for c, r in res66.items():
    print(f"  {LABEL[c]:28s} E_max {r['E_max']:.3g}  C_RN {r['C_RN_fF']:.3g} fF  I_pk {r['I_pk_uA']:.3g} uA")
print("floating ITO potential (case d) per V of RF:", res["d"].get("V_ITO_float_per_V"))
print("RF capacitance:", json.dumps(summary["rf_capacitance"], indent=1))
