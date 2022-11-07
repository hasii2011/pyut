
from logging import Logger
from logging import getLogger

from wx import ALL
from wx import EVT_CHECKBOX
from wx import VERTICAL

from wx import CommandEvent
from wx import StaticBoxSizer
from wx import BoxSizer
from wx import CheckBox
from wx import Window

from wx import NewIdRef as wxNewIdRef

from pyut.dialogs.preferences.PreferencesPanel import PreferencesPanel

from org.pyut.ui.widgets.DimensionsContainer import DimensionsContainer
from org.pyut.ui.widgets.PositionContainer import PositionContainer

from org.pyut.general.datatypes.Dimensions import Dimensions
from org.pyut.general.datatypes.Position import Position

# noinspection PyProtectedMember
from org.pyut.general.Globals import _


class PositioningPreferences(PreferencesPanel):

    VERTICAL_GAP:   int = 5
    HORIZONTAL_GAP: int = 5

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Window):

        super().__init__(parent=parent)

        self.__centerAppOnStartupId: int = wxNewIdRef()

        self._createControls()

        self._valuesChanged: bool = False

    @property
    def valuesChanged(self)  -> bool:
        return self._valuesChanged

    def _createControls(self):
        """
        Creates the main control and stashes them as private instance variables
        """

        self.__cbCenterAppOnStartup: CheckBox = CheckBox(self, self.__centerAppOnStartupId, _('Center Pyut on Startup'))

        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        mainSizer.Add(self.__cbCenterAppOnStartup,        0, ALL, PositioningPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__createAppPositionControls(), 0, ALL, PositioningPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__createAppSizeControls(),     0, ALL, PositioningPreferences.VERTICAL_GAP)

        self._setControlValues()

        self.Bind(EVT_CHECKBOX, self.__onCenterOnStartupChanged, id=self.__centerAppOnStartupId)

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

        self._appDimensionsContainer.dimensions = self._prefs.startupSize
        self._appPositionContainer.position     = self._prefs.startupPosition

    def __onCenterOnStartupChanged(self, event: CommandEvent):
        """
        """
        val: bool = event.IsChecked()

        self._prefs.centerAppOnStartUp = val
        self.__enablePositionControls(val)

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
        self._prefs.startupSize = newValue
        self._valuesChanged = True

    def __appPositionChanged(self, newValue: Position):
        self._prefs.startupPosition = newValue
        self._valuesChanged = True

    def __enablePositionControls(self, newValue: bool):
        """
        Enable/Disable position controls based on the value of appropriate preference value

        Args:
            newValue:  If 'True' position controls are disabled else they are enabled
        """
        if newValue is True:
            self._appPositionContainer.enableControls(False)
        else:
            self._appPositionContainer.enableControls(True)
