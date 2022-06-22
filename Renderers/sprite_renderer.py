from MiniGames.Utils.type_checker import type_check

from MiniGames.Utils.settings_and_info import Info
from MiniGames.Utils.vector2 import Vector2
from MiniGames.Utils.resources import Resources, Sprite
from MiniGames.Renderers.renderer_base import RendererBase
from MiniGames.Pipeline.camera import Camera
import pygame


class SpriteRenderer(RendererBase):
    def start(self):
        if not hasattr(self, "_SpriteRenderer__raw_surf"):
            self.__raw_surf = Resources.get_sprite("Circle")
        self.__surface = None
        self.__scaled_surface = None
        self.__pyCent = None

    @property
    def sprite(self) -> Sprite:
        return self.__raw_surf

    @sprite.setter
    def sprite(self, value: Sprite):
        type_check("sprite", value, Sprite)
        self.__raw_surf = value
        if Info.is_loop_running:
            self._recalculate_scale()

    def _recalculate_pos(self):
        if self.__surface is None:
            self._recalculate_scale()
            return

        pos = self.transform.global_pos_in_pixels
        cent = self.__surface.get_rect().center
        self.__pyCent = Vector2(pos.x - cent[0], pos.y - cent[1])

    def _recalculate_rot(self):
        if self.__scaled_surface is None:
            self._recalculate_scale()
            return

        self.__surface = pygame.transform.rotate(self.__scaled_surface, self.transform.rotation)
        self._recalculate_pos()

    def _recalculate_scale(self):
        scale = self.transform.lossy_scale
        new_size = (int(scale.x * self.__raw_surf.get_width()), int(scale.y * self.__raw_surf.get_height()))
        self.__scaled_surface = pygame.transform.scale(self.__raw_surf._Sprite__surfs, new_size)
        self._recalculate_rot()

    def _render(self):
        if self.__surface is None: self._recalculate_scale()
        Camera.put(self.__surface, self.__pyCent)
