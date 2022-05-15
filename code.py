"""
An App program for Adafruit MACROPAD. This was modified from the original
Adafruit Macropad Hotkeys code (https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/main/Macropad_Hotkeys).
It enables you to more easily create complex layouts and has other advanced
features, including double-tap support.
"""

from apps.home import HomeApp
from utils.app_pad import AppPad
from utils.commands import AppSwitchException

try:
    from user import Settings
except ImportError as e:
    from settings import BaseSettings as Settings

settings = Settings()

app_pad = AppPad()
current_app = settings.default_app(app_pad, settings)

while True: 
    try:
        print(f"Current App = {current_app}")
        current_app.run()
    except AppSwitchException as err:
        current_app = err.app
