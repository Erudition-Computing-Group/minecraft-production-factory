# itzg/minecraft-server Integration Plan

## Overview

The `itzg/minecraft-server` Docker image is the backbone of our local testing environment.
This plan outlines how to fully leverage its features for development, testing, and CI.

---

## 1. Environment Variables — Full Configuration

### Server Core
| Variable | Value | Purpose |
|----------|-------|---------|
| `EULA` | `TRUE` | Accept Minecraft EULA (required) |
| `TYPE` | `PAPER` | Server type (PaperMC for plugin support) |
| `VERSION` | `1.21.4` | Minecraft version (match plugin target) |
| `MEMORY` | `2G` | JVM heap (increase for heavy particle testing) |
| `MOTD` | `Particle Factory Gallery` | Server browser message |

### Plugin Management
| Variable | Value | Purpose |
|----------|-------|---------|
| `PLUGINS` | URL or path | Auto-download plugins (LuckPerms, spark, etc.) |
| `PLUGINS_FILE` | `/data/plugins.txt` | Plugin list file |
| `REMOVE_OLD_MODS` | `TRUE` | Clean old plugins on restart |

### RCON (Remote Control)
| Variable | Value | Purpose |
|----------|-------|---------|
| `ENABLE_RCON` | `true` | Enable RCON for remote commands |
| `RCON_PASSWORD` | `particlefactory` | RCON auth password |
| `RCON_PORT` | `25575` | RCON port |

### Performance
| Variable | Value | Purpose |
|----------|-------|---------|
| `USE_AIKAR_FLAGS` | `true` | Aikar's optimized JVM flags (better GC) |
| `MAX_TICK_TIME` | `60000` | Prevent watchdog kills during heavy particles |
| `VIEW_DISTANCE` | `10` | Reduce for performance testing |
| `SIMULATION_DISTANCE` | `6` | Reduce for TPS testing |

### World
| Variable | Value | Purpose |
|----------|-------|---------|
| `LEVEL` | `gallery` | World name |
| `LEVEL_TYPE` | `FLAT` | Flat world for clean gallery |
| `SPAWN_PROTECTION` | `0` | Disable spawn protection (test freely) |
| `DIFFICULTY` | `peaceful` | No mob interference |
| `MODE` | `creative` | Creative mode for testing |

---

## 2. Plugin Auto-Installation

### LuckPerms (permission gating)
```yaml
environment:
  PLUGINS: |
    https://github.com/LuckPerms/LuckPerms/releases/download/v5.4.147/LuckPerms-Bukkit-5.4.147.jar
    https://github.com/lucko/spark/releases/download/1.10.72/spark-1.10.72-bukkit.jar
```

### Plugin list file (plugins.txt)
```
# Core
https://github.com/LuckPerms/LuckPerms/releases/download/v5.4.147/LuckPerms-Bukkit-5.4.147.jar
https://github.com/lucko/spark/releases/download/1.10.72/spark-1.10.72-bukkit.jar

# Our plugin (mounted via volume)
# /plugins/particle-factory.jar (auto-mounted from build/libs)
```

---

## 3. RCON Automation — Remote Testing

### Use cases
- Send test commands without being in-game
- Automated test scripts
- CI integration for E2E tests

### Python RCON client
```python
import socket

def rcon_command(host, port, password, command):
    """Send an RCON command and return the response."""
    # RCON protocol implementation
    # 1. Authenticate
    # 2. Send command
    # 3. Receive response
    pass
```

### Test automation via RCON
```bash
# Spawn particles and verify no errors
python scripts/rcon_test.py --command "/cosmetics burst"
python scripts/rcon_test.py --command "/cosmetics orbit"
python scripts/rcon_test.py --command "/spark tps"
```

---

## 4. World Setup — Gallery Concept

### Flat Creative World
A flat world with a grid of test stations:

```
Station 1: Burst effects (explosions, critical hits)
Station 2: Orbit effects (halos, crowns, planets)
Station 3: Stream effects (torches, auras, trails)
Station 4: Vortex effects (void wings, black holes)
Station 5: Helix effects (level-up, DNA)
Station 6: Performance test (max particles, TPS measurement)
```

