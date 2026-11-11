package com.particlefactory.math;

/**
 * Force functions — modify a particle's acceleration.
 * Mirrors particles/forces.py
 */
public class Forces {
    public static final Vec3 GRAVITY_EARTH = new Vec3(0, -0.08, 0);
    public static final Vec3 GRAVITY_MOON  = new Vec3(0, -0.02, 0);
    public static final Vec3 GRAVITY_NONE  = new Vec3(0, 0, 0);

    public static void gravity(Particle p, Vec3 g) {
        p.applyForce(g);
    }
    public static void gravity(Particle p) { gravity(p, GRAVITY_EARTH); }

    public static void wind(Particle p, Vec3 direction, double strength) {
        p.applyForce(direction.normalize().scale(strength));
    }

    public static void drag(Particle p, double coeff) {
        p.applyForce(p.vel.scale(-coeff));
    }

    public static void turbulence(Particle p, double strength, int seed, double scale) {
        Vec3 pos = p.pos;
        double nx = simpleNoise(pos.x * scale, pos.y * scale, pos.z * scale, seed);
        double ny = simpleNoise(pos.x * scale + 100, pos.y * scale + 100, pos.z * scale + 100, seed + 1);
        double nz = simpleNoise(pos.x * scale + 200, pos.y * scale + 200, pos.z * scale + 200, seed + 2);
        Vec3 force = new Vec3(nx * 2 - 1, ny * 2 - 1, nz * 2 - 1).scale(strength);
        p.applyForce(force);
    }

    public static void attractor(Particle p, Vec3 target, double strength, double minDist) {
        Vec3 diff = target.sub(p.pos);
        double dist = diff.length();
        if (dist < 0.001) return;
        Vec3 dir = diff.normalize();
        double mag = strength / Math.max(dist, minDist);
        p.applyForce(dir.scale(mag));
    }

    public static void repulsor(Particle p, Vec3 source, double strength, double minDist) {
        Vec3 diff = p.pos.sub(source);
        double dist = diff.length();
        if (dist < 0.001) return;
        Vec3 dir = diff.normalize();
        double mag = strength / Math.max(dist, minDist);
        p.applyForce(dir.scale(mag));
    }

    public static void vortex(Particle p, Vec3 center, Vec3 axis, double strength, double radius) {
        Vec3 ax = axis.normalize();
        Vec3 diff = p.pos.sub(center);
        Vec3 proj = diff.sub(ax.scale(diff.dot(ax)));
        double dist = proj.length();
        if (dist < 0.001) return;
        Vec3 tangent = ax.cross(proj.normalize());
        double falloff = Math.max(0, 1.0 - dist / radius);
        p.applyForce(tangent.scale(strength * falloff));
    }

    public static void buoyancy(Particle p, double strength) {
        p.applyForce(new Vec3(0, strength, 0));
    }

    // --- helpers ---
    private static double simpleNoise(double x, double y, double z, int seed) {
        double n = Math.sin(x * 12.9898 + y * 78.233 + z * 37.719 + seed) * 43758.5453;
        return n - Math.floor(n);
    }

    public static Vec3 randomDirection() {
        double theta = Math.random() * 2 * Math.PI;
        double phi = Math.acos(2 * Math.random() - 1);
        return new Vec3(
            Math.sin(phi) * Math.cos(theta),
            Math.sin(phi) * Math.sin(theta),
            Math.cos(phi)
        );
    }
}
