"""RF primer numbers (Claude-authored, 2026-11-10). Feeds design/primers/RF_PRIMER.md.

Question: what do the basic RF, filter and capacitance formulas give for this chip, using one
example throughout (RF rail 53 V zero-to-peak, 28 MHz)? Which design numbers come from the sim outputs?

Model: circuit formulas only (I = w C V, Q and power, RC corners, skin depth, a lossy-dielectric
loss tangent, the capacitive divider, series L-C and shunt C on a 50 ohm line). No new simulation.
Inputs: values read from sim/out/18_e1_vs_e2, sim/out/10c_mirror_thickness, sim/out/19_lead_termination,
sim/out/22_rf_capacitance, sim/out/23_dc_rf_coupling, gds/measured_v4.json, and from the text of the repo files named in each block. Typed here: only the
example values (53 V, 28 MHz, 10 pF) and the literature RC pairs, each with its source.
Output: stdout only. Run from Git Bash: cd design/sim && ./run.sh ../primers/primer_numbers.py

Section 1 reads the chip RF capacitance from sim/out/22_rf_capacitance/summary.json.
Lumped models only; the sim 19 values are upper bounds. Order of magnitude where the source says so.
"""
import json
import math
import os
import re

DESIGN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F_RF = 28e6              # Hz, example drive frequency (design/CLAUDE.md, RF drive)
V_RF = 53.0              # V, example RF amplitude, zero-to-peak (sim/trapcalc.py V_RF)
OMEGA = 2 * math.pi * F_RF
EPS0 = 8.854e-12         # F/m
MU0 = 4e-7 * math.pi     # H/m
ACC = []                 # (name, value, target, ok)


def jload(rel):
    with open(os.path.join(DESIGN, rel), encoding="utf-8") as f:
        return json.load(f)


def ltext(rel):
    with open(os.path.join(DESIGN, rel), encoding="utf-8") as f:
        return f.read()


def check(name, value, target, tol):
    ok = abs(value - target) <= tol * abs(target)
    ACC.append((name, value, target, ok))


def find_row(rows, prefix):
    for r in rows:
        if r["quantity"].startswith(prefix):
            return r
    raise KeyError(prefix)


def sim19_current(case, die, option, r_pair=0.0):
    for r in jload("sim/out/19_lead_termination/summary.json"):
        if (r["case"] == case and r["die"] == die and r["option"] == option
                and r["R_pair"] == r_pair):
            return r["I_nw_uA"]
    raise KeyError(case)


meas = jload("gds/measured_v4.json")
Z0 = meas["constants"]["Z0_ohm"]
# Two 10c cases (design/sim/10c_mirror_thickness.py). Slot cross-section of the final stack
# (raised 100 nm Al, 110 nm SiO2 cap under the Au leads): the leads, the mirror strip, the mirror swing.
c10 = jload("sim/out/10c_mirror_thickness/summary.json")["al100_cap110"]
# Raised 100 nm Al with 160 nm SiO2 over the wires: the direct pickup in the nanowire window.
c10_win = jload("sim/out/10c_mirror_thickness/summary.json")["al100"]
s18 = jload("sim/out/18_e1_vs_e2/summary.json")["rows"]

# ---------------------------------------------------------------- 1
print("== 1. The chip is a capacitor ==")
i_pf = OMEGA * 1e-12 * V_RF * 1e3          # mA per pF
print(f"omega = 2 pi f = {OMEGA:.4e} rad/s  (f = {F_RF/1e6:g} MHz, V = {V_RF:g} V)")
print(f"I per pF at {V_RF:g} V, {F_RF/1e6:g} MHz = {i_pf:.2f} mA")
print(f"I per fF at {V_RF:g} V, {F_RF/1e6:g} MHz = {i_pf:.2f} uA")
# chip RF capacitance from sim 22 (Si treated as a lossless dielectric: the cold case)
s22 = jload("sim/out/22_rf_capacitance/summary.json")
for cfg in ("A30_E2", "A30_E1"):
    ch = s22["configs"][cfg]["chip"]
    c_chip = ch["C_chip_pF"]
    print(f"chip RF capacitance, {cfg.replace('_', ' on ')} (sim 22, Si lossless) = {c_chip:.2f} pF:"
          f" I = {OMEGA * c_chip * 1e-12 * V_RF * 1e3:.1f} mA")
