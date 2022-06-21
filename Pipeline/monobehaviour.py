from __future__ import annotations, absolute_import
from MiniGames.Utils.settings_and_info import Info
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from MiniGames.Pipeline import transform as m_trans
    from MiniGames.Pipeline import gameobject as m_go


class MonoBehaviour:
    def __init__(self, gameobject: m_go.GameObject):
        self.__gameobject = gameobject
        self.__enabled = False
        self.__enable_on_start = True

    def __repr__(self):
        return str(id(self))

    def __str__(self):
        return str(id(self))

    def Call(self, what: str):
        if hasattr(self, what):
            try:
                self.__getattribute__(what).__call__()
            except AttributeError:
                raise AssertionError(f"func ({what}) can't be called on {type(self).__qualname__}")

    def Enable(self):
        if self.__enabled: return

        if hasattr(self, "update"): self.__gameobject.AddTo("u", self)
        if hasattr(self, "late_update"): self.__gameobject.AddTo("lu", self)
        if hasattr(self, "fixed_update"): self.__gameobject.AddTo("fu", self)
        if hasattr(self, "on_collision_enter"): self.__gameobject.AddTo("oci", self)
        if hasattr(self, "on_collision_exit"): self.__gameobject.AddTo("oco", self)
        if hasattr(self, "on_collision_stay"): self.__gameobject.AddTo("oco", self)
        if hasattr(self, "on_trigger_enter"): self.__gameobject.AddTo("oti", self)
        if hasattr(self, "on_trigger_exit"): self.__gameobject.AddTo("oto", self)
        if hasattr(self, "on_trigger_stay"): self.__gameobject.AddTo("oto", self)
        self.__enabled = True
        self.Call("on_enable")

    def Disable(self):
        if not self.__enabled: return
        self.__gameobject.RemoveFromMultiple(self, "u", "lu", "fu", "oci", "oco", "ocs", "oti", "oto", "ots")
        self.__enabled = False
        self.Call("on_disable")

    def OnGameStartMono(self):
        self.Call("awake")
        if self.__enable_on_start:
            self.Enable()
            if Info.is_loop_running: self.Call("start")
        self.__delattr__("_MonoBehaviour__enable_on_start")

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, value: bool):
        if Info.is_loop_running:
            if value:
                self.Enable()
            else:
                self.Disable()
            self.__enabled = value
        else:
            self.__enable_on_start = value

    @property
    def gameobject(self) -> m_go.GameObject:
        return self.__gameobject

    @property
    def transform(self) -> m_trans.Transform:
        return self.__gameobject._GameObject__transform

    def remove(self):
        self.Disable()
        self.Call("on_remove")
        del self
