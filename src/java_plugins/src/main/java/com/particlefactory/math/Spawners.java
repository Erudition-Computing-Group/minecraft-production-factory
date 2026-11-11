package com.particlefactory.math;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Spawn patterns — initial position and velocity for particles.
 * Mirrors particles/spawners.py
 */
public class Spawners {
    private static final Random RNG = new Random();

    public static List<Particle> spawnSphere(Vec3 center, int count, double radius,
                                             double speed, double life, double size,
                                             double r, double g, double b) {
        List<Particle> out = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            Vec3 dir = Forces.randomDirection();
            Vec3 pos = center.add(dir.scale(radius));
            Vec3 vel = dir.scale(speed);
            double l = life + (RNG.nextDouble() * 4 - 2);
            out.add(new Particle(pos, vel, l, size, new double[]{r, g, b}, 1.0));
        }
        return out;
    }

    public static List<Particle> spawnRing(Vec3 center, int count, double radius,
                                           double speed, double life, double size,
                                           double r, double g, double b) {
        List<Particle> out = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            double theta = (i / (double) count) * 2 * Math.PI;
            Vec3 pos = new Vec3(
                center.x + radius * Math.cos(theta),
                center.y,
                center.z + radius * Math.sin(theta)
            );
            Vec3 vel = new Vec3(-Math.sin(theta) * speed, 0, Math.cos(theta) * speed);
            out.add(new Particle(pos, vel, life, size, new double[]{r, g, b}, 1.0));
        }
        return out;
    }

    public static List<Particle> spawnHelix(Vec3 center, int count, double radius,
                                            double verticalSpeed, double angularSpeed,
                                            double life, double size,
                                            double r, double g, double b) {
        List<Particle> out = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            double theta = (i / (double) count) * 2 * Math.PI;
            // strand 1
            Vec3 p1 = new Vec3(
                center.x + radius * Math.cos(theta),
                center.y + i * verticalSpeed,
                center.z + radius * Math.sin(theta)
            );
            Vec3 v1 = new Vec3(
                -radius * Math.sin(theta) * angularSpeed,
                verticalSpeed,
                radius * Math.cos(theta) * angularSpeed
            );
            out.add(new Particle(p1, v1, life, size, new double[]{r, g, b}, 1.0));
            // strand 2 (180° offset)
            Vec3 p2 = new Vec3(
                center.x + radius * Math.cos(theta + Math.PI),
                center.y + i * verticalSpeed,
                center.z + radius * Math.sin(theta + Math.PI)
            );
            Vec3 v2 = new Vec3(
                -radius * Math.sin(theta + Math.PI) * angularSpeed,
                verticalSpeed,
                radius * Math.cos(theta + Math.PI) * angularSpeed
            );
            out.add(new Particle(p2, v2, life, size, new double[]{r, g, b}, 1.0));
        }
        return out;
    }
}
