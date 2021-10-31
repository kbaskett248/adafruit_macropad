"""
Defines the AppPad class. This abstraction layer on top of the hardware
defines the interface used by apps to run.
"""

# pylint: disable=import-error, unused-import, too-few-public-methods
try:
    from typing import Callable, Iterable, List, Optional, Tuple, Union
except ImportError:
    pass

import time

from adafruit_macropad import MacroPad

from apps.base import BaseApp
from event import DoubleTapEvent, EncoderButtonEvent, EncoderEvent, KeyEvent


class DefaultApp(BaseApp):
    """A basic app that just displays a message that no apps were found."""

    name = "NO MACRO FILES FOUND"


class DoubleTapBuffer:
    """
    A class to manage an event buffer for tracking double-tap events.

    When creating the class, you pass it a list of key numbers it should track
    for double-taps. This avoids detecting double-taps for keys with no
    double-tap command.

    The class defines a buffer_event method to add events to the buffer. It
    also defines a drain_buffer event to pull items from the buffer.

    When buffering an event, if the event does not match the pattern of a
    double-tap, or if a double-tap was detected, an exception is raised
    containing the events from the buffer that should be passed on to the app.

    """

    class DrainBufferException(Exception):
        """
        A base exception class that includes a list of buffered events to pass
        back to the app.
        """

        def __init__(self, buffered_events: Iterable[KeyEvent]) -> None:
            super().__init__()
            self.buffered_events = list(buffered_events)

    class UntrackedIndex(DrainBufferException):
        """
        Exception raised when attempting to buffer an event for an untracked
        key.
        """

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
        """Add an event to the buffer.

        Args:
            event (KeyEvent): The event to add to the buffer

        Raises:
            self.UntrackedIndex: Raised when the event you buffer is not
                tracked by this Buffer instance. Includes any items in the
                buffer that should be passed to the app.
            self.DifferentIndexInBuffer: Raised when there are items in the
                buffer with a different key number. The buffer is first
                drained. Then the new event is added to the buffer, and the
                previous events are returned in this exception.
            self.DoubleTapDetected: Raised when the events in the buffer match
                a double-tap state. No event is included in this exception.
            self.UnexpectedState: Raised when the events in the buffer don't
                follow the expected Press, Release, Press, Release pattern.
                The events in the buffer are returned.
        """
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
        """Empty the buffer of events.

        Since we are detecting double-taps, when we drain the buffer we only
        want to return at most a press and release event. So if there are more
        than two events in the buffer, we truncate the list.

        Returns:
            Iterable[KeyEvent]: The events which should be passed on to the app.
        """
        result = self._buffered_events
        if len(result) > 2:
            result = result[:2]

        self._buffered_events = []

        return result


class AppPad:
    """
    An abstraction layer on top of the macropad hardware.

    Instantiating this class initializes the hardware.

    It also provides the following features on top of that hardware:
    - Double-tap detection, so tapping a key twice quickly can trigger a
      second function.
    - Adding timers to trigger callbacks after a set delay.

    """

    DOUBLE_TAP_TIMEOUT = 0.2
    # The delay in seconds to clear the double tap buffer

    DOUBLE_TAP_TIMER_ID = "_DRAIN_DOUBLE_TAP_BUFFER"
    # The ID of the time to clear the double tap buffer

    class AppChange(Exception):
        """Exception raised when an App triggers an App Change."""

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
        """Add an app to the list of apps in this instance.

        Note that this takes a class, and not an instance of the class.

        Args:
            app_class (subclass of BaseApp): The class of app to add.
        """
        if isinstance(self.apps[0], DefaultApp):
            del self.apps[0]
            self.apps.append(app_class(self))
            self.current_app = self.apps[0]
        else:
            self.apps.append(app_class(self))

    def add_timer(self, id_: str, delay: float, callback: Callable):
        """Add a timer to run a callback after a delay.

        Args:
            id_ (str): The id of the timer so it can be updated or deleted
            delay (float): Delay in seconds after which the callback will run
            callback (Callable): A callback taking no arguments to run after
                                 the delay. The callback should return None or
                                 an Iterable of Events.
        """
        execute_time = time.monotonic() + delay
        print(f"Added timer {id_}: {execute_time}")
        self._timers[id_] = (execute_time, callback)

    def delete_timer(self, id_: str):
        """Delete the timer with the given id_ if it exists.

        Args:
            id_ (str): The id of the timer
        """
        if id_ in self._timers:
            del self._timers[id_]

    def execute_ready_timers(self) -> Iterable:
        """Execute the callback for any timers that are past their delay.

        No arguments are passed to the callback.

        Returns:
            Iterable[Event]: If any of the callbacks return a value, those
                             values are assumed to be an Iterable of Events.
                             They are merged together and returned from this
                             method.
        """
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
    def encoder_position(self) -> int:
        """Return the position of the encoder."""
        return self.macropad.encoder

    @property
    def encoder_switch(self) -> bool:
        """Return the state of the encoder switch."""
        self.macropad.encoder_switch_debounced.update()
        return self.macropad.encoder_switch_debounced.pressed

    @property
    def app_index(self) -> int:
        """Return the current app index."""
        return self._app_index

    @app_index.setter
    def app_index(self, value: int):
        """Set the current app index and update the current app."""
        self._app_index = value
        self.current_app = self.apps[self._app_index]

    @property
    def current_app(self) -> BaseApp:
        """Return the current app"""
        return self._current_app

    @current_app.setter
    def current_app(self, new_app: BaseApp):
        """Set a new current app.

        Args:
            new_app (BaseApp): The new App to set

        Raises:
            self.AppChange: If the AppPad is in a running state, an AppChange
                exception is raised to trigger the current App to stop and the
                new App to start.
        """
        self._current_app = new_app
        if self._running:
            raise self.AppChange()

    def check_events(
        self,
    ) -> Tuple[Union[DoubleTapEvent, EncoderButtonEvent, EncoderEvent, KeyEvent], ...]:
        """Check for changes in state and return a tuple of events.

        Also execute any timers that are scheduled to run.

        Returns:
            Tuple[Union[DoubleTapEvent, EncoderButtonEvent, EncoderEvent, KeyEvent], ...]:
                A tuple of Events.
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

    def _handle_double_tap_event(
        self, event: KeyEvent
    ) -> Iterable[Union[DoubleTapEvent, KeyEvent]]:
        """Handle the DoubleTapBuffer and return any events as a result.

        Args:
            event (KeyEvent): The KeyEvent that was triggered.

        Returns:
            Iterable[Union[DoubleTapEvent, KeyEvent]]:
                An iterable of events resulting from buffering the event.
                This may be the events from the buffer or the DoubleTapEvents
                of a completed DoubleTap.
        """
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
        """Create a new DoubleTapBuffer tracking the specified key numbers.

        Args:
            indices (Iterable[int]): The key numbers to track.
        """
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
