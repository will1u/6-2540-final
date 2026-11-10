"""26 - How few DC DAC channels can the v4 trap use? The 35 DC electrodes (2 = centre DC, 3-32 segments,
33-36 end caps) are grouped into channels: a tied channel is the sum of its members' (phi, grad, H), so its
voltage drives all members in the same ratio. Electrodes that are not listed are grounded (not in the solve).

Configs (channel count in brackets):
  all35 (35), caps_gnd (31), caps_gnd_tie_far (27), gnd_29, gnd_25, gnd_21.

Per config, at the loading and readout zones (RF null as sim 12):
  natural 10 deg tilt: sim 12's rule, 14 channels with the largest |phi| at the ion.
  fixed split 45 deg, df 0.1 MHz, all channels, unclipped, at 0.8 and 0.6 MHz axial (sim 25's fixed_solve).
Transport: ion from loading to readout in 10 um steps, zero tilt, all channels (centre DC held at 0 V on
window dies, DESIGN_LOG step 25), dc_limit 10 V. Max |V|, max change of any channel per step, bounded steps.

Usage: ./run.sh 26_dc_channel_count.py [path/to/chip_sim.json]   (default ../gds/trap_die_v4_A30_sim.json)
Outputs: out/26_dc_channel_count/<TAG>/summary.json, transport_maxV.png
"""

import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from gds2itvg import Layout, build_electrodes
from gds2itvg.analysis import rf_null

import trapcalc as tc

HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
JS = os.path.abspath(ARGS[0] if ARGS else os.path.join(HERE, "..", "gds", "trap_die_v4_A30_sim.json"))
LAYOUT = json.load(open(JS))
GDS = os.path.join(os.path.dirname(JS), LAYOUT["_gds"]) if "_gds" in LAYOUT else JS.replace("_sim.json", ".gds")
TAG = os.path.basename(JS).replace("_sim.json", "")
OUT = os.path.join(HERE, "out", "26_dc_channel_count", TAG)
os.makedirs(OUT, exist_ok=True)

V_RF, F_RF = 53.0, tc.F_RF
F_AX, F_AX_ALT = 0.8e6, 0.6e6
DC_LIMIT = 10.0
N_ACTIVE = 14
TILT_DEG = 10.0
DF = 0.1e6
M = tc.M_BA138
WINDOW = LAYOUT.get("_window", {}).get("wx", 0) > 0     # window dies: centre DC held at 0 V in transport
ZONES = LAYOUT["_zones"]
X_LOAD, X_READ = ZONES["loading_itvg_y"], ZONES["readout_itvg_y"]

lay = Layout.from_json(JS)
els, _ = build_electrodes(GDS, lay, ion_box=(-20, 20, -900, 350), ion_z=(25, 90), return_ground=True)
ELEC = [str(i) for i in range(2, 37)]              # the 35 DC electrodes
assert all(n in els for n in ELEC), [n for n in ELEC if n not in els]

# ---- channel configurations: a list of channels, each a list of electrode names
CAPS = ["33", "34", "35", "36"]
TIES_FAR = [["3", "18"], ["4", "19"], ["17", "32"], ["16", "31"]]


def singles(removed):
    """One channel per electrode not in `removed` (removed electrodes are grounded)."""
    return [[e] for e in ELEC if e not in removed]


CONFIGS = {
    "all35": singles([]),
    "caps_gnd": singles(CAPS),
    "caps_gnd_tie_far": TIES_FAR + singles(CAPS + sum(TIES_FAR, [])),
    "gnd_29": singles(CAPS + ["3", "18"]),
    "gnd_25": singles(CAPS + ["3", "18", "4", "19", "17", "32"]),
    "gnd_21": singles(CAPS + ["3", "18", "4", "19", "5", "20", "17", "32", "16", "31"]),
}


def channel_taylor(T, chans):
    """Taylor data per channel name ("3+18" for a tied pair). A tied channel is the sum of its members."""
    out = {}
    for ch in chans:
        out["+".join(ch)] = (sum(T[e][0] for e in ch), sum(T[e][1] for e in ch), sum(T[e][2] for e in ch))
    out["1"] = T["1"]
    return out


def solve(Tc, active, fax, tilt=0.0, extra=None, dc_limit=DC_LIMIT):
    return tc.solve_dc(Tc, ["1"], active, f_axial=fax, v_rf=V_RF, f_rf=F_RF,
                       dc_limit=dc_limit, tilt_xz=tilt, extra_rows=extra)


def natural10(Tc, active):
    # sim 12 rule: untilted solve, set the tilt from K[2,2] - K[0,0], re-solve
    _, info0 = solve(Tc, active, F_AX)
    dk = info0["K"][2, 2] - info0["K"][0, 0]
    kxz = 0.5 * np.tan(2 * np.deg2rad(TILT_DEG)) * dk / tc.E / 1e12
    return solve(Tc, active, F_AX, tilt=kxz)[1]


def fixed45(Tc, active, fax, KPSI, dc_limit):
    # sim 25 fixed_solve: mean radial frequency from the untilted clipped solve, then target a 45 deg split
    _, info0 = solve(Tc, active, fax)
    fbar = np.sort(info0["freqs"])[1:].mean()
    f1, f2 = fbar + DF / 2, fbar - DF / 2
    dK = M * (2 * np.pi) ** 2 * (f1 ** 2 - f2 ** 2)
    th = np.deg2rad(45.0)
    hxz = (0.5 * dK * np.sin(2 * th) - KPSI[0, 2]) / (tc.E * 1e12)
    hdiff = (dK * np.cos(2 * th) - (KPSI[0, 0] - KPSI[2, 2])) / (tc.E * 1e12)
    row = np.array([[Tc[n][2][0, 0] - Tc[n][2][2, 2] for n in active]])
    return solve(Tc, active, fax, tilt=hxz, extra=(row, np.array([hdiff])), dc_limit=dc_limit)[1]


