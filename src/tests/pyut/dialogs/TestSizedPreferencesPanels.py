
from logging import Logger
from logging import getLogger

from wx import ID_ANY

from wx import App

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from pyut.general.datatypes.Dimensions import Dimensions
from pyut.general.datatypes.Position import Position
from pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from pyut.ui.widgets.DualSpinnerControl import DualSpinnerControl
from pyut.ui.widgets.DualSpinnerControl import SpinnerValues
from pyut.ui.widgets.DimensionsControl import DimensionsControl
from pyut.ui.widgets.PositionControl import PositionControl


class TestSizedPreferencesPanels(App):

    # noinspection PyUnusedLocal
    def OnInit(self):

        TestBase.setUpLogging()
        PyutPreferences.determinePreferencesLocation()
        self.logger: Logger = getLogger(__name__)

        frame: SizedFrame = SizedFrame(parent=None, id=ID_ANY, title="Test Sized PreferencesPanels")

        pane: SizedPanel = frame.GetContentsPane()
        pane.SetSizerType("vertical")

        ds: DualSpinnerControl = DualSpinnerControl(sizedPanel=pane, boxTitle='Bare Spinner', valueChangedCallback=self._spinnerChanged)
        pc: PositionControl    = PositionControl(sizedPanel=pane, displayText='Position',
                                                 valueChangedCallback=self._positionChanged, minValue=0, maxValue=2048)
        dc: DimensionsControl  = DimensionsControl(sizedPanel=pane, displayText='Dimensions',
                                                   valueChangedCallback=self._dimensionsChanged, minValue=100, maxValue=600)
        frame.Show(True)

        self.SetTopWindow(frame)
        frame.CreateStatusBar() # should always do this when there's a resize border

        # frame.Fit()

        self._frame:       SizedFrame = frame
        self._preferences: PyutPreferences = PyutPreferences()

        return True

    def OnExit(self):
        """
        """
        try:
            return App.OnExit(self)
        except (ValueError, Exception) as e:
            self.logger.error(f'OnExit: {e}')

    def _spinnerChanged(self, spinnerValues: SpinnerValues):
        self.logger.info(f'{spinnerValues=}')

    def _positionChanged(self, position: Position):
        self.logger.info(f'{position=}')

    def _dimensionsChanged(self, dimensions: Dimensions):
        self.logger.info(f'{dimensions=}')

testApp: App = TestSizedPreferencesPanels(redirect=False)

testApp.MainLoop()
