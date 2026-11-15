"""Colour conversion and perceptual colour-difference utilities.

The HEX conversion assumes IEC 61966-2-1 sRGB values, the D65 white
point, and the CIE 1931 2-degree standard observer.
"""

from __future__ import annotations

import math
import re
from typing import Sequence

_HEX_PATTERN = re.compile(r"^[0-9a-fA-F]{6}$")


def hex_to_lab(hex_value: str) -> tuple[float, float, float]:
    """Convert a six-digit sRGB HEX value to CIELAB (D65).

    A leading '#' is optional. Values are interpreted as encoded sRGB,
    linearised with the IEC sRGB transfer function, converted to XYZ,
    then to CIELAB using the D65 reference white.

    This conversion is for colour swatches. It does not estimate skin
    colour from a photograph or establish foundation suitability.
    """
    if not isinstance(hex_value, str):
        raise TypeError("HEX value must be a string.")

    value = hex_value.strip()
    if value.startswith("#"):
        value = value[1:]

    if not _HEX_PATTERN.fullmatch(value):
        raise ValueError(
            f"Invalid HEX value {hex_value!r}; expected exactly six hexadecimal digits."
        )

    encoded = [int(value[index:index + 2], 16) / 255.0 for index in (0, 2, 4)]

    def srgb_to_linear(channel: float) -> float:
        if channel <= 0.04045:
            return channel / 12.92
        return ((channel + 0.055) / 1.055) ** 2.4

    red, green, blue = (srgb_to_linear(channel) for channel in encoded)

    # sRGB / D65 to CIE XYZ, normalised to the D65 reference white.
    x = (0.4124564 * red + 0.3575761 * green + 0.1804375 * blue) / 0.95047
    y = (0.2126729 * red + 0.7151522 * green + 0.0721750 * blue) / 1.00000
    z = (0.0193339 * red + 0.1191920 * green + 0.9503041 * blue) / 1.08883

    epsilon = 216.0 / 24389.0
    kappa = 24389.0 / 27.0

    def xyz_to_lab_component(component: float) -> float:
        if component > epsilon:
            return component ** (1.0 / 3.0)
        return (kappa * component + 16.0) / 116.0

    fx, fy, fz = (
        xyz_to_lab_component(component) for component in (x, y, z)
    )

    lightness = 116.0 * fy - 16.0
    a_star = 500.0 * (fx - fy)
    b_star = 200.0 * (fy - fz)
    return lightness, a_star, b_star


def delta_e_2000(
    lab1: Sequence[float],
    lab2: Sequence[float],
    *,
    k_l: float = 1.0,
    k_c: float = 1.0,
    k_h: float = 1.0,
) -> float:
    """Return CIEDE2000 colour difference for two CIELAB triples.

    The default parametric factors (kL, kC, kH) are all 1. The
    implementation follows Sharma, Wu and Dalal (2005).
    """
    if len(lab1) != 3 or len(lab2) != 3:
        raise ValueError("Each Lab value must contain exactly three numbers.")

    values = tuple(float(value) for value in (*lab1, *lab2, k_l, k_c, k_h))
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Lab values and parametric factors must be finite.")
    if k_l <= 0 or k_c <= 0 or k_h <= 0:
        raise ValueError("CIEDE2000 parametric factors must be greater than zero.")

    l1, a1, b1, l2, a2, b2 = values[:6]

    c1 = math.hypot(a1, b1)
    c2 = math.hypot(a2, b2)
    c_bar = (c1 + c2) / 2.0

    c_bar_7 = c_bar ** 7
    g = (
        0.5 * (1.0 - math.sqrt(c_bar_7 / (c_bar_7 + 25.0 ** 7)))
        if c_bar > 0.0
        else 0.5
    )

    a1_prime = (1.0 + g) * a1
    a2_prime = (1.0 + g) * a2
    c1_prime = math.hypot(a1_prime, b1)
    c2_prime = math.hypot(a2_prime, b2)

    def hue_angle(a_value: float, b_value: float) -> float:
        if a_value == 0.0 and b_value == 0.0:
            return 0.0
        return math.degrees(math.atan2(b_value, a_value)) % 360.0

    h1_prime = hue_angle(a1_prime, b1)
    h2_prime = hue_angle(a2_prime, b2)

    delta_l_prime = l2 - l1
    delta_c_prime = c2_prime - c1_prime

    if c1_prime * c2_prime == 0.0:
        delta_h_angle = 0.0
    else:
        delta_h_angle = h2_prime - h1_prime
        if delta_h_angle > 180.0:
            delta_h_angle -= 360.0
        elif delta_h_angle < -180.0:
            delta_h_angle += 360.0

    delta_h_prime = (
        2.0
        * math.sqrt(c1_prime * c2_prime)
        * math.sin(math.radians(delta_h_angle / 2.0))
    )

    l_bar_prime = (l1 + l2) / 2.0
    c_bar_prime = (c1_prime + c2_prime) / 2.0

    if c1_prime * c2_prime == 0.0:
        h_bar_prime = h1_prime + h2_prime
    else:
        hue_difference = abs(h1_prime - h2_prime)
        hue_sum = h1_prime + h2_prime

        if hue_difference <= 180.0:
            h_bar_prime = hue_sum / 2.0
        elif hue_sum < 360.0:
            h_bar_prime = (hue_sum + 360.0) / 2.0
        else:
            h_bar_prime = (hue_sum - 360.0) / 2.0

    t = (
        1.0
        - 0.17 * math.cos(math.radians(h_bar_prime - 30.0))
        + 0.24 * math.cos(math.radians(2.0 * h_bar_prime))
        + 0.32 * math.cos(math.radians(3.0 * h_bar_prime + 6.0))
        - 0.20 * math.cos(math.radians(4.0 * h_bar_prime - 63.0))
    )

    delta_theta = 30.0 * math.exp(-((h_bar_prime - 275.0) / 25.0) ** 2)
    c_bar_prime_7 = c_bar_prime ** 7
    r_c = (
        2.0 * math.sqrt(c_bar_prime_7 / (c_bar_prime_7 + 25.0 ** 7))
        if c_bar_prime > 0.0
        else 0.0
    )

    s_l = 1.0 + (
        0.015 * (l_bar_prime - 50.0) ** 2
        / math.sqrt(20.0 + (l_bar_prime - 50.0) ** 2)
    )
    s_c = 1.0 + 0.045 * c_bar_prime
    s_h = 1.0 + 0.015 * c_bar_prime * t
    r_t = -math.sin(math.radians(2.0 * delta_theta)) * r_c

    term_l = delta_l_prime / (k_l * s_l)
    term_c = delta_c_prime / (k_c * s_c)
    term_h = delta_h_prime / (k_h * s_h)

    squared_distance = (
        term_l ** 2
        + term_c ** 2
        + term_h ** 2
        + r_t * term_c * term_h
    )
    return math.sqrt(max(0.0, squared_distance))
