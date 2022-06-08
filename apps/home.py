"""Primary Home App which allows switching into a number of other apps.

Also includes media control and settings management.
"""

try:
    from typing import Optional
except ImportError:
    pass

from apps.func import FuncKeysApp
from apps.nav import NavApp
from apps.numpad import NumpadApp
from apps.switcher import AppSwitcherApp
from apps.window import WindowManagementApp
from utils.app_pad import AppPad
from utils.apps.key import (
    Key,
    KeyApp,
    KeyAppSettings,
    SettingsSelectKey,
    SettingsValueKey,
)
from utils.commands import (
    ConsumerControlCode,
    Media,
    PreviousAppCommand,
    SwitchAppCommand,
)
from utils.constants import (
    COLOR_APPS,
    COLOR_FUNC,
    COLOR_LINUX,
    COLOR_MAC,
    COLOR_MEDIA,
    COLOR_NAV,
    COLOR_NUMPAD,
    COLOR_WINDOWS,
    COLOR_WINMAN,
    OS_LINUX,
    OS_MAC,
    OS_SETTING,
    OS_WINDOWS,
)


class MacroSettingsApp(KeyApp):
    name = "Macropad Settings"

    key_0 = SettingsSelectKey("MAC", 0x555555, OS_SETTING, OS_MAC, PreviousAppCommand())
    key_1 = SettingsSelectKey(
        "WIN", 0x00A4EF, OS_SETTING, OS_WINDOWS, PreviousAppCommand()
    )
    key_2 = SettingsSelectKey(
        "LIN", 0x25D366, OS_SETTING, OS_LINUX, PreviousAppCommand()
    )

    encoder_button = PreviousAppCommand()


class HomeApp(KeyApp):
    """
    Main menu app that displays when starting the Macropad. Includes media
    controls, a selector for the host OS, and buttons to switch to various
    the other defined apps.
    """

    name = "Home"

    # Fourth row
    key_9 = Key("<<", COLOR_MEDIA, Media(ConsumerControlCode.SCAN_PREVIOUS_TRACK))
    key_10 = Key(">||", COLOR_MEDIA, Media(ConsumerControlCode.PLAY_PAUSE))
    key_11 = Key(">>", COLOR_MEDIA, Media(ConsumerControlCode.SCAN_NEXT_TRACK))

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
        settings_app = MacroSettingsApp(app_pad, settings)
        cls.key_0 = SettingsValueKey(
            OS_SETTING,
            SwitchAppCommand(settings_app),
            color_mapping={
                OS_MAC: COLOR_MAC,
                OS_WINDOWS: COLOR_WINDOWS,
                OS_LINUX: COLOR_LINUX,
            },
            text_template="[ {value} ]",
        )

        numpad_app = NumpadApp(app_pad, settings)
        cls.key_3 = Key(
            text="Num", color=COLOR_NUMPAD, command=SwitchAppCommand(numpad_app)
        )

        nav_app = NavApp(app_pad, settings)
        cls.key_4 = Key(text="Nav", color=COLOR_NAV, command=SwitchAppCommand(nav_app))

        func_keys_app = FuncKeysApp(app_pad, settings)
        cls.key_5 = Key(
            text="Func", color=COLOR_FUNC, command=SwitchAppCommand(func_keys_app)
        )

        app_switcher_app = AppSwitcherApp(app_pad, settings)
        cls.key_6 = Key(
            text="Apps", color=COLOR_APPS, command=SwitchAppCommand(app_switcher_app)
        )

        window_manager_app = WindowManagementApp(app_pad, settings)
        cls.key_8 = Key(
            text="WinMan",
            color=COLOR_WINMAN,
            command=SwitchAppCommand(window_manager_app),
        )
