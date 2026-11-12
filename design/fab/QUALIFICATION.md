> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes. Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09. Updated 2026-11-12 for run R1_ONE: the Al mirror is raised (no recess), Ti 5 / Au 50 nm contacts, PECVD cap 110 nm blanket (160 nm over the wires), SiO₂ 348 nm between the Au and the Al off the wires, and the one-week versions of the loops (proposals, [verify]).

# Witness wafers and facility confirmations

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

> [!note] Electrode Au: both options shown
> E1 = Ti 10 nm / Au 350 nm lift-off. E2 = 6 µm plated Au on a Ti/Au seed. The team has not chosen between them ([open decisions](OPEN_DECISIONS.md)). Each loop is marked E1, E2 or both. The E1 and E2 loops have equal standing.

These loops qualify the v4 recipes ([local mirror H.2](variants/LOCAL_MIRROR.md); [process pages](process/01_FOUNDATION.md)). No completed loop measurements are recorded in the reviewed progress notes.

## Which loops apply

| Run | Focus | Electrode option |
|---|---|---|
| R1_ONE (current; one wafer, 3 × 3 block: 4 A30, 1 B60 spare, 2 SNSPD-only, 2 NODET; optional layer-50-only second wafer) | W8 Al mirror hillock check (co-loaded); W1 NbN on the spacer over Al; W2 HSQ dose (dose array on the SNSPD-only die); W3 layer-40 openings and contacts; W5 plating; E1 lift-off loop; W7 bond-and-leak | W5 for E2 only; E1 lift-off loop for E1 only; the others for both |
| R1_TRAP (superseded by R1_ONE) | W5 plating; E1 lift-off loop; W7 bond-and-leak | W5 for E2 only; E1 lift-off loop for E1 only; W7 for both |
| R1_FULL (superseded by R1_ONE) | W8 inlaid mirror; W1 NbN on the real stack; W2 HSQ dose and etch; W3 layer-40 openings and contacts; W7 bond-and-leak; W5 and E1 lift-off loop as for R1_TRAP | As for R1_TRAP |

Complete the loops that apply to R1_ONE and the chosen electrode option before its device wafer. W3 has no NbN and rehearses steps 3, 4, 8, 11 and 12–15 of the v4 traveler.

## One-week plan (proposal, [verify])

The team has about one week of fab. Separate witness wafers cannot run first. Each loop below therefore has a one-week version. These are proposals, not agreed with the facility. The three patterns used are:

1. **Co-loaded pieces.** A small Si piece (thermal SiO₂ or bare Si, as each loop needs) goes into the same deposition, etch or PECVD run as the device wafer, and is measured in place of a witness wafer.
2. **Dose array on the SNSPD-only die.** The eight detector cells D1 to D8 (layer-20 datatypes 1, 2, 3, 0, 0, 5, 6, 7; dose factors 0.80 to 1.20) replace a separate dose loop.
3. **Layer-50-only second wafer.** If the team runs the optional second wafer, it is the electrode-step and wire-bond trial.

## Witness loops

### W8 Al mirror, raised (step 3)

**Purpose:** 100 nm evaporated Al mirror on the base SiO₂, by lift-off, with no recess. The mirror stands on the base SiO₂ (raised), so no SiO₂ is etched for it. Hampel 2023 (arXiv:2302.01462) made a 50 nm e-beam evaporated Al mirror by lift-off, raised on SiO₂. The 100 nm thickness is this design's choice; it is not in Hampel.

**Stack / steps:** dummy thermal-SiO₂ wafer (Si / 1 µm SiO₂). Layer 10 (mirror): LOR + positive resist [verify thicknesses]; MLA150 exposure; e-beam evaporate Al, 100 nm nominal, on EBeam-Temescal-FC2800 [verify that it has an Al source]; lift-off in NMP or Remover PG [verify]. Then the 238 nm SiO₂ spacer (step 4) on the same pieces.

