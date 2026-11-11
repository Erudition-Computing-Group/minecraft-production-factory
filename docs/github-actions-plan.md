# GitHub Actions Plan — Particle Factory

## Overview

This document outlines the complete GitHub Actions strategy for the Minecraft Particle Factory repo.
It covers CI/CD, release automation, factory runs, and operational workflows.

---

## Workflow Inventory

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **CI** | `ci.yml` | Push/PR to main | Validate Python + build Java + lint |
| **Release** | `release.yml` | Tag `v*` | Build JAR + GitHub Release |
| **Factory Run** | `factory-run.yml` | Manual + weekly cron | Run agent orchestrator batch |
| **Nightly** | `nightly.yml` | Cron daily | Full test suite + demo on latest |
| **Dependabot** | `dependabot.yml` | Weekly | Auto-update Python + Gradle deps |
| **CodeQL** | `codeql.yml` | Push/PR + weekly | Security scanning |

---

## 1. CI Pipeline (`.github/workflows/ci.yml`)

### Jobs

```
┌─────────────────┐     ┌─────────────────┐
│ validate_python  │────▶│  build_plugin    │
│  (pytest + demo) │     │  (Gradle JAR)   │
└─────────────────┘     └────────┬────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
            ┌───────────────┐        ┌──────────────┐
            │  java_tests   │        │     lint     │
            │  (JUnit)      │        │  (py_compile)│
            └───────────────┘        └──────────────┘
```

### Triggers
- `push` to `main`
- `pull_request` to `main`

### What it validates
1. **Python math engine** — 12 tests (Vec3, Particle, spawners, emitters, schema, math bounds)
2. **Particle demo** — smoke test that all 6 emitters run 20 ticks without errors
3. **Java plugin build** — Gradle ShadowJar produces runnable JAR
4. **Java unit tests** — JUnit tests (when added)
5. **Lint** — Python syntax check + TODO/FIXME scan

### Artifacts produced
- `particle-factory-plugin` (JAR, 14-day retention)
- `junit-results` (XML, 7-day retention)

---

## 2. Release Pipeline (`.github/workflows/release.yml`)

### Trigger
Push a version tag: `git tag v1.0.0 && git push origin v1.0.0`

### Steps
1. Checkout code
2. Setup Java 21 (Temurin)
3. Build with Gradle ShadowJar
4. Create GitHub Release with:
   - JAR attached
   - Auto-generated release notes
   - Installation instructions

### Versioning strategy
- **Patch** (`v1.0.1`): Bug fixes, minor tweaks
- **Minor** (`v1.1.0`): New emitters, new particle effects
- **Major** (`v2.0.0`): Breaking API changes, new platform support

---

## 3. Factory Run (`.github/workflows/factory-run.yml`)

### Triggers
- **Manual:** Actions → "Factory Run" → Run workflow → enter batch path
- **Scheduled:** Weekly (Sunday midnight UTC)

### What it does
1. Runs `python -m agents.orchestrator --batch <path>`
2. Uploads artifacts: logs/, memory/episodic/, src/
3. 30-day retention

### Future: Agent ticket automation
When a valid PAT is available, add a step to create GitHub Issues for each generated spec:
```yaml
- name: Create spec issues
  env:
    GH_TOKEN: ${{ secrets.GH_PAT }}
  run: python scripts/create_issues.py --run-id ${{ github.run_id }}
```

---

## 4. Nightly Build (`.github/workflows/nightly.yml`)

### Trigger
Cron: daily at 2 AM UTC

### Purpose
- Run full test suite on latest dependencies
- Catch regressions from upstream changes (Paper API, etc.)
- Build and cache the plugin JAR

### Configuration
```yaml
name: Nightly
on:
  schedule:
    - cron: "0 2 * * *"
  workflow_dispatch:

jobs:
  nightly:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: "21" }
      - run: pip install -r requirements.txt
      - run: python scripts/run_tests.py
      - run: python scripts/particle_demo.py
      - working-directory: src/java_plugins
        run: ./gradlew shadowJar --no-daemon
      - uses: actions/upload-artifact@v4
        with:
          name: nightly-build
          path: src/java_plugins/build/libs/*.jar
          retention-days: 7
```

---

## 5. Dependabot (`.github/dependabot.yml`)

### Configuration
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    labels: ["dependencies", "python"]

  - package-ecosystem: "gradle"
    directory: "/src/java_plugins"
    schedule:
      interval: "weekly"
    labels: ["dependencies", "java"]
