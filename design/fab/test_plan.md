> **Claude-authored.** Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09.

# Finished device test plan

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

Use the run map's die IDs throughout. Test before dicing and repeat applicable electrical checks through the carrier after packaging.

- [Test setup: what has to be on the bench](tests/00_SETUP.md)
- [Can the testing be simpler than a wafer-level test?](tests/05_SIMPLER_TESTING.md)

| Order | Module | Applies to |
|---|---|---|
| 1 | [Electrical tests](tests/01_ELECTRICAL.md) | Both runs (R1_TRAP and R1_FULL); the applicability list is at the top of the page. Detector and Al-mirror checks on A30 / B60 and the test dies only |
| 2 | [Cryogenic tests](tests/02_CRYOGENIC.md) | Full-stack test die first, then detector trap die (R1_FULL) |
| 3 | [Readout electronics](tests/03_READOUT.md) | Detector experiment |
| 4 | [First trapping](tests/04_TRAPPING.md) | Integrated detector; [NODET values](RUNSHEET_R1_TRAP.md#4-first-trapping-on-a-nodet-die-expected-values) for R1_TRAP |

> [!warning] Before R1_FULL
> The detector reconciliation and the draft limits are not closed. The v4 test dies are drawn and checked (2026-11-09). “Dietl 2025” is identified in the [L2 note](../research/research_notes/Loose%20ends%202026-11/L2_open_sources.md) and its limits remain **[verify]**. See [open checks](OPEN_DECISIONS.md).

## (a) Room-temperature electrical test

[Electrical protocol a1–a19](tests/01_ELECTRICAL.md); a4 retired in v4 (replaced by a15); a9 and a11 retired earlier.

## (b) Cryogenic SNSPD characterisation before trapping

[Measurements b1–b10](tests/02_CRYOGENIC.md).

## (c) Readout electronics chain

[Bias, amplification, filters and timing](tests/03_READOUT.md). The RF termination at the SNSPD leads is open.

## (d) First trapping checklist

[Loading, transport, readout and heating](tests/04_TRAPPING.md).
