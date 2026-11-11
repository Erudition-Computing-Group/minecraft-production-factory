package com.particlefactory.math;

/**
 * Vec3 — the fundamental math primitive for all particle spatial calculations.
 * Mirrors particles/vector.py
 */
public class Vec3 {
    public double x, y, z;

    public Vec3() { this(0, 0, 0); }
    public Vec3(double x, double y, double z) { this.x = x; this.y = y; this.z = z; }

    // --- arithmetic ---
    public Vec3 add(Vec3 o) { return new Vec3(x + o.x, y + o.y, z + o.z); }
    public Vec3 sub(Vec3 o) { return new Vec3(x - o.x, y - o.y, z - o.z); }
    public Vec3 scale(double k) { return new Vec3(x * k, y * k, z * k); }
    public Vec3 neg() { return new Vec3(-x, -y, -z); }
    public Vec3 div(double k) { return new Vec3(x / k, y / k, z / k); }

    // --- vector ops ---
    public double dot(Vec3 o) { return x * o.x + y * o.y + z * o.z; }
    public Vec3 cross(Vec3 o) {
        return new Vec3(
            y * o.z - z * o.y,
            z * o.x - x * o.z,
            x * o.y - y * o.x
        );
    }
    public double length() { return Math.sqrt(x * x + y * y + z * z); }
    public double lengthSq() { return x * x + y * y + z * z; }
    public Vec3 normalize() {
        double l = length();
        if (l == 0) return new Vec3(0, 0, 0);
        return div(l);
    }
    public Vec3 lerp(Vec3 o, double t) {
        return new Vec3(
            x + (o.x - x) * t,
            y + (o.y - y) * t,
            z + (o.z - z) * t
        );
    }
    public double distanceTo(Vec3 o) { return sub(o).length(); }

    // --- static helpers ---
    public static Vec3 zero() { return new Vec3(0, 0, 0); }
    public static Vec3 up() { return new Vec3(0, 1, 0); }
    public static Vec3 from(double x, double y, double z) { return new Vec3(x, y, z); }

    public double[] toArray() { return new double[]{x, y, z}; }

    @Override
    public String toString() {
        return String.format("Vec3(%.4f, %.4f, %.4f)", x, y, z);
    }
}
