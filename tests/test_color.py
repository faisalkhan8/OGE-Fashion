"""Tests for sRGB-to-Lab conversion and CIEDE2000."""

import unittest

from oge_fashion.color import delta_e_2000, hex_to_lab


class HexToLabTests(unittest.TestCase):
    def test_white_reference(self):
        lightness, a_star, b_star = hex_to_lab("#FFFFFF")
        self.assertAlmostEqual(lightness, 100.0, places=4)
        self.assertAlmostEqual(a_star, 0.0, places=3)
        self.assertAlmostEqual(b_star, 0.0, places=3)

    def test_black_reference(self):
        lightness, a_star, b_star = hex_to_lab("000000")
        self.assertAlmostEqual(lightness, 0.0, places=5)
        self.assertAlmostEqual(a_star, 0.0, places=5)
        self.assertAlmostEqual(b_star, 0.0, places=5)

    def test_srgb_red_reference(self):
        lightness, a_star, b_star = hex_to_lab("FF0000")
        self.assertAlmostEqual(lightness, 53.2408, places=3)
        self.assertAlmostEqual(a_star, 80.0925, places=3)
        self.assertAlmostEqual(b_star, 67.2032, places=3)

    def test_invalid_hex_is_rejected(self):
        for value in ("FFF", "#FFFF", "GGGGGG", "", "12345678"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    hex_to_lab(value)


class CIEDE2000ReferenceTests(unittest.TestCase):
    # Standard reference pairs published by Sharma, Wu and Dalal (2005).
    # The expected values are rounded to four decimal places.
    REFERENCE_PAIRS = (
        ((50.0000, 2.6772, -79.7751), (50.0000, 0.0000, -82.7485), 2.0425),
        ((50.0000, 3.1571, -77.2803), (50.0000, 0.0000, -82.7485), 2.8615),
        ((50.0000, 2.8361, -74.0200), (50.0000, 0.0000, -82.7485), 3.4412),
        ((50.0000, -1.3802, -84.2814), (50.0000, 0.0000, -82.7485), 1.0000),
        ((50.0000, -1.1848, -84.8006), (50.0000, 0.0000, -82.7485), 1.0000),
        ((50.0000, -0.9009, -85.5211), (50.0000, 0.0000, -82.7485), 1.0000),
        ((50.0000, 0.0000, 0.0000), (50.0000, -1.0000, 2.0000), 2.3669),
        ((50.0000, 2.4900, -0.0010), (50.0000, -2.4900, 0.0009), 7.1792),
    )

    def test_reference_pairs(self):
        for lab1, lab2, expected in self.REFERENCE_PAIRS:
            with self.subTest(expected=expected, lab1=lab1, lab2=lab2):
                self.assertAlmostEqual(
                    delta_e_2000(lab1, lab2),
                    expected,
                    delta=0.0001,
                )

    def test_identical_colours_have_zero_distance(self):
        lab = (52.1, 13.2, -4.5)
        self.assertAlmostEqual(delta_e_2000(lab, lab), 0.0, places=10)

    def test_invalid_parametric_factor_is_rejected(self):
        with self.assertRaises(ValueError):
            delta_e_2000((50, 0, 0), (50, 1, 1), k_l=0)


if __name__ == "__main__":
    unittest.main()
