from logging import DEBUG
from logging import ERROR
from logging import FATAL
from logging import INFO
from logging import WARNING

from wx import CheckBox
from wx import Colour
from wx import CommandEvent
from wx import DefaultPosition
from wx import DefaultSize
from wx import EVT_CHECKBOX
from wx import ID_ANY

from wx import LC_REPORT
from wx import LIST_AUTOSIZE
from wx import LIST_MASK_FORMAT
from wx import LIST_MASK_TEXT

from wx.lib.agw import ultimatelistctrl as ULC

from wx.lib.agw.ultimatelistctrl import ULC_HAS_VARIABLE_ROW_HEIGHT
from wx.lib.agw.ultimatelistctrl import ULC_MASK_CHECK
from wx.lib.agw.ultimatelistctrl import ULC_REPORT
from wx.lib.agw.ultimatelistctrl import ULC_SORT_ASCENDING
from wx.lib.agw.ultimatelistctrl import ULC_VRULES
from wx.lib.agw.ultimatelistctrl import UltimateListItem

from wx.lib.mixins.listctrl import ListRowHighlighter


class DebugListControl(ULC.UltimateListCtrl, ListRowHighlighter):

    IDX_NAME_COLUMN:      int = 0
    IDX_LEVEL_COLUMN:     int = 1
    IDX_DISABLED_COLUMN:  int = 2
    IDX_PROPAGATE_COLUMN: int = 3

    CHECK_BOX_KIND:    int = 1
    RADIO_BUTTON_KIND: int = 2

    DARK_GRAY:  Colour = Colour(230, 230, 230)
    LIGHT_GRAY: Colour = Colour(250, 250, 250)

    def __init__(self, parent, ID, pos=DefaultPosition, size=(650, 200),
                 agwStyle=ULC_REPORT | ULC_HAS_VARIABLE_ROW_HEIGHT | ULC_SORT_ASCENDING | ULC_VRULES,
                 style=LC_REPORT):

        ULC.UltimateListCtrl.__init__(self, parent, ID, pos, size, agwStyle=agwStyle, style=style)
        ListRowHighlighter.__init__(self)

        import logging
        loggers = [logging.getLogger()]  # get the root logger

        # noinspection PyUnresolvedReferences
        self._loggers: List[Logger] = loggers + [logging.getLogger(name) for name in logging.root.manager.loggerDict]

    def populateList(self):

        defaultMask = LIST_MASK_TEXT | LIST_MASK_FORMAT

        self.InsertColumnInfo(self.IDX_NAME_COLUMN,      self._getColumnHeader("Name", mask=defaultMask))
        self.InsertColumnInfo(self.IDX_LEVEL_COLUMN,     self._getColumnHeader("Level", mask=defaultMask))
        self.InsertColumnInfo(self.IDX_DISABLED_COLUMN,  self._getColumnHeader('Disabled?',  self.CHECK_BOX_KIND, defaultMask | ULC_MASK_CHECK))
        self.InsertColumnInfo(self.IDX_PROPAGATE_COLUMN, self._getColumnHeader('Propagate?', self.CHECK_BOX_KIND, defaultMask | ULC_MASK_CHECK))

        row: int = 0

        for logger in self._loggers:

            self.InsertStringItem(row, logger.name)

            self.SetStringItem(row, self.IDX_LEVEL_COLUMN, self._levelToString(logger.level))
            self.SetStringItem(row, self.IDX_DISABLED_COLUMN,  '')
            self.SetStringItem(row, self.IDX_PROPAGATE_COLUMN, '')

            disabledCB: CheckBox = CheckBox(self, ID_ANY, "", DefaultPosition, DefaultSize, 0, name=f'Disabled_{str(row)}_{self.IDX_DISABLED_COLUMN}')
            disabledCB.SetValue(bool(logger.disabled))
            disabledCB.Bind(EVT_CHECKBOX, self._onListItemChecked)
            self.SetItemWindow(row, self.IDX_DISABLED_COLUMN, disabledCB, expand=True)

            propagateCB: CheckBox = CheckBox(self, ID_ANY, "", DefaultPosition, DefaultSize, 0, name=f'Propagate_{str(row)}_{self.IDX_PROPAGATE_COLUMN}')
            propagateCB.SetValue(bool(logger.propagate))
            propagateCB.Bind(EVT_CHECKBOX, self._onListItemChecked)
            self.SetItemWindow(row, self.IDX_PROPAGATE_COLUMN, propagateCB, expand=True)

            row += 1

        self.SetColumnWidth(self.IDX_NAME_COLUMN,      LIST_AUTOSIZE)
        self.SetColumnWidth(self.IDX_LEVEL_COLUMN,     LIST_AUTOSIZE)
        self.SetColumnWidth(self.IDX_DISABLED_COLUMN,  LIST_AUTOSIZE)
        self.SetColumnWidth(self.IDX_PROPAGATE_COLUMN, LIST_AUTOSIZE)

    def _getColumnHeader(self, text: str, kind=0, mask=LIST_MASK_TEXT | LIST_MASK_FORMAT) -> UltimateListItem:

        info: UltimateListItem = UltimateListItem()

        info._format = 0
        info.SetMask(mask)
        info.SetText(kind)
        info.SetText(text)

        return info

    def _levelToString(self, debugLevel: int) -> str:

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

    def _onListItemChecked(self, event: CommandEvent):

        print(f'name: {event.GetEventObject().Name} string: {event.GetString()}')
        # gp: DebugListControl = event.GetEventObject().GetGrandParent()
