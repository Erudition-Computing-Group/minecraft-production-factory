package com.particlefactory.emitters;

import com.particlefactory.math.Particle;
import com.particlefactory.math.Vec3;
import java.util.ArrayList;
import java.util.List;

/**
 * Base emitter — manages a list of particles, updates them each tick.
 * Mirrors particles/emitters.py
 */
public abstract class Emitter {
    protected Vec3 position;
    protected List<Particle> particles = new ArrayList<>();
    protected double age = 0;

    public Emitter(Vec3 position) {
        this.position = position;
    }

    public void update(double dt) {
        age += dt;
        for (Particle p : particles) {
            applyForces(p);
            p.integrate(dt);
        }
        particles.removeIf(p -> !p.isAlive());
    }

    protected abstract void applyForces(Particle p);

    public int getAliveCount() { return particles.size(); }
    public List<Particle> getParticles() { return particles; }
    public Vec3 getPosition() { return position; }
}
