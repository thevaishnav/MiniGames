from MiniGames.Utils.type_checker import type_check, types_check, type_check_num

from MiniGames.Utils.vector2 import Vector2
from MiniGames.Physics.collider_base import ColliderBase
from MiniGames.Pipeline.gameobject import GameObject
from MiniGames.Utils.settings_and_info import Settings
from MiniGames.Renderers.collider_renderer import ColliderRenderer
from MiniGames.Renderers.shapes import ShapeCircle


class CircleCollider(ColliderBase):
    def __init__(self, go: GameObject):
        super(CircleCollider, self).__init__(go)
        self.__center_off = Vector2.zero()
        self.__shape = ShapeCircle(1, Settings.colliders_thickness)
        self.__renderer = ColliderRenderer(self, self.__shape, self.transform)
        go._set_to("hidden_rend", self.__renderer)

    @property
    def center_offset(self) -> Vector2: return self.__center_off

    @center_offset.setter
    def center_offset(self, value: Vector2):
        types_check("center_offset", value, Vector2)
        self.__center_off = value
        self.__shape._recalculate_pos()

    @property
    def radius(self) -> float: return self.__shape.radius

    @radius.setter
    def radius(self, value: float):
        type_check_num("radius", value)
        self.__shape.radius = value

    def get_center_offset(self) -> Vector2: return self.__center_off

    def get_center(self) -> Vector2:
        trans = self.transform
        off = self.__center_off.rotate(self.transform.rotation) * trans.lossy_scale
        return off + trans.position

    def furthest_point(self, direction: Vector2) -> Vector2:
        types_check("direction", direction, Vector2)
        direct = direction.normalized()
        trans = self.transform
        rot = trans.rotation
        direct.rotate_self(-rot)
        p = direct * trans.lossy_scale * self.__shape.radius
        p.rotate_self(rot)
        return p + self.get_center()
