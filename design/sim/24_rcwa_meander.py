"""24 - rigorous check of the NbN meander absorption at 493 nm, RCWA with grcwa (Claude-authored).

Question: how much 493 nm light does the NbN nanowire grating absorb in the NbN, compared with the
effective-medium (EMT) transfer-matrix value used in 09c and 15b? RCWA treats the 130 nm / 200 nm grating
exactly, with no effective medium. The EMT value is the check.

Model (normal incidence, 493 nm, from vacuum; top to bottom):
  vacuum / SiO2 cap (80 nm, and 100-220 nm in 10 nm steps) / NbN grating 7 nm
  (lines 130 nm wide on a 200 nm period, fill 0.65, SiO2 between the lines) / SiO2 spacer 238 nm /
  Al 150 nm / SiO2 1000 nm / Si (semi-infinite).
  Lines run along y (the grating is periodic along x). E along y = "along the wires", E along x = "across".
  Indices are copied from 09c line 31 (not retyped). Al and the substrate stack as in 09c (T_AL 150, T_THERM 1000).
  15b used Al 450 nm; the Al is opaque at 493 nm (k 5.245), so this should not change the NbN value (run 2 tests it).
  Quantity: fraction of the incident power absorbed in the NbN grating layer only.
  Absorbed in a layer = (net downward Poynting flux at its top - at its bottom) / incident flux.

Methods used:
  - EMT and TMM: copy of 09c tmm_A (scalar epsilons) and 09c wires() (harmonic mean across the wires,
    arithmetic mean along them). The uniform-film TMM is the same routine with fill 1.0.
  - grcwa 0.1.2 (rcwa env), source read at
    C:/Users/willi/anaconda3/envs/rcwa/Lib/site-packages/grcwa/rcwa.py:
      obj.__init__ (line 6)          time convention exp(-i omega t); lengths in nm, freq = 1/493 nm
      obj.Add_LayerUniform (54)      uniform layers, complex epsilon
      obj.Add_LayerGrid (64)         patterned layer: Nx x Ny grid, one epsilon per pixel
      obj.Init_Setup (82)            reciprocal lattice (Gmethod 0 = circular truncation)
      obj.GridLayer_geteps (158)     Fourier transform of the grid (flat array, reshaped to Nx x Ny)
      obj.MakeExcitationPlanewave (125)  p_amp/s_amp: s = H_x amplitude (E along y), p = H_y (E along x) at phi = 0
      obj.GetAmplitudes (243)        field amplitudes at a given depth inside a layer
      obj.Solve_FieldFourier (264)   E field components of the zero order, used for the polarisation check
      GetZPoyntingFlux (module function, line 540)  forward and backward Poynting flux of a layer
    Not used: obj.Volume_integral (line 314) and RT_Solve (line 219), which gives the same R and T as the
    flux method below (cross-checked by the energy sum).
  - Harmonics: the grating is uniform along y. The second lattice vector is P2 = 1 nm, so the circular
    truncation keeps only orders with G_y = 0 (asserted in the code). The harmonic count is the grcwa nG,
    which it returns as complete shells (odd numbers). The loop requests nG and records the value returned.
  - Polarisation check: the transmitted zero-order field, from obj.Solve_FieldFourier, must be along y for
    s-excitation and along x for p-excitation.

Setup (one time):
  conda create -n rcwa python=3.11
  pip install grcwa
Run (from Git Bash):
  cd design/sim && ELECTRODE_ENV="$(cygpath -u "$(conda info --base)")/envs/rcwa" ./run.sh 24_rcwa_meander.py

Inputs: design/sim/out/09c_localmirror_optics/summary.json is not read; the TMM uses the constants below.
  design/sim/out/15b_collection_v4/summary.json (normal_incidence) is the EMT reference for run 2.
Outputs: design/sim/out/24_rcwa_meander/summary.json and table.md.

Limitations:
  - The grating is sampled on 1000 pixels per 200 nm period (0.2 nm pixels). The 0.65 fill edge is exact
    (650 pixels). Other pixel counts are not tested.
  - Convergence is judged on the NbN absorption only, with a change below 0.001 between the last two harmonic settings (requests 5 to 201).
  - The Al thickness is 150 nm as in 09c, not the 450 nm of 15b (opaque at 493 nm).
  - Numbers are not compared with any measurement. The 1e-9 floor on layer absorption is a numerical
    round-off allowance for the SiO2 layers (k = 0), not a physical threshold.
"""

