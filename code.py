"""
An App program for Adafruit MACROPAD. This was modified from the original
Adafruit Macropad Hotkeys code (https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/main/Macropad_Hotkeys).
It enables you to more easily create complex layouts and has other advanced
features, including double-tap support.
"""

from utils.app_pad import AppPad
from utils.commands import AppSwitchException

try:
    from user import DEFAULT_APP
except ImportError:
    from default_settings import DEFAULT_APP

app_pad = AppPad()
current_app = DEFAULT_APP(app_pad)

try:
    while True:
        try:
            print(f"Current App = {current_app}")
            current_app.run()
        except AppSwitchException as err:
            current_app = err.app
except Exception as e:
    print("Exception in event_stream, importing keyboard and releasing all keys.")

    from adafruit_hid.keyboard import Keyboard
    from usb_hid import devices

    Keyboard(devices).release_all()
    raise e
