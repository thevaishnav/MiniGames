from MiniGames.Utils.type_checker import type_check, types_check

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
        type_check("pos_count", value, int)
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
        type_check("index", index, int)
        types_check("position", position, Vector2)
        if index >= self.__pos_count:
            raise IndexError(f"Index index > pos_count ({index} > {self.__pos_count})")
        self.__py_pos[index] = __U2P__Point__(position)

    def get_position(self, index: int):
        type_check("index", index, int)
        if index >= self.__pos_count:
            raise IndexError(f"Index index > pos_count ({index} > {self.__pos_count})")
        return __P2U__Point__(self.__py_pos[index])

    def _recalculate_rot(self):
        pass

    def _recalculate_scale(self):
        pass

    def _recalculate_pos(self):
        pass

    def _render(self):
        for i in range(self.__pos_count - 1):
            Camera._draw_line(self.__py_pos[i], self.__py_pos[i + 1], self.color)
