"""
Author: Nadav Cohen
Date: 13/9/2024
Description: square class
"""
from Rectangle import Rectangle


class Square(Rectangle):
    def __int__(self, color,  width):
        """
        initializer for square
        :param color:
        :param width:
        """
        super().__init__(color, width, width)
