# Nav cluster

from apps.key import Key
from apps.settings import KeyAppWithSettings
from commands import Keycode, Press, PreviousAppCommand


class NavApp(KeyAppWithSettings):
    name = "Nav Cluster"

    key_0 = Key("PrtScrn", 0x004000, Press(Keycode.PRINT_SCREEN))
    key_1 = Key("Home", 0x004000, Press(Keycode.HOME))
    key_2 = Key("PgUp", 0x004000, Press(Keycode.PAGE_UP))

    key_3 = Key("Del", 0x004000, Press(Keycode.DELETE))
    key_4 = Key("End", 0x004000, Press(Keycode.END))
    key_5 = Key("PgDn", 0x004000, Press(Keycode.PAGE_DOWN))

    key_7 = Key("/\\", 0x200000, Press(Keycode.UP_ARROW))

    key_9 = Key("<-", 0x200000, Press(Keycode.LEFT_ARROW))
    key_10 = Key("\\/", 0x200000, Press(Keycode.DOWN_ARROW))
    key_11 = Key("->", 0x200000, Press(Keycode.RIGHT_ARROW))

    encoder_button = PreviousAppCommand()

    def encoder_button_event(self, event):
        if event.pressed:
            self.encoder_button.execute(self)
        else:
            self.encoder_button.undo(self)
