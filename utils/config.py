from adafruit_hid.keycode import Keycode
import usb_hid
from adafruit_hid.keycode import Keycode
import supervisor
import time
import json
import rtc


from utils.serial_tools import trigger_and_get, get_serial_data
from utils.constants import OS_WINDOWS, OS_SETTING, PREVIOUS_APP_SETTING


class Config:
    KEYCODE_NUMBER_MAPPING = {
        0: Keycode.ZERO,
        1: Keycode.ONE,
        2: Keycode.TWO,
        3: Keycode.THREE,
        4: Keycode.FOUR,
        5: Keycode.FIVE,
        6: Keycode.SIX,
        7: Keycode.SEVEN,
        8: Keycode.EIGHT,
        9: Keycode.NINE,
    }
    times = 0

    def __init__(self) -> None:
        self.OS_SETTING = OS_WINDOWS
        self.PREVIOUS_APP_SETTING = []

        self.pinned_apps = {
            "chrome": "1",
            "files": "2",
            "phpstorm": "3",
            "intellij": "4",
            "vscode": "5",
            "postman": "6",
            "slack": "7",
            "terminal": "8",
        }
        self.email = "mtyemail@email.com"
        self.host = {}

        self.reload_config(False)

    def reload_config(self, check_only=True):
        try:
            if check_only:
                if data := get_serial_data():
                    print(data)
                    self.host = data
                    return True
            else:
                self.host = trigger_and_get()
                # if timestamp := self.host.get('timestamp'):
                #     class RTC(object):
                #         @property
                #         def datetime(self):
                #             return time.struct_time((2018, 3, 17, 21, 1, 47, 0, 0, 0))

                #     r = RTC()
                #     rtc.set_time_source(r)
                #     # rtc.RTC().calibration = 9
                #     # rtc.RTC().datetime = time.localtime(int(timestamp))
                return True
        except Exception as e:
            print(str(e))
            return False


conf = Config()
