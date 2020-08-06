
from logging import Logger
from logging import getLogger
from typing import List

from wx import ALIGN_RIGHT
from wx import ALL
from wx import CANCEL
from wx import EVT_BUTTON
from wx import EVT_CLOSE
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
from wx import Yield as wxYield

from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.BaseDlgEdit import BaseDlgEdit
from org.pyut.general.Globals import _
from org.pyut.plugins.io.pyumlsupport.ImageFormat import ImageFormat
from org.pyut.plugins.io.pyumlsupport.ImageOptions import ImageOptions


class DlgImageOptions(BaseDlgEdit):

    HORIZONTAL_GAP: int = 5

    DEFAULT_LAYOUT_WIDTH:  int = 1280
    DEFAULT_LAYOUT_HEIGHT: int = 1024

    def __init__(self, theParent, imageOptions: ImageOptions = ImageOptions()):

        [self.__fileSelectId,     self.__selectedFileId,
         self.__imageWidthId,    self.__imageHeightId,
         self.__horizontalGapId, self.__verticalGapId,
         self.__fileSelectBtn
         ] = PyutUtils.assignID(7)

        super().__init__(theParent, theTitle='UML Image Generation Options')

        self.logger: Logger = getLogger(__name__)

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

        self.Bind(EVT_BUTTON, self._OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self._OnClose, id=ID_CANCEL)

    @property
    def imageOptions(self) -> ImageOptions:
        return self._imageOptions

    @imageOptions.setter
    def imageOptions(self, newOptions: ImageOptions):
        self._imageOptions = newOptions

    # noinspection PyUnusedLocal
    def _onFileSelectClick(self, event: CommandEvent):

        self.logger.warning(f'File Select Click')
        wxYield()

        fmtSelIdx:    int = self._imageFormatChoice.GetCurrentSelection()
        outputFormat: str = self._imageFormatChoice.GetString(fmtSelIdx)

        # file:         str = FileSelector(message="Choose the export file name",
        #                                  default_filename='PyutExport',
        #                                  default_extension=outputFormat,
        #                                  flags=FD_SAVE | FD_OVERWRITE_PROMPT | FD_CHANGE_DIR)
        #
        wildCard = "Png files (*.png)|*.png|"
        dlg: FileDialog = FileDialog(self,
                                     message='Choose the export file name',
                                     defaultFile='PyutExport',
                                     style=FD_SAVE | FD_OVERWRITE_PROMPT | FD_CHANGE_DIR
                                     )
        if dlg.ShowModal() == ID_OK:
            wxYield()
            path:     str = dlg.GetPath()
            fileName: str = dlg.GetFilename()
            self._selectedFile.SetValue(fileName)

            self._imageOptions.outputFileName = path

        dlg.Destroy()

    def _onImageSizeChange(self, event: SpinEvent):

        eventId:  int = event.GetId()
        newValue: int = event.GetInt()
        if eventId == self.__imageWidthId:
            self._imageOptions.imageWidth = newValue
        elif eventId == self.__imageHeightId:
            self._imageOptions.imageHeight = newValue
        else:
            self.logger.error(f'Unknown onSizeChange event id: {eventId}')

    def __layoutFileSelection(self) -> StaticBoxSizer:

        box:                StaticBox      = StaticBox(self, ID_ANY, label="Output Filename")
        fileSelectionSizer: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        fileSelectBtn:       Button   = Button(self, label=_("&Select"), id=self.__fileSelectBtn)
        self._selectedFile:  TextCtrl = TextCtrl(self, value='PyutExport.png', id=self.__fileSelectId)

        fileSelectionSizer.Add(fileSelectBtn,       proportion=0, flag=ALL, border=5)
        fileSelectionSizer.Add(self._selectedFile,  proportion=1, flag=ALL | EXPAND, border=5)

        self.Bind(EVT_BUTTON, self._onFileSelectClick, id=self.__fileSelectBtn)

        return fileSelectionSizer

    def __layoutImageSizeControls(self) -> StaticBoxSizer:

        imageWidth  = SpinCtrl(self, self.__imageWidthId,  "")
        imageHeight = SpinCtrl(self, self.__imageHeightId, "")

        imageWidth.SetRange(500, 3000)
        imageHeight.SetRange(500, 3000)

        box:        StaticBox = StaticBox(self, ID_ANY, "Layout Width/Height")
        szrAppSize: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrAppSize.Add(imageWidth, 0, ALL, DlgImageOptions.HORIZONTAL_GAP)
        szrAppSize.Add(imageHeight, 0, ALL, DlgImageOptions.HORIZONTAL_GAP)

        self.__imageWidth  = imageWidth
        self.__imageHeight = imageHeight

        self.__imageWidth.SetValue(self._imageOptions.imageWidth)
        self.__imageHeight.SetValue(self._imageOptions.imageHeight)

        self.Bind(EVT_SPINCTRL, self._onImageSizeChange, id=self.__imageWidthId)
        self.Bind(EVT_SPINCTRL, self._onImageSizeChange, id=self.__imageHeightId)

        return szrAppSize

    def __layoutImageFormatChoice(self) -> StaticBoxSizer:

        imageChoices: List[str] = [ImageFormat.PNG.value, ImageFormat.JPG.value, ImageFormat.BMP.value, ImageFormat.GIF.value]
        self._imageFormatChoice = Choice(self, ID_ANY, choices=imageChoices)

        box:            StaticBox = StaticBox(self, ID_ANY, "Image Format")
        szrImageFormat: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrImageFormat.Add(self._imageFormatChoice, 0, ALL)

        return szrImageFormat

    def __layoutImagePadding(self) -> StaticBoxSizer:

        box:                  StaticBox = StaticBox(self, ID_ANY, "Shape Padding")
        szrImagePaddingSizer: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        self._horizontalGap: SpinCtrl = SpinCtrl(self, id=self.__horizontalGapId, value="60", min=0, max=100)
        self._verticalGap:   SpinCtrl = SpinCtrl(self, id=self.__verticalGapId,   value="60", min=0, max=100)

        szrImagePaddingSizer.Add(self._horizontalGap, flag=ALL, border=5)
        szrImagePaddingSizer.Add(self._verticalGap,   flag=ALL, border=5)

        return szrImagePaddingSizer
