from MiniGames.Utils.type_checker import type_check, types_check

from MiniGames.Pipeline.monobehaviour import MonoBehaviour
from MiniGames.Utils.color import Color
from MiniGames.Pipeline.gameobject import GameObject
from MiniGames.Utils.decorators import inner_method


class RendererBase(MonoBehaviour):
    @inner_method
    def __init__(self, gameobject: GameObject):
        super(RendererBase, self).__init__(gameobject)
        self.__color = Color.white()

        self.transform._add_to_on_pos_change(self._recalculate_pos)
        self.transform._add_to_on_scale_change(self._recalculate_scale)
        self.transform._add_to_on_rot_change(self._recalculate_rot)

    @property
    def color(self) -> Color:
        return self.__color

    @color.setter
    def color(self, value: Color):
        types_check("color", value, Color)
        if type(value) is not Color:
            raise TypeError()
        self.__color = value

    def _recalculate_rot(self): raise NotImplementedError()

    def _recalculate_scale(self): raise NotImplementedError()

    def _recalculate_pos(self): raise NotImplementedError()

    def _render(self): raise NotImplementedError()

    def _enable_mono(self):
        super(RendererBase, self)._enable_mono()
        self.gameobject._set_to("r", self)

    def _disable_mono(self):
        super(RendererBase, self)._disable_mono()
        self.gameobject._remove_from("r", self)
