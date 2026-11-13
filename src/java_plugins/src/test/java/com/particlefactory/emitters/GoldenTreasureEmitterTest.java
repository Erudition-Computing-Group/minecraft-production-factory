package com.particlefactory.emitters;

import com.particlefactory.math.Vec3;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class GoldenTreasureEmitterTest {
    @Test
    void emitsOneStaticParticleAtTheConfiguredInterval() {
        GoldenTreasureEmitter emitter = new GoldenTreasureEmitter(new Vec3(10, 64, -4));
        emitter.update(1.0);

        assertEquals(1, emitter.getAliveCount());
        var particle = emitter.getParticles().getFirst();
        assertTrue(Math.abs(particle.pos.x - 10) <= 1.0);
        assertTrue(Math.abs(particle.pos.y - 64) <= 1.0);
        assertTrue(Math.abs(particle.pos.z + 4) <= 1.0);
        assertEquals(0.0, particle.vel.x);
        assertEquals(0.0, particle.vel.y);
        assertEquals(0.0, particle.vel.z);

        for (int tick = 0; tick < 14; tick++) {
            emitter.update(1.0);
        }
        assertEquals(1, emitter.getAliveCount());

        emitter.update(1.0);
        assertEquals(2, emitter.getAliveCount());
    }
}
