# Extra keys missing from my keyboard

from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values
from adafruit_hid.mouse import Mouse

from app import BaseApp
from key import LabeledKey, Press, Scroll


class ExtraKeysApp(BaseApp):
    name = "Extra keys"

    key_1 = LabeledKey("Home", 0x004000, Press(Keycode.HOME))
    key_2 = LabeledKey("End", 0x004000, Press(Keycode.END))
    key_3 = LabeledKey("Up", 0x400000, Scroll(5))

    key_6 = LabeledKey("Down", 0x400000, Scroll(-5))


ExtraKeysApp()
