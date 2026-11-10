> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes. Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

# Witness wafers and facility confirmations

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

> [!note] Electrode Au: both options shown
> E1 = Ti 10 nm / Au 350 nm lift-off. E2 = 6 µm plated Au on a Ti/Au seed. The team has not chosen between them ([open decisions](OPEN_DECISIONS.md)). Each loop is marked E1, E2 or both. The E1 and E2 loops have equal standing.

These loops qualify the v4 recipes ([local mirror H.2](variants/LOCAL_MIRROR.md); [process pages](process/01_FOUNDATION.md)). No completed loop measurements are recorded in the reviewed progress notes.

## Which loops apply

| Run | Focus | Electrode option |
|---|---|---|
| R1_TRAP | W5 plating; E1 lift-off loop; W7 bond-and-leak | W5 for E2 only; E1 lift-off loop for E1 only; W7 for both |
| R1_FULL | W8 inlaid mirror; W1 NbN on the real stack; W2 HSQ dose and etch; W3 layer-40 openings and contacts; W7 bond-and-leak; W5 and E1 lift-off loop as for R1_TRAP | As for R1_TRAP |

Complete the loops that apply to the chosen run and electrode option before its device wafer. W3 has no NbN and rehearses steps 3, 4, 8, 11 and 12–15 of the v4 traveler.

## Witness loops

### W8 Inlaid Al mirror (step 3)

**Purpose:** the 100 nm inlaid Al local mirror: layer-10 recess, Al lift-off, and a planar surface before the spacer goes on. Hampel 2023 (arXiv:2302.01462) made a 50 nm e-beam evaporated Al mirror by lift-off, raised on SiO₂. The recess is not in Hampel. It is this design's addition and is unproven until this loop passes.

**Stack / steps:** dummy thermal-SiO₂ wafer (Si / 1 µm SiO₂). 3a: LOR + positive resist [verify thicknesses]; MLA150; layer 10 exposed drawn. 3b: RIE a 100 nm recess (CHF₃ 25 / CF₄ 5 / Ar 50 sccm, 130 mTorr, 600 W, as in step 11) [verify on our tool; verify etch rate]; RIE-F-Samco-230iP or RIE-PlasmaTherm-210RL; target depth 100 ± 10 nm [design call; verify]. 3c: e-beam evaporate Al through the same resist, 100 nm nominal (equal to the measured recess depth), on EBeam-Temescal-FC2800 [verify that it has an Al source]. 3d: lift-off in NMP or Remover PG [verify]. Then the 238 nm SiO₂ spacer (step 4) on the same pieces.

**Measure:** RIE rate and recess depth (profilometer or AFM); Al thickness (crystal monitor and witness); residual step and edge profile after lift-off, and again after the 238 nm spacer (profilometer or AFM); lift-off quality after the fluorine etch (the plasma can harden the resist); hillocks after a 300 °C cycle (darkfield) [verify]; sheet resistance of the Al on a witness (4-pt).

**Go / no-go:** residual step between the Al and the SiO₂ ≤ 20 nm, and any lip or groove at the mirror edge ≤ 20 nm, by profilometer or AFM [design call; verify]; lift-off complete, with no residue.

**Fail:** go to the fallback in [process/01_FOUNDATION.md](process/01_FOUNDATION.md).

**Run and electrode:** R1_FULL only. R1_TRAP has no Al and skips step 3. No electrode step in this loop; both options.

### W1 NbN on spacer over Al

**Purpose:** NbN on the real v4 stack, with the 238 nm spacer over the 100 nm inlaid Al local mirror (team decision 2026-11-09, [`notes/decisions.md`](../../notes/decisions.md); `sim/10c`, DESIGN_LOG step 37). v3 witnesses carried 150 nm Al.

**Stack / steps:** Si / 1 µm thermal SiO₂ with the 100 nm recess (0.9 µm SiO₂ under the Al) / 100 nm evaporated Al, inlaid (from W8 pieces) / 238 nm SiO₂ spacer → NbN 7 nm, co-loaded with a thermal-SiO₂/Si chip (Medeiros ellipsometry model).

