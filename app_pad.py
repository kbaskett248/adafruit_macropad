# pylint: disable=import-error, unused-import, too-few-public-methods
from adafruit_macropad import MacroPad

from apps.base import BaseApp
from event import EncoderButtonEvent, EncoderEvent, KeyEvent


class DefaultApp(BaseApp):
    name = "NO MACRO FILES FOUND"


class AppPad:
    class AppChange(Exception):
        """Exception raised when an App triggers an App Change."""

        pass

    def __init__(self):
        self.macropad = self._init_macropad()

        self._last_encoder_position = self.encoder_position
        self._last_encoder_switch = self.encoder_switch
        self._running = False

        self.apps = [DefaultApp(self)]
        self._app_index = 0
        self.app_index = 0

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
    def app_index(self):
        return self._app_index

    @app_index.setter
    def app_index(self, value):
        self._app_index = value
        self.current_app = self.apps[self._app_index]

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
        if self._running:
            raise self.AppChange()

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
        """The main event loop.

        Run the current app until an AppChange exception is raised.
        Then run the new app.
        """
        self._running = True

        while True:
            try:
                self.current_app.run()
            except self.AppChange:
                pass