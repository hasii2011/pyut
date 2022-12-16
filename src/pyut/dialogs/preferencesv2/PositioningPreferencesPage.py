
from typing import cast

from wx import EVT_CHECKBOX

from wx import CheckBox
from wx import CommandEvent
from wx import StockPreferencesPage
from wx import Window

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedPanel

from pyut.general.datatypes.Dimensions import Dimensions
from pyut.general.datatypes.Position import Position
from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.widgets.DimensionsControl import DimensionsControl
from pyut.ui.widgets.PositionControl import PositionControl


class PositioningPreferencesPage(StockPreferencesPage):

    def __init__(self):
        super().__init__(kind=StockPreferencesPage.Kind_General)

        self._preferences: PyutPreferences = PyutPreferences()

        self._centerAppOnStartupId: int  = wxNewIdRef()
        self._valuesChanged:        bool = False

        self._cbCenterAppOnStartup:   CheckBox              = cast(CheckBox, None)
        self._appPositionControls:    PositionControl   = cast(PositionControl, None)
        self._appDimensionsContainer: DimensionsControl = cast(DimensionsControl, None)

    def CreateWindow(self, parent) -> Window:

        verticalPanel: SizedPanel = SizedPanel(parent)
        verticalPanel.SetSizerType('vertical')

        self._cbCenterAppOnStartup = CheckBox(verticalPanel, self._centerAppOnStartupId, 'Center Pyut on Startup')

        self._appPositionControls = self._createAppPositionControls(sizedPanel=verticalPanel)
        self._appDimensionsContainer: DimensionsControl = self._createAppSizeControls(sizedPanel=verticalPanel)

        self._setControlValues()
        parent.Bind(EVT_CHECKBOX, self._onCenterOnStartupChanged, id=self._centerAppOnStartupId)

        # Do the following or does not get resized correctly
        # A little trick to make sure that the sizer cannot be resized to
        # less screen space than the controls need
        verticalPanel.Fit()
        verticalPanel.SetMinSize(verticalPanel.GetSize())

        return verticalPanel

    def GetName(self) -> str:
        return 'Positions'

    def _createAppPositionControls(self, sizedPanel: SizedPanel) -> PositionControl:

        appPositionControls: PositionControl = PositionControl(sizedPanel=sizedPanel, displayText='Startup Position',
                                                               minValue=0, maxValue=2048,
                                                               valueChangedCallback=self._appPositionChanged)

        return appPositionControls

    def _createAppSizeControls(self, sizedPanel: SizedPanel) -> DimensionsControl:

        appSizeControls: DimensionsControl = DimensionsControl(sizedPanel=sizedPanel, displayText="Startup Width/Height",
                                                               minValue=480, maxValue=4096,
                                                               valueChangedCallback=self._appSizeChanged)
        return appSizeControls

    def _setControlValues(self):
        """
        Set the position controls based on the value of appropriate preference value
        """
        if self._preferences.centerAppOnStartUp is True:
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
            newValue:  If 'True' position controls are disabled else they are enabled
        """
        if newValue is True:
            self._appPositionControls.enableControls(False)
        else:
            self._appPositionControls.enableControls(True)

    def _appPositionChanged(self, newValue: Position):
        self._preferences.startupPosition = newValue
        self._valuesChanged = True

    def _appSizeChanged(self, newValue: Dimensions):
        self._preferences.startupSize = newValue
        self._valuesChanged = True

    def _onCenterOnStartupChanged(self, event: CommandEvent):
        """
        """
        val: bool = event.IsChecked()

        self._preferences.centerAppOnStartUp = val
        self._enablePositionControls(val)

        self._valuesChanged = True



