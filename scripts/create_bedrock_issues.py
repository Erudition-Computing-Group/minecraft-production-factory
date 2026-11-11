"""Create GitHub Issues for Bedrock marketplace roadmap items."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

token = open("/mnt/c/Users/tpugh/.t3/userdata/secrets/files/711dcafa5aadc69a958d0da137adec25").read().strip()

from github import Github

gh = Github(token)
repo = gh.get_repo("Erudition-Computing-Group/minecraft-production-factory")

issues = [
    {
        "title": "[BEDROCK] Bedrock .particle.json + Molang files — Builder Agent needs Bedrock templates",
        "body": """## Goal
Extend the Builder Agent to generate Bedrock Edition particle files (`.particle.json` + Molang curves) instead of only Java/PaperMC code.

## Context
The Minecraft Marketplace is **Bedrock-only**. Our factory currently only produces Java plugins. To sell on the official Marketplace, we need Bedrock add-ons.

## Tasks
- [ ] Create Bedrock `.particle.json` templates (emitter definitions, Molang curves, flipbook textures)
- [ ] Add Molang math translation (convert Python/Java formulas to Molang expressions)
- [ ] Create resource pack + behavior pack scaffolding
- [ ] Add Bedrock particle preview in Blockbench/Snowstorm
- [ ] Update Builder Agent system prompt with Bedrock output mode
- [ ] Update `template_manifest.json` with Bedrock schema version

## Acceptance Criteria
- Builder Agent can output a valid `.particle.json` file from a spec
- File loads in Blockbench without errors
- Molang curves produce correct 3D motion

## References
- docs/architecture.md (agent roster)
- docs/apis-and-sdks.md (Bedrock Molang & Particle JSON schema)
- config/template_manifest.json
""",
        "labels": ["edition:bedrock", "platform:bedrock", "status:spec-ready"],
    },
    {
        "title": "[BEDROCK] Resource packs + behavior packs — packaged as .mcpack",
        "body": """## Goal
Package generated Bedrock particle effects into `.mcpack` files that can be imported into Minecraft Bedrock Edition.

## Context
Bedrock add-ons require both a resource pack (textures, particles) and a behavior pack (entity definitions, spawn rules). These must be zipped and packaged as `.mcpack`.

## Tasks
- [ ] Create resource pack template (manifest.json, textures, .particle.json files)
- [ ] Create behavior pack template (manifest.json, entity definitions, spawn rules)
- [ ] Implement `.mcpack` packaging (zip with correct structure)
- [ ] Add import testing (double-click .mcpack on Windows)
- [ ] Add to Storefront Agent output (delivery instructions for Bedrock)

## Acceptance Criteria
- `.mcpack` file imports into Minecraft Bedrock without errors
- Particle effects render correctly in-game on Bedrock
- Pack structure follows Bedrock add-on conventions

## References
- docs/visual-review.md (Bedrock viewing instructions)
- docs/go-to-market.md (Phase 4: Bedrock expansion)
""",
        "labels": ["edition:bedrock", "platform:bedrock", "status:spec-ready"],
    },
    {
        "title": "[BUSINESS] Apply to Microsoft Partner Program — requires registered business entity + tax ID (EIN)",
        "body": """## Goal
Register a legal business entity and apply to the Minecraft Marketplace Partner Program.

## Context
The official Minecraft Marketplace requires:
- Registered business entity (LLC or equivalent)
- Valid Tax ID (EIN in the US)
- At least 3 polished original content pieces
- Application at minecraft.net/partner

Partners receive 70% of sales revenue.

## Tasks
- [ ] Register business entity (LLC or equivalent)
- [ ] Obtain EIN (Employer Identification Number) from IRS
- [ ] Set up dedicated business bank account
- [ ] Prepare 3 polished original Bedrock content pieces
- [ ] Submit application at minecraft.net/partner
- [ ] Configure tax documentation (W-9 or equivalent)

## Acceptance Criteria
- Business entity registered and active
- EIN obtained and documented
- Partner Program application submitted
- Partner status approved

## References
- docs/go-to-market.md (blind spot #5: Business entity & tax readiness)
- docs/cost-analysis.md (platform fees)
""",
        "labels": ["business", "priority:high", "status:spec-ready"],
    },
    {
        "title": "[PORTFOLIO] Build at least 3 polished original Bedrock content pieces",
        "body": """## Goal
Create 3 high-quality, original Bedrock particle effect add-ons to serve as a portfolio for the Microsoft Partner Program application.

## Context
Microsoft requires at least 3 polished original content pieces before approving Partner applications. These should demonstrate variety and quality.

## Suggested portfolio pieces
1. **Magic Spells & Aura Pack** — 5+ particle effects (wings, halos, trails, bursts)
2. **Elemental Weapons Add-on** — particles attached to custom weapons (fire, ice, lightning, void)
3. **Ambient World Pack** — environmental particles (cherry blossom vortex, bubble vents, cursed void)

## Tasks
- [ ] Design and build 3 distinct Bedrock particle add-ons
- [ ] Test each in Minecraft Bedrock (Windows + console if possible)
- [ ] Record 10-second preview videos/GIFs for each
- [ ] Create store listing copy (descriptions, feature bullets)
- [ ] Package each as .mcpack

## Acceptance Criteria
- 3 complete, polished Bedrock add-ons
- Each has preview media (video/GIF)
- Each is packaged as importable .mcpack
- Store copy written for each

## References
- docs/particle-concepts.md (24 effect concepts)
- docs/visual-review.md (Bedrock viewing instructions)
""",
        "labels": ["edition:bedrock", "portfolio", "status:spec-ready"],
    },
    {
        "title": "[MONETIZATION] Minecoins currency integration",
        "body": """## Goal
Integrate Minecoins as the in-game currency for Bedrock Marketplace purchases.

## Context
The Minecraft Marketplace uses Minecoins as its currency. Players purchase Minecoins with real money, then spend them on content. Creators receive 70% of revenue.

## Tasks
- [ ] Understand Minecoins pricing tiers (how many Minecoins per effect/pack)
- [ ] Set pricing strategy (e.g., 310 Minecoins = ~$1.99, 830 Minecoins = ~$4.99)
- [ ] Configure Minecoins in Partner dashboard
- [ ] Test purchase flow in Bedrock
- [ ] Set up revenue tracking and payout configuration

## Acceptance Criteria
- Pricing tiers defined and documented
- Minecoins purchase flow tested
- Revenue tracking configured
- Payout threshold ($200 minimum) understood

## References
- docs/cost-analysis.md (platform fees and margins)
- docs/go-to-market.md (Phase 4: Bedrock expansion)
""",
        "labels": ["monetization", "edition:bedrock", "status:spec-ready"],
    },
]

# Create a milestone for the Bedrock Marketplace track
try:
    milestone = repo.create_milestone(
        title="Bedrock Marketplace Launch",
        description="Track all work needed to publish particle effects on the official Minecraft Marketplace (Bedrock Edition).",
        state="open",
    )
    print(f"Created milestone: {milestone.title} (#{milestone.number})")
except Exception as e:
    print(f"Milestone creation: {e}")
    milestone = None

for issue_data in issues:
    try:
        kwargs = {
            "title": issue_data["title"],
            "body": issue_data["body"],
            "labels": issue_data["labels"],
        }
        if milestone:
            kwargs["milestone"] = milestone
        issue = repo.create_issue(**kwargs)
        print(f"Created issue #{issue.number}: {issue.title}")
        print(f"  URL: {issue.html_url}")
    except Exception as e:
        print(f"Error creating issue '{issue_data['title']}': {e}")

print(f"\nDone. Created {len(issues)} issues.")