summary = {c: dict(n_channels=len(chs), zones={}, transport={}) for c, chs in CONFIGS.items()}
for zname, y in (("loading", X_LOAD), ("readout", X_READ)):
    r = rf_null(els, ["1"], y=float(y), z_range=(15, 150))
    T = tc.taylor_all(els, np.array([r["x"], y, r["z"]]))
    _, _, Hrf = tc.sum_taylor(T, {"1": 1.0})
    _, _, KPSI = tc.rf_hessian_to_freqs(Hrf, V_RF, F_RF)
    for cname, chs in CONFIGS.items():
        Tc = channel_taylor(T, chs)
        names = ["+".join(ch) for ch in chs]
        phi = {n: abs(Tc[n][0]) for n in names}
        active14 = sorted(names, key=lambda n: -phi[n])[:N_ACTIVE]
        info = natural10(Tc, active14)
        z = {"natural10": dict(vmax=float(info["vmax"]), bounded=bool(info["bounded"]),
                               freqs_MHz=(info["freqs"] / 1e6).round(3).tolist(),
                               f_axial_MHz=float(info["f_axial"] / 1e6))}
        for fax, key in ((F_AX, "fixed45_0.8MHz"), (F_AX_ALT, "fixed45_0.6MHz")):
            iu = fixed45(Tc, names, fax, KPSI, dc_limit=1e9)
            z[key] = dict(vmax_unclipped=float(iu["vmax"]), f_axial_MHz=float(iu["f_axial"] / 1e6))
        summary[cname]["zones"][zname] = z
        print(f"{zname:8s} {cname:18s} natural10 vmax {z['natural10']['vmax']:.2f} "
              f"bounded {z['natural10']['bounded']}; 45deg unc 0.8 {z['fixed45_0.8MHz']['vmax_unclipped']:.2f}, "
              f"0.6 {z['fixed45_0.6MHz']['vmax_unclipped']:.2f}")

# ---- transport: one taylor_all per position, reused for every config
ty = np.arange(X_LOAD, X_READ + 1, 10.0)
tr = {c: dict(V=[], fax=[], bnd=[], names=["+".join(ch) for ch in chs]) for c, chs in CONFIGS.items()}
for y in ty:
    r = rf_null(els, ["1"], y=float(y), z_range=(15, 150))
    T = tc.taylor_all(els, np.array([r["x"], y, r["z"]]))
    for cname, chs in CONFIGS.items():
        Tc = channel_taylor(T, chs)
        names = tr[cname]["names"]
        active = [n for n in names if not (WINDOW and n == "2")]
        V, info = solve(Tc, active, F_AX)
        tr[cname]["V"].append([V.get(n, 0.0) for n in names])
        tr[cname]["fax"].append(info["f_axial"] / 1e6)
        tr[cname]["bnd"].append(bool(info["bounded"]))

for cname in CONFIGS:
    W = np.array(tr[cname]["V"])
    summary[cname]["transport"] = dict(
        n_steps=len(ty), max_abs_V=float(np.abs(W).max()),
        max_step_V=float(np.abs(np.diff(W, axis=0)).max()),
        bounded_steps=int(sum(tr[cname]["bnd"])),
        f_axial_MHz=[float(min(tr[cname]["fax"])), float(max(tr[cname]["fax"]))])
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(dict(die=TAG, window=WINDOW, configs=summary), fh, indent=1)

# ---- table
hdr = (f"{'config':18s} {'n':>3s} {'L 10deg':>8s} {'R 10deg':>8s} {'L45@.8':>8s} {'R45@.8':>8s} "
       f"{'L45@.6':>8s} {'R45@.6':>8s} {'maxV':>7s} {'maxstep':>8s} {'bnd':>4s} {'f_ax range':>13s}")
print(hdr)
for c, s in summary.items():
    zl, zr = s["zones"]["loading"], s["zones"]["readout"]
    t = s["transport"]
    print(f"{c:18s} {s['n_channels']:3d} {zl['natural10']['vmax']:8.2f} {zr['natural10']['vmax']:8.2f} "
          f"{zl['fixed45_0.8MHz']['vmax_unclipped']:8.2f} {zr['fixed45_0.8MHz']['vmax_unclipped']:8.2f} "
          f"{zl['fixed45_0.6MHz']['vmax_unclipped']:8.2f} {zr['fixed45_0.6MHz']['vmax_unclipped']:8.2f} "
          f"{t['max_abs_V']:7.2f} {t['max_step_V']:8.3f} {t['bounded_steps']:4d} "
          f"{t['f_axial_MHz'][0]:6.3f}-{t['f_axial_MHz'][1]:6.3f}")

# ---- plot: transport max |V| and max step per config
names_c = list(CONFIGS)
x = np.arange(len(names_c))
w = 0.38
fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(x - w / 2, [summary[c]["transport"]["max_abs_V"] for c in names_c], w, label="max |V| over transport (V)")
ax.bar(x + w / 2, [summary[c]["transport"]["max_step_V"] for c in names_c], w, label="max change per 10 um step (V)")
ax.axhline(DC_LIMIT, color="k", ls="--", lw=1, label="10 V limit")
ax.set_xticks(x)
ax.set_xticklabels([f"{c}\n({summary[c]['n_channels']} ch)" for c in names_c], fontsize=8)
ax.set(ylabel="V", title=f"{TAG}: transport voltages vs channel count")
ax.grid(alpha=0.3, axis="y")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "transport_maxV.png"), dpi=140)
