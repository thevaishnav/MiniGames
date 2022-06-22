from __future__ import annotations
from MiniGames.Utils.type_checker import type_check, types_check, type_check_num

from MiniGames.Utils.color import Color
from MiniGames.Utils import vector2 as mod_v2
from MiniGames.Pipeline import camera as mod_cam
from typing import TYPE_CHECKING
from MiniGames.Utils import decorators

if TYPE_CHECKING:
    from MiniGames.Utils.vector2 import Vector2 as Vector2Anot
    from MiniGames.Pipeline.application import Application as ApplicationAnot


class SettingsClass:
    @decorators.inner_method
    def __init__(self): pass
    @property
    def active_camera(self):
        return mod_cam.Camera.active()

    @property
    def background_color(self) -> Color:
        return __background_color__

    @background_color.setter
    def background_color(self, value: Color):
        types_check("background_color", value, Color)
        global __background_color__
        __background_color__ = value

    @property
    def grid_color(self) -> Color:
        return __grid_color__

    @grid_color.setter
    def grid_color(self, value: Color):
        types_check("grid_color", value, Color)
        global __grid_color__
        __grid_color__ = value

    @property
    def x_axis_color(self) -> Color:
        return __x_axis_color__

    @x_axis_color.setter
    def x_axis_color(self, value: Color):
        types_check("x_axis_color", value, Color)
        global __x_axis_color__
        __x_axis_color__ = value

    @property
    def y_axis_color(self) -> Color:
        return __y_axis_color__

    @y_axis_color.setter
    def y_axis_color(self, value: Color):
        types_check("y_axis_color", value, Color)
        global __y_axis_color__
        __y_axis_color__ = value

    @property
    def collision_threads_count(self) -> int:
        return __collision_threads__

    @collision_threads_count.setter
    def collision_threads_count(self, value: int):
        type_check("collision_threads_count", value, int)
        global __collision_threads__
        __collision_threads__ = value

    @property
    def half_screen_width(self):
        return __HSW__

    @half_screen_width.setter
    def half_screen_width(self, value: int):
        type_check("half_screen_width", value, int)
        if Info.instance is None: raise PermissionError("Cannot change screen size, once the game is running")
        global __HSW__
        __HSW__ = value

    @property
    def half_screen_height(self):
        return __HSH__

    @half_screen_height.setter
    def half_screen_height(self, value: float):
        type_check_num("half_screen_height", value)
        if Info.instance is None: raise PermissionError("Cannot change screen size, once the game is running")
        global __HSH__
        __HSH__ = value

    @property
    def screen_width(self):
        return __HSW__ * 2

    @screen_width.setter
    def screen_width(self, value: float):
        type_check_num("screen_width", value)
        if Info.instance is None: raise PermissionError("Cannot change screen size, once the game is running")
        global __HSW__
        __HSW__ = value / 2

    @property
    def screen_height(self):
        return __HSH__ * 2

    @screen_height.setter
    def screen_height(self, value: float):
        type_check_num("screen_height", value)
        if Info.instance is None: raise PermissionError("Cannot change screen size, once the game is running")
        global __HSH__
        __HSH__ = value / 2

    @property
    def screen_size_pixels(self):
        return mod_v2.Vector2(__HSW__ * 2, __HSH__ * 2)

    @screen_size_pixels.setter
    def screen_size_pixels(self, value: Vector2Anot):
        types_check("screen_size_pixels", value, mod_v2.Vector2)
        global __HSW__, __HSH__
        __HSW__, __HSH__ = int(value.x / 2), int(value.y / 2)

    @property
    def screen_size(self) -> Vector2Anot:
        return mod_v2.Vector2(__HSW__ * 2, __HSH__ * 2) / __space_scale__

    @screen_size.setter
    def screen_size(self, value: Vector2Anot):
        types_check("screen_size", value, Vector2Anot)
        self.screen_size_pixels = value * __space_scale__

    @property
    def half_screen_size(self):
        return mod_v2.Vector2(__HSW__, __HSH__)

    @half_screen_size.setter
    def half_screen_size(self, value: Vector2Anot):
        types_check("half_screen_size", value, Vector2Anot)
        if type(value) is not mod_v2.Vector2: raise ValueError(
            f"Invalid value type for Screen Size, expected 'Vector2' got \'{type(value).__qualname__}\'")
        global __HSW__, __HSH__
        __HSW__, __HSH__ = value.x / 2, value.y / 2

    @property
    def space_scale(self) -> Vector2Anot:
        return __space_scale__

    @space_scale.setter
    def space_scale(self, value: Vector2Anot):
        types_check("space_scale", value, mod_v2.Vector2)
        if Info.is_loop_running:
            raise PermissionError("Cannot change space scale while game is running")
        global __space_scale__
        __space_scale__ = value._fix_self()

    @property
    def draw_colliders(self) -> bool:
        return __draw_colliders__

    @draw_colliders.setter
    def draw_colliders(self, value: bool):
        type_check("draw_colliders", value, bool)
        global __draw_colliders__
        __draw_colliders__ = value

    @property
    def colliders_thickness(self) -> float:
        return __colliders_thickness__

    @colliders_thickness.setter
    def colliders_thickness(self, value: float):
        type_check_num("colliders_thickness", value)
        if Info.is_loop_running:
            raise PermissionError("Cannot change collider thickness while game is running")
        global __colliders_thickness__
        __colliders_thickness__ = value

    @property
    def colliders_color(self) -> Color:
        return __colliders_color__

    @colliders_color.setter
    def colliders_color(self, value: Color):
        types_check("colliders_color", value, Color)
        if Info.is_loop_running:
            raise PermissionError("Cannot change collider color while game is running")
        global __colliders_color__
        __colliders_color__ = value

    @property
    def gravity(self):
        return __gravity__

    @gravity.setter
    def gravity(self, value: Vector2Anot):
        types_check("gravity", value, mod_v2.Vector2)
        global __gravity__
        __gravity__ = value

    @property
    def frame_rate(self):
        return __frame_rate__

    @frame_rate.setter
    def frame_rate(self, value: int):
        type_check("frame_rate", value, int)
        global __frame_rate__
        __frame_rate__ = value

    @property
    def draw_grid(self) -> bool:
        return __draw_grid__

    @draw_grid.setter
    def draw_grid(self, value: bool):
        type_check("draw_grid", value, bool)
        global __draw_grid__
        __draw_grid__ = value