**Measure:** AFM on the spacer before NbN (hillocks, roughness); NbN thickness by ellipsometry; Rsq (4-pt); Tc (dipstick / PPMS [verify access]).

**Go / no-go:** Rsq ≈ 400 Ω/sq ± 15 % [team calc]; Tc ≥ 7.5 K on both pieces [verify]; no hillocks > 100 nm [verify].

**Run and electrode:** R1_FULL. No electrode step in this loop.

**Open:** No loop in the v4 list covers the thermal load of the step-8 cap (≤ 300 °C) on NbN. The old W1-b (5 × D2-equivalent PECVD cycles) covered the removed 10 µm SiO₂ and is retired. [verify whether a witness is needed for the cap.]

### W2 HSQ dose test on the real stack (Al / spacer / NbN)

**Purpose:** HSQ dose, development and CF₄ etch on the EBL tool, mark recognition, and layer 22 to layer 50 overlay.

**Stack / steps:** NbN on the W1 pieces. Dose matrix (mask_list L20); salty vs TMAH develop; CF₄ 2.0 / 2.5 / 3.0 min.

**Measure:** SEM linewidth; remaining HSQ thickness (the cap is then 160 nm minus this value, step 8); room-temperature R of test meanders; EBL mark recognition; layer 22 to layer 50 overlay.

**Go / no-go:** current target 130 nm wires / 70 nm spaces; calibrate linewidth tolerance [verify]. No bridges or breaks; R / R_expected 0.8–1.3 [verify]. Inspect T9 controls at their own nominal widths. Overlay budget [verify].

**Run and electrode:** R1_FULL; both options (the overlay applies to the electrode step).

### W3 Layer-40, contact and electrode rehearsal (no NbN)

**Purpose:** rehearse the layer-40 etches for the 0.40 µm mirror via and the 160 nm SNSPD contacts; Au-to-Al contact at the mirror via with and without the Ar pre-clean; sidewall coverage on the via; then the electrode step.

**Stack / steps:** Si / 1 µm SiO₂ with a 100 nm recess under the mirror (0.9 µm SiO₂ under the Al) / 100 nm evaporated Al, inlaid (from W8 pieces) / 238 nm SiO₂ spacer / SiO₂ cap to 160 nm total [verify: with or without HSQ] → layer-40 openings (0.40 µm to the Al at the mirror via; 160 nm onto a Ti/Au pad drawn as layer 22 [verify]) → electrode Au for the option in use (E1 lift-off, or E2 seed and plating), with and without the Ar pre-clean on the mirror via.

**Test structures** (v4 test die, drawn and checked 2026-11-09):
- T11 Au-to-Al via chain;
- T12 twin Au leads over Al (continuity across the planar mirror edge, and lead-to-lead leakage);
- T10 mirror strip, four-point (18.8–25.1 Ω expected at 100 nm, `sim/10c`, DESIGN_LOG step 37; acceptance not set [verify]);
- T2v Au / 0.40 µm SiO₂ / Al capacitor (about 3.5 pF [team calc]; geometry to confirm [verify]).

**Measure:** layer-40 depth and profile at the via and at the contacts (Dektak; SEM cross-section); over-etch time; over-etch into the 100 nm Al at the mirror via [verify]; clean Al and Au at each floor; T11 resistance with and without the Ar pre-clean; sidewall coverage of the seed or Au on the via wall (cross-section); T12 continuity and leakage; T10 strip resistance; T2v leakage at 50 V.

**Go / no-go:**
- Etch: about 1 min for 0.40 µm at the v3 rate of ~360 nm/min [team calc]; over-etch set here [verify].
- T11 resistance acceptance [verify]. The old < 10 Ω link limit was for the v3 M1 vias, not for this path.
- Seed or Au continuous over the via wall [verify].
- T12 continuity across the planar mirror edge and no lead-to-lead leakage [verify].
- T10 18.8–25.1 Ω expected at 100 nm (`sim/10c`, DESIGN_LOG step 37); acceptance [verify].
- T2v leakage ≤ 100 nA at 50 V [verify].

**Run and electrode:** R1_FULL; the electrode option in use (both, if both stay open).

### W5 Plating calibration (E2 only)

**Purpose:** current calibration, thickness map and roughness for the 6 µm plated Au (branch E2).

