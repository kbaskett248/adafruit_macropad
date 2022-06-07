try:
    from typing import Dict
except ImportError:
    pass

from apps.home import HomeApp
from utils.apps.key import KeyAppSettings
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


DEFAULT_APP = lambda app_pad: HomeApp(app_pad, AppSettings())