class InfoClass:
    @decorators.inner_method
    def __init__(self): pass

    @property
    def instance(self) -> ApplicationAnot: return __instance__

    @property
    def fixedDeltaTime(self) -> float: return __fixedDeltaTime__

    @property
    def deltaTime(self) -> float: return __deltaTime__

    @property
    def time(self) -> float: return __time__

    def _update_time(self):
        global __time__, __deltaTime__
        __time__ += __deltaTime__

    def has_been_init(self) -> bool: return __instance__ is not None

    @property
    def is_loop_running(self) -> bool:
        return __instance__ is not None and __instance__._Application__is_loop_running

    @property
    def has_been_runned(self) -> bool:
        return __instance__ is not None and __instance__._Application__has_been_runned


__gravity__ = mod_v2.Vector2(0, -9.8)
__frame_rate__ = 60
__HSW__ = 0  # HalfScreenWidth
__HSH__ = 0  # HalfScreenHeight
__space_scale__ = mod_v2.Vector2(100, 100)  # How many pixels equal one unit
__draw_grid__ = True
__collision_threads__ = 1
__draw_colliders__ = True
__colliders_color__ = Color.collider_green()
__colliders_thickness__ = 1
__grid_color__ = Color(43, 43, 43)
__x_axis_color__ = Color(83, 135, 62)
__y_axis_color__ = Color(135, 62, 80)
__background_color__ = Color(0, 0, 0)
__instance__ = None
__fixedDeltaTime__ = 0
__deltaTime__ = 0
__time__ = 0

decorators.__IS_HIDDEN__ = False
Settings = SettingsClass()
Info = InfoClass()
decorators.__IS_HIDDEN__ = True

"""
Info:
    __instance
    __fixedDeltaTime
    __deltaTime
    __time
    __screen
    
Settings:
    space_scale
    gravity
    half_screen_width
    half_screen_height
    screen_width
    screen_height
    
"""
