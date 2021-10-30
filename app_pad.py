# pylint: disable=import-error, unused-import, too-few-public-methods
try:
    from typing import Callable, Iterable, List, Optional, Tuple
except ImportError:
    pass

import time

from adafruit_macropad import MacroPad

from apps.base import BaseApp
from commands import Sequence
from event import DoubleTapEvent, EncoderButtonEvent, EncoderEvent, KeyEvent


class DefaultApp(BaseApp):
    name = "NO MACRO FILES FOUND"


class DoubleTapBuffer:
    class DrainBufferException(Exception):
        def __init__(self, buffered_events: Iterable[KeyEvent]) -> None:
            super().__init__()
            self.buffered_events = list(buffered_events)

    class UntrackedIndex(DrainBufferException):
        """Exception raised when attempting to buffer an event for an untracked key."""

    class DifferentIndexInBuffer(DrainBufferException):
        """
        Exception raised when attempting to buffer an event for a tracked key
        when there are already events in the buffer for another tracked key.
        """

    class UnexpectedState(DrainBufferException):
        """
        Exception raised when attempting to buffer an event for a tracked key
        when the pressed state of the key does not match the expected state.
        """

    class DoubleTapDetected(Exception):
        """
        Exception raised when attempting to buffer an event and that event
        completes a double tap.
        """

    def __init__(self, tracked_indices: Iterable[int]) -> None:
        self._tracked_indices = set(tracked_indices)
        self._buffered_events: List[KeyEvent] = []

    def buffer_event(self, event: KeyEvent):
        if event.number not in self._tracked_indices:
            raise self.UntrackedIndex(self.drain_buffer())

        if not self._buffered_events:
            self._buffered_events.append(event)
            return

        if any(
            buffered_event.number != event.number
            for buffered_event in self._buffered_events
        ):
            buffered_events = self.drain_buffer()
            self._buffered_events.append(event)
            raise self.DifferentIndexInBuffer(buffered_events)

        buffered_states = tuple(
            buffered_event.pressed for buffered_event in self._buffered_events
        )
        if buffered_states == (True, False, True) and not event.pressed:
            raise self.DoubleTapDetected()
        elif buffered_states == (True, False) and event.pressed:
            self._buffered_events.append(event)
        elif buffered_states == (True,) and not event.pressed:
            self._buffered_events.append(event)
        else:
            raise self.UnexpectedState(self.drain_buffer())

    def drain_buffer(self) -> Iterable[KeyEvent]:
        result = self._buffered_events
        if len(result) > 2:
            result = result[:2]

        self._buffered_events = []

        return result


class AppPad:
    DOUBLE_TAP_TIMEOUT = 0.2
    DOUBLE_TAP_TIMER_ID = "_DRAIN_DOUBLE_TAP_BUFFER"

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

        self._timers = dict()

        self._double_tap_buffer: Optional[DoubleTapBuffer] = None

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

    def add_timer(self, id_: str, delay: float, callback: Callable):
        execute_time = time.monotonic() + delay
        print(f"Added timer {id_}: {execute_time}")
        self._timers[id_] = (execute_time, callback)

    def delete_timer(self, id_: str):
        if id_ in self._timers:
            del self._timers[id_]

    def execute_ready_timers(self) -> Iterable:
        finished_timers = []
        current_time = time.monotonic()

        finished_timers = [
            (id_, timer[1])
            for id_, timer in self._timers.items()
            if current_time >= timer[0]
        ]

        results = []
        for id_, callback in finished_timers:
            print(f"Executing timer {id_}")
            self._timers.pop(id_)
            callback_result = callback()
            try:
                results.extend(callback_result)
            except Exception:
                pass

        return results

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
            double_tap_events = self._handle_double_tap_event(
                KeyEvent(number=key_event.key_number, pressed=key_event.pressed)
            )
            events.extend(double_tap_events)

        events.extend(self.execute_ready_timers())

        return tuple(events)

    def _handle_double_tap_event(self, event: KeyEvent) -> Iterable:
        if self._double_tap_buffer is None:
            return (event,)

        try:
            self._double_tap_buffer.buffer_event(event)
        except self._double_tap_buffer.DrainBufferException as err:
            self.delete_timer(self.DOUBLE_TAP_TIMER_ID)
            result = list(err.buffered_events)
            result.append(event)
            return result
        except self._double_tap_buffer.DoubleTapDetected:
            self.delete_timer(self.DOUBLE_TAP_TIMER_ID)
            return (
                DoubleTapEvent(number=event.number, pressed=True),
                DoubleTapEvent(number=event.number, pressed=False),
            )
        else:
            self.add_timer(
                self.DOUBLE_TAP_TIMER_ID,
                self.DOUBLE_TAP_TIMEOUT,
                self._double_tap_buffer.drain_buffer,
            )
            return tuple()

    def track_double_taps(self, indices: Iterable[int]):
        print("Tracking double taps: ", indices)
        if indices:
            self._double_tap_buffer = DoubleTapBuffer(indices)
        else:
            self._double_tap_buffer = None

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