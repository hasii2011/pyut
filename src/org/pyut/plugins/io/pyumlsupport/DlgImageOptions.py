
from logging import Logger
from logging import getLogger

from wx import ALIGN_RIGHT
from wx import ALL
from wx import CANCEL
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import HORIZONTAL
from wx import ID_ANY
from wx import ID_CANCEL
from wx import ID_OK
from wx import OK
from wx import VERTICAL

from wx import Button
from wx import CommandEvent
from wx import BoxSizer
from wx import Sizer
from wx import SpinCtrl
from wx import StaticBox
from wx import StaticBoxSizer
from wx import TextCtrl

from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.BaseDlgEdit import BaseDlgEdit
from org.pyut.general.Globals import _


class DlgImageOptions(BaseDlgEdit):

    HORIZONTAL_GAP: int = 5

    DEFAULT_LAYOUT_WIDTH:  int = 1280
    DEFAULT_LAYOUT_HEIGHT: int = 1024

    def __init__(self, theParent, imageWidth=DEFAULT_LAYOUT_WIDTH, imageHeight=DEFAULT_LAYOUT_HEIGHT):

        [self.__fileSelectId, self.__selectedFileId,
         self.__imageWidthId, self.__imageHeightId] = PyutUtils.assignID(4)

        super().__init__(theParent, theTitle='UML Image Generation Options')

        self.logger: Logger = getLogger(__name__)

        self._imageWidth:  int = imageWidth
        self._imageHeight: int = imageHeight

        fs: BoxSizer   = self.__layoutFileSelection()
        imgS: BoxSizer = self.__layoutImageSizeControls()
        hs: Sizer      = self._createDialogButtonsContainer(buttons=OK | CANCEL)

        mainSizer: BoxSizer = BoxSizer(orient=VERTICAL)
        mainSizer.Add(fs, 0, ALL, 5)
        mainSizer.Add(imgS, 0, ALL, 5)
        mainSizer.Add(hs, 0, ALIGN_RIGHT)

        self.SetSizer(mainSizer)

        mainSizer.Fit(self)

        self.Bind(EVT_BUTTON, self._OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self._OnClose, id=ID_CANCEL)

    def __layoutFileSelection(self) -> BoxSizer:

        fileSelectionSizer: BoxSizer = BoxSizer(orient=HORIZONTAL)

        fileSelectBtn: Button   = Button(self, OK, _("&Select"),)
        selectedFile:  TextCtrl = TextCtrl(self, value='PyutExport.png', id=self.__fileSelectId,)

        # lblSelectedFilename: StaticText = StaticText(self, ID_ANY, _("Selected Filename"), style=ALIGN_LEFT)

        fileSelectionSizer.Add(fileSelectBtn, proportion=0, flag=ALL, border=10)
        fileSelectionSizer.Add(selectedFile,  proportion=0, flag=ALL, border=10)
        # fileSelectionSizer.Add(lblSelectedFilename)

        self.Bind(EVT_BUTTON, self._onFileSelectClick, id=self.__fileSelectId)

        return fileSelectionSizer

    def __layoutImageSizeControls(self) -> StaticBoxSizer:

        layoutWidth  = SpinCtrl(self, self.__imageWidthId,  "", (30, 50))
        layoutHeight = SpinCtrl(self, self.__imageHeightId, "", (30, 50))

        layoutWidth.SetRange(500, 3000)
        layoutHeight.SetRange(500, 3000)

        box:        StaticBox = StaticBox(self, ID_ANY, "Layout Width/Height")
        szrAppSize: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrAppSize.Add(layoutWidth, 0,  ALL, DlgImageOptions.HORIZONTAL_GAP)
        szrAppSize.Add(layoutHeight, 0, ALL, DlgImageOptions.HORIZONTAL_GAP)

        self.__layoutWidth  = layoutWidth
        self.__layoutHeight = layoutHeight

        self.__layoutWidth.SetValue(self._imageWidth)
        self.__layoutHeight.SetValue(self._imageHeight)

        return szrAppSize

    # noinspection PyUnusedLocal
    def _onFileSelectClick(self, event: CommandEvent):

        self.logger.warning(f'File Select Click')
