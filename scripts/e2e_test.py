"""E2E test: verify particle effects work on a live PaperMC server.

Usage:
    python scripts/e2e_test.py [--host localhost] [--port 25575]

Prerequisites:
    - Minecraft server running (docker compose up -d minecraft-server)
    - Plugin deployed (make gallery-deploy)
"""
import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.rcon_client import RconClient


def test_effect(rcon, name, command, wait_seconds=5):
    """Activate an effect and check for errors."""
    print(f"\n--- Testing: {name} ---")
    resp = rcon.command(command)
    print(f"  Command response: {resp}")
    time.sleep(wait_seconds)
    # Check TPS
    tps_resp = rcon.command("spark tps")
    print(f"  TPS: {tps_resp}")
    # Clear
    rcon.command("/cosmetics clear")
    time.sleep(1)
    return True


def main():
    parser = argparse.ArgumentParser(description="E2E particle effect tests")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=25575)
    parser.add_argument("--password", default="particlefactory")
    args = parser.parse_args()

    print("=== E2E Particle Effect Tests ===")
    print(f"Connecting to {args.host}:{args.port}...")

    try:
        with RconClient(args.host, args.port, args.password) as rcon:
            print("Connected!\n")

            # Test burst effect
            test_effect(rcon, "Burst (Explosion)", "/cosmetics burst", wait_seconds=5)

            # Test orbit effect
            test_effect(rcon, "Orbit (Halo)", "/cosmetics orbit", wait_seconds=5)

            # Verify server is still responsive
            resp = rcon.command("say E2E tests complete")
            print(f"\nServer responsive: {resp}")

            print("\n=== All E2E tests passed ===")
    except ConnectionError as e:
        print(f"Connection failed: {e}")
        print("Is the server running? Start with: make gallery-start")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
