# MACROPAD Hotkeys example: Mouse control

# The syntax for Mouse macros is highly peculiar, in order to maintain
# backward compatibility with the original keycode-only macro files.
# The third item for each macro is a list in brackets, and each value within
# is normally an integer (Keycode), float (delay) or string (typed literally).
# Consumer Control codes were added as list-within-list, and then mouse
# further complicates this by adding dicts-within-list. Each mouse-related
# dict can have any mix of keys 'buttons' w/integer mask of button values
# (positive to press, negative to release), 'x' w/horizontal motion,
# 'y' w/vertical and 'wheel' with scrollwheel motion.

# To reference Mouse constants, import Mouse like so...
from adafruit_hid.mouse import Mouse

# You can still import Keycode and/or ConsumerControl as well if a macro file
# mixes types! See other macro files for typical Keycode examples.

from app import BaseApp


class MouseApp(BaseApp):
    name = "Mouse"

    # First row
    key_1 = (0x200000, "L", [{"buttons": Mouse.LEFT_BUTTON}])
    key_2 = (0x202000, "M", [{"buttons": Mouse.MIDDLE_BUTTON}])
    key_3 = (0x002000, "R", [{"buttons": Mouse.RIGHT_BUTTON}])

    # Second row
    key_5 = (0x202020, "Up", [{"y": -10}])

    # Third row
    key_7 = (0x202020, "Left", [{"x": -10}])
    key_9 = (0x202020, "Right", [{"x": 10}])

    # Fourth row
    key_11 = (0x202020, "Down", [{"y": 10}])


MouseApp()
