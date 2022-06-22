from __future__ import annotations, absolute_import
from MiniGames.Utils.type_checker import type_check
from MiniGames.Utils.decorators import inner_method
from MiniGames.Utils.settings_and_info import Info
from typing import TYPE_CHECKING
from MiniGames.Pipeline import gameobject as m_go

if TYPE_CHECKING:
    from MiniGames.Pipeline.transform import Transform as TransAnot
    from MiniGames.Pipeline.gameobject import GameObject as GameObjectAnot


class MonoBehaviour:
    @inner_method
    def __init__(self, gameobject: GameObjectAnot):
        type_check("gameobject", gameobject, m_go.GameObject)
        self.__gameobject = gameobject
        self.__enabled = False
        self.__enable_on_start = True

    def __repr__(self):
        return str(id(self))

    def __str__(self):
        return str(id(self))

    def _call(self, what: str):
        if hasattr(self, what):
            att = self.__getattribute__(what)
            att()
            # try:
            # except AttributeError:
            #     raise AssertionError(f"func ({what}) can't be called on {type(self).__qualname__}. {what} type is \'{type(att).__qualname__}\' and value is \'{att}\'")

    def _enable_mono(self):
        if self.__enabled: return

        if hasattr(self, "update"): self.__gameobject._set_to("u", self)
        if hasattr(self, "late_update"): self.__gameobject._set_to("lu", self)
        if hasattr(self, "fixed_update"): self.__gameobject._set_to("fu", self)
        if hasattr(self, "on_collision_enter"): self.__gameobject._set_to("oci", self)
        if hasattr(self, "on_collision_exit"): self.__gameobject._set_to("oco", self)
        if hasattr(self, "on_collision_stay"): self.__gameobject._set_to("oco", self)
        if hasattr(self, "on_trigger_enter"): self.__gameobject._set_to("oti", self)
        if hasattr(self, "on_trigger_exit"): self.__gameobject._set_to("oto", self)
        if hasattr(self, "on_trigger_stay"): self.__gameobject._set_to("oto", self)
        self.__enabled = True
        self._call("on_enable")

    def _disable_mono(self):
        if not self.__enabled: return
        self.__gameobject._remove_from_multiple(self, "u", "lu", "fu", "oci", "oco", "ocs", "oti", "oto", "ots")
        self.__enabled = False
        self._call("on_disable")

    def _on_game_start_mono(self):
        self._call("awake")
        if self.__enable_on_start:
            self._enable_mono()
            if Info.is_loop_running: self._call("start")
        self.__delattr__("_MonoBehaviour__enable_on_start")

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, value: bool):
        type_check("enabled", value, bool)
        if Info.is_loop_running:
            if value:
                self._enable_mono()
            else:
                self._disable_mono()
            self.__enabled = value
        else:
            self.__enable_on_start = value

    @property
    def gameobject(self) -> GameObjectAnot:
        return self.__gameobject

    @property
    def transform(self) -> TransAnot:
        return self.__gameobject._GameObject__transform

    def remove(self):
        self._disable_mono()
        self._call("on_remove")
        del self
