from __future__ import annotations
import MiniGames.Utils.settings_and_info as others
from MiniGames.Utils.vector2 import Vector2
from MiniGames.Utils.input import Input
from MiniGames.Physics.physics_system import PhysicsSystem
from MiniGames.Pipeline.camera import Camera
from MiniGames.Pipeline.storages import AppStorage
from MiniGames.Utils import decorators
import os
import time
import os.path as path
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from MiniGames.Physics.rigidbody import RigidBody
    from MiniGames.Pipeline.gameobject import GameObject


class Application:
    @decorators.inner_method
    def __init__(self):
        print("Starting Game", end=" - ")

        if others.Info.has_been_init():
            print("Application is already running")
            return

        others.__instance__ = self
        self.__has_been_runned = False  # look at self.run func to know difference
        self.__is_loop_running = False  # between __has_been_runned and __is_loop_running
        self.__camera = Camera(Vector2.zero())

        self.__Storage = AppStorage()
        self.__phy_sym = PhysicsSystem()
        print("Done")

    def run(self):
        if not others.Info.has_been_init():
            raise BrokenPipeError("Too early to run. Must call \"App.init\" first")

        self.__has_been_runned = True

        for go in self.__Storage.loop_gos():
            go._on_go_start()

        for go in self.__Storage.loop_gos():
            go._call_on_monos("start")

        try:
            self.__is_loop_running = True
            # self.__phy_sym.start_physics_loop()
            self._render_loop()
        except KeyboardInterrupt:
            stop_game()

    def _call_physics_update(self):
        for go in self.__Storage.loop_gos():
            go._call_physics_update()

    def _render_loop(self):
        while self.__is_loop_running:
            now = time.perf_counter()
            Input._in_update()
            if Input.SHOULD_QUIT:
                stop_game()
                break

            others.Info._update_time()
            self.__camera.clear_screen()

            for go in self.__Storage.loop_gos():
                go._go_update()

            self.__camera.update()
            Camera._wait_in_frame()
            others.__deltaTime__ = time.perf_counter() - now

        for go in self.__Storage.loop_gos():
            go.destroy()

    def _add_to_active_game_objects(self, go: GameObject):
        self.__Storage.add_to_gos(go)

    def _rem_from_active_game_objects(self, go: GameObject):
        self.__Storage.rem_from_gos(go)

    def _add_to_rbs(self, rb: RigidBody):
        self.__phy_sym.add_rb(rb)

    def _rem_from_rbs(self, rb: RigidBody):
        self.__phy_sym.rem_rb(rb)

    def _add_to_active_colliders(self, go: GameObject):
        self.__phy_sym.add_col(go)

    def _rem_from_active_colliders(self, go: GameObject):
        self.__phy_sym.rem_col(go)


def init():
    decorators.__IS_HIDDEN__ = False
    app = Application()
    decorators.__IS_HIDDEN__ = True
    return app


def run():
    if others.Info.instance is None: raise BrokenPipeError("Too early to run. Must call \"App.init\" first")
    others.Info.instance.run()


def resources_path():
    return path.join(path.dirname(path.dirname(path.realpath(__file__))), "Resources")


def assets_path(): return path.join(os.getcwd(), "Assets")


def stop_game():
    if others.Info.instance is None: return
    others.Info.instance._Application__is_loop_running = False
