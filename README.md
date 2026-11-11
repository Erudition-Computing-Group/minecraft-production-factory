# Minecraft Particle Effects Factory

![CI](https://github.com/Erudition-Computing-Group/minecraft-production-factory/actions/workflows/ci.yml/badge.svg)
![Nightly](https://github.com/Erudition-Computing-Group/minecraft-production-factory/actions/workflows/nightly.yml/badge.svg)
![Release](https://github.com/Erudition-Computing-Group/minecraft-production-factory/actions/workflows/release.yml/badge.svg)

> An automated, multi-agent pipeline that turns raw creative concepts ("Cybernetic Wings", "Soul Harvest")
> into compiled, performance-tested, store-ready Minecraft particle-effect assets — complete with Java/PaperMC
> source, Bedrock `.particle.json` files, LuckPerms nodes, and marketplace listings.

Built from the blueprint in [`docs/`](docs/). Targets **GitHub** for version control, issue tracking, and CI/CD
(GitHub Actions), replacing the original GitLab-centric design.

## What this factory produces

- **Java Edition plugins** (Paper/Spigot) using `world.spawnParticle()` + PacketEvents for lag-free dispatch.
- **Bedrock Edition add-ons** (`.particle.json` + Molang) for the official Minecraft Marketplace.
- **Storefront copy** for BuiltByBit, Polymart/Voxel Shop, SpigotMC, and Tebex.
- **Automated tickets** that move every effect through `Spec → Math → Build → QA → Visual Review → Release`.

## The 5-agent roster

| # | Agent | Core responsibility |
|---|-------|---------------------|
| 1 | **Concept & Spec** | Turns a theme into a structured JSON spec (particle types, RGB, edition, budget). |
| 2 | **Math & Geometry** | Solves 3D parametric equations / rotation matrices; verifies with Python. |
| 3 | **Builder** | Writes production Java/PaperMC classes or Bedrock `.particle.json` files. |
| 4 | **QA & Performance** | Compiles, lints, stress-tests TPS/MSPT, files `[QA-FAIL]` or `[VISUAL-REVIEW]`. |
| 5 | **Storefront & Ops** | Packages releases, writes listings, emits Tebex/BuiltByBit delivery commands. |

See [`docs/architecture.md`](docs/architecture.md).

## Quick start

### Option A: Docker (recommended — matches CI exactly)

```bash
# 1. Clone
git clone git@github.com:Erudition-Computing-Group/minecraft-production-factory.git
cd minecraft-production-factory

# 2. Run all tests
docker compose run --rm python-tests
docker compose run --rm java-tests

# 3. Build plugin JAR
docker compose run --rm java-build

# 4. Run particle demo
docker compose run --rm python-demo

# Or use make:
make test      # all tests
make build     # build JAR
make ci        # full CI check
make clean     # clean up
```

### Option B: Local (no Docker)

```bash
# 1. Clone
git clone git@github.com:Erudition-Computing-Group/minecraft-production-factory.git
cd minecraft-particle-factory

# 2. Python tooling (agents + tests)
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Run tests
python -m pytest tests/qa_benchmarks/ -v
python scripts/particle_demo.py

# 4. Java build (requires Gradle 8+ and Java 21)
cd src/java_plugins && gradle shadowJar --no-daemon

# 5. Run a batch
python -m agents.orchestrator --batch config/batch_01.json

# 6. Local visual check
# drop build/libs/*.jar into a PaperMC server's plugins/ folder, connect via localhost
```

## Repository layout

```
minecraft-particle-factory/
├── agents/          # Agent implementations + system prompts + JSON schemas
├── particles/       # Particle math engine (Vec3, Particle, forces, spawners, emitters)
├── config/          # Particle budgets, template manifests, compatibility matrix
├── memory/          # Semantic (long-term) + episodic (run state) memory
├── src/             # Generated outputs: java_plugins/, bedrock_addons/
├── scripts/         # Demo, smoke tests, test runner
├── tests/           # Schema + math-bounds + particle engine tests
├── logs/            # Structured JSONL agent traces + build reports
├── docs/            # Architecture, roadmap, LLM stack, testing, costs, ...
└── .github/         # Workflows, issue templates, PR template
```

## Documentation index

- [Architecture & agent roster](docs/architecture.md)
- [Roadmap (phases 1–4)](docs/roadmap.md)
- [LLM stack (local + cloud)](docs/llm-stack.md)
- [Memory & logging on GitHub](docs/memory-and-logging.md)
- [Ticket / issue taxonomy](docs/ticket-taxonomy.md)
- [Test & integration strategy](docs/test-strategy.md)
- [APIs & SDKs](docs/apis-and-sdks.md)
- [Cost analysis](docs/cost-analysis.md)
- [24 particle concepts](docs/particle-concepts.md)
- [Visual review gate](docs/visual-review.md)
- [Local Minecraft gallery](docs/local-gallery.md)
- [itzg integration plan](docs/itzg-integration-plan.md)
- [Go-to-market & blind spots](docs/go-to-market.md)

## License

MIT — see [LICENSE](LICENSE). Marketplace assets you ship are governed by Mojang's Commercial Use Guidelines.