```

### What it does
- Opens PRs to update Python deps (jsonschema, PyGithub, etc.)
- Opens PRs to update Gradle deps (Paper API, PacketEvents, LuckPerms)
- Runs CI on each PR automatically

---

## 6. CodeQL Security Scanning (`.github/workflows/codeql.yml`)

### Trigger
- Push/PR to main
- Weekly schedule

### Configuration
```yaml
name: CodeQL
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }
  schedule: [{ cron: "0 6 * * 1" }]

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: java, python
      - uses: github/codeql-action/autobuild@v3
      - uses: github/codeql-action/analyze@v3
```

---

## 7. Branch Protection (Manual Setup)

### Recommended rules for `main` branch
1. Go to repo → Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
     - Select: `validate_python`, `build_plugin`, `java_tests`, `lint`
   - ✅ Require branches to be up to date before merging
   - ✅ Require conversation resolution before merging
   - ✅ Do not allow bypassing the above settings

### Label setup
Create these labels in repo → Issues → Labels:
| Label | Color | Used by |
|-------|-------|---------|
| `status:spec-ready` | `#0E8A16` | Concept & Spec Agent |
| `status:math-verified` | `#1D76DB` | Math & Geometry Agent |
| `status:ready-for-qa` | `#FBCA04` | Builder Agent |
| `status:needs-fix` | `#D93F0B` | QA Agent (failure) |
| `status:human-review` | `#6F42C1` | QA Agent (success) |
| `status:ready-to-publish` | `#0E8A16` | Storefront & Ops Agent |
| `priority:high` | `#B60205` | QA failures |
| `edition:java` | `#BFD4F2` | Java effects |
| `edition:bedrock` | `#C5DEF5` | Bedrock effects |
| `platform:papermc` | `#0075CA` | PaperMC builds |

---

## 8. Secrets Required

| Secret | Where | Purpose |
|--------|-------|---------|
| `GITHUB_TOKEN` | Auto-provided | CI builds, releases, issue comments |
| `GH_PAT` | Repo secrets (manual) | Agent ticket automation, cross-repo ops |
| `CODECOV_TOKEN` | Repo secrets (optional) | Code coverage reporting |

### Setting up `GH_PAT`
1. Create a PAT at https://github.com/settings/tokens
2. Scopes: `repo`, `read:org`, `workflow`
3. If org requires SSO: authorize the token for `Erudition-Computing-Group`
4. Add to repo: Settings → Secrets → Actions → New secret → `GH_PAT`

---

## 9. Recommended Workflow for Contributors

```
1. Fork repo / create feature branch
   git checkout -b feature/my-effect

2. Make changes (code, docs, tests)

3. Run locally
   python scripts/run_tests.py
   cd src/java_plugins && ./gradlew shadowJar

4. Push and open PR
   git push origin feature/my-effect
   # → CI runs automatically

5. CI passes → merge to main

6. Tag release (maintainers only)
   git tag v1.1.0 && git push origin v1.1.0
   # → Release workflow builds + publishes JAR
```

---

## 10. Monitoring & Notifications

### GitHub Actions notifications
- Go to repo → Settings → Notifications
- Enable: "Actions" → "Failed workflows" → email or Slack webhook

### Status badges (add to README)
```markdown
![CI](https://github.com/Erudition-Computing-Group/minecraft-production-factory/actions/workflows/ci.yml/badge.svg)
![Release](https://github.com/Erudition-Computing-Group/minecraft-production-factory/actions/workflows/release.yml/badge.svg)
```

---

## Summary: What's Already Done vs. What's Needed

| Item | Status |
|------|--------|
| CI pipeline (Python + Java + lint) | ✅ Done |
| Release pipeline (tag → JAR + Release) | ✅ Done |
| Factory run (manual + cron) | ✅ Done |
| Nightly build | 📋 Planned (config in this doc) |
| Dependabot | 📋 Planned (config in this doc) |
| CodeQL scanning | 📋 Planned (config in this doc) |
| Branch protection rules | 🔧 Manual setup needed |
| Label creation | 🔧 Manual setup needed |
| `GH_PAT` secret | 🔧 Needs valid token |
| Status badges in README | 🔧 Add to README.md |
| MockBukkit tests | 🚧 Not yet written |
| Plugwright E2E | 🚧 Not yet written |
