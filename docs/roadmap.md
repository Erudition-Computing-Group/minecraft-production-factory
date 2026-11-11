# Roadmap — bringing the Particle Effects Factory to market

Phased rollout: start where barrier to entry is zero (B2B plugin marketplaces), use cash flow + portfolio to
expand into Bedrock and enterprise server contracts.

## Phase 1 — Factory MVP & Pipeline Validation (Weeks 1–4)

**Goal:** prove the multi-agent pipeline can reliably compile lag-free effects.

- Lock the base PaperMC plugin template (`ParticleEffect` interface, async math scheduler, LuckPerms hooks).
- Stand up a containerized PaperMC test server with hot-reload.
- Generate an initial catalog of 10–15 flagship effects (5 wings, 5 halos, 5 footstep trails) under the
  particle-per-tick TPS budget.
- Record 10-second looping preview GIFs/videos of each effect in action.
- **Milestone:** 15 compiled, lag-free effects.

## Phase 2 — B2B Soft Launch on Plugin Marketplaces (Weeks 5–8)

**Goal:** first revenue + real server-owner feedback.

- Launch a "Starter Pack" plugin bundling the first 15 effects, priced $9.99–$14.99.
- Channels: BuiltByBit (9.9% fee), Voxel Shop/Polymart (2% fee), SpigotMC (0% fee, capped $19.99).
- Two build artifacts: DRM-free build for SpigotMC, protected build (MC License) for BuiltByBit/Polymart.
- Deploy Storefront Agent to output BBCode/Markdown product pages, permission-node tables, config examples.
- **Milestone:** first 50+ downloads & reviews.

## Phase 3 — Scale Production & Custom B2B Commissions (Months 3–4)

**Goal:** turn factory speed into an unfair competitive advantage.

- Seasonal/niche packs (Halloween, Winter, Cyberpunk, RPG classes) in days instead of weeks.
- High-margin custom commissions on BuiltByBit + Fiverr: $50–$200+ per commission, 24–48h turnaround.
- Tebex direct store (5% fee, handles global VAT/sales tax) for bundles and memberships.
- **Milestone:** automated seasonal drops + commission pipeline.

## Phase 4 — Bedrock Expansion & Official Marketplace (Months 5+)

**Goal:** tap the massive console/mobile player base.

- Extend Builder Agent with Bedrock `.particle.json` + Molang output templates.
- Build a 3-piece polished original Bedrock portfolio.
- Apply to the Minecraft Partner Program (70% creator split) at minecraft.net/partner — requires registered
  business entity + tax ID — or partner with an established Marketplace studio.
- **Milestone:** Partner Program acceptance.

## Summary timeline

| Phase | Timeframe | Primary channel | Revenue model | Key milestone |
|-------|-----------|-----------------|---------------|---------------|
| 1. Factory MVP | Weeks 1–4 | Local PaperMC / GitHub | $0 (R&D) | 15 compiled, lag-free effects |
| 2. B2B Launch | Weeks 5–8 | BuiltByBit, Voxel Shop, SpigotMC | $10–$15 per plugin sale | First 50+ downloads & reviews |
| 3. Scale & Agency | Months 3–4 | Tebex + custom commissions | Bundles + $50–$200+ gigs | Automated seasonal drops |
| 4. Bedrock / Official | Months 5+ | Minecraft Marketplace | 70% creator split | Partner Program acceptance |
