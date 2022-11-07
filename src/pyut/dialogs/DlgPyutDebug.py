from typing import List
from typing import Tuple

from logging import Logger
from logging import getLogger

from wx import ALIGN_LEFT

from wx import BORDER_SUNKEN
from wx import CANCEL
from wx import CAPTION
from wx import CENTER
from wx import CLOSE_BOX

from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EVT_SIZE
from wx import LEFT
from wx import OK
from wx import ID_OK
from wx import RESIZE_BORDER
from wx import RIGHT
from wx import Sizer
from wx import VERTICAL

from wx import BoxSizer
from wx import CommandEvent
from wx import SizeEvent

from pyut.PyutUtils import PyutUtils

from pyut.dialogs.BaseDlgEdit import BaseDlgEdit

from pyut.dialogs.DebugListControl import DebugListControl


class DlgPyutDebug(BaseDlgEdit):
    """
    Sample use:

        with DlgPyutDebug(self._diagramFrame, ID_ANY) as dlg:
            dlg: DlgPyutDebug = cast(DlgPyutDebug, dlg)
            if dlg.ShowModal() == OK:
                self.logger.info(f'Normal Quite')
            else:
                self.logger.info(f'Cancelled')

    """

    SCROLL_BAR_SPACE: int = 7

    NAME_PERCENTAGE:      float = 0.45
    LEVEL_PERCENTAGE:     float = 0.25
    PROPAGATE_PERCENTAGE: float = 0.10
    DISABLED_PERCENTAGE:  float = 0.10

    COLUMN_WIDTH_RATIOS: List[float] = [NAME_PERCENTAGE, LEVEL_PERCENTAGE, DISABLED_PERCENTAGE, PROPAGATE_PERCENTAGE]

    def __init__(self, theParent, theWindowId):

        super().__init__(theParent, theWindowId, "Debug Pyut", theStyle=CLOSE_BOX | CAPTION | RESIZE_BORDER)
        self.logger: Logger = getLogger(__name__)

        hs:        Sizer    = self._createDialogButtonsContainer()
        mainSizer: BoxSizer = BoxSizer(orient=VERTICAL)

        self._list: DebugListControl = self.__initializeTheControls()

        mainSizer.Add(self._list, 0, LEFT | RIGHT | ALIGN_LEFT, border=5)
        mainSizer.Add(hs,         0, CENTER)

        self.SetSizer(mainSizer)

        mainSizer.Fit(self)

        self.Bind(EVT_SIZE, self.__onSize)

        self.Bind(EVT_BUTTON, self.__OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self.__OnClose)

    def __initializeTheControls(self) -> DebugListControl:
        """
        Initialize the controls.
        """
        [self.__tId] = PyutUtils.assignID(1)

        dbgListCtrl: DebugListControl = DebugListControl(self, self.__tId, style=BORDER_SUNKEN)

        dbgListCtrl.populateList()

        return dbgListCtrl

    def __onSize(self, event: SizeEvent):
        """

        Args:
            event:

        """
        size: Tuple[int, int] = event.GetSize()

        width:    int = size[0]
        nColumns: int = self._list.GetColumnCount()
        self.logger.info(f'width: {width} nColumns: {nColumns}')

        adjustedWidth = width - DlgPyutDebug.SCROLL_BAR_SPACE
        for x in range(nColumns):
            colWidth: float = adjustedWidth * DlgPyutDebug.COLUMN_WIDTH_RATIOS[x]
            self.logger.info(f'x: {x} colWidth: {colWidth}')
            self._list.SetColumnWidth(x, colWidth)  # Allow room for scroll bar

        dlgSize: Tuple[int, int] = self._list.GetSize()
        dlgHeight: int = dlgSize[1]

        self._list.SetSize(adjustedWidth, dlgHeight)

    def __OnCmdOk(self, event: CommandEvent):
        """
        """
        event.Skip(skip=True)
        self.SetReturnCode(OK)
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def __OnClose(self, event: CommandEvent):
        """
        """
        self.SetReturnCode(CANCEL)
        self.EndModal(CANCEL)
