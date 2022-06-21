import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"

import MiniGames.Pipeline.application as App
from MiniGames.Physics.rigidbody import RigidBody
from MiniGames.Pipeline.gameobject import GameObject
from MiniGames.Pipeline.monobehaviour import MonoBehaviour
from MiniGames.Renderers.sprite_renderer import SpriteRenderer
from MiniGames.Renderers.shape_renderer import ShapeRenderer
from MiniGames.Renderers.shapes import ShapeCircle, ShapeArrow, ShapeBox, ShapeBase
from MiniGames.Renderers.line_renderer import LineRenderer
from MiniGames.Renderers.text_renderer import TextRenderer
from MiniGames.Renderers.point_renderer import PointRenderer
from MiniGames.Utils.settings_and_info import Settings, Info
from MiniGames.Utils.vector2 import Vector2
from MiniGames.Utils.input import Input, Keycodes
from MiniGames.Utils.resources import Resources
from MiniGames.Utils.color import Color
from MiniGames.Physics.circle_collider import CircleCollider
from MiniGames.Physics.box_collider import BoxCollider

print("Welcome to MiniGames Game Engine.")
print("A project by Vaishnav Chincholkar (https://www.linkedin.com/in/vaishnav-chincholkar/)")
