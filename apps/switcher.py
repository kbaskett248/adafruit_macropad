"""Hotkeys for switching between desktop apps."""

try:
    from typing import Any, Dict, Optional
except ImportError:
    pass

from app_pad import AppPad
from apps.chrome import ChromeApp
from apps.key import Key, KeyApp, MacroKey
from apps.spotify import SpotifyApp
from commands import (
    ConsumerControlCode,
    Keycode,
    Media,
    Press,
    PreviousAppCommand,
    Release,
    Sequence,
    SwitchAppCommand,
    Wait,
)
from constants import (
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
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.FOUR)),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.SHIFT),
            Press(Keycode.ENTER),
        ),
    )
    key_4 = MacroKey(
        "Files",
        COLOR_FILES,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.TWO)),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.CONTROL),
            Press(Keycode.OPTION),
            Press(Keycode.F),
        ),
    )
    key_5 = MacroKey(
        "Spotify",
        COLOR_SPOTIFY,
        Sequence(
            Press(Keycode.WINDOWS),
            Press(Keycode.SEVEN),
        ),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.OPTION),
            Press(Keycode.CONTROL),
            Press(Keycode.S),
        ),
    )

    key_6 = MacroKey(
        "PyCharm",
        COLOR_PYCHARM,
        Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.OPTION),
            Press(Keycode.CONTROL),
            Press(Keycode.H),
        ),
        windows_command=None,
    )
    key_7 = MacroKey(
        "Code",
        COLOR_CODE,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.FIVE)),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.OPTION),
            Press(Keycode.CONTROL),
            Press(Keycode.V),
        ),
    )
    key_8 = MacroKey(
        "Merge",
        COLOR_SUBLIME_MERGE,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.SIX)),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.OPTION),
            Press(Keycode.CONTROL),
            Press(Keycode.M),
        ),
    )

    key_9 = MacroKey(
        "Chrome",
        COLOR_CHROME,
        Sequence(
            Press(Keycode.WINDOWS),
            Press(Keycode.ONE),
            Wait(0.1),
            Release(Keycode.ONE),
            Release(Keycode.WINDOWS),
        ),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.CONTROL),
            Press(Keycode.OPTION),
            Press(Keycode.C),
        ),
    )
    key_10 = MacroKey(
        "Notion",
        COLOR_NOTION,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.THREE)),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.CONTROL),
            Press(Keycode.OPTION),
            Press(Keycode.N),
        ),
    )
    key_11 = MacroKey(
        "Slack",
        COLOR_SLACK,
        Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.CONTROL),
            Press(Keycode.OPTION),
            Press(Keycode.L),
        ),
        windows_command=None,
    )

    encoder_button = Media(ConsumerControlCode.MUTE)

    encoder_increase = Media(ConsumerControlCode.VOLUME_INCREMENT)
    encoder_decrease = Media(ConsumerControlCode.VOLUME_DECREMENT)

    def __init__(self, app_pad: AppPad, settings: Optional[Dict[str, Any]] = None):
        self.initialize_settings_dependent_keys(app_pad, settings)
        super().__init__(app_pad, settings=settings)

    @classmethod
    def initialize_settings_dependent_keys(
        cls, app_pad: AppPad, settings: Optional[Dict[str, Any]] = None
    ):
        chrome_app = ChromeApp(app_pad, settings)
        spotify_app = SpotifyApp(app_pad, settings)

        cls.key_5 = MacroKey(
            "Spotify",
            COLOR_SPOTIFY,
            Sequence(
                Press(Keycode.WINDOWS),
                Press(Keycode.SEVEN),
                SwitchAppCommand(spotify_app),
            ),
            mac_command=Sequence(
                Press(Keycode.COMMAND),
                Press(Keycode.OPTION),
                Press(Keycode.CONTROL),
                Press(Keycode.S),
                SwitchAppCommand(spotify_app),
            ),
        )

        cls.key_9 = MacroKey(
            "Chrome",
            COLOR_CHROME,
            Sequence(
                Press(Keycode.WINDOWS),
                Press(Keycode.ONE),
                Wait(0.1),
                Release(Keycode.ONE),
                Release(Keycode.WINDOWS),
                SwitchAppCommand(chrome_app),
            ),
            mac_command=Sequence(
                Press(Keycode.COMMAND),
                Press(Keycode.CONTROL),
                Press(Keycode.OPTION),
                Press(Keycode.C),
                SwitchAppCommand(chrome_app),
            ),
        )
