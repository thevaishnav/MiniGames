from MiniGames.Pipeline.application import resources_path
from MiniGames.Utils.exceptions import ResourceNotFoundError
import pygame
import os



class Sprite:
    def __init__(self):
        self.__surfs = None

    def get_width(self) -> float: return self.__surfs.get_width()

    def get_height(self) -> float: return self.__surfs.get_height()


class Resources:
    @staticmethod
    def get_sprite(nick_name: str) -> Sprite:
        nn = nick_name.lower()
        if nn in all_res: return all_res[nn]
        raise ResourceNotFoundError(f"Resource nicknamed {nick_name} not found. Did you load it?")

    @staticmethod
    def load_sprite(nick_name: str, path: str) -> Sprite:
        if not os.path.isfile(path): raise FileNotFoundError("Given path is not a file")

        sp = Sprite()
        sp._Sprite__surfs = pygame.image.load(path)
        all_res[nick_name.lower()] = sp
        return sp

all_res = dict()

Resources.load_sprite(nick_name="circle", path=os.path.join(resources_path(), "Circle.png"))
Resources.load_sprite(nick_name="square", path=os.path.join(resources_path(), "Square.png"))
