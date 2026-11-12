"""22b - base SiO2 thickness sweep for the final stack with a raised 100 nm Al mirror (Claude-authored).

Questions answered:
  1. How does the RF capacitance of the A30 chip change when the base SiO2 (under the Al mirror and under the
     spacer) is made thinner, from 2.00 um down to 0.15 um?
  2. What fraction of the field energy sits in Si and in SiO2 at each base thickness?
  3. What RF current does each case draw at 53 V, 28 MHz?
  4. Does a finer grid change the thinnest case by more than 1 %?
  Comparison: at base 1.00 um, what does the cap change alone (0.110 -> 0.160 um) do?

Model: the 2-D electrostatics of sim 22, imported unchanged (module 22_rf_capacitance). Same grid, same Si and
SiO2 permittivities, same length table (LEN_A30). Only the stack changes:
  slot section:   Au / SiO2 cap / NbN / SiO2 spacer 0.238 um / raised Al 0.100 um / base SiO2
  other sections: Au / SiO2 cap / SiO2 spacer 0.238 um / base SiO2 (no Al, no NbN)
The acceptance step first reproduces sim 22's A30 chip totals with sim 22's own parameters, so the import is
known to be right before the sweep runs.

Each chip total is the sum of sim 22's section() over the A30 sections, as sim 22's config() does.
RF current I = omega C V_RF (the same formula as sim 18 and sim 22).

Limits: 2-D; ideal conductors; end effects neglected [inference]; the raised mirror's step is not modelled in the
electrode shape (the mirror is a flat zero-volt box, as in sim 22); the loss numbers are not in this script.

Outputs (design/sim/out/22b_base_sio2_sweep/): summary.json, table.md, sweep.png.
Run: cd design/sim && ./run.sh 22b_base_sio2_sweep.py
"""

import importlib
import json
import os
import sys
from math import pi

import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "22b_base_sio2_sweep")
os.makedirs(OUT, exist_ok=True)

# Sim 22 is named with a leading digit, so it is imported by name (its main() is not run here).
m = importlib.import_module("22_rf_capacitance")

T_SP = 0.238              # SiO2 spacer, um (as sim 22)
T_AL = 0.100              # raised Al mirror, um (slot section only)
T_CAP_SWEEP = 0.110       # SiO2 cap for the sweep, um (cap 160 nm minus HSQ, see RULES.md)
T_CAP_COMP = 0.160        # SiO2 cap for the comparison rows, um
BASES = [0.15, 0.30, 0.50, 1.00, 2.00]
DIES = [("E2", 6.0), ("E1", 0.35)]
TARGETS = {"E2": (6.0, 2.590, 22.628), "E1": (0.35, 2.395, 22.410)}   # sim 22 table, A30 chip totals


def params_sim22(sec, t_au):
    """Sim 22's own parameters (full stack, 160 nm cap), used for the acceptance check."""
    return m.params(sec, t_au, "full")


def params_sweep(sec, t_au, t_cap, t_base):
    """The raised-mirror stack. Only the slot section has the Al mirror."""
    if sec == "slot":
        return dict(t_au=t_au, t_cap=t_cap, t_sp=T_SP, nbn=True, t_al=T_AL, t_d1=t_base)
    return dict(t_au=t_au, t_cap=t_cap, t_sp=T_SP, nbn=False, t_al=0.0, t_d1=t_base)


def chip(pfun):
    """A30 chip totals. pfun(sec) gives the stack for each section."""
    C = 0.0
    Cg = 0.0
    L_tot = 0.0
    p_si_w = 0.0
    p_ox_w = 0.0
    for sec, L in m.LEN_A30:
        r = m.section(sec, L, pfun(sec))
        C += r["C_pF"]
        Cg += r["C_groundSi_pF"]
        L_tot += L
        p_si_w += r["p_Si"] * L
        p_ox_w += r["p_SiO2"] * L
    return dict(C_chip_pF=C, C_chip_groundSi_pF=Cg,
                p_Si_length_weighted=p_si_w / L_tot, p_SiO2_length_weighted=p_ox_w / L_tot,
                I_mA=m.OMEGA * C * 1e-12 * m.V_RF * 1e3)


def acceptance():
    """Step 1: sim 22's chip totals must come back before the sweep is trusted."""
    ok = True
    out = {}
    for name, (t_au, want_c, want_g) in TARGETS.items():
        c = chip(lambda sec, t=t_au: params_sim22(sec, t))
        dc = abs(c["C_chip_pF"] - want_c)
        dg = abs(c["C_chip_groundSi_pF"] - want_g)
        good = dc <= 0.001 and dg <= 0.01
        ok = ok and good
        out[name] = dict(C_chip_pF=c["C_chip_pF"], want_C_chip_pF=want_c, C_chip_groundSi_pF=c["C_chip_groundSi_pF"],
                         want_groundSi_pF=want_g, PASS=good)
        print(f"ACCEPTANCE {name}: C_chip {c['C_chip_pF']:.4f} pF (sim 22 {want_c:.3f}, +-0.001), "
              f"grounded-Si {c['C_chip_groundSi_pF']:.4f} pF (sim 22 {want_g:.3f}, +-0.01): "
              f"{'PASS' if good else 'FAIL'}", flush=True)
    return ok, out


