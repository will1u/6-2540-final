> **Claude-authored.** Reading pointers into Dietl et al. 2025 for the test-setup pages, 2026-11-10. Read from the arXiv PDF (v2, 16 pages), pages 4–12. Pages 1–3 and 13–16 (Appendices C–E, references) were not read for this note.

# T1: Dietl 2025, what the wafer test is and what it needs

**Source:** M. Dietl et al., "Test and characterization of multilayer ion traps on fused silica", arXiv:2505.21284 (bib key `Dietl2025`). This note says where to look; read the pages themselves before relying on a number.

## Where to read

| Question | Where in the paper | What is there |
|---|---|---|
| Why test electrically at all? | Sec. 3, page 6, the paragraph after Eq. 2 | Optical inspection sees only the top metal layer, so it is enough for single-layer traps; electrical testing is preferred for multilayer traps because lower-layer defects are hidden. |
| What hardware? | Sec. 3, page 6, last paragraph | 120 probe needles with 40 µm tips, one per bond pad; ambient pressure, 295 K. The words "probe card" do not appear on pages 4–12. |
| Why two pads per electrode? | Sec. 3, page 7, first paragraph; Fig. 2(a) | A needle dents the metal, so needles never touch an electrode. Each electrode is a loop between two bond pads; continuity is measured pad to pad through the electrode. |
| The limits | Table 2, page 7 | Continuity: 1 mA forced, pass 0–100 mV (and 0.8–1.3 mA measured). Leakage (DC): 50 V, pass 0–100 nA. Leakage (RF): 300 V, pass 0–100 nA. Resistance (DC and RF): 5 mV, pass 0–50 Ω. Two temperature-sensor rows. |
| Why 300 V on the RF electrode? | Sec. 3, page 7, third paragraph | Chosen low enough to avoid breakdown through air. Leakage tests run twice to catch a short made by the first pass. No breakdown was seen. |
| How long, how many steps? | Sec. 3, page 7 | 480 steps per trap in about 7.8 s; a trap stops at its first failure. (The "540 measurements" quoted elsewhere in this repo came from a conference abstract, not from this paper.) |
| Yield | Sec. 3, pages 7–8; Fig. 2(b) | 54 % (258 of 477 chips); 29.8 % fail leakage with a pattern that repeats with the 3 × 3 reticle; 15.5 % fail continuity, mostly at the wafer edge. |
| What the test does not cover | Sec. 5, page 10, third paragraph | It runs at room temperature while the traps run cold; a cryogenic wafer probe is left for future work. |
| A failure the wafer test did not prevent | Sec. 4.2, page 10, second paragraph | After three cooldowns two trapping sites stopped working and the cause could not be assigned to the trap or the setup. The authors plan enough DC lines to test each loop from outside the cryostat. |
| DC filters used when trapping | Sec. 4.2, page 9 | First-order RC filters with a 5 kHz corner. |
| Cold resistance measurement | Sec. 4.1, page 8; Fig. 3(a) | Four-wire measurement in a cryogenic setup with four needles, 10–300 K. |

## Also useful for the RF pages

| Question | Where | What is there |
|---|---|---|
| RF power formulas | Sec. 2.2, Eq. 1; Appendix A, Eqs. 9–12 (pages 11–12) | Ohmic and dielectric loss of an RF electrode treated as a distributed resistor charging a capacitor. The effective series resistance is one third of the electrode's end-to-end resistance (Eq. 11). |
| Capacitances and power of three real traps | Table 1, page 5 | 28, 42 and 12 pF; all at 22 MHz and 160 V with tan δ = 10⁻³. |
| RF over bare Si | Sec. 2.2, page 5, last paragraph | Where the RF field reaches low-resistivity Si the trap ran hotter than the model predicted; the model has no Si absorption. |
| RF-to-DC coupling at crossings | Sec. 2.1, page 4, first paragraph | 14 fF without a ground layer between the RF and DC lines, 0.6 fF with one. |

## What differs from this project (facts from our own files)

| | Dietl 2025 | This project |
|---|---|---|
| Metal layers | Three Al layers; routing is buried | One Au layer on top, plus a local Al mirror on the detector dies (`fab/STACK.md`) |
| Pads per electrode | Two (loop) | One (`gds/trap_die_v4_A30_pads.csv`) |
| Chips per wafer | 477 on 200 mm | 8 dies per run (`fab/RUN_PLAN.md`) |
| Probing | 120 needles at once | Manual probing planned (`fab/RUNSHEET_R1_TRAP.md`, step 17) |

## Corrections to earlier notes in this repo

- `fab/tests/01_ELECTRICAL.md` line 8 and `Loose ends 2026-11/L2_open_sources.md` say the 120 needles were not found in the paper. They are on page 6. What is not on pages 4–12 is the phrase "probe card", a comb structure, or a measured flashover voltage.
- The Table 2 limits quoted in `fab/tests/01_ELECTRICAL.md` (a1–a3) match the PDF.
