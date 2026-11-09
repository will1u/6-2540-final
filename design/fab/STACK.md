> **Claude-authored.** Rewritten for v4 2026-11-09.

# Layer stack and thermal budget

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

> [!note] Electrode Au: both options shown
> E1 = Ti 10 nm / Au 350 nm lift-off. E2 = 6 µm plated Au. The team has not chosen between them ([open decisions](OPEN_DECISIONS.md)). Rows that depend on the choice say so. The rest of this page is the adopted v4 stack.

> [!note] Scope
> v4 local-mirror architecture ([LOCAL_MIRROR.md](variants/LOCAL_MIRROR.md) H.1–H.4; team decisions of 2026-11-08 in [decisions](../../notes/decisions.md); DESIGN_LOG steps 25–28). No die-wide Al, no 10 µm SiO₂ (D2), no ITO. A30 and B60 dies carry the Al mirror, SiO₂ spacer, NbN, SiO₂ cap and Au electrodes. NODET dies carry no Al. The [R1_TRAP sheet](RUNSHEET_R1_TRAP.md) skips steps 4–8 (spacer, NbN, leads, nanowire, cap). Whether NODET dies in other runs get steps 4–8 is not stated in the sources [verify]. Optical values are TMM with effective medium, not RCWA.

## Readout cross section

![v4 trap stack: readout window, slot, NODET die, mirror ground via and SNSPD contact](figures/stack_v4.svg)

Stack under the readout window, listed bottom to top. Values are v4 (DESIGN_LOG steps 25, 26, 28; LOCAL_MIRROR H.3).

| Layer | Thickness | Role / note |
|---|---|---|
| HR FZ Si | ~525 µm [verify]; ρ > 20 kΩ·cm (was > 10⁴ Ω·cm) | RF substrate with no ground plane. This Si is what the local-mirror design needs (NIST practice; LOCAL_MIRROR H.4) |
| Thermal SiO₂ (D1) | 1.0 µm | Isolation under the mirror and electrodes; also on the backside |
| Al-1%Cu local mirror (L10) | 450 nm (was 150 nm) | Strip |y| ≤ 20 µm, x = −2240 … +268 µm (A30); it lies under the window. Opaque (≥ 100 nm). Not under the RF rails |
| PECVD SiO₂ spacer | 238 ± 10 nm | Second-order cavity spacer for 493 nm. 64 nm (first order) is optically equal (DESIGN_LOG step 26) but sits closer to Al hillocks. **Avoid ≈ 148 nm** (absorption node) |
| NbN meander (L20) | 7 nm; 130 / 200 nm line / pitch; 160 lines | Lines 36 µm (A30) / 69 µm (B60) long, with end blocks and tabs under Au (`gds/snspd_geom.py`, step 24) |
| Ti/Au contacts (L22) | 10 / 350 nm [verify for contacts] | NbN tabs to the slot contact pads; EBL marks. Contacts only: no buried leads |
| HSQ (on wires only) + PECVD SiO₂ cap | **160 ± 10 nm** total over the wires (was 80 ± 10) | Window floor and optical matching layer, since vacuum now sits on it. Cap thickness = 160 − measured remaining HSQ. The floor is 0.40 µm above the mirror (238 + 160 nm) |
| Au window walls (L50) | E1: 0.35 µm; E2: 6 µm | Window is a 30 × 30 µm hole (A30) or 60 × 30 µm (B60) in the electrode Au. Both options shown; choice open |
| Vacuum; ion | Ion planar height 49.98 µm at readout. Over the window: A30 −1.19 µm (E2), ≤ −0.37 µm (E1); B60 −2.04 µm (E2), ≤ −0.55 µm (E1) | Recess from the grounded floor (steps 25, 26) |

**Optics (v4, DESIGN_LOG step 26, `09c`).** Absorption in NbN at 493 nm ≈ 0.66 with a 159–160 nm cap (±10 nm box mean 0.645; worst corner 0.596). The earlier 80 nm cap gives 0.44. `make_chip.py` and the simulation metadata state 160 nm (corrected 2026-11-09; geometry unchanged); 160 nm is the deposition target (DESIGN_LOG overhang audit). The model reads ~10 % pessimistic against Hampel. These are TMM effective-medium numbers, not RCWA. `09b` (vacuum above the cap) is superseded by `09c` for v4.

### (a) Readout window, top to bottom (A30; B60 has a 60 × 30 µm opening)

