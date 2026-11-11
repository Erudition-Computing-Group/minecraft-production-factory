"""Tests for the particle math engine."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from particles.vector import Vec3
from particles.particle import Particle
from particles.spawners import spawn_sphere, spawn_ring, spawn_helix
from particles.emitters import BurstEmitter, OrbitEmitter


def test_vec3_operations():
    a = Vec3(1, 2, 3)
    b = Vec3(4, 5, 6)
    assert (a + b).to_tuple() == (5, 7, 9)
    assert (a - b).to_tuple() == (-3, -3, -3)
    assert (a * 2).to_tuple() == (2, 4, 6)
    assert a.dot(b) == 1*4 + 2*5 + 3*6
    assert abs(a.length() - (14**0.5)) < 1e-9
    n = a.normalize()
    assert abs(n.length() - 1.0) < 1e-9


def test_particle_life_ratio():
    p = Particle(life=20.0)
    assert p.life_ratio == 0.0
    p.life = 10.0
    assert abs(p.life_ratio - 0.5) < 1e-9
    p.life = 0.0
    assert p.life_ratio == 1.0
    assert not p.is_alive


def test_particle_integration():
    p = Particle(pos=Vec3(0, 0, 0), vel=Vec3(1, 0, 0), life=10.0)
    p.integrate(1.0)
    assert p.pos.x == 1.0
    assert p.life == 9.0


def test_spawn_sphere_count():
    parts = spawn_sphere((0, 0, 0), count=10, radius=1.0)
    assert len(parts) == 10
    for p in parts:
        assert p.pos.length() > 0


def test_spawn_ring_count():
    parts = spawn_ring((0, 0, 0), count=8, radius=1.0)
    assert len(parts) == 8


def test_spawn_helix_count():
    parts = spawn_helix((0, 0, 0), count=5)
    assert len(parts) == 10  # 2 strands


def test_burst_emitter():
    em = BurstEmitter(position=(0, 0, 0), count=15)
    em.spawn()
    assert em.get_alive_count() == 15
    em.update()
    assert em.get_alive_count() <= 15


def test_orbit_emitter_maintains_count():
    em = OrbitEmitter(position=(0, 2, 0), count=6)
    assert em.get_alive_count() == 6
    for _ in range(5):
        em.update()
    assert em.get_alive_count() == 6
