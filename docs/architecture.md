# Architecture — Particle Effects Factory

## Overview

A Particle Effects Factory is an automated, multi-agent pipeline that takes a raw creative concept
(e.g. "Cybernetic Wings") and turns it into compiled, performance-tested, store-ready Minecraft assets —
complete with code, configuration files, and storefront copy.

## The 5 agents

### 1. Concept & Spec Agent

- **Role:** Translates a theme into a concrete technical specification that fits Mojang's cosmetic-only rules.
- **Input:** Raw idea (e.g. "Void Wings").
- **Output:** JSON spec — particle types, RGB/dust colors, target edition (Java/Bedrock), animation style,
  particle budget, view-distance culling radius, compliance check.
- **Model tier:** Fast/cheap (Gemma 4 12B / Claude Sonnet mini). Handles structured JSON well.

### 2. Math & Geometry Agent

- **Role:** Solves the 3D spatial math — parametric equations, rotation matrices, Bezier curves — needed to
  render a shape relative to a player's yaw/pitch.
- **Input:** Technical spec.
- **Output:** Verified `(x,y,z)` offset formulas, tick intervals, Molang curves; Python sanity-check proving the
  bounding box stays within `±2.5` blocks and the particle-per-tick budget holds.
- **Model tier:** Reasoning model (Qwen 3 27B / GPT-6 Sol). **Must** be given a Python interpreter tool.

### 3. Builder Agent

- **Role:** Writes production code.
- **Input:** Math formulas + spec.
- **Output:** `.java` source files (PaperMC), `plugin.yml`, or Bedrock resource/behavior pack files (`.particle.json`).
- **Model tier:** Coding model (Devstral Small 2 / Qwen 3 Coder 30B / Claude Sonnet).

### 4. QA & Performance Agent

- **Role:** Audits for TPS impact, packet spam, memory leaks. Compiles code and runs unit/lint checks.
- **Input:** Source code.
- **Output:** Compiled `.jar` / `.mcpack`, performance report, or `[QA-FAIL]` tickets back to Builder/Math.
- **Model tier:** Reasoning/coding (GPT-OSS 20B / Claude Opus). Needs shell access to `gradle`/`mvn`.

### 5. Storefront & Ops Agent

- **Role:** Packages the final asset for sale.
- **Input:** Compiled asset + spec.
- **Output:** Store copy, Tebex delivery commands, pricing tier, changelog, permission-node tables.
- **Model tier:** Fast/cheap (Gemma 4 12B).

## Assembly line workflow

1. **Trigger & Spec** — batch list of ideas → Concept Agent → structured specs (standardized particle counts).
2. **Spatial Calculation** — Math Agent writes trig (Bezier curves, sine-wave flapping).
3. **Code Generation** — Builder wraps math into modular template with `world.spawnParticle()` + view-distance culling.
4. **Automated Build & Audit** — QA runs Gradle/Maven build; rejects effects exceeding the particle-per-tick budget
   (e.g. max 150 particles/tick) or with main-thread blocking.
5. **Human-in-the-Loop (Visual Check)** — LLMs cannot "see" 3D motion; pipeline pauses for in-game approval.
6. **Packaging & Listing** — Storefront Agent emits Tebex command (`/lp user {name} permission set ...`),
   feature list, markdown store page.

## Recommended tech stack

- **Orchestration:** state-machine / multi-agent framework (LangGraph, AG2, CrewAI, OpenAI Agents SDK).
- **Tooling for agents:** shell access to `gradle build` / `mvn package`, linter, Python interpreter.
- **Local test environment:** lightweight PaperMC server in Docker with a hot-reload plugin.
- **Version control:** Git on GitHub; each approved effect is its own feature branch or modular class, enabling
  mega-pack bundling later.
- **Spatial math verification:** Math Agent writes Python (numpy/scipy) to sanity-check bounding boxes and
  particle density before handing formulas to Builder.

## Mojang compliance (hard rules)

- Effects must be **cosmetic only**: no hitboxes, no buffs, no pay-to-win.
- No restricted items (capes, etc.).
- Follow Mojang's Commercial Use Guidelines for monetized servers.
- Bedrock Marketplace: 70% creator / 30% Microsoft split; requires registered business entity + tax ID.
