"""24b - RCWA scan of the readout window stack at 493 nm, with ITO option and tolerance boxes (Claude-authored).

Question: over the v4 readout window stack, how much 493 nm light does the NbN grating absorb, how
sensitive is that to the SiO2 spacer and cap, the NbN thickness and the SiO2 index, and does a
uniform ITO layer on top help? The +-10 nm tolerance box gives the worst corner, not only the nominal.

Model (grcwa RCWA, normal incidence, 493 nm, from vacuum; top to bottom):
  vacuum / [ITO, uniform, optional] / SiO2 cap / NbN grating / SiO2 spacer / Al 150 nm / SiO2 1000 nm / Si
  NbN grating: lines 130 nm wide on a 200 nm period (fill 0.65), SiO2 between the lines (n_sio2).
  Cap, spacer, SiO2 between the lines and the bottom SiO2 all use n_sio2 (default 1.463).
  Unpolarised = mean of "along" (E along y, the wires) and "across" (E along x), each solved separately.
  Harmonics: every solve uses one fixed request of 57 (grcwa returns nG = 55). Sim 24 raised the
  request per case until the NbN absorption changed by < 0.001, which needs 101 for the "across"
  polarisation and costs about 10 s per stack on one thread, against 1.7 s at 57. With about 330
  stacks that was over an hour, so the first full run of this script was stopped (2026-11-12).
  The cost in accuracy, measured at spacer 238 / cap 160: across 0.83383 at 57 against 0.83307 at
  101 and 0.83254 at 201, so the unpolarised value is about 0.0005 high. The decision threshold of
  this script is 0.02. Step 1 checks the two sim 24 reference values at this setting.
  The NbN layer is found by position: index 2 without ITO, index 3 with ITO (layer 0 is vacuum).
  ITO index: 1.965 + 0.003j at 493 nm, the value in sim 09 (line 84). It is one literature value.
  Al 150 nm stands for any opaque Al (k 5.245 at 493 nm, so the thickness is not critical).
  Limits: normal incidence only; the grating is sampled on 1000 pixels per period; nothing is
  compared with a measurement; the tolerance box is +-10 nm on spacer and cap only, not on the wire
  width or the fill.
  Quantities: A_nbn = fraction of incident power absorbed in the NbN grating layer; A_ito = in the ITO.
  Absorbed in a layer = (net downward Poynting flux at its top - at its bottom) / incident flux.

Acceptance (step 1): spacer 238, NbN 7 nm, n 1.463, no ITO, unpolarised A_nbn must be 0.8274 at cap 160
and 0.5826 at cap 80 (+-0.002). Those are the sim 24 values (table.md, rows 160 and 80, unpol).
The script stops if they do not reproduce.

Setup (one time): conda create -n rcwa python=3.11; pip install grcwa
Run (from Git Bash):
  cd design/sim && ELECTRODE_ENV="$(cygpath -u "$(conda info --base)")/envs/rcwa" ./run.sh 24b_rcwa_stack_scan.py
Outputs: design/sim/out/24b_rcwa_stack_scan/summary.json, table.md, heatmap.png.
"""

import json
import os
import time

import numpy as np
import grcwa
from grcwa.rcwa import GetZPoyntingFlux
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "24b_rcwa_stack_scan")
os.makedirs(OUT, exist_ok=True)

