"""Report figures from existing simulation output (Claude-authored).

Plots only: axis names, tick labels, legends and short in-plot annotations. No titles, no captions.
Reads existing JSON and CSV files; runs no simulation.

Figures (one function each, written to design/figures/report/<name>.pdf and .png):
  rf_null_height           fig_rf_null_height: RF null height along the trap axis (sim 12, summary.json null_along_axis)
  transport_static         fig_transport_static: static transport voltages vs ion position (sim 12, trap_die_v4_A30_V2zero waveforms.csv)
  collection_vs_height     fig_collection_vs_height: geometric collection vs ion height (sim 17, summary.json table_A)
  termination              fig_termination: RF current through the nanowire per lead termination (sim 19, summary.json)
  stack                    fig_stack: readout-zone layer stack, final stack of 2026-11-12 (typed in the function)
  transport_waveform       fig_transport_waveform: ion position and electrode voltages vs time (sim 21, waveform.csv)
  rf_capacitance_sections  fig_rf_capacitance_sections: RF capacitance to ground per configuration (sim 22, summary.json)
The die map (die_map.pdf, .png, .svg) is made by make_die_map.py, not by this file.
Skipped: absorption_vs_cap. sim 09c summary.json keeps only the best values and band ends, not the scan
arrays, so the cap scan cannot be replotted without rerunning it (not done here).

Run: cd design/sim && ./run.sh ../figures/make_report_figures.py
"""

import csv
import json
import os
import re

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

import plotstyle as ps

HERE = os.path.dirname(os.path.abspath(__file__))
SIMOUT = os.path.join(HERE, "..", "sim", "out")
GDS = os.path.join(HERE, "..", "gds")


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def fig_rf_null_height():
    base = os.path.join(SIMOUT, "12_final_chip")
    e2 = load_json(os.path.join(base, "trap_die_v4_A30", "summary.json"))
    e1 = load_json(os.path.join(base, "trap_die_v4_A30_E1", "summary.json"))
    nd = load_json(os.path.join(base, "trap_die_v4_NODET", "summary.json"))
    zones = load_json(os.path.join(GDS, "trap_die_v4_A30_sim.json"))["_zones"]
    y = np.array(e2["null_along_axis"]["y"])
    z2 = np.array(e2["null_along_axis"]["z"])
    z1 = np.array(e1["null_along_axis"]["z"])
    zn = np.array(nd["null_along_axis"]["z"])
    assert np.array_equal(y, np.array(e1["null_along_axis"]["y"]))
    assert np.array_equal(y, np.array(nd["null_along_axis"]["y"]))
    d1, dn = np.max(np.abs(z1 - z2)), np.max(np.abs(zn - z2))
    print(f"rf_null_height: max |E1 - E2| = {d1:.3e} um, max |NODET - E2| = {dn:.3e} um")
    coincide = max(d1, dn) < 0.5   # about one line width (1.5 pt) on the axis below
    print("rf_null_height: curves coincide within the line width:", coincide)

    fig, ax = plt.subplots(figsize=(ps.W1, 2.6))
    ax.plot(y, z2, color=ps.BLUE, ls="-", marker="none",
            label="A30, E2 (E1 and NODET coincide)" if coincide else "A30, E2")
    if not coincide:
        ax.plot(y, z1, color=ps.ORANGE, ls="--", label="A30, E1")
        ax.plot(y, zn, color=ps.AQUA, ls="-.", label="NODET")
    ax.plot(0, e2["readout"]["null_z_with_recess"], marker="o", color=ps.BLUE, ls="none",
            label="A30, E2, readout with window recess")
    ax.plot(0, e1["readout"]["null_z_with_recess"], marker="D", color=ps.ORANGE, ls="none",
            label="A30, E1, readout with window recess")
    print("rf_null_height: readout recess values E2, E1 (um):",
          e2["readout"]["null_z_with_recess"], e1["readout"]["null_z_with_recess"])
    for x, lab, side, ha in [(zones["loading_itvg_y"], "loading", -1, "right"),
                             (zones["readout_itvg_y"], "readout", 1, "left")]:
        ax.axvline(x, color=ps.AXIS, lw=0.8, ls=":")
        ax.text(x + side * 30, 0.97, lab, transform=ax.get_xaxis_transform(), fontsize=8, va="top", ha=ha)
    ax.set_ylim(40, 52)
    ax.set_xlabel("axial position from the readout zone (µm)")
    ax.set_ylabel("RF null height (µm)")
    ax.legend(loc="lower right", handlelength=2.2)
    fig.tight_layout()
    ps.save(fig, "rf_null_height")
    i = len(y) // 2
    print("rf_null_height plotted points (y, z):", [(float(y[k]), float(z2[k])) for k in (0, i, -1)])
    print("rf_null_height check: from file:", [(e2["null_along_axis"]["y"][k], e2["null_along_axis"]["z"][k]) for k in (0, i, -1)])


