
from typing import cast

from wx import App
from wx import Button
from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_BUTTON
from wx import ID_ANY
from wx import PreferencesEditor
from wx import StaticText
from wx import StockPreferencesPage
from wx import Window

from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedFrame


class DemoPreferencesPage(StockPreferencesPage):

    def __init__(self):
        super().__init__(kind=StockPreferencesPage.Kind_General)

    def CreateWindow(self, parent) -> Window:

        sizedPanel: SizedPanel = SizedPanel(parent)
        # noinspection PyUnusedLocal
        label:      StaticText = StaticText(parent=sizedPanel, id=ID_ANY, label="Preferences Go Here")

        return sizedPanel

    def GetName(self) -> str:
        return 'Demo Preferences'


class MainFrame(SizedFrame):
    def __init__(self):
        super().__init__(parent=None, id=ID_ANY, title="Show da' Anomaly", size=(300, 200), style=DEFAULT_FRAME_STYLE)

        self._preferencesEditor: PreferencesEditor = cast(PreferencesEditor, None)
        sizedPanel:   SizedPanel = self.GetContentsPane()
        showMeButton: Button     = Button(parent=sizedPanel, label='Press Me')

        self.Bind(EVT_BUTTON, self._onShowMe, showMeButton)
        self.Fit()

    # noinspection PyUnusedLocal
    def _onShowMe(self, event: CommandEvent):
        print('I was pressed')
        preferencesEditor: PreferencesEditor = PreferencesEditor()
        preferencesEditor.AddPage(DemoPreferencesPage())

        preferencesEditor.Show(self)

        print('Hasta La Vista')
        self._preferencesEditor = preferencesEditor


class PreferencesEditorDemo(App):

    def OnInit(self):

        self._frame: MainFrame = MainFrame()

        self._frame.Show()
        return True


testApp: App = PreferencesEditorDemo(redirect=False)
testApp.MainLoop()
