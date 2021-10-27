# Nav cluster

from apps.macro import MacroKey
from apps.settings import KeyAppWithSettings, PreviousAppCommand
from commands import Keycode, Press, Sequence


class WindowManagementApp(KeyAppWithSettings):
    name = "Window Manager"

    key_0 = MacroKey(
        "<-Desk",
        0x101010,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.LEFT_ARROW)
        ),
        mac_command=Sequence(Press(Keycode.CONTROL), Press(Keycode.LEFT_ARROW)),
    )
    key_1 = MacroKey(
        "View",
        0x101010,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.TAB)),
        mac_command=Sequence(Press(Keycode.CONTROL), Press(Keycode.UP_ARROW)),
    )
    key_2 = MacroKey(
        "Desk->",
        0x101010,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.RIGHT_ARROW)
        ),
        mac_command=Sequence(Press(Keycode.CONTROL), Press(Keycode.RIGHT_ARROW)),
    )

    key_3 = MacroKey(
        "TL",
        0x101010,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_SEVEN)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_SEVEN)
        ),
    )
    key_4 = MacroKey(
        "Top",
        0x101010,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_EIGHT)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_EIGHT)
        ),
    )
    key_5 = MacroKey(
        "TR",
        0x101010,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_NINE)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_NINE)
        ),
    )

    key_6 = MacroKey(
        "Left",
        0x101010,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_FOUR)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_FOUR)
        ),
    )
    key_7 = MacroKey(
        "Max",
        0x1ED760,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_FIVE)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_FIVE)
        ),
    )
    key_8 = MacroKey(
        "Right",
        0x1ED760,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_SIX)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_SIX)
        ),
    )

    key_9 = MacroKey(
        "BL",
        0x1ED760,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_ONE)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_ONE)
        ),
    )
    key_10 = MacroKey(
        "Bottom",
        0x1ED760,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_TWO)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_TWO)
        ),
    )
    key_11 = MacroKey(
        "BR",
        0x1ED760,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_THREE)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_THREE)
        ),
    )
    encoder_button = PreviousAppCommand()

    def encoder_button_event(self, event):
        if event.pressed:
            self.encoder_button.execute(self)
        else:
            self.encoder_button.undo(self)
