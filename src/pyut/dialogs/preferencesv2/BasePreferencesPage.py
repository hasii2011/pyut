
from abc import abstractmethod
from abc import ABCMeta

from wx import StockPreferencesPage
from wx.lib.sized_controls import SizedPanel

from pyut.preferences.PyutPreferences import PyutPreferences

class MyMetaBasePreferencesPage(ABCMeta, type(StockPreferencesPage)):        # type: ignore
    """
    I have know idea why this works:
    https://stackoverflow.com/questions/66591752/metaclass-conflict-when-trying-to-create-a-python-abstract-class-that-also-subcl
    """
    pass

class BasePreferencesPage(StockPreferencesPage):

    __metaclass__ = MyMetaBasePreferencesPage

    def __init__(self, kind=StockPreferencesPage.Kind_General):

        super().__init__(kind)

        self._preferences: PyutPreferences = PyutPreferences()

    @abstractmethod
    def GetName(self) -> str:
        pass

    @abstractmethod
    def _setControlValues(self):
        pass
    def _fixPanelSize(self, panel: SizedPanel):
        """
        Do the following or does not get resized correctly
        A little trick to make sure that the sizer cannot be resized to
        less screen space than the controls need

        Args:
            panel:
        """
        panel.Fit()
        panel.SetMinSize(panel.GetSize())