1. Vacuum; ion at 49.98 µm planar, lowered over the window by the recess in the table above.
2. HSQ + PECVD SiO₂ cap, 160 ± 10 nm. Its top surface is the window floor, 0.40 µm above the mirror.
3. NbN meander, 7 nm.
4. PECVD SiO₂ spacer, 238 nm.
5. Al-1%Cu mirror, 450 nm, under the window, grounded through the mirror via and the Au ground fill.
6. Thermal SiO₂ (D1), 1.0 µm.
7. HR Si, ρ > 20 kΩ·cm.

Beside the window the Au walls (L50) sit on the cap: 0.35 µm (E1) or 6 µm (E2) deep.

### (b) Slot region with the Au SNSPD leads over the mirror, top to bottom

The slot is |y| < 12.5 µm, x < 175 µm (A30). Two 5 µm leads sit at |y| = 5 µm. The mirror lies under the whole slot.

1. Vacuum.
2. Au SNSPD lead (part of L50): E1 Ti 10 nm / Au 350 nm lift-off, or E2 6 µm plated Au on the L50 seed.
3. HSQ + PECVD SiO₂ cap, 160 ± 10 nm. The cap is opened (L40) only at the contact pad: the lead reaches the L22 Ti/Au pad (27 × 7 µm, x = 143 … 170 µm), which is the contact to the NbN tab.
4. PECVD SiO₂ spacer, 238 nm.
5. Al-1%Cu mirror, 450 nm, grounded through the mirror via at (−2140, 130) µm.
6. Thermal SiO₂ (D1), 1.0 µm.
7. HR Si.

No Au or Ti is buried under the centre DC; the leads are the only Au in the slot.

### (c) NODET die (R1_TRAP), top to bottom

1. Vacuum.
2. Au electrodes (L50): E1 Ti 10 nm / Au 350 nm lift-off, or E2 Ti 15 nm / Au 50 nm seed with 6 µm plated Au (steps 12–15 as written).
3. Thermal SiO₂ (D1), 1.0 µm. No spacer, NbN or cap (R1_TRAP skips steps 4–8).
4. HR Si, ρ > 20 kΩ·cm.

No Al in the stack. The Au sits directly on thermal SiO₂, and the 5 µm gaps expose it.

### (d) Elsewhere on A30 and B60 (RF rails, outer DC segments)

Top to bottom: vacuum; Au electrodes (E1 or E2); PECVD SiO₂ spacer and cap; thermal SiO₂ (D1); HR Si. No Al below. The spacer and cap are exposed in the gaps (LOCAL_MIRROR H.4).

## Layer table (v4)

| GDS layer | Name | Material | Thickness | How patterned | Purpose |
|---|---|---|---|---|---|
| 1 | MARK | Si | ~1 µm etch | MLA150 + RIE (step 1) | Alignment marks |
| – | D1 | Thermal SiO₂ | 1.0 µm, both sides | Oxidation, blanket (step 2) | Isolation under the mirror and electrodes |
| 10 | M1 | Al-1%Cu | 450 nm | Drawn (not inverted): route A etch or route B lift-off (step 3) | SNSPD mirror and its ground; grounded to the Au fill through the mirror via |
| – | Spacer | PECVD SiO₂ | 238 ± 10 nm | Blanket (step 4) | Cavity spacer for 493 nm |
| 20 | NbN | NbN | 7 nm | Blanket sputter (step 5); meander by EBL and CF₄ etch (step 7) | Detector |
| 22 | Ti/Au | Ti/Au | 10 / 350 nm [verify] | Lift-off (step 6) | NbN tab to slot contact pads; EBL marks. Not leads |
| – | Cap | HSQ on wires + PECVD SiO₂ | 160 ± 10 nm total over the wires | HSQ by EBL (step 7); PECVD (step 8) | Optical matching layer; window floor |
| 40 | Openings | SiO₂ (cap and spacer) | ≈ 160 nm (SNSPD contacts); ≈ 0.40 µm (mirror via, spacer + cap) to the Al | Thin positive resist ≈ 1.3 µm; CHF₃ / CF₄ / Ar; ≈ 1 min [verify for 0.40 µm] (step 11) | SNSPD contact and mirror ground openings; stops on Al and Au |
| 50 | Electrodes | Au; Ti adhesion (E1 Ti 10 nm; E2 Ti 15 nm / Au 50 nm seed) | E1: 0.35 µm Au [verify thickness]; E2: 6 µm plated Au | E1: LOR + positive resist, MLA150, lift-off in NMP, in-situ Ar pre-clean before Ti (steps 12v–15v). E2: steps 12–15 as written [verify seed on the thin stack] | RF and DC electrodes, ground fill, SNSPD leads in the slot, window walls |
| 100, 101 | Notes, outlines | – | – | – | Not fabricated |

