from __future__ import annotations
from pygame.color import Color as pyColor


class Color(pyColor):
    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"

    def __str__(self):
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"

    def __mul__(self, other: Color | int | float) -> Color:
        if type(other) is Color: return super(Color, self).__mul__(other)
        if type(other) is int: return Color(self.r * other, self.g * other, self.b * other, self.a * other)
        if type(other) is float: return Color(int(self.r * other), int(self.g * other), int(self.b * other), int(self.a * other))
        raise TypeError(f"unsupported operand type(s) for *: {type(other)} and 'Color'")

    @staticmethod
    def Lerp(c1: Color, c2: Color, t: float) -> Color:
        t1 = max(0.0, min(1.0, t))
        return (c2 * (1 - t1)) + (c1 * t1)

    @staticmethod
    def White() -> Color: return Color(255, 255, 255)

    @staticmethod
    def Black() -> Color: return Color(0, 0, 0)

    @staticmethod
    def Clear() -> Color: return Color(0, 0, 0, 0)

    @staticmethod
    def Maroon() -> Color:  return Color(128, 0, 0)

    @staticmethod
    def Red() -> Color:     return Color(255, 0, 0)

    @staticmethod
    def Orange() -> Color:  return Color(255, 165, 0)

    @staticmethod
    def Yellow() -> Color:  return Color(255, 255, 0)

    @staticmethod
    def Olive() -> Color:   return Color(128, 128, 0)

    @staticmethod
    def Green() -> Color:   return Color(0, 128, 0)

    @staticmethod
    def Collider_Green() -> Color:
        return Color(0, 255, 0)

    @staticmethod
    def Purple() -> Color:  return Color(128, 0, 128)

    @staticmethod
    def Fuchsia() -> Color: return Color(255, 0, 255)

    @staticmethod
    def Teal() -> Color:    return Color(0, 128, 128)

    @staticmethod
    def Aqua() -> Color:    return Color(0, 255, 255)

    @staticmethod
    def Blue() -> Color:    return Color(0, 0, 255)

    @staticmethod
    def Navy() -> Color:    return Color(0, 0, 128)

    @staticmethod
    def Gold() -> Color:    return Color(255, 215, 0)

    @staticmethod
    def Cyan() -> Color:    return Color(0, 255, 255)
