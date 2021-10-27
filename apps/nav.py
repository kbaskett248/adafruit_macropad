# Nav cluster

from apps.key import Key
from apps.settings import KeyAppWithSettings, PreviousAppCommand
from commands import Keycode, Press
from constants import COLOR_2, COLOR_4, COLOR_8, COLOR_ALERT, COLOR_NAV


class NavApp(KeyAppWithSettings):
    name = "Nav Cluster"

    key_0 = Key("PrtScrn", COLOR_8, Press(Keycode.PRINT_SCREEN))
    key_1 = Key("Home", COLOR_2, Press(Keycode.HOME))
    key_2 = Key("PgUp", COLOR_4, Press(Keycode.PAGE_UP))

    key_3 = Key("Del", COLOR_ALERT, Press(Keycode.DELETE))
    key_4 = Key("End", COLOR_2, Press(Keycode.END))
    key_5 = Key("PgDn", COLOR_4, Press(Keycode.PAGE_DOWN))

    key_7 = Key("/\\", COLOR_NAV, Press(Keycode.UP_ARROW))

    key_9 = Key("<-", COLOR_NAV, Press(Keycode.LEFT_ARROW))
    key_10 = Key("\\/", COLOR_NAV, Press(Keycode.DOWN_ARROW))
    key_11 = Key("->", COLOR_NAV, Press(Keycode.RIGHT_ARROW))

    encoder_button = PreviousAppCommand()
