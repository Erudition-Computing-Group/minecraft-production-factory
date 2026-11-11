package com.particlefactory.math;

/**
 * Particle — core state object for a single visual sprite.
 * Mirrors particles/particle.py
 */
public class Particle {
    public Vec3 pos;
    public Vec3 vel;
    public Vec3 acc;
    public double life;
    public double maxLife;
    public double size;
    public double r, g, b;   // color channels 0.0-1.0
    public double alpha;
    public double rotation;

    public Particle(Vec3 pos, Vec3 vel, double life, double size,
                    double r, double g, double b, double alpha) {
        this.pos = (pos != null) ? pos : Vec3.zero();
        this.vel = (vel != null) ? vel : Vec3.zero();
        this.acc = Vec3.zero();
        this.life = life;
        this.maxLife = life;
        this.size = size;
        this.r = r; this.g = g; this.b = b;
        this.alpha = alpha;
        this.rotation = 0;
    }

    // convenience constructor
    public Particle(Vec3 pos, Vec3 vel, double life, double size, double[] color, double alpha) {
        this(pos, vel, life, size, color[0], color[1], color[2], alpha);
    }

    public double lifeRatio() {
        if (maxLife <= 0) return 1.0;
        return 1.0 - (life / maxLife);
    }

    public boolean isAlive() { return life > 0; }

    public void applyForce(Vec3 force) {
        acc = acc.add(force);
    }

    /** Semi-implicit Euler integration. */
    public void integrate(double dt) {
        vel = vel.add(acc.scale(dt));
        pos = pos.add(vel.scale(dt));
        life -= dt;
        acc = Vec3.zero();
    }

    /** Color gradient: stops = array of {ratio, r, g, b}. */
    public void setColorGradient(double[][] stops) {
        double ratio = lifeRatio();
        for (int i = 0; i < stops.length - 1; i++) {
            double r0 = stops[i][0], r1 = stops[i + 1][0];
            if (ratio >= r0 && ratio <= r1) {
                double t = (r1 != r0) ? (ratio - r0) / (r1 - r0) : 0;
                this.r = stops[i][1] + (stops[i + 1][1] - stops[i][1]) * t;
                this.g = stops[i][2] + (stops[i + 1][2] - stops[i][2]) * t;
                this.b = stops[i][3] + (stops[i + 1][3] - stops[i][3]) * t;
                return;
            }
        }
        this.r = stops[stops.length - 1][1];
        this.g = stops[stops.length - 1][2];
        this.b = stops[stops.length - 1][3];
    }

    public void setAlphaFadeOut() { alpha = Math.max(0, 1.0 - lifeRatio()); }
    public void setAlphaFadeInOut() { alpha = Math.max(0, Math.sin(lifeRatio() * Math.PI)); }
    public void setSizeShrink(double maxSize) { size = maxSize * (1.0 - lifeRatio()); }
    public void setSizeGrowShrink(double maxSize) { size = maxSize * Math.sin(lifeRatio() * Math.PI); }

    @Override
    public String toString() {
        return String.format("Particle(pos=%s, vel=%s, life=%.1f/%.1f, color=[%.2f,%.2f,%.2f], alpha=%.2f)",
            pos, vel, life, maxLife, r, g, b, alpha);
    }
}
