"""Spawn patterns — initial position and velocity for particles."""
import math
import random
from particles.vector import Vec3
from particles.particle import Particle


def random_direction():
    """Uniform random direction on unit sphere."""
    theta = random.uniform(0, 2 * math.pi)
    phi = math.acos(random.uniform(-1, 1))
    return Vec3(
        math.sin(phi) * math.cos(theta),
        math.sin(phi) * math.sin(theta),
        math.cos(phi),
    )


def spawn_point(center, vel=None, life=20.0, size=0.1, color=(1, 1, 1)):
    """Single particle at a point."""
    return Particle(pos=Vec3(*center), vel=vel or Vec3.zero(), life=life, size=size, color=color)


def spawn_sphere(center, count, radius=1.0, speed=0.5, life=20.0, size=0.1, color=(1, 1, 1)):
    """Burst: particles radiate outward from a sphere surface."""
    particles = []
    for _ in range(count):
        dir_vec = random_direction()
        p = Vec3(*center) + dir_vec * radius
        v = dir_vec * speed
        particles.append(Particle(pos=p, vel=v, life=life + random.uniform(-2, 2), size=size, color=color))
    return particles


def spawn_cone(center, direction, count, angle=0.5, speed=0.5, life=20.0, size=0.1, color=(1, 1, 1)):
    """Directional spray: particles spread within a cone."""
    particles = []
    axis = Vec3(*direction).normalize()
    for _ in range(count):
        # random angle within cone
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, angle)
        # build vector at angle phi from axis, rotated theta around axis
        # use a reference perpendicular
        if abs(axis.y) < 0.99:
            ref = Vec3(0, 1, 0)
        else:
            ref = Vec3(1, 0, 0)
        perp = axis.cross(ref).normalize()
        perp2 = axis.cross(perp).normalize()
        v = (axis * math.cos(phi) + perp * math.cos(theta) * math.sin(phi)
             + perp2 * math.sin(theta) * math.sin(phi)) * speed
        particles.append(Particle(pos=Vec3(*center), vel=v, life=life, size=size, color=color))
    return particles


def spawn_ring(center, count, radius=1.0, speed=0.3, life=20.0, size=0.1, color=(1, 1, 1)):
    """Aura/halo: particles orbit in a ring."""
    particles = []
    for i in range(count):
        theta = (i / count) * 2 * math.pi
        p = Vec3(
            center[0] + radius * math.cos(theta),
            center[1],
            center[2] + radius * math.sin(theta),
        )
        # tangential velocity
        v = Vec3(-math.sin(theta) * speed, 0, math.cos(theta) * speed)
        particles.append(Particle(pos=p, vel=v, life=life, size=size, color=color))
    return particles


def spawn_helix(center, count, radius=1.0, vertical_speed=0.1, angular_speed=0.2,
                life=30.0, size=0.1, color=(1, 1, 1)):
    """Level-up effect: two intertwined spirals."""
    particles = []
    for i in range(count):
        theta = (i / count) * 2 * math.pi
        # strand 1
        p1 = Vec3(
            center[0] + radius * math.cos(theta),
            center[1] + i * vertical_speed,
            center[2] + radius * math.sin(theta),
        )
        v1 = Vec3(
            -radius * math.sin(theta) * angular_speed,
            vertical_speed,
            radius * math.cos(theta) * angular_speed,
        )
        particles.append(Particle(pos=p1, vel=v1, life=life, size=size, color=color))
        # strand 2 (180° offset)
        p2 = Vec3(
            center[0] + radius * math.cos(theta + math.pi),
            center[1] + i * vertical_speed,
            center[2] + radius * math.sin(theta + math.pi),
        )
        v2 = Vec3(
            -radius * math.sin(theta + math.pi) * angular_speed,
            vertical_speed,
            radius * math.cos(theta + math.pi) * angular_speed,
        )
        particles.append(Particle(pos=p2, vel=v2, life=life, size=size, color=color))
    return particles


def spawn_trail(points, count_per_segment=3, life=10.0, size=0.05, color=(1, 1, 1)):
    """Trail: particles along a path of points."""
    particles = []
    for i in range(len(points) - 1):
        a = Vec3(*points[i])
        b = Vec3(*points[i + 1])
        for _ in range(count_per_segment):
            t = random.uniform(0, 1)
            p = a.lerp(b, t)
            particles.append(Particle(pos=p, vel=Vec3.zero(), life=life, size=size, color=color))
    return particles
