"""
Author: Nadav Cohen
Date: 13/9/2024
Description: rectangle class
"""
from Shape import Shape
import random


"""
constants
"""


class Rectangle(Shape):
    def __init__(self, color, width, length):
        """
        initializer for Rectangle
        :param color:
        :param width:
        :param length:
        """
        super().__init__(color)
        self.width = float(width)
        self.length = float(length)

    def calc_area(self):
        """
        calcs the area of the rectangle
        :return:
        """
        return self.width * self.length

    def calc_perimeter(self):
        """
        calcs the perimeter of the squares
        :return:
        """
        return 2 * (self.width + self.length)

    def __add__(self, other):
        """
        fuses two rectangles
        :param other:
        :return:
        """
        new_width = self.width + other.width
        new_length = self.length + other.length
        new_color = self.color if random.randint(1, 2) == 1 else other.color
        return Rectangle(new_color, new_width, new_length)
