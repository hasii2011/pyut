
from typing import List
from typing import Tuple

from logging import Logger
from logging import getLogger
from logging import DEBUG
from logging import WARNING
from logging import INFO
from logging import ERROR
from logging import FATAL

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
from wx import LC_EDIT_LABELS
from wx import LIST_AUTOSIZE

from wx import VERTICAL

from wx import BoxSizer
from wx import CommandEvent
from wx import SizeEvent


from org.pyut.PyutUtils import PyutUtils

from org.pyut.dialogs.BaseDlgEdit import BaseDlgEdit

from org.pyut.dialogs.DebugListControl import DebugListControl


class DlgPyutDebug(BaseDlgEdit):

    def __init__(self, theParent, theWindowId):

        super().__init__(theParent, theWindowId, "Debug Pyut", theStyle=CLOSE_BOX | CAPTION)
        self.logger: Logger = getLogger(__name__)

        import logging
        loggers = [logging.getLogger()]  # get the root logger

        # noinspection PyUnresolvedReferences
        self._loggers: List[Logger] = loggers + [logging.getLogger(name) for name in logging.root.manager.loggerDict]

        hs:        BoxSizer = self._createDialogButtonsContainer()
        mainSizer: BoxSizer = BoxSizer(orient=VERTICAL)

        self._list: DebugListControl = self.__initializeTheControls()

        mainSizer.Add(self._list, 0, ALL | EXPAND, BaseDlgEdit.VERTICAL_GAP)
        mainSizer.Add(hs,         0, CENTER)

        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.InsertSpacer(index=0, size=7)    # magic # for the index
        mainSizer.InsertSpacer(index=2, size=20)    # magic # for the index
        mainSizer.SetSizeHints(self)
        mainSizer.Fit(self)

        self.Bind(EVT_SIZE, self._onSize)

        self.Bind(EVT_BUTTON, self.__OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self.__OnClose)

    def __initializeTheControls(self) -> DebugListControl:
        """
        Initialize the controls.
        """
        # IDs
        [
            self.__xId, self.__tId
        ] = PyutUtils.assignID(2)

        dbgListCtrl: DebugListControl = DebugListControl(self, self.__tId, style=BORDER_SUNKEN | LC_EDIT_LABELS)

        self._populateList(dbgListCtrl)

        return dbgListCtrl

    def _populateList(self, dbgListCtrl: DebugListControl):

        dbgListCtrl.InsertColumn(0, "Name")
        dbgListCtrl.InsertColumn(1, "Level")
        dbgListCtrl.InsertColumn(2, "Disabled?")
        dbgListCtrl.InsertColumn(3, "Propagate?")

        for logger in self._loggers:
            levelStr: str = self.__levelToString(logger.level)
            entry = (logger.name, levelStr, str(logger.disabled), str(logger.propagate))
            dbgListCtrl.Append(entry)

        dbgListCtrl.SetColumnWidth(0, LIST_AUTOSIZE)
        dbgListCtrl.SetColumnWidth(1, LIST_AUTOSIZE)
        dbgListCtrl.SetColumnWidth(2, LIST_AUTOSIZE)
        dbgListCtrl.SetColumnWidth(3, LIST_AUTOSIZE)

    def __levelToString(self, debugLevel: int) -> str:

        levelStr: str = ' NOTSET '
        if debugLevel == ERROR:
            levelStr = ' ERROR '
        elif debugLevel == WARNING:
            levelStr = ' WARNING '
        elif debugLevel == INFO:
            levelStr = ' INFO '
        elif debugLevel == DEBUG:
            levelStr = ' DEBUG '
        elif debugLevel == FATAL:
            levelStr = ' FATAL '

        return levelStr

    def _onSize(self, event: SizeEvent):

        size: Tuple[int, int] = event.GetSize()

        width:    int = size[0]

        nColumns: int = self._list.GetColumnCount()
        colWidth: int = width // nColumns
        self.logger.info(f'width: {width} nColumns: {nColumns} colWidth: {colWidth}')

        for x in range(nColumns):
            self._list.SetColumnWidth(x, colWidth)

        dlgSize: Tuple[int, int] = self._list.GetSize()
        dlgHeight: int = dlgSize[1]
        self._list.SetSizeWH(width, dlgHeight)


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