**Measure:** Al thickness (crystal monitor and witness); lift-off quality and residue; edge profile of the Al after lift-off, and again after the 238 nm spacer (profilometer or AFM); sheet resistance of the Al on a witness (4-point); hillocks after a 300 °C cycle (darkfield) [verify].

**Go / no-go:** lift-off complete, with no residue; edge profile recorded [verify limits]; hillock limit [verify]. No numeric acceptance is set here.

**Fail:** go to the fallback in [process/01_FOUNDATION.md](process/01_FOUNDATION.md).

**One-week version (proposal, [verify]):** a co-loaded piece in the R1_ONE Al evaporation. Its hillock check and sheet resistance stand in for the witness loop. The edge profile is taken on the same piece after the spacer.

**Run and electrode:** R1_ONE. No electrode step in this loop; both options.

### W1 NbN on spacer over Al

**Purpose:** NbN on the real v4 stack, with the 238 nm spacer over the 100 nm raised Al mirror (facts decided 2026-11-12; the 100 nm thickness is from the 2026-11-09 team decision, [`notes/decisions.md`](../../notes/decisions.md); `sim/10c`, DESIGN_LOG step 37). v3 witnesses carried 150 nm Al.

**Stack / steps:** Si / 1 µm thermal SiO₂ / 100 nm evaporated Al, raised (from W8 pieces) / 238 nm SiO₂ spacer → NbN 7 nm, co-loaded with a thermal-SiO₂/Si chip (Medeiros ellipsometry model).

**Measure:** AFM on the spacer before NbN (hillocks, roughness); NbN thickness by ellipsometry; Rsq (4-pt); Tc (dipstick / PPMS [verify access]).

**Go / no-go:** Rsq ≈ 400 Ω/sq ± 15 % [team calc]; Tc ≥ 7.5 K on both pieces [verify]; no hillocks > 100 nm [verify].

**Open:** No loop in the v4 list covers the thermal load of the step-8 cap (≤ 300 °C) on NbN. The old W1-b (5 × D2-equivalent PECVD cycles) covered the removed 10 µm SiO₂ and is retired. [verify whether a witness is needed for the cap.]

**One-week version (proposal, [verify]):** NbN co-loaded with the device wafer's NbN run, on a thermal-SiO₂/Si piece and on a piece from the W8 Al evaporation. Rsq and Tc are read on those pieces.

**Run and electrode:** R1_ONE. No electrode step in this loop.

### W2 HSQ dose test on the real stack (Al / spacer / NbN)

**Purpose:** HSQ dose, development and CF₄ etch on the EBL tool, mark recognition, and layer 22 to layer 50 overlay.

**Stack / steps:** NbN on the W1 pieces. Dose matrix (mask_list L20); salty vs TMAH develop; CF₄ 2.0 / 2.5 / 3.0 min.

**Measure:** SEM linewidth; remaining HSQ thickness after develop (target 50 nm; the PECVD cap is 110 nm blanket, so the SiO₂ over the wires is 160 ± 10 nm); room-temperature R of the test meanders; EBL mark recognition; layer 22 to layer 50 overlay.

**Go / no-go:** current target 130 nm wires / 70 nm spaces; calibrate linewidth tolerance [verify]. No bridges or breaks; R / R_expected 0.8–1.3 [verify]. Overlay budget [verify].

**One-week version (proposal, [verify]):** the dose array on the SNSPD-only die (cells D1 to D8, datatypes as in [01_ELECTRICAL.md](tests/01_ELECTRICAL.md) a12) replaces the separate dose matrix. Its room-temperature resistances are read by a12. The HSQ thickness is read on a co-loaded piece.

**Run and electrode:** R1_ONE; both options (the overlay applies to the electrode step).

### W3 Layer-40, contact and electrode rehearsal (no NbN)

