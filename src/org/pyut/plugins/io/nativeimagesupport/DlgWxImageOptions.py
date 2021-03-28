
from logging import Logger
from logging import getLogger
from typing import List

from wx import ALIGN_RIGHT
from wx import ALL
from wx import CANCEL
from wx import EVT_BUTTON
from wx import EVT_CHOICE
from wx import EVT_CLOSE
from wx import EVT_MOTION

from wx import EXPAND
from wx import FD_CHANGE_DIR
from wx import FD_OVERWRITE_PROMPT
from wx import FD_SAVE
from wx import HORIZONTAL
from wx import ID_ANY
from wx import ID_CANCEL
from wx import ID_OK
from wx import OK
from wx import TE_READONLY
from wx import VERTICAL

from wx import Button
from wx import Choice
from wx import CommandEvent
from wx import FileDialog
from wx import BoxSizer
from wx import Sizer

from wx import StaticBox
from wx import StaticBoxSizer
from wx import TextCtrl

from wx import MouseEvent

from wx import Yield as wxYield

from org.pyut.PyutUtils import PyutUtils

from org.pyut.dialogs.BaseDlgEdit import BaseDlgEdit

from org.pyut.plugins.io.nativeimagesupport.WxImageFormat import WxImageFormat

from org.pyut.general.Globals import _

from org.pyut.preferences.PyutPreferences import PyutPreferences


class DlgWxImageOptions(BaseDlgEdit):

    HORIZONTAL_GAP: int = 5

    MIN_UML_SHAPE_GAP: int = 0
    MAX_UML_SHAPE_GAP: int = 100

    def __init__(self, parent):

        [self.__selectedFileId,
         self.__imageWidthId,    self.__imageHeightId,
         self.__horizontalGapId, self.__verticalGapId,
         self.__fileSelectBtn,   self.__imageFormatChoiceId
         ] = PyutUtils.assignID(7)

        super().__init__(parent, theTitle='Native Image Generation Options')

        self.logger:          Logger        = getLogger(__name__)
        self._outputFileName: str           = PyutPreferences().wxImageFileName
        self._imageFormat:    WxImageFormat = WxImageFormat.PNG

        fs:   StaticBoxSizer = self.__layoutFileSelection()
        imgF: StaticBoxSizer = self.__layoutImageFormatChoice()

        hs:   Sizer      = self._createDialogButtonsContainer(buttons=OK | CANCEL)

        mainSizer: BoxSizer = BoxSizer(orient=VERTICAL)
        mainSizer.Add(fs,   0, ALL | EXPAND, 5)
        mainSizer.Add(imgF, 0, ALL, 5)
        mainSizer.Add(hs,   0, ALIGN_RIGHT)

        self.SetSizerAndFit(mainSizer)

        self._bindEventHandlers()

        self.Bind(EVT_BUTTON, self._OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self._OnClose, id=ID_CANCEL)

    @property
    def imageFormat(self) -> WxImageFormat:
        return self._imageFormat

    @imageFormat.setter
    def imageFormat(self, newFormat: WxImageFormat):
        self._imageFormat = newFormat

    @property
    def outputFileName(self) -> str:
        return self._outputFileName

    @outputFileName.setter
    def outputFileName(self, newName: str):
        self._outputFileName = newName

    def _bindEventHandlers(self):

        self.Bind(EVT_BUTTON, self._onFileSelectClick,     id=self.__fileSelectBtn)

        self.Bind(EVT_CHOICE, self._onImageFormatChoice, id=self.__imageFormatChoiceId)

        self._selectedFile.Bind(EVT_MOTION, self._fileSelectionMotion, id=self.__selectedFileId)

    def _fileSelectionMotion(self, event: MouseEvent):

        ctrl: TextCtrl = event.EventObject

        tip = ctrl.GetToolTip()
        tip.SetTip(self._outputFileName)

    # noinspection PyUnusedLocal
    def _onFileSelectClick(self, event: CommandEvent):

        self.logger.warning(f'File Select Click')
        wxYield()

        fmtSelIdx:    int = self._imageFormatChoice.GetCurrentSelection()
        outputFormat: str = self._imageFormatChoice.GetString(fmtSelIdx)

        dlg: FileDialog = FileDialog(self,
                                     message='Choose the export file name',
                                     defaultFile=self._outputFileName,
                                     style=FD_SAVE | FD_OVERWRITE_PROMPT | FD_CHANGE_DIR
                                     )
        if dlg.ShowModal() == ID_OK:
            wxYield()
            path:     str = dlg.GetPath()
            fileName: str = dlg.GetFilename()

            self._selectedFile.SetValue(fileName)       # for simple viewing
            self._selectedFile.SetModified(True)
            self._outputFileName = path                 # for actual us

        dlg.Destroy()

    def _onImageFormatChoice(self, event: CommandEvent):

        ctrl:      Choice = event.EventObject
        idx:       int    = ctrl.GetCurrentSelection()
        newValue:  str    = ctrl.GetString(idx)

        newFormat: WxImageFormat = WxImageFormat(newValue)

        self._imageFormat = newFormat

    def __layoutFileSelection(self) -> StaticBoxSizer:

        box:                StaticBox      = StaticBox(self, ID_ANY, label="Output Filename")
        fileSelectionSizer: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        currentFile: str = self._outputFileName

        fileSelectBtn:      Button   = Button(self, label=_("&Select"),  id=self.__fileSelectBtn)
        self._selectedFile: TextCtrl = TextCtrl(self, value=currentFile, id=self.__selectedFileId, style=TE_READONLY)

        self._selectedFile.SetToolTip(currentFile)

        fileSelectionSizer.Add(fileSelectBtn,       proportion=1, flag=ALL, border=5)
        fileSelectionSizer.Add(self._selectedFile,  proportion=2, flag=ALL | EXPAND, border=5)

        return fileSelectionSizer

    def __layoutImageFormatChoice(self) -> StaticBoxSizer:

        imageChoices: List[str] = [WxImageFormat.PNG.value, WxImageFormat.JPG.value, WxImageFormat.BMP.value, WxImageFormat.TIFF.value]
        self._imageFormatChoice = Choice(self, self.__imageFormatChoiceId, choices=imageChoices)

        box:            StaticBox = StaticBox(self, ID_ANY, "Image Format")
        szrImageFormat: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrImageFormat.Add(self._imageFormatChoice, 0, ALL)

        return szrImageFormat
