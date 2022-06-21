from MiniGames.Renderers.renderer_base import RendererBase
from MiniGames.Utils.vector2 import Vector2
from MiniGames.Pipeline.transform import __U2P__Point__
from MiniGames.Pipeline.gameobject import GameObject
from MiniGames.Pipeline.camera import Camera


class PointRenderer(RendererBase):
    def __init__(self, gameobject: GameObject):
        super(PointRenderer, self).__init__(gameobject)
        self.__pPos = Vector2()

    def RecalculatePos(self): self.__pPos = __U2P__Point__(self.transform.position)
    def RecalculateRot(self): pass
    def RecalculateScale(self): pass

    def Render(self):
        Camera.draw_point(self.__pPos, self.color)
