"""
An App program for Adafruit MACROPAD. This was modified from the original
Adafruit Macropad Hotkeys code (https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/main/Macropad_Hotkeys).
It enables you to more easily create complex layouts and has other advanced 
features, including double-tap support.
"""

from apps.home import HomeApp
from utils.app_pad import AppPad
from utils.commands import AppSwitchException
from utils.constants import OS_MAC, OS_SETTING, PREVIOUS_APP_SETTING


app_settings = {
    OS_SETTING: OS_MAC,
    PREVIOUS_APP_SETTING: [], 
}

app_pad = AppPad()
current_app = HomeApp(app_pad, app_settings)

while True:
    try:
        print(f"Current App = {current_app}")
        current_app.run()
    except AppSwitchException as err:
        current_app = err.app
