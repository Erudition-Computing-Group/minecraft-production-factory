package com.particlefactory.emitters;

import com.particlefactory.math.Particle;
import com.particlefactory.math.Vec3;

import java.util.concurrent.ThreadLocalRandom;

/**
 * A low-rate, static gold sparkle emitter for a 2 x 2 x 2 block treasure area.
 * It emits at most one particle every 15 ticks, which is well below the factory
 * budget of 150 particles per tick.
 */
public class GoldenTreasureEmitter extends Emitter {
    private static final int EMIT_INTERVAL_TICKS = 15;
    private static final int ACTIVE_TICKS = 200;
    private static final double HALF_DIMENSION = 1.0;

    @Override
    public void update(double dt) {
        if (age < ACTIVE_TICKS && ((int) age) % EMIT_INTERVAL_TICKS == 0) {
            ThreadLocalRandom random = ThreadLocalRandom.current();
            particles.add(new Particle(
                new Vec3(
                    position.x + random.nextDouble(-HALF_DIMENSION, HALF_DIMENSION),
                    position.y + random.nextDouble(-HALF_DIMENSION, HALF_DIMENSION),
                    position.z + random.nextDouble(-HALF_DIMENSION, HALF_DIMENSION)
                ),
                Vec3.zero(),
                random.nextDouble(12.0, 24.0),
                0.12,
                new double[]{1.0, 0.78, 0.19},
                1.0
            ));
        }
        super.update(dt);
    }

    public GoldenTreasureEmitter(Vec3 position) {
        super(position);
    }

    @Override
    protected void applyForces(Particle particle) {
        // Static sparkles deliberately have no velocity, gravity, or turbulence.
    }
}
