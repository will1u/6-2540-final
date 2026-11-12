> **Claude-authored.** Rewritten for v4 2026-11-09; mirror 100 nm 2026-11-09; final stack 2026-11-12.

# Steps 0 to 3 substrate, base SiO₂ and raised Al mirror

[Traveler](../TRAVELER.md) · [R1_TRAP sheet (superseded for R1_ONE)](../RUNSHEET_R1_TRAP.md) · [Process checks](../process_checks.md) · [Open decisions](../OPEN_DECISIONS.md)

Which dies: on R1_ONE every die goes through steps 0 to 3. The NODET die gets only the four corner marks in step 3 (Al, outside the trap). The A30, B60 and SNSPD-only dies get the full step 3 (mirror and marks). After Al deposition, keep subsequent steps at or below 300 °C.

Wafer ID: ________ Run: ________ Operator: ________ Generator revision: ________

## 0. Wafer prep and clean

- **Purpose:** clean HR FZ Si start, ρ > 20 kΩ·cm [verify spec sheet] (was > 10⁴ Ω·cm). The RF runs over thin SiO₂ on this Si with no ground plane (LOCAL_MIRROR H.4).
- **Tool:** Acid-Etch-General-* hood.
- **Recipe:**
  - Scribe the ID on the backside edge.
  - Piranha 15 min (JoVE substrate step).
  - DI rinse, spin dry. RCA clean if the furnace rules require it before step 2 [verify MIT.nano furnace cleanliness rules].
- **Inspect:** particles under a darkfield microscope.
- **Also:** set aside **≥ 3 dummy Si wafers** for W1/W3/W5.
- [ ] Done — date: ____ operator: ____ notes: ____

## 1. L1 alignment marks (Si RIE ~1 µm)

**REMOVED 2026-11-12.** The Si-etched marks are gone. The layer-1 mark shapes are now written in Al in step 3, in the same exposure and lift-off as layer 10. This step does nothing on R1_ONE. The heading is kept so older links still resolve.

- [ ] Done — date: ____ (removed; not used on R1_ONE) notes: ____

## 2. Thermal SiO₂ D1, ~1 µm, both sides

- **Purpose:** the base SiO₂: isolation of the Al mirror and the Au electrodes from the Si. Under the mirror it is 1.0 µm (no recess).
- **Base SiO₂ range:** 1.0 µm nominal. Accept 0.5–2.0 µm as supplied (sim 22b: cold chip capacitance 2.88 to 2.38 pF on E2 across that range; warm, a thin base makes room-temperature RF worse, see [STACK](../STACK.md#base-sio₂-thickness-sim-22b)).
- **Which base the team uses:** [verify which the team does]
  - If the wafers arrive with 0.5–2.0 µm of thermal SiO₂: **skip step 2**. Measure the thickness on arrival.
  - If the wafers are bare: wet oxidation to 1.0 µm (tool below) [verify time/T on the tool chart], or a PECVD SiO₂ base. Hampel 2023 used 150 nm PECVD SiO₂ and Todaro 2021 used 134 nm (cited as examples; not our recipe).
- **Tool:** Ox-Tube-Lindberg or Tube-OxAnneal-Expertech-CTR200 (for thermal); PECVD tool as in step 4 (for the PECVD option).
- **Recipe reference:** JoVE used 0.5 µm at 900 °C for 4.5 h plus 0.2 µm LPCVD SiN. Romaszko gives 1–2 µm as typical for D1.
- **Target:** 1.0 µm nominal; accept 0.5–2.0 µm; measure by ellipsometry on 5 points.
- **Hazards:** none.
- [ ] Done — date: ____ operator: ____ t_SiO₂ (5 pts): ____ base route (skipped / thermal / PECVD): ____ notes: ____

## 3. M1 raised Al local mirror and marks (L10 and L1)

- **Purpose:** SNSPD mirror (238 nm PECVD SiO₂ spacer below the NbN; DESIGN_LOG steps 9, 26), the ground of that mirror (tied to the Au ground fill through the mirror via, step 11), and the alignment marks for the later layers. This is not an RF ground plane: v4 has no Al under the RF rails.
- **Thickness:** **100 ± 10 nm**, evaporated Al, raised on the base SiO₂. No recess etch. History: 150 nm (v3) → 450 nm (2026-11-08) → 100 nm inlaid (2026-11-09) → 100 nm raised (2026-11-12, team decision, [decisions](../../../notes/decisions.md)). The raised mirror lifts the RF null 0.13–0.16 µm, the same as the inlaid one (DESIGN_LOG step 39).
- **Marks:** the layer-1 alignment marks are written in this same Al, in the same exposure and lift-off as layer 10. The Si mark etch of the old step 1 is gone.
- **Shape (drawn, not inverted):** |y| ≤ 20 µm from x = −2240 µm to just past the detector (x = +268 µm on A30; +284.5 µm on B60), plus a branch under the Au ground fill to the mirror ground via at (−2140, 130) µm. Nothing under the RF rails. Four corner marks on NODET dies.
- **Tool:** MLA150; EBeam-Temescal-FC2800 [verify Al source]; lift-off bath (NMP or Remover PG) [verify].
- **Recipe:**
  - **3a Resist.** LOR + positive resist [verify thicknesses]. MLA150. Expose layers 10 and 1 **drawn, together** (the resist is open where the mirror and the marks go). Layer 10 data and alignment are unchanged.
  - **3b Al.** E-beam evaporate Al 100 nm through the same resist. [verify Al thickness on the tool monitor]
  - **3c Lift-off.** NMP or Remover PG [verify]. The Al stays where it was evaporated onto the base SiO₂; the surface is not etched.
  - The Al deposition and lift-off follow Hampel 2023 (arXiv:2302.01462), which made a 50 nm e-beam evaporated Al mirror by lift-off. The 100 nm thickness is this design's value, not Hampel's; unproven until witness loop W8 passes.
- **Layer / align:** step 3 is the first layer: it aligns to the wafer flat. Layers 22, 40 and 50 later align to the Al marks made here. Layers 10 and 1 share one exposure, so their relative position is set by the layout [inference].
- **Inspect:**
  - Lift-off complete; no Al flags or residue.
  - Mark crosses sharp, sized as drawn, in Al [verify].
  - Rsq by 4-pt on a co-deposited witness: expected 0.30–0.40 Ω/sq [team calc, ρ 3–4 µΩ·cm] [verify].
  - Darkfield for hillocks / whiskers before the spacer, and again after the spacer deposition (step 4).
  - Mirror shape against the drawing, including the branch to the ground via.
  - Mirror strip resistance: not measured on R1_ONE (no T10 on this run; not drawn). Expected 18.8–25.1 Ω (62.75 squares) is a calculated value [`sim/10c`, DESIGN_LOG step 37]. Acceptance not set [verify].
  - Cut-outs: none (no Al under the SNSPD pads or the mark sites beyond the marks themselves).
- **Hazards:** from here on the **≤ 300 °C rule** applies to every die.
- [ ] Done — date: ____ operator: ____ t_Al: ____ Rsq (co-loaded): ____ mark crosses: ____ notes: ____

Continue: [next stage](02_DETECTOR.md).