**Purpose:** rehearse the layer-40 etches for the 348 nm SiO₂ at the mirror via and for the contact openings onto the Ti/Au pads; Au-to-Al contact at the mirror via with and without the Ar pre-clean; sidewall coverage on the via; then the electrode step.

**Stack / steps:** Si / 1 µm SiO₂ / 100 nm evaporated Al, raised (from W8 pieces) / 238 nm SiO₂ spacer / PECVD SiO₂ cap, 110 nm blanket (348 nm off the wires) → layer-40 openings (348 nm to the Al at the mirror via; 110 nm onto a Ti/Au contact pad: HSQ is left only where layer 20 is written, and no layer 20 lies on the contact pads) → electrode Au for the option in use (E1 lift-off, or E2 seed and plating), with and without the Ar pre-clean on the mirror via. Ti 5 / Au 50 nm contact layer (layer 22) on the piece [verify].

**Test structures** (R1_ONE SNSPD-only die, probe station; the rest of the structures are not drawn):
- T11 Au-to-Al via chain, kept (at the centre of each SNSPD-only die);
- T12 (twin Au leads over Al) not drawn; the lead-to-SiO₂-to-Al isolation is measured on every detector by a8 ([01_ELECTRICAL.md](tests/01_ELECTRICAL.md));
- T10 (four-point Al strip) not drawn; Al sheet resistance four-point on a co-loaded piece instead (`sim/10c` gives 18.8–25.1 Ω for the old strip; a calculated value, not a measurement);
- T2v (SiO₂ capacitor) not drawn; SiO₂ thickness by ellipsometry on Si pieces co-loaded in each PECVD run [verify].

**Measure:** layer-40 depth and profile at the via and at the contacts (Dektak; SEM cross-section); over-etch time; over-etch into the 100 nm Al at the mirror via [verify]; clean Al and Au at each floor; T11 resistance with and without the Ar pre-clean; sidewall coverage of the seed or Au on the via wall (cross-section); Al sheet resistance (four-point, co-loaded piece); SiO₂ thickness (ellipsometry); detector pad isolation (a8) on the SNSPD-only die.

**Go / no-go:**
- Etch: about 1 min for 348 nm at the v3 rate of ~360 nm/min [team calc]; over-etch set here [verify].
- T11 resistance acceptance [verify]. The old < 10 Ω link limit was for the v3 M1 vias, not for this path.
- Seed or Au continuous over the via wall [verify].
- Al sheet resistance and SiO₂ thickness acceptance [verify]; the 18.8–25.1 Ω figure is calculated, not a limit.
- Detector pad isolation through the SiO₂ (a8, > 1 GΩ) [verify].

**One-week version (proposal, [verify]):** the layer-40 etches are checked on a piece co-loaded in the R1_ONE run; T11 is measured on the SNSPD-only die of the same run; the electrode step is rehearsed on the layer-50-only second wafer, if the team runs it.

**Run and electrode:** R1_ONE; the electrode option in use (both, if both stay open).

### W5 Plating calibration (E2 only)

**Purpose:** current calibration, thickness map and roughness for the 6 µm plated Au (branch E2).

**Stack / steps:** Ti 15 nm / Au 50 nm seed + nLOF mold (≥ 8 µm, the L50 job of the run) + 6 µm Au on a bare-SiO₂ dummy (1.0 µm thermal SiO₂ on Si), as in the [R1_TRAP sheet](RUNSHEET_R1_TRAP.md) (the R1_ONE sheet is the same plating step [verify]).

**Measure:** current calibration; thickness map; AFM roughness; gap width at top and bottom of the mold; plated area for the run [verify].

**Go / no-go:** 6.0 ± 0.5 µm; ≤ 10 % across the wafer [verify]; roughness ~8 nm rms after seed removal (PTB 8.3(5) nm); no nodules.

**One-week version (proposal, [verify]):** the plating calibration rides on the R1_ONE layer-50 plating step on a co-loaded dummy piece. Not needed for E1.

**Run and electrode:** R1_ONE; E2 only.