LAM = 493.0
NK = dict(Si=4.333 + 0.048j, Al=0.605 + 5.245j, NbN=2.109 + 1.997j, ITO=1.965 + 0.003j)  # as sim 24 / sim 09 line 84
N_SIO2 = 1.463
T_NBN = 7.0
FILL, PERIOD = 0.65, 200.0
T_AL, T_THERM = 150.0, 1000.0
NX = 1000                       # pixels per period; 650 = 0.65 * 1000 is exact
P2 = 1.0                        # second lattice vector (nm); only G_y = 0 orders are kept (asserted)
TOL_HARM = 0.001                # same as sim 24
NG_REQUESTS = [57]              # one fixed request (see the docstring); sim 24 used 5 ... 201 per case
ENERGY_TOL = 1e-3
SIM24_REF = {160.0: 0.8274, 80.0: 0.5826}   # sim 24 table.md, unpolarised rows
SPACERS = [float(s) for s in np.arange(200, 271, 5)]   # 15 values
CAPS = [float(c) for c in np.arange(120, 201, 5)]      # 17 values
BOX_SPACERS = [float(s) for s in np.arange(220, 251, 5)]
BOX_CAPS = [float(c) for c in np.arange(140, 181, 5)]
ITO_CAPS = [float(c) for c in np.arange(60, 201, 10)]  # 15 values
ITO_T = [20.0, 50.0]
DELTA = 10.0                    # tolerance box half-width (nm)

CACHE = {}                      # solves already done, keyed by the stack parameters
ALL_ENERGY = []                 # energy sums and layer absorptions, for the check at the end


def rcwa_run(pol, n_req, cap, spacer, t_nbn, n_sio2, t_ito):
    """One grcwa solve. pol 'along' = E along y (s excitation), 'across' = E along x (p excitation)."""
    eps_sio2 = n_sio2 ** 2
    obj = grcwa.obj(n_req, [PERIOD, 0.0], [0.0, P2], 1.0 / LAM, 0.0, 0.0, verbose=0)
    obj.Add_LayerUniform(0.0, 1.0 + 0j)                       # layer 0: vacuum (incidence), thickness 0
    if t_ito > 0:
        obj.Add_LayerUniform(t_ito, NK["ITO"] ** 2)           # uniform ITO, directly under vacuum
    obj.Add_LayerUniform(cap, eps_sio2)                       # cap
    obj.Add_LayerGrid(t_nbn, NX, 1)                           # NbN grating
    obj.Add_LayerUniform(spacer, eps_sio2)
    obj.Add_LayerUniform(T_AL, NK["Al"] ** 2)
    obj.Add_LayerUniform(T_THERM, eps_sio2)
    obj.Add_LayerUniform(0.0, NK["Si"] ** 2)                  # substrate, thickness 0
    obj.Init_Setup(Gmethod=0)
    assert np.all(obj.G[:, 1] == 0), "orders with G_y != 0 found; P2 is too small"
    n_nbn = int(round(FILL * NX))
    ep = np.where(np.arange(NX) < n_nbn, NK["NbN"] ** 2, eps_sio2).astype(complex)
    obj.GridLayer_geteps(ep)
    if pol == "along":
        obj.MakeExcitationPlanewave(0.0, 0.0, 1.0, 0.0)
    else:
        obj.MakeExcitationPlanewave(1.0, 0.0, 0.0, 0.0)
    last = obj.Layer_N - 1
    k_nbn = 3 if t_ito > 0 else 2                             # NbN is after vacuum (and ITO, if present) and cap

    # incident flux: forward part of a0 alone (normalisation)
    zero = 0 * obj.a0
    fi = float(np.real(GetZPoyntingFlux(obj.a0, zero, obj.omega, obj.kp_list[0], obj.phi_list[0],
                                        obj.q_list[0])[0]))
    aN, bN = obj.GetAmplitudes(last, 0.0)
    A = {}
    for k in range(1, last):
        top = obj.GetAmplitudes(k, 0.0)
        bot = obj.GetAmplitudes(k, obj.thickness_list[k])
        f1, b1 = GetZPoyntingFlux(top[0], top[1], obj.omega, obj.kp_list[k], obj.phi_list[k], obj.q_list[k])
        f2, b2 = GetZPoyntingFlux(bot[0], bot[1], obj.omega, obj.kp_list[k], obj.phi_list[k], obj.q_list[k])
        A[k] = (float(np.real(f1 + b1)) - float(np.real(f2 + b2))) / fi
    fl, bl = GetZPoyntingFlux(aN, bN, obj.omega, obj.kp_list[last], obj.phi_list[last], obj.q_list[last])
    T = float(np.real(fl + bl)) / fi
    f0, b0 = GetZPoyntingFlux(obj.GetAmplitudes(0, 0.0)[0], obj.GetAmplitudes(0, 0.0)[1], obj.omega,
                              obj.kp_list[0], obj.phi_list[0], obj.q_list[0])
    R = float(-np.real(b0)) / fi
    return dict(nG=int(obj.nG), A_nbn=float(A[k_nbn]),
                A_ito=float(A[1]) if t_ito > 0 else None,
                A_layers=[float(A[k]) for k in sorted(A)],
                energy_sum=R + T + float(sum(A.values())))


