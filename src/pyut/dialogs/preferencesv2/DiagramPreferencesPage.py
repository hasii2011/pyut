from wx import StockPreferencesPage
from wx import Window

from pyut.dialogs.preferences.BackgroundPreferences import BackgroundPreferences


class DiagramPreferencesPage(StockPreferencesPage):

    def __init__(self):
        super().__init__(kind=StockPreferencesPage.Kind_General)

    def CreateWindow(self, parent) -> Window:
        return BackgroundPreferences(parent=parent)

    def GetName(self) -> str:
        return 'Diagram'