ch = s22["configs"]["A30_E2"]["chip"]
print(f"  share of the field energy in the Si = {ch['p_Si_length_weighted']:.2f}, in the SiO2 = {ch['p_SiO2_length_weighted']:.2f} (A30 on E2)")
txt = ltext("fab/variants/LOCAL_MIRROR.md")
m = re.search(r"C_RF–ground ≈ ([\d.]+) pF instead of ([\d.]+) pF", txt)
c_plane, c_thin = float(m.group(1)), float(m.group(2))
print(f"fab/variants/LOCAL_MIRROR.md (line 19-33 area): die-wide Al plane on the thin stack C_RF-ground = {c_plane:g} pF,"
      f" thick 10 um D2 baseline C_RF-ground = {c_thin:g} pF")
print(f"  I = omega C V at {V_RF:g} V, {F_RF/1e6:g} MHz: {OMEGA * c_plane * 1e-12 * V_RF:.2f} A (thin stack, die-wide plane, 127 pF),"
      f" {OMEGA * c_thin * 1e-12 * V_RF * 1e3:.1f} mA (thick 10 um D2 baseline, plane 10.3 um down, {c_thin:g} pF)")

# ---------------------------------------------------------------- 2
print("== 2. Why the drive needs a resonator ==")
C_TOT = 10e-12                              # F, example total capacitance (NOT the chip)
w_stored = 0.5 * C_TOT * V_RF ** 2          # J, peak stored energy W = C V^2 / 2
print(f"example C_tot = {C_TOT*1e12:g} pF (example value, not the chip)")
print(f"stored energy W = C V^2 / 2 = {w_stored*1e9:.2f} nJ")
for q in (50, 100, 200, 500):
    p = OMEGA * w_stored / q                # W, P = omega W / Q
    print(f"power for Q = {q}: P = omega W / Q = {p*1e3:.1f} mW")
l_req = 1 / (OMEGA ** 2 * C_TOT)            # H
print(f"L for C_tot = {C_TOT*1e12:g} pF at {F_RF/1e6:g} MHz: L = {l_req*1e6:.2f} uH")
print(f"bandwidth f0/Q for Q = 100: {F_RF/100/1e3:.0f} kHz")
df = F_RF * (-1e-12 / (2 * C_TOT))          # Hz, shift for dC = 1 pF
print(f"df for dC = 1 pF: df = f0 (-dC / 2 C_tot) = {df/1e6:.2f} MHz")

# ---------------------------------------------------------------- 3
print("== 3. Where the Q goes (loss) ==")
kohm_cm = float(re.search(r"> (\d+) k[^ ]*cm", ltext("CLAUDE.md")).group(1))
rho_si = kohm_cm * 10.0                     # ohm m; 1 kohm cm = 10 ohm m
eps_si = float(re.search(r"EPS_OX, EPS_SI = ([\d.]+), ([\d.]+)",
                         ltext("sim/10b_rf_pickup_v4.py")).group(2))
print(f"Si: eps_r = {eps_si:g} (sim/10b_rf_pickup_v4.py), rho = {rho_si:g} ohm m"
      f" ({kohm_cm:g} kohm cm, lower spec in design/CLAUDE.md)")
for f_hz in (F_RF, 1e6):
    tan_d = 1 / (2 * math.pi * f_hz * EPS0 * eps_si * rho_si)
    print(f"tan delta of Si at {f_hz/1e6:g} MHz = {tan_d:.3f}")
p_scale = 0.5 * (i_pf * 1e-3) ** 2 * 1.0   # W, I = 9.32 mA into 1 ohm
print(f"scale: P = I^2 R / 2 for I = {i_pf:.2f} mA, R = 1 ohm: {p_scale*1e6:.1f} uW")

