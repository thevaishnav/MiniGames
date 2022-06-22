from MiniGames.Utils.type_checker import type_check

import pygame
from enum import Enum


class Keycodes(Enum):
    keypad_0 = 48
    keypad_1 = 49
    keypad_2 = 50
    keypad_3 = 51
    keypad_4 = 52
    keypad_5 = 53
    keypad_6 = 54
    keypad_7 = 55
    keypad_8 = 56
    keypad_9 = 57
    numpad_0 = 1073741922
    numpad_1 = 1073741913
    numpad_2 = 1073741914
    numpad_3 = 1073741915
    numpad_4 = 1073741916
    numpad_5 = 1073741917
    numpad_6 = 1073741918
    numpad_7 = 1073741919
    numpad_8 = 1073741920
    numpad_9 = 1073741921
    a = 97
    b = 98
    c = 99
    d = 100
    e = 101
    f = 102
    g = 103
    h = 104
    i = 105
    j = 106
    k = 107
    l = 108
    m = 109
    n = 110
    o = 111
    p = 112
    q = 113
    r = 114
    s = 115
    t = 116
    u = 117
    v = 118
    w = 119
    x = 120
    y = 121
    z = 122

    ac_back = 1073742094
    ampersand = 38
    asterisk = 42
    at = 64
    backquote = 96
    backslash = 92
    backspace = 8
    break_ = 1073741896
    capslock = 1073741881
    caret = 94
    clear = 1073741980
    colon = 58
    comma = 44
    currencysubunit = 1073742005
    currencyunit = 1073742004
    delete = 127
    dollar = 36
    down = 1073741905
    end = 1073741901
    equals = 61
    escape = 27
    euro = 1073742004
    exclaim = 33
    f1 = 1073741882
    f2 = 1073741883
    f3 = 1073741884
    f4 = 1073741885
    f5 = 1073741886
    f6 = 1073741887
    f7 = 1073741888
    f8 = 1073741889
    f9 = 1073741890
    f10 = 1073741891
    f11 = 1073741892
    f12 = 1073741893
    f13 = 1073741928
    f14 = 1073741929
    f15 = 1073741930
    greater = 62
    hash = 35
    help = 1073741941
    home = 1073741898
    insert = 1073741897
    kp_divide = 1073741908
    kp_enter = 1073741912
    kp_equals = 1073741927
    kp_minus = 1073741910
    kp_multiply = 1073741909
    kp_period = 1073741923
    kp_plus = 1073741911
    lalt = 1073742050
    lctrl = 1073742048
    left = 1073741904
    leftbracket = 91
    leftparen = 40
    less = 60
    lgui = 1073742051
    lmeta = 1073742051
    lshift = 1073742049
    lsuper = 1073742051
    menu = 1073741942
    minus = 45
    mode = 1073742081
    numlock = 1073741907
    numlockclear = 1073741907
    pagedown = 1073741902
    pageup = 1073741899
    pause = 1073741896
    percent = 37
    period = 46
    plus = 43
    power = 1073741926
    print = 1073741894
    printscreen = 1073741894
    question = 63
    quote = 39
    quotedbl = 34
    ralt = 1073742054
    rctrl = 1073742052
    return_ = 13
    rgui = 1073742055
    right = 1073741903
    rightbracket = 93
    rightparen = 41
    rmeta = 1073742055
    rshift = 1073742053
    rsuper = 1073742055
    scrolllock = 1073741895
    scrollock = 1073741895
    semicolon = 59
    slash = 47
    space = 32
    sysreq = 1073741978
    tab = 9
    underscore = 95
    unknown = 0
    up = 1073741906


class InputClass:
    def __init__(self):
        self.__mDown = set()
        self.__mHold = set()
        self.__mUp = set()
        self.__kDown = set()
        self.__kHold = set()
        self.__kUp = set()
        self.SHOULD_QUIT = False

    def _in_update(self):
        self.__mHold.update(self.__mDown)
        self.__mUp.clear()
        self.__mDown.clear()

        self.__kHold.update(self.__kDown)
        self.__kUp.clear()
        self.__kDown.clear()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.SHOULD_QUIT = True

            if ev.type == pygame.KEYUP:
                self.__kHold.discard(ev.key)
                self.__kUp.add(ev.key)
            elif ev.type == pygame.KEYDOWN:
                self.__kDown.add(ev.key)

            elif ev.type == pygame.MOUSEBUTTONUP:
                self.__mHold.discard(ev.button)
                self.__mUp.add(ev.button)
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                self.__mDown.add(ev.button)

    def get_mouse_down(self, button: int) -> bool:
        type_check("button", button, int)
        """
        :param button: 1 = left_mouse_button, 2 = middle_mouse_button, 3 = right_mouse_button
        :return: True if specified mouse button was pressed in this frame, else False
        """
        return button in self.__mDown

    def get_mouse_up(self, button: int) -> bool:
        type_check("button", button, int)
        """
        :param button: 1 = left_mouse_button, 2 = middle_mouse_button, 3 = right_mouse_button
        :return: True if specified mouse button was released in this frame, else False
        """
        return button in self.__mUp

    def get_mouse_hold(self, button: int) -> bool:
        type_check("button", button, int)
        """
        :param button: 1 = left_mouse_button, 2 = middle_mouse_button, 3 = right_mouse_button
        :return: True if specified mouse button is held down in this frame, else False
        """
        return button in self.__mHold

    def get_key_down(self, code: Keycodes) -> bool:
        type_check("code", code, Keycodes)
        """
        :param code: enum-value of enum Keycodes
        :return: True if specified keyboard button was pressed in this frame, else False
        """
        return int(code.value) in self.__kDown

    def get_key_up(self, code: Keycodes) -> bool:
        type_check("code", code, Keycodes)
        """
        :param code: enum-value of enum Keycodes
        :return: True if specified mouse button was released in this frame, else False
        """
        return int(code.value) in self.__kUp

    def get_key_hold(self, code: Keycodes) -> bool:
        type_check("code", code, Keycodes)
        """
        :param code: enum-value of enum Keycodes
        :return: True if specified mouse button is held down in this frame, else False
        """
        return int(code.value) in self.__kHold

    def get_mouse_wheel(self) -> int:
        """
        :return: number of times the mouse wheel was rotated. Up is +ve, Down is -ve, 0 means not rotated
        """
        evs = pygame.event.get(pygame.MOUSEWHEEL)
        if evs: return evs[0].y
        return 0


Input = InputClass()