def converge(pol, cap, spacer, t_nbn, n_sio2, t_ito):
    """Solve at each request in NG_REQUESTS (here one); "converged" is only meaningful with several."""
    seq = []
    prev = None
    for n_req in NG_REQUESTS:
        r = rcwa_run(pol, n_req, cap, spacer, t_nbn, n_sio2, t_ito)
        seq.append(dict(n_request=n_req, nG=r["nG"], A_nbn=r["A_nbn"]))
        if prev is not None and abs(r["A_nbn"] - prev["A_nbn"]) < TOL_HARM:
            return r, seq, True
        prev = r
    return r, seq, False


def point(cap, spacer, t_nbn=T_NBN, n_sio2=N_SIO2, t_ito=0.0):
    """Unpolarised result for one stack, cached. Both polarisations use the fixed harmonic request."""
    key = (round(cap, 3), round(spacer, 3), round(t_nbn, 3), round(n_sio2, 5), round(t_ito, 3))
    if key in CACHE:
        return CACHE[key]
    res = {}
    for pol in ("along", "across"):
        r, seq, ok = converge(pol, cap, spacer, t_nbn, n_sio2, t_ito)
        res[pol] = dict(A_nbn=r["A_nbn"], A_ito=r["A_ito"], nG=r["nG"], converged=ok, sequence=seq)
        ALL_ENERGY.append((r["energy_sum"], min(r["A_layers"])))
    res["A_nbn"] = 0.5 * (res["along"]["A_nbn"] + res["across"]["A_nbn"])
    res["A_ito"] = None if t_ito <= 0 else 0.5 * (res["along"]["A_ito"] + res["across"]["A_ito"])
    CACHE[key] = res
    return res


def box(s, c):
    """+-DELTA box around (s, c): 9 points. Returns mean, worst corner and the point list."""
    pts = []
    for ds in (-DELTA, 0.0, DELTA):
        for dc in (-DELTA, 0.0, DELTA):
            pts.append([s + ds, c + dc, point(c + dc, s + ds)["A_nbn"]])
    v = [p[2] for p in pts]
    return dict(s=s, c=c, mean=float(np.mean(v)), worst=float(min(v)), points=pts)


# ---- step 1: acceptance
print("STEP 1: acceptance (spacer 238, NbN 7 nm, n 1.463, no ITO)")
t0 = time.time()
rcwa_run("along", 9, 160.0, 238.0, T_NBN, N_SIO2, 0.0)
dt = time.time() - t0
print("  one grcwa solve (request 9): %.3f s" % dt)
acc = {}
for cap in (160.0, 80.0):
    p = point(cap, 238.0)
    acc[str(int(cap))] = dict(
        harmonic_sequence={pol: p[pol]["sequence"] for pol in ("along", "across")},
        nG={pol: p[pol]["nG"] for pol in ("along", "across")},
        converged={pol: p[pol]["converged"] for pol in ("along", "across")},
        A_along=p["along"]["A_nbn"], A_across=p["across"]["A_nbn"], A_unpol=p["A_nbn"],
        sim24_unpol=SIM24_REF[cap], diff=abs(p["A_nbn"] - SIM24_REF[cap]))
    print("  cap %3.0f: along %.5f (request %d, nG %d)  across %.5f (request %d, nG %d)"
          % (cap, p["along"]["A_nbn"], p["along"]["sequence"][-1]["n_request"], p["along"]["nG"],
             p["across"]["A_nbn"], p["across"]["sequence"][-1]["n_request"], p["across"]["nG"]))
    print("           unpol %.5f   sim 24 %.4f   |diff| %.5f   harmonic sequences %s"
          % (p["A_nbn"], SIM24_REF[cap], abs(p["A_nbn"] - SIM24_REF[cap]),
             {pol: [(s["n_request"], s["nG"]) for s in p[pol]["sequence"]] for pol in ("along", "across")}))