import json
import os

import numpy as np
import grcwa
from grcwa.rcwa import GetZPoyntingFlux

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "24_rcwa_meander")
os.makedirs(OUT, exist_ok=True)
REF_15B = os.path.join(HERE, "out", "15b_collection_v4", "summary.json")

LAM = 493.0
NK = dict(SiO2=1.463, Si=4.333 + 0.048j, Al=0.605 + 5.245j, NbN=2.109 + 1.997j)   # copied from 09c line 31
T_NBN, FILL, PERIOD = 7.0, 0.65, 200.0
T_SPACER, T_AL, T_THERM = 238.0, 150.0, 1000.0          # spacer as the v4 readout stack; Al and oxide as 09c
NX = 1000                                               # pixels per period; 650 = 0.65 * 1000 is exact
P2 = 1.0                                                # second lattice vector (nm), see docstring
TOL_HARM = 0.001                                        # tightened from 0.005: across the wires the value drifts slowly with the harmonic count
NG_REQUESTS = [5, 9, 21, 57, 101, 151, 201]             # requested harmonic counts (grcwa returns nG <= request)
RUN3_CAPS = [80.0, 160.0]
SCAN_CAPS = [float(c) for c in np.arange(100.0, 221.0, 10.0)]
ALL_CAPS = sorted(set(RUN3_CAPS + SCAN_CAPS))
ENERGY_TOL = 1e-3
ABS_FLOOR = -1e-9


def eps(name):
    return NK[name] ** 2


def emt(f):
    """09c wires(): across the wires = harmonic mean (first component), along the wires = arithmetic mean."""
    ew, eh = eps("NbN"), eps("SiO2")
    return 1.0 / (f / ew + (1 - f) / eh), f * ew + (1 - f) * eh


def tmm_absorption(layers, eps_sub):
    """Per-layer absorbed fraction at normal incidence from vacuum. layers = [(eps, d nm), ...] top to bottom.
    Copy of 09c tmm_A with scalar epsilons."""
    k0 = 2 * np.pi / LAM
    E, H = 1.0 + 0j, np.sqrt(eps_sub + 0j)
    flux = [np.real(E * np.conj(H))]
    for e, d in reversed(layers):
        kz = np.sqrt(e + 0j)
        if kz.imag < 0:
            kz = -kz
        c, s = np.cos(k0 * kz * d), np.sin(k0 * kz * d)
        E, H = c * E - 1j * s / kz * H, -1j * kz * s * E + c * H
        flux.append(np.real(E * np.conj(H)))
    flux = flux[::-1]
    a_in = (E + H) / 2
    return [(flux[j] - flux[j + 1]) / np.abs(a_in) ** 2 for j in range(len(layers))]


def tmm_nbn(cap, wire_eps):
    """NbN absorption by TMM for a given wire epsilon (EMT component, or NbN for the uniform film)."""
    layers = [(eps("SiO2"), cap), (wire_eps, T_NBN), (eps("SiO2"), T_SPACER), (eps("Al"), T_AL),
              (eps("SiO2"), T_THERM)]
    return tmm_absorption(layers, eps("Si"))[1]


def net_flux(obj, ai, bi, idx):
    """Net downward power flux (forward + backward, signed) of the layer idx, for amplitudes ai, bi."""
    f, b = GetZPoyntingFlux(ai, bi, obj.omega, obj.kp_list[idx], obj.phi_list[idx], obj.q_list[idx])
    return float(np.real(f + b))


