# Bedrock particle testing

## What is automated

Run the same validation used by GitHub Actions:

```bash
python scripts/bedrock_pack.py --output dist/minecraft-production-factory.mcpack
```

It checks that the resource-pack manifest is valid, each particle definition is
valid JSON, identifiers are unique and use a non-`minecraft` namespace, referenced
PNG textures exist (unless the built-in particle atlas is used), and simple
emitter-budget limits are respected. The output is a
standard `.mcpack` whose root contains `manifest.json`.

## Test in Minecraft Bedrock for Windows

1. Install Minecraft Bedrock for Windows and enable **Content Log File** in
   Settings → Creator.
2. For iterative testing, copy `src/bedrock_addons/resource_pack` to:

   ```text
   %appdata%\Minecraft Bedrock\users\shared\games\com.mojang\development_resource_packs\minecraft-production-factory
   ```

   On older UWP installations, use the legacy `LocalState\games\com.mojang`
   directory instead.
3. Start Minecraft, create a Creative world, and activate **Minecraft Production
   Factory – Development Resource Pack** in Resource Packs.
4. Run the Golden Treasure pilot effect:

   ```mcfunction
   /particle mpf:golden_treasure_sparkle ~ ~1 ~3
   ```
5. Review `%appdata%\Minecraft Bedrock\logs\` for content errors.

## Acceptance checklist

- Particle appears without a content-log error.
- The effect is clean from first-person and all third-person views.
- Spawn it repeatedly and alongside other effects; there is no visible hitching.
- Verify it at the supported minimum Bedrock version and record a 10-second
  capture for the storefront review.

## Release handoff

CI publishes the `.mcpack` as a build artifact. Download it, double-click it to
import into Minecraft, then activate the imported Resource Pack in a clean Creative
world for final acceptance. Do not merge an effect until this manual check passes.
