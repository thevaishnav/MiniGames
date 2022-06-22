from __future__ import annotations
from MiniGames.Utils.type_checker import type_check, type_check_num, types_check
import typing
import pygame  # Only for rendering purposes
from MiniGames.Utils.settings_and_info import Settings
from MiniGames.Pipeline.camera import Camera
from MiniGames.Utils.vector2 import Vector2
from MiniGames.Pipeline.transform import __U2P__Point__

if typing.TYPE_CHECKING:
    from MiniGames.Renderers.shape_renderer import ShapeRenderer as ShapeRendAnot


class ShapeBase:
    def __init__(self, edge_size: int = 5):
        self.__edge_size = edge_size
        self._rend: ShapeRendAnot = None

    def _set_renderer(self, rend: ShapeRendAnot):
        self._rend = rend

    @property
    def edge_size(self) -> int:
        return self.__edge_size

    @edge_size.setter
    def edge_size(self, value: int):
        type_check("edge_size", value, int)
        self.__edge_size = value

    def _recalculate_pos(self): raise NotImplementedError()

    def _recalculate_scale(self): raise NotImplementedError()

    def _recalculate_rot(self): raise NotImplementedError()

    def _render(self): raise NotImplementedError()


class ShapeCircle(ShapeBase):
    def __init__(self, radius: float, edge_size: int = 5):
        super(ShapeCircle, self).__init__(edge_size)
        self.__radius = radius

        self.__raw_surf = None
        self.__surf = None
        self.__pCenter = None

    @property
    def radius(self) -> float:
        return self.__radius

    @radius.setter
    def radius(self, value: float):
        type_check_num("radius", value)
        self.__radius = value
        self._recalculate_scale()

    def _recalculate_pos(self):
        if self.__surf is None:
            self._recalculate_scale()
            return

        ppos = self._rend._absolute_center
        rc = self.__surf.get_rect().center
        self.__pCenter = Vector2(ppos.x - rc[0], ppos.y - rc[1])

    def _recalculate_rot(self):
        if self.__raw_surf is None:
            self._recalculate_scale()
            return
        self.__surf = pygame.transform.rotate(self.__raw_surf, self._rend._absolute_rotation)
        self._recalculate_pos()

    def _recalculate_scale(self):
        # Scale
        trans = self._rend.transform
        sc = self.__radius * trans.lossy_scale * Settings.space_scale
        rect = pygame.Rect((0, 0), (sc * 2).__call__())
        self.__raw_surf = pygame.surface.Surface(rect.size, pygame.SRCALPHA)

        pygame.draw.ellipse(surface=self.__raw_surf, color=self._rend.color, rect=rect, width=self.edge_size)
        self._recalculate_rot()

    def _render(self):
        if self.__surf is None: self._recalculate_scale()
        Camera.put(self.__surf, self.__pCenter)


class ShapeArrow(ShapeBase):
    def __init__(self, start_pt: Vector2, end_pt: Vector2, edge_size: int = 5):
        super(ShapeArrow, self).__init__(edge_size)
        self.__start_pt = start_pt
        self.__end_pt = end_pt
        self.__py_start = __U2P__Point__(self.__start_pt)
        self.__py_end = __U2P__Point__(self.__end_pt)
        self.__tri_points = self._gr_three_points()

    @property
    def start_point(self) -> Vector2:
        return self.__start_pt

    @start_point.setter
    def start_point(self, value: Vector2):
        types_check("start_point", value, Vector2)
        self.__start_pt = value
        self.__py_start = __U2P__Point__(self.__start_pt)
        self.__tri_points = self._gr_three_points()

    @property
    def end_point(self) -> Vector2:
        return self.__end_pt

    @end_point.setter
    def end_point(self, value: Vector2):
        types_check("end_point", value, Vector2)
        self.__end_pt = value
        self.__py_end = __U2P__Point__(self.__end_pt)
        self.__tri_points = self._gr_three_points()

    def _gr_three_points(self):
        p2 = (self.__start_pt - self.__end_pt) * 0.1
        p3 = p2.copy() + self.__end_pt
        p2.rotate_self(90)
        p2Fin = __U2P__Point__(p2 + p3)
        p3Fin = __U2P__Point__(p3 - p2)
        return self.__py_end, p2Fin, p3Fin

    def _recalculate_pos(self): pass

    def _recalculate_scale(self): pass

    def _recalculate_rot(self): pass

    def _render(self):
        Camera._draw_line(self.__py_start, self.__py_end, self._rend.color, self.edge_size)
        Camera._draw_polygon(self.__tri_points, self._rend.color, edge_size=0)


class ShapeBox(ShapeBase):
    def __init__(self, size: Vector2, edge_size: int = 5):
        super(ShapeBox, self).__init__(edge_size)
        self.__size = size
        self.__redii_tl = 1
        self.__redii_tr = 1
        self.__redii_bl = 1
        self.__redii_br = 1
        self.__surf = None
        self.__raw_surf = None
        self.__pyCent = Vector2.zero()

    def _recalculate_pos(self):
        if self.__surf is None:
            self._recalculate_scale()
            return

        r = self.__surf.get_rect().center
        c = self._rend._absolute_center
        self.__pyCent = Vector2(c.x - r[0], c.y - r[1])

    def _recalculate_rot(self):
        if self.__raw_surf is None:
            self._recalculate_scale()
            return

        self.__surf = pygame.transform.rotate(self.__raw_surf, self._rend._absolute_rotation)
        self._recalculate_pos()

    def _recalculate_scale(self):
        py_size = (self.__size * self._rend.transform.lossy_scale * Settings.space_scale).__call__()
        rect = pygame.Rect((0, 0), py_size)
        self.__raw_surf = pygame.surface.Surface(py_size, pygame.SRCALPHA)

        pygame.draw.rect(self.__raw_surf,
                         color=self._rend.color,
                         rect=rect,
                         width=self.edge_size,
                         border_top_left_radius=self.__redii_tl,
                         border_top_right_radius=self.__redii_tr,
                         border_bottom_right_radius=self.__redii_br,
                         border_bottom_left_radius=self.__redii_bl
                         )
        self._recalculate_rot()

    def _render(self):
        if self.__surf is None:
            self._recalculate_scale()
        Camera.put(self.__surf, self.__pyCent)

    @property
    def size(self) -> Vector2:
        return self.__size

    @size.setter
    def size(self, value: Vector2):
        types_check("size", value, Vector2)
        self.__size = value
        self._recalculate_scale()

    @property
    def redii_tl(self) -> int:
        return self.__redii_tl

    @redii_tl.setter
    def redii_tl(self, value: int):
        type_check("redii_tl", value, int)
        self.__redii_tl = value

    @property
    def redii_tr(self) -> int:
        return self.__redii_tr

    @redii_tr.setter
    def redii_tr(self, value: int):
        type_check("redii_tr", value, int)
        self.__redii_tr = value

    @property
    def redii_bl(self) -> int:
        return self.__redii_bl

    @redii_bl.setter
    def redii_bl(self, value: int):
        type_check("redii_bl", value, int)
        self.__redii_bl = value

    @property
    def redii_br(self) -> int:
        return self.__redii_br

    @redii_br.setter
    def redii_br(self, value: int):
        type_check("redii_br", value, int)
        self.__redii_br = value
