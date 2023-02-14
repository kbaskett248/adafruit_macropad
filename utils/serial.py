import json

import supervisor
import usb_cdc

# from adafruit_hid.keyboard import Keyboard
# from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
# from usb_hid import devices

# keyboard = Keyboard(devices)
# keyboard_layout = KeyboardLayoutUS(keyboard)


def get_serial_data():
    if not usb_cdc.data:
        return None

    data = None
    if usb_cdc.data.in_waiting > 0:
        data = usb_cdc.data.readline()

    if not data:
        return None

    if len(data) > 0:
        usb_cdc.data.reset_input_buffer()
        return json.loads(data)

    return None


def clear_serial():
    while supervisor.runtime.serial_bytes_available:
        input()
