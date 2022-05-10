import json
import time

import supervisor
import usb_cdc
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from usb_hid import devices

keyboard = Keyboard(devices)
keyboard_layout = KeyboardLayoutUS(keyboard)


def get_serial_data(is_json: bool = True):
    if usb_cdc.data.in_waiting > 0:
        data = usb_cdc.data.readline()
        if len(data) > 0:
            usb_cdc.data.reset_input_buffer()
            return json.loads(data)
    return {}


def trigger_serial_script():
    keyboard.press(Keycode.F13)
    keyboard.release_all()


def clear_serial():
    while supervisor.runtime.serial_bytes_available:
        input()


def trigger_and_get():
    trigger_serial_script()
    time.sleep(0.5)
    return get_serial_data()
