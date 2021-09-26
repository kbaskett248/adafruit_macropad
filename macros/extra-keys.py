# Extra keys missing from my keyboard

from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values
from adafruit_hid.mouse import Mouse

from app import BaseApp


class ExtraKeysApp(BaseApp):
    name = "Extra keys"

    key_1 = (0x004000, "Home", [Keycode.HOME])
    key_2 = (0x004000, "End", [Keycode.END])
    key_3 = (0x400000, "Up", [{"wheel": 5}])

    key_6 = (0x400000, "Down", [{"wheel": -5}])


ExtraKeysApp()
