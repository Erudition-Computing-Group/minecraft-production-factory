# Particle System Math Reference

This document defines the mathematical foundation for all particle effects in the factory.
Every agent (especially the Math & Geometry Agent) should reference this when deriving formulas.

---

## 1. Core State — The Particle

Every particle is a point in 3D space with the following state:

| Property | Symbol | Type | Description |
|----------|--------|------|-------------|
| Position | **p** | Vec3 | Current (x, y, z) in world space |
| Velocity | **v** | Vec3 | Rate of position change (units/tick) |
| Acceleration | **a** | Vec3 | Rate of velocity change (units/tick²) |
| Life | *t* | float | Remaining lifetime in ticks |
| Max Life | *t_max* | float | Total lifetime (for ratio calculations) |
| Size | *s* | float | Render size (blocks) |
| Color | **c** | RGB | Current color (0.0–1.0 per channel) |
| Alpha | *α* | float | Opacity (0.0 = invisible, 1.0 = solid) |

### Life Ratio
The most important derived value is the **life ratio**:

```
r = t / t_max     (0.0 = just born, 1.0 = about to die)
```

All visual properties (color, size, alpha) are driven by `r`.

---

## 2. Vector3 — The Math Primitive

All spatial math uses a 3-component vector. Operations:

```
Add:        a + b = (ax+bx, ay+by, az+bz)
Subtract:   a - b = (ax-bx, ay-by, az-bz)
Scale:      a * k = (ax*k, ay*k, az*k)
Dot:        a · b = ax*bx + ay*by + az*bz
Cross:      a × b = (ay*bz - az*by, az*bx - ax*bz, ax*by - ay*bx)
Length:     |a| = sqrt(ax² + ay² + az²)
Normalize:  â = a / |a|
Lerp:       lerp(a, b, t) = a + (b - a) * t
```

---

## 3. Physics Integration

### Semi-Implicit Euler (Recommended)
The simplest stable integrator. Update velocity first, then position:

```
v(t+1) = v(t) + a(t) * dt
p(t+1) = p(t) + v(t+1) * dt
t(t+1) = t(t) - dt
```

Where `dt = 1` tick (Minecraft runs at 20 TPS, so 1 tick = 50ms).

### Why Semi-Implicit over Explicit Euler?
Explicit Euler updates position first, then velocity. This causes energy to *increase* over time (particles spiral outward). Semi-implicit Euler is more stable and particles settle naturally.

---

## 4. Force Functions

Forces modify acceleration **a**. Multiple forces can be summed per tick.

### Gravity
```
a_gravity = (0, -g, 0)     where g = 0.08 (Minecraft-like)
```

### Wind (Directional)
```
a_wind = wind_vector * strength
```

### Turbulence (Perlin Noise)
Uses 3D Perlin noise to create organic, swirling drift. The noise field is sampled at the particle's position:

```
a_turbulence = (noise(p.x, p.y, p.z, seed),
                noise(p.x+100, p.y+100, p.z+100, seed),
                noise(p.x+200, p.y+200, p.z+200, seed)) * strength
```

This makes particles appear to "swirl" like smoke or dust.

### Attractor (Point Pull)
Pulls particles toward a target point (e.g., a vortex or black hole):

```
dir = normalize(target - p)
dist = |target - p|
a_attractor = dir * (strength / max(dist, min_dist))
```

### Repulsor (Point Push)
Same as attractor but pushes away:

```
a_repulsor = -dir * (strength / max(dist, min_dist))
```

### Drag (Air Resistance)
Slows particles over time. Critical for smoke and dust:

```
a_drag = -v * drag_coefficient
```

---

## 5. Spawn Patterns

How particles are initially positioned and given velocity.

### Point
```
p = spawn_point
v = (0, 0, 0)   or random small offset
```

### Sphere (Explosion Burst)
```
theta = random(0, 2π)
phi   = random(0, π)
r     = spawn_radius
p = spawn_point + (r*sin(phi)*cos(theta), r*sin(phi)*sin(theta), r*cos(phi))
v = normalize(p - spawn_point) * speed
```

### Cone (Directional Spray)
```
axis = normalize(direction)
angle = random(0, cone_angle)
theta = random(0, 2π)
v = rotate_around(axis, theta) applied to a vector at `angle` from axis, scaled by speed
```

