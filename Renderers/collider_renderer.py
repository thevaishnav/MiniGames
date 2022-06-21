from __future__ import annotations
from MiniGames.Utils.settings_and_info import Settings

import typing
if typing.TYPE_CHECKING:
    from MiniGames.Utils.vector2 import Vector2
    from MiniGames.Pipeline.transform import Transform
    from MiniGames.Physics.collider_base import ColliderBase
    from MiniGames.Renderers.shape_renderer import ShapeBase


class ColliderRenderer:
    def __init__(self, collider: ColliderBase, shape: ShapeBase, transform: Transform):
        self.__shape = shape
        self.__transform = transform
        self.__shape.SET_RENDERER(self)
        self.__collider = collider

        self.transform.ADD_TO_ON_POS_CHANGE(self.__shape.RecalculatePos)
        self.transform.ADD_TO_ON_SCA_CHANGE(self.__shape.RecalculateScale)
        self.transform.ADD_TO_ON_ROT_CHANGE(self.__shape.RecalculateRot)

    @property
    def transform(self):
        return self.__transform

    @property
    def color(self):
        return Settings.colliders_color

    def Render(self):
        self.__shape.Render()

    @property
    def ABS_ROT(self):
        return self.transform.rotation

    @property
    def ABS_CENT(self) -> Vector2:
        return self.__collider.absolute_center_in_pixels()
