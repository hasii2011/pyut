from wx import StockPreferencesPage
from wx import Window

from pyut.dialogs.preferences.MiscellaneousPreferences import MiscellaneousPreferences


class MiscellaneousPreferencesPage(StockPreferencesPage):

    def __init__(self):
        super().__init__(kind=StockPreferencesPage.Kind_General)

    def CreateWindow(self, parent) -> Window:
        return MiscellaneousPreferences(parent=parent)

    def GetName(self) -> str:
        return 'Miscellaneous'