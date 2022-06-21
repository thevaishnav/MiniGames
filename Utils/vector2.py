from __future__ import annotations
import math
import random
import numpy as np
from MiniGames.Utils import settings_and_info as mod_sai


class Vector2:
    def __init__(self, x: float = 0, y: float = 0):
        self.__X = round(x, 5)
        self.__Y = round(y, 5)
        self.__allow_modification = True

    def __len__(self):
        return 2

    def __iter__(self):
        yield self.__X
        yield self.__Y

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __call__(self) -> tuple[float, float]:
        return self.__X, self.__Y

    def __add__(self, other: float | Vector2):
        if type(other) is Vector2: return Vector2(self.x + other.x, self.y + other.y)
        if type(other) is float or type(other) is int: return Vector2(self.x + other, self.y + other)
        raise TypeError(f"unsupported operand type(s) for +: {type(other)} and 'Vector2'")

    def __sub__(self, other: float | Vector2):
        if type(other) is float or type(other) is int: return Vector2(self.x - other, self.y - other)
        if type(other) is Vector2: return Vector2(self.x - other.x, self.y - other.y)
        raise TypeError(f"unsupported operand type(s) for -: {type(other)} and 'Vector2'")

    def __mul__(self, other: float | Vector2):
        if type(other) is float or type(other) is int:
            return Vector2(self.x * other, self.y * other)
        if type(other) is Vector2:
            return Vector2(self.x * other.x, self.y * other.y)
        raise TypeError(f"unsupported operand type(s) for *: {type(other)} and 'Vector2'")

    def __truediv__(self, other: float | Vector2):
        if type(other) is float or type(other) is int:
            return Vector2(self.x / other, self.y / other)
        if type(other) is Vector2:
            return Vector2(self.x / other.x, self.y / other.y)
        raise TypeError(f"unsupported operand type(s) for /: {type(other)} and 'Vector2'")

    def __mod__(self, other: float | Vector2):
        if type(other) is Vector2:
            return Vector2(self.__X % other.__X, self.__Y % other.__Y)
        if type(other) is float or type(other) is int:
            return Vector2(self.__X % other, self.__Y % other)
        raise TypeError(f"unsupported operand type(s) for %: {type(other)} and 'Vector2'")

    def __floordiv__(self, other: float | Vector2):
        if type(other) is Vector2:
            return Vector2(self.__X // other.__X, self.__Y // other.__Y)
        if type(other) is float or type(other) is int:
            return Vector2(self.__X // other, self.__Y // other)
        raise TypeError(f"unsupported operand type(s) for //: {type(other)} and 'Vector2'")

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __eq__(self, other):
        if type(other) is not Vector2: return False
        return self.__X == other.__X and self.__Y == other.__Y

    def __ne__(self, other):
        if type(other) is not Vector2: return True
        return self.__X != other.__X or self.__Y != other.__Y

    def __iadd__(self, other: float | Vector2):
        return self.__add__(other)

    def __imul__(self, other: float | Vector2):
        return self.__mul__(other)

    def __isub__(self, other: float | Vector2):
        return self.__sub__(other)

    def __itruediv__(self, other: float | Vector2):
        return self.__truediv__(other)

    def __imod__(self, other: float | Vector2):
        return self.__mod__(other)

    def __ifloordiv__(self, other: float | Vector2):
        return self.__floordiv__(other)

    def __radd__(self, other: float | Vector2):
        return self + other

    def __rmul__(self, other: float | Vector2):
        return self * other

    def __rsub__(self, other: float | Vector2):
        if type(other) is float or type(other) is int:
            return Vector2(other - self.x, other - self.y)
        if type(other) is Vector2:
            return Vector2(other.x - self.x, other.y - self.y)
        raise TypeError(f"unsupported operand type(s) for -: {type(other)} and 'Vector2'")

    def __rtruediv__(self, other: float | Vector2):
        if type(other) is float or type(other) is int:
            return Vector2(other / self.x, other / self.y)
        if type(other) is Vector2:
            return Vector2(other.x / self.x, other.y / self.y)
        raise TypeError(f"unsupported operand type(s) for /: {type(other)} and 'Vector2'")

    def __rmod__(self, other: float | Vector2):
        if type(other) is float or type(other) is int:
            return Vector2(other % self.x, other % self.y)
        if type(other) is Vector2:
            return Vector2(other.x % self.x, other.y % self.y)
        raise TypeError(f"unsupported operand type(s) for %: {type(other)} and 'Vector2'")

    def __rfloordiv__(self, other: float | Vector2):
        if type(other) is float or type(other) is int:
            return Vector2(other // self.x, other // self.y)
        if type(other) is Vector2:
            return Vector2(other.x // self.x, other.y // self.y)
        raise TypeError(f"unsupported operand type(s) for //: {type(other)} and 'Vector2'")

    def FIX_SELF(self):
        self.__allow_modification = False
        return self

    @property
    def x(self) -> float:
        return self.__X

    @x.setter
    def x(self, value: float):
        if not self.__allow_modification:
            raise PermissionError("You are not allowed to change the value of X")
        self.__X = value

    @property
    def x_int(self):
        return int(self.__X)

    @property
    def y(self) -> float:
        return self.__Y

    @property
    def y_int(self):
        return int(self.__Y)

    @y.setter
    def y(self, value: float):
        if not self.__allow_modification: raise PermissionError("You are not allowed to change the value of Y")
        self.__Y = value

    @property
    def sqr_mag(self) -> float:
        return self.__X * self.__X + self.__Y * self.__Y

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.sqr_mag)

    @magnitude.setter
    def magnitude(self, val: float):
        if self.magnitude == 0: return
        m = val / self.magnitude
        self.x *= m
        self.y *= m

    @staticmethod
    def random(x_min=-5, x_max=5, y_min=-3, y_max=3, step=0.001):
        x = (random.random() * (x_max - x_min)) + x_min
        y = (random.random() * (y_max - y_min)) + y_min
        return Vector2(round(x / step) * step, round(y / step) * step)

    @staticmethod
    def zero():
        return Vector2(0, 0)

    @staticmethod
    def one():
        return Vector2(1, 1)

    @staticmethod
    def left():
        return Vector2(-1, 0)

    @staticmethod
    def right():
        return Vector2(1, 0)

    @staticmethod
    def up():
        return Vector2(0, 1)

    @staticmethod
    def down():
        return Vector2(0, -1)

    @staticmethod
    def triple_product(u: Vector2, v: Vector2, w: Vector2):
        """
        :return: (v1 x v2) x v3 == v1 x (v2 x v3)
        """
        return v * u.dot(w) - w * u.dot(v)

    @staticmethod
    def direction_vector(angle: float):
        a = math.radians(angle)
        return Vector2(round(math.sin(a), 3), round(math.cos(a), 3))

    def set_self(self, to_set: Vector2):
        self.__X = to_set.x
        self.__Y = to_set.y

    def rotate_self(self, angle: float):
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        newX = cos * self.x - sin * self.y
        newY = sin * self.x + cos * self.y
        self.x, self.y = newX, newY

    def scale_self(self, factor: float):
        self.__X *= factor
        self.__Y *= factor

    def offset(self, pos_off: Vector2, scale_off: Vector2, rot_off: float, do_space_scaling: bool = False):
        if do_space_scaling:
            vec = self * mod_sai.Settings.space_scale
        else:
            vec = self.copy()
        vec.rotate_self(-rot_off)
        vec.__X = pos_off.__X + vec.__X * scale_off.__X  # scale, pos
        vec.__Y = pos_off.__Y + vec.__Y * scale_off.__Y
        return vec

    def offset_reverse(self, pos_off: Vector2, scale_off: Vector2, rot_off: float, do_space_scaling: bool = False):
        vec = self - pos_off  # pos
        vec.__X /= scale_off.__X  # scale,
        vec.__Y /= scale_off.__Y  # scale,
        vec.rotate_self(rot_off)
        if do_space_scaling:
            vec.__X /= mod_sai.Settings.space_scale.__X
            vec.__Y /= mod_sai.Settings.space_scale.__Y
            return vec
        return vec

    def normalize_self(self):
        mag = self.magnitude
        if mag == 0: return
        mag = 1 / mag
        self.__X *= mag
        self.__Y *= mag

    def to_np_array(self):
        return np.array([self.__X, self.__Y])

    def abs(self) -> Vector2:
        return Vector2(abs(self.__X), abs(self.__Y))

    def normalized(self) -> Vector2:
        mag = self.magnitude
        if mag == 0: return Vector2.zero()
        mag = 1 / mag
        return Vector2(self.x * mag, self.y * mag)

    def reflected(self, reflect_on: Vector2) -> Vector2:
        n = reflect_on.normalized()
        dot = (self * n)
        return self - (dot * 2) * n

    def dot(self, other: Vector2) -> float:
        return self.x * other.x + self.y * other.y

    def rotate(self, angle: float) -> Vector2:
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        # print(f'cos({angle}) = {cos}, sin({angle}) = {sin}')
        newX = cos * self.__X - sin * self.__Y
        newY = sin * self.__X + cos * self.__Y
        return Vector2(newX, newY)

    def project_on(self, other: Vector2) -> Vector2:
        normy = other.normalized()
        dot = self.dot(normy)
        return Vector2(dot * normy.x, dot * normy.y)

    def sqr_dist_from(self, other: Vector2) -> float:
        return (other.x - self.x) ** 2 + (other.y - self.y) ** 2

    def dist_from(self, other: Vector2) -> float:
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def copy(self) -> Vector2:
        return Vector2(self.x, self.y)
