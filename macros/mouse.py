# MACROPAD Hotkeys example: Mouse control

# To reference Mouse constants, import Mouse like so...
from adafruit_hid.mouse import Mouse

# You can still import Keycode and/or ConsumerControl as well if a macro file
# mixes types! See other macro files for typical Keycode examples.

from app import BaseApp, MacroApp
from key import Key, MouseClick, MouseMove


@BaseApp.register_app
class MouseApp(MacroApp):
    name = "Mouse"

    # First row
    key_0 = Key("L", 0x200000, MouseClick(Mouse.LEFT_BUTTON))
    key_1 = Key("M", 0x202000, MouseClick(Mouse.MIDDLE_BUTTON))
    key_2 = Key("R", 0x002000, MouseClick(Mouse.RIGHT_BUTTON))

    # Second row
    key_4 = Key("Up", 0x202020, MouseMove(y=-10))

    # Third row
    key_6 = Key("Left", 0x202020, MouseMove(x=-10))
    key_8 = Key("Right", 0x202020, MouseMove(x=10))

    # Fourth row
    key_10 = Key("Down", 0x202020, MouseMove(y=10))
