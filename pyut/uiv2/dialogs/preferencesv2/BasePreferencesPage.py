
from abc import abstractmethod
from abc import ABCMeta

from wx import Window

from wx.lib.sized_controls import SizedPanel

from pyut.preferences.PyutPreferencesV2 import PyutPreferencesV2


class MyMetaBasePreferencesPage(ABCMeta, type(SizedPanel)):        # type: ignore
    """
    I have no idea why this works:
    https://stackoverflow.com/questions/66591752/metaclass-conflict-when-trying-to-create-a-python-abstract-class-that-also-subcl
    """
    pass


class BasePreferencesPage(SizedPanel):

    __metaclass__ = MyMetaBasePreferencesPage

    def __init__(self, parent: Window):

        super().__init__(parent)

        self._preferences: PyutPreferencesV2 = PyutPreferencesV2()

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def _setControlValues(self):
        pass

    def _fixPanelSize(self, panel: SizedPanel):
        """
        Use this method or a dialog will not get resized correctly
        A little trick to make sure that the sizer cannot be resized to
        less screen space than the controls needs;

        Args:
            panel:
        """
        panel.Fit()
        panel.SetMinSize(panel.GetSize())
