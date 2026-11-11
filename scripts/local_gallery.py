"""Local Minecraft Gallery — deploy plugin and test particle effects.

Usage:
    python scripts/local_gallery.py --build    # Build JAR + deploy to server
    python scripts/local_gallery.py --start    # Start Minecraft server
    python scripts/local_gallery.py --stop     # Stop Minecraft server
    python scripts/local_gallery.py --logs     # Tail server logs
    python scripts/local_gallery.py --rcon     # Send RCON command
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCKER = "docker"  # or full path to docker.exe on Windows

# Adjust for Windows Docker Desktop
import platform
if platform.system() == "Windows":
    DOCKER = r"C:\Program Files\Docker\Docker\resources\bin\docker.exe"


def run(cmd, **kwargs):
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, **kwargs)


def build_plugin():
    """Build the Java plugin JAR using Docker."""
    print("=== Building plugin JAR ===")
    run([DOCKER, "compose", "run", "--rm", "java-build"])
    jar = ROOT / "src" / "java_plugins" / "build" / "libs"
    jars = list(jar.glob("*.jar"))
    if jars:
        print(f"Built: {jars[0].name}")
    else:
        print("ERROR: No JAR found after build")
        sys.exit(1)


def start_server():
    """Start the Minecraft PaperMC server."""
    print("=== Starting Minecraft server ===")
    run([DOCKER, "compose", "up", "-d", "minecraft-server"])
    print("\nWaiting for server to start...")
    time.sleep(10)
    print("\nServer starting. Connect with:")
    print("  Minecraft Java Edition → Multiplayer → Direct Connection → localhost:25565")
    print("\nRCON (for commands): localhost:25575, password: particlefactory")
    print("\nTest commands in-game:")
    print("  /cosmetics burst   — explosion effect")
    print("  /cosmetics orbit   — halo effect")
    print("  /cosmetics clear   — remove all effects")


def stop_server():
    """Stop the Minecraft server."""
    print("=== Stopping Minecraft server ===")
    run([DOCKER, "compose", "stop", "minecraft-server"])
    run([DOCKER, "compose", "rm", "-f", "minecraft-server"])


def tail_logs():
    """Tail server logs."""
    print("=== Server logs (Ctrl+C to stop) ===")
    run([DOCKER, "compose", "logs", "-f", "minecraft-server"])


def send_rcon(command):
    """Send an RCON command to the server."""
    print(f"=== RCON: {command} ===")
    # Use mcrcon if available, otherwise docker exec
    run([DOCKER, "exec", "particle-factory-mc", "rcon-cli", command])


def deploy_and_restart():
    """Build, deploy, and restart server."""
    build_plugin()
    print("\n=== Restarting server with new plugin ===")
    run([DOCKER, "compose", "restart", "minecraft-server"])
    print("\nPlugin deployed. Reconnect to localhost:25565")


def main():
    parser = argparse.ArgumentParser(description="Local Minecraft Gallery")
    parser.add_argument("--build", action="store_true", help="Build plugin JAR")
    parser.add_argument("--start", action="store_true", help="Start Minecraft server")
    parser.add_argument("--stop", action="store_true", help="Stop Minecraft server")
    parser.add_argument("--logs", action="store_true", help="Tail server logs")
    parser.add_argument("--rcon", type=str, help="Send RCON command")
    parser.add_argument("--deploy", action="store_true", help="Build + deploy + restart")
    args = parser.parse_args()

    if args.build:
        build_plugin()
    elif args.start:
        start_server()
    elif args.stop:
        stop_server()
    elif args.logs:
        tail_logs()
    elif args.rcon:
        send_rcon(args.rcon)
    elif args.deploy:
        deploy_and_restart()
    else:
        parser.print_help()
        print("\nQuick start:")
        print("  python scripts/local_gallery.py --build    # Build JAR")
        print("  python scripts/local_gallery.py --start    # Start server")
        print("  python scripts/local_gallery.py --deploy   # Build + deploy + restart")


if __name__ == "__main__":
    main()
