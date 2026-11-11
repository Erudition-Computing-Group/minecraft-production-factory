"""Demo: run all emitter types for 20 ticks and print stats."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from particles.emitters import (
    BurstEmitter, StreamEmitter, OrbitEmitter, TrailEmitter,
    VortexEmitter, HelixEmitter,
)

emitters = {
    "Burst (Explosion)": BurstEmitter(position=(0, 5, 0), count=20),
    "Stream (Torch)": StreamEmitter(position=(0, 0, 0), rate=5),
    "Orbit (Halo)": OrbitEmitter(position=(0, 2, 0), count=8),
    "Vortex (Void)": VortexEmitter(position=(0, 0, 0), count=15),
    "Helix (Level Up)": HelixEmitter(position=(0, 0, 0), count=6),
}

# Spawn burst immediately
emitters["Burst (Explosion)"].spawn()

print("=== Particle System Demo — 20 ticks ===\n")
for tick in range(1, 21):
    print(f"--- Tick {tick} ---")
    for name, em in emitters.items():
        if name == "Trail (Movement)":
            em.update_position((tick * 0.5, 2, 0))
        else:
            em.update()
        alive = em.get_alive_count()
        print(f"  {name}: {alive} particles alive")

# Trail demo
print("\n=== Trail Emitter Demo ===")
trail = TrailEmitter(life=6.0, size=0.05, color=(0.2, 0.8, 1.0))
for i in range(10):
    trail.update_position((i * 0.5, 2, 0))
    print(f"  tick {i}: {trail.get_alive_count()} trail particles")

print("\nDemo complete.")
