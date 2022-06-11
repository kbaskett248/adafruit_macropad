try:
    from typing import Dict
except ImportError:
    pass

from apps.home import HomeApp
from utils.app_pad import SerialEvent
from utils.apps.key import KeyApp, KeyAppSettings
from utils.commands import SwitchAppCommand
from utils.constants import (
    COLOR_1,
    COLOR_2,
    COLOR_3,
    COLOR_4,
    COLOR_5,
    COLOR_6,
    COLOR_7,
    COLOR_8,
    COLOR_9,
    COLOR_10,
    COLOR_ALERT,
    COLOR_APPS,
    COLOR_BACK,
    COLOR_CHROME,
    COLOR_CLOSE,
    COLOR_CODE,
    COLOR_FILES,
    COLOR_FUNC,
    COLOR_GO,
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
    COLOR_WARNING,
    COLOR_WINDOWS,
    COLOR_WINMAN,
    EVENT_UPDATE_ACTIVE_WINDOW,
    OS_WINDOWS,
)


class AppSettings(KeyAppSettings):
    color_scheme: Dict[str, int | str] = {
        COLOR_1: 0x4D0204,
        COLOR_2: 0x431A04,
        COLOR_3: 0x442602,
        COLOR_4: 0x4E1C02,
        COLOR_5: 0x4F3803,
        COLOR_6: 0x243417,
        COLOR_7: 0x112A22,
        COLOR_8: 0x132423,
        COLOR_9: 0x161D24,
        COLOR_10: 0x0A1F28,
        COLOR_APPS: COLOR_7,
        COLOR_FUNC: COLOR_4,
        COLOR_MEDIA: COLOR_6,
        COLOR_NAV: COLOR_3,
        COLOR_NUMPAD: COLOR_2,
        COLOR_WINMAN: COLOR_9,
        COLOR_ALERT: COLOR_1,
        COLOR_WARNING: COLOR_5,
        COLOR_GO: COLOR_6,
        COLOR_BACK: COLOR_5,
        COLOR_CLOSE: COLOR_1,
        COLOR_MAC: 0x555555,
        COLOR_WINDOWS: 0x00A4EF,
        COLOR_LINUX: 0x25D366,
        COLOR_CHROME: 0xDC5044,
        COLOR_CODE: 0x1774A5,
        COLOR_FILES: COLOR_2,
        COLOR_NOTION: COLOR_4,
        COLOR_PYCHARM: 0xF4F048,
        COLOR_SLACK: 0x481449,
        COLOR_SPOTIFY: 0x1ED760,
        COLOR_SUBLIME_MERGE: 0x00B3B3,
        COLOR_TERMINAL: COLOR_10,
    }
    host_os = OS_WINDOWS

    AUTO_SWITCH_APPS = ("Chrome", "Spotify")

    def serial_event(self, app: KeyApp, event: SerialEvent):
        event_type = event.message.get("event")
        if event_type == EVENT_UPDATE_ACTIVE_WINDOW:
            active_window = event.message.get("active_window", "")
            self.handle_autoswitch(app, active_window)
        else:
            return super().serial_event(app, event)

    def handle_autoswitch(self, app: KeyApp, active_window: str):
        if not active_window:
            return

        active_window = active_window.lower()

        for app_name in self.AUTO_SWITCH_APPS:
            if app_name.lower() in active_window:
                new_app = self.get_app(app_name)
                if new_app:
                    SwitchAppCommand.switch_app(app, new_app)
                    break

        return


DEFAULT_APP = lambda app_pad: HomeApp(app_pad, AppSettings())
