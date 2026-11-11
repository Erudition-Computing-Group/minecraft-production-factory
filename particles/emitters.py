"""Emitter agents — combine spawners + forces into reusable effect behaviors."""
import math
import random
from particles.vector import Vec3
from particles.particle import Particle
from particles import spawners, forces


class Emitter:
    """Base emitter: manages a list of particles, updates them each tick."""

    def __init__(self, position=(0, 0, 0)):
        self.position = Vec3(*position)
        self.particles = []
        self.age = 0

    def update(self, dt=1.0):
        """Tick all particles: apply forces, integrate, remove dead ones."""
        self.age += dt
        for p in self.particles:
            self.apply_forces(p)
            p.integrate(dt)
        # remove dead
        self.particles = [p for p in self.particles if p.is_alive]

    def apply_forces(self, particle):
        """Override in subclasses to define force behavior."""
        forces.gravity(particle)
        forces.drag(particle, 0.02)

    def spawn(self, *args, **kwargs):
        """Override in subclasses."""
        pass

    def get_alive_count(self):
        return len(self.particles)

    def get_positions(self):
        return [p.pos.to_tuple() for p in self.particles]


# --- Burst Emitter (Explosion, Critical Hit) ---
class BurstEmitter(Emitter):
    def __init__(self, position=(0, 0, 0), count=30, speed=0.8, life=20.0,
                 color=(1.0, 0.8, 0.2), size=0.15):
        super().__init__(position)
        self.count = count
        self.speed = speed
        self.life = life
        self.color = color
        self.size = size
        self.spawned = False

    def spawn(self):
        if self.spawned:
            return
        self.particles = spawners.spawn_sphere(
            self.position.to_tuple(), self.count, radius=0.3,
            speed=self.speed, life=self.life, size=self.size, color=self.color
        )
        self.spawned = True

    def apply_forces(self, particle):
        forces.gravity(particle, forces.GRAVITY_EARTH)
        forces.drag(particle, 0.03)
        forces.turbulence(particle, strength=0.02, seed=42)


# --- Stream Emitter (Torch, Waterfall, Aura) ---
class StreamEmitter(Emitter):
    def __init__(self, position=(0, 0, 0), rate=3, speed=0.2, life=15.0,
                 color=(1.0, 0.6, 0.1), size=0.1, direction=(0, 1, 0)):
        super().__init__(position)
        self.rate = rate
        self.speed = speed
        self.life = life
        self.color = color
        self.size = size
        self.direction = Vec3(*direction).normalize()

    def update(self, dt=1.0):
        # spawn at rate
        if self.age % (1.0 / self.rate) < dt or self.age < 0.01:
            new_parts = spawners.spawn_cone(
                self.position.to_tuple(), self.direction.to_tuple(),
                count=1, angle=0.3, speed=self.speed, life=self.life,
                size=self.size, color=self.color
            )
            self.particles.extend(new_parts)
        super().update(dt)

    def apply_forces(self, particle):
        forces.buoyancy(particle, 0.03)
        forces.drag(particle, 0.05)
        forces.turbulence(particle, strength=0.03, seed=7)


# --- Orbit Emitter (Halo, Crown, Planet) ---
class OrbitEmitter(Emitter):
    def __init__(self, position=(0, 0, 0), count=12, radius=0.8, height=0.3,
                 angular_speed=0.15, life=40.0, color=(1.0, 0.9, 0.3), size=0.08):
        super().__init__(position)
        self.count = count
        self.radius = radius
        self.height = height
        self.angular_speed = angular_speed
        self.life = life
        self.color = color
        self.size = size
        self.angle_offset = 0.0
        # pre-spawn all particles
        self.particles = spawners.spawn_ring(
            self.position.to_tuple(), count, radius=radius, speed=0,
            life=life, size=size, color=color
        )

    def update(self, dt=1.0):
        self.age += dt
        self.angle_offset += self.angular_speed * dt
        # update positions (orbit around center)
        for i, p in enumerate(self.particles):
            theta = (i / self.count) * 2 * math.pi + self.angle_offset
            p.pos = Vec3(
                self.position.x + self.radius * math.cos(theta),
                self.position.y + self.height,
                self.position.z + self.radius * math.sin(theta),
            )
            p.life -= dt
        self.particles = [p for p in self.particles if p.is_alive]
        # respawn dead particles
        while len(self.particles) < self.count:
            i = len(self.particles)
            theta = (i / self.count) * 2 * math.pi + self.angle_offset
            p = Particle(
                pos=Vec3(
                    self.position.x + self.radius * math.cos(theta),
                    self.position.y + self.height,
                    self.position.z + self.radius * math.sin(theta),
                ),
                vel=Vec3.zero(),
                life=self.life, size=self.size, color=self.color,
            )
            self.particles.append(p)


