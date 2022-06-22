from MiniGames.Utils.type_checker import type_check, types_check

from MiniGames.Utils.vector2 import Vector2
from MiniGames.Pipeline.transform import __U2P__Point__
from MiniGames.Pipeline.gameobject import GameObject
from MiniGames.Pipeline.camera import Camera
from MiniGames.Utils.color import Color
from MiniGames.Renderers.renderer_base import RendererBase
import pygame


class TextRenderer(RendererBase):
    def __init__(self, gameobject: GameObject):
        super(TextRenderer, self).__init__(gameobject)
        self.__text = "text"
        self.__fontName = "freesansbold.ttf"
        self.__fontSize = 15
        self.__pPos = None
        self.__background = Color.clear()
        self.__raw_surf = None
        self.__surf = None

    @property
    def text(self) -> str: return self.__text

    @text.setter
    def text(self, value: str):
        type_check("text", value, str)
        self.__text = value
        self._recalculate_scale()

    @property
    def fontName(self) -> str: return self.__fontName

    @fontName.setter
    def fontName(self, value: str):
        type_check("fontName", value, str)
        self.__fontName = value
        self._recalculate_scale()

    @property
    def fontSize(self) -> int:
        return self.__fontSize

    @fontSize.setter
    def fontSize(self, value: int):
        type_check("fontSize", value, int)
        self.__fontSize = value
        self._recalculate_scale()

    @property
    def background(self) -> Color:
        return self.__background

    @background.setter
    def background(self, value: Color):
        types_check("background", value, Color)
        self.__background = value

    def _recalculate_pos(self):
        if self.__surf is None:
            self._recalculate_rot()
            return

        rect = self.__surf.get_rect().center
        p = __U2P__Point__(self.transform.position)
        self.__pPos = Vector2(p.x - rect[0], p.y - rect[1])

    def _recalculate_rot(self):
        if self.__raw_surf is None:
            self._recalculate_scale()
            return

        self.__surf = pygame.transform.rotate(self.__raw_surf, -self.transform.rotation)
        self._recalculate_pos()

    def _recalculate_scale(self):
        font = pygame.font.Font(self.__fontName, self.__fontSize)
        surf = font.render(self.__text, True, self.color, (0, 0, 0, 0)).convert_alpha()
        rect = surf.get_rect()
        scale = self.transform.lossy_scale
        sx, sy = int(rect.width * scale.x), int(rect.height * scale.y)
        self.__raw_surf = pygame.transform.scale(surf, (sx, sy))
        self._recalculate_rot()

    def _render(self):
        if self.__surf is None: self._recalculate_scale()
        Camera.put(self.__surf, self.__pPos)
