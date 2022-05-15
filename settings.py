from utils.constants import OS_WINDOWS
from apps.home import HomeApp


class BaseSettings:
    host_os = OS_WINDOWS
    defult_app = HomeApp
    pixels_disabled = False 
    previous_app_settings = []

    # a place for apps to keep their settings
    _app_settings = {}
    