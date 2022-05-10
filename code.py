"""
An App program for Adafruit MACROPAD. This was modified from the original
Adafruit Macropad Hotkeys code (https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/main/Macropad_Hotkeys).
It enables you to more easily create complex layouts and has other advanced 
features, including double-tap support.
"""
try:
    from apps_private.default import DEFAULT_APP, SELECT_APPS
except Exception:
    from apps.home import HomeApp

    DEFAULT_APP = HomeApp
    SELECT_APPS = {}

from utils.app_pad import AppPad
from utils.commands import AppSwitchException
from utils.config import conf
from utils.constants import OS_WINDOWS, OS_SETTING, PREVIOUS_APP_SETTING


class SettingsAppPad(AppPad):
    def main_loop_hook(self):
        if conf.reload_config():
            raise AppSwitchException(None)


def get_settings():
    app_settings = {OS_SETTING: OS_WINDOWS, PREVIOUS_APP_SETTING: []}

    for k, v in conf.__dict__.items():
        app_settings[k] = v

    return app_settings


def get_app():
    if process := get_settings().get("host", {}).get("process"):
        print(process.lower(), SELECT_APPS.get(process.lower(), DEFAULT_APP))
        return SELECT_APPS.get(process.lower(), DEFAULT_APP)
    return DEFAULT_APP


if __name__ == "__main__":
    try:
        APP_PAD = SettingsAppPad()
        current_app = get_app()(APP_PAD, get_settings())

        while True:
            try:
                print(f"Current App = {current_app}")
                current_app.run()
            except AppSwitchException as err:
                current_app = err.app if err.app else get_app()(APP_PAD, get_settings())
                print("Changing to app:", current_app.name)

    except Exception as e:
        print(f"❌ Exception in event_stream: {e}")
        print("❌ Importing keyboard and releasing all keys")

        from usb_hid import devices
        from adafruit_hid.keyboard import Keyboard
        from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

        keyboard = Keyboard(devices)
        keyboard_layout = KeyboardLayoutUS(keyboard)
        keyboard.release_all()

        print("❌ Keys released")
        print("❌ Re-raiseing exception")
        raise e
