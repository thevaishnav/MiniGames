from __future__ import annotations
import typing
import pygame  # Only for rendering purposes

from MiniGames.Utils import settings_and_info as mod_sai
from MiniGames.Utils import vector2 as mod_vec

if typing.TYPE_CHECKING:
    from MiniGames.Utils.vector2 import Vector2 as VectorAn
    from MiniGames.Utils.color import Color


class Camera:
    __active: Camera = None

    def __init__(self, pos: VectorAn):
        Camera.__active = self
        self.__pos = pos.FIX_SELF()
        self.__pyPos = pos * mod_sai.Settings.space_scale
        pygame.init()
        self.__screen = pygame.display.set_mode([mod_sai.Settings.screen_width, mod_sai.Settings.screen_height])
        self.__clock = pygame.time.Clock()
        self.update = pygame.display.flip

    @staticmethod
    def WAIT_IN_FRAME():
        Camera.__active.__clock.tick(mod_sai.Settings.frame_rate)

    @staticmethod
    def active() -> Camera:
        return Camera.__active

    @property
    def position(self) -> VectorAn:
        return self.__pos

    @position.setter
    def position(self, value: VectorAn):
        self.__pos = value.FIX_SELF()
        self.__pyPos = (value * mod_sai.Settings.space_scale * mod_vec.Vector2(1, -1)).FIX_SELF()

    @staticmethod
    def screen_size() -> tuple[int, int]:
        return Camera.__active.__screen.get_size()

    @staticmethod
    def put(obj, pos: VectorAn):
        Camera.__active.__screen.blit(obj, Camera.trans_point(pos))

    @staticmethod
    def trans_point(point: VectorAn) -> tuple[float, float]:
        return point.x - Camera.__active.__pyPos.x, point.y - Camera.__active.__pyPos.y

    @staticmethod
    def draw_line(start_point: VectorAn, end_point: VectorAn, color: Color, width: int = 4):
        pygame.draw.line(surface=Camera.__active.__screen,
                         color=color,
                         start_pos=Camera.trans_point(start_point),
                         end_pos=Camera.trans_point(end_point),
                         width=width)

    @staticmethod
    def draw_point(position: VectorAn, color: Color):
        pygame.draw.circle(Camera.__active.__screen, color=color, center=Camera.trans_point(position), radius=5)

    @staticmethod
    def draw_polygon(points: typing.Iterable[VectorAn], color: Color, edge_size: int = 4):
        pts = [Camera.trans_point(pts) for pts in points]
        pygame.draw.polygon(Camera.__active.__screen, color, pts, edge_size)

    def DRAW_GRID(self):
        if not mod_sai.__draw_grid__:
            return
        scree_size = mod_sai.Settings.screen_size_pixels
        space_scale = mod_sai.Settings.space_scale

        # off = self.__pyPos.x % space_scale

        stco = scree_size // space_scale
        stco.scale_self(0.5)
        enco = scree_size

        ss = self.__pyPos % space_scale

        for x_pos in range(int(stco.x - ss.x), int(enco.x - ss.x), space_scale.x_int):
            pygame.draw.line(self.__screen, mod_sai.__grid_color__, (x_pos, 0), (x_pos, scree_size.y), width=1)

        for y_pos in range(int(stco.y - ss.y), int(enco.y - ss.y), space_scale.y_int):
            pygame.draw.line(self.__screen, mod_sai.__grid_color__, (0, y_pos), (scree_size.x, y_pos), width=1)

        half_screen = (scree_size / 2) - self.__pyPos
        x, y = int(half_screen.x) - 1, int(half_screen.y) + 1
        pygame.draw.line(self.__screen, mod_sai.__y_axis_color__, (x, 0), (x, scree_size.y), width=3)
        pygame.draw.line(self.__screen, mod_sai.__x_axis_color__, (0, y), (scree_size.x, y), width=3)

    def clear_screen(self):
        self.__screen.fill(mod_sai.__background_color__)
        self.DRAW_GRID()
