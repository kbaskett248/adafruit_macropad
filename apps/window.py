"""App with macros for managing windows and virtual desktops."""

from utils.apps.key import KeyApp, MacroKey
from utils.commands import Keycode, Press, PreviousAppCommand
from utils.constants import COLOR_2, COLOR_3, COLOR_WINMAN


class WindowManagementApp(KeyApp):
    name = "Window Manager"

    key_0 = MacroKey(
        "<-Desk",
        COLOR_3,
        Press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.LEFT_ARROW),
        mac_command=Press(Keycode.CONTROL, Keycode.LEFT_ARROW),
    )
    key_1 = MacroKey(
        "View",
        COLOR_2,
        Press(Keycode.WINDOWS, Keycode.TAB),
        mac_command=Press(Keycode.CONTROL, Keycode.UP_ARROW),
    )
    key_2 = MacroKey(
        "Desk->",
        COLOR_3,
        Press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.RIGHT_ARROW),
        double_tap_command=PreviousAppCommand(),
        mac_command=Press(Keycode.CONTROL, Keycode.RIGHT_ARROW),
    )

    key_3 = MacroKey(
        "TL",
        COLOR_WINMAN,
        Press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.KEYPAD_SEVEN),
        mac_command=Press(Keycode.CONTROL, Keycode.COMMAND, Keycode.KEYPAD_SEVEN),
    )
    key_4 = MacroKey(
        "Top",
        COLOR_WINMAN,
        Press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.KEYPAD_EIGHT),
        mac_command=Press(Keycode.CONTROL, Keycode.COMMAND, Keycode.KEYPAD_EIGHT),
    )
    key_5 = MacroKey(
        "TR",
        COLOR_WINMAN,
        Press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.KEYPAD_NINE),
        mac_command=Press(Keycode.CONTROL, Keycode.COMMAND, Keycode.KEYPAD_NINE),
    )

    key_6 = MacroKey(
        "Left",
        COLOR_WINMAN,
        Press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.KEYPAD_FOUR),
        mac_command=Press(Keycode.CONTROL, Keycode.COMMAND, Keycode.KEYPAD_FOUR),
    )
    key_7 = MacroKey(
        "Max",
        COLOR_WINMAN,
        Press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.KEYPAD_FIVE),
        mac_command=Press(Keycode.CONTROL, Keycode.COMMAND, Keycode.KEYPAD_FIVE),
    )
    key_8 = MacroKey(
        "Right",
        COLOR_WINMAN,
        Press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.KEYPAD_SIX),
        mac_command=Press(Keycode.CONTROL, Keycode.COMMAND, Keycode.KEYPAD_SIX),
    )

    key_9 = MacroKey(
        "BL",
        COLOR_WINMAN,
        Press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.KEYPAD_ONE),
        mac_command=Press(Keycode.CONTROL, Keycode.COMMAND, Keycode.KEYPAD_ONE),
    )
    key_10 = MacroKey(
        "Bottom",
        COLOR_WINMAN,
        Press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.KEYPAD_TWO),
        mac_command=Press(Keycode.CONTROL, Keycode.COMMAND, Keycode.KEYPAD_TWO),
    )
    key_11 = MacroKey(
        "BR",
        COLOR_WINMAN,
        Press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.KEYPAD_THREE),
        mac_command=Press(Keycode.CONTROL, Keycode.COMMAND, Keycode.KEYPAD_THREE),
    )
    encoder_button = PreviousAppCommand()