def fig_transport_static():
    path = os.path.join(SIMOUT, "12_final_chip", "trap_die_v4_A30_V2zero", "waveforms.csv")
    with open(path, newline="") as fh:
        rows = list(csv.reader(fh))
    head = rows[0]
    data = np.array([[float(v) for v in r] for r in rows[1:]])
    y = data[:, 0]
    cols = {int(h[1:]): data[:, k] for k, h in enumerate(head) if k > 0}
    assert len(cols) == 34, len(cols)
    # electrodes 18-32 mirror 3-17 (N+15); check that numerically
    dmax = {n: float(np.max(np.abs(cols[n] - cols[n + 15]))) for n in range(3, 18)}
    print("transport_static: largest |V_N - V_(N+15)| over 3-17 (V):", round(max(dmax.values()), 5),
          "; per electrode (V):", {n: round(v, 5) for n, v in dmax.items()})
    peak = {n: float(np.max(np.abs(cols[n]))) for n in range(3, 18)}
    top4 = sorted(peak, key=lambda n: -peak[n])[:4]
    print("transport_static: top four of electrodes 3-17 by peak |V|:",
          [(n, round(peak[n], 3)) for n in top4])
    hidden = set(top4) | {n + 15 for n in top4}
    print("transport_static: max |V_N - V_(N+15)| for the four plotted (V):",
          round(max(dmax[n] for n in top4), 5))

    fig, ax = plt.subplots(figsize=(ps.W2, 2.8))
    for n, v in cols.items():
        if n not in hidden:
            ax.plot(y, v, color="#b9b7af", lw=0.5, zorder=1)
    styles = [ps.STYLE_SOLID, ps.STYLE_DASHED, ps.STYLE_DASHDOT, ps.STYLE_DOTTED]
    colours = [ps.BLUE, ps.ORANGE, ps.AQUA, ps.YELLOW]
    for k, n in enumerate(top4):
        ls, mk = styles[k]
        ax.plot(y, cols[n], color=colours[k], ls=ls, lw=1.2, label=f"electrode {n} (mirror of {n + 15})", zorder=3)
    ax.set_xlabel("ion position (µm)")
    ax.set_ylabel("electrode voltage (V)")
    ax.set_ylim(-7.0, 11.5)
    ax.set_yticks([-6, -4, -2, 0, 2, 4, 6])
    ax.legend(loc="upper center", ncol=4, handlelength=2.4, columnspacing=1.0)
    fig.tight_layout()
    ps.save(fig, "transport_static")
    k = len(y) // 2
    j_last = len(y) - 1
    print("transport_static plotted points (y, V):",
          [(float(y[j]), float(cols[top4[0]][j])) for j in (0, k, j_last)])
    print("transport_static check: from file:",
          [(float(rows[1 + j][0]), float(rows[1 + j][head.index(f"V{top4[0]}")])) for j in (0, k, j_last)])


def fig_collection_vs_height():
    s = load_json(os.path.join(SIMOUT, "17_height_tradeoff", "summary.json"))
    t = s["table_A"]
    h = np.array([r["h"] for r in t], dtype=float)
    series = [
        ("A30, E2", "A30_E2", ps.BLUE, "-", "o"),
        ("A30, E1", "A30_E1", ps.ORANGE, "-", "o"),
        ("B60, E2", "B60_E2", ps.BLUE, "--", "s"),
        ("B60, E1", "B60_E1", ps.ORANGE, "--", "s"),
    ]
    fig, ax = plt.subplots(figsize=(ps.W1, 2.6))
    for lab, key, col, ls, mk in series:
        ax.plot(h, [r[key] for r in t], color=col, ls=ls, marker=mk, ms=4, label=lab)
    ax.set_xlabel("ion height (µm)")
    ax.set_ylabel("geometric collection (%)")
    ax.legend(loc="upper right", ncol=2, handlelength=2.2)
    fig.tight_layout()
    ps.save(fig, "collection_vs_height")
    print("collection_vs_height plotted points (h, A30_E2):",
          [(float(h[j]), float(t[j]["A30_E2"])) for j in (0, 2, -1)])