## Thermal budget

| Step | Max T | Time at T | Note |
|---|---|---|---|
| 2 Thermal SiO₂ (D1) | ~1000–1100 °C [verify furnace recipe] | hours | Before Al and NbN, so no limit applies |
| 3 Al sputter (450 nm) | < 100 °C [verify] | min | Sputter heating not quantified [verify] |
| 4 Spacer PECVD | ≤ 300 °C | ~5 min | First anneal of the Al. Check the Al for hillocks after this step (darkfield) |
| 5 NbN sputter | ~RT (unheated; plasma heating unquantified) | min | Dane 2017 recipe is unheated |
| 6, 7, 11, 13 resist bakes | ≤ 115 °C (HSQ bake per datasheet [verify]) | min | – |
| 8 Cap PECVD (160 nm) | ≤ 300 °C | min | – |
| 9, 10 | Skipped in v4 (10 µm D2 removed) | – | No long 300 °C exposure |
| 14 Plating bath (E2 only) | ~50–65 °C [verify bath datasheet] | ~30–60 min | No plating step on E1 |
| 19 Die attach / bake-out | ≤ 150–200 °C [verify adhesive] | hours–days | Au–Al intermetallics on bakes [inference] |

| Limit | Value | Source |
|---|---|---|
| Al hillocks / voids | significant at ~350 °C; Al-1%Cu or a Ti/TiW cap suppresses them | SINTEF; JoVE M1 step ("prevent whisker formation during bakeout") |
| **Rule for this run** | **≤ 300 °C for every step after step 3** | team inference from the two lines above |
| NbN, inert ambient | Tc stable to 500 °C | arXiv:2501.07780 |
| NbN, uncapped in O₂ | Tc drops | Ioffe paper (research report) |
| NbN in air | Nb₂O₅ grows as d_ox = 0.78 t^0.17 nm (t in days): ~0.8 nm after 1 day | Medeiros 2019 |

## Changed from v3

- Substrate: ρ > 10⁴ Ω·cm → ρ > 20 kΩ·cm.
- Layer 10: die-wide inverted Al plane → local mirror, |y| ≤ 20 µm, x = −2240 … +268 µm (A30); 150 nm → 450 nm.
- RF ground plane removed: no Al under the RF rails.
- 10 µm PECVD SiO₂ (D2) removed, with its gap etch and its thermal load (≤ 300 °C, 1–2 h). Layer 45 (protect) removed.
- Cap: 80 ± 10 nm → 160 ± 10 nm total over the wires. Spacer unchanged at 238 nm.
- Window floor: bare SiO₂ at the top of the 10 µm D2 (6 µm pocket) → the cap, 0.40 µm above the mirror.
- Electrodes: 6 µm plated Au only → E1 0.35 µm lift-off or E2 6 µm plated (open).
- SNSPD leads: buried Ti/Au under the centre DC (L22) → Au leads in the slot (L50). L22 is contacts only.
- L40 openings: through about 10.3 µm of D2 → through the cap and spacer only (SNSPD contacts ≈ 160 nm; mirror via ≈ 0.40 µm; no probe opening on the trap die: the mirror is checked on the test die, T10, T11 and the T4/T4b probe pads).
- Mirror ground via: moved to (−2140, 130) µm, just past the RF open end (was (−2450, 130) µm).
- L10 cut-outs under the SNSPD pads and at the mark sites removed (no Al there).
- Window recess: −1.38 µm (A30, v3) → −1.19 µm (A30, E2) or ≤ −0.37 µm (E1).
- Absorption in NbN: ≈ 0.40 (v3, with D2 and no ITO) → ≈ 0.66 (v4, 160 nm cap; DESIGN_LOG step 26).
- Mirror-to-ground resistance: the < 10 Ω test → T10 strip four-point, about 5 Ω expected at 450 nm [team calc]; acceptance limit [verify]. At 150 nm the path was ≈ 14–18 Ω (DESIGN_LOG step 25 [team calc]).
- Hillock check: now also after the spacer deposition (step 4).
- Thermal: plating runs only on E2.
- ITO (layers 30, 31) and the M1 via (layer 24) remain removed.
