from typing import Any
from typing import cast
from typing import Dict
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from codeallybasic.SecureConversions import SecureConversions
from wx import CANCEL
from wx import CAPTION
from wx import CheckBox
from wx import Choice
from wx import CommandEvent
from wx import DEFAULT_DIALOG_STYLE
from wx import DefaultPosition
from wx import DefaultSize
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EVT_LISTBOX
from wx import ID_ANY
from wx import ID_CANCEL
from wx import ID_OK
from wx import LB_SINGLE
from wx import LB_SORT
from wx import ListBox
from wx import NOT_FOUND
from wx import OK
from wx import STAY_ON_TOP
from wx import StaticText
from wx import Window

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel

from codeallybasic.DynamicConfiguration import StringList

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.dialogs.logcontrol.DebugLevel import DebugLevel

LoggerList  = NewType('LoggerList',  List[Logger])
LoggerNames = NewType('LoggerNames', List[str])
LevelNames  = NewType('LevelNames',  List[str])
LoggerMap   = NewType('LoggerMap',   Dict[str, Logger])


class DlgLogControl(SizedDialog):

    def __init__(self, parent: Window):

        self.logger: Logger = getLogger(__name__)
        super().__init__(parent=parent, title='Pyut Logging Control', style=DEFAULT_DIALOG_STYLE | STAY_ON_TOP)

        self._preferences:      PyutPreferences = PyutPreferences()
        self._loggers:          LoggerList      = self._getRelevantLoggers()
        self._loggerMap:        LoggerMap       = self._createLoggerMap(self._loggers)

        self._loggerSelector:   ListBox         = cast(ListBox, None)
        self._levelChoice:      Choice          = cast(Choice, None)
        self._loggerEnabled:    CheckBox        = cast(CheckBox, None)
        self._loggerPropagated: CheckBox        = cast(CheckBox, None)

        mainPanel: SizedPanel = self.GetContentsPane()
        mainPanel.SetSizerType("vertical")
        mainPanel.SetSizerProps(expand=True, proportion=1)

        self._layoutDialog(mainPanel=mainPanel)
        self.SetButtonSizer(self.CreateStdDialogButtonSizer(OK))

        self.Bind(EVT_BUTTON, self._onOk,    id=ID_OK)
        self.Bind(EVT_BUTTON, self._onClose, id=ID_CANCEL)
        self.Bind(EVT_CLOSE,  self._onClose)

        self.Bind(EVT_LISTBOX, self._onLoggerSelected, self._loggerSelector)
        #
        # a little trick to make sure that you can't resize the dialog to
        # less screen space than the controls need
        self.Fit()
        self.SetMinSize(self.GetSize())

    def _layoutDialog(self, mainPanel: SizedPanel):

        innerPanel: SizedPanel = SizedPanel(mainPanel)
        innerPanel.SetSizerType('horizontal')
        innerPanel.SetSizerProps(expand=True, proportion=1)

        self._layoutLoggerSelector(innerPanel)
        self._layoutLoggerForm(innerPanel)

    def _layoutLoggerSelector(self, innerPanel: SizedPanel):
        """

        Args:
            innerPanel: The selector's parent
        """
        loggerNames: LoggerNames = LoggerNames([logger.name for logger in self._loggers])

        self._loggerSelector = ListBox(innerPanel, choices=loggerNames, style=LB_SINGLE | LB_SORT)

    def _layoutLoggerForm(self, innerPanel: SizedPanel):

        formPanel: SizedPanel = SizedPanel(innerPanel)
        formPanel.SetSizerType('form')
        formPanel.SetSizerProps(expand=True, proportion=1)

        levelNames: LevelNames = LevelNames([debugLevel.value for debugLevel in DebugLevel])

        StaticText(formPanel, ID_ANY, 'Level:', style=CAPTION)
        self._levelChoice = Choice(formPanel, ID_ANY, (100, 50), choices=levelNames)
        self._levelChoice.SetSelection(NOT_FOUND)

        StaticText(formPanel, ID_ANY, 'Disabled:', style=CAPTION)
        self._loggerEnabled = CheckBox(formPanel, ID_ANY, "", DefaultPosition, DefaultSize)

        StaticText(formPanel, ID_ANY, 'Propagate:', style=CAPTION)
        self._loggerPropagated = CheckBox(formPanel, ID_ANY, "", DefaultPosition, DefaultSize)

    def _getRelevantLoggers(self) -> LoggerList:
        """
        Use the debug preferences to determine which loggers we want to consider

        Returns:  The filtered list
        """
        import logging

        trackedLoggers: StringList = self._preferences.trackedLoggers
        loggers:        LoggerList = LoggerList([getLogger()])  # get the root _logger

        loggers = LoggerList(loggers + [getLogger(name) for name in logging.root.manager.loggerDict])

        filteredLoggers: LoggerList = LoggerList([])
        #
        # This would be unreadable as a list comprehension.  In general for me,
        # list comprehensions are incomprehensible; ;-)
        #
        for lg in loggers:
            logger: Logger = cast(Logger, lg)
            name:   str    = logger.name
            try:
                checkValue: str = name[:name.index('.')]
                if checkValue in trackedLoggers:
                    filteredLoggers.append(logger)
            except ValueError:
                # It might be just the package name
                if name in trackedLoggers:
                    filteredLoggers.append(logger)
                else:
                    self.logger.info(f'Ignored logger: {name}')

        return filteredLoggers

    def _createLoggerMap(self, loggerList: LoggerList) -> LoggerMap:

        loggerMap: LoggerMap = LoggerMap({})

        for lg in loggerList:
            logger: Logger = cast(Logger, lg)
            loggerMap[logger.name] = logger

        return loggerMap

    def _onLoggerSelected(self, event: CommandEvent):

        self.logger.warning(f'{event.GetSelection()=} {event.GetString()=}')

        loggerName:  str    = event.GetString()
        logger:      Logger = self._loggerMap[loggerName]
        loggerLevel: int    = logger.getEffectiveLevel()
        self.logger.warning(f'{loggerLevel=}')

        levelName: str = DebugLevel.toEnum(loggerLevel).value
        idx:       int = self._levelChoice.FindString(levelName, caseSensitive=False)
        self._levelChoice.SetSelection(idx)

        # noinspection PyTypeChecker
        loggerDisabled: bool = self._bugWorkAround(name=f'{loggerName}.loggerDisabled', value=logger.disabled)
        self._loggerEnabled.SetValue(loggerDisabled)

        loggerPropagated: bool = self._bugWorkAround(name=f'{loggerName}.loggerPropagated', value=logger.propagate)
        self.logger.info(f'{loggerPropagated=}')
        self._loggerPropagated.SetValue(loggerPropagated)

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        """
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onClose(self, event: CommandEvent):
        """
        """
        self.EndModal(CANCEL)

    def _bugWorkAround(self, name: str, value: Any) -> bool:
        """
        Sometimes for some loggers boolean we get a string;  It is the ones that we put in
        the JSON logging configuration dictionary

        "propagate": "False",

        should be

        "propagate": false,

        Big bug in all of my configuration files
        Args:
            value:

        Returns:  A boolean value
        """
        if isinstance(value, str):
            self.logger.warning(f'Logger {name} returned string instead of boolean. {value=}')
            return SecureConversions.secureBoolean(value)
        else:
            return value
