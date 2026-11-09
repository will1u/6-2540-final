"""19 - Lead termination: RF current through the SNSPD nanowire for several terminations.

Claude-authored.

The SNSPD has two Au leads. Each lead picks up a common-mode RF displacement current at 28 MHz
(DESIGN_LOG step 28, per-lead upper bound at the pad). Each lead end sees ground through a bond wire
inductance and a termination. The nanowire joins the two lead ends through its kinetic inductance L_k
in series with the lead resistance R_pair. With identical terminations no RF current crosses the
nanowire; any asymmetry drives part of it through the nanowire.

Lumped, linear model at one frequency (28 MHz). Node A = pad end of the signal lead, node B = pad end
of the return lead. Both nodes get the same injected current I_inj. Nodal equations:
    (1/Z_A + 1/Z_nw) V_A - V_B/Z_nw = I_inj
    (1/Z_B + 1/Z_nw) V_B - V_A/Z_nw = I_inj
The nanowire current is I_nw = (V_A - V_B)/Z_nw.

The script prints numbers only and recommends no termination.

Outputs: sim/out/19_lead_termination/summary.json, sim/out/19_lead_termination/termination.png
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "19_lead_termination")
os.makedirs(OUT, exist_ok=True)

F = 28e6                                   # RF drive frequency (design/CLAUDE.md: 53 V at 28 MHz)
W = 2 * np.pi * F
Z0 = 50.0                                  # ohm, the 50 ohm line (task spec)
L_BOND = 2e-9                              # H, about 2 mm of bond wire [verify]
R_PAIRS = (0.0, 10.0, 30.0, 140.0)         # ohm, series R of both Au leads [verify]; large value = thin E1 Au
DIES = {"A30": 3.10e-6, "B60": 5.94e-6}    # H, nanowire kinetic inductance L_k (DESIGN_LOG 2026-11-08 overhang audit)
OPTIONS = {"E2": 44.5e-6, "E1": 28.3e-6}   # A per lead, common mode (DESIGN_LOG step 28, slot-lead pickup)
I_LO, I_HI = 8e-6, 20e-6                   # A, NbN switching-current bracket (task spec; DESIGN_LOG step 26)
C_TRAP = 100e-12                           # F, L-C trap capacitor (task spec) [verify]
R_TRAP = 0.5                               # ohm, trap series resistance (task spec) [verify]
TRAP_FREQS = (1e6, 3e6, 10e6, 28e6, 100e6)
TRAP_DETUNE = (("trap nominal", 1.00), ("trap L -5 %", 0.95), ("trap L +5 %", 1.05))


def par(a, b):
    """Parallel combination of two impedances."""
    return a * b / (a + b)


def z_trap(f, l_trap):
    """Series L-C trap: r + jwL + 1/(jwC)."""
    w = 2 * np.pi * f
    return R_TRAP + 1j * w * l_trap + 1 / (1j * w * C_TRAP)


def i_nw(z_a, z_b, z_nw, i_inj):
    """Current through the nanowire from A to B for equal injection i_inj into both nodes."""
    y_nw = 1 / z_nw
    y = np.array([[1 / z_a + y_nw, -y_nw], [-y_nw, 1 / z_b + y_nw]], dtype=complex)
    v = np.linalg.solve(y, np.array([i_inj, i_inj], dtype=complex))
    return (v[0] - v[1]) / z_nw


def build_cases():
    """Termination cases: (label, Z_termA, Z_termB, pulse note). Z_term excludes the bond wire."""
    cases = []
    # 1. 50 ohm line on A, short on B
    cases.append(("1 50 ohm line / short", Z0, 0.0, "no added filter"))
    # 2. shunt capacitor on A; pulse corner of the RC from 50 ohm and C
    for c in (100e-12, 1e-9, 10e-9):
        fc = 1 / (2 * np.pi * Z0 * c)
        cases.append((f"2 shunt {c * 1e9:g} nF on A", par(Z0, 1 / (1j * W * c)), 0.0,
                      f"A-side low-pass corner {fc / 1e6:.3f} MHz"))
    # 3. 50 ohm || C on A, capacitor C(1+m) on B (as specified; B has no 50 ohm)
    for c in (1e-9, 10e-9):
        fc = 1 / (2 * np.pi * Z0 * c)
        for m in (0.0, 0.05, 0.10, 0.20):
            cases.append((f"3 matched {c * 1e9:g} nF m={m:.2f}", par(Z0, 1 / (1j * W * c)),
                          1 / (1j * W * c * (1 + m)), f"A-side low-pass corner {fc / 1e6:.3f} MHz"))
    # 4. series L-C trap at 28 MHz on A (50 ohm || trap), B to ground
    l0 = 1 / (W ** 2 * C_TRAP)
    for name, fac in TRAP_DETUNE:
        lt = fac * l0
        zt = z_trap(F, lt)
        note = "abs(Z_trap) ohm at 1/3/10/28/100 MHz: " + ", ".join(
            f"{abs(z_trap(f, lt)):.4g}" for f in TRAP_FREQS)
        cases.append((f"4 {name}", par(Z0, zt), 0.0, note))
    # 5. symmetric 50 ohm on both leads; then mismatch on B (50 ohm x (1 + m))
    cases.append(("5 symmetric 50 / 50", Z0, Z0, "no added filter"))
    for m in (0.05, 0.10):
        cases.append((f"5 B 50 ohm x (1+{m:.2f})", Z0, Z0 * (1 + m), "no added filter"))
    return cases


def main():
    cases = build_cases()
    res = {}      # (label, die, option, R_pair) -> abs(I_nw) in uA
    rows = []
    for label, z_ta, z_tb, note in cases:
        for die, lk in DIES.items():
            for opt, i_inj in OPTIONS.items():
                for rp in R_PAIRS:
                    z_nw = 1j * W * lk + rp
                    z_a = 1j * W * L_BOND + z_ta
                    z_b = 1j * W * L_BOND + z_tb
                    ia = abs(i_nw(z_a, z_b, z_nw, i_inj)) * 1e6
                    res[(label, die, opt, rp)] = ia
                    rows.append(dict(case=label, die=die, option=opt, R_pair=float(rp),
                                     I_nw_uA=float(ia), pct_of_8uA=float(100 * ia / (I_LO * 1e6)),
                                     pulse_note=note))

    # ------------------------------------------------ pulse effects
    print("SNSPD pulse reference (tau = L_k / 50 ohm):")
    for die, lk in DIES.items():
        tau = lk / Z0
        print(f"  {die}: tau = {tau * 1e9:.1f} ns, corner 1/(2 pi tau) = {1 / (2 * np.pi * tau) / 1e6:.2f} MHz")

    print("\nPulse effects of the terminations:")
    for label, z_ta, z_tb, note in cases:
        print(f"  {label:32s} {note}")

    # ------------------------------------------------ tables
    print(f"\nabs(I_nw) in uA (percent of 8 uA). Reference lines: 8 uA = 100 %, 20 uA = 250 %.")
    for die in DIES:
        for opt in OPTIONS:
            print(f"\n{die} / {opt}  (I_inj = {OPTIONS[opt] * 1e6:.1f} uA per lead)")
            print(f"{'case':30s}" + "".join(f"{'R_pair=' + str(int(r)) + ' ohm':>22s}" for r in R_PAIRS))
            for label, _, _, _ in cases:
                cells = []
                for rp in R_PAIRS:
                    v = res[(label, die, opt, rp)]
                    cells.append(f"{v:9.3f} ({100 * v / (I_LO * 1e6):6.1f}%)")
                print(f"{label:30s}" + "".join(f"{c:>22s}" for c in cells))

    # ------------------------------------------------ outputs
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(rows, fh, indent=1)

    labels = [c[0] for c in cases]
    vals = [max(res[(lb, "A30", "E2", 0.0)], 1e-4) for lb in labels]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(range(len(vals)), vals, color="0.45")
    ax.set_yscale("log")
    ax.set_ylim(1e-4, 100)
    ax.axhline(I_LO * 1e6, color="C3", ls="--", lw=1, label="8 uA")
    ax.axhline(I_HI * 1e6, color="C1", ls="--", lw=1, label="20 uA")
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(labels, rotation=75, ha="right", fontsize=7)
    ax.set_ylabel("abs(I_nw) (uA), log scale")
    ax.set_title("A30, E2, R_pair = 0 (values below 1e-4 uA plotted at 1e-4 uA)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "termination.png"), dpi=150)

    # ------------------------------------------------ acceptance
    print("\nAcceptance:")
    a1 = res[("1 50 ohm line / short", "A30", "E2", 0.0)]
    hand = 44.5e-6 * Z0 / abs(Z0 + 1j * W * DIES["A30"]) * 1e6
    print(f"  case 1, A30, E2, R_pair=0: {a1:.3f} uA (hand estimate {hand:.3f} uA), "
          f"in [3.5, 4.5]: {'PASS' if 3.5 <= a1 <= 4.5 else 'FAIL'}")
    sym = [v for (lb, d, o, r), v in res.items() if lb == "5 symmetric 50 / 50"]
    print(f"  case 5 zero mismatch: max abs(I_nw) = {max(sym):.3e} uA, "
          f"zero to precision: {'PASS' if max(sym) < 1e-9 else 'FAIL'}")
    fc1 = 1 / (2 * np.pi * Z0 * 1e-9) / 1e6
    print(f"  case 2, C = 1 nF: low-pass corner {fc1:.3f} MHz, "
          f"3.18 MHz: {'PASS' if abs(fc1 - 3.183) < 0.005 else 'FAIL'}")


if __name__ == "__main__":
    main()
