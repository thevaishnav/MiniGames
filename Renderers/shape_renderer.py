from __future__ import annotations
import typing
from MiniGames.Utils.type_checker import type_check
from MiniGames.Renderers.renderer_base import RendererBase
from MiniGames.Pipeline.transform import __U2P__Point__
from MiniGames.Pipeline import gameobject as mod_go
from MiniGames.Renderers import shapes as mod_shapes

if typing.TYPE_CHECKING:
    from MiniGames.Renderers.shapes import ShapeBase as ShapeBaseAnot
    from MiniGames.Pipeline.gameobject import GameObject as GameObjectAnot
    from MiniGames.Utils.vector2 import Vector2 as Vector2Anot


class ShapeRenderer(RendererBase):
    def __init__(self, gameobject: GameObjectAnot):
        super(ShapeRenderer, self).__init__(gameobject)
        self.__shape = mod_shapes.ShapeCircle(1, 5)
        self.__shape._set_renderer(self)

    @property
    def shape(self) -> ShapeBaseAnot:
        return self.__shape

    @shape.setter
    def shape(self, value: ShapeBaseAnot):
        t = type(value)
        if not issubclass(t, mod_shapes.ShapeBase):
            raise TypeError(f"Invalid type for \'value\': Expected \'ShapeBase\' got \'{t.__qualname__}\'")

        if self.__shape:
            del self.__shape
        self.__shape = value
        value._set_renderer(self)

    def _recalculate_pos(self): self.__shape._recalculate_pos()

    def _recalculate_scale(self): self.__shape._recalculate_scale()

    def _recalculate_rot(self): self.__shape._recalculate_rot()

    def _render(self): self.__shape._render()

    @property
    def _absolute_rotation(self) -> float:
        return self.transform.rotation

    @property
    def _absolute_center(self) -> Vector2Anot:
        return __U2P__Point__(self.transform.position)
