"""
An App program for Adafruit MACROPAD. Apps can send hotkeys or do pretty much
anything else.
"""

from apps.chrome import ChromeApp
from apps.func import FuncKeysApp
from apps.key import Key
from apps.macro import MacroKey, MacroSettingsApp
from apps.nav import NavApp
from apps.numpad import NumpadApp
from apps.settings import (
    KeyAppWithSettings,
    SettingsValueKey,
    SwitchAppCommand,
    PreviousAppCommand,
)
from apps.spotify import SpotifyApp
from app_pad import AppPad
from apps.window import WindowManagementApp
from commands import (
    ConsumerControlCode,
    Keycode,
    Media,
    Press,
    Release,
    Sequence,
    Wait,
)
from constants import (
    COLOR_APPS,
    COLOR_BACK,
    COLOR_CHROME,
    COLOR_CODE,
    COLOR_FILES,
    COLOR_FUNC,
    COLOR_LINUX,
    COLOR_MAC,
    COLOR_MEDIA,
    COLOR_NAV,
    COLOR_NOTION,
    COLOR_NUMPAD,
    COLOR_PYCHARM,
    COLOR_SLACK,
    COLOR_SPOTIFY,
    COLOR_SUBLIME_MERGE,
    COLOR_TERMINAL,
    COLOR_WINDOWS,
    COLOR_WINMAN,
    OS_SETTING,
    OS_LINUX,
    OS_MAC,
    OS_WINDOWS,
    PREVIOUS_APP_SETTING,
)

app_pad = AppPad()


macro_settings = {
    OS_SETTING: OS_MAC,
    PREVIOUS_APP_SETTING: [],
}


chrome_app = ChromeApp(app_pad, macro_settings)
func_keys_app = FuncKeysApp(app_pad, macro_settings)
nav_app = NavApp(app_pad, macro_settings)
numpad_app = NumpadApp(app_pad, macro_settings)
settings_app = MacroSettingsApp(app_pad, macro_settings)
spotify_app = SpotifyApp(app_pad, macro_settings)
window_manager_app = WindowManagementApp(app_pad, macro_settings)


class AppSwitcherApp(KeyAppWithSettings):
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
            Press(Keycode.WINDOWS), Press(Keycode.SEVEN), SwitchAppCommand(spotify_app)
        ),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.OPTION),
            Press(Keycode.CONTROL),
            Press(Keycode.S),
            SwitchAppCommand(spotify_app),
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


app_switcher_app = AppSwitcherApp(app_pad, macro_settings)


class HomeApp(KeyAppWithSettings):
    name = "Home"

    key_0 = SettingsValueKey(
        OS_SETTING,
        SwitchAppCommand(settings_app),
        color_mapping={
            OS_MAC: COLOR_MAC,
            OS_WINDOWS: COLOR_WINDOWS,
            OS_LINUX: COLOR_LINUX,
        },
        text_template="[ {value} ]",
    )

    key_3 = Key(text="Num", color=COLOR_NUMPAD, command=SwitchAppCommand(numpad_app))
    key_4 = Key(text="Nav", color=COLOR_NAV, command=SwitchAppCommand(nav_app))
    key_5 = Key(text="Func", color=COLOR_FUNC, command=SwitchAppCommand(func_keys_app))

    key_6 = Key(
        text="Apps", color=COLOR_APPS, command=SwitchAppCommand(app_switcher_app)
    )
    key_8 = Key(
        text="WinMan", color=COLOR_WINMAN, command=SwitchAppCommand(window_manager_app)
    )

    # Fourth row
    key_9 = Key("<<", COLOR_MEDIA, Media(ConsumerControlCode.SCAN_PREVIOUS_TRACK))
    key_10 = Key(">||", COLOR_MEDIA, Media(ConsumerControlCode.PLAY_PAUSE))
    key_11 = Key(">>", COLOR_MEDIA, Media(ConsumerControlCode.SCAN_NEXT_TRACK))

    encoder_button = Media(ConsumerControlCode.MUTE)

    encoder_increase = Media(ConsumerControlCode.VOLUME_INCREMENT)
    encoder_decrease = Media(ConsumerControlCode.VOLUME_DECREMENT)

    def __init__(self, app_pad):
        super().__init__(app_pad, settings=macro_settings)


app_pad.add_app(HomeApp)
app_pad.run()
