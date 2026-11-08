> **Claude-authored.** Reorganized 2026-11-08 from the project fabrication notes.

# Sapphire and fused silica alternatives

[Variants](../VARIANTS.md) · [Baseline stack](../STACK.md) · [Open decisions](../OPEN_DECISIONS.md)

Handling changes to the baseline; HR Si remains the current substrate.

The Al ground plane makes RF substrate loss largely irrelevant (Romaszko 2020 Sec. 3.2; Leibrandt Q 100 → 150 with the ground plane). The NbN always grows on the PECVD spacer, so the substrate does not change NbN growth. What changes is handling.

| Step | Sapphire | Fused silica |
|---|---|---|
| Wafer sensing (loadlocks, MLA, EBL height sensor, PECVD/RIE wafer-present sensors) | Transparent wafers are often not detected or focused. Dietl 2025 used a **temporary 2 µm backside poly-Si** for handling on fused silica. For us a permanent backside coating (poly-Si by LPCVD before step 3, or a metal) is fine because nothing is imaged through the back [verify tool rules]. MLA150: use the AirAF variant on transparent substrates [verify] | same |
| 1 Marks | The Si RIE does not apply. Use Ti/Au or Cr/Au lift-off marks, or a Cl₂/BCl₃ sapphire etch (slow) [verify] | CHF₃/CF₄ RIE 1 µm into the glass, or metal marks |
| 2 D1 | No thermal oxide: use PECVD SiO₂ 1 µm, or skip | Optional (the substrate is already SiO₂) |
| 9 D2 stress | Sapphire CTE ≈ 7–8 ppm/K vs SiO₂ ≈ 0.5: extra thermal stress on cooldown [verify]. Re-tune the backside balance on a witness | Good CTE match; intrinsic PECVD stress still needs balancing |
| Ellipsometry | Over the M1 area the stack is opaque, so measure there. On transparent areas, backside reflections spoil the fits | same |
| EBL charging | No issue: the blanket NbN film and Al are conductive at step 7. Ground them through the clip | same |
| 5 K thermal | Sapphire conducts heat well | Glass conducts poorly. RF heating of the SNSPD (Hampel's residual limit) is worse [inference] |
| 18 Dicing | Hard: diamond blade, slow feed [verify] | Dedicated glass blade [verify] |
