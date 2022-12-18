
from logging import Logger
from logging import getLogger

from wx import EVT_TEXT
from wx import ID_ANY

from wx import CommandEvent
from wx import StaticText
from wx import StockPreferencesPage
from wx import TextCtrl
from wx import Window

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedPanel
from pyut.dialogs.preferencesv2.BasePreferencesPage import BasePreferencesPage


class MiscellaneousPreferencesPage(BasePreferencesPage):

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        super().__init__(kind=StockPreferencesPage.Kind_General)

        self._pdfFileNameWxId:   int = wxNewIdRef()
        self._imageFileNameWxId: int = wxNewIdRef()
        self._fastEditNameWxId:  int = wxNewIdRef()

    def CreateWindow(self, parent) -> Window:

        panel: SizedPanel = SizedPanel(parent)
        panel.SetSizerType('form')

        StaticText(panel, ID_ANY, 'PDF Filename:')
        pdfFileName: TextCtrl = TextCtrl(panel, self._pdfFileNameWxId, self._preferences.pdfExportFileName)
        pdfFileName.SetSizerProps(expand=True)

        StaticText(panel, ID_ANY, 'Image Filename:')
        imageFileName: TextCtrl = TextCtrl(panel, self._imageFileNameWxId, self._preferences.wxImageFileName)
        imageFileName.SetSizerProps(expand=True)

        StaticText(panel, ID_ANY, 'FastEdit Editor Name:')
        fastEditorName: TextCtrl = TextCtrl(panel,  self._fastEditNameWxId, self._preferences.editor)
        fastEditorName.SetSizerProps(expand=True)

        parent.Bind(EVT_TEXT, self._onNameChange, id=self._pdfFileNameWxId)
        parent.Bind(EVT_TEXT, self._onNameChange, id=self._imageFileNameWxId)
        parent.Bind(EVT_TEXT, self._onNameChange, id=self._fastEditNameWxId)
        return panel

    def GetName(self) -> str:
        return 'Miscellaneous'

    def _setControlValues(self):
        pass

    def _onNameChange(self, event: CommandEvent):

        eventID:  int = event.GetId()
        newValue: str = event.GetString()

        match eventID:
            case  self._pdfFileNameWxId:
                self._preferences.pdfExportFileName = newValue
            case self._imageFileNameWxId:
                self._preferences.wxImageFileName = newValue
            case self._fastEditNameWxId:
                self._preferences.editor = newValue
            case _:
                self.logger.error(f'Unknown event id')

