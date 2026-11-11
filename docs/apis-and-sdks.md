# APIs & SDKs the agents should leverage

## Minecraft runtime & plugin APIs (Builder + QA agents)

- **PaperMC API (`paper-api`)** — primary Java target. `world.spawnParticle()`, async scheduling, modern
  performance hooks. Runs on Paper/Purpur/Folia-compatible setups.
- **PacketEvents API** — construct & send raw particle packets asynchronously; multi-version protocol support
  without fragile NMS internals. Key for lag-free effects.
- **Adventure API (Kyori)** — rich text, MiniMessage gradients, UI components for `/cosmetics` GUIs (bundled in Paper).
- **LuckPerms API** — gating paid cosmetics; Tebex grants access via permission nodes on purchase.
- **Bedrock Molang & Particle JSON schema** — for Marketplace targets (Snowstorm tooling).

## Agent orchestration & GitHub APIs (factory floor)

- **PyGithub / GitHub REST API** — read assigned issues, create feature branches, commit generated files, transition
  labels, post PR comments.
- **Agent framework SDK** (AG2 / LangGraph / OpenAI Agents SDK / CrewAI) — stateful Builder↔QA loop with
  tool-calling, retries on `gradle build` failure, structured JSON logging.
- **Python interpreter tool** (numpy/scipy) — Math Agent verifies bounding boxes / rotation matrices instead of guessing.

## Testing & CI/CD tooling (QA agent)

- **Gradle + shadowJar** — compile + shade dependencies in GitHub Actions.
- **MockBukkit + JUnit 5** — fast in-process unit tests.
- **Plugwright / run-paper** — headless PaperMC server + bot stress tests for TPS/MSPT.

## Storefront & monetization APIs (Storefront & Ops agent)

- **Tebex Headless API / webhooks** — sync packages, pricing tiers, LuckPerms delivery commands; Tebex acts as
  Merchant of Record for global VAT.
- **BuiltByBit Ultimate API** — automate resource updates, version changelogs, license-key management (upgraded tier).
- **MC License** — licensing SDK for protected `.jar` builds (BuiltByBit/Polymart only; Spigot bans external DRM).
