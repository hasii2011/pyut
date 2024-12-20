
from typing import Tuple
from typing import List

from logging import Logger
from logging import getLogger
from logging import getLevelName    # Goes both ways int --> str and str --> int

from wx import DefaultPosition
from wx import DefaultSize
from wx import EVT_CHECKBOX
from wx import EVT_CHOICE
from wx import ID_ANY

from wx import LC_REPORT
from wx import LIST_MASK_FORMAT
from wx import LIST_MASK_TEXT

from wx import Colour
from wx import CheckBox
from wx import Choice
from wx import CommandEvent

from wx.lib.agw import ultimatelistctrl as ULC

from wx.lib.agw.ultimatelistctrl import ULC_HAS_VARIABLE_ROW_HEIGHT
from wx.lib.agw.ultimatelistctrl import ULC_MASK_CHECK
from wx.lib.agw.ultimatelistctrl import ULC_REPORT
from wx.lib.agw.ultimatelistctrl import ULC_SORT_ASCENDING
from wx.lib.agw.ultimatelistctrl import ULC_VRULES

from wx.lib.agw.ultimatelistctrl import UltimateListItem

from wx.lib.mixins.listctrl import ListRowHighlighter

AGW_STYLE:         int             = ULC_REPORT | ULC_HAS_VARIABLE_ROW_HEIGHT | ULC_SORT_ASCENDING | ULC_VRULES
LIST_CONTROL_SIZE: Tuple[int, int] = (650, 300)


