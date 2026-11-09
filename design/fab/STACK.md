> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Layer stack and thermal budget

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

> [!warning] Architecture changed to v4 (2026-11-08)
> The team chose the local-mirror architecture (no die-wide Al, no 10 µm D2), leads in a slot along the centre DC, A30 and B60 detector dies (B60 briefly dropped, then kept), and the same no-Al stack for R1_TRAP ([decisions](../../notes/decisions.md); DESIGN_LOG step 25). The GDS is now v4 (`gds/trap_die_v4_*`). **This page still describes the v3 baseline process.** It must be rewritten before any run; the rewrite waits on the electrode Au choice (E1 lift-off vs E2 plated). Do not fabricate from it.

> [!note] Scope
> Full-stack architecture with a die-wide Al plane and 10 µm D2. [R1_TRAP](RUNSHEET_R1_TRAP.md) omits spacer/NbN/cap. Optical values below are **earlier v3 estimates at 50 % fill**, pending reconciliation for v3.1.

## Readout cross section

All values are DESIGN_LOG steps 2, 6, 9, 9b and 10.

| Layer                           | Thickness                                                                                                                                | Role / note                                                                                                                             |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| HR FZ Si                        | ~525 µm [verify]                                                                                                                         | RF substrate loss largely irrelevant under the Al plane (Romaszko 2020 Sec. 3.2; Leibrandt 2009)                                        |
| Thermal SiO₂ (D1)               | 1.0 µm                                                                                                                                   | Isolation; also on the backside                                                                                                         |
| Al-1%Cu (M1)                    | 150 nm                                                                                                                                   | Ground plane and optical mirror; ≥ 100 nm is opaque (TMM: 50 nm transmits 0.12 %)                                                       |
| PECVD SiO₂ spacer               | 238 ± 10 nm                                                                                                                              | Second-order cavity spacer. 64 nm (first order) is optically equal but sits closer to Al hillocks. **Avoid ≈ 148 nm** (absorption node) |
| NbN meander                     | 7 nm; current width/pitch 130/200 nm                                                                                                     | Current v3.1: 160 lines; line regions 36 × 32 µm (A30) / 69 × 32 µm (B60); [revision comparison](VARIANTS.md#detector-revision)         |
| HSQ (on wires only) + PECVD cap | 80 ± 10 nm total over the wires                                                                                                          | Cap thickness = 80 − measured remaining HSQ                                                                                             |
| PECVD SiO₂ (D2)                 | 10.0 µm                                                                                                                                  | Stays over the detector. Its top surface is the window floor the ion sees (bare SiO₂)                                                   |
| Au walls (centre DC, 5 µm rims) | 6.0 µm                                                                                                                                   | Window 30 × 30 µm (A30) or 60 × 30 µm (B60); pocket depth 6 µm                                                                          |
| Vacuum; ion                     | h ≈ 50.1 µm above the Au top, minus the 3-D recess effect over the bare-SiO₂ window: −1.38 µm (A30), −2.50 µm (B60) (DESIGN_LOG step 17) | –                                                                                                                                       |

Expected NbN absorption ≈ 0.40 (worst ±10 nm corner 0.39) with no ITO, vs 0.53 for the v2 two-ITO stack. The model reads ~10 % pessimistic against Hampel. These are TMM effective-medium numbers, not RCWA (DESIGN_LOG steps 9b and 17).

Under the trap electrodes elsewhere: Si / D1 / M1 / spacer / cap / D2 / Ti-Au seed / 6 µm Au. Ground is ~10.3 µm below the Au. The same Al is the SNSPD mirror (238 nm below the NbN) and the RF ground plane (10.3 µm below the Au). The [local-mirror comparison](variants/LOCAL_MIRROR.md#h0-why-the-baseline-has-a-thick-d2-ground-plane-and-mirror-together) explains the two distances.

## Thermal budget

| Step | Max T | Time at T | Note |
|---|---|---|---|
| 2 Thermal oxide | ~1000–1100 °C [verify furnace recipe] | hours | Before Al and NbN, so no limit applies |
| 3 Al sputter | < 100 °C [verify] | min | – |
| 4 Spacer PECVD | ≤ 300 °C | ~5 min | First anneal of the Al |
| 5 NbN sputter | ~RT (unheated; plasma heating unquantified) | min | Dane 2017 recipe is unheated |
| 6, 7, 11, 13 resist bakes | ≤ 115 °C (HSQ bake per datasheet [verify]) | min | – |
| 8 Cap PECVD | ≤ 300 °C | min | – |
| 9 D2 PECVD (front + back) | ≤ 300 °C | cumulative ~1–2 h [verify rate] | Hottest long step after Al and NbN. JoVE ran 350 °C; we cap at 300 °C because of the Al |
| 14 Plating bath | ~50–65 °C [verify bath datasheet] | ~30–60 min | – |
| 19 Die attach / bake-out | ≤ 150–200 °C [verify adhesive] | hours–days | Au–Al intermetallics on bakes [inference] |

| Limit | Value | Source |
|---|---|---|
| Al hillocks / voids | significant at ~350 °C; Al-1%Cu or a Ti/TiW cap suppresses them | SINTEF; JoVE M1 step ("prevent whisker formation during bakeout") |
| **Rule for this run** | **≤ 300 °C for every step after step 3** | team inference from the two lines above |
| NbN, inert ambient | Tc stable to 500 °C | arXiv:2501.07780 |
| NbN, uncapped in O₂ | Tc drops | Ioffe paper (research report) |
| NbN in air | Nb₂O₅ grows as d_ox = 0.78 t^0.17 nm (t in days): ~0.8 nm after 1 day | Medeiros 2019 |
