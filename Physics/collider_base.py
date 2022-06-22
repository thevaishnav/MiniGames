from __future__ import annotations
from MiniGames.Utils.type_checker import type_check, types_check
from MiniGames.Utils.decorators import inner_method
from MiniGames.Utils.vector2 import Vector2
from MiniGames.Utils.settings_and_info import Info, Settings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from MiniGames.Pipeline.gameobject import GameObject
    from MiniGames.Pipeline.transform import Transform


class ColliderBase:
    __COL_ID = 1
    @inner_method
    def __init__(self, go: GameObject):
        self.__go = go
        self.__is_enabled = True
        self.__is_trigger = False
        self.__id = ColliderBase.__COL_ID
        ColliderBase.__COL_ID += 1

    @property
    def is_trigger(self) -> bool:
        return self.__is_trigger

    @is_trigger.setter
    def is_trigger(self, value: bool):
        type_check("is_trigger", value, bool)
        self.__is_trigger = value

    @property
    def _col_id(self) -> int:
        return self.__id

    @property
    def enabled(self) -> bool:
        return self.__is_enabled

    @enabled.setter
    def enabled(self, value: bool):
        type_check("enabled", value, bool)
        if value == self.__is_enabled: return
        if value:
            Info.instance._add_to_active_colliders(self)
        else:
            Info.instance._rem_from_active_colliders(self)
        self.__is_enabled = value

    @property
    def gameobject(self) -> GameObject:
        return self.__go

    @property
    def transform(self) -> Transform:
        return self.__go.transform

    def remove(self) -> None:
        Info.instance._rem_from_active_colliders(self)
        del self

    def absolute_center_in_pixels(self) -> Vector2:
        trans = self.transform
        off = self.get_center_offset().rotate(trans.rotation) * Settings.space_scale * trans.lossy_scale * Vector2(1, -1)
        pos = trans.global_pos_in_pixels
        return Vector2(off.x + pos.x, off.y + pos.y)

    def get_center_offset(self) -> Vector2:
        """
        :return: By how much the center of collider is offset from center of gameobject.
        Don't account for Rotation and Scaling
        """
        raise NotImplementedError()

    def get_center(self) -> Vector2:
        """
        Note: Usually, taking average of all edge points should work, but you must account for Rotation and Scaling of Gameobject
        Remember: Rotate first, Scale second, and Translate third.
        The Good News is, this doesn't have to be accurate. Because the only time its used is to calculate initial direction for GJK algorythm.
        :return: Vector2(x_cord_of_center_of_shape, y_cord_of_center_of_shape)
        """
        raise NotImplementedError()

    def furthest_point(self, direction: Vector2) -> Vector2:
        """
        Note:
            For most polygons, it's the edge-point that maximizes the dot product with direction vector.
            But you will also need to account for Rotation and Scaling of the Gameobject
            Check out Support Point Calculation in GJK implementation
        Remember: Rotate first, Scale second, and Translate third.
        :return: furthest edge point on the curve, in direction defined by normal vector :param direction:
        """
        raise NotImplementedError()
