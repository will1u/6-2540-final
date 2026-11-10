"""12 - Final check on the fabrication GDS itself (default input gds/trap_die_v4_A30_sim.json, which names the layer-50 GDS it reads).

Single source of truth: the exported chip is read back with gds2itvg (device-stack 'profile'
model; the window floor enters as a fill of the centre DC electrode, see make_chip.py).
  1. RF null height and RF-only frequencies along the axis from beyond the loading zone to beyond
     the readout zone (and the RF-rail ends)
  2. DC solutions at the loading zone (the _zones entry in the layout JSON, 480 um left of readout on v4) and readout zone: zero field, axial
     f_ax, radial-mode tilt, |V| <= DC_LIMIT, using the N_ACTIVE electrodes nearest the ion
  3. Transport loading -> readout in 10 um steps (single-position solve per step, as in
     workflow.ipynb; no trajectory optimisation): voltage waveforms, axial frequency, height
  4. The 3-D recess correction at the readout window is added to the reported readout height. It is
     looked up by the window size in the layout JSON ("_window") from sim/04b's results for that floor
     (v3: bare oxide; 30 x 30 -> -1.38 um, 30 x 60 -> -2.50 um; v4: mirror_t6 / mirror_t1, the grounded
     floor over the local mirror for E2 / E1; no window -> 0).
Writes gridfiles-free outputs: sim/out/12_final_chip/ (labels.png, null.png, waveforms.png,
waveforms.csv, summary.json).
Usage: ./run.sh 12_final_chip_check.py [path/to/chip_sim.json] [--centre-dc-zero]
"""

import csv
import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from gds2itvg import Layout, build_electrodes
from gds2itvg.analysis import rf_null
from gds2itvg.plot import label_map

import trapcalc as tc

HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
JS = ARGS[0] if ARGS else os.path.join(HERE, "..", "gds", "trap_die_v4_A30_sim.json")
LAYOUT = json.load(open(JS))
# v4 layouts name the GDS to simulate ("_gds": the A30 _simfloor.gds adds the grounded window floor)
GDS = os.path.join(os.path.dirname(JS), LAYOUT["_gds"]) if "_gds" in LAYOUT else JS.replace("_sim.json", ".gds")
# --centre-dc-zero: hold the centre DC (electrode 2) at 0 V in every solve (DESIGN_LOG step 25). On the v4 A30
# die the lead slot and the grounded window floor give electrode 2 a strong axial ripple, so any voltage on it
# makes the transport waveforms rough; at 0 V the slot, leads and window floor are all at the same potential.
FIX2 = "--centre-dc-zero" in sys.argv
TAG = os.path.basename(JS).replace("_sim.json", "") + ("_V2zero" if FIX2 else "")
OUT = os.path.join(HERE, "out", "12_final_chip", TAG)
os.makedirs(OUT, exist_ok=True)

V_RF, F_RF = 53.0, tc.F_RF
F_AX = 0.8e6
DC_LIMIT = 10.0
N_ACTIVE = 14
ZONES = LAYOUT["_zones"]
X_LOAD, X_READ = ZONES["loading_itvg_y"], ZONES["readout_itvg_y"]      # ITVG y (= GDS x - x_read)
WIN = LAYOUT.get("_window", {"wx": 30.0, "wy": 30.0, "floor": "ito6"})   # v2 layouts: ITO-on-D2 30 x 30
if WIN["wx"] > 0:
    case = f"{WIN['wy']:g}x{WIN['wx']:g} {WIN['floor']}"                     # 04b names: radial x axial
    DH_RECESS = json.load(open(os.path.join(HERE, "out", "04b_window_3d", f"summary_{WIN['floor']}.json")))[case]["dh"][0]
else:
    case, DH_RECESS = "no window", 0.0
print(f"3-D recess correction ({case}): {DH_RECESS:+.2f} um")
TILT_DEG = 10.0

lay = Layout.from_json(JS)
els, gnd = build_electrodes(GDS, lay, ion_box=(-20, 20, -900, 350), ion_z=(25, 90), return_ground=True)
label_map(els, os.path.join(OUT, "labels.png"), ground=gnd, ion_box=(-20, 20, -900, 350),
          title=f"{TAG}: electrode numbers (layer 50)")
dc_names = [n for n in els if n != "1" and not (FIX2 and n == "2")]

# 1. RF null along the axis
ys = np.arange(-2200, 1601, 50.0)          # RF rails span ITVG y = -2300 ... +1700 (U bar)
nulls = [rf_null(els, ["1"], y=float(y), z_range=(15, 150)) for y in ys]
hz = np.array([r["z"] for r in nulls])


