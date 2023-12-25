import math


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other_position):
        """Calculate the Euclidean distance between two positions."""
        dx = self.x - other_position.x
        dy = self.y - other_position.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Vector addition."""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Vector subtraction."""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """Scalar multiplication."""
        return Vector(self.x * scalar, self.y * scalar)

    def magnitude(self):
        """Calculate the magnitude (length or size) of the
        vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)
