from __future__ import annotations
from MiniGames.Physics.gjk_implementation import are_colliding
from MiniGames.Utils.settings_and_info import Info, Settings
from MiniGames.Utils import settings_and_info as others
from MiniGames.Utils.decorators import inner_method
import threading
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from MiniGames.Physics.rigidbody import RigidBody as RigidBodyAnot
    from MiniGames.Physics.collider_base import ColliderBase as ColliderBaseAnot


class PhysicsSystem:
    @inner_method
    def __init__(self):
        self._rbs: list[RigidBodyAnot] = []
        self._cols: list[ColliderBaseAnot] = []

        self._to_add_col: list[ColliderBaseAnot] = []
        self._to_rem_col: list[ColliderBaseAnot] = []
        self._looping_col = False

        self._to_add_rbs: list[RigidBodyAnot] = []
        self._to_rem_rbs: list[RigidBodyAnot] = []
        self._looping_rbs = False

        self.col_start: set[int] = set()
        self.col_stay: set[int] = set()

        self.__col_iter = None

        self.__is_psy_loop_running = False

    def add_rb(self, obj: RigidBodyAnot):
        if not self.__is_psy_loop_running:
            self._rbs.append(obj)
            self.start_physics_loop()
            return

        if not self._looping_rbs:
            if obj not in self._rbs:
                self._rbs.append(obj)
        else:
            if obj not in self._rbs and obj not in self._to_add_rbs:
                self._to_add_rbs.append(obj)

    def rem_rb(self, obj: RigidBodyAnot):
        if not self._looping_rbs:
            if obj in self._rbs:
                self._rbs.remove(obj)
        else:
            if obj in self._rbs or obj in self._to_add_rbs and obj not in self._to_rem_rbs:
                self._to_rem_rbs.append(obj)

    def add_col(self, obj):
        if not self.__is_psy_loop_running:
            self._cols.append(obj)
            self.physics_loop()
            return

        if not self._looping_col:
            if obj not in self._cols:
                self._cols.append(obj)
        else:
            if obj not in self._cols and obj not in self._to_add_col:
                self._to_add_col.append(obj)

    def rem_col(self, obj):
        if not self._looping_col:
            if obj in self._cols:
                self._cols.remove(obj)
        else:
            if obj in self._cols or obj in self._to_add_col and obj not in self._to_rem_rbs:
                self._to_rem_col.append(obj)

    def __remove_colliders(self):
        if not self._to_rem_col: return

        for r in self._to_rem_col:
            self._cols.remove(r)
        self._to_rem_col.clear()

    def loop_colliders(self):
        self._looping_col = True
        col_len = len(self._cols)
        for i in range(col_len - 1):
            for j in range(i + 1, col_len):
                yield self._cols[i], self._cols[j]

        if not self._to_add_col:
            self.__remove_colliders()
            return

        while self._to_add_col:
            new_loop = list(self._to_add_col)
            self._to_add_col.clear()

            for i in self._cols:
                for j in new_loop:
                    yield i, j

            col_len = len(new_loop)
            for i in range(col_len - 1):
                coli = new_loop[i]
                self._cols.append(coli)
                for j in range(i + 1, col_len):
                    yield coli, new_loop[j]
            self._cols.append(new_loop[-1])

        self.__remove_colliders()
        self._looping_col = False

    def loop_rbs(self):
        self._looping_rbs = True
        for r in self._rbs:
            yield r
        self._looping_rbs = False

    def get_collision_id(self, col1: ColliderBaseAnot, col2: ColliderBaseAnot):
        return (1 << col1._col_id) | (1 << col2._col_id)

    def collide_rbs(self, col1: ColliderBaseAnot, col2: ColliderBaseAnot):
        r1 = col1.gameobject.rigid_body
        r2 = col2.gameobject.rigid_body
        if r1 and r2: r1._collide_with(r2)

    def process_collision(self, col1: ColliderBaseAnot, col2: ColliderBaseAnot):
        cid = self.get_collision_id(col1, col2)

        if cid in self.col_start or cid in self.col_stay:
            self.col_stay.add(cid)
            self.col_start.discard(cid)
            if col1.is_trigger or col2.is_trigger:
                col1.gameobject._call_on_monos_on_tri_stay(col2)
                col2.gameobject._call_on_monos_on_tri_stay(col1)
            else:
                self.collide_rbs(col1, col2)
                col1.gameobject._call_on_monos_on_col_stay(col2)
                col2.gameobject._call_on_monos_on_col_stay(col1)
        else:
            self.col_start.add(cid)
            if col1.is_trigger or col2.is_trigger:
                col1.gameobject._call_on_monos_on_tri_enter(col2)
                col2.gameobject._call_on_monos_on_tri_enter(col1)
            else:
                self.collide_rbs(col1, col2)
                col1.gameobject._call_on_monos_on_col_enter(col2)
                col2.gameobject._call_on_monos_on_col_enter(col1)

    def process_collision_2(self, col1: ColliderBaseAnot, col2: ColliderBaseAnot):
        cid = self.get_collision_id(col1, col2)
        if cid not in self.col_stay: return

        self.col_stay.remove(cid)
        if col1.is_trigger or col2.is_trigger:
            col1.gameobject._call_on_monos_on_tri_exit(col2)
            col2.gameobject._call_on_monos_on_tri_exit(col1)
        else:
            col1.gameobject._call_on_monos_on_col_exit(col2)
            col2.gameobject._call_on_monos_on_col_exit(col1)

    def start_physics_loop(self):
        if not self._rbs and not self._cols:
            self.__is_psy_loop_running = False
            return

        if Settings.collision_threads_count == 1:
            self.__collision_det_func = self.single_thread_col_det
            print(f"Collision Detection Thread Count: {Settings.collision_threads_count}")
        else:
            self.__collision_det_func = self.multi_thread_col_det
            print(f"Collision Detection Thread Count: {Settings.collision_threads_count}")

        threading.Thread(target=self.physics_loop).start()

    def multi_thread_col_det(self):
        thrds = []
        for i in range(Settings.collision_threads_count - 1):
            thrd = threading.Thread(target=self.one_thread_of_multi)
            thrd.start()
            thrds.append(thrd)
        self.one_thread_of_multi()
        for t in thrds:
            t.join()

    def one_thread_of_multi(self):
        while True:
            try:
                while True:
                    try:
                        col1, col2 = self.__col_iter.__next__()
                        break
                    except ValueError:
                        pass

                if are_colliding(col1, col2):
                    self.process_collision(col1, col2)
                else:
                    self.process_collision_2(col1, col2)
            except StopIteration:
                break

    def single_thread_col_det(self):
        while True:
            try:
                col1, col2 = self.__col_iter.__next__()
                if are_colliding(col1, col2):
                    self.process_collision(col1, col2)
                else:
                    self.process_collision_2(col1, col2)
            except StopIteration:
                break

    def physics_loop(self):
        self.__is_psy_loop_running = True
        while Info.is_loop_running:
            now = time.perf_counter()
            Info.instance._call_physics_update()

            self.__col_iter = self.loop_colliders()
            self.__collision_det_func()

            for rb in self.loop_rbs():
                rb.physics_update()

            others.__fixedDeltaTime__ = time.perf_counter() - now
