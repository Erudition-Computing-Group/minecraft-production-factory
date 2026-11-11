# Ticket / issue taxonomy (GitHub Issues)

Each agent creates structured GitHub Issues at key handoff points and failure gates. Use the templates in
`.github/ISSUE_TEMPLATE/`.

## 1. Concept & Spec Agent → `[SPEC]` issue

- **Created:** whenever a new batch of particle ideas is approved for production.
- **Assigned to:** Math & Geometry Agent.
- **Labels:** `status:spec-ready`, `edition:java` (or `edition:bedrock`), `category:wings`.
- **Body payload:** theme & visuals, target particle types, budget constraints (max particles/tick, culling radius),
  compliance check (cosmetic-only).

## 2. Math & Geometry Agent → `[MATH]` issue

- **Created:** after Python verification of 3D coordinate formulas.
- **Assigned to:** Builder Agent.
- **Labels:** `status:math-verified`, `blocked-by:<SPEC-ID>`.
- **Body payload:** parametric equations, animation cycle (tick interval, loop), Python sanity-check output
  (bounding box within ±2.5 blocks, particle-per-tick budget).

## 3. Builder Agent → `[BUILD]` issue (or Pull Request)

- **Created:** after writing Java/PaperMC or Bedrock files and committing to a feature branch.
- **Assigned to:** QA & Performance Agent.
- **Labels:** `status:ready-for-qa`, `platform:papermc`.
- **Body payload:** modified files, async architecture confirmation, proposed LuckPerms node.

## 4. QA & Performance Agent → two issue types

### A. `[QA-FAIL]` bug issue (loops back to Builder/Math)

- **Created:** `gradle build` fails, linter flags main-thread blocking, or particle budget exceeded.
- **Assigned to:** Builder Agent (or Math Agent if coordinates out of bounds).
- **Labels:** `status:needs-fix`, `priority:high`.
- **Body payload:** failure reason (compiler error / stack trace / TPS metric), link to log artifact.

### B. `[VISUAL-REVIEW]` human-in-the-loop gate

- **Created:** automated build, unit tests, and TPS benchmarks all pass.
- **Assigned to:** human operator.
- **Labels:** `status:human-review`.
- **Body payload:** download link to compiled `.jar`/`.mcpack`, test command, checklist (shape from all angles,
  camera obstruction, 10s preview GIF).

## 5. Storefront & Ops Agent → `[RELEASE]` issue

- **Created:** after `[VISUAL-REVIEW]` approval and merge to `main`.
- **Assigned to:** human (final publish click) or automated marketplace webhook.
- **Labels:** `status:ready-to-publish`, `channel:builtbybit`, `channel:tebex`.
- **Body payload:** store copy (Markdown/BBCode), platform compliance checklist, Tebex delivery command.

## Automation on GitHub

Wire the Python orchestrator to create/transition issues via `PyGithub` or the REST API (`requests`):

1. Each agent reads its assigned issue's JSON payload from the issue body.
2. On completion, posts output as a comment and creates the next downstream issue, closing its own with a
   label transition (`status:ready-for-qa` → `status:human-review`).
3. The GitHub Project board becomes a live factory floor: Spec → Math → Build → QA → Visual Review → Release.