# ---------------------------------------------------------------- 4
rho_au = float(re.search(r"rho = ([0-9.e+-]+) ohm m",
                         find_row(s18, "Rs, room temperature, bulk rho")["quantity"]).group(1))
t_e1 = c10["E1"]["t_au_um"]
t_e2 = c10["E2"]["t_au_um"]
delta_au = math.sqrt(rho_au / (math.pi * F_RF * MU0)) * 1e6   # um
print("== 4. Skin depth and sheet resistance (E1 versus E2) ==")
print(f"Au bulk rho = {rho_au:.3g} ohm m (sim/out/18_e1_vs_e2/summary.json)")
print(f"skin depth at {F_RF/1e6:g} MHz = {delta_au:.2f} um")
for label, t_um in (("E1", t_e1), ("E2", t_e2)):
    rsq = rho_au / (t_um * 1e-6)
    print(f"{label}: t = {t_um:g} um, R_sq = rho/t = {rsq:.4f} ohm/sq,"
          f" t/delta = {t_um/delta_au:.3f} (thinner than delta: {'yes' if t_um < delta_au else 'no'})")
lead_e1 = float(find_row(s18, "one lead R, room temperature, bulk rho")["E1"])
lead_e2 = float(find_row(s18, "one lead R, room temperature, bulk rho")["E2"])
print(f"SNSPD slot lead, one lead, room temperature, bulk rho: E1 = {lead_e1:.2f} ohm,"
      f" E2 = {lead_e2:.2f} ohm (sim/out/18_e1_vs_e2)")

# ---------------------------------------------------------------- 5
print("== 5. Capacitive pickup ==")
slot = c10["E2"]["slot"]
win = c10_win["E2"]["window"]
c_per_um = slot["C_rf_lead_fF_per_um"]        # fF/um
l_lead_um = 2240.0   # um, lead length in the trap (the outline's value; the JSON agrees to 0.1 %)
c_lead_fF = c_per_um * l_lead_um
i_lead = OMEGA * c_lead_fF * 1e-15 * V_RF * 1e6   # uA
print(f"C_c per um (RF rail to slot lead) = {c_per_um*1000:.3f} aF/um")
print(f"lead length in trap (from the JSON) = {l_lead_um:.0f} um")
print(f"total C_c over {l_lead_um:.0f} um = {c_lead_fF:.3f} fF")
print(f"I = omega C_c V = {i_lead:.2f} uA (JSON I_lead_in_trap_uA = {slot['I_lead_in_trap_uA']:.3f})")
c_rn = win["C_RN_fF"]
i_rn = OMEGA * c_rn * 1e-15 * V_RF * 1e6
print(f"nanowire window: C_RN = {c_rn:.4f} fF, I = omega C V = {i_rn:.4f} uA"
      f" (JSON I_pk_uA = {win['I_pk_uA']:.4f})")

# ---------------------------------------------------------------- 6
print("== 6. Filters on the DC lines ==")
# Centre DC coupling from sim 23 (design/sim/23_dc_rf_coupling.py). The divider is
# V_el = V C_c / (C_c + C_f + C_g), where C_g is the centre DC's own capacitance to ground.
s23 = jload("sim/out/23_dc_rf_coupling/summary.json")
c_c_pF = s23["per_electrode"]["E2"]["centre_A30"]["C_c_pF"]
c_g_pF = s23["per_electrode"]["E2"]["centre_A30"]["C_g_pF"]
print(f"C_c = {c_c_pF:.3f} pF rail-to-centre, C_g = {c_g_pF:.3f} pF to ground"
      f" (sim/out/23_dc_rf_coupling/summary.json, per_electrode.E2.centre_A30)")
sim23_div = {d["C_f_pF"]: d["V_el_V"] for d in s23["divider"]
             if d["electrode"] == "centre DC (A30)" and d["Au"] == "E2"}
