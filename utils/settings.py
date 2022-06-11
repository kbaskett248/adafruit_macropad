try:
    from typing import TYPE_CHECKING, Any, Dict, Optional
except ImportError:
    TYPE_CHECKING = False

from utils.constants import EMPTY_VALUE

if TYPE_CHECKING:
    from utils.apps.base import BaseApp


class BaseSettings:
    additional_settings: Dict[str, Any]
    registered_apps: Dict[str, BaseApp]

    def __init__(self, **kwargs):
        self.additional_settings = {}
        self.registered_apps = {}
        for key, value in kwargs.items():
            self[key] = value

    def __getitem__(self, key: str) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            return self.additional_settings[key]

    def __setitem__(self, key, value) -> None:
        try:
            setattr(self, key, value)
        except:
            self.additional_settings[key] = value

    def get(self, setting: str, default=EMPTY_VALUE) -> Any:
        try:
            return self[setting]
        except KeyError as err:
            if default is EMPTY_VALUE:
                raise err
            return default

    def register_app(self, app: BaseApp):
        self.registered_apps[app.name] = app

    def get_app(self, name: str) -> Optional[BaseApp]:
        return self.registered_apps.get(name, None)
