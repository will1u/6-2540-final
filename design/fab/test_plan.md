> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Finished device test plan

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

Use the run map's die IDs throughout. Test before dicing and repeat applicable electrical checks through the carrier after packaging.

| Order | Module | Applies to |
|---|---|---|
| 1 | [Electrical tests](tests/01_ELECTRICAL.md) | Both runs; detector checks where present |
| 2 | [Cryogenic tests](tests/02_CRYOGENIC.md) | Full-stack test die first, then detector trap die |
| 3 | [Readout electronics](tests/03_READOUT.md) | Detector experiment |
| 4 | [First trapping](tests/04_TRAPPING.md) | Integrated detector; [NODET values](RUNSHEET_R1_TRAP.md#4-first-trapping-on-a-nodet-die-expected-values) for R1_TRAP |

> [!warning] Before R1_FULL
> Reconcile v3.1 predictions and T9 acceptance with the generated layout. “Dietl 2025” remains unresolved. See [open checks](OPEN_DECISIONS.md).

## (a) Room-temperature electrical test

[Electrical protocol a1–a14](tests/01_ELECTRICAL.md); a9/a11 retired.

## (b) Cryogenic SNSPD characterisation before trapping

[Measurements b1–b9](tests/02_CRYOGENIC.md).

## (c) Readout electronics chain

[Bias, amplification, filters and timing](tests/03_READOUT.md).

## (d) First trapping checklist

[Loading, transport, readout and heating](tests/04_TRAPPING.md).
