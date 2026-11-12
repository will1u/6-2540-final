> **Claude-authored.** Rewritten for v4 2026-11-09; mirror 100 nm inlaid 2026-11-09; run R1_ONE and raised mirror 2026-11-12 (the inlaid mirror is superseded).

# Finished device test plan

[Fab overview](README.md) · [Variants](VARIANTS.md) · [Open decisions](OPEN_DECISIONS.md)

Use the run map's die IDs throughout. Test before dicing and repeat applicable electrical checks through the carrier after packaging.

- [Test setup: what has to be on the bench](tests/00_SETUP.md)
- [Can the testing be simpler than a wafer-level test?](tests/05_SIMPLER_TESTING.md)

| Order | Module | Applies to |
|---|---|---|
| 1 | [Electrical tests](tests/01_ELECTRICAL.md) | Run R1_ONE (replaces R1_TRAP and R1_FULL); the applicability list is at the top of the page. Detector and Al-mirror checks on the A30 die and the SNSPD-only die cells |
| 2 | [Cryogenic tests](tests/02_CRYOGENIC.md) | R1_ONE: SNSPD-only die first (test 1), then the A30 with RF (test 2), the trap cryostat tests (tests 3 and 4) |
| 3 | [Readout electronics](tests/03_READOUT.md) | Detector experiment |
| 4 | [First trapping](tests/04_TRAPPING.md) | Integrated detector (A30); [NODET values](RUNSHEET_R1_TRAP.md#4-first-trapping-on-a-nodet-die-expected-values) for the NODET dies |

### R1_ONE: the four tests and the dies that serve them

One wafer, a 3 × 3 block of 10 × 10 mm dies: 4 A30, 1 B60 (spare), 2 SNSPD-only (`snspd_die_v4`), 2 NODET. No TEST or TEST_TRAP die. An optional second wafer exposes only layer 50 (Au) and is the trap-only backup.

| Test | Where | Die in R1_ONE |
|---|---|---|
| 1. SNSPD alone | SNSPD test setup [verify: not described in the repo] | SNSPD-only die (8 detector cells D1–D8, plus T3 and T11) |
| 2. SNSPD with trap RF applied | SNSPD test setup [verify] | A30 die |
| 3. Trap alone | Trap chamber | NODET die |
| 4. SNSPD in the trap chamber | Trap chamber | A30 die |

The B60 die is a spare; the B60 meander exists only on that one die.

> [!warning] Before R1_ONE
> The detector reconciliation and the draft limits are not closed. The v4 test dies are drawn and checked (2026-11-09) and are replaced in R1_ONE by the SNSPD-only die (2026-11-12). “Dietl 2025” is identified in the [L2 note](../research/research_notes/Loose%20ends%202026-11/L2_open_sources.md) and its limits remain **[verify]**. See [open checks](OPEN_DECISIONS.md).

## (a) Room-temperature electrical test

[Electrical protocol a1–a19](tests/01_ELECTRICAL.md); a4 retired in v4 (replaced by a15); a9 and a11 retired earlier.

## (b) Cryogenic SNSPD characterisation before trapping

[Measurements b1–b10](tests/02_CRYOGENIC.md).

## (c) Readout electronics chain

[Bias, amplification, filters and timing](tests/03_READOUT.md). The RF termination at the SNSPD leads is open.

## (d) First trapping checklist

[Loading, transport, readout and heating](tests/04_TRAPPING.md).
