import time
import json
import supervisor

import usb_cdc
from usb_hid import devices
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

keyboard = Keyboard(devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
 

def get_serial_data(is_json: bool = True):
    # if supervisor.runtime.serial_bytes_available:
    #     value = input().strip()
    #     return value if not is_json else json.loads(value)
    if usb_cdc.data.in_waiting > 0:
        data = usb_cdc.data.readline()
        if len(data) > 0:
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