def pretty_case(case):
    """Readable y label for a sim 19 case name. Same meaning, shorter text (see sim 19 build_cases)."""
    c = re.sub(r"^\d+\s+", "", case)
    m = re.match(r"^matched (\S+ nF) m=([\d.]+)$", c)
    if m:
        return f"matched {m.group(1)}, {round(float(m.group(2)) * 100):d} % mismatch"
    m = re.match(r"^B 50 ohm x \(1\+([\d.]+)\)$", c)
    if m:
        return f"50 Ω / 50 Ω, {round(float(m.group(1)) * 100):d} % mismatch"
    if c == "trap nominal":
        return "28 MHz L-C trap, nominal"
    m = re.match(r"^trap L ([+-]\d+) %$", c)
    if m:
        return f"28 MHz L-C trap, L {m.group(1).replace('-', '−')} %"
    if c == "symmetric 50 / 50":
        return "50 Ω / 50 Ω, symmetric"
    return c.replace("50 ohm", "50 Ω")


def fig_termination():
    rows = load_json(os.path.join(SIMOUT, "19_lead_termination", "summary.json"))
    rp = 0.0   # the script's headline case (A30, E2, R_pair = 0); the first listed value
    print("termination: R_pair values in file:", sorted({r["R_pair"] for r in rows}), "; plotted:", rp)
    cases = list(dict.fromkeys(r["case"] for r in rows))
    val = {}
    for r in rows:
        if r["die"] == "A30" and r["R_pair"] == rp:
            val[(r["case"], r["option"])] = r["I_nw_uA"]
    labels = [pretty_case(c) for c in cases]
    e2_raw = np.array([val[(c, "E2")] for c in cases])
    e1_raw = np.array([val[(c, "E1")] for c in cases])
    zero_rows = [i for i in range(len(cases)) if max(e2_raw[i], e1_raw[i]) < 1e-12]   # ~1e-15 uA is floating-point zero
    print("termination: rows below 1e-12 uA (zero, no bars) in both options:", [cases[i] for i in zero_rows])
    floor = 1e-4   # uA, log axis floor for the non-zero rows
    print("termination: smallest non-zero value (uA):",
          round(float(min(v for v in np.r_[e2_raw, e1_raw] if v > 0)), 6))
    ypos = np.arange(len(cases))[::-1]
    h = 0.36
    fig, ax = plt.subplots(figsize=(ps.W2, 4.6))
    keep = [i for i in range(len(cases)) if i not in zero_rows]
    ax.barh(ypos[keep] + h / 2, np.maximum(e2_raw[keep], floor), height=h * 0.9, color=ps.BLUE,
            label="E2 (6 µm Au)")
    ax.barh(ypos[keep] - h / 2, np.maximum(e1_raw[keep], floor), height=h * 0.9, color=ps.ORANGE,
            label="E1 (0.35 µm Au)")
    for i in zero_rows:
        ax.text(floor * 1.1, ypos[i], "0", va="center", ha="left", fontsize=8, color=ps.INK)
    ax.set_xscale("log")
    ax.set_xlim(floor, 10)
    ax.set_yticks(ypos)
    ax.set_yticklabels(labels)
    ax.set_xlabel("RF current through the nanowire (µA)")
    ax.grid(False)
    ax.legend(loc="lower right", handlelength=1.2)
    fig.tight_layout()
    ps.save(fig, "termination")
    print("termination labels:", labels)
    print("termination plotted (case, E2, E1) first and last:",
          (labels[0], float(e2_raw[0]), float(e1_raw[0])), (labels[-1], float(e2_raw[-1]), float(e1_raw[-1])))


