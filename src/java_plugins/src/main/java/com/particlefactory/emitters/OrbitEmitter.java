package com.particlefactory.emitters;

import com.particlefactory.math.Particle;
import com.particlefactory.math.Spawners;
import com.particlefactory.math.Vec3;
import java.util.ArrayList;
import java.util.List;

public class OrbitEmitter extends Emitter {
    private final int count;
    private final double radius, height, angularSpeed, life, size;
    private final double r, g, b;
    private double angleOffset = 0;

    public OrbitEmitter(Vec3 position, int count, double radius, double height,
                        double angularSpeed, double life, double size,
                        double r, double g, double b) {
        super(position);
        this.count = count;
        this.radius = radius;
        this.height = height;
        this.angularSpeed = angularSpeed;
        this.life = life;
        this.size = size;
        this.r = r; this.g = g; this.b = b;
        // pre-spawn
        particles = Spawners.spawnRing(position, count, radius, 0, life, size, r, g, b);
    }

    @Override
    public void update(double dt) {
        age += dt;
        angleOffset += angularSpeed * dt;
        List<Particle> alive = new ArrayList<>();
        for (int i = 0; i < particles.size(); i++) {
            Particle p = particles.get(i);
            double theta = (i / (double) count) * 2 * Math.PI + angleOffset;
            p.pos = new Vec3(
                position.x + radius * Math.cos(theta),
                position.y + height,
                position.z + radius * Math.sin(theta)
            );
            p.life -= dt;
            if (p.isAlive()) alive.add(p);
        }
        particles = alive;
        // respawn
        while (particles.size() < count) {
            int i = particles.size();
            double theta = (i / (double) count) * 2 * Math.PI + angleOffset;
            Particle p = new Particle(
                new Vec3(position.x + radius * Math.cos(theta),
                         position.y + height,
                         position.z + radius * Math.sin(theta)),
                Vec3.zero(), life, size, new double[]{r, g, b}, 1.0
            );
            particles.add(p);
        }
    }

    @Override
    protected void applyForces(Particle p) {
        // orbit is kinematic, no forces needed
    }
}
