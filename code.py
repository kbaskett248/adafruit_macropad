"""
A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), load up just the ones you're likely to
use. Plug into computer's USB port, use dial to select an application macro
set, press MACROPAD keys to send key sequences and other USB protocols.
"""

# pylint: disable=import-error, unused-import, too-few-public-methods

from adafruit_macropad import MacroPad

from app import BaseApp

# CONFIGURABLES ------------------------
MACRO_FOLDER = "/macros"


# CLASSES AND FUNCTIONS ----------------
class HotkeyPad:
    def __init__(self, apps):
        """
        Args:
            apps (List[BaseApp]): List of apps to display
        """
        self.apps = apps
        self.macropad = self._init_macropad()

        self.last_encoder_position = self.encoder_position
        self.last_encoder_switch = self.encoder_switch

        self.app_index = 0
        self.current_app = self.apps[self.app_index]

    @classmethod
    def _init_macropad(cls):
        """Initialize the macropad component."""
        macropad = MacroPad()
        macropad.display.auto_refresh = False
        macropad.pixels.auto_write = False

        return macropad

    @property
    def encoder_position(self):
        return self.macropad.encoder

    @property
    def encoder_switch(self):
        self.macropad.encoder_switch_debounced.update()
        return self.macropad.encoder_switch_debounced.pressed

    @property
    def current_app(self):
        return self._current_app

    @current_app.setter
    def current_app(self, new_app):
        """Set a new current app.

        Update the display, set the keyboard pixels, and reset the macropad
        state.

        Args:
            new_app (App): The new App to set
        """
        self._current_app = new_app
        self._current_app.on_focus(self.macropad)

    def run(self):
        """The main event loop when there is an active app."""
        while True:
            # Read encoder position. If it's changed, switch apps.
            position = self.encoder_position
            if position != self.last_encoder_position:
                self.last_encoder_position = position
                self.app_index = position % len(self.apps)
                self.current_app = self.apps[self.app_index]

            pressed_key = self.get_pressed_key()
            if pressed_key is None:
                continue

            key_number, pressed = pressed_key

            if pressed:
                self.current_app.key_press(self.macropad, key_number)
            else:
                self.current_app.key_release(self.macropad, key_number)

    def get_pressed_key(self):
        # Handle encoder button. If state has changed, and if there's a
        # corresponding macro, set up variables to act on this just like
        # the keypad keys, as if it were a 13th key/macro.
        encoder_switch = self.encoder_switch
        if encoder_switch != self.last_encoder_switch:
            self.last_encoder_switch = encoder_switch
            if len(self.current_app) < 13:
                return None
            return None

        event = self.macropad.keys.events.get()
        if not event:
            return None

        return (event.key_number, event.pressed)


class DefaultApp(BaseApp):
    name = "NO MACRO FILES FOUND"


apps = BaseApp.load_apps(MACRO_FOLDER)
if not apps:
    apps = [DefaultApp()]
macropad = HotkeyPad(apps)
macropad.run()
