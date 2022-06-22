from __future__ import annotations
from MiniGames.Utils.type_checker import type_check, types_check

from MiniGames.Utils.settings_and_info import Settings

import typing
from MiniGames.Utils.decorators import inner_method

if typing.TYPE_CHECKING:
    from MiniGames.Utils.vector2 import Vector2
    from MiniGames.Pipeline.transform import Transform
    from MiniGames.Physics.collider_base import ColliderBase
    from MiniGames.Renderers.shape_renderer import ShapeBase


class ColliderRenderer:
    @inner_method
    def __init__(self, collider: ColliderBase, shape: ShapeBase, transform: Transform):
        self.__shape = shape
        self.__transform = transform
        self.__shape._set_renderer(self)
        self.__collider = collider

        self.transform._add_to_on_pos_change(self.__shape._recalculate_pos)
        self.transform._add_to_on_scale_change(self.__shape._recalculate_scale)
        self.transform._add_to_on_rot_change(self.__shape._recalculate_rot)

    @property
    def transform(self):
        return self.__transform

    @property
    def color(self):
        return Settings.colliders_color

    def _render(self):
        self.__shape._render()

    @property
    def _absolute_rotation(self) -> float:
        return self.transform.rotation

    @property
    def _absolute_center(self) -> Vector2:
        return self.__collider.absolute_center_in_pixels()