acc_ok = all(v["diff"] <= 0.002 for v in acc.values())
print("  acceptance within +-0.002: %s" % acc_ok)
if not acc_ok:
    raise SystemExit("ACCEPTANCE FAILED: physics does not reproduce sim 24; stop here")

# ---- step 2: grid
print("\nSTEP 2: grid, spacer %g..%g step 5 x cap %g..%g step 5" % (SPACERS[0], SPACERS[-1], CAPS[0], CAPS[-1]))
grid = np.zeros((len(CAPS), len(SPACERS)))
t0 = time.time()
for i, c in enumerate(CAPS):
    for j, s in enumerate(SPACERS):
        grid[i, j] = point(c, s)["A_nbn"]
print("  grid done in %.1f s; min %.4f max %.4f" % (time.time() - t0, grid.min(), grid.max()))

# heat map
fig, ax = plt.subplots(figsize=(7.5, 5.5))
im = ax.imshow(grid, origin="lower", aspect="auto", cmap="viridis",
               extent=[SPACERS[0] - 2.5, SPACERS[-1] + 2.5, CAPS[0] - 2.5, CAPS[-1] + 2.5])
cb = fig.colorbar(im, ax=ax)
cb.set_label("NbN absorption at 493 nm")
ax.set_xlabel("SiO2 spacer (nm)")
ax.set_ylabel("SiO2 cap over the wires (nm)")
ax.plot([238], [160], marker="x", color="white", markersize=10, markeredgewidth=2)
ax.annotate("238 / 160: %.3f" % point(160.0, 238.0)["A_nbn"], (238, 160), xytext=(6, 6),
            textcoords="offset points", color="white", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "heatmap.png"), dpi=150)
plt.close(fig)

# ---- step 3: tolerance boxes
print("\nSTEP 3: +-10 nm tolerance boxes")
boxes_all = []
for s in BOX_SPACERS:
    for c in BOX_CAPS:
        boxes_all.append(box(s, c))
boxes_all.sort(key=lambda b: -b["worst"])
top5 = boxes_all[:5]
print("  top 5 nominals by worst corner (spacer, cap, box mean, worst):")
for b in top5:
    print("    %g / %g   mean %.4f   worst %.4f" % (b["s"], b["c"], b["mean"], b["worst"]))
best = top5[0]

nom = box(238.0, 160.0)
print("  238/160 box (spacer rows 228, 238, 248 x cap cols 150, 160, 170):")
for ds in (-DELTA, 0.0, DELTA):
    row = [point(160.0 + dc, 238.0 + ds)["A_nbn"] for dc in (-DELTA, 0.0, DELTA)]
    print("    spacer %g: %s" % (238.0 + ds, "  ".join("%.4f" % v for v in row)))
print("  238/160 box mean %.4f  worst corner %.4f" % (nom["mean"], nom["worst"]))
diff_z = best["worst"] - nom["worst"]
decision = ("238/160 worst corner %.4f; best worst corner %.4f at %g/%g; difference %.4f"
            % (nom["worst"], best["worst"], best["s"], best["c"], diff_z))
print("  DECISION: " + decision + ("; Z <= 0.02: %s" % (diff_z <= 0.02)))

# ---- step 4: sensitivities at 238/160
print("\nSTEP 4: sensitivities at spacer 238, cap 160 (unpolarised A_nbn)")
base = point(160.0, 238.0)["A_nbn"]
sens = dict(base=base, nbn_thickness={}, sio2_index={})
for t in (6.0, 7.0, 8.0):
    sens["nbn_thickness"][str(int(t))] = point(160.0, 238.0, t_nbn=t)["A_nbn"]
    print("  NbN %g nm: %.4f" % (t, sens["nbn_thickness"][str(int(t))]))
