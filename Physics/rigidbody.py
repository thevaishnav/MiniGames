from __future__ import annotations
from MiniGames.Utils.type_checker import type_check, types_check, type_check_num
from MiniGames.Pipeline.monobehaviour import MonoBehaviour
from MiniGames.Utils.settings_and_info import Settings, Info
from MiniGames.Utils.vector2 import Vector2
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from MiniGames.Pipeline.gameobject import GameObject


class RigidBody(MonoBehaviour):
    def __init__(self, gameobject: GameObject):
        super(RigidBody, self).__init__(gameobject)
        self.__gravity_scale = 1
        self.__mass = 1
        self.__vel = Vector2()
        self.__acc = Vector2()

    def _collide_with(self, other: RigidBody):
        m1, m2 = self.__mass, other.__mass
        u1, u2 = self.__vel, other.__vel
        rep = 1 / (m1 + m2)
        dif = m1 - m2
        self.__vel = (dif * u1 + 2 * m2 * u2) * rep
        other.__vel = (2 * m1 * u1 - dif * u2) * rep

    def _on_game_start_mono(self):
        pass

    def _enable_mono(self):
        Info.instance._add_to_rbs(self)
        self.__enabled = True

    def _disable_mono(self):
        Info.instance._rem_from_rbs(self)
        self.__enabled = False

    @property
    def gravity_scale(self) -> float:
        return self.__gravity_scale

    @gravity_scale.setter
    def gravity_scale(self, value: float):
        type_check_num("gravity_scale", value)
        t = type(value)
        if t is not float and t is not int:
            raise ValueError(f"Invalid type for gravity_scale, expected 'float' got \'{t.__qualname__}\'")
        self.__gravity_scale = float(value)

    @property
    def mass(self) -> float:
        return self.__mass

    @mass.setter
    def mass(self, value: float):
        type_check_num("mass", value)
        if value <= 0: raise ValueError("Mass can't be negative or zero")
        self.__mass = value

    @property
    def velocity(self) -> Vector2:
        return self.__vel

    @velocity.setter
    def velocity(self, value: Vector2):
        types_check("velocity", value, Vector2)
        if type(value) is not Vector2: raise ValueError("Velocity must be a Vector")
        self.__vel = value

    def add_force(self, force: Vector2):
        types_check("force", force, Vector2)
        self.__acc = force / self.__mass

    def physics_update(self):
        if self.__gravity_scale != 0: self.add_force(Settings.gravity * self.__gravity_scale)
        self.__vel += self.__acc * Info.fixedDeltaTime
        posDelta = self.__vel * Info.fixedDeltaTime
        pos = self.transform.position
        new_val = pos + posDelta
        self.transform.position = new_val
