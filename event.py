"""Define the events that the AppPad generates."""

from collections import namedtuple


# Event indicating the Encoder Button was pressed or released.
EncoderButtonEvent = namedtuple("EncoderButtonEvent", ("pressed",))


# Event indicating the Encoder was rotated.
EncoderEvent = namedtuple("EncoderEvent", ("position", "previous_position"))


# Event indicating a key was pressed or released.
KeyEvent = namedtuple("KeyEvent", ("number", "pressed"))


# Event indicating a key was tapped twice quickly.
DoubleTapEvent = namedtuple("DoubleTapEvent", ("number", "pressed"))
