# MACROPAD Hotkeys example: Universal Numpad

from apps.key import Key
from apps.settings import KeyAppWithSettings, PreviousAppCommand
from commands import Keycode, Press


class FuncKeysApp(KeyAppWithSettings):
    name = "Function Keys"

    # First row
    key_0 = Key("F1", 0x202000, Press(Keycode.F1))
    key_1 = Key("F2", 0x202000, Press(Keycode.F2))
    key_2 = Key("F3", 0x202000, Press(Keycode.F3))

    # Second row
    key_3 = Key("F4", 0x202000, Press(Keycode.F4))
    key_4 = Key("F5", 0x202000, Press(Keycode.F5))
    key_5 = Key("F6", 0x202000, Press(Keycode.F6))

    # Third row
    key_6 = Key("F7", 0x202000, Press(Keycode.F7))
    key_7 = Key("F8", 0x202000, Press(Keycode.F8))
    key_8 = Key("F9", 0x202000, Press(Keycode.F9))

    # Fourth row
    key_9 = Key("F10", 0x101010, Press(Keycode.F10))
    key_10 = Key("F11", 0x800000, Press(Keycode.F11))
    key_11 = Key("F12", 0x101010, Press(Keycode.F12))

    encoder_button = PreviousAppCommand()

    def encoder_button_event(self, event):
        if event.pressed:
            self.encoder_button.execute(self)
        else:
            self.encoder_button.undo(self)