def fig_stack():
    # Final stack of 2026-11-12, top to bottom (raised 100 nm Al mirror; base SiO2 1.0 um nominal).
    # Typed by hand; the values are the ones in design/fab/TRAVELER.md and design/CLAUDE.md.
    layers = [
        ("Vacuum; ion (planar height 49.98 µm at readout)", None, "#ffffff"),
        ("HSQ 50 nm + PECVD SiO₂ cap 110 nm\n(window floor), 160 ± 10 nm over the wires", None, "#ecebe7"),
        ("NbN meander (L20), 7 nm", None, "#d5d3cc"),
        ("PECVD SiO₂ spacer, 238 nm", None, "#eeede9"),
        ("Al mirror (L10), raised, 100 nm", None, "#c4c4c2"),
        ("Base SiO₂ (thermal), 1.0 µm nominal", None, "#e4e1d8"),
        ("HR Si, ρ > 20 kΩ·cm, ~525 µm [verify]", None, "#b9b8b2"),
    ]
    fig, ax = plt.subplots(figsize=(ps.W1, 3.4))
    n = len(layers)
    for k, (text, _, col) in enumerate(layers):
        y = n - 1 - k
        ax.add_patch(Rectangle((0, y), 1, 1, fc=col, ec="#898781", lw=0.6))
        ax.text(0.5, y + 0.5, text, ha="center", va="center", fontsize=7, color=ps.INK, wrap=True)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, n)
    ax.axis("off")
    fig.tight_layout()
    ps.save(fig, "stack")
    print("stack: bands drawn:", n)


