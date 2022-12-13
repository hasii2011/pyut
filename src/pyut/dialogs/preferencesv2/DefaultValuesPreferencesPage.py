
from wx import StockPreferencesPage
from wx import Window

from pyut.dialogs.preferences.ValuePreferencesBook import ValuePreferencesBook


class DefaultValuesPreferencesPage(StockPreferencesPage):

    def __init__(self):
        super().__init__(kind=StockPreferencesPage.Kind_General)

    def CreateWindow(self, parent) -> Window:
        return ValuePreferencesBook(parent=parent)

    def GetName(self) -> str:
        return 'Default Values'