for n in (1.45, 1.463, 1.48):
    sens["sio2_index"][str(n)] = point(160.0, 238.0, n_sio2=n)["A_nbn"]
    print("  n_SiO2 %g: %.4f" % (n, sens["sio2_index"][str(n)]))

ito = {}
print("  no ITO scan (cap 60..200 step 10, spacer 238):")
noito = [(c, point(c, 238.0)["A_nbn"]) for c in ITO_CAPS]
nbest = max(noito, key=lambda x: x[1])
print("    " + "  ".join("%g:%.4f" % (c, v) for c, v in noito))
print("    best cap %g, A_nbn %.4f; at 160: %.4f" % (nbest[0], nbest[1], point(160.0, 238.0)["A_nbn"]))
ito["no_ito"] = dict(scan=[[c, v] for c, v in noito], best_cap=nbest[0], best_A=nbest[1], at160=base)
for t in ITO_T:
    rows = []
    for c in ITO_CAPS:
        p = point(c, 238.0, t_ito=t)
        rows.append([c, p["A_nbn"], p["A_ito"]])
    bestrow = max(rows, key=lambda r: r[1])
    r160 = [r for r in rows if r[0] == 160.0][0]
    ito[str(int(t))] = dict(scan=rows, at160=dict(A_nbn=r160[1], A_ito=r160[2]),
                            best=dict(cap=bestrow[0], A_nbn=bestrow[1], A_ito=bestrow[2]))
    print("  ITO %g nm: A_nbn at 160 %.4f (A_ito %.4f); best cap %g: A_nbn %.4f (A_ito %.4f)"
          % (t, r160[1], r160[2], bestrow[0], bestrow[1], bestrow[2]))
    print("    " + "  ".join("%g:%.4f/%.4f" % (r[0], r[1], r[2]) for r in rows))

# ---- checks
max_dev = max(abs(e - 1.0) for e, _ in ALL_ENERGY)
min_layer = min(m for _, m in ALL_ENERGY)
print("\nEnergy check over %d polarised solves: max |sum - 1| = %.2e, min layer absorption = %.2e"
      % (len(ALL_ENERGY), max_dev, min_layer))
assert max_dev < ENERGY_TOL, "energy not conserved"

# ---- write outputs
with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(dict(
        lam_nm=LAM, NK=dict((k, [v.real, v.imag]) for k, v in NK.items()), n_sio2_default=N_SIO2,
        t_nbn_default=T_NBN, fill=FILL, period_nm=PERIOD, t_al=T_AL, t_therm=T_THERM, grid_pixels=NX,
        tol_harmonic=TOL_HARM, ng_requests=NG_REQUESTS, solve_time_s=dt,
        acceptance=dict(ok=acc_ok, cases=acc),
        grid=dict(spacer=SPACERS, cap=CAPS, A_nbn_unpol=grid.tolist()),
        box_top5=[dict(spacer=b["s"], cap=b["c"], mean=b["mean"], worst=b["worst"]) for b in top5],
        box_238_160=nom,
        decision=dict(text=decision, worst_238_160=nom["worst"], best_worst=best["worst"],
                      best_s=best["s"], best_c=best["c"], difference=diff_z, le_0_02=bool(diff_z <= 0.02)),
        sensitivity=sens, ito=ito,
        energy=dict(max_dev=max_dev, min_layer=min_layer, n_solves=len(ALL_ENERGY))), fh, indent=1)

