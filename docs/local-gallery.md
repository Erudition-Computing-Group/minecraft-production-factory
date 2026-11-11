# Local Minecraft Gallery — Testing Particle Effects

## Concept

A **local Minecraft gallery** is a PaperMC server running in Docker that lets you visually inspect
and test particle effects in real-time. Instead of guessing how math looks in 3D, you connect with
your Minecraft client and see effects render live.

## Architecture

```
┌─────────────────────────────────────────────────┐
│  Your Machine                                   │
│                                                 │
│  ┌─────────────┐     ┌──────────────────────┐  │
│  │  Minecraft   │────▶│  PaperMC Server      │  │
│  │  Java Client │     │  (Docker container)  │  │
│  │  localhost   │     │  Port: 25565         │  │
│  └─────────────┘     │                      │  │
│                      │  plugins/            │  │
│  ┌─────────────┐     │  └── particle-factory│  │
│  │  Blockbench  │     │      .jar            │  │
│  │  (Bedrock    │     │                      │  │
│  │  preview)    │     │  RCON: 25575         │  │
│  └─────────────┘     └──────────────────────┘  │
│                                                 │
│  ┌─────────────┐     ┌──────────────────────┐  │
│  │  Python      │────▶│  Particle Math       │  │
│  │  Math Agent  │     │  Engine (particles/)  │  │
│  └─────────────┘     └──────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Quick Start

### 1. Build the plugin
```bash
make gallery-build
# or: python scripts/local_gallery.py --build
```

### 2. Start the server
```bash
make gallery-start
# or: python scripts/local_gallery.py --start
```

### 3. Connect
- Open Minecraft Java Edition
- Multiplayer → Direct Connection → `localhost:25565`
- No authentication needed (offline mode)

### 4. Test effects
In-game commands:
```
/cosmetics burst    — 20-particle explosion effect
/cosmetics orbit    — 12-particle orbiting halo
/cosmetics clear    — remove all effects
```

### 5. Hot-reload (fast iteration)
```bash
# After editing Java code:
make gallery-deploy
# Reconnect to localhost:25565
```

### 6. Stop when done
```bash
make gallery-stop
```

## Server Details

| Setting | Value |
|---------|-------|
| Image | `itzg/minecraft-server` (PaperMC) |
| Version | 1.21.4 |
| Port | 25565 (game), 25575 (RCON) |
| RCON password | `particlefactory` |
| Memory | 2G |
| Plugins dir | `./src/java_plugins/build/libs/` (mounted read-only) |
| Data dir | `./minecraft-data/` (persistent world data) |

## RCON Commands (remote control)
```bash
# Send a command to the server without being in-game
python scripts/local_gallery.py --rcon "say Hello from RCON"
python scripts/local_gallery.py --rcon "tp @a 0 100 0"
python scripts/local_gallery.py --rcon "time set day"
```

## Docker Image Comparison

| Image | Pros | Cons |
|-------|------|------|
| `itzg/minecraft-server` | Most popular, supports PaperMC/Spigot/Fabric, auto-downloads, RCON built-in, plugin auto-install | Larger image |
| `marctv/minecraft-papermc-server` | Lightweight, PaperMC-focused | Less flexible, fewer features |
| Manual (eclipse-temurin + wget) | Full control | More setup, slower |

**Recommendation:** `itzg/minecraft-server` — best balance of features and ease of use.

## Gallery Workflow

```
1. Edit particle math (particles/*.py) or Java code (src/java_plugins/)
       ↓
2. Run Python tests: make test-python
       ↓
3. Build plugin: make gallery-build
       ↓
4. Deploy + restart: make gallery-deploy
       ↓
5. Connect to localhost:25565
       ↓
6. Test effects in-game (/cosmetics burst, /cosmetics orbit)
       ↓
7. Check TPS: /spark tps (or /spark mspt)
       ↓
8. Record 10s preview GIF for storefront
       ↓
9. Approve → merge PR → tag release
```

## Troubleshooting

### Server won't start
- Check Docker is running: `docker ps`
- Check logs: `make gallery-logs`
- Ensure port 25565 isn't in use: `netstat -an | findstr 25565`

### Plugin not loading
- Verify JAR exists: `ls src/java_plugins/build/libs/*.jar`
- Check server logs for errors: `make gallery-logs`
- Ensure plugin.yml is valid (name, version, main class)

### Can't connect
- Server may still be starting (wait 30-60 seconds)
- Check firewall allows localhost:25565
- Use "Direct Connection" not "Add Server" (avoids DNS issues)

### Performance issues
- Reduce particle count in config/particle_budgets.json
- Lower server memory: change MEMORY in docker-compose.yml
- Check MSPT: `/spark mspt` in-game (should be < 50ms)