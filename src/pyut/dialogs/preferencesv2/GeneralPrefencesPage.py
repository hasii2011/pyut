
from wx import StockPreferencesPage
from wx import Window

from pyut.dialogs.preferences.GeneralPreferencesPanel import GeneralPreferencesPanel


class GeneralPreferencesPage(StockPreferencesPage):
    def __init__(self):
        super().__init__(kind=StockPreferencesPage.Kind_General)

    def CreateWindow(self, parent) -> Window:

        return GeneralPreferencesPanel(parent=parent)