with open(os.path.join(OUT, "table.md"), "w") as fh:
    fh.write("> **Claude-authored.** Written by sim/24b_rcwa_stack_scan.py (regenerate, do not edit).\n\n")
    fh.write("## Acceptance (spacer 238, NbN 7 nm, n 1.463, no ITO)\n\n")
    fh.write("| cap (nm) | along | across | unpol | sim 24 unpol | abs diff | nG along | nG across |\n")
    fh.write("|---|---|---|---|---|---|---|---|\n")
    for k, v in acc.items():
        fh.write("| %s | %.5f | %.5f | %.5f | %.4f | %.5f | %d | %d |\n"
                 % (k, v["A_along"], v["A_across"], v["A_unpol"], v["sim24_unpol"], v["diff"],
                    v["nG"]["along"], v["nG"]["across"]))
    fh.write("\nSolve time (one grcwa solve, request 9): %.3f s. Every solve uses a fixed harmonic request of 57 (nG 55); "
             "the script's docstring gives the reason and the 0.0005 it costs.\n\n" % dt)
    fh.write("## Top 5 nominals by worst corner (spacer 220..250, cap 140..180, +-10 nm box)\n\n")
    fh.write("| spacer (nm) | cap (nm) | box mean | worst corner |\n|---|---|---|---|\n")
    for b in top5:
        fh.write("| %g | %g | %.4f | %.4f |\n" % (b["s"], b["c"], b["mean"], b["worst"]))
    fh.write("\n## Tolerance box at 238 / 160\n\n")
    fh.write("| spacer (nm) | cap 150 | cap 160 | cap 170 |\n|---|---|---|---|\n")
    for ds in (-DELTA, 0.0, DELTA):
        fh.write("| %g | %s |\n" % (238.0 + ds, " | ".join("%.4f" % point(160.0 + dc, 238.0 + ds)["A_nbn"]
                                                       for dc in (-DELTA, 0.0, DELTA))))
    fh.write("\nBox mean %.4f, worst corner %.4f.\n\n" % (nom["mean"], nom["worst"]))
    fh.write("**Decision:** %s; Z <= 0.02: %s.\n\n" % (decision, "yes" if diff_z <= 0.02 else "no"))
    fh.write("## Sensitivities at spacer 238, cap 160 (unpolarised A_nbn)\n\n")
    fh.write("| change | value | A_nbn |\n|---|---|---|\n")
    for t in ("6", "7", "8"):
        fh.write("| NbN thickness %s nm | | %.4f |\n" % (t, sens["nbn_thickness"][t]))
    for n in ("1.45", "1.463", "1.48"):
        fh.write("| SiO2 index | %s | %.4f |\n" % (n, sens["sio2_index"][n]))
    fh.write("\n## ITO on top (spacer 238, cap 60..200 step 10)\n\n")
    fh.write("| cap (nm) | no ITO A_nbn | ITO 20 nm A_nbn | ITO 20 nm A_ito | ITO 50 nm A_nbn | ITO 50 nm A_ito |\n")
    fh.write("|---|---|---|---|---|---|\n")
    for i, c in enumerate(ITO_CAPS):
        fh.write("| %g | %.4f | %.4f | %.4f | %.4f | %.4f |\n"
                 % (c, noito[i][1], ito["20"]["scan"][i][1], ito["20"]["scan"][i][2],
                    ito["50"]["scan"][i][1], ito["50"]["scan"][i][2]))
    fh.write("\n| case | A_nbn at 160 | A_ito at 160 | best cap | best A_nbn | A_ito at best |\n")
    fh.write("|---|---|---|---|---|---|\n")
    fh.write("| no ITO | %.4f | - | %g | %.4f | - |\n" % (base, nbest[0], nbest[1]))
    for t in ("20", "50"):
        b = ito[t]["best"]
        fh.write("| ITO %s nm | %.4f | %.4f | %g | %.4f | %.4f |\n"
                 % (t, ito[t]["at160"]["A_nbn"], ito[t]["at160"]["A_ito"], b["cap"], b["A_nbn"], b["A_ito"]))
    fh.write("\nEnergy: max |sum - 1| = %.2e over %d polarised solves.\n" % (max_dev, len(ALL_ENERGY)))
print("wrote", os.path.join(OUT, "summary.json"), os.path.join(OUT, "table.md"), os.path.join(OUT, "heatmap.png"))
