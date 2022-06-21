from __future__ import annotations
import collections
import math
import typing
from MiniGames.Utils.exceptions import InvalidHierarchyError
from MiniGames.Utils.settings_and_info import Settings
from MiniGames.Utils.vector2 import Vector2
from MiniGames.Pipeline.monobehaviour import MonoBehaviour

if typing.TYPE_CHECKING:
    from MiniGames.Pipeline.gameobject import GameObject as GameObjectAnot


class Transform(MonoBehaviour):
    def __init__(self, gameobject: GameObjectAnot):
        super().__init__(gameobject)
        self.__loc_uPos = Vector2().FIX_SELF()
        self.__loc_pPos = __U2P__Point__(self.__loc_uPos).FIX_SELF()
        self.__loc_sca = Vector2(1, 1).FIX_SELF()
        self.__loc_rot = 0
        self.__on_pos_changed: list[typing.Callable[[], None]] = []
        self.__on_sca_changed: list[typing.Callable[[], None]] = []
        self.__on_rot_changed: list[typing.Callable[[], None]] = []

        self.__parent: Transform = None
        self.__children: list[Transform] = []

    def __iter__(self) -> collections.Iterable[Transform]:
        for i in self.__children:
            yield i

    def __str__(self):
        return f"Transform(pos: {self.__loc_uPos}, scale: {self.__loc_sca}, rot: {self.__loc_rot})"

    def ADD_TO_ON_POS_CHANGE(self, func: typing.Callable[[], None]):
        self.__on_pos_changed.append(func)

    def ADD_TO_ON_SCA_CHANGE(self, func: typing.Callable[[], None]):
        self.__on_sca_changed.append(func)

    def ADD_TO_ON_ROT_CHANGE(self, func: typing.Callable[[], None]):
        self.__on_rot_changed.append(func)

    def CALL_POS_CHANGE(self):
        for func in self.__on_pos_changed:
            func()

        for trans in self.__children:
            trans.CALL_POS_CHANGE()

    def CALL_SCA_CHANGE(self):
        for func in self.__on_sca_changed:
            func()

        for trans in self.__children:
            trans.CALL_SCA_CHANGE()

    def CALL_ROT_CHANGE(self):
        for func in self.__on_rot_changed:
            func()

        for trans in self.__children:
            trans.CALL_ROT_CHANGE()

    def IsItParentOrSuperParent(self, trans: Transform):
        if self.__parent is None: return False
        if trans == self.__parent: return True
        return self.__parent.IsItParentOrSuperParent(trans)

    def AddChild(self, child: Transform):
        if child not in self.__children:
            self.__children.append(child)

    def RemoveChild(self, child: Transform):
        if child in self.__children:
            self.__children.remove(child)

    def Enable(self):
        pass

    def Disable(self):
        pass

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, trans: Transform or None):
        if trans == self: raise InvalidHierarchyError("Transform can't be parent of itself")

        global_pos = self.position
        global_sca = self.lossy_scale
        global_rot = self.rotation
        if self.__parent is not None:
            self.__parent.RemoveChild(self)

        if trans is None:
            self.__parent = trans
            self.local_rotation = global_rot
            self.local_scale = global_sca
            self.local_position = global_pos
            return

        if trans.IsItParentOrSuperParent(self):
            raise InvalidHierarchyError(
                f"{trans.gameobject.name} can't be parent of {self.gameobject.name}, because, its a child (or sub-child)")
        self.__parent = trans
        self.rotation = global_rot
        self.local_scale = global_sca / self.parent.lossy_scale
        self.position = global_pos
        trans.AddChild(self)

    def remove(self):
        raise PermissionError(
            "Cannot remove component Transform. If you want to destroy gameobject, then call \"gameobject.destroy\"")

    @property
    def enabled(self) -> bool:
        return True

    @enabled.setter
    def enabled(self, value: bool):
        raise PermissionError("Cannot enable or disable Transform.")

    @property
    def global_pos_in_pixels(self) -> Vector2:
        return __U2P__Point__(self.position)

    @property
    def position(self) -> Vector2:
        if self.__parent is None: return self.__loc_uPos
        return (self.__loc_uPos * self.__parent.lossy_scale).rotate(self.parent.rotation) + self.__parent.position

    @position.setter
    def position(self, value: Vector2):
        if self.__parent is None:
            self.local_position = value
            return

        loc_uPos = value - self.__parent.position
        loc_uPos.rotate_self(-self.__parent.rotation)
        new_pos = loc_uPos / self.__parent.lossy_scale
        if new_pos != self.__loc_uPos:
            self.__loc_uPos = new_pos.FIX_SELF()
            self.CALL_POS_CHANGE()

    @property
    def rotation(self) -> float:
        if self.__parent is None: return self.__loc_rot
        return self.__parent.rotation + self.__loc_rot

    @rotation.setter
    def rotation(self, value: float):
        if self.__parent is None:
            self.local_rotation = value
            return

        r = value - self.__parent.rotation
        if self.__loc_rot != r:
            self.__loc_rot = r
            self.CALL_ROT_CHANGE()

    @property
    def lossy_scale(self) -> Vector2:
        if self.__parent is None: return self.__loc_sca
        theta = math.radians(self.__loc_rot)
        c2 = math.pow(math.cos(theta), 2)
        s2 = 1 - c2
        pScale = self.__parent.lossy_scale
        x, y = pScale.x, pScale.y
        v = Vector2(x * c2 + y * s2, x * s2 + y * c2)
        return v * self.__loc_sca

    @lossy_scale.setter
    def lossy_scale(self, value: Vector2):
        if self.__parent is None:
            self.local_scale = value
            return

        theta = math.radians(self.__loc_rot)
        c2 = math.pow(math.cos(theta), 2)
        s2 = 1 - c2
        pScale = self.__parent.lossy_scale
        x, y = pScale.x, pScale.y
        v = Vector2(x * c2 + y * s2, x * s2 + y * c2)
        new_val = value / v
        if new_val != self.__loc_sca:
            self.__loc_sca.FIX_SELF()
            self.CALL_SCA_CHANGE()

    @property
    def local_position(self) -> Vector2:
        return self.__loc_uPos

    @local_position.setter
    def local_position(self, value: Vector2):
        if self.__loc_uPos == value: return

        self.__loc_uPos = value.FIX_SELF()
        self.__loc_pPos = __U2P__Point__(value).FIX_SELF()
        self.CALL_POS_CHANGE()

    @property
    def local_scale(self) -> Vector2:
        return self.__loc_sca

    @local_scale.setter
    def local_scale(self, value: Vector2):
        if self.__loc_sca == value: return
        self.__loc_sca = value.FIX_SELF()
        self.CALL_SCA_CHANGE()

    @property
    def local_rotation(self) -> float:
        return self.__loc_rot

    @local_rotation.setter
    def local_rotation(self, value: float):
        if self.__loc_rot == value: return
        self.__loc_rot = value
        self.CALL_ROT_CHANGE()


def __U2P__Point__(uPoint: Vector2) -> Vector2:
    return Vector2(x=uPoint.x * Settings.space_scale.x + Settings.half_screen_width,
                   y=-uPoint.y * Settings.space_scale.y + Settings.half_screen_height)


def __P2U__Point__(pPoint: Vector2) -> Vector2:
    return Vector2((pPoint.x - Settings.half_screen_width) / Settings.space_scale.x,
                   (pPoint.y - Settings.half_screen_height) / -Settings.space_scale.y)
