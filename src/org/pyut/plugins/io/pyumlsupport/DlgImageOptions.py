
from logging import Logger
from logging import getLogger
from typing import List
from typing import cast

from wx import ALIGN_RIGHT
from wx import ALL
from wx import CANCEL
from wx import EVT_BUTTON
from wx import EVT_CHOICE
from wx import EVT_CLOSE
from wx import EVT_MOTION
from wx import EVT_SPINCTRL
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
from wx import SpinCtrl
from wx import StaticBox
from wx import StaticBoxSizer
from wx import TextCtrl
from wx import SpinEvent
from wx import MouseEvent

from wx import Yield as wxYield

from org.pyut.preferences.PyutPreferences import PyutPreferences
from org.pyut.PyutUtils import PyutUtils

from org.pyut.dialogs.BaseDlgEdit import BaseDlgEdit

from org.pyut.plugins.io.pyumlsupport.ImageFormat import ImageFormat
from org.pyut.plugins.io.pyumlsupport.ImageOptions import ImageOptions

from org.pyut.general.Globals import _
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine

# Until I get the new Plugins
NO_EVENT_ENGINE = cast(IEventEngine, None)


class DlgImageOptions(BaseDlgEdit):

    HORIZONTAL_GAP: int = 5

    MIN_UML_SHAPE_GAP: int = 0
    MAX_UML_SHAPE_GAP: int = 100

    def __init__(self, theParent, imageOptions: ImageOptions = ImageOptions()):

        [self.__selectedFileId,
         self.__imageWidthId,    self.__imageHeightId,
         self.__horizontalGapId, self.__verticalGapId,
         self.__fileSelectBtn,   self.__imageFormatChoiceId
         ] = PyutUtils.assignID(7)

        super().__init__(theParent, NO_EVENT_ENGINE, title='UML Image Generation Options')

        self.logger:        Logger       = getLogger(__name__)
        imageOptions.outputFileName = PyutPreferences().pdfExportFileName
        self._imageOptions: ImageOptions = imageOptions

        fs:   StaticBoxSizer = self.__layoutFileSelection()
        imgS: StaticBoxSizer = self.__layoutImageSizeControls()
        imgF: StaticBoxSizer = self.__layoutImageFormatChoice()
        imgP: StaticBoxSizer = self.__layoutImagePadding()

        hs:   Sizer      = self._createDialogButtonsContainer(buttons=OK | CANCEL)

        mainSizer: BoxSizer = BoxSizer(orient=VERTICAL)
        mainSizer.Add(fs,   0, ALL | EXPAND, 5)
        mainSizer.Add(imgS, 0, ALL, 5)
        mainSizer.Add(imgF, 0, ALL, 5)
        mainSizer.Add(imgP, 0, ALL, 5)
        mainSizer.Add(hs,   0, ALIGN_RIGHT)

        self.SetSizer(mainSizer)

        mainSizer.Fit(self)
        self._bindEventHandlers()

        self.Bind(EVT_BUTTON, self._OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self._OnClose, id=ID_CANCEL)

    @property
    def imageOptions(self) -> ImageOptions:
        return self._imageOptions

    @imageOptions.setter
    def imageOptions(self, newOptions: ImageOptions):
        self._imageOptions = newOptions

    def _bindEventHandlers(self):

        self.Bind(EVT_BUTTON, self._onFileSelectClick,     id=self.__fileSelectBtn)

        self.Bind(EVT_SPINCTRL, self._onImageSizeChange, id=self.__imageWidthId)
        self.Bind(EVT_SPINCTRL, self._onImageSizeChange, id=self.__imageHeightId)

        self.Bind(EVT_CHOICE, self._onImageFormatChoice, id=self.__imageFormatChoiceId)

        self.Bind(EVT_SPINCTRL, self._onImagePaddingChange, id=self.__horizontalGapId)
        self.Bind(EVT_SPINCTRL, self._onImagePaddingChange, id=self.__verticalGapId)

        self._selectedFile.Bind(EVT_MOTION, self._fileSelectionMotion, id=self.__selectedFileId)

    def _fileSelectionMotion(self, event: MouseEvent):

        ctrl: TextCtrl = event.EventObject

        tip = ctrl.GetToolTip()
        tip.SetTip(self._imageOptions.outputFileName)

    # noinspection PyUnusedLocal
    def _onFileSelectClick(self, event: CommandEvent):

        self.logger.warning(f'File Select Click')
        wxYield()

        fmtSelIdx:    int = self._imageFormatChoice.GetCurrentSelection()
        outputFormat: str = self._imageFormatChoice.GetString(fmtSelIdx)

        dlg: FileDialog = FileDialog(self,
                                     message='Choose the export file name',
                                     defaultFile='PyutExport',
                                     style=FD_SAVE | FD_OVERWRITE_PROMPT | FD_CHANGE_DIR
                                     )
        if dlg.ShowModal() == ID_OK:
            wxYield()
            path:     str = dlg.GetPath()
            fileName: str = dlg.GetFilename()

            self._selectedFile.SetValue(fileName)       # for simple viewing
            self._selectedFile.SetModified(True)
            self._imageOptions.outputFileName = path    # for actual us

        dlg.Destroy()

    def _onImageSizeChange(self, event: SpinEvent):

        eventId:  int = event.GetId()
        newValue: int = event.GetInt()
        if eventId == self.__imageWidthId:
            self._imageOptions.imageWidth = newValue
        elif eventId == self.__imageHeightId:
            self._imageOptions.imageHeight = newValue
        else:
            self.logger.error(f'Unknown _onImageSizeChange event id: {eventId}')

    def _onImagePaddingChange(self, event: SpinEvent):

        eventId:  int = event.GetId()
        newValue: int = event.GetInt()
        if eventId == self.__horizontalGapId:
            self._imageOptions.horizontalGap = newValue
        elif eventId == self.__verticalGapId:
            self._imageOptions.verticalGap = newValue
        else:
            self.logger.error(f'Unknown _onImagePaddingChange event id: {eventId}')

    def _onImageFormatChoice(self, event: CommandEvent):

        ctrl:      Choice = event.EventObject
        idx:       int    = ctrl.GetCurrentSelection()
        newValue:  str    = ctrl.GetString(idx)

        newFormat: ImageFormat = ImageFormat(newValue)

        self._imageOptions.imageFormat = newFormat

    def __layoutFileSelection(self) -> StaticBoxSizer:

        box:                StaticBox      = StaticBox(self, ID_ANY, label="Output Filename")
        fileSelectionSizer: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        currentFile: str = self._imageOptions.outputFileName

        fileSelectBtn:      Button   = Button(self, label=_("&Select"),  id=self.__fileSelectBtn)
        self._selectedFile: TextCtrl = TextCtrl(self, value=currentFile, id=self.__selectedFileId, style=TE_READONLY)

        self._selectedFile.SetToolTip(currentFile)

        fileSelectionSizer.Add(fileSelectBtn,       proportion=0, flag=ALL, border=5)
        fileSelectionSizer.Add(self._selectedFile,  proportion=1, flag=ALL | EXPAND, border=5)

        return fileSelectionSizer

    def __layoutImageSizeControls(self) -> StaticBoxSizer:

        imageWidth  = SpinCtrl(self, self.__imageWidthId,  value=str(self._imageOptions.imageWidth))
        imageHeight = SpinCtrl(self, self.__imageHeightId, value=str(self._imageOptions.imageHeight))

        imageWidth.SetRange(500, 3000)
        imageHeight.SetRange(500, 3000)

        box:        StaticBox = StaticBox(self, ID_ANY, "Layout Width/Height")
        szrAppSize: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrAppSize.Add(imageWidth, 0, ALL, DlgImageOptions.HORIZONTAL_GAP)
        szrAppSize.Add(imageHeight, 0, ALL, DlgImageOptions.HORIZONTAL_GAP)

        return szrAppSize

    def __layoutImageFormatChoice(self) -> StaticBoxSizer:

        imageChoices: List[str] = [ImageFormat.PNG.value, ImageFormat.JPG.value, ImageFormat.BMP.value, ImageFormat.GIF.value]
        self._imageFormatChoice = Choice(self, self.__imageFormatChoiceId, choices=imageChoices)

        box:            StaticBox = StaticBox(self, ID_ANY, "Image Format")
        szrImageFormat: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrImageFormat.Add(self._imageFormatChoice, 0, ALL)

        return szrImageFormat

    def __layoutImagePadding(self) -> StaticBoxSizer:

        box:                  StaticBox = StaticBox(self, ID_ANY, "Shape Padding")
        szrImagePaddingSizer: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        hGap: int = self._imageOptions.horizontalGap
        vGap: int = self._imageOptions.verticalGap

        horizontalGap: SpinCtrl = SpinCtrl(self, id=self.__horizontalGapId, value=str(hGap),
                                           min=DlgImageOptions.MIN_UML_SHAPE_GAP, max=DlgImageOptions.MAX_UML_SHAPE_GAP)
        verticalGap:   SpinCtrl = SpinCtrl(self, id=self.__verticalGapId,   value=str(vGap),
                                           min=DlgImageOptions.MIN_UML_SHAPE_GAP, max=DlgImageOptions.MAX_UML_SHAPE_GAP)

        szrImagePaddingSizer.Add(horizontalGap, flag=ALL, border=5)
        szrImagePaddingSizer.Add(verticalGap,   flag=ALL, border=5)

        return szrImagePaddingSizer