for c_f_pF in (100.0, 1000.0, 10000.0):
    v_div = V_RF * c_c_pF / (c_c_pF + c_f_pF + c_g_pF)          # V
    print(f"  C_f = {c_f_pF:g} pF, V_RF on centre DC = {v_div*1e3:.2f} mV"
          f" (sim 23 divider: {sim23_div[c_f_pF]*1e3:.2f} mV)")
    check(f"centre DC divider, C_f = {c_f_pF:g} pF = sim 23 divider", v_div, sim23_div[c_f_pF], 0.001)
c_no_cg = V_RF * c_c_pF / (c_c_pF + 1000.0)
print(f"  (without C_g, 1 nF: {c_no_cg*1e3:.2f} mV)")
for name, r_ohm, c_f in (("1 kohm / 1 nF", 1e3, 1e-9), ("35 kohm / 220 pF", 35e3, 220e-12)):
    fc = 1 / (2 * math.pi * r_ohm * c_f)
    att = 1 / math.sqrt(1 + (0.8e6 / fc) ** 2)
    print(f"RC pair {name}: f_c = {fc/1e3:.2f} kHz, attenuation at 0.8 MHz = {att:.4f}")
for f_c in [float(x) for x in re.search(r"F_FILTS = \(([^)]*)\)",
                                        ltext("sim/20_transport_timing.py")).group(1).split(",")]:
    print(f"corner f_c = {f_c/1e3:g} kHz (sim/20_transport_timing.py F_FILTS): tau = 1/(2 pi f_c) = {1e6/(2*math.pi*f_c):.3f} us")

# ---------------------------------------------------------------- 7
print("== 7. The SNSPD as a circuit, and its readout chain ==")
L_A30 = meas["files"]["trap_die_v4_A30.gds"]["meander"]["L_uH"]
L_B60 = meas["files"]["trap_die_v4_B60.gds"]["meander"]["L_uH"]
for name, l_uh in (("A30", L_A30), ("B60", L_B60)):
    tau_ns = l_uh * 1e-6 / Z0 * 1e9
    print(f"{name}: L_k = {l_uh:.2f} uH (gds/measured_v4.json), tau = L_k/50 ohm = {tau_ns:.2f} ns,"
          f" pulse corner 1/(2 pi tau) = {1e-6/(2*math.pi*tau_ns*1e-9)*1e3/1e3:.3f} MHz")
    print(f"   pulse height for I_b = 8 uA: {8e-6*Z0*1e3:.2f} mV, nanowire |Z| at 28 MHz = omega L_k = {OMEGA*l_uh*1e-6:.1f} ohm")
c_shunt = 1e-9
print(f"1 nF shunt across 50 ohm: reactance 1/(omega C) = {1/(OMEGA*c_shunt):.2f} ohm,"
      f" corner 1/(2 pi 50 ohm C) = {1/(2*math.pi*Z0*c_shunt)/1e6:.2f} MHz")
l_trap = 1 / (OMEGA ** 2 * c_shunt)
print(f"series L-C trap, C = 1 nF at 28 MHz: L = {l_trap*1e9:.1f} nH")
# sim/19_lead_termination.py simulates its trap with C_TRAP = 100 pF; the matching inductor:
l_trap_100 = 1.0 / (OMEGA ** 2 * 100e-12)
print(f"series L-C trap, C = 100 pF at 28 MHz (the value sim 19 uses): L = {l_trap_100*1e9:.0f} nH")
i_plain = sim19_current("1 50 ohm line / short", "A30", "E2")
i_shunt = sim19_current("2 shunt 1 nF on A", "A30", "E2")
i_trap = sim19_current("4 trap nominal", "A30", "E2")
i_mis = sim19_current("5 B 50 ohm x (1+0.05)", "A30", "E2")
print(f"A30 / E2 nanowire current, sim/out/19_lead_termination/summary.json, R_pair = 0 rows:")
print(f"  plain 50 ohm line, return shorted: {i_plain:.3f} uA")
print(f"  1 nF shunt on A:                   {i_shunt:.3f} uA")
print(f"  28 MHz L-C trap (4 trap nominal):  {i_trap:.4f} uA")
print(f"  50/50 ohm with 5 % mismatch:       {i_mis:.4f} uA")

