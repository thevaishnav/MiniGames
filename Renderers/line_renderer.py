from MiniGames.Utils.vector2 import Vector2
from MiniGames.Pipeline.transform import __U2P__Point__, __P2U__Point__
from MiniGames.Pipeline.camera import Camera
from MiniGames.Renderers.renderer_base import RendererBase
from MiniGames.Pipeline.gameobject import GameObject


class LineRenderer(RendererBase):
    def __init__(self, gameobject: GameObject):
        super(LineRenderer, self).__init__(gameobject)
        self.__pos_count = 0
        self.__py_pos: dict[int, Vector2] = {}

    @property
    def pos_count(self) -> int:
        return self.__pos_count

    @pos_count.setter
    def pos_count(self, value: int):
        self.__pos_count = value
        lp = len(self.__py_pos)
        if value > lp:
            zero = __U2P__Point__(Vector2.zero())
            for i in range(lp, value):
                self.__py_pos[i] = zero.copy()
        elif lp > value:
            for i in range(value, lp):
                self.__py_pos.pop(i)

    def set_position(self, index: int, position: Vector2):
        if index >= self.__pos_count:
            raise IndexError(f"Index index > pos_count ({index} > {self.__pos_count})")
        self.__py_pos[index] = __U2P__Point__(position)

    def get_position(self, index: int):
        if index >= self.__pos_count:
            raise IndexError(f"Index index > pos_count ({index} > {self.__pos_count})")
        return __P2U__Point__(self.__py_pos[index])

    def RecalculateRot(self):
        pass

    def RecalculateScale(self):
        pass

    def RecalculatePos(self):
        pass

    def Render(self):
        for i in range(self.__pos_count - 1):
            Camera.draw_line(self.__py_pos[i], self.__py_pos[i + 1], self.color)
