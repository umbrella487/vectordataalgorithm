#import python modules required
from math import sqrt
from typing import Union

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
    def __init__(self, x:Union[float,int], y:Union[float,int]):
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
       A enclosed feature consisting of series of points connected together

       Has length and Area.
       
       Attributes
       ----------
       Length
       Summation of all distance between successive points
       
       Area
       ----
       returns the area of the enclosed area"""

    def __init__(self, inputs):
        for obj in inputs:
            if type(obj) != Point:
                raise TypeError('Cannot create polyline object with given argument.Input must be an iterable of Points')
        if len(inputs) < 2:
            raise Exception('Cannot create polyline object with given argument. Insufficeint number of points')
        
        self.__inputs = inputs
        self.__inputs.append(self.__inputs[0])

    @property
    def Length(self):
        """returns the length of the linear feature"""
        sum = 0.0
        for i in range(0, len(self.__inputs) - 1):
            sum += self.__inputs[i].distance_to_other(self.__inputs[i+1])

        return sum


    @property
    def Area(self):
        """returns the area of the enclosed figure"""
        sum = 0.0
        for i in range(0, len(self.__inputs) - 1):
            sum += ((self.__inputs[i].X * self.__inputs[i+1].Y) - (self.__inputs[i+1].X * self.__inputs[i].Y))
        sum *=0.5

        return abs(sum)