# Cost analysis

## 1. Compute & AI inference (the factory brains)

| Stack | Monthly cost | Notes |
|-------|--------------|-------|
| Local open-weight (Ollama/LM Studio) | $0 | Runs on existing hardware (32 GB RAM). Zero per-token fees, full privacy. |
| Cloud API (Anthropic/OpenAI/DeepSeek) | $15–$60 | ~$0.003–$0.015 per 1k tokens. A 20-effect batch (~1–3M tokens) costs $5–$20. |

## 2. Development, testing & hosting (infrastructure)

| Item | Cost | Notes |
|------|------|-------|
| GitHub (free tier) | $0 | Private repos, Issues, Actions (2000 min/mo public; 500 min/mo private free). |
| Local PaperMC test server | $0 | Dockerized on dev machine. |
| Paid runners (optional scale-up) | $10–$15/mo | Self-hosted runner on a cheap VPS if CI minutes exceed free tier. |

## 3. Marketplace & platform fees (tolls on revenue)

- **BuiltByBit:** 9.9% platform fee + gateway processing (~2.9% + $0.30).
- **Voxel Shop / Polymart:** 2% platform fee.
- **SpigotMC:** 0% fee (capped at $19.99; no external DRM).
- **Tebex:** 5% fee (Merchant of Record, handles global VAT).
- **Minecraft Marketplace (Bedrock):** 30% Microsoft cut (70% creator).

## Net margin on a $14.99 plugin sale

| Platform | Platform fee | Est. gateway fee | Net profit | Net margin |
|----------|--------------|------------------|------------|------------|
| BuiltByBit | 9.9% ($1.48) | ~$0.73 | ~$12.78 | ~85.3% |
| Tebex | 5.0% ($0.75) | ~$0.73 | ~$13.51 | ~90.1% |

**Takeaway:** Tebex nets ~$0.73 more per sale; BuiltByBit provides built-in marketplace traffic. Most creators
list on BuiltByBit for discovery and run a Tebex store for direct sales/bundles.

## Summary cost matrix

| Approach | Monthly running | Per-batch | Revenue split / platform cut |
|----------|-----------------|-----------|------------------------------|
| Zero-dollar local stack (Ollama + GitHub free) | $0 | $0 | 0%–90%+ (depends on marketplace) |
| Hybrid cloud (APIs + GitHub) | $15–$40 | $5–$20 | 2%–30% platform fees |

Out-of-pocket dev cost is effectively $0 when running orchestration locally on existing hardware.
