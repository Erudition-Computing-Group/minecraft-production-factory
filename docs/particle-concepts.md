# Particle effect concepts (24)

Each concept lists visual, motion logic, and the math complexity the Builder Agent must implement.

## Layer 1 — Cosmetic & vanity (player store items)

1. **Galactic Rings aura** — rotating tilted plane of blue/purple/silver sparkles around torso. Circle parametric eq (`sin`/`cos`) with a variable tilt angle; slight random velocity.
2. **Cybernetic Glitch steps** — neon cyan digital runes + black/white static erupting from feet only while moving. Triggered on `PlayerMoveEvent`; foot-level spawn, zero vertical velocity, 5–10 tick lifetime.
3. **Phoenix Rise wings** — two jagged frames of slow-drifting red/orange embers forming wings on the back. Bezier curves / vector table relative to back (yaw/pitch/roll); oscillating vertical offsets for flapping.
4. **Soul-Fire Halo crown** — swirling erratic ring of blue soul-fire above head, shedding gray smoke. Simple circle eq with high `extra` (speed multiplier) for turbulent motion.
5. **Rainbow Ribbon trail** — solid multi-colored dust band trailing 2 blocks behind player. Deque of last 20 locations; spawn particles along all stored points, update every 2 ticks.

## Layer 2 — Ambient & environmental (world emitters)

6. **Cherry Blossom Breeze vortex** — slow massive swirl of pink petal particles filling a 20×20×20 area. Helical parametric eq (spiral widening as it rises), radius large, speed 0.01.
7. **Cursed Void spasms** — dark purple portal + black cloud particles violently yanked from doorway edge inward. Inward-attraction: spawn on sphere radius, vector from particle to center, high negative velocity.
8. **Deep-Sea Bubble vents** — thick vertical column of large bubbles erupting from floor, rising then popping 10 blocks up. Spawn on circular plane (diameter 1); random Y velocity 0.2–0.5; `BlockBreak` pop at max height.
9. **Golden Treasure sparkle** — subtle infrequent high-brightness gold sparkles around a block/area. Random-point spawn in 2×2×2 box; static particles; low rate (once per 10–20 ticks).

## Layer 3 — Combat & feedback (action confirmation)

10. **Soul Harvest kill effect** — victim erupts in green soul-flame that gathers and spirals into killer's chest. Burst (`EXPLOSION`) at death location, then vector math updates each particle toward killer's chest per tick.
11. **Critical Shockwave burst** — flat expanding ring of red dust parallel to ground from target's feet on crit. Small circle eq, radius rapidly increases over 5 ticks then despawn.
12. **Level Up helix** — two contrasting spirals (emerald + gold) intertwined, rising feet→head. Double helix eq: two circle sets separated by 180° phase shift, constant Y increase.
13. **Enchantment Glyphs pull** — runes pull inward from air toward held item. Inward-attraction logic with focus = player hand location.
14. **Poison Cloud lingering** — static low-lying greenish-gray cloud at a location for seconds. Gaussian offsets in 2-block radius; near-static with tiny upward drift.

## Additional cosmetic concepts (from earlier list)

15. Phoenix Wings — fiery orange/red flame particles flapping, shedding embers.
16. Cybernetic Wings — cyan/white end-rod particles in geometric segmented frames.
17. Void Wings — dark purple portal + black ink swirling inward like a black hole.
18. Fairy Wings — pastel dust in fast-fluttering figure-eight.
19. Skeletal Wings — white cloud + ash in jagged rib-like structures.
20. Angelic Halo — rotating gold-tinted glow ring above head.
21. Devil Horns — curved crimson dust arcs + lava sparks.
22. Orbiting Planets — multi-colored particle spheres circling head at varied angles/speeds.
23. Personal Storm Cloud — gray smoke overhead, yellow electric sparks, dripping water.
24. Soul-Fire Crown — jagged pulsing blue soul-flame ring on head.

## Math complexity taxonomy (for the Builder Agent)

| Math logic | Complexity | Example |
|------------|------------|---------|
| Static cluster | Low | Poison Cloud, Treasure Sparkle |
| Parametric circle | Low/Mid | Halo, Orbiter |
| Parametric helix | Mid | Level-up Helix, Cherry Breeze |
| Trail (queue) | Mid | Rainbow Ribbon |
| Rotation matrix | High | Tilted Galactic Ring |
| Parametric curves | High | Wings, Lightning Arcs |
| Vector field | High | Soul Harvest, Void Door |
