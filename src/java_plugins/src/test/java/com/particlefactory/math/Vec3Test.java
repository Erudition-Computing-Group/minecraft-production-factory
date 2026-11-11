package com.particlefactory.math;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Vec3Test {

    @Test
    void addition() {
        Vec3 a = new Vec3(1, 2, 3);
        Vec3 b = new Vec3(4, 5, 6);
        Vec3 r = a.add(b);
        assertEquals(5, r.x, 1e-9);
        assertEquals(7, r.y, 1e-9);
        assertEquals(9, r.z, 1e-9);
    }

    @Test
    void subtraction() {
        Vec3 a = new Vec3(4, 5, 6);
        Vec3 b = new Vec3(1, 2, 3);
        Vec3 r = a.sub(b);
        assertEquals(3, r.x, 1e-9);
        assertEquals(3, r.y, 1e-9);
        assertEquals(3, r.z, 1e-9);
    }

    @Test
    void scaling() {
        Vec3 v = new Vec3(1, 2, 3);
        Vec3 r = v.scale(2);
        assertEquals(2, r.x, 1e-9);
        assertEquals(4, r.y, 1e-9);
        assertEquals(6, r.z, 1e-9);
    }

    @Test
    void dotProduct() {
        Vec3 a = new Vec3(1, 2, 3);
        Vec3 b = new Vec3(4, 5, 6);
        assertEquals(32, a.dot(b), 1e-9);
    }

    @Test
    void crossProduct() {
        Vec3 a = new Vec3(1, 0, 0);
        Vec3 b = new Vec3(0, 1, 0);
        Vec3 r = a.cross(b);
        assertEquals(0, r.x, 1e-9);
        assertEquals(0, r.y, 1e-9);
        assertEquals(1, r.z, 1e-9);
    }

    @Test
    void length() {
        Vec3 v = new Vec3(3, 4, 0);
        assertEquals(5, v.length(), 1e-9);
    }

    @Test
    void normalize() {
        Vec3 v = new Vec3(3, 4, 0);
        Vec3 n = v.normalize();
        assertEquals(1.0, n.length(), 1e-9);
        assertEquals(0.6, n.x, 1e-9);
        assertEquals(0.8, n.y, 1e-9);
    }

    @Test
    void lerp() {
        Vec3 a = new Vec3(0, 0, 0);
        Vec3 b = new Vec3(10, 10, 10);
        Vec3 r = a.lerp(b, 0.5);
        assertEquals(5, r.x, 1e-9);
        assertEquals(5, r.y, 1e-9);
        assertEquals(5, r.z, 1e-9);
    }

    @Test
    void zeroVector() {
        Vec3 z = Vec3.zero();
        assertEquals(0, z.x, 1e-9);
        assertEquals(0, z.y, 1e-9);
        assertEquals(0, z.z, 1e-9);
        assertEquals(0, z.length(), 1e-9);
    }
}
