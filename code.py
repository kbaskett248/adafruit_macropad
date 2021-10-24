"""
A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), load up just the ones you're likely to
use. Plug into computer's USB port, use dial to select an application macro
set, press MACROPAD keys to send key sequences and other USB protocols.
"""

from apps.base import BaseApp
from app_pad import AppPad


MACRO_FOLDER = "/macros"


app_pad = AppPad()
for app in BaseApp.load_apps(MACRO_FOLDER):
    app_pad.add_app(app)
app_pad.run()