class DebugListControl(ULC.UltimateListCtrl, ListRowHighlighter):

    IDX_NAME_COLUMN:      int = 0
    IDX_LEVEL_COLUMN:     int = 1
    IDX_DISABLED_COLUMN:  int = 2
    IDX_PROPAGATE_COLUMN: int = 3

    CHECK_BOX_KIND:    int = 1
    RADIO_BUTTON_KIND: int = 2

    DARK_GRAY:  Colour = Colour(230, 230, 230)
    LIGHT_GRAY: Colour = Colour(250, 250, 250)

    COLUMN_NAME_PROPAGATE: str = 'Propagate'
    COLUMN_NAME_DISABLED:  str = 'Disabled'
    COLUMN_NAME_LEVEL:     str = 'Level'

    LEVEL_NOT_SET: str = 'NOTSET'
    LEVEL_ERROR:   str = 'ERROR'
    LEVEL_WARNING: str = 'WARNING'
    LEVEL_INFO:    str = 'INFO'
    LEVEL_DEBUG:   str = 'DEBUG'
    LEVEL_FATAL:   str = 'FATAL'

    LEVELS: List[str] = [LEVEL_NOT_SET, LEVEL_INFO, LEVEL_DEBUG, LEVEL_ERROR, LEVEL_FATAL, LEVEL_WARNING]

    def __init__(self, parent, ID, pos=DefaultPosition, size=LIST_CONTROL_SIZE, agwStyle=AGW_STYLE, style=LC_REPORT):

        ULC.UltimateListCtrl.__init__(self, parent, ID, pos, size, agwStyle=agwStyle, style=style)
        ListRowHighlighter.__init__(self)

        self.logger: Logger = getLogger(__name__)

        loggers = [getLogger()]  # get the root _logger

        import logging
        # noinspection PyUnresolvedReferences
        self._loggers: List[Logger] = loggers + [getLogger(name) for name in logging.root.manager.loggerDict]

    def populateList(self):

        defaultMask = LIST_MASK_TEXT | LIST_MASK_FORMAT

        self.InsertColumnInfo(self.IDX_NAME_COLUMN,      self._getColumnHeader("Name", mask=defaultMask))
        self.InsertColumnInfo(self.IDX_LEVEL_COLUMN,     self._getColumnHeader("Level", mask=defaultMask))
        self.InsertColumnInfo(self.IDX_DISABLED_COLUMN,  self._getColumnHeader(self.COLUMN_NAME_DISABLED,  self.CHECK_BOX_KIND, defaultMask | ULC_MASK_CHECK))
        self.InsertColumnInfo(self.IDX_PROPAGATE_COLUMN, self._getColumnHeader(self.COLUMN_NAME_PROPAGATE, self.CHECK_BOX_KIND, defaultMask | ULC_MASK_CHECK))

        row: int = 0

        for logger in self._loggers:

            self.InsertStringItem(row, logger.name)

            self.SetStringItem(row, self.IDX_LEVEL_COLUMN,     '')
            self.SetStringItem(row, self.IDX_DISABLED_COLUMN,  '')
            self.SetStringItem(row, self.IDX_PROPAGATE_COLUMN, '')

            self._makeASelectionList(valueToSet=logger.level, rowNumber=row)
            self._makeACheckBox(valueToSet=bool(logger.disabled),  rowNumber=row, columnName=self.COLUMN_NAME_DISABLED,  columnIdx=self.IDX_DISABLED_COLUMN)
            self._makeACheckBox(valueToSet=bool(logger.propagate), rowNumber=row, columnName=self.COLUMN_NAME_PROPAGATE, columnIdx=self.IDX_PROPAGATE_COLUMN)

            row += 1

    def _getColumnHeader(self, text: str, kind=0, mask=LIST_MASK_TEXT | LIST_MASK_FORMAT) -> UltimateListItem:

        info: UltimateListItem = UltimateListItem()

        info._format = 0
        info.SetMask(mask)
        info.SetText(kind)
        info.SetText(text)

        return info

    def _makeACheckBox(self, valueToSet: bool, rowNumber: int, columnName: str, columnIdx: int):

        nameInfo: str = self.__embedInformationInName(columnName=columnName, rowNumber=rowNumber, columnNumber=columnIdx)
        retCB: CheckBox = CheckBox(self, ID_ANY, "", DefaultPosition, DefaultSize, 0, name=nameInfo)
        retCB.SetValue(valueToSet)
        retCB.Bind(EVT_CHECKBOX, self._onListItemChecked)

        self.SetItemWindow(rowNumber, columnIdx, retCB, expand=True)

    def _makeASelectionList(self, valueToSet: int, rowNumber: int):

        nameInfo: str = self.__embedInformationInName(columnName=DebugListControl.COLUMN_NAME_LEVEL, rowNumber=rowNumber, columnNumber=DebugListControl.IDX_LEVEL_COLUMN)
        ch: Choice = Choice(self, ID_ANY, (100, 50), choices=self.LEVELS, name=nameInfo)

        selStr: str = getLevelName(valueToSet)
        selIdx: int = DebugListControl.LEVELS.index(selStr)

        ch.SetSelection(selIdx)
        self.Bind(EVT_CHOICE, self._onLevelChoice, ch)
        self.SetItemWindow(rowNumber, self.IDX_LEVEL_COLUMN, ch, expand=True)

    def _onListItemChecked(self, event: CommandEvent):

        itemName: str = event.GetEventObject().Name
        self.logger.info(f'string: {event.GetString()}')

        columnName, row, column = self.__extractInformationFromName(theName=itemName)
        clickedLogger: Logger   = self._loggers[row]
        cb:            CheckBox = event.GetEventObject()
        isChecked:     bool     = cb.IsChecked()
        self.logger.info(f'isChecked: `{isChecked}`')

        if columnName == DebugListControl.COLUMN_NAME_PROPAGATE:
            clickedLogger.propagate = isChecked
        elif columnName == DebugListControl.COLUMN_NAME_DISABLED:
            clickedLogger.disabled = isChecked
        else:
            assert False, f'I do not handle this column name: {columnName}'

    def _onLevelChoice(self, event: CommandEvent):

        itemName: str = event.GetEventObject().Name

        columnName, row, column = self.__extractInformationFromName(theName=itemName)
        selectedLogger: Logger = self._loggers[row]

        ch: Choice = event.GetEventObject()
        selIdx: int = ch.GetSelection()
        selStr: str = ch.GetString(selIdx)

        # This is weird;  This method goes both ways
        logLevel: int = getLevelName(selStr)
        selectedLogger.setLevel(logLevel)

        self.logger.info(f'Changed {selectedLogger.name} to {getLevelName(selectedLogger.level)}')

    def __embedInformationInName(self, columnName: str, rowNumber: int, columnNumber: int) -> str:
        """
        This code is a hack.  I have not figured out how to attach data to UltimateListItem;  So
        I encoded it in the name as follows:

        columnName_rowNumber_columnNumber

        Args:
            columnName:
            rowNumber:
            columnNumber:

        Returns:

        """
        return f'{columnName}_{str(rowNumber)}_{str(columnNumber)}'

    def __extractInformationFromName(self, theName: str) -> Tuple[str, int, int]:
        """
        This code is a hack.  I have not figured out how to attach data to UltimateListItem;  So
        I encoded it in the name as follows:

        columnName_rowNumber_columnNumber

        Args:
            theName:

        Returns: A tuple of three items

        """

        self.logger.info(f'name: {theName}')

        itemList: List[str] = theName.split('_')    # columnName, row, col
        self.logger.info(f'itemList: {itemList}')

        columnName: str = itemList[0]
        row:    int = int(itemList[1])
        column: int = int(itemList[2])

        return columnName, row, column
