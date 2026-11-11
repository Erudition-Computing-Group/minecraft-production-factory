# Memory & logging — adapted for GitHub

A robust factory repo separates three things: **episodic memory** (ephemeral run states), **semantic memory**
(the factory's knowledge base), and **structured telemetry** (agent traces + build logs). On GitHub we use
GitHub Actions artifacts + the Issues API instead of GitLab CI artifacts.

## Repository layout for memory

```
particle-factory/
├── .github/workflows/     # factory-run.yml, ci.yml
├── agents/                # agent definitions, system prompts, logic
├── config/                # particle_budgets.json, template_manifest.json, compatibility_matrix.json
├── memory/
│   ├── semantic/          # long-term knowledge base (math formulas, templates, style guides)
│   │   ├── math_patterns.json
│   │   └── approved_templates/
│   └── episodic/          # short-term run states (cleared/archived per batch)
│       └── active_runs/
├── src/                   # generated outputs
│   ├── java_plugins/
│   └── bedrock_addons/
├── logs/
│   ├── agent_traces/      # JSONL per run
│   └── build_reports/
└── tests/
    └── qa_benchmarks/
```

## Memory tiers

### Semantic memory (long-term)

- **What:** reusable math formulas (verified Bezier scripts for wings), successful Java class templates, color
  palettes, Mojang compliance rulebook.
- **Storage:** version-controlled JSON/Markdown under `memory/semantic/`. Agents query these static references
  instead of hallucinating syntax.
- **Updates:** when an agent discovers a better rotation matrix, it opens a PR against `memory/semantic/`.

### Episodic memory (short-term run state)

- **What:** intermediate state of a batch (Concept X generated → Math output Y → Builder wrote Z → QA rejected).
- **Storage:** `memory/episodic/active_runs/<run_id>.json`.
- **On GitHub:** persist as GitHub Actions artifacts (`actions/upload-artifact`) so a failed run can be debugged
  from the exact context window + state variables of each agent.

## Structured logging schema

Every agent action emits JSON:

```json
{
  "timestamp": "2026-11-10T17:00:00Z",
  "run_id": "batch-void-wings-042",
  "agent": "math_agent",
  "input_spec": { "theme": "Void Wings", "particle_type": "PORTAL" },
  "tool_invoked": "python_interpreter",
  "output_payload": {
    "status": "success",
    "equations": "x = r * sin(theta) * cos(phi)",
    "max_particles_per_tick": 80
  },
  "token_usage": { "prompt": 420, "completion": 185 }
}
```

- **Directory output:** `logs/agent_traces/<run_id>.jsonl` (JSON Lines).
- **CI integration:** a GitHub Actions job runs the factory, captures `logs/` + `src/` + `memory/episodic/`
  as artifacts, and (optionally) posts a summary comment to the PR via `gh`/`actions/github-script`.

## Git-driven workflow & human-in-the-loop gates

1. **Automated feature branches** — orchestrator creates `feature/particle-batch-<id>` on run start.
2. **The QA gate** — GitHub Actions runs `gradle build` + linters; failure blocks merge (branch protection).
3. **The Visual Review gate** — once CI is green, the issue moves to `status:human-review` and pings the
   human operator for the in-game check before merging to `main`.
4. **Release** — merge to `main` triggers the Storefront Agent publishing script.

## GitHub-specific notes

- Use **GitHub Issues** + labels (`status:spec-ready`, `status:math-verified`, …) as the factory floor board.
- Use **GitHub Actions** for CI minutes (2000 free min/month on public repos; 500 on private free tier).
- Use **branch protection rules** on `main` requiring the `build` + `e2e` checks to pass.
- Use **CODEOWNERS** to route `[VISUAL-REVIEW]` issues to the human operator.
