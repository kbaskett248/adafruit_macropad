# MACROPAD Hotkeys example: Mouse control

# To reference Mouse constants, import Mouse like so...
from adafruit_hid.mouse import Mouse

# You can still import Keycode and/or ConsumerControl as well if a macro file
# mixes types! See other macro files for typical Keycode examples.

from app import BaseApp
from key import LabeledKey, MouseClick, MouseMove


class MouseApp(BaseApp):
    name = "Mouse"

    # First row
    key_1 = LabeledKey("L", 0x200000, MouseClick(Mouse.LEFT_BUTTON))
    key_2 = LabeledKey("M", 0x202000, MouseClick(Mouse.MIDDLE_BUTTON))
    key_3 = LabeledKey("R", 0x002000, MouseClick(Mouse.RIGHT_BUTTON))

    # Second row
    key_5 = LabeledKey("Up", 0x202020, MouseMove(y=-10))

    # Third row
    key_7 = LabeledKey("Left", 0x202020, MouseMove(x=-10))
    key_9 = LabeledKey("Right", 0x202020, MouseMove(x=10))

    # Fourth row
    key_11 = LabeledKey("Down", 0x202020, MouseMove(y=10))


MouseApp()
