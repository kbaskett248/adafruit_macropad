"""
A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), load up just the ones you're likely to
use. Plug into computer's USB port, use dial to select an application macro
set, press MACROPAD keys to send key sequences and other USB protocols.
"""

# pylint: disable=import-error, unused-import, too-few-public-methods
from adafruit_macropad import MacroPad

from app import BaseApp
from event import EncoderButtonEvent, EncoderEvent, KeyEvent

# CONFIGURABLES ------------------------
MACRO_FOLDER = "/macros"


class DefaultApp(BaseApp):
    name = "NO MACRO FILES FOUND"


# CLASSES AND FUNCTIONS ----------------
class AppPad:
    def __init__(self):
        self.macropad = self._init_macropad()

        self._last_encoder_position = self.encoder_position
        self._last_encoder_switch = self.encoder_switch

        self.apps = [DefaultApp(self)]
        self.app_index = 0
        self.current_app = self.apps[self.app_index]

    @classmethod
    def _init_macropad(cls):
        """Initialize the macropad component."""
        macropad = MacroPad()
        macropad.display.auto_refresh = False
        macropad.pixels.auto_write = False

        return macropad

    def add_app(self, app_class):
        if isinstance(self.apps[0], DefaultApp):
            del self.apps[0]
            self.apps.append(app_class(self))
            self.current_app = self.apps[0]
        else:
            self.apps.append(app_class(self))

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
        self._current_app.on_focus()

    def check_events(self):
        """Check for changes in state and return a tuple of events.

        Returns:
            Tuple[Union[EncoderButtonEvent, EncoderEvent, KeyEvent]]: A tuple of Events.
        """
        events = []

        position = self.encoder_position
        if position != self._last_encoder_position:
            events.append(
                EncoderEvent(
                    position=position,
                    previous_position=self._last_encoder_position,
                )
            )
            self._last_encoder_position = position

        encoder_switch = self.encoder_switch
        if encoder_switch != self._last_encoder_switch:
            events.append(EncoderButtonEvent(pressed=encoder_switch))

        key_event = self.macropad.keys.events.get()
        if key_event:
            events.append(
                KeyEvent(number=key_event.key_number, pressed=key_event.pressed)
            )

        return tuple(events)

    def run(self):
        """The main event loop when there is an active app."""
        while True:
            for event in self.check_events():
                if isinstance(event, EncoderEvent):
                    self.app_index = event.position % len(self.apps)
                    self.current_app = self.apps[self.app_index]
                elif isinstance(event, EncoderButtonEvent):
                    pass
                elif isinstance(event, KeyEvent):
                    if event.pressed:
                        self.current_app.key_press(event.number)
                    else:
                        self.current_app.key_release(event.number)


app_pad = AppPad()
for app in BaseApp.load_apps(MACRO_FOLDER):
    app_pad.add_app(app)
app_pad.run()
