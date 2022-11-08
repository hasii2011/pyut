
from typing import cast

from configparser import ConfigParser

from pyut.general.Singleton import Singleton


class BaseSubPreference(Singleton):

    def init(self, *args, **kwds):

        self._config: ConfigParser = cast(ConfigParser, None)

        for name, value in kwds.items():
            protectedName: str = f'_{name}'
            if not hasattr(self, protectedName):
                raise TypeError(f"Unexpected keyword argument {protectedName}")
            setattr(self, protectedName, value)

    @property
    def configParser(self) -> ConfigParser:
        return self._config

    @configParser.setter
    def configParser(self, newValue: ConfigParser):
        self._config = newValue