### Setup via RCON / commands
```bash
# Create flat world with test stations
/gamemode creative
/give @p minecraft:command_block
# Place command blocks at each station that trigger effects
```

### World template
Pre-build a world with:
- Sign posts at each station
- Command blocks to trigger effects
- Armor stands to attach effects to
- Particle count displays (scoreboards)

---

## 5. CI Integration — E2E Testing

### GitHub Actions E2E job
```yaml
e2e_paper_tests:
  runs-on: ubuntu-latest
  services:
    minecraft:
      image: itzg/minecraft-server:latest
      env:
        EULA: "TRUE"
        TYPE: "PAPER"
        VERSION: "1.21.4"
        MEMORY: "1G"
        ENABLE_RCON: "true"
        RCON_PASSWORD: "particlefactory"
      ports:
        - 25565:25565
        - 25575:25575
  steps:
    - uses: actions/checkout@v4
    - name: Wait for server
      run: |
        for i in $(seq 1 60); do
          if nc -z localhost 25565; then echo "Server ready"; break; fi
          sleep 2
        done
    - name: Run E2E tests
      run: python scripts/e2e_test.py
```

### E2E test script
```python
# scripts/e2e_test.py
# 1. Connect via RCON
# 2. Send /cosmetics burst
# 3. Wait 5 seconds
# 4. Check server logs for errors
# 5. Send /spark tps → verify MSPT < 50
# 6. Send /cosmetics clear
# 7. Repeat for orbit
```

---

## 6. Performance Benchmarking

### Metrics to track
| Metric | Target | Tool |
|--------|--------|------|
| MSPT (Milliseconds Per Tick) | < 50ms | `/spark mspt` |
| TPS (Ticks Per Second) | ≥ 20 | `/spark tps` |
| Particle count | ≤ 150/tick | Plugin logs |
| Memory usage | < 1G | Docker stats |
| Startup time | < 60s | CI timer |

### Benchmark script
```python
# scripts/benchmark.py
# 1. Start server
# 2. Activate all effects simultaneously
# 3. Measure MSPT over 30 seconds
# 4. Report: avg MSPT, max MSPT, TPS, memory
# 5. Fail if MSPT > 50ms or TPS < 20
```

---

## 7. Multi-Version Testing

### Test matrix
| Minecraft Version | PaperMC | Priority |
|-------------------|---------|----------|
| 1.21.4 | Latest | Primary |
| 1.21.1 | Stable | Secondary |
| 1.20.4 | LTS | Tertiary |

### Docker Compose override
```yaml
# docker-compose.1.20.4.yml
services:
  minecraft-server:
    environment:
      VERSION: "1.20.4"
```

Run: `docker compose -f docker-compose.yml -f docker-compose.1.20.4.yml up`

---

## 8. Implementation Roadmap

### Phase 1: Basic Gallery (Done ✅)
- [x] Docker Compose with itzg/minecraft-server
- [x] Plugin auto-mount from build/libs
- [x] RCON enabled
- [x] Local gallery script (build, start, stop, deploy, logs)
- [x] Documentation

### Phase 2: Automated Testing
- [ ] RCON Python client (`scripts/rcon_client.py`)
- [ ] E2E test script (`scripts/e2e_test.py`)
- [ ] Performance benchmark (`scripts/benchmark.py`)
- [ ] CI integration (E2E job in GitHub Actions)

### Phase 3: Gallery World
- [ ] Pre-built flat world with test stations
- [ ] Command blocks to trigger effects
- [ ] Armor stands for effect attachment
- [ ] Scoreboard particle counters

### Phase 4: Multi-Version
- [ ] Docker Compose overrides for 1.20.4, 1.21.1
- [ ] Compatibility test matrix in CI
- [ ] Version-specific plugin builds

### Phase 5: Bedrock Testing
- [ ] Bedrock Dedicated Server in Docker (for Bedrock add-ons)
- [ ] Cross-platform test (Java + Bedrock via GeyserMC)