"""
An App program for Adafruit MACROPAD. This was modified from the original
Adafruit Macropad Hotkeys code (https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/main/Macropad_Hotkeys).
It enables you to more easily create complex layouts and has other advanced 
features, including double-tap support.
"""

from apps.home import HomeApp
from app_pad import AppPad


app_pad = AppPad()
app_pad.add_app(HomeApp)
app_pad.run()
