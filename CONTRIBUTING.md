# Contributing

1. Fork the repo and create a feature branch: `feature/<slug>`.
2. Keep particle effects cosmetic-only (Mojang Commercial Use Guidelines).
3. Run `pytest tests/qa_benchmarks/` before opening a PR.
4. Respect the particle-per-tick budget in `config/particle_budgets.json`.
5. Open a PR using the provided template; link the originating issue.

## Adding a new particle concept

1. Add the idea to a batch file under `config/`.
2. Run `python -m agents.orchestrator --batch config/<batch>.json`.
3. Review the generated `[SPEC]` → `[MATH]` → `[BUILD]` issues on the GitHub Project board.
