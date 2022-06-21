from MiniGames.Utils.vector2 import Vector2
from MiniGames.Physics.collider_base import ColliderBase


def get_support_point(s1: ColliderBase, s2: ColliderBase, d: Vector2) -> Vector2:
    d.normalize_self()
    return s1.furthest_point(d) - s2.furthest_point(-d)


def line_case(simplex: list[Vector2], d: Vector2) -> bool:
    B, A = simplex
    AB, AO = B - A, -A
    ABperp = Vector2.triple_product(AB, AO, AB)
    d.set_self(ABperp)
    d.normalize_self()
    return False


def triangle_case(simplex: list[Vector2], d: Vector2) -> bool:
    C, B, A = simplex
    AB, AC, AO = B - A, C - A, -A
    ABperp = Vector2.triple_product(AC, AB, AB)
    ACperp = Vector2.triple_product(AB, AC, AC)
    if ABperp.dot(AO) > 0:
        simplex.remove(C)
        d.set_self(ABperp)
        d.normalize_self()
        return False

    if ACperp.dot(AO) > 0:
        simplex.remove(B)
        d.set_self(ACperp)
        d.normalize_self()
        return False
    return True


def handle_simplex(simplex: list[Vector2], d: Vector2) -> bool:
    if len(simplex) == 2:
        return line_case(simplex, d)
    return triangle_case(simplex, d)


def are_colliding(s1: ColliderBase, s2: ColliderBase) -> bool:
    d = s2.get_center() - s1.get_center()
    d.normalize_self()
    simplex = [get_support_point(s1, s2, d)]
    d = -simplex[0]

    while True:
        A = get_support_point(s1, s2, d)
        if A.dot(d) < 0:
            return False

        simplex.append(A)
        if handle_simplex(simplex, d):
            return True