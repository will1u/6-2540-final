"""13 - Can the DC electrodes put the ion back at 50 um over the readout window? (Claude-authored;
DESIGN_LOG step 19)

Background. The ion's height is set by the RF null: the point where the RF field vanishes. Only the
RF electrode geometry (and the grounded metal around it) sets where that is; DC voltages add a static
potential, they cannot move the place where the RF field is zero. What a DC field CAN do is push the
ion away from the null, like a spring: displacement = force / stiffness. The ion then sits where the
RF field is not zero, so it is driven at the RF frequency (excess micromotion). This script measures
how much DC that takes and what the micromotion is.

Method (planar gds2itvg model of the v3 die, readout zone, ITVG frame: x radial, y axial, z height):
  1. Same DC set as sim 12 (0.8 MHz axial, the 14 electrodes nearest the ion), for two radial tilts: 0 and
     10 deg. Solved WITHOUT the +-10 V clip so the reported max |V| is the true cost (sim 12 clips at 10 V;
     with the open bare-SiO2 window the 10 deg tilt alone already needs 13-15 V, DESIGN_LOG step 19).
  2. For a wanted upward shift dz, the force needed is F = K . (0, 0, dz), with K the full 3x3 stiffness
     (RF pseudopotential + DC curvature; the tilt couples x and z, so F has an x part too). The DC
     gradient at the null is set to -F/e (trapcalc.solve_dc grad_target); repeated 3 times because K
     depends slightly on the voltages.
  3. Check: minimise the full energy U = Psi_RF + e*phi_DC in (x, z) to get the real ion position.
  4. At that position: RF field amplitude E_RF = V_RF |grad phi_RF|, micromotion amplitude
     a = e E_RF / (m Omega^2), and modulation index beta = k a for a 493 nm beam with k along the
     micromotion (worst case; in-plane beams have k_z = 0 and barely see vertical micromotion).
Swept dz = 0 ... 3 um. The window drop to undo comes from sim 04b (bare-oxide floor): -1.38 um
(A30, 30 x 30) and -2.50 um (B60, 30 x 60). The planar model does not contain the drop itself, so the
spring constant and RF gradient are those of the unperturbed trap (fine for a few-um shift).

Outputs: sim/out/13_dc_height_tuning/summary.json, dc_height.png
Usage:   ./run.sh 13_dc_height_tuning.py            (A30 and B60)
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
from gds2itvg import Layout, build_electrodes, unit_potentials
from gds2itvg.analysis import rf_null
from scipy.optimize import minimize

import trapcalc as tc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "13_dc_height_tuning")
os.makedirs(OUT, exist_ok=True)

V_RF, F_RF = 53.0, tc.F_RF
OM = 2 * np.pi * F_RF
F_AX, DAC, N_ACTIVE, TILTS = 0.8e6, 10.0, 14, (0.0, 10.0)
DC_LIMIT = 1e9                             # no clipping; compare max |V| with the DAC range afterwards
LAM = 493e-9
DZ = np.arange(0.0, 3.01, 0.25)           # wanted upward shift (um)
DH_WINDOW = {}
for k, case in (("A30", "30x30 oxide"), ("B60", "30x60 oxide")):
    DH_WINDOW[k] = json.load(open(os.path.join(HERE, "out", "04b_window_3d", "summary_oxide.json")))[case]["dh"][0]


def rf_grad(els, p, h=0.25):
    """grad phi_RF (per um, per V) at p by central differences."""
    pts = [np.array(p) + s * h * e for e in np.eye(3) for s in (1, -1)]
    v = np.asarray(unit_potentials({"1": els["1"]}, np.array(pts))["1"])
    return np.array([(v[2 * i] - v[2 * i + 1]) / (2 * h) for i in range(3)])


def energy_eV(els, V, p):
    """Ion energy (eV): RF pseudopotential + DC potential, at point p (um)."""
    phi = unit_potentials({n: els[n] for n in V}, np.array([p]))
    dc = sum(V[n] * float(np.asarray(phi[n])[0]) for n in V)
    return float(tc.pseudo_eV(rf_grad(els, p), V_RF, F_RF)) + dc


summary = {}
fig, axs = plt.subplots(1, 3, figsize=(16, 4.2))
for die in ("A30", "B60"):
    js = os.path.join(HERE, "..", "gds", f"trap_die_v3_{die}_sim.json")
    lay = Layout.from_json(js)
    els = build_electrodes(js.replace("_sim.json", ".gds"), lay, ion_box=(-20, 20, -200, 200), ion_z=(25, 90))
    dc_names = [n for n in els if n != "1"]
    r = rf_null(els, ["1"], y=0.0, z_range=(15, 150))
    p0 = np.array([r["x"], 0.0, r["z"]])
    T = tc.taylor_all(els, p0)
    active = sorted(dc_names, key=lambda n: -abs(T[n][0]))[:N_ACTIVE]
    V0, info0 = tc.solve_dc(T, ["1"], active, f_axial=F_AX, v_rf=V_RF, f_rf=F_RF, dc_limit=DC_LIMIT)
    summary[die] = dict(null=p0.tolist(), window_drop_um=DH_WINDOW[die], shift_needed_um=-DH_WINDOW[die])
    for tilt in TILTS:
        kxz = 0.5 * np.tan(2 * np.deg2rad(tilt)) * (info0["K"][2, 2] - info0["K"][0, 0]) / tc.E / 1e12
        rows = []
        for dz in DZ:
            g = np.zeros(3)
            for _ in range(3):                       # K depends a little on the voltages: iterate
                V, info = tc.solve_dc(T, ["1"], active, f_axial=F_AX, v_rf=V_RF, f_rf=F_RF, dc_limit=DC_LIMIT,
                                      tilt_xz=kxz, grad_target=tuple(g))
                F = info["K"] @ np.array([0.0, 0.0, dz * 1e-6])          # N
                g = -F / tc.E * 1e-6                                       # V/um
            # real equilibrium in the radial plane (axial position y = 0)
            res = minimize(lambda q: energy_eV(els, V, [q[0], 0.0, q[1]]), [p0[0], p0[2] + dz],
                           method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-12, maxiter=400))
            p = np.array([res.x[0], 0.0, res.x[1]])
            E_rf = V_RF * np.linalg.norm(rf_grad(els, p)) * 1e6               # V/m amplitude
            a_mm = tc.E * E_rf / (tc.M_BA138 * OM ** 2)                        # m
            rows.append(dict(dz_target=float(dz), z_ion=float(p[2]), x_ion=float(p[0]), dz_achieved=float(p[2] - p0[2]),
                             vmax=info["vmax"], within_dac=bool(info["vmax"] <= DAC), E_dc_V_per_m=(-g * 1e6).tolist(),
                             E_rf_V_per_m=float(E_rf), a_mm_nm=float(a_mm * 1e9),
                             beta_493=float(2 * np.pi / LAM * a_mm), f_MHz=(info["freqs"] / 1e6).round(3).tolist(),
                             V={n: round(v, 3) for n, v in V.items()}))
            print(f"{die} tilt {tilt:2.0f} dz {dz:4.2f}: ion z {p[2]:.2f} (x {p[0]:+.2f}) um, |V|max {info['vmax']:.2f} V, "
                  f"E_dc ({-g[0]*1e6:+.0f}, {-g[2]*1e6:+.0f}) V/m, E_RF {E_rf:.0f} V/m, micromotion {a_mm*1e9:.0f} nm, "
                  f"beta(493) {2*np.pi/LAM*a_mm:.2f}")
        need = -DH_WINDOW[die]
        zs = np.array([q["dz_target"] for q in rows])
        # The pseudopotential softens above the null, so the real shift (energy minimum) exceeds the linear
        # target (e.g. 1.11 um for a 1.00 um target). Read the results off at the ACHIEVED shift.
        za = np.array([q["dz_achieved"] for q in rows])
        at = {k: float(np.interp(need, za, [q[k] for q in rows]))
              for k in ("vmax", "dz_target", "a_mm_nm", "beta_493", "E_rf_V_per_m")}
        at["E_dc_z_V_per_m"] = float(np.interp(need, za, [q["E_dc_V_per_m"][2] for q in rows]))
        summary[die][f"tilt_{tilt:g}deg"] = dict(at_needed_shift=at, sweep=rows)
        print(f"{die} tilt {tilt:g}: undoing the {DH_WINDOW[die]:+.2f} um window drop needs |V|max {at['vmax']:.2f} V "
              f"(DAC {DAC:g} V), E_dc,z {at['E_dc_z_V_per_m']:.0f} V/m; leaves E_RF {at['E_rf_V_per_m']:.0f} V/m, "
              f"micromotion {at['a_mm_nm']:.0f} nm, beta(493, k along it) {at['beta_493']:.2f}")
        ls = "-" if tilt == 0 else "--"
        lab = f"{die}, tilt {tilt:g} deg"
        axs[0].plot(zs, [q["vmax"] for q in rows], "o" + ls, ms=3, label=lab)
        axs[1].plot(zs, [q["dz_achieved"] for q in rows], "o" + ls, ms=3, label=lab)
        axs[2].plot(zs, [q["a_mm_nm"] for q in rows], "o" + ls, ms=3, label=lab)
    for a_ in axs:
        a_.axvline(-DH_WINDOW[die], ls=":", lw=0.8, color="C0" if die == "A30" else "C2")
axs[0].axhline(DAC, color="r", lw=0.8)
axs[0].set(xlabel="wanted upward shift (um)", ylabel="max |V| (V)", title="DC voltage needed (red: 10 V DAC)")
axs[1].plot(DZ, DZ, "k:", lw=0.8)
axs[1].set(xlabel="wanted upward shift (um)", ylabel="achieved shift (um)", title="check: energy minimum")
axs[2].set(xlabel="wanted upward shift (um)", ylabel="micromotion amplitude (nm)",
           title="excess micromotion (dotted: window drop to undo)")
for a_ in axs:
    a_.grid(alpha=0.3)
    a_.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "dc_height.png"), dpi=140)
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(summary, fh, indent=1, default=float)
