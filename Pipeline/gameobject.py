from __future__ import annotations
from MiniGames.Utils.type_checker import type_check
from MiniGames.Utils import decorators
from MiniGames.Pipeline import monobehaviour as mod_mono
from MiniGames.Pipeline.transform import Transform
from MiniGames.Pipeline.coroutines import WaitFor
from MiniGames.Pipeline.storages import GameObjectsStorage
from MiniGames.Physics.collider_base import ColliderBase
from MiniGames.Physics.rigidbody import RigidBody
from MiniGames.Utils.settings_and_info import Info, Settings
from MiniGames.Utils.exceptions import InvalidComponentException
from MiniGames.Utils.exceptions import MultiRigidbodyException
from MiniGames.Utils import decorators

import typing
if typing.TYPE_CHECKING:
    from MiniGames.Renderers.renderer_base import RendererBaseAnot
    from MiniGames.Pipeline.monobehaviour import MonoBehaviour as MonoAnot


class GameObject:
    def __init__(self, name: str):
        type_check("name", name, str)
        if not Info.has_been_init():
            raise BrokenPipeError("Too early to create a Game Object. Must call \"App.init\" first")
        self.__rb = None
        self.name = name
        self.__transform = Transform(self)
        self.__is_active = False
        self.__activate_on_start = True
        decorators.__IS_HIDDEN__ = False
        self.__Storage = GameObjectsStorage()
        decorators.__IS_HIDDEN__ = True
        self.__activate_when_parent_does = True
        Info.instance._add_to_active_game_objects(self)
        if Info.is_loop_running:
            self._on_go_start()

    @property
    def gameobject(self) -> GameObject:
        return self

    @property
    def transform(self) -> Transform:
        return self.__transform

    def _on_go_start(self):
        if not self.__activate_on_start: return

        for mono in self.__Storage.loop_all():
            mono._on_game_start_mono()
        self.__is_active = True

    def _set_rb(self, rb: RigidBody):
        if self.__rb is not None: return False
        self.__rb = rb
        return True

    def _set_to(self, code: str, mono: MonoAnot or ColliderBase or RendererBaseAnot):
        self.__Storage.add_to(code, mono)

    def _remove_from(self, code: str, mono: MonoAnot):
        self.__Storage.rem_from(code, mono)

    def _add_to_multiple(self, mono: MonoAnot, *codes):
        for code in codes:
            self.__Storage.add_to(code, mono)

    def _remove_from_multiple(self, mono: MonoAnot, *codes):
        for code in codes:
            self.__Storage.rem_from(code, mono)

    def _parent_activated(self):
        self.__is_active = self.__activate_when_parent_does
        self._call_on_monos("on_enabled")
        for child in self.__transform:
            child.gameobject._parent_activated()

    def _parent_deactivated(self):
        self.__activate_when_parent_does = bool(self.__is_active)
        self.__is_active = False
        self._call_on_monos("on_disabled")
        for child in self.__transform:
            child.gameobject._parent_activated()

    def _go_update(self):
        for mono in self.__Storage.loop("u"): mono.update()
        for mono in self.__Storage.loop("lu"): mono.late_update()
        for rend in self.__Storage.loop("r"): rend._render()
        self.__Storage.handle_courotines()
        if not Settings.draw_colliders: return

        for rend in self.__Storage.loop("hidden_rend"):
            rend._render()

    def _call_on_monos(self, to_call: str):
        if not self.__is_active: return
        for mono in self.__Storage.loop_all():
            mono._call(to_call)

    def _call_on_monos_on_col_enter(self, other: ColliderBase):
        for go in self.__Storage.loop("oci"):
            go.on_collision_enter(other)

    def _call_on_monos_on_col_exit(self, other: ColliderBase):
        for go in self.__Storage.loop("oco"):
            go.on_collision_exit(other)

    def _call_on_monos_on_col_stay(self, other: ColliderBase):
        for go in self.__Storage.loop("ocs"):
            go.on_collision_stay(other)

    def _call_on_monos_on_tri_enter(self, other: ColliderBase):
        for go in self.__Storage.loop("ocs"):
            go.on_trigger_enter(other)

    def _call_on_monos_on_tri_exit(self, other: ColliderBase):
        for go in self.__Storage.loop("ocs"):
            go.on_trigger_exit(other)

    def _call_on_monos_on_tri_stay(self, other: ColliderBase):
        for go in self.__Storage.loop("ocs"):
            go.on_trigger_stay(other)

    def _call_physics_update(self):
        for mono in self.__Storage.loop("fu"):
            mono.fixed_update()

    @property
    def rigid_body(self) -> RigidBody:
        return self.__rb

    @property
    def is_active(self) -> bool:
        return self.__is_active

    @is_active.setter
    def is_active(self, value: bool):
        type_check("is_active", value, bool)
        if Info.is_loop_running:
            if value:
                Info.instance._add_to_active_game_objects(self)
                self._call_on_monos("on_enabled")
            else:
                Info.instance._rem_from_active_game_objects(self)
                self._call_on_monos("on_disabled")
            self.__is_active = value
        else:
            self.__activate_on_start = value

        if value:
            for child in self.__transform:
                child.gameobject._parent_activated()
        else:
            for child in self.__transform:
                child.gameobject._parent_deactivated()

    def get_component(self, _t: type):
        self.__Storage.get_component(_t)

    def get_all_components(self, _t: type):
        return self.__Storage.get_all_components(_t)

    def add_component(self, _type: type) -> MonoAnot or RendererBaseAnot:
        if not issubclass(_type, mod_mono.MonoBehaviour) and not issubclass(_type, ColliderBase):
            raise InvalidComponentException(f"The given class ({_type}) doesn't inherit from MonoBehaviour")

        decorators.__IS_HIDDEN__ = False
        comp = _type(self)
        decorators.__IS_HIDDEN__ = True

        if _type is RigidBody:
            if self.__rb is not None:
                raise MultiRigidbodyException(f"Gamobject {self.name} already has a rigidbody")

            self.__rb = comp
            Info.instance._add_to_rbs(comp)

        if not issubclass(_type, ColliderBase):
            self.__Storage.add_to_all(comp)
            if Info.has_been_runned: comp._on_game_start_mono()
        else:
            Info.instance._add_to_active_colliders(comp)
        return comp

    def destroy(self):
        if not self.__is_active: return
        Info.instance.RemFrGameObjects(self)
        self.__is_active = False
        for mono in self.__Storage.loop_all():
            if not mono.enabled: continue
            mono.remove()
            mono._call("on_destroy")
        del self

    def start_coroutine(self, iter: typing.Generator[WaitFor, None, None]):
        try:
            self.__Storage.add_cour(iter, iter.__next__())
        except StopIteration:
            pass


