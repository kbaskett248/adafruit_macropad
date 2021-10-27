# MACROPAD Hotkeys example: Universal Numpad

from apps.key import Key
from apps.settings import KeyAppWithSettings, PreviousAppCommand
from commands import Keycode, Press
from constants import COLOR_FUNC


class FuncKeysApp(KeyAppWithSettings):
    name = "Function Keys"

    # First row
    key_0 = Key("F1", COLOR_FUNC, Press(Keycode.F1))
    key_1 = Key("F2", COLOR_FUNC, Press(Keycode.F2))
    key_2 = Key("F3", COLOR_FUNC, Press(Keycode.F3))

    # Second row
    key_3 = Key("F4", COLOR_FUNC, Press(Keycode.F4))
    key_4 = Key("F5", COLOR_FUNC, Press(Keycode.F5))
    key_5 = Key("F6", COLOR_FUNC, Press(Keycode.F6))

    # Third row
    key_6 = Key("F7", COLOR_FUNC, Press(Keycode.F7))
    key_7 = Key("F8", COLOR_FUNC, Press(Keycode.F8))
    key_8 = Key("F9", COLOR_FUNC, Press(Keycode.F9))

    # Fourth row
    key_9 = Key("F10", COLOR_FUNC, Press(Keycode.F10))
    key_10 = Key("F11", COLOR_FUNC, Press(Keycode.F11))
    key_11 = Key("F12", COLOR_FUNC, Press(Keycode.F12))

    encoder_button = PreviousAppCommand()
