"""Vec3 — the fundamental math primitive for all particle spatial calculations."""
import math


class Vec3:
    __slots__ = ("x", "y", "z")

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    # --- arithmetic ---
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __truediv__(self, scalar):
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return f"Vec3({self.x:.4f}, {self.y:.4f}, {self.z:.4f})"

    # --- vector operations ---
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def length_squared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def normalize(self):
        ln = self.length()
        if ln == 0:
            return Vec3(0, 0, 0)
        return Vec3(self.x / ln, self.y / ln, self.z / ln)

    def lerp(self, other, t):
        return Vec3(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t,
            self.z + (other.z - self.z) * t,
        )

    def distance_to(self, other):
        return (self - other).length()

    def to_tuple(self):
        return (self.x, self.y, self.z)

    @staticmethod
    def from_tuple(t):
        return Vec3(t[0], t[1], t[2])

    @staticmethod
    def zero():
        return Vec3(0, 0, 0)

    @staticmethod
    def up():
        return Vec3(0, 1, 0)

    @staticmethod
    def forward():
        return Vec3(0, 0, 1)

    @staticmethod
    def lerp_static(a, b, t):
        return a.lerp(b, t)
