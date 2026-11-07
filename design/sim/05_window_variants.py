"""05 - SNSPD window: what does a missing patch of electrode metal do to the trap?

Readout zone at GDS x = 0. The detector sits below a window: a patch with no Au electrode metal.
The window is modelled purely electrostatically (no field from the SNSPD itself). Variants:

  V0  no window (reference)
  V1  window inside the centre DC electrode (wy < c), floor = grounded ITO/Al ~10 um below
  V1w window wider than the centre electrode: the centre DC is cut through (wy = c + 2g), so the
      opening reaches the RF rail edges
  V1r window cut into the RF rails as well (wy > c + 2g): the RF electrode itself is missing metal
  V2  ITO flush with the top surface and tied to the centre DC electrode: electrically = V0

For each: RF null height h(y) through the readout zone, axial pseudopotential along the ion line
(RF field along the axis at the null -> barrier and axial micromotion), RF-only radial frequencies
at the readout zone, and the DC voltages needed to hold an ion there at f_ax with zero field.

The 'profile' model treats the opening over a buried ground at ground_depth with the 2-D
cross-section correction (gds2itvg crosssection.opening_profile); 'drawn' (opening at 0 V) is run
too as a bound.

Outputs: sim/out/05_window/<variant>/..., compare.png, summary.json
"""

import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from gds2itvg import Layout, build_electrodes, unit_potentials
from gds2itvg.analysis import rf_null

import trapcalc as tc
import trapgeom

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "05_window")
os.makedirs(OUT, exist_ok=True)
V_RF, F_RF, F_AX = 53.0, tc.F_RF, 0.8e6
C, A, G = trapgeom.BASE["c"], trapgeom.BASE["a"], trapgeom.BASE["g"]
WX = float(sys.argv[1]) if len(sys.argv) > 1 else 30.0     # window length along the axis

VARIANTS = {
    "V0": None,
    "V1_wy30": dict(x=0.0, wx=WX, wy=30.0, kind="open"),
    "V1w_cut_centre": dict(x=0.0, wx=WX, wy=C + 2 * G, kind="open"),
    "V1r_into_rf": dict(x=0.0, wx=WX, wy=C + 2 * G + 20.0, kind="open"),
}
Y = np.linspace(-200, 200, 81)       # ion line through the readout zone (ITVG y = GDS x)


def window_cut_rf(P):
    """trapgeom only cuts the centre electrode; for wy > c + 2g also cut the RF rails."""
    return P["window"] and P["window"]["wy"] > C + 2 * G


def build_variant(name, win, gap_model):
    import gdstk
    P = dict(half_len=1500.0, n_seg=9, seg_x0=-(9 * 100.0 - 5.0) / 2, window=win)
    stem = os.path.join(OUT, f"{name}_{gap_model}")
    gds, js, info = trapgeom.write(stem, P, gap_model=gap_model)
    if win and window_cut_rf(P):
        # remove RF metal inside the window too, rewrite the GDS
        lib = gdstk.read_gds(gds)
        cell = lib.top_level()[0]
        hole = gdstk.rectangle((win["x"] - win["wx"] / 2, -win["wy"] / 2),
                               (win["x"] + win["wx"] / 2, win["wy"] / 2))
        polys = gdstk.boolean(cell.polygons, hole, "not", layer=trapgeom.LAYER_AU, datatype=0)
        cell.remove(*cell.polygons)
        cell.add(*polys)
        lib.write_gds(gds)
        # the centre DC is now two pieces: seed both
        lay = Layout.from_json(js)
        lay.electrodes["2"] = [[win["x"] - win["wx"] / 2 - 50, 0.0], [win["x"] + win["wx"] / 2 + 50, 0.0]]
        lay.to_json(js)
    elif win and win["wy"] >= C:
        lay = Layout.from_json(js)
        lay.electrodes["2"] = [[win["x"] - win["wx"] / 2 - 50, 0.0], [win["x"] + win["wx"] / 2 + 50, 0.0]]
        lay.to_json(js)
    lay = Layout.from_json(js)
    return build_electrodes(gds, lay, ion_box=(-20, 20, -250, 250), ion_z=(25, 80))


def analyse(els):
    nulls = [rf_null(els, ["1"], y=float(y), z_range=(15, 150)) for y in Y]
    hz = np.array([r["z"] for r in nulls])
    hx = np.array([r["x"] for r in nulls])
    # pseudopotential along the line of nulls (includes the axial RF field component)
    d = 0.05
    pts = np.column_stack([hx, Y, hz])
    grads = []
    for k in range(3):
        e = np.zeros(3)
        e[k] = d
        grads.append((unit_potentials({"1": els["1"]}, pts + e)["1"]
                      - unit_potentials({"1": els["1"]}, pts - e)["1"]) / (2 * d))
    grad = np.column_stack(grads)
    psi_line = tc.pseudo_eV(grad, V_RF, F_RF)
    i0 = int(np.argmin(np.abs(Y)))
    p = np.array([hx[i0], 0.0, hz[i0]])
    T = tc.taylor_all(els, p)
    _, _, Hrf = tc.sum_taylor(T, {"1": 1.0})
    f_rf, q, _ = tc.rf_hessian_to_freqs(Hrf, V_RF, F_RF)
    dc = [n for n in els if n != "1"]
    V, info = tc.solve_dc(T, ["1"], dc, f_axial=F_AX, v_rf=V_RF, f_rf=F_RF)
    return dict(h=hz.tolist(), x=hx.tolist(), psi_meV=(1e3 * psi_line).tolist(),
                Ey_rf_at_null=(grad[:, 1]).tolist(), h0=float(hz[i0]), f_rf_MHz=sorted((f_rf / 1e6).tolist()),
                q=float(q.max()), dc_vmax=info["vmax"], dc_freqs_MHz=(info["freqs"] / 1e6).tolist(),
                dc_bounded=info["bounded"], V={k: float(v) for k, v in V.items()})


summary = {}
for gm in ("profile", "drawn"):
    for name, win in VARIANTS.items():
        res = analyse(build_variant(name, win, gm))
        summary[f"{name}|{gm}"] = res
        print(f"[{gm:7s}] {name:16s} h(0) = {res['h0']:6.2f} um  min h = {min(res['h']):6.2f}  "
              f"Psi barrier on axis = {max(res['psi_meV']):.3f} meV  RF-only f = "
              f"{res['f_rf_MHz'][1]:.2f}/{res['f_rf_MHz'][2]:.2f} MHz  DC |V|max = {res['dc_vmax']:.2f} V")

with open(os.path.join(OUT, f"summary_wx{int(WX)}.json"), "w") as fh:
    json.dump(dict(Y=Y.tolist(), WX=WX, results=summary), fh, indent=1)

fig, axs = plt.subplots(1, 2, figsize=(12, 4))
for key, res in summary.items():
    name, gm = key.split("|")
    ls = "-" if gm == "profile" else ":"
    axs[0].plot(Y, res["h"], ls, label=key)
    axs[1].plot(Y, res["psi_meV"], ls, label=key)
axs[0].set(xlabel="axial position (um)", ylabel="RF null height (um)", title=f"window {WX:g} um long, centred at 0")
axs[1].set(xlabel="axial position (um)", ylabel="pseudopotential on the null line (meV)", yscale="symlog",
           title="axial RF barrier / micromotion")
for a in axs:
    a.grid(alpha=0.3)
    a.legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(OUT, f"compare_wx{int(WX)}.png"), dpi=150)
