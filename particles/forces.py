"""Force functions — modify a particle's acceleration."""
import math
import random
from particles.vector import Vec3


# --- Gravity ---
GRAVITY_EARTH = Vec3(0, -0.08, 0)   # Minecraft-like gravity (blocks/tick²)
GRAVITY_MOON  = Vec3(0, -0.02, 0)
GRAVITY_NONE  = Vec3(0, 0, 0)


def gravity(particle, g=GRAVITY_EARTH):
    """Constant downward acceleration."""
    particle.apply_force(g)


# --- Wind ---
def wind(particle, direction, strength=0.02):
    """Directional push (e.g., horizontal gust)."""
    force = direction.normalize() * strength
    particle.apply_force(force)


# --- Drag (Air Resistance) ---
def drag(particle, coefficient=0.05):
    """Slows particle proportional to velocity. Essential for smoke/dust."""
    force = particle.vel * (-coefficient)
    particle.apply_force(force)


# --- Turbulence (Perlin-like noise) ---
def _simple_noise(x, y, z, seed=0):
    """Simplified pseudo-Perlin noise using sin/cos (good enough for game effects)."""
    n = math.sin(x * 12.9898 + y * 78.233 + z * 37.719 + seed) * 43758.5453
    return n - math.floor(n)


def turbulence(particle, strength=0.05, seed=0, scale=0.5):
    """Organic swirling drift using 3D noise sampled at particle position."""
    p = particle.pos
    nx = _simple_noise(p.x * scale, p.y * scale, p.z * scale, seed)
    ny = _simple_noise(p.x * scale + 100, p.y * scale + 100, p.z * scale + 100, seed + 1)
    nz = _simple_noise(p.x * scale + 200, p.y * scale + 200, p.z * scale + 200, seed + 2)
    # map [0,1] → [-1,1]
    force = Vec3(nx * 2 - 1, ny * 2 - 1, nz * 2 - 1) * strength
    particle.apply_force(force)


# --- Attractor (Point Pull) ---
def attractor(particle, target, strength=0.5, min_dist=0.5):
    """Pulls particle toward a target point (vortex, black hole, magnet)."""
    diff = target - particle.pos
    dist = diff.length()
    if dist < 0.001:
        return
    dir_vec = diff.normalize()
    force_mag = strength / max(dist, min_dist)
    particle.apply_force(dir_vec * force_mag)


# --- Repulsor (Point Push) ---
def repulsor(particle, source, strength=0.5, min_dist=0.5):
    """Pushes particle away from a point (explosion shockwave)."""
    diff = particle.pos - source
    dist = diff.length()
    if dist < 0.001:
        return
    dir_vec = diff.normalize()
    force_mag = strength / max(dist, min_dist)
    particle.apply_force(dir_vec * force_mag)


# --- Vortex (Rotational Force) ---
def vortex(particle, center, axis=Vec3(0, 1, 0), strength=0.3, radius=2.0):
    """Applies a tangential force, making particles orbit around an axis."""
    diff = particle.pos - center
    # project onto plane perpendicular to axis
    proj = diff - axis.normalize() * diff.dot(axis.normalize())
    dist = proj.length()
    if dist < 0.001:
        return
    # tangential direction = axis × radial
    tangent = axis.normalize().cross(proj.normalize())
    # strength falls off with distance from vortex center
    falloff = max(0, 1.0 - dist / radius)
    particle.apply_force(tangent * strength * falloff)


# --- Buoyancy (Rising) ---
def buoyancy(particle, strength=0.05):
    """Upward force (smoke rising, bubbles)."""
    particle.apply_force(Vec3(0, strength, 0))


# --- Combine multiple forces ---
def apply_forces(particle, *force_funcs):
    """Apply a list of force functions to a particle."""
    for f in force_funcs:
        f(particle)
    particle.integrate()
