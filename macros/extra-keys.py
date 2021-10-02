# Extra keys missing from my keyboard

from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values
from adafruit_hid.mouse import Mouse

from app import BaseApp
from key import LabeledKey, Media, Press, Scroll


class ExtraKeysApp(BaseApp):
    name = "Extra keys"

    key_1 = LabeledKey("Home", 0x004000, Press(Keycode.HOME))
    key_2 = LabeledKey("End", 0x004000, Press(Keycode.END))
    key_3 = LabeledKey("Up", 0x400000, Scroll(5))

    key_6 = LabeledKey("Down", 0x400000, Scroll(-5))

    key_7 = LabeledKey("Vol-", 0x000020, Media(ConsumerControlCode.VOLUME_DECREMENT))
    key_8 = LabeledKey("Mute", 0x200000, Media(ConsumerControlCode.MUTE))
    key_9 = key_2 = LabeledKey(
        "Vol+", 0x000020, Media(ConsumerControlCode.VOLUME_INCREMENT)
    )

    key_10 = LabeledKey("<<", 0x202000, Media(ConsumerControlCode.SCAN_PREVIOUS_TRACK))
    key_11 = LabeledKey("Play/Pause", 0x002000, Media(ConsumerControlCode.PLAY_PAUSE))
    key_12 = LabeledKey(">>", 0x202000, Media(ConsumerControlCode.SCAN_NEXT_TRACK))


ExtraKeysApp()