**Stack / steps:** Ti 15 nm / Au 50 nm seed + nLOF mold (≥ 8 µm, the L50 job of the run) + 6 µm Au on a bare-SiO₂ dummy (1.0 µm thermal SiO₂ on Si), as in the [R1_TRAP sheet](RUNSHEET_R1_TRAP.md).

**Measure:** current calibration; thickness map; AFM roughness; gap width at top and bottom of the mold; plated area for the run [verify].

**Go / no-go:** 6.0 ± 0.5 µm; ≤ 10 % across the wafer [verify]; roughness ~8 nm rms after seed removal (PTB 8.3(5) nm); no nodules.

**Run and electrode:** R1_TRAP and R1_FULL; E2 only.

### E1 lift-off loop (E1 only)

**Purpose:** lift-off of 0.35 µm Au over 5 µm gaps, Au coverage of the 0.40 µm mirror-via step (R1_FULL), and wedge bonding on evaporated Au.

**Stack / steps:** LOR + positive resist; L50 drawn; in-situ Ar pre-clean [verify whether needed on this die]; Ti 10 nm / Au 350 nm evaporated [verify thicknesses]; lift-off in NMP. R1_TRAP: on the thermal-SiO₂ dummy. R1_FULL: on the W3 stack, across the 0.40 µm via step.

**Measure:** LOR and resist profile (undercut); Ti and Au thickness on a witness; gap isolation at 10 V; Au continuity over the via step (cross-section); wedge-bond pull on the evaporated Au.

**Go / no-go:** all 5 µm gaps open, no Au across them; isolation > 100 MΩ at 10 V [verify]; Au continuous over the via step [verify]; wedge-bond pull [verify].

**Run and electrode:** R1_TRAP and R1_FULL; E1 only. The evaporator is a facility question ([below](#facility-confirmations)).

### W7 Bond-and-leak (step 19)

**Stack / steps:** dummy die with the planned Au bond pads (plated for E2, evaporated for E1), with the planned wire, tool and force [verify]. R1_FULL: also T2v with bonded pads (T2v replaces the old D2 capacitor T2).

**Measure:** Au-to-ground-fill leakage at ≤ 1 V before and after bonding (R1_TRAP); T2v leakage at ≤ 1 V before and after bonding (R1_FULL); pull and shear.

**Go / no-go:** no leakage change (> 1 GΩ) [verify, carried from v3]; pull and shear acceptance [verify]. A leak opened by bonding goes to the team as a design question; no change is proposed here. Shorts under bond pads: Leibrandt 2009 (thin Si₃N₄).

**Run and electrode:** R1_TRAP and R1_FULL; both options.

## Facility confirmations

All items below are **[verify]**. Gold and tool compatibility, the evaporator, the plating tank (E2 only), holders and training apply before R1_TRAP. NbN access is needed for R1_FULL.

- **Gold.** Which tools accept wafers carrying Au. On A30 and B60 dies the Ti/Au contacts (step 6) go on before the EBL, the RIE and the PECVD cap (steps 7 and 8), so those tools must accept it. Later Au steps: the layer-40 etch (step 11), the electrode step (12–15), the probe station and the dicing saw.
- **Evaporator (E1 only).** Which evaporator accepts Ti and Au for the E1 electrodes, and whether it has the in-situ Ar pre-clean. EBeam-Temescal-FC2800 is the tool named in the v4 pages for step 6 and for E1 [verify that it accepts Ti and Au for E1].
- **Step 3 and sputter.** Al source on the EBeam-Temescal-FC2800 for step 3 [verify]; SiO₂ RIE rate for a 100 nm recess with the lift-off resist on the wafer [verify]; the substrate RF etch in the Sputter-AJA-* tool, used for the E2 seed and the W3 Ar pre-clean [verify].
- **NbN.** Which sputter tool and recipe (Dane 2017 is a Berggren-group process), and whether access goes through that group.
- **Plating (E2 only).** Whether a gold plating tank exists (Plating-U04 is named; chemistry unverified), its chemistry, and its minimum plated area. Not needed for E1.
- **Holders.** Piece holders for the short loops.
- **Training and booking.** The order in which tool trainings must be done.
