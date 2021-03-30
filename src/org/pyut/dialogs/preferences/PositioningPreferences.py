
from typing import Tuple

from logging import Logger
from logging import getLogger

from wx import ALL
from wx import EVT_CHECKBOX
from wx import EVT_SPINCTRL
from wx import VERTICAL

from wx import CommandEvent
from wx import SpinEvent
from wx import StaticBoxSizer
from wx import BoxSizer
from wx import CheckBox
from wx import Window

from org.pyut.dialogs.preferences.PreferencesPanel import PreferencesPanel

from org.pyut.ui.widgets.DimensionsContainer import DimensionsContainer
from org.pyut.ui.widgets.PositionContainer import PositionContainer

from org.pyut.general.datatypes.Dimensions import Dimensions
from org.pyut.general.datatypes.Position import Position

from org.pyut.general.Globals import _

from org.pyut.PyutUtils import PyutUtils


class PositioningPreferences(PreferencesPanel):

    VERTICAL_GAP:   int = 5
    HORIZONTAL_GAP: int = 5

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Window):

        super().__init__(parent=parent)
        [
            self.__centerAppOnStartupID,
            self.__scAppWidthID, self.__scAppHeightID,
            self.__scAppPosXID,  self.__scAppPosYID
        ] = PyutUtils.assignID(5)

        self._createControls()

        self._valuesChanged: bool = False

    @property
    def valuesChanged(self)  -> bool:
        return self._valuesChanged

    def _createControls(self):
        """
        Creates the main control and stashes them as private instance variables
        """

        self.__cbCenterAppOnStartup: CheckBox = CheckBox(self, self.__centerAppOnStartupID, _('Center Pyut on Startup'))

        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        mainSizer.Add(self.__cbCenterAppOnStartup,        0, ALL, PositioningPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__createAppPositionControls(), 0, ALL, PositioningPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__createAppSizeControls(),     0, ALL, PositioningPreferences.VERTICAL_GAP)

        self._setControlValues()

        self.Bind(EVT_SPINCTRL, self.__onSpinnerValueChanged, id=self.__scAppPosXID)
        self.Bind(EVT_SPINCTRL, self.__onSpinnerValueChanged, id=self.__scAppPosYID)
        self.Bind(EVT_SPINCTRL, self.__onSpinnerValueChanged, id=self.__scAppWidthID)
        self.Bind(EVT_SPINCTRL, self.__onSpinnerValueChanged, id=self.__scAppHeightID)

        self.Bind(EVT_CHECKBOX, self.__onCenterOnStartupChanged, id=self.__centerAppOnStartupID)

        self.SetAutoLayout(True)
        self.SetSizer(mainSizer)

    def _setControlValues(self):
        """
        Set the position controls based on the value of appropriate preference value
        """
        if self._prefs.centerAppOnStartUp is True:
            self._appPositionContainer.enableControls(False)
            self.__cbCenterAppOnStartup.SetValue(True)
        else:
            self._appPositionContainer.enableControls(True)
            self.__cbCenterAppOnStartup.SetValue(False)

        self._appDimensionsContainer.dimensions = self._prefs.startupDimensions
        self._appPositionContainer.position     = self._prefs.startupPosition

    def __onSpinnerValueChanged(self, event: SpinEvent):

        self.__changed = True
        eventId:  int = event.GetId()
        newValue: int = event.GetInt()

        if eventId == self.__scAppPosXID:
            oldValue:    Tuple[int, int] = self._prefs.appStartupPosition
            newPosition: Tuple[int, int] = (newValue, oldValue[1])
            self._prefs.appStartupPosition = newPosition
        elif eventId == self.__scAppPosYID:
            oldValue:    Tuple[int, int] = self._prefs.appStartupPosition
            newPosition: Tuple[int, int] = (oldValue[0], newValue)
            self._prefs.appStartupPosition = newPosition
        else:
            self.clsLogger.error(f'Unknown __OnValueChanged event id: {eventId}')

        self._prefs.overrideOnProgramExit = False
        self._valuesChanged               = True

    def __onCenterOnStartupChanged(self, event: CommandEvent):
        """
        """
        eventID = event.GetId()
        val: bool = event.IsChecked()

        if eventID == self.__centerAppOnStartupID:
            self._prefs.centerAppOnStartUp = val
            self.__enablePositionControls(val)
        else:
            self.clsLogger.warning(f'Unknown check box ID: {eventID}')

        self._valuesChanged = True

    def __createAppPositionControls(self) -> StaticBoxSizer:

        self._appPositionContainer: PositionContainer = PositionContainer(parent=self, displayText=_('Startup Position'),
                                                                          minValue=0, maxValue=2048, valueChangedCallback=self.__appPositionChanged)

        return self._appPositionContainer

    def __createAppSizeControls(self) -> StaticBoxSizer:

        self._appDimensionsContainer: DimensionsContainer = DimensionsContainer(parent=self, displayText=_("Startup Width/Height"),
                                                                                minValue=480, maxValue=4096,
                                                                                valueChangedCallback=self.__appSizeChanged)
        return self._appDimensionsContainer

    def __appSizeChanged(self, newValue: Dimensions):
        self._prefs.startupDimensions = newValue

    def __appPositionChanged(self, newValue: Position):
        self._prefs.startupPosition = newValue

    def __enablePositionControls(self, newValue: bool):
        """
        Enable/Disable position controls based on the value of appropriate preference value

        Args:
            newValue:  If 'True" disabled else enabled
        """
        if newValue is True:
            self._appPositionContainer.enableControls(False)
        else:
            self._appPositionContainer.enableControls(True)