### Ring (Aura / Halo)
```
theta = random(0, 2π)
r = ring_radius
p = spawn_point + (r*cos(theta), 0, r*sin(theta))
v = (-sin(theta)*speed, 0, cos(theta)*speed)   // tangential velocity
```

### Line (Trail)
```
p = lerp(start, end, random(0, 1))
v = (0, 0, 0)   or inherit from moving source
```

### Helix (Level-Up Effect)
```
theta = t * angular_speed
r = helix_radius
p = spawn_point + (r*cos(theta), t * vertical_speed, r*sin(theta))
v = (-r*sin(theta)*angular_speed, vertical_speed, r*cos(theta)*angular_speed)
```

---

## 6. Visual Properties (Driven by Life Ratio r)

### Color Interpolation
Define color stops at specific life ratios:

```
stops = [(0.0, color_white), (0.3, color_yellow), (0.7, color_orange), (1.0, color_grey)]
c = interpolate_stops(stops, r)
```

### Alpha (Fade)
Common patterns:
- **Fade In/Out:** `α = sin(r * π)` — starts invisible, peaks at middle, fades out
- **Fade Out Only:** `α = 1.0 - r` — solid at birth, fades to nothing
- **Flicker:** `α = (1.0 - r) * (0.5 + 0.5 * sin(t * flicker_speed))`

### Size
- **Grow then Shrink:** `s = s_max * sin(r * π)`
- **Constant:** `s = s_max`
- **Shrink to nothing:** `s = s_max * (1.0 - r)`

---

## 7. Emitter Types

### Burst Emitter
Spawns N particles at once, all with initial velocities radiating outward. Used for explosions, critical hits, kill effects.

```
for i in range(count):
    particle = spawn_at(center)
    particle.velocity = random_direction() * speed
    particle.life = random(life_min, life_max)
```

### Stream Emitter
Spawns particles at a fixed rate per tick from a continuous source. Used for torches, waterfalls, aura effects.

```
if tick % spawn_rate == 0:
    particle = spawn_at(source_position)
    particle.velocity = base_velocity + random_offset
```

### Orbit Emitter
Particles maintain a fixed distance from a moving target, rotating around it. Used for halos, crowns, planet effects.

```
particle.position = target + (radius * cos(angle), height, radius * sin(angle))
angle += angular_speed * dt
```

### Trail Emitter
Spawns particles along the path of a moving entity. Used for movement trails, sword swings, rocket exhaust.

```
if distance_moved > threshold:
    particle = spawn_at(entity_previous_position)
    particle.velocity = (0, 0, 0)  // or inherit entity velocity
```

---

## 8. Performance Budget

| Metric | Budget | Rationale |
|--------|--------|-----------|
| Max particles/tick | 150 | Keeps MSPT under 50ms at 20 TPS |
| Max spawn radius | 32 blocks | Beyond this, players can't see particles |
| Max life | 80 ticks (4s) | Prevents memory accumulation |
| Noise samples/tick | 3 | Perlin noise is expensive; cache when possible |
| View-distance culling | 32 blocks | Don't send packets to players who can't see them |

---

## 9. Common Effect Recipes

### Phoenix Wings (Flapping)
```
// Two wings, each is a set of particles along a Bezier curve
left_wing_points = bezier_curve(wing_root, wing_tip, control_point)
right_wing_points = mirror(left_wing_points)
flap_offset = sin(t * flap_speed) * flap_amplitude
// Spawn particles along curves with flap_offset applied to Y
```

### Soul Harvest (Kill Effect)
```
// Burst at victim, then attract toward killer
phase 1 (ticks 0-5):  burst 30 particles outward (sphere pattern)
phase 2 (ticks 5-20):  attractor force toward killer.chest_position
                       drag = 0.05 (particles slow down as they arrive)
                       alpha = fade out as they get close to killer
```

### Critical Shockwave (Expanding Ring)
```
radius = initial_radius + (tick * expansion_speed)
for each particle in ring:
    angle = particle_index * (2π / particle_count)
    p = center + (radius*cos(angle), 0, radius*sin(angle))
    alpha = 1.0 - (radius / max_radius)
```

### DNA Double Helix
```
// Two intertwined spirals
for i in range(particles_per_strand):
    theta = (i / particles_per_strand) * 2π + t * rotation_speed
    strand1 = (r*cos(theta), i*vertical_step, r*sin(theta))
    strand2 = (r*cos(theta+π), i*vertical_step, r*sin(theta+π))  // 180° offset
```
