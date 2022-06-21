from __future__ import annotations

from typing import TYPE_CHECKING
from MiniGames import Vector2
from MiniGames.Physics.collider_base import ColliderBase
from MiniGames.Utils.settings_and_info import Settings
from MiniGames.Renderers.collider_renderer import ColliderRenderer
from MiniGames.Renderers.shapes import ShapeBox

if TYPE_CHECKING:
    from MiniGames.Pipeline.gameobject import GameObject


class BoxCollider(ColliderBase):
    def __init__(self, go: GameObject):
        super(BoxCollider, self).__init__(go)
        self.__center_off = Vector2.zero()
        self.__shape = ShapeBox(Vector2.one(), Settings.colliders_thickness)
        self.__renderer = ColliderRenderer(self, self.__shape, self.transform)
        go.AddTo("hidden_rend", self.__renderer)

    @property
    def center_offset(self) -> Vector2:
        return self.__center_off

    @center_offset.setter
    def center_offset(self, value: Vector2):
        self.__center_off = value
        self.__shape.RecalculateScale()

    @property
    def size(self) -> Vector2:
        return self.__shape.size

    @size.setter
    def size(self, value: Vector2):
        self.__shape.size = value

    def get_center_offset(self) -> Vector2:
        return self.__center_off

    def get_center(self) -> Vector2:
        trans = self.transform
        off = self.__center_off.rotate(trans.rotation) * trans.lossy_scale
        return off + trans.position

    def furthest_point(self, direction: Vector2) -> Vector2:
        trans = self.transform
        rot = trans.rotation
        scale = trans.lossy_scale
        dire = direction.rotate(-rot)

        size = self.size / 2
        cent = self.get_center()
        p2 = (cent + size) * scale
        p1 = (cent - size) * scale
        size.y = -size.y
        p3 = (cent + size) * scale
        p4 = (cent - size) * scale
        p1d = p1.dot(dire)
        p2d = p2.dot(dire)
        p3d = p3.dot(dire)
        p4d = p4.dot(dire)
        mx = max(p1d, p2d, p3d, p4d)
        if mx == p1d:
            return p1.rotate(rot)
        if mx == p2d:
            return p2.rotate(rot)
        if mx == p3d:
            return p3.rotate(rot)
        if mx == p4d:
            return p4.rotate(rot)
