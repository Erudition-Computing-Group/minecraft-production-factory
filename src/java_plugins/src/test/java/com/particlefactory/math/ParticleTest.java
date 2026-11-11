package com.particlefactory.math;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ParticleTest {

    @Test
    void lifeRatioAtBirth() {
        Particle p = new Particle(new Vec3(0, 0, 0), new Vec3(0, 0, 0), 20.0, 0.1,
                new double[]{1, 1, 1}, 1.0);
        assertEquals(0.0, p.lifeRatio(), 1e-9);
    }

    @Test
    void lifeRatioAtDeath() {
        Particle p = new Particle(new Vec3(0, 0, 0), new Vec3(0, 0, 0), 20.0, 0.1,
                new double[]{1, 1, 1}, 1.0);
        p.life = 0;
        assertEquals(1.0, p.lifeRatio(), 1e-9);
    }

    @Test
    void lifeRatioAtHalf() {
        Particle p = new Particle(new Vec3(0, 0, 0), new Vec3(0, 0, 0), 20.0, 0.1,
                new double[]{1, 1, 1}, 1.0);
        p.life = 10.0;
        assertEquals(0.5, p.lifeRatio(), 1e-9);
    }

    @Test
    void isAlive() {
        Particle p = new Particle(new Vec3(0, 0, 0), new Vec3(0, 0, 0), 5.0, 0.1,
                new double[]{1, 1, 1}, 1.0);
        assertTrue(p.isAlive());
        p.life = 0;
        assertFalse(p.isAlive());
    }

    @Test
    void integration() {
        Particle p = new Particle(new Vec3(0, 0, 0), new Vec3(1, 0, 0), 10.0, 0.1,
                new double[]{1, 1, 1}, 1.0);
        p.integrate(1.0);
        assertEquals(1.0, p.pos.x, 1e-9);
        assertEquals(9.0, p.life, 1e-9);
    }

    @Test
    void alphaFadeOut() {
        Particle p = new Particle(new Vec3(0, 0, 0), new Vec3(0, 0, 0), 20.0, 0.1,
                new double[]{1, 1, 1}, 1.0);
        p.life = 10.0;
        p.setAlphaFadeOut();
        assertEquals(0.5, p.alpha, 1e-9);
    }

    @Test
    void alphaFadeInOut() {
        Particle p = new Particle(new Vec3(0, 0, 0), new Vec3(0, 0, 0), 20.0, 0.1,
                new double[]{1, 1, 1}, 1.0);
        p.life = 10.0; // middle of life
        p.setAlphaFadeInOut();
        assertEquals(1.0, p.alpha, 1e-9);
    }
}
