"""
Author: Nadav Cohen
Date: 13/9/2024
Description: circle class
"""
import Shape
import math


class Circle(Shape.Shape):
    def __init__(self, color, radius):
        """
        initializer for circle
        :param color:
        """
        super().__init__(color)
        self.radius = float(radius)

    def calc_area(self) -> float:
        """
        calcs area of circle
        :return:
        """
        return math.pi * self.radius * self.radius

    def calc_perimeter(self):
        """
        calcs perimeter of circle
        :return:
        """
        return 2 * math.pi * self.radius