def main():
    # ---------------- step 1: acceptance (printed first; stop if not reproduced)
    acc_ok, acc = acceptance()
    if not acc_ok:
        print("ACCEPTANCE FAILED: sim 22 totals not reproduced; no sweep run.", flush=True)
        sys.exit(1)

    # ---------------- step 2: sweep
    cases = []
    for name, t_au in DIES:
        for t_base in BASES:
            cases.append(dict(die=name, t_au=t_au, t_base=t_base, t_cap=T_CAP_SWEEP, kind="sweep"))
    for name, t_au in DIES:
        cases.append(dict(die=name, t_au=t_au, t_base=1.00, t_cap=T_CAP_COMP, kind="comparison"))

    rows = []
    for cs in cases:
        c = chip(lambda sec, cs=cs: params_sweep(sec, cs["t_au"], cs["t_cap"], cs["t_base"]))
        cs.update(c)
        rows.append(cs)
        print(f"{cs['kind']:10s} {cs['die']} base {cs['t_base']:.2f} um cap {cs['t_cap']:.3f} um: "
              f"C {c['C_chip_pF']:.4f} pF, grounded-Si {c['C_chip_groundSi_pF']:.4f} pF, "
              f"p_Si {c['p_Si_length_weighted']:.4f}, p_SiO2 {c['p_SiO2_length_weighted']:.4f}, "
              f"I {c['I_mA']:.3f} mA", flush=True)

    # ---------------- step 3: grid check (thinnest case, E2, plain section)
    # Plain section has no Al, so it is the same stack as the other sections of the thinnest case.
    p_thin = params_sweep("plain", 6.0, T_CAP_SWEEP, 0.15)
    coarse = m.run("plain", p_thin)["half"]
    fine = m.run("plain", p_thin, hs=0.5)["half"]
    rel = abs(fine - coarse) / coarse
    print(f"GRID CHECK plain, base 0.15 um, cap 0.110 um, E2: coarse {coarse:.6f} pF/mm, "
          f"half spacing {fine:.6f} pF/mm, change {rel:.4%}", flush=True)
    if rel > 0.01:
        print("GRID CHECK: change exceeds 1 %", flush=True)

    # ---------------- summary.json
    summary = dict(acceptance=acc, cases=rows,
                   grid_check=dict(section="plain", t_base_um=0.15, t_cap_um=T_CAP_SWEEP, t_au_um=6.0,
                                   coarse_pF_per_mm=coarse, half_spacing_pF_per_mm=fine, rel_change=rel),
                   inputs=dict(T_SP=T_SP, T_AL=T_AL, T_CAP_SWEEP=T_CAP_SWEEP, T_CAP_COMP=T_CAP_COMP,
                               V_RF=m.V_RF, F_RF=m.F_RF))
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)

    # ---------------- table.md
    L = ["> **Claude-authored.** Written by sim/22b_base_sio2_sweep.py (regenerate, do not edit).", "",
         "## Acceptance (sim 22 A30 chip totals reproduced) [team calc]", ""]
    for name, a in acc.items():
        L.append(f"- {name}: C_chip {a['C_chip_pF']:.4f} pF (sim 22 {a['want_C_chip_pF']:.3f}); "
                 f"grounded-Si {a['C_chip_groundSi_pF']:.4f} pF (sim 22 {a['want_groundSi_pF']:.3f}): "
                 f"{'PASS' if a['PASS'] else 'FAIL'}")
    L += ["", "## Sweep: A30 chip, raised 100 nm Al mirror [team calc]", "",
          "Base SiO2 = the SiO2 under the Al mirror and under the spacer. Cap = SiO2 over the NbN. "
          "Current I = omega C V_RF, V_RF = 53 V, 28 MHz. Energy fractions are length-weighted, as sim 22's config().", "",
          "| Die option | Row | Base SiO2 (um) | Cap SiO2 (um) | C_chip, Si lossless (pF) | C_chip, Si grounded (pF) | "
          "p_Si | p_SiO2 | I (mA) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        label = "sweep" if r["kind"] == "sweep" else "comparison (cap only)"
        L.append(f"| {r['die']} | {label} | {r['t_base']:.2f} | {r['t_cap']:.3f} | {r['C_chip_pF']:.3f} | "
                 f"{r['C_chip_groundSi_pF']:.3f} | {r['p_Si_length_weighted']:.4f} | "
                 f"{r['p_SiO2_length_weighted']:.4f} | {r['I_mA']:.2f} |")
    L += ["", "## Grid check [team calc]", "",
          f"Plain section, base SiO2 0.15 um, cap 0.110 um, E2 (6.0 um Au). Half-domain capacitance: "
          f"{coarse:.6f} pF/mm at the sim 22 grid, {fine:.6f} pF/mm at half the spacing. "
          f"Relative change {rel:.2%}" + (" (above 1 %)." if rel > 0.01 else " (below 1 %)."), "",
          "## Limits", "",
          "2-D; ideal conductors; end effects neglected [inference]; the raised mirror step is not modelled in the "
          "electrode shape (flat zero-volt box, as sim 22) [inference]; a10 limits are for the chip alone [inference]."]
    with open(os.path.join(OUT, "table.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    # ---------------- sweep.png
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for name, style in (("E2", "-"), ("E1", "--")):
        sweep = [r for r in rows if r["die"] == name and r["kind"] == "sweep"]
        xs = [r["t_base"] for r in sweep]
        ax.plot(xs, [r["C_chip_pF"] for r in sweep], style, marker="o", color="C0",
                label=f"{name}, Si lossless")
        ax.plot(xs, [r["C_chip_groundSi_pF"] for r in sweep], style, marker="s", color="C1",
                label=f"{name}, Si grounded")
    ax.set_xscale("log")
    ax.set_xlabel("Base SiO$_2$ thickness (µm)")
    ax.set_ylabel("RF capacitance, A30 chip (pF)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "sweep.png"), dpi=150)
    plt.close(fig)

    print("\nDONE: summary.json, table.md, sweep.png written", flush=True)


if __name__ == "__main__":
    main()
