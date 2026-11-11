# Visual review gate (human-in-the-loop)

LLMs cannot reliably judge 3D visual appeal in motion, so the pipeline **pauses** here for a human check.

## Viewing generated effects locally

### Java Edition plugins (`.jar`)

- **Option A — local PaperMC server:** download PaperMC, run `java -Xmx2G -jar paper.jar --nogui`,
  accept EULA, drop the factory `.jar` (+ LuckPerms) into `plugins/`, connect via `localhost` in the client.
  Use `run-paper` or BlockDev for one-click build/deploy/hot-reload.
- **Option B — live tweaking:** install PlayerParticles on the local server and use `/pp gui` to test particle
  types/patterns without recompiling Java.

### Bedrock Edition add-ons (`.particle.json`)

- **Blockbench:** open the 3D model → Animate Mode → Animate Effects → load `.particle.json` into a particle
  keyframe; auto-reloads on file edit.
- **Snowstorm Particle Editor:** instant 3D preview of emitter physics, flipbook textures, Molang curves.
- **In-game:** double-click the `.mcpack` on Windows to import into Bedrock, load into a creative world.

## Visual review checklist

- [ ] Shape looks clean from front, side, and back (cycle F5 third-person).
- [ ] Does not obstruct the player's first-person camera.
- [ ] Sprint, jump, spin rapidly — math rotates cleanly with yaw.
- [ ] 10-second looping preview GIF recorded for the storefront.
- [ ] MSPT/TPS within budget on the local server.

## Gate transition

Once approved, merge the feature branch to `main` → triggers the Storefront Agent publishing script and the
`[RELEASE]` issue. On rejection, file a `[QA-FAIL]`-style tweak ticket back to the Builder Agent.
