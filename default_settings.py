from apps.home import HomeApp
from utils.constants import OS_SETTING, OS_WINDOWS, PREVIOUS_APP_SETTING

app_settings = {
    OS_SETTING: OS_WINDOWS,
    PREVIOUS_APP_SETTING: [],
}

DEFAULT_APP = lambda app_pad: HomeApp(app_pad, app_settings)
