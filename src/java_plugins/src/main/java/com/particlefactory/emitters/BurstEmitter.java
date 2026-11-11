package com.particlefactory.emitters;

import com.particlefactory.math.Forces;
import com.particlefactory.math.Particle;
import com.particlefactory.math.Spawners;
import com.particlefactory.math.Vec3;

public class BurstEmitter extends Emitter {
    private final int count;
    private final double speed, life, size;
    private final double r, g, b;
    private boolean spawned = false;

    public BurstEmitter(Vec3 position, int count, double speed, double life,
                        double size, double r, double g, double b) {
        super(position);
        this.count = count;
        this.speed = speed;
        this.life = life;
        this.size = size;
        this.r = r; this.g = g; this.b = b;
    }

    public void spawn() {
        if (spawned) return;
        particles = Spawners.spawnSphere(position, count, 0.3, speed, life, size, r, g, b);
        spawned = true;
    }

    @Override
    protected void applyForces(Particle p) {
        Forces.gravity(p);
        Forces.drag(p, 0.03);
        Forces.turbulence(p, 0.02, 42, 0.5);
    }
}
