from MiniGames.Utils.type_checker import type_check

from MiniGames.Renderers.renderer_base import RendererBase
from MiniGames.Utils.vector2 import Vector2
from MiniGames.Pipeline.transform import __U2P__Point__
from MiniGames.Pipeline.gameobject import GameObject
from MiniGames.Pipeline.camera import Camera


class PointRenderer(RendererBase):
    def __init__(self, gameobject: GameObject):
        super(PointRenderer, self).__init__(gameobject)
        self.__pPos = Vector2()

    def _recalculate_pos(self): self.__pPos = __U2P__Point__(self.transform.position)
    def _recalculate_rot(self): pass
    def _recalculate_scale(self): pass

    def _render(self):
        Camera._draw_point(self.__pPos, self.color)
