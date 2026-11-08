"""14 - Do the staircase fingers + lead tracks change the DC electrodes? (Claude-authored; DESIGN_LOG step 20)

On the real die every outer DC electrode continues as a full-width finger up to its own lead track
(make_chip.py), so neighbouring segments end 12 um apart in height and 6 um tracks run above them.
Three layouts, same method (gds2itvg device-stack model, unit potentials evaluated at the RF null):

  FW  electrode repo example (../../electrode/examples/fivewire): five identical 120 um fingers per side,
      rectangles of equal depth, guard ring. The known reference: RF null 67.2 um (electrode RESULTS.md).
  U   trap_die_v3_UNIFORM (make_chip.py --uniform, sim reference only): our trap, every outer DC electrode a
      plain 200 um deep rectangle, no leads, ground fill around it. This is a five-wire built the FW way.
  S   trap_die_v3_NODET: the real die, staircase fingers and leads.

Checks:
  1. RF null height at the centre of each layout (FW: compare 67.2 um).
  2. Translation symmetry: identical segments must give phi_k(c_k + u) = phi_{k+1}(c_{k+1} + u) along the
     axis. Max mismatch over u in +-3 pitches, relative to the peak. Ends (caps, finite length) break it a
     little even for identical segments, so FW and U set the floor that S is compared against.
  3. Top/bottom mirror: phi_top(x, y, z) = phi_bottom(-x, y, z).
  4. S vs U directly, per segment at its own centre: phi, axial curvature d2phi/dy2 and vertical field
     dphi/dz (the three things the DC solve uses most), relative difference.
The zone solves and transport of U vs S come from 12_final_chip_check.py (out/12_log_v3_UNIFORM.txt,
out/12_log_v3_NODET_rerun.txt); this script reads both summaries and prints the differences.

Outputs: sim/out/14_staircase_check/summary.json, profiles.png
Usage:   ./run.sh 14_staircase_check.py      (run 12_final_chip_check.py on UNIFORM and NODET first)
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
from gds2itvg import Layout, build_electrodes, unit_potentials
from gds2itvg.analysis import rf_null

import trapcalc as tc

HERE = os.path.dirname(os.path.abspath(__file__))
GDSDIR = os.path.join(HERE, "..", "gds")
FWDIR = os.path.join(HERE, "..", "..", "..", "electrode", "examples", "fivewire")
OUT = os.path.join(HERE, "out", "14_staircase_check")
os.makedirs(OUT, exist_ok=True)

# name: (gds, layout json, RF electrode, top segment names, bottom segment names, segment centres (ITVG y), pitch, ion_box)
OUR_TOP = [str(3 + k) for k in range(15)]
OUR_BOT = [str(18 + k) for k in range(15)]
OUR_C = [-1000.0 + 100.0 * k for k in range(15)]             # ITVG y = GDS x - 300; centres -700 ... +700 GDS
CASES = {
    "FW": (os.path.join(FWDIR, "fivewire.gds"), os.path.join(FWDIR, "fivewire.json"), "16",
           ["1", "2", "3", "4", "5"], ["6", "7", "8", "9", "10"], [-248.0, -124.0, 0.0, 124.0, 248.0], 124.0,
           (-20, 20, -700, 700)),
    "U": (os.path.join(GDSDIR, "trap_die_v3_UNIFORM.gds"), os.path.join(GDSDIR, "trap_die_v3_UNIFORM_sim.json"), "1",
          OUR_TOP, OUR_BOT, OUR_C, 100.0, (-20, 20, -1300, 700)),
    "S": (os.path.join(GDSDIR, "trap_die_v3_NODET.gds"), os.path.join(GDSDIR, "trap_die_v3_NODET_sim.json"), "1",
          OUR_TOP, OUR_BOT, OUR_C, 100.0, (-20, 20, -1300, 700)),
}

res, prof = {}, {}
for tag, (gds, js, rf, top, bot, cen, p, box) in CASES.items():
    lay = Layout.from_json(js)
    els = build_electrodes(gds, lay, ion_box=box, ion_z=(25, 90))
    r = rf_null(els, [rf], y=0.0, z_range=(15, 150))
    x0, z0 = r["x"], r["z"]
    # 2. profiles along the axis, u = y - c_k in +-3 pitches
    u = np.linspace(-3 * p, 3 * p, 121)
    pts = np.array([[x0, c + uu, z0] for c in cen for uu in u])
    v = unit_potentials({n: els[n] for n in top}, pts)
    phi = {n: np.asarray(v[n]).reshape(len(cen), len(u))[k] for k, n in enumerate(top)}
    inner = range(1, len(top) - 2)                               # pairs (k, k+1) away from the ends
    trans = [float(np.abs(phi[top[k]] - phi[top[k + 1]]).max() / phi[top[k]].max()) for k in inner]
    # 3. mirror: top segment at (x0, y, z0) vs bottom segment at (-x0, y, z0)
    mid = len(top) // 2
    ptsm = np.array([[-x0, cen[mid] + uu, z0] for uu in u])
    mir = float(np.abs(np.asarray(unit_potentials({bot[mid]: els[bot[mid]]}, ptsm)[bot[mid]]) - phi[top[mid]]).max()
                / phi[top[mid]].max())
    # 4. value, d2/dy2, d/dz at each segment's own centre
    at = []
    for c, n in zip(cen, top):
        T = tc.taylor_all({n: els[n]}, np.array([x0, c, z0]))
        f, g, H = T[n]
        at.append(dict(phi=float(f), d2y=float(H[1, 1]), dz=float(g[2])))
    res[tag] = dict(null_x=float(x0), null_z=float(z0), translation_mismatch=trans, mirror_mismatch=mir, at_centre=at)
    prof[tag] = (u, phi, top)
    print(f"{tag}: RF null x = {x0:.3f}, z = {z0:.2f} um; translation mismatch (interior pairs) "
          f"max {max(trans):.2e}, median {np.median(trans):.2e}; top/bottom mirror {mir:.1e}")

# S vs U per segment
d = {}
for key in ("phi", "d2y", "dz"):
    s = np.array([a[key] for a in res["S"]["at_centre"]])
    uu = np.array([a[key] for a in res["U"]["at_centre"]])
    d[key] = ((s - uu) / np.abs(uu)).tolist()
print("\nS vs U at each top segment's centre (relative difference, S/U - 1):")
print(" seg  y_ITVG   phi        d2phi/dy2  dphi/dz    phi_U")
for k in range(15):
    print(f" {OUR_TOP[k]:>3s} {OUR_C[k]:7.0f}  {d['phi'][k]:+.2e}  {d['d2y'][k]:+.2e}  {d['dz'][k]:+.2e}  "
          f"{res['U']['at_centre'][k]['phi']:.4f}")
res["S_vs_U_relative"] = d
prof_max = max(np.abs(prof["S"][1][n] - prof["U"][1][n]).max() / prof["U"][1][n].max() for n in OUR_TOP)
res["S_vs_U_profile_max_relative"] = float(prof_max)
print(f"max |phi_S - phi_U| along any profile, relative to peak: {prof_max:.2e}")

# zone solves and transport from 12_final_chip_check.py
sm = {t: json.load(open(os.path.join(HERE, "out", "12_final_chip", f"trap_die_v3_{n}", "summary.json")))
      for t, n in (("U", "UNIFORM"), ("S", "NODET"))}
print("\nzone solves (12_final_chip_check.py), U vs S:")
for z in ("loading", "readout"):
    a, b = sm["U"][z], sm["S"][z]
    print(f" {z:8s} null z {a['null_z']:.3f} / {b['null_z']:.3f} um; DC freqs {a['dc_freqs_MHz']} / {b['dc_freqs_MHz']} MHz; "
          f"max|V| {a['vmax']} / {b['vmax']} V; tilt {a['radial_axis_angle_deg']} / {b['radial_axis_angle_deg']} deg")
    common = sorted(set(a["V"]) | set(b["V"]), key=int)
    dv = max(abs(a["V"].get(n, 0.0) - b["V"].get(n, 0.0)) for n in common)
    print(f"          largest single-electrode voltage difference {dv:.3f} V")
    res[f"zone_{z}"] = dict(U=a, S=b, max_dV=dv)
ta, tb = sm["U"]["transport"], sm["S"]["transport"]
print(f" transport max|V| {ta['max_abs_V']:.2f} / {tb['max_abs_V']:.2f} V; max step {ta['max_step_change_V']:.3f} / "
      f"{tb['max_step_change_V']:.3f} V")
wa = np.genfromtxt(os.path.join(HERE, "out", "12_final_chip", "trap_die_v3_UNIFORM", "waveforms.csv"), delimiter=",", names=True)
wb = np.genfromtxt(os.path.join(HERE, "out", "12_final_chip", "trap_die_v3_NODET", "waveforms.csv"), delimiter=",", names=True)
dw = max(np.abs(wa[n] - wb[n]).max() for n in wa.dtype.names[1:])
print(f" largest transport waveform difference, any electrode, any step: {dw:.3f} V")
res["transport"] = dict(U=ta, S=tb, max_waveform_dV=float(dw))

with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(res, fh, indent=1)

fig, axs = plt.subplots(1, 3, figsize=(16, 4))
for tag in ("FW", "U"):
    u, phi, top = prof[tag]
    for n in top[1:-1]:
        axs[0].plot(u, phi[n] / phi[n].max(), lw=0.8, color="C0" if tag == "FW" else "C1")
axs[0].set(xlabel="y - segment centre (um)", ylabel="phi / peak", title="interior segment profiles: FW (blue), U (orange)")
u, phiS, _ = prof["S"]
for n in OUR_TOP:
    axs[1].plot(u, (phiS[n] - prof["U"][1][n]) / prof["U"][1][n].max(), lw=0.8, label=n)
axs[1].set(xlabel="y - segment centre (um)", ylabel="(phi_S - phi_U) / peak", title="staircase die minus uniform, per segment")
axs[1].legend(fontsize=6, ncol=3)
for key, lab in (("phi", "phi"), ("d2y", "d2phi/dy2"), ("dz", "dphi/dz")):
    axs[2].plot(OUR_C, d[key], "o-", ms=3, label=lab)
axs[2].set(xlabel="segment centre, ITVG y (um)", ylabel="S/U - 1", title="at each segment centre")
axs[2].legend(fontsize=7)
for a in axs:
    a.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "profiles.png"), dpi=140)
