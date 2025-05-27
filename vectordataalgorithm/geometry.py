#import python modules required
from math import sqrt

class Point():
    """Description:
       ------------
       A point refers to the x-y coordinate pair that defines the geographic location
       of a Feature.
       
       Attribute
       ---------
       X - Component
       Defines how far a point is from the origin along the x-axis
       
       Y - Component
       Defines how far a point is from the origin along the y- axis
       
       Methods
       -------
       distance_to_other()
       
        returns the distance to other shape objects
       """
    def __init__(self, x:float|int, y:float|int):
        """intialize x-y components of point"""
        if type(x) != float and type(x) != int:
            raise TypeError('Cannot create point object with given x-argument. Input must be a number')
        if type(y) != float and type(y) != int:
            raise TypeError('Cannot create point object with given y-argument. Input must be a number')

        self.__x = x
        self.__y = y

    @property
    def X(self):
        """return x-component of point object"""
        return self.__x

    @property
    def Y(self):
        """return the y-component of a point object"""
        return self.__y
    
    def distance_to_other(self, other):
        """return the distance to other point object"""
        if type(other) != Point:
            raise TypeError('Cannot perform operation with given argument. input must be of type:{}'.format(type(self)))
        
        return sqrt((other.Y - self.Y)**2 + (other.X - self.X)**2)

    def __eq__(self, __o):
        """compares a given object to an instance"""
        if __o != None or type(__o) != Point:
            return False
        return __o.X == self.__x and __o.Y == self.__y

    
    def __str__(self):
        """returns the string format of a point object"""
        return 'X:{} Y:{}'.format(self.__x, self.__y)


class Polyline():
    """Description:
       ------------
       A linear feature consisting of series of points connected together
       
       Attributes
       ----------
       Length
       Summation of all distance between successive points"""

    def __init__(self, inputs):
        for obj in inputs:
            if type(obj) != Point:
                raise TypeError('Cannot create polyline object with given argument.Input must be an iterable of Points')
        if len(inputs) < 2:
            raise Exception('Cannot create polyline object with given argument. Insufficeint number of points')
        
        self.__inputs = inputs

    @property
    def Length(self):
        """returns the length of the linear feature"""
        sum = 0.0
        for i in range(0, len(self.__inputs) - 1):
            sum += self.__inputs[i].distance_to_other(self.__inputs[i+1])

        return sum


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