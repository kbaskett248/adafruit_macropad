"""
An App program for Adafruit MACROPAD. This was modified from the original
Adafruit Macropad Hotkeys code (https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/main/Macropad_Hotkeys).
It enables you to more easily create complex layouts and has other advanced 
features, including double-tap support.
"""
from apps.work import Work, VSCode
from utils.app_pad import AppPad
from utils.commands import AppSwitchException
from utils.constants import OS_MAC, OS_SETTING, PREVIOUS_APP_SETTING
from utils.config import conf

def get_settings():
    app_settings = {
        OS_SETTING: OS_MAC,
        PREVIOUS_APP_SETTING: []
    }

    for k, v in conf.__dict__.items():
        app_settings[k] = v
    
    return app_settings

class SettingsAppPad(AppPad):
    def main_loop_hook(self):
        if conf.reload_config():
            raise AppSwitchException(None)

app_pad = SettingsAppPad()

def get_app():
    apps = {
        "code": VSCode
    }

    PRIMARY_APP = Work

    if process := get_settings().get("host", {}).get("process"):
        print(process.lower(), apps.get(process.lower(), PRIMARY_APP) )
        return apps.get(process.lower(), PRIMARY_APP) 
    return PRIMARY_APP

current_app = get_app()(app_pad, get_settings())
 
while True:
    try: 
        current_app.run()
    except AppSwitchException as err:
        current_app = err.app if err.app else get_app()(app_pad, get_settings())
        print("Changing to app:", current_app.name)
