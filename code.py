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
        for i, labeled_key in enumerate(self.current_app):
            try:
                # Key in use, set label + LED color
                self.macropad.pixels[i] = labeled_key.color
            except AttributeError:  # Key not in use, no label or LED
                self.macropad.pixels[i] = 0

        self.macropad.keyboard.release_all()
        self.macropad.consumer_control.release()
        self.macropad.mouse.release_all()
        self.macropad.stop_tone()
        self.macropad.pixels.show()
        self.macropad.display.show(self._current_app.display_group)
        self.macropad.display.refresh()

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

            # If code reaches here, a key or the encoder button WAS pressed/released
            # and there IS a corresponding macro available for it...other situations
            # are avoided by 'continue' statements above which resume the loop.

            key, key_number, pressed = pressed_key

            if pressed:
                self.macropad.pixels[key_number] = 0xFFFFFF
                self.macropad.pixels.show()
                key.press(self.macropad)
            else:
                # Release any still-pressed keys, consumer codes, mouse buttons
                # Keys and mouse buttons are individually released this way (rather
                # than release_all()) because pad supports multi-key rollover, e.g.
                # could have a meta key or right-mouse held down by one macro and
                # press/release keys/buttons with others. Navigate popups, etc.
                key.release(self.macropad)
                self.macropad.consumer_control.release()

                self.macropad.pixels[key_number] = key.color
                self.macropad.pixels.show()

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

        key_number = event.key_number
        if key_number >= len(self.current_app):
            return None

        key = self.current_app[key_number + 1]
        if key is None:
            return None

        pressed = event.pressed
        return (key, key_number, pressed)


class DefaultApp(BaseApp):
    name = "NO MACRO FILES FOUND"


apps = BaseApp.load_apps(MACRO_FOLDER)
if not apps:
    apps = [DefaultApp()]
macropad = HotkeyPad(apps)
macropad.run()