# --- Trail Emitter (Movement Trail, Sword Swing) ---
class TrailEmitter(Emitter):
    def __init__(self, life=8.0, size=0.06, color=(0.3, 0.7, 1.0)):
        super().__init__((0, 0, 0))
        self.life = life
        self.size = size
        self.color = color
        self.prev_pos = None

    def update_position(self, new_pos):
        """Call this when the tracked entity moves."""
        new_pos = Vec3(*new_pos)
        if self.prev_pos is not None and self.prev_pos.distance_to(new_pos) > 0.1:
            new_parts = spawners.spawn_trail(
                [self.prev_pos.to_tuple(), new_pos.to_tuple()],
                count_per_segment=2, life=self.life, size=self.size, color=self.color
            )
            self.particles.extend(new_parts)
        self.prev_pos = new_pos
        # update existing
        for p in self.particles:
            p.set_alpha_fade_out()
            p.integrate()
        self.particles = [p for p in self.particles if p.is_alive]


# --- Vortex Emitter (Black Hole, Void Wings) ---
class VortexEmitter(Emitter):
    def __init__(self, position=(0, 0, 0), count=20, radius=2.0, life=25.0,
                 color=(0.5, 0.0, 0.8), size=0.1):
        super().__init__(position)
        self.count = count
        self.radius = radius
        self.life = life
        self.color = color
        self.size = size
        # spawn on sphere surface
        self.particles = spawners.spawn_sphere(
            position, count, radius=radius, speed=0.1, life=life, size=size, color=color
        )

    def apply_forces(self, particle):
        forces.attractor(particle, self.position, strength=0.8, min_dist=0.3)
        forces.vortex(particle, self.position, strength=0.4, radius=self.radius)
        forces.drag(particle, 0.05)
        forces.turbulence(particle, strength=0.02, seed=99)


# --- Helix Emitter (Level Up) ---
class HelixEmitter(Emitter):
    def __init__(self, position=(0, 0, 0), count=10, radius=0.6, vertical_speed=0.15,
                 angular_speed=0.2, life=30.0, color1=(0.0, 1.0, 0.3), color2=(1.0, 0.8, 0.0)):
        super().__init__(position)
        self.count = count
        self.radius = radius
        self.vertical_speed = vertical_speed
        self.angular_speed = angular_speed
        self.life = life
        self.color1 = color1
        self.color2 = color2
        self.age = 0.0
        self.particles = spawners.spawn_helix(
            position, count, radius=radius, vertical_speed=vertical_speed,
            angular_speed=angular_speed, life=life, size=0.08, color=color1
        )

    def update(self, dt=1.0):
        self.age += dt
        for p in self.particles:
            p.set_color_gradient([(0.0, self.color1), (1.0, self.color2)])
            p.set_alpha_fade_out()
            p.integrate(dt)
        self.particles = [p for p in self.particles if p.is_alive]
        # respawn
        if len(self.particles) < self.count * 2:
            new = spawners.spawn_helix(
                self.position.to_tuple(), 1, radius=self.radius,
                vertical_speed=self.vertical_speed, angular_speed=self.angular_speed,
                life=self.life, size=0.08, color=self.color1
            )
            self.particles.extend(new)