### E1 lift-off loop (E1 only)

**Purpose:** lift-off of 0.35 µm Au over 5 µm gaps, Au coverage of the 348 nm SiO₂ step at the mirror via (R1_ONE), and wedge bonding on evaporated Au.

**Stack / steps:** LOR + positive resist; L50 drawn; in-situ Ar pre-clean [verify whether needed on this die]; Ti 10 nm / Au 350 nm evaporated [verify thicknesses]; lift-off in NMP. R1_ONE: on a co-loaded piece across the 348 nm via step (the W3 stack).

**Measure:** LOR and resist profile (undercut); Ti and Au thickness on a witness; gap isolation at 10 V; Au continuity over the via step (cross-section); wedge-bond pull on the evaporated Au.

**Go / no-go:** all 5 µm gaps open, no Au across them; isolation > 100 MΩ at 10 V [verify]; Au continuous over the via step [verify]; wedge-bond pull [verify].

**One-week version (proposal, [verify]):** the layer-50-only second wafer is the electrode-step trial (gap lift-off and wedge bond). The via step is checked on a co-loaded W3 piece.

**Run and electrode:** R1_ONE; E1 only. The evaporator is a facility question ([below](#facility-confirmations)).

### W7 Bond-and-leak (step 19)

**Stack / steps:** dummy die with the planned Au bond pads (plated for E2, evaporated for E1), with the planned wire, tool and force [verify]. R1_ONE: the bond pads of the SNSPD-only die cells (120 × 200 µm, each cell two pads) and the A30 SNS and SNG pads. There is no T2v in R1_ONE.

**Measure:** trap die: Au-to-ground-fill leakage at ≤ 1 V before and after bonding; SNSPD-only die cells: pad to GND (a8) at ≤ 1 V before and after bonding; pull and shear.

**Go / no-go:** no leakage change (> 1 GΩ) [verify, carried from v3]; pull and shear acceptance [verify]. A leak opened by bonding goes to the team as a design question; no change is proposed here. Shorts under bond pads: Leibrandt 2009 (thin Si₃N₄).

**One-week version (proposal, [verify]):** the first bonds are on the SNSPD-only die cells of R1_ONE, in the same run as the detectors. A dummy die is not made separately.

**Run and electrode:** R1_ONE; both options.

## Facility confirmations

All items below are **[verify]**. Gold and tool compatibility, the evaporator, the plating tank (E2 only), holders and training apply before R1_ONE. NbN access is needed for R1_ONE.

- **Gold.** Which tools accept wafers carrying Au. On A30 and B60 dies the Ti/Au contacts (step 6) go on before the EBL, the RIE and the PECVD cap (steps 7 and 8), so those tools must accept it. Later Au steps: the layer-40 etch (step 11), the electrode step (12–15), the probe station and the dicing saw.
- **Evaporator (E1 only).** Which evaporator accepts Ti and Au for the E1 electrodes, and whether it has the in-situ Ar pre-clean. EBeam-Temescal-FC2800 is the tool named in the v4 pages for step 6 and for E1 [verify that it accepts Ti and Au for E1].
- **Step 3 and sputter.** Al source on the EBeam-Temescal-FC2800 for step 3 (raised mirror, lift-off only; no RIE recess step) [verify]; the substrate RF etch in the Sputter-AJA-* tool, used for the E2 seed and the W3 Ar pre-clean [verify].
- **NbN.** Which sputter tool and recipe (Dane 2017 is a Berggren-group process), and whether access goes through that group.
- **Plating (E2 only).** Whether a gold plating tank exists (Plating-U04 is named; chemistry unverified), its chemistry, and its minimum plated area. Not needed for E1.
- **Second wafer (layer 50 only).** Whether the facility can expose only layer 50 on a second wafer for the trap-only backup [verify].
- **Holders.** Piece holders for the short loops.
- **Training and booking.** The order in which tool trainings must be done.
