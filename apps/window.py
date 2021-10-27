# Nav cluster

from apps.macro import MacroKey
from apps.settings import KeyAppWithSettings, PreviousAppCommand
from commands import Keycode, Press, Sequence
from constants import COLOR_2, COLOR_3, COLOR_WINMAN


class WindowManagementApp(KeyAppWithSettings):
    name = "Window Manager"

    key_0 = MacroKey(
        "<-Desk",
        COLOR_3,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.LEFT_ARROW)
        ),
        mac_command=Sequence(Press(Keycode.CONTROL), Press(Keycode.LEFT_ARROW)),
    )
    key_1 = MacroKey(
        "View",
        COLOR_2,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.TAB)),
        mac_command=Sequence(Press(Keycode.CONTROL), Press(Keycode.UP_ARROW)),
    )
    key_2 = MacroKey(
        "Desk->",
        COLOR_3,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.RIGHT_ARROW)
        ),
        mac_command=Sequence(Press(Keycode.CONTROL), Press(Keycode.RIGHT_ARROW)),
    )

    key_3 = MacroKey(
        "TL",
        COLOR_WINMAN,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_SEVEN)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_SEVEN)
        ),
    )
    key_4 = MacroKey(
        "Top",
        COLOR_WINMAN,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_EIGHT)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_EIGHT)
        ),
    )
    key_5 = MacroKey(
        "TR",
        COLOR_WINMAN,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_NINE)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_NINE)
        ),
    )

    key_6 = MacroKey(
        "Left",
        COLOR_WINMAN,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_FOUR)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_FOUR)
        ),
    )
    key_7 = MacroKey(
        "Max",
        COLOR_WINMAN,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_FIVE)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_FIVE)
        ),
    )
    key_8 = MacroKey(
        "Right",
        COLOR_WINMAN,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_SIX)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_SIX)
        ),
    )

    key_9 = MacroKey(
        "BL",
        COLOR_WINMAN,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_ONE)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_ONE)
        ),
    )
    key_10 = MacroKey(
        "Bottom",
        COLOR_WINMAN,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_TWO)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_TWO)
        ),
    )
    key_11 = MacroKey(
        "BR",
        COLOR_WINMAN,
        Sequence(
            Press(Keycode.CONTROL), Press(Keycode.WINDOWS), Press(Keycode.KEYPAD_THREE)
        ),
        mac_command=Sequence(
            Press(Keycode.CONTROL), Press(Keycode.COMMAND), Press(Keycode.KEYPAD_THREE)
        ),
    )
    encoder_button = PreviousAppCommand()
