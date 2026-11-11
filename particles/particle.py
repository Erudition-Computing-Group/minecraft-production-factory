"""Particle — the core state object for a single visual sprite."""
import math
from particles.vector import Vec3


class Particle:
    __slots__ = (
        "pos", "vel", "acc", "life", "max_life",
        "size", "color", "alpha", "rotation",
        "custom_data",
    )

    def __init__(self, pos=None, vel=None, life=20.0, size=0.1,
                 color=(1.0, 1.0, 1.0), alpha=1.0):
        self.pos = pos if pos is not None else Vec3.zero()
        self.vel = vel if vel is not None else Vec3.zero()
        self.acc = Vec3.zero()
        self.life = life
        self.max_life = life
        self.size = size
        self.color = tuple(color)
        self.alpha = alpha
        self.rotation = 0.0
        self.custom_data = {}

    # --- derived properties ---
    @property
    def life_ratio(self):
        """0.0 = just born, 1.0 = about to die."""
        if self.max_life <= 0:
            return 1.0
        return 1.0 - (self.life / self.max_life)

    @property
    def is_alive(self):
        return self.life > 0

    @property
    def age_ratio(self):
        """Alias for life_ratio (how far through life)."""
        return self.life_ratio

    # --- physics ---
    def apply_force(self, force):
        """Accumulate a force into acceleration."""
        self.acc = self.acc + force

    def integrate(self, dt=1.0):
        """Semi-implicit Euler integration step."""
        # v(t+1) = v(t) + a(t) * dt
        self.vel = self.vel + self.acc * dt
        # p(t+1) = p(t) + v(t+1) * dt
        self.pos = self.pos + self.vel * dt
        # decay life
        self.life -= dt
        # reset acceleration for next frame
        self.acc = Vec3.zero()

    # --- visual helpers ---
    def set_color_gradient(self, stops):
        """Interpolate color from a list of (ratio, (r,g,b)) stops."""
        r = self.life_ratio
        # find the two stops we're between
        for i in range(len(stops) - 1):
            r0, c0 = stops[i]
            r1, c1 = stops[i + 1]
            if r0 <= r <= r1:
                t = (r - r0) / (r1 - r0) if r1 != r0 else 0.0
                self.color = (
                    c0[0] + (c1[0] - c0[0]) * t,
                    c0[1] + (c1[1] - c0[1]) * t,
                    c0[2] + (c1[2] - c0[2]) * t,
                )
                return
        # clamp to last
        self.color = stops[-1][1]

    def set_alpha_fade_out(self):
        """Alpha decreases linearly from 1 to 0 over lifetime."""
        self.alpha = max(0.0, 1.0 - self.life_ratio)

    def set_alpha_fade_in_out(self):
        """Alpha peaks at middle of life, 0 at start and end."""
        self.alpha = max(0.0, math.sin(self.life_ratio * math.pi))

    def set_size_shrink(self, max_size):
        """Size shrinks to 0 over lifetime."""
        self.size = max_size * (1.0 - self.life_ratio)

    def set_size_grow_shrink(self, max_size):
        """Size grows then shrinks (peaks at middle)."""
        self.size = max_size * math.sin(self.life_ratio * math.pi)

    def __repr__(self):
        return (f"Particle(pos={self.pos}, vel={self.vel}, "
                f"life={self.life:.1f}/{self.max_life:.1f}, "
                f"color={self.color}, alpha={self.alpha:.2f})")
