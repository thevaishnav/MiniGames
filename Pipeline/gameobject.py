from __future__ import annotations
from MiniGames.Pipeline.monobehaviour import MonoBehaviour
from MiniGames.Pipeline.transform import Transform
from MiniGames.Pipeline.coroutines import WaitFor
from MiniGames.Pipeline.storages import GameObjectsStorage
from MiniGames.Physics.collider_base import ColliderBase
from MiniGames.Physics.rigidbody import RigidBody
from MiniGames.Utils.settings_and_info import Info, Settings
from MiniGames.Utils.exceptions import InvalidComponentError
from MiniGames.Utils.exceptions import MultiRigidbodyError

import typing
if typing.TYPE_CHECKING:
    from MiniGames.Renderers.renderer_base import RendererBaseAnot


class GameObject:
    def __init__(self, name: str):
        if not Info.has_been_init():
            raise BrokenPipeError("Too early to create a Game Object. Must call \"App.init\" first")
        self.__rb = None
        self.name = name
        self.__transform = Transform(self)
        self.__is_active = False
        self.__activate_on_start = True
        self.__Storage = GameObjectsStorage()
        self.__activate_when_parent_does = True
        Info.instance.AddToActiveGameObjects(self)
        if Info.is_loop_running:
            self.OnGameStart()

    @property
    def gameobject(self) -> GameObject:
        return self

    @property
    def transform(self) -> Transform:
        return self.__transform

    def OnGameStart(self):
        if not self.__activate_on_start: return

        for mono in self.__Storage.LoopAll():
            mono.OnGameStartMono()
        self.__is_active = True

    def SETRB(self, rb: RigidBody):
        if self.__rb is not None: return False
        self.__rb = rb
        return True

    def AddTo(self, code: str, mono: MonoBehaviour or ColliderBase or RendererBaseAnot):
        self.__Storage.add_to(code, mono)

    def RemoveFrom(self, code: str, mono: MonoBehaviour):
        self.__Storage.rem_from(code, mono)

    def AddToMultiple(self, mono: MonoBehaviour, *codes):
        for code in codes:
            self.__Storage.add_to(code, mono)

    def RemoveFromMultiple(self, mono: MonoBehaviour, *codes):
        for code in codes:
            self.__Storage.rem_from(code, mono)

    def PARENT_ACTIVATED(self):
        self.__is_active = self.__activate_when_parent_does
        self.CallOnMonos("on_enabled")
        for child in self.__transform:
            child.gameobject.PARENT_ACTIVATED()

    def PARENT_DEACTIVATED(self):
        self.__activate_when_parent_does = bool(self.__is_active)
        self.__is_active = False
        self.CallOnMonos("on_disabled")
        for child in self.__transform:
            child.gameobject.PARENT_ACTIVATED()

    def GOUpdate(self):
        for mono in self.__Storage.Loop("u"): mono.update()
        for mono in self.__Storage.Loop("lu"): mono.late_update()
        for rend in self.__Storage.Loop("r"): rend.Render()
        self.__Storage.HandleCour()
        if not Settings.draw_colliders: return

        for rend in self.__Storage.Loop("hidden_rend"):
            rend.Render()

    def CallOnMonos(self, to_call: str):
        if not self.__is_active: return
        for mono in self.__Storage.LoopAll():
            mono.Call(to_call)

    def CallOnMonos_OCEn(self, other: ColliderBase):
        for go in self.__Storage.Loop("oci"):
            go.on_collision_enter(other)

    def CallOnMonos_OCEx(self, other: ColliderBase):
        for go in self.__Storage.Loop("oco"):
            go.on_collision_exit(other)

    def CallOnMonos_OCSt(self, other: ColliderBase):
        for go in self.__Storage.Loop("ocs"):
            go.on_collision_stay(other)

    def CallOnMonos_OTEn(self, other: ColliderBase):
        for go in self.__Storage.Loop("ocs"):
            go.on_trigger_enter(other)

    def CallOnMonos_OTEx(self, other: ColliderBase):
        for go in self.__Storage.Loop("ocs"):
            go.on_trigger_exit(other)

    def CallOnMonos_OTSt(self, other: ColliderBase):
        for go in self.__Storage.Loop("ocs"):
            go.on_trigger_stay(other)

    def CALL_PHYSICS_UPDATE(self):
        for mono in self.__Storage.Loop("fu"):
            mono.fixed_update()

    @property
    def rigid_body(self) -> RigidBody:
        return self.__rb

    @property
    def is_active(self) -> bool:
        return self.__is_active

    @is_active.setter
    def is_active(self, value: bool):
        if Info.is_loop_running:
            if value:
                Info.instance.AddToActiveGameObjects(self)
                self.CallOnMonos("on_enabled")
            else:
                Info.instance.RemFrActiveGameObjects(self)
                self.CallOnMonos("on_disabled")
            self.__is_active = value
        else:
            self.__activate_on_start = value

        if value:
            for child in self.__transform:
                child.gameobject.PARENT_ACTIVATED()
        else:
            for child in self.__transform:
                child.gameobject.PARENT_DEACTIVATED()

    def get_component(self, _t: type):
        self.__Storage.get_component(_t)

    def get_all_components(self, _t: type):
        return self.__Storage.get_all_components(_t)

    def add_component(self, _type: type) -> MonoBehaviour or RendererBaseAnot:
        if not issubclass(_type, MonoBehaviour) and not issubclass(_type, ColliderBase):
            raise InvalidComponentError(f"The given class ({_type}) doesn't inherit from MonoBehaviour")

        comp = _type(self)

        if _type is RigidBody:
            if self.__rb is not None:
                raise MultiRigidbodyError(f"Gamobject {self.name} already has a rigidbody")

            self.__rb = comp
            Info.instance.AddToRBs(comp)

        if not issubclass(_type, ColliderBase):
            self.__Storage.add_to_all(comp)
            if Info.has_been_runned: comp.OnGameStartMono()
        else:
            Info.instance.AddToActiveColliders(comp)
        return comp

    def destroy(self):
        if not self.__is_active: return
        Info.instance.RemFrGameObjects(self)
        self.__is_active = False
        for mono in self.__Storage.LoopAll():
            if not mono.enabled: continue
            mono.remove()
            mono.Call("on_destroy")
        del self

    def start_coroutine(self, iter: typing.Generator[WaitFor, None, None]):
        try:
            self.__Storage.add_cour(iter, iter.__next__())
        except StopIteration:
            pass


