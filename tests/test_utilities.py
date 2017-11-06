import math
import unittest
import utilities


class UtilitiesTestCase(unittest.TestCase):
    def test_unit_circle_angle(self):
        angles = list(range(-20, 20))
        hypotenuse = 5
        assumed_angles = {}
        for angle in angles:
            opposite = hypotenuse * math.sin(angle)
            assumed_angles[angle] = opposite

        for angle in angles:
            with self.subTest(angle=angle):
                converted_angle = utilities.unit_angle(angle)
                self.assertLessEqual(converted_angle, math.pi * 2)
                self.assertGreaterEqual(converted_angle, 0)
                opposite = hypotenuse * math.sin(converted_angle)
                self.assertAlmostEqual(assumed_angles[angle], opposite, 10)

    def test_unit_circle_angle_bounds(self):
        hypotenuse = 10
        angles = (0, math.pi * 2)

        for angle in angles:
            with self.subTest(angle=angle):
                expected_adjacent = hypotenuse
                adjacent = hypotenuse * math.cos(utilities.unit_angle(angle))
                self.assertAlmostEqual(adjacent, expected_adjacent)

                expected_opposite = 0
                opposite = hypotenuse * math.sin(utilities.unit_angle(angle))
                self.assertAlmostEqual(opposite, expected_opposite)
