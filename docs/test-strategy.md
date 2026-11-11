# Test & integration strategy

Bridges two worlds: software verification (Java/JSON compilation + server performance) and spatial/visual
verification (how the 3D geometry looks in-game).

## 4-layer testing pyramid

### Layer 1 — Math & schema unit tests (milliseconds)

- **What:** outputs of Concept + Math agents before any Java/Bedrock files are written.
- **How:**
  - JSON schema validation (valid particle names, RGB 0–255, particle counts under budget).
  - Python bounding-box assertions: run Math Agent formulas across `t=0…T` to assert no coordinate is `NaN`/
    `Infinity` and stays within a `±3` block radius.

### Layer 2 — Mocked API unit tests (seconds)

- **What:** plugin commands, LuckPerms permission checks, config loading, particle scheduling logic.
- **Tooling:** MockBukkit + JUnit 5.
- **How:** MockBukkit simulates the Paper/Bukkit API in-process (no full server). Assert `/cosmetics equip
  cybernetic_wings` fails without permission, succeeds with it, and registers the async task cleanly.

### Layer 3 — Headless E2E & TPS stress tests (10–30s)

- **What:** real server startup, multi-plugin compatibility, packet-spam / TPS degradation.
- **Tooling:** Plugwright (Gradle plugin using headless Mineflayer bots on a real PaperMC server) or `run-paper`.
- **How:** GitHub Actions spins up an ephemeral PaperMC server with the compiled `.jar`; headless bots join, equip
  the effect, sprint/jump 10s. Performance gate: server MSPT stays well below 50ms (20 TPS), zero exceptions in
  `logs/latest.log`.

### Layer 4 — Human-in-the-loop visual gate (manual)

- **What:** aesthetics, camera obstruction, overall "vibe" (LLMs can't judge 3D motion).
- **How:** pull the passing branch, drop the `.jar` onto the local Dockerized PaperMC server, verify in-game, record
  the 10s storefront GIF.

## GitHub Actions pipeline (`.github/workflows/ci.yml`)

```yaml
stages: validate_spec → build → unit_test → e2e_stress_test → package
```

1. **validate_math_and_spec** — `pytest tests/qa_benchmarks/` (schema + math bounds).
2. **build_plugin** — `./gradlew shadowJar`, artifact `build/libs/*.jar`.
3. **mockbukkit_tests** — `./gradlew test`, JUnit report.
4. **e2e_paper_tests** — `./gradlew plugwrightTest`, always-upload `logs/`.

## Self-healing feedback loop

- **On failure:** GitHub Actions webhook/orchestrator extracts the JUnit XML / Gradle stack trace, opens a
  `[QA-FAIL]` issue, feeds it back to the Builder Agent to patch and re-commit.
- **On success:** pipeline moves the issue to `status:human-review` and pings the human operator for the final
  visual check before merging to `main`.