def rcwa_run(cap, pol, n_req, fill):
    """One grcwa solve. pol 'along' = E along y (s excitation), 'across' = E along x (p excitation)."""
    obj = grcwa.obj(n_req, [PERIOD, 0.0], [0.0, P2], 1.0 / LAM, 0.0, 0.0, verbose=0)
    obj.Add_LayerUniform(0.0, 1.0 + 0j)                 # layer 0: vacuum (incidence), thickness 0
    obj.Add_LayerUniform(cap, eps("SiO2"))              # cap
    obj.Add_LayerGrid(T_NBN, NX, 1)                     # layer 2: NbN grating
    obj.Add_LayerUniform(T_SPACER, eps("SiO2"))
    obj.Add_LayerUniform(T_AL, eps("Al"))
    obj.Add_LayerUniform(T_THERM, eps("SiO2"))
    obj.Add_LayerUniform(0.0, eps("Si"))                # substrate, thickness 0
    obj.Init_Setup(Gmethod=0)
    assert np.all(obj.G[:, 1] == 0), "orders with G_y != 0 found; P2 is too small"
    n_nbn = int(round(fill * NX))
    ep = np.where(np.arange(NX) < n_nbn, eps("NbN"), eps("SiO2")).astype(complex)
    obj.GridLayer_geteps(ep)
    if pol == "along":
        obj.MakeExcitationPlanewave(0.0, 0.0, 1.0, 0.0)
    else:
        obj.MakeExcitationPlanewave(1.0, 0.0, 0.0, 0.0)
    last = obj.Layer_N - 1

    # incident flux: forward part of a0 alone (normalisation)
    zero = 0 * obj.a0
    fi = float(np.real(GetZPoyntingFlux(obj.a0, zero, obj.omega, obj.kp_list[0], obj.phi_list[0],
                                        obj.q_list[0])[0]))
    ai0, bi0 = obj.GetAmplitudes(0, 0.0)
    f0, b0 = GetZPoyntingFlux(ai0, bi0, obj.omega, obj.kp_list[0], obj.phi_list[0], obj.q_list[0])
    R = float(-np.real(b0)) / fi
    aN, bN = obj.GetAmplitudes(last, 0.0)
    T = net_flux(obj, aN, bN, last) / fi
    A = {}
    for k in range(1, last):
        top = obj.GetAmplitudes(k, 0.0)
        bot = obj.GetAmplitudes(k, obj.thickness_list[k])
        A[k] = (net_flux(obj, top[0], top[1], k) - net_flux(obj, bot[0], bot[1], k)) / fi
    # polarisation check: zero-order field of the transmitted wave
    E_comp, _ = obj.Solve_FieldFourier(last, 0.0)
    ex0, ey0 = abs(E_comp[0][0]), abs(E_comp[1][0])
    return dict(nG=int(obj.nG), R=R, T=T, A_nbn=float(A[2]), A_layers=[float(A[k]) for k in sorted(A)],
                energy_sum=R + T + float(sum(A.values())), ey_over_ex=float(ey0 / max(ex0, 1e-300)))


def converge(cap, pol, fill):
    """Increase the harmonic request until the NbN absorption changes by < TOL_HARM between the last two settings."""
    seq = []
    prev = None
    for n_req in NG_REQUESTS:
        r = rcwa_run(cap, pol, n_req, fill)
        seq.append(dict(n_request=n_req, nG=r["nG"], A_nbn=r["A_nbn"]))
        if prev is not None and abs(r["A_nbn"] - prev["A_nbn"]) < TOL_HARM:
            return r, seq, True
        prev = r
    return r, seq, False


print("TMM / EMT / uniform-film references")
uniform_tmm, emt_tmm = {}, {}
for cap in ALL_CAPS:
    uniform_tmm[cap] = tmm_nbn(cap, eps("NbN"))
    e_across, e_along = emt(FILL)
    emt_tmm[cap] = dict(along=tmm_nbn(cap, e_along), across=tmm_nbn(cap, e_across))
    emt_tmm[cap]["unpol"] = 0.5 * (emt_tmm[cap]["along"] + emt_tmm[cap]["across"])
print("  EMT indices (eps): across %s, along %s" % (np.round(emt(FILL)[0], 4), np.round(emt(FILL)[1], 4)))
print("  NbN eps = %s, SiO2 eps = %s" % (np.round(eps("NbN"), 4), np.round(eps("SiO2"), 4)))

