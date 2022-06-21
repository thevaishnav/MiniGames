from __future__ import annotations

import typing

from MiniGames.Renderers.renderer_base import RendererBase
from MiniGames.Renderers.shapes import ShapeCircle
from MiniGames.Pipeline.transform import __U2P__Point__

if typing.TYPE_CHECKING:
    from MiniGames.Renderers.shapes import ShapeBase as ShapeBaseAnot
    from MiniGames.Pipeline.gameobject import GameObject as GameObjectAnot
    from MiniGames.Utils.vector2 import Vector2 as Vector2Anot


class ShapeRenderer(RendererBase):
    def __init__(self, gameobject: GameObjectAnot):
        super(ShapeRenderer, self).__init__(gameobject)
        self.__shape = ShapeCircle(1, 5)
        self.__shape.SET_RENDERER(self)

    @property
    def shape(self) -> ShapeBaseAnot:
        return self.__shape

    @shape.setter
    def shape(self, value: ShapeBaseAnot):
        if self.__shape:
            del self.__shape
        self.__shape = value
        value.SET_RENDERER(self)

    def RecalculatePos(self): self.__shape.RecalculatePos()

    def RecalculateScale(self): self.__shape.RecalculateScale()

    def RecalculateRot(self): self.__shape.RecalculateRot()

    def Render(self): self.__shape.Render()

    @property
    def ABS_ROT(self) -> float:
        return self.transform.rotation

    @property
    def ABS_CENT(self) -> Vector2Anot:
        return __U2P__Point__(self.transform.position)
