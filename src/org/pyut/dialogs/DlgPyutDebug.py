
from typing import Tuple

from logging import Logger
from logging import getLogger

from wx import ALL
from wx import BORDER_SUNKEN
from wx import CANCEL
from wx import CAPTION
from wx import CENTER
from wx import CLOSE_BOX

from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EVT_SIZE
from wx import EXPAND
from wx import OK
from wx import ID_OK
from wx import VERTICAL

from wx import BoxSizer
from wx import CommandEvent
from wx import SizeEvent

from org.pyut.PyutUtils import PyutUtils

from org.pyut.dialogs.BaseDlgEdit import BaseDlgEdit

from org.pyut.dialogs.DebugListControl import DebugListControl


class DlgPyutDebug(BaseDlgEdit):

    SCROLL_BAR_SPACE: int = 6

    def __init__(self, theParent, theWindowId):

        super().__init__(theParent, theWindowId, "Debug Pyut", theStyle=CLOSE_BOX | CAPTION)
        self.logger: Logger = getLogger(__name__)

        hs:        BoxSizer = self._createDialogButtonsContainer()
        mainSizer: BoxSizer = BoxSizer(orient=VERTICAL)

        self._list: DebugListControl = self.__initializeTheControls()

        mainSizer.Add(self._list, 0, ALL | EXPAND, BaseDlgEdit.VERTICAL_GAP)
        mainSizer.Add(hs,         0, CENTER)

        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.InsertSpacer(index=0, size=7)     # magic # for the index
        mainSizer.InsertSpacer(index=2, size=20)    # magic # for the index
        mainSizer.SetSizeHints(self)
        mainSizer.Fit(self)

        self.Bind(EVT_SIZE, self.__onSize)

        self.Bind(EVT_BUTTON, self.__OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self.__OnClose)

    def __initializeTheControls(self) -> DebugListControl:
        """
        Initialize the controls.
        """
        [ self.__tId] = PyutUtils.assignID(1)

        dbgListCtrl: DebugListControl = DebugListControl(self, self.__tId, style=BORDER_SUNKEN)

        dbgListCtrl.populateList()

        return dbgListCtrl

    def __onSize(self, event: SizeEvent):
        """
        This will only fire once since I don't allow resize of the dialog
        Args:
            event:

        Returns:

        """
        size: Tuple[int, int] = event.GetSize()

        width:    int = size[0]

        nColumns: int = self._list.GetColumnCount()
        colWidth: int = width // nColumns
        self.logger.info(f'width: {width} nColumns: {nColumns} colWidth: {colWidth}')

        for x in range(nColumns):
            self._list.SetColumnWidth(x, colWidth - DlgPyutDebug.SCROLL_BAR_SPACE)  # Allow room for scroll bar

        dlgSize: Tuple[int, int] = self._list.GetSize()
        dlgHeight: int = dlgSize[1]

        self._list.SetSize(width, dlgHeight)

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
