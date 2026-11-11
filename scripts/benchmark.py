"""Performance benchmark: measure MSPT/TPS under particle load.

Usage:
    python scripts/benchmark.py [--host localhost] [--port 25575] [--duration 30]
"""
import argparse
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.rcon_client import RconClient


def get_mspt(rcon):
    """Get current MSPT from spark."""
    resp = rcon.command("spark mspt")
    # Parse MSPT from response (format varies)
    match = re.search(r"(\d+\.?\d*)\s*ms", resp)
    if match:
        return float(match.group(1))
    return None


def main():
    parser = argparse.ArgumentParser(description="Performance benchmark")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=25575)
    parser.add_argument("--password", default="particlefactory")
    parser.add_argument("--duration", type=int, default=30, help="Test duration in seconds")
    args = parser.parse_args()

    print("=== Performance Benchmark ===")
    print(f"Duration: {args.duration}s")

    try:
        with RconClient(args.host, args.port, args.password) as rcon:
            # Activate all effects
            print("\nActivating all effects...")
            rcon.command("/cosmetics burst")
            rcon.command("/cosmetics orbit")
            time.sleep(2)

            # Measure MSPT over duration
            mspt_values = []
            start = time.time()
            while time.time() - start < args.duration:
                mspt = get_mspt(rcon)
                if mspt is not None:
                    mspt_values.append(mspt)
                    print(f"  MSPT: {mspt:.2f}ms", end="\r")
                time.sleep(1)

            # Results
            if mspt_values:
                avg = sum(mspt_values) / len(mspt_values)
                max_mspt = max(mspt_values)
                min_mspt = min(mspt_values)
                tps = 1000 / avg if avg > 0 else 0

                print(f"\n\n=== Results ===")
                print(f"  Samples:    {len(mspt_values)}")
                print(f"  Avg MSPT:   {avg:.2f}ms")
                print(f"  Max MSPT:   {max_mspt:.2f}ms")
                print(f"  Min MSPT:   {min_mspt:.2f}ms")
                print(f"  Est. TPS:   {tps:.1f}")
                print(f"  Budget:     MSPT < 50ms, TPS >= 20")

                if avg < 50 and tps >= 20:
                    print("  ✅ PASS — within performance budget")
                else:
                    print("  ❌ FAIL — exceeds performance budget")
            else:
                print("Could not parse MSPT from spark output")

            # Cleanup
            rcon.command("/cosmetics clear")
    except ConnectionError as e:
        print(f"Connection failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