print("\nRun 1: uniform NbN film, 7 nm, RCWA vs TMM")
run1 = {}
for cap in RUN3_CAPS:
    run1[cap] = {}
    for pol in ("along", "across"):
        r, seq, ok = converge(cap, pol, 1.0)
        run1[cap][pol] = dict(A_rcwa=r["A_nbn"], A_tmm=uniform_tmm[cap], nG=r["nG"], converged=ok,
                              sequence=seq, energy_sum=r["energy_sum"], R=r["R"], T=r["T"],
                              ey_over_ex=r["ey_over_ex"], A_layers=r["A_layers"])
        rel = abs(r["A_nbn"] - uniform_tmm[cap]) / uniform_tmm[cap]
        print("  cap %3.0f %-6s RCWA %.5f  TMM %.5f  rel %.2e  nG %d" % (cap, pol, r["A_nbn"], uniform_tmm[cap], rel, r["nG"]))

print("\nRun 2: EMT in TMM vs 15b normal_incidence")
with open(REF_15B) as fh:
    ref15 = json.load(fh)["normal_incidence"]
run2 = {}
for cap in RUN3_CAPS:
    ref = ref15["%g" % cap]
    run2[str(int(cap))] = dict(tmm=emt_tmm[cap], ref_15b=dict(
        unpol=ref["unpol"], along=[ref["linear"]["s_xz"], ref["linear"]["p_yz"]],
        across=[ref["linear"]["s_yz"], ref["linear"]["p_xz"]]))
    for pol in ("along", "across"):
        for v in run2[str(int(cap))]["ref_15b"][pol]:
            print("  cap %3.0f %-6s TMM %.5f  15b %.5f  rel %.2e" % (cap, pol, emt_tmm[cap][pol], v, abs(emt_tmm[cap][pol] - v) / v))
    v = ref["unpol"]
    print("  cap %3.0f %-6s TMM %.5f  15b %.5f  rel %.2e" % (cap, "unpol", emt_tmm[cap]["unpol"], v, abs(emt_tmm[cap]["unpol"] - v) / v))

print("\nRun 3: RCWA of the grating, harmonics converged")
run3 = {}
for cap in RUN3_CAPS:
    run3[str(int(cap))] = {}
    for pol in ("along", "across"):
        r, seq, ok = converge(cap, pol, FILL)
        run3[str(int(cap))][pol] = dict(A_rcwa=r["A_nbn"], nG=r["nG"], converged=ok, sequence=seq,
                                        energy_sum=r["energy_sum"], R=r["R"], T=r["T"],
                                        ey_over_ex=r["ey_over_ex"], A_layers=r["A_layers"])
        print("  cap %3.0f %-6s A %.5f  nG %d  converged %s  seq %s" %
              (cap, pol, r["A_nbn"], r["nG"], ok, [round(s["A_nbn"], 5) for s in seq]))

print("\nRun 4: cap scan, 100-220 nm, converged harmonics per case")
scan = {}
for cap in SCAN_CAPS:
    scan[str(int(cap))] = {}
    for pol in ("along", "across"):
        r, seq, ok = converge(cap, pol, FILL)
        scan[str(int(cap))][pol] = dict(A_rcwa=r["A_nbn"], nG=r["nG"], converged=ok, energy_sum=r["energy_sum"],
                                        R=r["R"], T=r["T"], ey_over_ex=r["ey_over_ex"], A_layers=r["A_layers"],
                                        sequence_len=len(seq))
    a = scan[str(int(cap))]
    a["unpol"] = dict(A_rcwa=0.5 * (a["along"]["A_rcwa"] + a["across"]["A_rcwa"]))
    print("  cap %3.0f  along %.5f (nG %d)  across %.5f (nG %d)" %
          (cap, a["along"]["A_rcwa"], a["along"]["nG"], a["across"]["A_rcwa"], a["across"]["nG"]))

