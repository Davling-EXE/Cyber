"""
Author: Nadav Cohen
Date: 13/9/2024
Description: shape class
"""


class Shape:
    def __init__(self, color):
        """
        initializer for shape
        :param color:
        """
        self.color = color

    def set_color(self, color):
        """
        sets the color of the shape
        :param color:
        :return:
        """
        self.color = color

    def get_color(self):
        """
        returns the color of the shape
        :return:
        """
        return self.color

    def calc_area(self):
        """
        calcs the area of the shape (defined by subclass)
        :return:
        """
        pass

    def calc_perimeter(self):
        """
        calcs the perimeter of the shape (defined by subclass)
        :return:
        """
        pass
