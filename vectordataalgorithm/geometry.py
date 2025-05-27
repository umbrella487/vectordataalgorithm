#import python modules required
from math import sqrt

class Point:
    """
    Represents a 2D point in Cartesian (planar) space.
    Commonly used in GIS, mapping, and spatial analysis.
    """
    def __init__(self, x: float | int, y: float | int):
        """Initialize x-y components of point."""
        if not isinstance(x, (float, int)):
            raise TypeError('x must be a number (float or int)')
        if not isinstance(y, (float, int)):
            raise TypeError('y must be a number (float or int)')
        self.__x = float(x)
        self.__y = float(y)

    @property
    def X(self) -> float:
        """Return x-component (easting) of point."""
        return self.__x

    @property
    def Y(self) -> float:
        """Return y-component (northing) of point."""
        return self.__y

    def distance_to_other(self, other: 'Point') -> float:
        """Return the Euclidean distance to another Point."""
        if not isinstance(other, Point):
            raise TypeError(f'Input must be of type Point, not {type(other)}')
        return sqrt((other.Y - self.Y) ** 2 + (other.X - self.X) ** 2)

    def to_tuple(self) -> tuple:
        """Return the (x, y) tuple representation."""
        return (self.__x, self.__y)

    def __eq__(self, other) -> bool:
        """Check if another object is a Point with the same coordinates."""
        return isinstance(other, Point) and self.X == other.X and self.Y == other.Y

    def __str__(self) -> str:
        """Return the string format of a point object."""
        return f'Point(X={self.__x}, Y={self.__y})'

    def __repr__(self) -> str:
        """Return the official string representation."""
        return f'Point({self.__x}, {self.__y})'


class Polyline:
    """
    Represents a linear feature as a series of connected points (vertices).
    Commonly used for roads, rivers, and other linear features in GIS/mapping.
    """

    def __init__(self, vertices):
        if not all(isinstance(obj, Point) for obj in vertices):
            raise TypeError('All elements must be Point instances')
        if len(vertices) < 2:
            raise ValueError('Polyline requires at least two points')
        self.__vertices = list(vertices)

    @property
    def Length(self):
        """Returns the total length (sum of segment distances)."""
        return sum(self.__vertices[i].distance_to_other(self.__vertices[i+1]) for i in range(len(self.__vertices) - 1))

    @property
    def is_closed(self):
        """Returns True if the polyline is closed (first and last vertex are the same)."""
        return self.__vertices[0] == self.__vertices[-1]

    def to_lines(self):
        """Returns a list of (Point, Point) tuples representing each segment."""
        return [(self.__vertices[i], self.__vertices[i+1]) for i in range(len(self.__vertices) - 1)]

    def reverse(self):
        """Reverses the order of the vertices."""
        self.__vertices.reverse()

    def __len__(self):
        """Returns the number of vertices."""
        return len(self.__vertices)

    def __getitem__(self, idx):
        """Allows indexing into the vertices."""
        return self.__vertices[idx]

    def __repr__(self):
        return f'Polyline({self.__vertices})'


class Polygon():
    """Description:
       ------------
       An enclosed feature consisting of a series of points connected together.

       Has length and area, and supports spatial analysis operations.
    """

    def __init__(self, inputs):
        for obj in inputs:
            if type(obj) != Point:
                raise TypeError('Cannot create polygon object with given argument. Input must be an iterable of Points')
        if len(inputs) < 3:
            raise Exception('Cannot create polygon object with given argument. Insufficient number of points')
        self.__inputs = list(inputs)
        if self.__inputs[0] != self.__inputs[-1]:
            self.__inputs.append(self.__inputs[0])

    @property
    def Length(self):
        """Returns the perimeter of the polygon."""
        return sum(self.__inputs[i].distance_to_other(self.__inputs[i+1]) for i in range(len(self.__inputs) - 1))

    @property
    def Area(self):
        """Returns the area of the enclosed figure (Shoelace formula)."""
        area = 0.0
        for i in range(len(self.__inputs) - 1):
            area += (self.__inputs[i].X * self.__inputs[i+1].Y) - (self.__inputs[i+1].X * self.__inputs[i].Y)
        return abs(area) * 0.5

    @property
    def Centroid(self):
        """Returns the centroid (geometric center) of the polygon as a Point."""
        x_sum = 0.0
        y_sum = 0.0
        area = self.Area
        factor = 0.0
        for i in range(len(self.__inputs) - 1):
            cross = (self.__inputs[i].X * self.__inputs[i+1].Y) - (self.__inputs[i+1].X * self.__inputs[i].Y)
            x_sum += (self.__inputs[i].X + self.__inputs[i+1].X) * cross
            y_sum += (self.__inputs[i].Y + self.__inputs[i+1].Y) * cross
            factor += cross
        if factor == 0:
            return None  # Degenerate polygon
        cx = x_sum / (3 * factor)
        cy = y_sum / (3 * factor)
        return Point(cx, cy)

    @property
    def BoundingBox(self):
        """Returns the bounding box as (min_x, min_y, max_x, max_y)."""
        xs = [pt.X for pt in self.__inputs]
        ys = [pt.Y for pt in self.__inputs]
        return (min(xs), min(ys), max(xs), max(ys))

    @property
    def is_clockwise(self):
        """Returns True if the polygon vertices are ordered clockwise."""
        sum = 0.0
        for i in range(len(self.__inputs) - 1):
            sum += (self.__inputs[i+1].X - self.__inputs[i].X) * (self.__inputs[i+1].Y + self.__inputs[i].Y)
        return sum > 0

    def contains_point(self, point):
        """Ray casting algorithm for point-in-polygon test."""
        x, y = point.X, point.Y
        inside = False
        n = len(self.__inputs) - 1
        for i in range(n):
            xi, yi = self.__inputs[i].X, self.__inputs[i].Y
            xj, yj = self.__inputs[i+1].X, self.__inputs[i+1].Y
            intersect = ((yi > y) != (yj > y)) and \
                        (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi)
            if intersect:
                inside = not inside
        return inside