> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Witness wafers and facility confirmations

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

> [!warning] Architecture changed to v4 (2026-11-08)
> The team chose the local-mirror architecture (no die-wide Al, no 10 µm D2), leads in a slot along the centre DC, A30 and B60 detector dies (B60 briefly dropped, then kept), and the same no-Al stack for R1_TRAP ([decisions](../../notes/decisions.md); DESIGN_LOG step 25). The GDS is now v4 (`gds/trap_die_v4_*`). **This page still describes the v3 baseline process.** It must be rewritten before any run; the rewrite waits on the electrode Au choice (E1 lift-off vs E2 plated). Do not fabricate from it.

These loops qualify the proposed recipes. No completed loop measurements are recorded in the reviewed progress notes.

## Which loops apply

| Run | Focus | Conditional work |
|---|---|---|
| R1_TRAP | W3 stress, etches and ground vias; W5 plating; W7 bonds | W6 only for a future undercut |
| R1_FULL | Carry forward trap qualification; add W1-a/b NbN and W2 dose/etch | Verify revised detector/T9 layout and cold-test access |

## Witness loops

Complete the loops applicable to the chosen run before its device wafer. W3 is the most valuable: it rehearses steps 9–18 with no NbN.

### W1-a NbN on spacer-over-Al

**Stack / steps:** Si / 1 µm SiO₂ / 150 nm Al-1%Cu / 238 nm spacer → NbN 7 nm, co-loaded with a thermal-SiO₂/Si chip (Medeiros ellipsometry model)

**Measure:** AFM on the spacer before NbN (hillocks, roughness); NbN thickness by ellipsometry; Rsq (4-pt); Tc (dipstick / PPMS [verify access])

**Go / no-go:** Rsq ≈ 400 Ω/sq ± 15 % [team calc]; Tc ≥ 7.5 K on both pieces [verify]; no hillocks > 100 nm [verify]

### W1-b NbN thermal history

**Stack / steps:** W1-a pieces with HSQ / cap → 5 × D2-equivalent PECVD cycles at 300 °C

**Measure:** Rsq and Tc again

**Go / no-go:** ΔTc ≤ 0.3 K, ΔRsq ≤ 10 % [verify]

### W2 HSQ dose test on the real stack (Al / spacer / NbN)

**Stack / steps:** Dose matrix (mask_list L20); salty vs TMAH develop; CF₄ 2.0 / 2.5 / 3.0 min

**Measure:** SEM linewidth; remaining HSQ thickness (needed for the cap thickness); RT R of test meanders

**Go / no-go:** current target 130 nm wires / 70 nm spaces; calibrate linewidth tolerance [verify]. No bridges or breaks; R / R_expected 0.8–1.3 [verify]. Inspect T9 controls at their own nominal widths.

### W3 D2-to-dicing rehearsal (no NbN)

**Stack / steps:** Si / thermal SiO₂ / Al / SiO₂ spacer / SiO₂ cap / 10 µm D2 (+back) / L40 / seed / L50 / plate / seed removal / L45 / gap etch / dice

**Measure:** Bow per D2 increment; D2 BOE rate and index; L40 profile; plating thickness and roughness; seed-removal roughness; gap-etch rate, uniformity and profile (SEM cross-section); Au redeposition on sidewalls; T1/T2/T6 (T7 retired) on the test dies; Al pad bondability (pull test); **fill-to-M1 via contact** (step 22): resistance through a via with and without the step-12 Ar pre-clean, plus a cross-section of the seed and Au on the via sidewall

**Go / no-go:** See [process checks](process_checks.md); via link < 10 Ω ([ground-link test a13](tests/01_ELECTRICAL.md))

### W5 Plating test

**Stack / steps:** Seed + nLOF mold (real L50) + 6 µm Au on a W3 wafer or a bare-SiO₂ wafer

**Measure:** Current calibration; thickness map; AFM roughness; gap width top/bottom

**Go / no-go:** 6.0 ± 0.5 µm; roughness ~8 nm rms after seed removal (PTB 8.3(5) nm)

### W6 Optional BOE

**Stack / steps:** Al / Ti coupons in 6:1 BOE for 10–60 s

**Measure:** Etch rates

**Go / no-go:** Only if an undercut is ever wanted (step 16 note)

### W7 Bond-and-leak (step 21)

**Stack / steps:** W3 test-die T2 (Au / D2 / M1 capacitor) and plated Au pads, with the planned wire, tool and force

**Measure:** Au-to-M1 leakage at ≤ 1 V before and after bonding; pull / shear

**Go / no-go:** No leakage change (> 1 GΩ) [verify]. If bonding opens a leak, cut the Al out under the DC pads next revision (keep it under the RF pad). Shorts under bond pads: Leibrandt 2009 (thin Si₃N₄)

## Facility confirmations

All items below are **[verify]**. Gold/tool compatibility, plating, holders and training apply before R1_TRAP; NbN access is needed for R1_FULL.

- **Gold.** Which tools accept wafers carrying Au. The D2 gap etch (step 16), the L45 resist step, the probe station and the dicing saw all come *after* plating.
- **NbN.** Which sputter tool and recipe (Dane 2017 is a Berggren-group process), and whether access goes through that group.
- **Plating.** Whether a gold plating tank exists, its chemistry, and its minimum plated area.
- **Holders.** Piece holders for the short loops.
- **Training and booking.** The order in which tool trainings must be done.
