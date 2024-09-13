"""
Author: Nadav Cohen
Date: 13/9/2024
Description: shape warehouse class
"""
import random
from Rectangle import Rectangle
from Square import Square
from Circle import Circle


class ShapeWarehouse:
    COLORS = ["Red", "Green", "Blue", "Purple", "White", "Black"]

    def __init__(self):
        """
        initializer for shape warehouse
        """
        self.shapes = []

    def generate(self, x):
        """
        generates x amounts of shapes into the warehouse
        :param x:
        :return:
        """
        for i in range(x):
            color = random.choice(self.COLORS)
            shape_index = random.randint(1, 4)
            if shape_index == 1:
                self.shapes.append(Circle(color, random.randint(1, 20)))
            if shape_index == 2:
                side1 = random.randint(1, 20)
                side2 = random.randint(1, 20)
                while side1 == side2:
                    side2 = random.randint(1, 20)
                self.shapes.append(Rectangle(color, side1, side2))
            if shape_index == 3:
                num = random.randint(1, 20)
                self.shapes.append(Square(color, num, num))

    def sum_area(self) -> float:
        """
        adds up the area of all the shapes in the warehouse
        :return:
        """
        sum_area = 0
        for shape in self.shapes:
            sum_area += shape.calc_area()
        return sum_area

    def sum_perimeter(self):
        """
        adds up the perimeters of all the shapes in the warehouse
        :return:
        """
        sum_perimeter = 0
        for shape in self.shapes:
            sum_perimeter += shape.calc_perimeter()
        return sum_perimeter

    def count_colors(self):
        """
        counts how many of each color there is in the warehouse
        :return:
        """
        color_count = dict.fromkeys(ShapeWarehouse.COLORS, 0)

        for shape in self.shapes:
            color_count[shape.get_color()] += 1

        return color_count
