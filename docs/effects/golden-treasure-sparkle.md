# Golden Treasure sparkle — effect run record

Issue: [#22 Golden Treasure sparkle](https://github.com/Erudition-Computing-Group/minecraft-production-factory/issues/22)

## Outcome

This is the factory's first low-risk Bedrock pilot and a matching Java/PaperMC
effect. It emits subtle static gold sparkles inside a 2 x 2 x 2 block area. The
Bedrock asset is testable with `/particle mpf:golden_treasure_sparkle ~ ~1 ~3`;
the Java asset is testable with `/cosmetics treasure`.

| Target | Source | Test artifact |
|---|---|---|
| Bedrock | `src/bedrock_addons/resource_pack/particles/factory/golden_treasure_sparkle.particle.json` | CI artifact `minecraft-production-factory-bedrock` (`.mcpack`) |
| PaperMC 1.21.4 | `GoldenTreasureEmitter.java` | plugin JAR + `/cosmetics treasure` |

## Agent handoff record

### 1. Concept & Spec Agent

Created [`config/effects/golden_treasure_sparkle.bedrock.json`](../../config/effects/golden_treasure_sparkle.bedrock.json).
It specifies an ambient, cosmetic-only effect with gold RGB `255,199,48`, a
16-block culling radius, and a maximum of one emitted particle per tick.

### 2. Math & Geometry Agent

Selected uniform random coordinates:

```text
x = center_x + U(-1, 1)
y = center_y + U(-1, 1)
z = center_z + U(-1, 1)
```

The position is therefore always inside the requested 2 x 2 x 2 block box. The
Java emitter runs every 15 ticks and creates at most one particle; the Bedrock
emitter uses 0.75 particles/second. Both are comfortably below the factory's
150-particles/tick ceiling.

### 3. Builder Agent

Built the Bedrock resource-pack particle and a matching PaperMC emitter. The
Bedrock effect uses the built-in particle atlas so the first pilot has no custom
texture asset or texture-path risk.

### 4. QA & Performance Agent

The Bedrock validator checks JSON structure, identifiers, texture references,
and rate caps, then packages a `.mcpack`. The Java unit test checks the spawn
interval, 2 x 2 x 2 bounds, and zero velocity. Human visual review is still
required before release.

### 5. Storefront & Ops Agent

The CI pipeline publishes the importable `.mcpack` as the
`minecraft-production-factory-bedrock` workflow artifact. Storefront capture
should use a 10-second clip of the effect around a treasure chest or display
pedestal after manual Bedrock approval.

## Lessons learned and improvements

1. **Start with a static area effect.** It avoids entity attachment, player
   movement state, Molang variables, and rotation math, so failures isolate the
   pack/validation/import path.
2. **Ship a testable artifact on every change.** A source JSON file is not a
   verification result; the CI-generated `.mcpack` is the handoff artifact.
3. **Keep the Bedrock and Java paths explicit.** PaperMC Docker tests do not
   test Bedrock. Each asset needs platform-specific packaging and human review.
4. **Use built-in textures for the pilot.** Custom PNGs introduce UV and path
   failures. Add custom textures only after the pack import is proven.
5. **The next improvement is Creator Tools validation.** The current validator
   intentionally uses only Python's standard library. Add official Creator
   Tools validation in CI before generating marketplace candidates.

## Human acceptance checklist

- Build the artifact: `python scripts/bedrock_pack.py --output dist/minecraft-production-factory.mcpack`.
- Import it into Bedrock and activate the Resource Pack in a Creative world.
- Run `/particle mpf:golden_treasure_sparkle ~ ~1 ~3` and check the Content Log.
- Run `/cosmetics treasure` in the PaperMC gallery and confirm the effect lasts
  about 10 seconds with no visual obstruction.
- Record the 10-second store preview and attach it to issue #22 before release.
