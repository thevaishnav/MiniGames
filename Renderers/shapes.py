from __future__ import annotations
import typing
import pygame  # Only for rendering purposes
from MiniGames.Utils.settings_and_info import Settings
from MiniGames.Pipeline.camera import Camera
from MiniGames.Utils.vector2 import Vector2
from MiniGames.Pipeline.transform import __U2P__Point__

if typing.TYPE_CHECKING:
    from MiniGames.Renderers.shape_renderer import ShapeRenderer as ShapeRendAnot


class ShapeBase:
    def __init__(self, edge_size: int=5):
        self.__edge_size = edge_size
        self._rend: ShapeRendAnot = None

    def SET_RENDERER(self, rend: ShapeRendAnot):
        self._rend = rend

    @property
    def edge_size(self) -> int:
        return self.__edge_size

    @edge_size.setter
    def edge_size(self, value: int):
        self.__edge_size = value

    def Initialize(self): raise NotImplementedError()

    def RecalculatePos(self): raise NotImplementedError()

    def RecalculateScale(self): raise NotImplementedError()

    def RecalculateRot(self): raise NotImplementedError()

    def Render(self): raise NotImplementedError()


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
        self.__radius = value
        self.RecalculateScale()

    def RecalculatePos(self):
        if self.__surf is None:
            self.RecalculateScale()
            return

        ppos = self._rend.ABS_CENT
        rc = self.__surf.get_rect().center
        self.__pCenter = Vector2(ppos.x - rc[0], ppos.y - rc[1])

    def RecalculateRot(self):
        if self.__raw_surf is None:
            self.RecalculateScale()
            return
        self.__surf = pygame.transform.rotate(self.__raw_surf, self._rend.ABS_ROT)
        self.RecalculatePos()

    def RecalculateScale(self):
        # Scale
        trans = self._rend.transform
        sc = self.__radius * trans.lossy_scale * Settings.space_scale
        rect = pygame.Rect((0, 0), (sc * 2).__call__())
        self.__raw_surf = pygame.surface.Surface(rect.size, pygame.SRCALPHA)

        pygame.draw.ellipse(surface=self.__raw_surf, color=self._rend.color, rect=rect, width=self.edge_size)
        self.RecalculateRot()

    def Render(self):
        if self.__surf is None: self.RecalculateScale()
        Camera.put(self.__surf, self.__pCenter)


class ShapeArrow(ShapeBase):
    def __init__(self, start_pt: Vector2, end_pt: Vector2, edge_size: int = 5):
        super(ShapeArrow, self).__init__(edge_size)
        self.__start_pt = start_pt
        self.__end_pt = end_pt
        self.__py_start = __U2P__Point__(self.__start_pt)
        self.__py_end = __U2P__Point__(self.__end_pt)
        self.__tri_points = self.GET_TRI_POINTS()

    @property
    def start_point(self) -> Vector2:
        return self.__start_pt

    @start_point.setter
    def start_point(self, value: Vector2):
        self.__start_pt = value
        self.__py_start = __U2P__Point__(self.__start_pt)
        self.__tri_points = self.GET_TRI_POINTS()

    @property
    def end_point(self) -> Vector2:
        return self.__end_pt

    @end_point.setter
    def end_point(self, value: Vector2):
        self.__end_pt = value
        self.__py_end = __U2P__Point__(self.__end_pt)
        self.__tri_points = self.GET_TRI_POINTS()

    def GET_TRI_POINTS(self):
        p2 = (self.__start_pt - self.__end_pt) * 0.1
        p3 = p2.copy() + self.__end_pt
        p2.rotate_self(90)
        p2Fin = __U2P__Point__(p2 + p3)
        p3Fin = __U2P__Point__(p3 - p2)
        return self.__py_end, p2Fin, p3Fin

    def RecalculateSelf(self): pass

    def RecalculatePos(self): pass

    def RecalculateScale(self): pass

    def RecalculateRot(self): pass

    def Render(self):
        Camera.draw_line(self.__py_start, self.__py_end, self._rend.color, self.edge_size)
        Camera.draw_polygon(self.__tri_points, self._rend.color, edge_size=0)


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

    def RecalculatePos(self):
        if self.__surf is None:
            self.RecalculateScale()
            return

        r = self.__surf.get_rect().center
        c = self._rend.ABS_CENT
        self.__pyCent = Vector2(c.x - r[0], c.y - r[1])

    def RecalculateRot(self):
        if self.__raw_surf is None:
            self.RecalculateScale()
            return

        self.__surf = pygame.transform.rotate(self.__raw_surf, self._rend.ABS_ROT)
        self.RecalculatePos()

    def RecalculateScale(self):
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
        self.RecalculateRot()

    def Render(self):
        if self.__surf is None:
            self.RecalculateScale()
        Camera.put(self.__surf, self.__pyCent)

    @property
    def size(self) -> Vector2:
        return self.__size

    @size.setter
    def size(self, value: Vector2):
        self.__size = value
        self.RecalculateScale()

    @property
    def redii_tl(self) -> int:
        return self.__redii_tl

    @redii_tl.setter
    def redii_tl(self, value: int):
        self.__redii_tl = value

    @property
    def redii_tr(self) -> int:
        return self.__redii_tr

    @redii_tr.setter
    def redii_tr(self, value: int):
        self.__redii_tr = value

    @property
    def redii_bl(self) -> int:
        return self.__redii_bl

    @redii_bl.setter
    def redii_bl(self, value: int):
        self.__redii_bl = value

    @property
    def redii_br(self) -> int:
        return self.__redii_br

    @redii_br.setter
    def redii_br(self, value: int):
        self.__redii_br = value
