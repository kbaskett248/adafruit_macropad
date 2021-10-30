from collections import namedtuple


EncoderButtonEvent = namedtuple("EncoderButtonEvent", ("pressed",))


EncoderEvent = namedtuple("EncoderEvent", ("position", "previous_position"))


KeyEvent = namedtuple("KeyEvent", ("number", "pressed"))

DoubleTapEvent = namedtuple("DoubleTapEvent", ("number", "pressed"))