def zone(y_ion, tilt_deg=TILT_DEG, active=None):
    """DC set at one axial position. active=None: the N_ACTIVE electrodes with the largest unit
    potential at the ion (static zones). For transport a FIXED list is passed so the minimum-norm
    solution varies smoothly with position (a changing active set makes the waveforms jump)."""
    r = rf_null(els, ["1"], y=float(y_ion), z_range=(15, 150))
    p = np.array([r["x"], y_ion, r["z"]])
    T = tc.taylor_all(els, p)
    phi_ion = {n: abs(T[n][0]) for n in dc_names}
    if active is None:
        active = sorted(dc_names, key=lambda n: -phi_ion[n])[:N_ACTIVE]
    # first solve without tilt to get the radial curvature split, then rotate by tilt_deg
    V0, info0 = tc.solve_dc(T, ["1"], active, f_axial=F_AX, v_rf=V_RF, f_rf=F_RF, dc_limit=DC_LIMIT)
    K = info0["K"]
    dk = K[2, 2] - K[0, 0]
    kxz = 0.5 * np.tan(2 * np.deg2rad(tilt_deg)) * dk / tc.E / 1e12
    V, info = tc.solve_dc(T, ["1"], active, f_axial=F_AX, v_rf=V_RF, f_rf=F_RF, dc_limit=DC_LIMIT,
                          tilt_xz=kxz)
    _, _, Hrf = tc.sum_taylor(T, {"1": 1.0})
    f_rf, q, _ = tc.rf_hessian_to_freqs(Hrf, V_RF, F_RF)
    ev, evec = np.linalg.eigh(info["K"][np.ix_([0, 2], [0, 2])])
    ang = np.degrees(np.arctan2(evec[1, 0], evec[0, 0]))
    return dict(y=y_ion, x=r["x"], z=r["z"], V={n: V.get(n, 0.0) for n in dc_names}, info=info,
                f_rf=np.sort(f_rf), q=q.max(), tilt_angle=ang)


summary = {}
for name, y in (("loading", X_LOAD), ("readout", X_READ)):
    zr = zone(y)
    i = zr["info"]
    summary[name] = dict(y=y, null_z=zr["z"], null_x=zr["x"], rf_only_MHz=(zr["f_rf"] / 1e6).round(3).tolist(),
                         q=round(float(zr["q"]), 3), dc_freqs_MHz=(i["freqs"] / 1e6).round(3).tolist(),
                         f_axial_MHz=round(i["f_axial"] / 1e6, 3), vmax=round(i["vmax"], 2),
                         bounded=bool(i["bounded"]), residual_field_V_per_um=float(i["residual_field"]),
                         radial_axis_angle_deg=round(float(zr["tilt_angle"]), 1),
                         V={k: round(v, 3) for k, v in zr["V"].items() if abs(v) > 1e-6})
    print(f"{name:8s} y={y:7.0f}: null z = {zr['z']:.2f} um (x {zr['x']:.2f}); RF-only {zr['f_rf'][1:]/1e6} MHz, "
          f"q = {zr['q']:.3f}; DC freqs {np.round(i['freqs']/1e6,3)} MHz; |V|max {i['vmax']:.2f} V; "
          f"bounded {i['bounded']}; radial axes at {zr['tilt_angle']:.1f} deg")
summary["readout"]["null_z_with_recess"] = summary["readout"]["null_z"] + DH_RECESS
summary["readout"]["recess_case"], summary["readout"]["dh_recess"] = case, DH_RECESS

# 3. transport: fixed electrode set (all DC electrodes), no radial tilt while moving; the 10 deg
#    tilt is added only once the ion sits in a zone (the tilt set can be ramped in separately)
ty = np.arange(X_LOAD, X_READ + 1, 10.0)
waves, fax, hh, vmx, bnd = [], [], [], [], []
for y in ty:
    zr = zone(y, tilt_deg=0.0, active=dc_names)
    waves.append([zr["V"][n] for n in dc_names])
    fax.append(zr["info"]["f_axial"] / 1e6)
    hh.append(zr["z"])
    vmx.append(zr["info"]["vmax"])
    bnd.append(zr["info"]["bounded"])
waves = np.array(waves)
jump = np.abs(np.diff(waves, axis=0)).max()
summary["transport"] = dict(step_um=10.0, n_steps=len(ty), max_abs_V=float(np.abs(waves).max()),
                            max_step_change_V=float(jump), any_bounded=bool(any(bnd)),
                            f_axial_range_MHz=[float(min(fax)), float(max(fax))],
                            height_range_um=[float(min(hh)), float(max(hh))])
print(f"transport: {len(ty)} steps, max |V| {np.abs(waves).max():.2f} V, max change per 10 um step "
      f"{jump:.3f} V, axial {min(fax):.3f}-{max(fax):.3f} MHz, height {min(hh):.2f}-{max(hh):.2f} um, "
      f"bounded steps: {sum(bnd)}")
with open(os.path.join(OUT, "waveforms.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["y_um"] + [f"V{n}" for n in dc_names])
    for y, row in zip(ty, waves):
        w.writerow([y] + [f"{v:.5f}" for v in row])

fig, axs = plt.subplots(1, 3, figsize=(16, 4))
axs[0].plot(ys, hz, "o-", ms=3)
axs[0].axvline(X_LOAD, color="g", ls="--", label="loading")
axs[0].axvline(X_READ, color="r", ls="--", label="readout (planar model)")
axs[0].plot([X_READ], [summary["readout"]["null_z_with_recess"]], "rv", label="readout incl. 3-D recess")
axs[0].set(xlabel="axial position (um)", ylabel="RF null height (um)", title="RF null along the chip axis")
axs[0].legend(fontsize=7)
for j, n in enumerate(dc_names):
    if np.abs(waves[:, j]).max() > 0.05:
        axs[1].plot(ty, waves[:, j], label=n)
axs[1].set(xlabel="ion position (um)", ylabel="V (V)", title="transport waveforms (loading -> readout)")
axs[1].legend(fontsize=6, ncol=3)
axs[2].plot(ty, fax, label="axial (MHz)")
axs[2].plot(ty, np.array(hh) / 50, label="height / 50 um")
axs[2].set(xlabel="ion position (um)", title="axial frequency and height during transport")
axs[2].legend(fontsize=7)
for a in axs:
    a.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "transport.png"), dpi=140)
summary["null_along_axis"] = dict(y=ys.tolist(), z=hz.tolist())
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(summary, fh, indent=1, default=float)
