"""
Author: Nadav Cohen
Date: 10/5/2023
Description: helping romeo decrypt and encrypt his letters
"""
import math
from ShapeWarehouse import ShapeWarehouse
from Rectangle import Rectangle
from Square import Square
from Circle import Circle


def test_rectangle():
    """
    Tests for the Rectangle class.

    :return: None
    """

    rect1 = Rectangle("White", 6, 4)
    rect2 = Rectangle("Black", 8, 3)

    # Test color
    assert rect1.get_color() == "White"

    # Test area calculation
    assert rect1.calc_area() == 24

    # Test perimeter calculation
    assert rect1.calc_perimeter() == 20

    # Test color change
    rect1.set_color("Black")
    assert rect1.get_color() == "Black"

    # Test addition of rectangles
    combo_rect = rect1 + rect2

    # Verify the dimensions of the resulting rectangle
    assert math.isclose(combo_rect.width, 14, rel_tol=1e-9)
    assert math.isclose(combo_rect.length, 7, rel_tol=1e-9)

    # Verify that the color is one of the original colors
    assert combo_rect.get_color() in ["Black", "Black"]


def test_circle():
    """
    Tests for the Circle class.

    :return: None
    """

    circ = Circle("Purple", 14)

    # Test color
    assert circ.get_color() == "Purple"

    # Test area calculation
    assert circ.calc_area() == math.pi * 196

    # Test perimeter calculation
    assert circ.calc_perimeter() == 2 * math.pi * 14


def test_shape_container():
    """
    Tests for the ShapeContainer class.

    :return: None
    """

    shape_num = 5

    Warehouse = ShapeWarehouse()

    # Generate shapes
    Warehouse.generate(shape_num)

    # Test sum_area and sum_perimeter with generated shapes
    area_sum = Warehouse.sum_area()
    perimeter_sum = Warehouse.sum_perimeter()

    # Check if sums are positive
    assert area_sum > 0
    assert perimeter_sum > 0

    # Test color count
    color_count = Warehouse.count_colors()

    # check all colors are present
    assert sorted(ShapeWarehouse.COLORS) == sorted(color_count.keys())
    # Check if color counts are correct and non-negative and in range
    for color in ShapeWarehouse.COLORS:
        assert 0 <= color_count[color] <= shape_num


def main():
    my_container = ShapeWarehouse()
    my_container.generate(100)
    print("total area:", my_container.sum_area())
    print("total perimeter:", my_container.sum_perimeter())
    print("colors:", my_container.count_colors())


if __name__ == '__main__':
    test_rectangle()
    test_circle()
    test_shape_container()
    main()
