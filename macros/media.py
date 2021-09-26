# MACROPAD Hotkeys example: Consumer Control codes (media keys)

# The syntax for Consumer Control macros is a little peculiar, in order to
# maintain backward compatibility with the original keycode-only macro files.
# The third item for each macro is a list in brackets, and each value within
# is normally an integer (Keycode), float (delay) or string (typed literally).
# Consumer Control codes are distinguished by enclosing them in a list within
# the list, which is why you'll see double brackets [[ ]] below.
# Like Keycodes, Consumer Control codes can be positive (press) or negative
# (release), and float values can be inserted for pauses.

# To reference Consumer Control codes, import ConsumerControlCode like so...
from adafruit_hid.consumer_control_code import ConsumerControlCode

# You can still import Keycode as well if a macro file mixes types!
# See other macro files for typical Keycode examples.

from app import BaseApp


class MediaApp(BaseApp):
    name = "Media"

    # First row
    key_2 = (0x000020, "Vol+", [[ConsumerControlCode.VOLUME_INCREMENT]])
    key_3 = (0x202020, "Bright+", [[ConsumerControlCode.BRIGHTNESS_INCREMENT]])

    # Second row
    key_5 = (0x000020, "Vol-", [[ConsumerControlCode.VOLUME_DECREMENT]])
    key_6 = (0x202020, "Bright-", [[ConsumerControlCode.BRIGHTNESS_DECREMENT]])

    # Third row
    key_8 = (0x200000, "Mute", [[ConsumerControlCode.MUTE]])

    # Fourth row
    key_10 = (0x202000, "<<", [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]])
    key_11 = (0x002000, "Play/Pause", [[ConsumerControlCode.PLAY_PAUSE]])
    key_12 = (0x202000, ">>", [[ConsumerControlCode.SCAN_NEXT_TRACK]])


MediaApp()
