"""Defines numerous constants used throughout the project."""

# A unique empty value used when None is a valid value.
EMPTY_VALUE = object()

# The height and width of the macropad display.
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

# Settings

# The setting name for the previous app setting
PREVIOUS_APP_SETTING = "previous app"

# The setting name and options for the OS setting
OS_SETTING = "OS"
OS_MAC = "MAC"
OS_WINDOWS = "WIN"
OS_LINUX = "LIN"

# Setting name for the pixels disabled setting
PIXELS_DISABLED_SETTING = "pixels disabled"

# Timeout after which the pixels will be disabled
ONE_MINUTE = 60
DISABLE_PIXELS_TIMEOUT = 20 * ONE_MINUTE

# Timer ID for the disabled pixels timer
TIMER_DISABLE_PIXELS = "disable pixels timer"

# Defines a color scheme for the Macropad. You can reference these constants
# for pixel colors to define a consistent color scheme and make it easy to
# update the colors
COLOR_1 = 0x4D0204
COLOR_2 = 0x431A04
COLOR_3 = 0x442602
COLOR_4 = 0x4E1C02
COLOR_5 = 0x4F3803
COLOR_6 = 0x243417
COLOR_7 = 0x112A22
COLOR_8 = 0x132423
COLOR_9 = 0x161D24
COLOR_10 = 0x0A1F28

COLOR_APPS = COLOR_7
COLOR_FUNC = COLOR_4
COLOR_MEDIA = COLOR_6
COLOR_NAV = COLOR_3
COLOR_NUMPAD = COLOR_2
COLOR_WINMAN = COLOR_9

COLOR_ALERT = COLOR_1
COLOR_WARNING = COLOR_5
COLOR_GO = COLOR_6

COLOR_BACK = COLOR_5
COLOR_CLOSE = COLOR_1

COLOR_MAC = 0x555555
COLOR_WINDOWS = 0x00A4EF
COLOR_LINUX = 0x25D366

COLOR_CHROME = 0xDC5044
COLOR_CODE = 0x1774A5
COLOR_FILES = COLOR_2
COLOR_NOTION = COLOR_4
COLOR_PYCHARM = 0xF4F048
COLOR_SLACK = 0x481449
COLOR_SPOTIFY = 0x1ED760
COLOR_SUBLIME_MERGE = 0x00B3B3
COLOR_TERMINAL = COLOR_10
