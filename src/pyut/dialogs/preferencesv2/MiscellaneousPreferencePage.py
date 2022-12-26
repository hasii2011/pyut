
from logging import Logger
from logging import getLogger

from wx import EVT_TEXT
from wx import ID_ANY

from wx import CommandEvent
from wx import StaticText
from wx import TextCtrl
from wx import Window

from wx import NewIdRef as wxNewIdRef

from pyut.dialogs.preferencesv2.BasePreferencesPage import BasePreferencesPage


class MiscellaneousPreferencesPage(BasePreferencesPage):

    def __init__(self, parent: Window):
        self.logger: Logger = getLogger(__name__)

        super().__init__(parent)
        self.SetSizerType('form')
        self._pdfFileNameWxId:   int = wxNewIdRef()
        self._imageFileNameWxId: int = wxNewIdRef()
        self._fastEditNameWxId:  int = wxNewIdRef()

        self._createWindow(parent)

    def _createWindow(self, parent):

        StaticText(self, ID_ANY, 'PDF Filename:')
        TextCtrl(self, id=self._pdfFileNameWxId, value=self._preferences.pdfExportFileName, size=(100,25))

        StaticText(self, ID_ANY, 'Image Filename:')
        TextCtrl(self, self._imageFileNameWxId, self._preferences.wxImageFileName, size=(100,25))

        StaticText(self, ID_ANY, 'FastEdit Editor Name:')
        TextCtrl(self,  self._fastEditNameWxId, self._preferences.editor, size=(100,25))

        parent.Bind(EVT_TEXT, self._onNameChange, id=self._pdfFileNameWxId)
        parent.Bind(EVT_TEXT, self._onNameChange, id=self._imageFileNameWxId)
        parent.Bind(EVT_TEXT, self._onNameChange, id=self._fastEditNameWxId)

    @property
    def name(self) -> str:
        return 'Plugins'

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

