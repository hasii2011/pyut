
from wx import CheckBox
from wx import StockPreferencesPage
from wx import Window

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedPanel

from pyut.general.datatypes.Dimensions import Dimensions
from pyut.general.datatypes.Position import Position
from pyut.preferences.PyutPreferences import PyutPreferences
from pyut.ui.widgets.DimensionsContainerV2 import DimensionsContainerV2
from pyut.ui.widgets.PositionContainerV2 import PositionContainerV2


class PositioningPreferencesPage(StockPreferencesPage):

    def __init__(self):
        super().__init__(kind=StockPreferencesPage.Kind_General)

        self._preferences: PyutPreferences = PyutPreferences()

        self._centerAppOnStartupId: int  = wxNewIdRef()
        self._valuesChanged:        bool = False

    def CreateWindow(self, parent) -> Window:

        verticalPanel: SizedPanel = SizedPanel(parent)
        verticalPanel.SetSizerType('vertical')

        self._cbCenterAppOnStartup: CheckBox = CheckBox(verticalPanel, self._centerAppOnStartupId, 'Center Pyut on Startup')

        self._createAppPositionControls(sizedPanel=verticalPanel)
        self._createAppSizeControls(sizedPanel=verticalPanel)

        # Do the following or does not get resized correctly
        # A little trick to make sure that the sizer cannot be resized to
        # less screen space than the controls need
        verticalPanel.Fit()
        verticalPanel.SetMinSize(verticalPanel.GetSize())
        return verticalPanel

    def GetName(self) -> str:
        return 'Positions'

    def _createAppPositionControls(self, sizedPanel: SizedPanel) -> PositionContainerV2:

        self._appPositionContainer: PositionContainerV2 = PositionContainerV2(sizedPanel=sizedPanel, displayText='Startup Position',
                                                                              minValue=0, maxValue=2048,
                                                                              valueChangedCallback=self.__appPositionChanged)

        return self._appPositionContainer

    def _createAppSizeControls(self, sizedPanel: SizedPanel) -> DimensionsContainerV2:

        self._appDimensionsContainer: DimensionsContainerV2 = DimensionsContainerV2(sizedPanel=sizedPanel, displayText="Startup Width/Height",
                                                                                    minValue=480, maxValue=4096,
                                                                                    valueChangedCallback=self._appSizeChanged)
        return self._appDimensionsContainer


    def __appPositionChanged(self, newValue: Position):
        self._preferences.startupPosition = newValue
        self._valuesChanged = True

    def _appSizeChanged(self, newValue: Dimensions):
        self._preferences.startupSize = newValue
        self._valuesChanged = True
