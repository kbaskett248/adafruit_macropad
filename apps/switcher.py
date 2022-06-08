"""Hotkeys for switching between desktop apps."""

try:
    from typing import Optional
except ImportError:
    pass

from apps.chrome import ChromeApp
from apps.spotify import SpotifyApp
from utils.app_pad import AppPad
from utils.apps.key import Key, KeyApp, KeyAppSettings, MacroKey
from utils.commands import (
    ConsumerControlCode,
    Keycode,
    MacroCommand,
    Media,
    Press,
    PreviousAppCommand,
    Release,
    Sequence,
    SwitchAppCommand,
    Wait,
)
from utils.constants import (
    COLOR_BACK,
    COLOR_CHROME,
    COLOR_CODE,
    COLOR_FILES,
    COLOR_NOTION,
    COLOR_PYCHARM,
    COLOR_SLACK,
    COLOR_SPOTIFY,
    COLOR_SUBLIME_MERGE,
    COLOR_TERMINAL,
    OS_MAC,
)


class AppSwitcherApp(KeyApp):
    """
    App with commands for switching between desktop apps. Some desktop apps
    also have a context-specific app for that desktop app. These will display
    when you switch to the app with the hotkey.
    """

    name = "App Switcher"

    key_2 = Key(
        "Back",
        COLOR_BACK,
        PreviousAppCommand(),
        double_tap_command=PreviousAppCommand(),
    )

    key_3 = MacroKey(
        "Term",
        COLOR_TERMINAL,
        Press(Keycode.WINDOWS, Keycode.FOUR),
        mac_command=Press(Keycode.COMMAND, Keycode.SHIFT, Keycode.ENTER),
    )
    key_4 = MacroKey(
        "Files",
        COLOR_FILES,
        Press(Keycode.WINDOWS, Keycode.TWO),
        mac_command=Press(Keycode.COMMAND, Keycode.CONTROL, Keycode.OPTION, Keycode.F),
    )
    key_5 = MacroKey(
        "Spotify",
        COLOR_SPOTIFY,
        Press(Keycode.WINDOWS, Keycode.SEVEN),
        mac_command=Press(Keycode.COMMAND, Keycode.OPTION, Keycode.CONTROL, Keycode.S),
    )

    key_6 = MacroKey(
        "PyCharm",
        COLOR_PYCHARM,
        Press(Keycode.COMMAND, Keycode.OPTION, Keycode.CONTROL, Keycode.H),
        windows_command=None,
    )
    key_7 = MacroKey(
        "Code",
        COLOR_CODE,
        Press(Keycode.WINDOWS, Keycode.FIVE),
        mac_command=Press(Keycode.COMMAND, Keycode.OPTION, Keycode.CONTROL, Keycode.V),
    )
    key_8 = MacroKey(
        "Merge",
        COLOR_SUBLIME_MERGE,
        Press(Keycode.WINDOWS, Keycode.SIX),
        mac_command=Press(Keycode.COMMAND, Keycode.OPTION, Keycode.CONTROL, Keycode.M),
    )

    key_9 = MacroKey(
        "Chrome",
        COLOR_CHROME,
        Sequence(
            Press(Keycode.WINDOWS, Keycode.ONE),
            Wait(0.1),
            Release(Keycode.ONE, Keycode.WINDOWS),
        ),
        mac_command=Press(Keycode.COMMAND, Keycode.CONTROL, Keycode.OPTION, Keycode.C),
    )
    key_10 = MacroKey(
        "Notion",
        COLOR_NOTION,
        Press(Keycode.WINDOWS, Keycode.THREE),
        mac_command=Press(Keycode.COMMAND, Keycode.CONTROL, Keycode.OPTION, Keycode.N),
    )
    key_11 = MacroKey(
        "Slack",
        COLOR_SLACK,
        Press(Keycode.COMMAND, Keycode.CONTROL, Keycode.OPTION, Keycode.L),
        windows_command=None,
    )

    encoder_button = Media(ConsumerControlCode.MUTE)

    encoder_increase = Media(ConsumerControlCode.VOLUME_INCREMENT)
    encoder_decrease = Media(ConsumerControlCode.VOLUME_DECREMENT)

    def __init__(self, app_pad: AppPad, settings: Optional[KeyAppSettings] = None):
        self.initialize_settings_dependent_keys(app_pad, settings)
        super().__init__(app_pad, settings=settings)

    @classmethod
    def initialize_settings_dependent_keys(
        cls, app_pad: AppPad, settings: Optional[KeyAppSettings] = None
    ):
        chrome_app = ChromeApp(app_pad, settings)
        spotify_app = SpotifyApp(app_pad, settings)

        cls.key_5 = MacroKey(
            "Spotify",
            COLOR_SPOTIFY,
            Press(Keycode.WINDOWS, Keycode.SEVEN),
            mac_command=Press(
                Keycode.COMMAND, Keycode.OPTION, Keycode.CONTROL, Keycode.S
            ),
            double_tap_command=MacroCommand(
                Sequence(
                    Press(Keycode.WINDOWS, Keycode.SEVEN),
                    SwitchAppCommand(spotify_app),
                ),
                **{
                    OS_MAC: Sequence(
                        Press(
                            Keycode.COMMAND, Keycode.OPTION, Keycode.CONTROL, Keycode.S
                        ),
                        SwitchAppCommand(spotify_app),
                    ),
                }
            ),
        )

        cls.key_9 = MacroKey(
            "Chrome",
            COLOR_CHROME,
            Sequence(
                Press(Keycode.WINDOWS, Keycode.ONE),
                Wait(0.1),
                Release(Keycode.ONE, Keycode.WINDOWS),
            ),
            mac_command=Press(
                Keycode.COMMAND, Keycode.CONTROL, Keycode.OPTION, Keycode.C
            ),
            double_tap_command=MacroCommand(
                Sequence(
                    Press(Keycode.WINDOWS, Keycode.ONE),
                    Wait(0.1),
                    Release(Keycode.ONE, Keycode.WINDOWS),
                    SwitchAppCommand(chrome_app),
                ),
                **{
                    OS_MAC: Sequence(
                        Press(
                            Keycode.COMMAND, Keycode.CONTROL, Keycode.OPTION, Keycode.C
                        ),
                        SwitchAppCommand(chrome_app),
                    ),
                }
            ),
        )
