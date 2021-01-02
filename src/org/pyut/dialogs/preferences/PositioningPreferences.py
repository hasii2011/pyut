
from typing import Tuple

from logging import Logger
from logging import getLogger

from wx import ALL
from wx import CommandEvent
from wx import EVT_CHECKBOX
from wx import EVT_SPINCTRL
from wx import HORIZONTAL
from wx import ID_ANY
from wx import VERTICAL

from wx import SpinCtrl
from wx import SpinEvent
from wx import StaticBox
from wx import StaticBoxSizer
from wx import BoxSizer
from wx import CheckBox
from wx import Window

from org.pyut.dialogs.preferences.PreferencesPanel import PreferencesPanel

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _


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

        self.__setControlValues()

        self.Bind(EVT_SPINCTRL, self.__onSpinnerValueChanged, id=self.__scAppPosXID)
        self.Bind(EVT_SPINCTRL, self.__onSpinnerValueChanged, id=self.__scAppPosYID)
        self.Bind(EVT_SPINCTRL, self.__onSpinnerValueChanged, id=self.__scAppWidthID)
        self.Bind(EVT_SPINCTRL, self.__onSpinnerValueChanged, id=self.__scAppHeightID)

        self.Bind(EVT_CHECKBOX, self.__onCenterOnStartupChanged, id=self.__centerAppOnStartupID)

        self.SetAutoLayout(True)
        self.SetSizer(mainSizer)

    def __onSpinnerValueChanged(self, event: SpinEvent):

        self.__changed = True
        eventId:  int = event.GetId()
        newValue: int = event.GetInt()

        if eventId == self.__scAppWidthID:
            self._prefs.startupWidth = newValue
        elif eventId == self.__scAppHeightID:
            self._prefs.startupHeight = newValue
        elif eventId == self.__scAppPosXID:
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

        scAppPosX = SpinCtrl(self, self.__scAppPosXID, "", (30, 50))
        scAppPosY = SpinCtrl(self, self.__scAppPosYID, "", (30, 50))

        scAppPosX.SetRange(0, 4096)
        scAppPosY.SetRange(0, 4096)
        scAppPosX.SetValue(self._prefs.appStartupPosition[0])
        scAppPosY.SetValue(self._prefs.appStartupPosition[1])

        box:            StaticBox = StaticBox(self, ID_ANY, _("Startup Position"))
        szrAppPosition: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrAppPosition.Add(scAppPosX, 0, ALL, PositioningPreferences.HORIZONTAL_GAP)
        szrAppPosition.Add(scAppPosY, 0, ALL, PositioningPreferences.HORIZONTAL_GAP)

        self.__scAppPosX = scAppPosX
        self.__scAppPosY = scAppPosY

        return szrAppPosition

    def __createAppSizeControls(self) -> StaticBoxSizer:

        scAppWidth  = SpinCtrl(self, self.__scAppWidthID,  "", (30, 50))
        scAppHeight = SpinCtrl(self, self.__scAppHeightID, "", (30, 50))

        scAppWidth.SetRange(960, 4096)
        scAppHeight.SetRange(480, 4096)

        box:        StaticBox = StaticBox(self, ID_ANY, _("Startup Width/Height"))
        szrAppSize: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrAppSize.Add(scAppWidth,  0, ALL, PositioningPreferences.HORIZONTAL_GAP)
        szrAppSize.Add(scAppHeight, 0, ALL, PositioningPreferences.HORIZONTAL_GAP)

        self.__scAppWidth  = scAppWidth
        self.__scAppHeight = scAppHeight

        return szrAppSize

    def __setControlValues(self):
        """
        Set the position controls based on the value of appropriate preference value
        """
        if self._prefs.centerAppOnStartUp is True:
            self.__scAppPosX.Disable()
            self.__scAppPosY.Disable()
            self.__cbCenterAppOnStartup.SetValue(True)
        else:
            self.__scAppPosX.Enable()
            self.__scAppPosY.Enable()
            self.__cbCenterAppOnStartup.SetValue(False)

        self.__scAppWidth.SetValue(self._prefs.startupWidth)
        self.__scAppHeight.SetValue(self._prefs.startupHeight)

    def __enablePositionControls(self, newValue: bool):
        """
        Enable/Disable position controls based on the value of appropriate preference value

        Args:
            newValue:  If 'True" enabled else disabled
        """
        if newValue is True:
            self.__scAppPosX.Disable()
            self.__scAppPosY.Disable()
        else:
            self.__scAppPosX.Enable()
            self.__scAppPosY.Enable()
