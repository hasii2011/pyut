
from org.pyut.general.Singleton import Singleton


class BaseSubPreference(Singleton):

    def init(self, *args, **kwds):

        for name, value in kwds.items():
            protectedName: str = f'_{name}'
            if not hasattr(self, protectedName):
                raise TypeError(f"Unexpected keyword argument {protectedName}")
            setattr(self, protectedName, value)
