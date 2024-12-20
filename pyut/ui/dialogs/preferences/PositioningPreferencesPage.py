
from typing import cast

from wx import EVT_CHECKBOX

from wx import CheckBox
from wx import CommandEvent
from wx import Panel
from wx import Window

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedPanel

from codeallybasic.Dimensions import Dimensions
from codeallybasic.Position import Position

from codeallyadvanced.ui.widgets.DimensionsControl import DimensionsControl
from codeallyadvanced.ui.widgets.PositionControl import PositionControl

from pyut.ui.dialogs.preferences.BasePreferencesPage import BasePreferencesPage
from pyut.ui.eventengine.EventType import EventType
from pyut.ui.eventengine.IEventEngine import IEventEngine


class PositioningPreferencesPage(BasePreferencesPage):
    """
    Implemented using sized components for better platform look and feel
    """

    def __init__(self, parent: Window, eventEngine: IEventEngine):

        self._eventEngine: IEventEngine = eventEngine

        super().__init__(parent)
        self.SetSizerType('vertical')
        self._centerAppOnStartupId: int  = wxNewIdRef()
        self._valuesChanged:        bool = False

        self._cbCenterAppOnStartup:   CheckBox          = cast(CheckBox, None)
        self._appPositionControls:    PositionControl   = cast(PositionControl, None)
        self._appDimensionsContainer: DimensionsControl = cast(DimensionsControl, None)
        self._createWindow(parent)

    def _createWindow(self, parent):

        self._cbCenterAppOnStartup = CheckBox(self, self._centerAppOnStartupId, 'Center Pyut on Startup')

        self._appPositionControls    = self._createAppPositionControls(sizedPanel=self)
        self._appDimensionsContainer = self._createAppSizeControls(sizedPanel=self)

        Panel(self, size=(1, 75))  # TODO: this is a hack

        self._setControlValues()
        parent.Bind(EVT_CHECKBOX, self._onCenterOnStartupChanged, id=self._centerAppOnStartupId)

    @property
    def name(self) -> str:
        return 'Positions'

    def _createAppPositionControls(self, sizedPanel: SizedPanel) -> PositionControl:

        appPositionControls: PositionControl = PositionControl(sizedPanel=sizedPanel, displayText='Startup Position',
                                                               minValue=0, maxValue=2048,
                                                               valueChangedCallback=self._appPositionChanged,
                                                               setControlsSize=False)

        return appPositionControls

    def _createAppSizeControls(self, sizedPanel: SizedPanel) -> DimensionsControl:

        appSizeControls: DimensionsControl = DimensionsControl(sizedPanel=sizedPanel, displayText="Startup Width/Height",
                                                               minValue=480, maxValue=4096,
                                                               valueChangedCallback=self._appSizeChanged,
                                                               setControlsSize=False)
        return appSizeControls

    def _setControlValues(self):
        """
        Set the position controls based on the value of appropriate preference value
        """
        if self._preferences.centerAppOnStartup is True:
            self._appPositionControls.enableControls(False)
            self._cbCenterAppOnStartup.SetValue(True)
        else:
            self._appPositionControls.enableControls(True)
            self._cbCenterAppOnStartup.SetValue(False)

        self._appDimensionsContainer.dimensions = self._preferences.startupSize
        self._appPositionControls.position      = self._preferences.startupPosition

    def _enablePositionControls(self, newValue: bool):
        """
        Enable/Disable position controls based on the value of appropriate preference value

        Args:
            newValue:  If 'True' the position controls are disabled else they are enabled
        """
        if newValue is True:
            self._appPositionControls.enableControls(False)
        else:
            self._appPositionControls.enableControls(True)

    def _appPositionChanged(self, newValue: Position):
        self._preferences.startupPosition = newValue
        self._valuesChanged = True
        self._eventEngine.sendEvent(EventType.OverrideProgramExitPosition, override=True)

    def _appSizeChanged(self, newValue: Dimensions):
        self._preferences.startupSize = newValue
        self._valuesChanged = True
        self._eventEngine.sendEvent(EventType.OverrideProgramExitSize, override=True)

    def _onCenterOnStartupChanged(self, event: CommandEvent):
        """
        """
        val: bool = event.IsChecked()

        self._preferences.centerAppOnStartup = val
        self._enablePositionControls(val)

        self._valuesChanged = True