# ---- summary and acceptance
run1_ok = all(
    abs(run1[c][p]["A_rcwa"] - run1[c][p]["A_tmm"]) / run1[c][p]["A_tmm"] < 0.01
    for c in RUN3_CAPS for p in ("along", "across")
)
run1_pol_ok = all(
    abs(run1[c]["along"]["A_rcwa"] - run1[c]["across"]["A_rcwa"]) / run1[c]["along"]["A_rcwa"] < 0.01
    for c in RUN3_CAPS
)
run2_ok = True
for cap in RUN3_CAPS:
    ref = ref15["%g" % cap]
    pairs = [(emt_tmm[cap]["along"], ref["linear"]["s_xz"]), (emt_tmm[cap]["along"], ref["linear"]["p_yz"]),
             (emt_tmm[cap]["across"], ref["linear"]["s_yz"]), (emt_tmm[cap]["across"], ref["linear"]["p_xz"]),
             (emt_tmm[cap]["unpol"], ref["unpol"])]
    run2_ok = run2_ok and all(abs(a - b) / b < 0.005 for a, b in pairs)
all_runs = []
for c in RUN3_CAPS:
    for p in ("along", "across"):
        all_runs.append(run1[c][p])
        all_runs.append(run3[str(int(c))][p])
for c in SCAN_CAPS:
    for p in ("along", "across"):
        all_runs.append(scan[str(int(c))][p])
energy_ok = all(abs(x["energy_sum"] - 1.0) < ENERGY_TOL for x in all_runs) and all(
    min(x["A_layers"]) > ABS_FLOOR for x in all_runs)
harm_ok = all(run3[str(int(c))][p]["converged"] for c in RUN3_CAPS for p in ("along", "across"))
acceptance = dict(
    uniform_film_matches_tmm=bool(run1_ok and run1_pol_ok),
    emt_tmm_reproduces_15b=bool(run2_ok),
    energy_conserved=bool(energy_ok),
    harmonics_converged=bool(harm_ok),
)
print("\nAcceptance:", json.dumps(acceptance))

ratio_rows = []
for c in ALL_CAPS:
    if c in RUN3_CAPS:
        rc = run3[str(int(c))]
        rcwa_along, rcwa_across = rc["along"]["A_rcwa"], rc["across"]["A_rcwa"]
    else:
        rc = scan[str(int(c))]
        rcwa_along, rcwa_across = rc["along"]["A_rcwa"], rc["across"]["A_rcwa"]
    rcwa_unpol = 0.5 * (rcwa_along + rcwa_across)
    e = emt_tmm[c]
    ratio_rows.append(dict(cap=c, polarisation="along", emt=e["along"], rcwa=rcwa_along, ratio=rcwa_along / e["along"]))
    ratio_rows.append(dict(cap=c, polarisation="across", emt=e["across"], rcwa=rcwa_across, ratio=rcwa_across / e["across"]))
    ratio_rows.append(dict(cap=c, polarisation="unpol", emt=e["unpol"], rcwa=rcwa_unpol, ratio=rcwa_unpol / e["unpol"]))

with open(os.path.join(OUT, "summary.json"), "w") as fh:
    json.dump(dict(
        inputs=dict(lam_nm=LAM, NK=dict((k, [v.real, v.imag]) for k, v in NK.items()), t_nbn=T_NBN,
                    fill=FILL, period_nm=PERIOD, t_spacer=T_SPACER, t_al=T_AL, t_therm=T_THERM,
                    grid_pixels=NX, P2_nm=P2, tol_harmonic=TOL_HARM, caps_run3=RUN3_CAPS,
                    caps_scan=SCAN_CAPS, emt_indices=dict(across=[emt(FILL)[0].real, emt(FILL)[0].imag],
                                                           along=[emt(FILL)[1].real, emt(FILL)[1].imag])),
        run1_uniform=run1, run2_emt_vs_15b=run2, run3_rcwa=run3, run4_cap_scan=scan,
        table=ratio_rows, acceptance=acceptance), fh, indent=1)

with open(os.path.join(OUT, "table.md"), "w") as fh:
    fh.write("> **Claude-authored.** NbN absorption at 493 nm, EMT (TMM) against RCWA (grcwa), normal incidence, 2026-11-10.\n\n")
    fh.write("| cap (nm) | polarisation | EMT (TMM) | RCWA | ratio (RCWA / EMT) |\n")
    fh.write("|---|---|---|---|---|\n")
    for row in ratio_rows:
        fh.write("| %g | %s | %.4f | %.4f | %.4f |\n" % (row["cap"], row["polarisation"], row["emt"], row["rcwa"], row["ratio"]))
print("wrote", os.path.join(OUT, "summary.json"), "and table.md")