def fig_transport_waveform():
    """Two stacked panels: ion position (top) and electrode voltages (bottom) against time."""
    path = os.path.join(SIMOUT, "21_transport_waveform", "trap_die_v4_A30_V2zero", "waveform.csv")
    with open(path, newline="") as fh:
        rows = list(csv.reader(fh))
    head = rows[0]
    print("transport_waveform header:", head[:6], "...", head[-2:], "(", len(head), "columns )")
    print("transport_waveform first two rows:", rows[1][:5], rows[2][:5])
    phase = [r[1] for r in rows[1:]]
    data = np.array([[float(v) if k != 1 else 0.0 for k, v in enumerate(r)] for r in rows[1:]])
    t = data[:, 0]
    y = data[:, 2]
    cols = {int(h[1:]): data[:, k] for k, h in enumerate(head) if h.startswith("V")}
    # phase boundaries: row where the phase string changes
    bounds = [i for i in range(1, len(phase)) if phase[i] != phase[i - 1]]
    tb = [float(t[i]) for i in bounds]
    print("transport_waveform phase boundaries (row, t_us):", list(zip(bounds, tb)))
    edges = [float(t[0])] + tb + [float(t[-1])]
    names = ["tilt out", "move", "tilt in"]   # CSV phases untilt, move, tilt in that order
    styles = [ps.STYLE_SOLID, ps.STYLE_DASHED, ps.STYLE_DASHDOT, ps.STYLE_DOTTED]
    colours = [ps.BLUE, ps.ORANGE, ps.AQUA, ps.YELLOW]
    hl = [7, 12, 8, 11]

    fig, (axt, axb) = plt.subplots(2, 1, sharex=True, figsize=(ps.W2, 4.8),
                                   gridspec_kw={"height_ratios": [1, 2.4], "hspace": 0.28})
    axt.plot(t, y, color=ps.BLUE, lw=1.2)
    axt.set_ylabel("ion position (µm)")
    for n, v in cols.items():
        if n not in hl:
            axb.plot(t, v, color="#b9b7af", lw=0.5, zorder=1)
    lines = {}
    for k, n in enumerate(hl):
        ls, mk = styles[k]
        (lines[n],) = axb.plot(t, cols[n], color=colours[k], ls=ls, lw=1.2, label=f"electrode {n}", zorder=3)
    axb.set_ylabel("electrode voltage (V)")
    axb.set_xlabel("time (µs)")
    for ax in (axt, axb):
        for tbi in tb:
            ax.axvline(tbi, color=ps.AXIS, lw=0.6, ls=":", zorder=0)
    for k, nm in enumerate(names):
        mid = 0.5 * (edges[k] + edges[k + 1])
        axt.text(mid, 0.93, nm, transform=axt.get_xaxis_transform(), ha="center", va="top", fontsize=8)
    axb.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=4, handlelength=2.4, columnspacing=1.0)
    fig.tight_layout()
    ps.save(fig, "transport_waveform")

    # spot check: V7 at three rows, file vs plotted line
    xd = lines[7].get_xdata()
    yd = lines[7].get_ydata()
    idx = [0, len(t) // 2, len(t) - 1]
    print("transport_waveform V7 check, file:", [(float(rows[1 + j][0]), float(rows[1 + j][head.index("V7")])) for j in idx])
    print("transport_waveform V7 check, plotted:", [(float(xd[j]), float(yd[j])) for j in idx])


def fig_rf_capacitance_sections():
    """Horizontal stacked bars: RF capacitance to ground per configuration, lossless-Si values."""
    s = load_json(os.path.join(SIMOUT, "22_rf_capacitance", "summary.json"))
    order = ["A30_E2", "A30_E1", "NODET_E2_full", "NODET_E2_thermal", "NODET_E1_full", "NODET_E1_thermal"]
    pretty = {"A30_E2": "A30, E2", "A30_E1": "A30, E1", "NODET_E2_full": "NODET, E2",
              "NODET_E2_thermal": "NODET, E2, thermal SiO₂ only", "NODET_E1_full": "NODET, E1",
              "NODET_E1_thermal": "NODET, E1, thermal SiO₂ only"}
    seg_names = ["rails over the lead slot", "rails, plain", "feed line", "U bar and pad"]
    seg_cols = [ps.BLUE, ps.ORANGE, ps.AQUA, ps.YELLOW]
    vals = {}
    for key in order:
        sec = s["configs"][key]["sections"]
        slot = sec["slot"]["C_pF"] if "slot" in sec else 0.0      # NODET has no lead slot
        vals[key] = [slot, sec["plain"]["C_pF"], sec["feed"]["C_pF"], sec["ubar"]["C_pF"] + sec["pad"]["C_pF"]]
        total = s["configs"][key]["chip"]["C_chip_pF"]
        print(f"rf_capacitance {key}: segments {[round(v, 4) for v in vals[key]]} sum {sum(vals[key]):.4f}, "
              f"chip total {total:.4f} pF")
    ylab = [pretty[k] for k in order]
    ypos = np.arange(len(order))[::-1]
    fig, ax = plt.subplots(figsize=(ps.W2, 3.0))
    left = np.zeros(len(order))
    containers = []
    for j in range(4):
        w = np.array([vals[k][j] for k in order])
        bars = ax.barh(ypos, w, left=left, height=0.6, color=seg_cols[j], ec="white", lw=0.8, label=seg_names[j])
        containers.append(bars)
        left = left + w
    for i, key in enumerate(order):
        total = s["configs"][key]["chip"]["C_chip_pF"]
        ax.text(total + 0.04, ypos[i], f"{total:.2f} pF", va="center", ha="left", fontsize=8)
    ax.set_yticks(ypos)
    ax.set_yticklabels(ylab)
    ax.set_xlim(0, 3.2)
    ax.set_xlabel("RF capacitance to ground (pF)")
    ax.grid(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.2), ncol=2, handlelength=1.4, columnspacing=1.0)
    fig.tight_layout()
    ps.save(fig, "rf_capacitance_sections")

    # spot check A30_E2: four segment values and total, JSON vs plotted patches
    i = order.index("A30_E2")
    plotted = [containers[j][i].get_width() for j in range(4)]
    print("rf_capacitance A30_E2 segments, JSON:", [round(v, 6) for v in vals["A30_E2"]])
    print("rf_capacitance A30_E2 segments, plotted:", [round(v, 6) for v in plotted])
    print("rf_capacitance A30_E2 total, JSON:", round(s["configs"]["A30_E2"]["chip"]["C_chip_pF"], 6),
          "plotted sum:", round(sum(plotted), 6), "label:", f"{s['configs']['A30_E2']['chip']['C_chip_pF']:.2f} pF")


def main():
    ps.apply()
    fig_rf_null_height()
    fig_transport_static()
    fig_collection_vs_height()
    fig_termination()
    fig_stack()
    fig_transport_waveform()
    fig_rf_capacitance_sections()


if __name__ == "__main__":
    main()