# ---------------------------------------------------------------- 8
l_bond = float(re.search(r"L_BOND = ([0-9.e-]+)", ltext("sim/19_lead_termination.py")).group(1))
print("== 8. Grounding and return current ==")
print(f"bond wire L = {l_bond*1e9:g} nH (sim/19_lead_termination.py, tagged [verify]):"
      f" omega L = {OMEGA*l_bond:.3f} ohm at {F_RF/1e6:g} MHz")
for key in ("3e-08", "4e-08"):
    r = c10["E2"]["rho"][key]
    print(f"Al mirror strip, rho = {key} ohm m (100 nm raised Al, 110 nm cap, E2): i_mirror = {r['i_mirror_mA']:.3f} mA,"
          f" t10 = {r['t10_ohm']:.3f} ohm, v_m = {r['v_m_mV']:.2f} mV, p = {r['p_uW']:.2f} uW")

# ---------------------------------------------------------------- 9
print("== 9. Cheat sheet ==")
print("| quantity | formula | value on this chip | printed by |")
print("|---|---|---|---|")
print(f"| current per pF | I = omega C V | {i_pf:.2f} mA | yes |")
print(f"| stored energy, example 10 pF | W = C V^2 / 2 | {w_stored*1e9:.2f} nJ | yes |")
print(f"| power for Q = 100, example 10 pF | P = omega W / Q | {OMEGA*w_stored/100*1e3:.1f} mW | yes |")
print(f"| pickup current, slot lead | I = omega C_c V | {i_lead:.2f} uA | yes |")
print(f"| pickup current, nanowire window | I = omega C_RN V | {i_rn:.4f} uA | yes |")
print(f"| RC corner, 1 kohm / 1 nF | f_c = 1/(2 pi R C) | {1/(2*math.pi*1e3*1e-9)/1e3:.2f} kHz | yes |")
print(f"| tan delta of Si, 28 MHz | 1/(omega eps0 eps_r rho) | {1/(OMEGA*EPS0*eps_si*rho_si):.3f} | yes |")
print(f"| pulse time constant, A30 | tau = L_k/50 ohm | {L_A30*1e-6/Z0*1e9:.2f} ns | yes |")

# ---------------------------------------------------------------- ACCEPTANCE
check("I per pF at 53 V, 28 MHz = 9.32 mA", i_pf, 9.32, 0.01)
check("reactance of 1 nF at 28 MHz = 5.68 ohm", 1 / (OMEGA * 1e-9), 5.68, 0.01)
check("50 ohm with 1 nF corner = 3.18 MHz", 1 / (2 * math.pi * Z0 * 1e-9) / 1e6, 3.18, 0.01)
check("3.10 uH / 50 ohm = 62.0 ns", L_A30 * 1e-6 / Z0 * 1e9, 62.0, 0.01)
check("1 kohm / 1 nF corner = 159 kHz", 1 / (2 * math.pi * 1e3 * 1e-9) / 1e3, 159.0, 0.01)
check("lead pickup from C_c = JSON I_lead_in_trap_uA (0.1 %)", i_lead, slot["I_lead_in_trap_uA"], 0.001)
check("nanowire I from C_RN = JSON I_pk_uA (0.1 %)", i_rn, win["I_pk_uA"], 0.001)
check("tan delta of Si at 200 ohm m, 28 MHz = 0.274", 1 / (OMEGA * EPS0 * eps_si * rho_si), 0.274, 0.01)
print("== ACCEPTANCE ==")
for name, value, target, ok in ACC:
    print(f"{'PASS' if ok else 'FAIL'}  {name}: computed {value:.6g}, target {target:g}")
print("ALL PASS" if all(a[3] for a in ACC) else "SOME FAIL")
