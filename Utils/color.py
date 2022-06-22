from __future__ import annotations
from MiniGames.Utils.type_checker import types_check, type_check_num

from pygame.color import Color as pyColor


class Color(pyColor):
    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"

    def __str__(self):
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"

    def __mul__(self, other: Color | int | float) -> Color:
        types_check("other", other, Color, int, float)
        if type(other) is Color: return super(Color, self).__mul__(other)
        if type(other) is int: return Color(self.r * other, self.g * other, self.b * other, self.a * other)
        if type(other) is float: return Color(int(self.r * other), int(self.g * other), int(self.b * other), int(self.a * other))
        raise TypeError(f"unsupported operand type(s) for *: {type(other)} and 'Color'")

    @staticmethod
    def lerp(c1: Color, c2: Color, t: float) -> Color:
        types_check("c1", c1, Color)
        types_check("c2", c2, Color)
        type_check_num("t", t)
        t1 = max(0.0, min(1.0, t))
        return (c2 * (1 - t1)) + (c1 * t1)

    @staticmethod
    def white() -> Color: return Color(255, 255, 255)

    @staticmethod
    def black() -> Color: return Color(0, 0, 0)

    @staticmethod
    def clear() -> Color: return Color(0, 0, 0, 0)

    @staticmethod
    def maroon() -> Color:  return Color(128, 0, 0)

    @staticmethod
    def red() -> Color:     return Color(255, 0, 0)

    @staticmethod
    def orange() -> Color:  return Color(255, 165, 0)

    @staticmethod
    def yellow() -> Color:  return Color(255, 255, 0)

    @staticmethod
    def olive() -> Color:   return Color(128, 128, 0)

    @staticmethod
    def green() -> Color:   return Color(0, 128, 0)

    @staticmethod
    def collider_green() -> Color:
        return Color(0, 255, 0)

    @staticmethod
    def purple() -> Color:  return Color(128, 0, 128)

    @staticmethod
    def fuchsia() -> Color: return Color(255, 0, 255)

    @staticmethod
    def teal() -> Color:    return Color(0, 128, 128)

    @staticmethod
    def aqua() -> Color:    return Color(0, 255, 255)

    @staticmethod
    def blue() -> Color:    return Color(0, 0, 255)

    @staticmethod
    def navy() -> Color:    return Color(0, 0, 128)

    @staticmethod
    def gold() -> Color:    return Color(255, 215, 0)

    @staticmethod
    def cyan() -> Color:    return Color(0, 255, 255)
