# Go-to-market & operational blind spots

## What the plan already covers

Marketplace opportunity (Marketplace 70/30, Tebex 5%, BuiltByBit 9.9%, Polymart 2%, Spigot 0%), 4 revenue
paths, agent roster, LLM routing, GitLab/GitHub memory + logging, 4-layer testing, roadmap phases 1–4,
ticket taxonomy, 24 concepts, APIs/SDKs, cost analysis, and net-margin math.

## Blind spots to close before scaling

1. **Anti-piracy, licensing & obfuscation.** Unprotected `.jar` files get decompiled and leaked within days.
   - Add a packaging step: ProGuard obfuscation + a licensing SDK (MC License / BuiltByBit placeholder injection).
   - Spigot bans external DRM → ship **two artifacts**: DRM-free (Spigot) and protected (BuiltByBit/Polymart).
2. **Multi-version & cross-platform compatibility.** Owners run 1.20.4 → latest; some run GeyserMC (Bedrock on Java).
   - Math/Builder need a compatibility matrix; particle names/packets change between versions (e.g. DUST data).
   - QA should test 2–3 PaperMC versions via Plugwright, or enforce PacketEvents for version-agnostic dispatch.
3. **Customer support, refunds & post-sale triage.** 50 buyers → bug reports, "how do I configure?" tickets, chargebacks.
   - Discord support workflow (FAQ bot / ticket channel), clean `config.yml` with comments, wiki page of permission
     nodes, LuckPerms + PlaceholderAPI hook instructions.
4. **Automated marketing & visual assets.** Manual 10s GIF recording is a bottleneck at 20 effects/batch.
   - Add a media/preview capture step (headless camera mod / ReplayMod script) + distribution plan:
     eye-catching thumbnails, short YouTube/TikTok showcases, a free "Lite" version (2–3 basic particles) on
     SpigotMC to funnel traffic to the paid pack.
5. **Business entity & tax readiness (before Phase 4).** Casual selling is fine; scaling needs formal infra.
   - Register an LLC, dedicated business bank/PayPal, valid Tax ID (EIN) — Microsoft requires a registered
     business entity + tax docs before Partner approval.
6. **Agent guardrails against "slop" & cascading errors.** Small upstream assumptions compound downstream.
   - Add a deduplication/quality gate: similarity check in semantic memory so the factory doesn't flood the
     catalog with redundant circle/spiral variants.

## Pricing & licensing reference (Phase 2)

- Starter Pack: 15 effects, $9.99–$14.99.
- SpigotMC: 0% fee, max $19.99, no external DRM → ship Lite/DRM-free.
- BuiltByBit: 9.9% + gateway → protected build, MC License.
- Polymart/Voxel Shop: 2% → protected build.
- Tebex: 5% + Merchant of Record → direct store, bundles, memberships.

## Visual review checklist (human gate)

- Shape clean from front, side, back (F5 third-person).
- Does not obstruct first-person camera.
- Sprint, jump, spin — math rotates cleanly with yaw; no camera block.
- 10s looping preview GIF recorded for storefront.
- MSPT/TPS within budget on local server.
