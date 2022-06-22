import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"

from MiniGames.Utils.color import Color
from MiniGames.Utils.input import Input, Keycodes
from MiniGames.Pipeline.coroutines import WaitFor, WaitForEndOfFrame, WaitForSeconds, WaitForEndOfFrames, WaitWhileFalse, WaitWhileTrue
from MiniGames.Pipeline.gameobject import GameObject
from MiniGames.Utils.settings_and_info import Settings, Info
from MiniGames.Utils.vector2 import Vector2
from MiniGames.Physics.collider_base import ColliderBase
from MiniGames.Pipeline.monobehaviour import MonoBehaviour
from MiniGames.Physics.rigidbody import RigidBody
from MiniGames.Renderers.shapes import ShapeCircle, ShapeArrow, ShapeBox, ShapeBase
from MiniGames.Physics.box_collider import BoxCollider
from MiniGames.Physics.circle_collider import CircleCollider
from MiniGames.Utils.resources import Resources
from MiniGames.Renderers.line_renderer import LineRenderer
from MiniGames.Renderers.point_renderer import PointRenderer
from MiniGames.Renderers.shape_renderer import ShapeRenderer
from MiniGames.Renderers.sprite_renderer import SpriteRenderer
from MiniGames.Renderers.text_renderer import TextRenderer
import MiniGames.Pipeline.application as App

print("Welcome to MiniGames Game Engine.")
print("A project by Vaishnav Chincholkar (https://www.linkedin.com/in/vaishnav-chincholkar/)")
