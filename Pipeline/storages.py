from __future__ import annotations
import typing, collections
from MiniGames.Utils.settings_and_info import Info
if typing.TYPE_CHECKING:
    from MiniGames.Pipeline.gameobject import GameObject
    from MiniGames.Pipeline.monobehaviour import MonoBehaviour
    from MiniGames.Pipeline.coroutines import WaitFor
    from MiniGames.Renderers.renderer_base import RendererBase


class GameObjectsStorage:
    def __init__(self):
        self.all_monos: dict[str: list[MonoBehaviour]] = {}

        self.cour: dict[typing.Generator[WaitFor, None, None], WaitFor] = {}
        self.hidden_rend: set[MonoBehaviour] = set()
        self.u: set[MonoBehaviour] = set()
        self.lu: set[MonoBehaviour] = set()
        self.fu: set[MonoBehaviour] = set()
        self.oci: set[MonoBehaviour] = set()
        self.oco: set[MonoBehaviour] = set()
        self.ocs: set[MonoBehaviour] = set()
        self.oti: set[MonoBehaviour] = set()
        self.oto: set[MonoBehaviour] = set()
        self.ots: set[MonoBehaviour] = set()
        self.r: set[RendererBase] = set()
        self.to_add: dict[str: list[MonoBehaviour]] = {}
        self.rem_fr: dict[str: list[MonoBehaviour]] = {}

    def Loop(self, code: str) -> collections.Iterable[MonoBehaviour]:
        self.to_add[code] = []
        self.rem_fr[code] = []

        for i in self.__dict__[code]:
            yield i

        while self.to_add[code]:
            new_looper = list(self.to_add[code])
            self.to_add[code].clear()
            for i in new_looper:
                self.__dict__[code].add(i)
                yield i

        for ob in self.rem_fr[code]:
            self.__dict__[code].discard(ob)

        self.rem_fr.pop(code)
        self.to_add.pop(code)

    def LoopAll(self) -> collections.Iterable[MonoBehaviour]:
        self.to_add["all"] = []
        self.rem_fr["all"] = []

        for mono_list in self.all_monos.values():
            for mono in mono_list:
                yield mono

        while self.to_add["all"]:
            new_looper = list(self.to_add["all"])
            self.to_add["all"].clear()
            for i in new_looper:
                qName = type(i).__qualname__
                if qName in self.all_monos:
                    if i not in self.all_monos[qName]:
                        self.all_monos[qName].append(i)
                        yield i
                else:
                    self.all_monos[qName] = [i, ]
                    yield i

        for ob in self.rem_fr["all"]:
            qname = type(ob).__qualname__
            if qname in self.all_monos and ob in self.all_monos[qname]:
                self.all_monos[qname].remove(ob)
        self.rem_fr.pop("all")
        self.to_add.pop("all")

    def add_to(self, code: str, obj):
        if code not in self.to_add:
            self.__dict__[code].add(obj)
        else:
            self.to_add[code].append(obj)

    def add_to_all(self, obj):
        if "all" not in self.to_add:
            qname = type(obj).__qualname__
            if qname in self.all_monos:
                self.all_monos[qname].append(obj)
            else:
                self.all_monos[qname] = [obj]
        else:
            self.to_add["all"].append(obj)

    def add_cour(self, iter, i):
        self.cour[iter] = i

    def rem_from(self, code, obj):
        if code not in self.rem_fr:
            self.__dict__[code].discard(obj)
        else:
            self.rem_fr[code].append(obj)

    def RMFRAL(self, obj):
        if "all" not in self.rem_fr:
            qname = type(obj).__qualname__
            if qname in self.all_monos:
                self.all_monos[qname].remove(obj)
        else:
            self.rem_fr["all"].append(obj)

    def rem_from_all(self, obj):
        try:
            self.RMFRAL(obj)
        except ValueError:
            pass

    def get_component(self, _t: type):
        if _t.__qualname__ in self.all_monos:
            return self.all_monos[_t.__qualname__][0]
        return None

    def get_all_components(self, _t: type):
        if _t.__class__ in self.all_monos:
            return self.all_monos[_t.__class__]
        return None

    def HandleCour(self):
        if len(self.cour) == 0: return
        to_pop = []
        for itr in self.cour:
            try:
                wait_for = self.cour[itr]
                if wait_for.should_call(Info.deltaTime):
                    self.cour[itr] = itr.__next__()
            except StopIteration:
                to_pop.append(itr)
        for p in to_pop:
            self.cour.pop(p)


class AppStorage:
    def __init__(self):
        self._active_gos = set()
        self._to_add_gos = []
        self._to_rem_gos = []
        self._looping_gos = False

    def Loop_GOs(self) -> typing.Iterable[GameObject]:
        self._looping_gos = True

        for i in self._active_gos:
            yield i

        while self._to_add_gos:
            new_looper = list(self._to_add_gos)
            self._to_add_gos.clear()
            for i in new_looper:
                self._active_gos.add(i)
                yield i

        for ob in self._to_rem_gos:
            self._active_gos.discard(ob)

        self._to_rem_gos.clear()
        self._to_add_gos.clear()
        self._looping_gos = False

    def add_to_gos(self, obj):
        if not self._looping_gos:
            self._active_gos.add(obj)
        else:
            self._to_add_gos.append(obj)

    def rem_from_gos(self, obj):
        if not self._looping_gos:
            self._active_gos.discard(obj)
        else:
            self._to_rem_gos.append(obj)


class LayeredStorage:
    def __init__(self):
        self.__inner = {}
        self.__all_layers = []
        self.__exclude = set()

    def add_obj(self, layer: int, obj):
        if layer in self.__inner:
            if obj not in self.__inner[layer]:
                self.__inner[layer].append(obj)
        else:
            self.__inner[layer] = [obj]
            self.__all_layers.append(layer)
            self.__all_layers.sort()

    def remove_obj(self, layer: int, obj):
        if layer not in self.__inner: return
        ins = self.__inner[layer]

        if obj not in ins: return
        ins.remove(obj)

        if len(ins) != 0: return

        self.__inner.pop(layer)
        self.__exclude.discard(layer)
        if layer in self.__all_layers:
            self.__all_layers.remove(layer)

    def change_obj_layer(self, obj, old_layer: int, new_layer: int):
        self.remove_obj(old_layer, obj)
        self.add_obj(new_layer, obj)

    def exclude_single(self, layer: int):
        self.__exclude.add(layer)

    def include_single(self, layer: int):
        self.__exclude.discard(layer)

    def exclude_double(self, layer1: int, layer2: int):
        self.__exclude.add(get_double_id(layer1, layer2))

    def include_double(self, layer1: int, layer2: int):
        self.__exclude.discard(get_double_id(layer1, layer2))

    def loop_single(self):
        for lyr in self.__all_layers:
            if lyr in self.__exclude: continue
            for item in self.__inner[lyr]:
                yield item

    def loop_double(self):
        for index, layer1 in enumerate(self.__all_layers):
            for layer2 in self.__all_layers[index + 1:]:
                if get_double_id(layer1, layer2) in self.__exclude: continue

                for obj1 in self.__inner[layer1]:
                    for obj2 in self.__inner[layer2]:
                        yield obj1, obj2

            if get_double_id(layer1, layer1) in self.__exclude: continue
            layer_objs = self.__inner[layer1]
            for i, obj1 in enumerate(layer_objs):
                for obj2 in layer_objs[i + 1:]:
                    yield obj1, obj2


def get_double_id(lyr1: int, lyr2: int):
    return str((1 << lyr1) | (1 << lyr2))
