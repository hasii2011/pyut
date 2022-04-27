
from logging import Logger
from logging import getLogger
from typing import List

from wx import ALL
from wx import CB_READONLY
from wx import EVT_CHECKBOX
from wx import EVT_CHOICE
from wx import EVT_COMBOBOX
from wx import EVT_SPINCTRL
from wx import EXPAND
from wx import HORIZONTAL
from wx import ID_ANY
from wx import LEFT
from wx import RIGHT
from wx import TOP
from wx import BOTTOM
from wx import VERTICAL
from wx import ALIGN_LEFT

from wx import CheckBox
from wx import Choice
from wx import CommandEvent
from wx import SpinCtrl
from wx import SpinEvent
from wx import StaticBox
from wx import StaticBoxSizer
from wx import BoxSizer
from wx import ComboBox
from wx import Window

from org.pyut.dialogs.preferences.PreferencesPanel import PreferencesPanel

from org.pyut.miniogl.MiniOglColorEnum import MiniOglColorEnum

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _
from org.pyut.miniogl.MiniOglPenStyle import MiniOglPenStyle


class BackgroundPreferences(PreferencesPanel):

    VERTICAL_GAP:   int = 5
    HORIZONTAL_GAP: int = 5

    MINI_GAP: int = 3

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Window):

        super().__init__(parent=parent)

        [self.enableBackgroundGridID, self.snapToGridID, self.scGridIntervalID, self.colorID] = PyutUtils.assignID(4)

        self._createControls()
        self._setControlValues()

    def _createControls(self):
        """
        Creates the main control and stashes them as private instance variables
        """
        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        mainSizer.Add(self.__createSimpleGridOptions(),      0, TOP | EXPAND, BackgroundPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__createGridLineColorContainer(), 0, TOP | EXPAND, BackgroundPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__createGridStyleChoice(),        0, TOP | EXPAND, BackgroundPreferences.VERTICAL_GAP)

        self.SetAutoLayout(True)
        self.SetSizer(mainSizer)

        self.Bind(EVT_COMBOBOX,         self.onGridLineColorSelectionChanged, self._cmbGridLineColor)

        self.Bind(EVT_CHECKBOX,         self.onEnableBackgroundGridChanged,   self.enableBackgroundGridID)
        self.Bind(EVT_CHECKBOX,         self.onSnapToGridChanged,             self.snapToGridID)

        self.Bind(EVT_SPINCTRL,         self.onGridIntervalChanged,           self._scGridInterval)

        self.Bind(EVT_CHOICE, self.onGridStyleChanged, self._gridStyleChoice)

    def _setControlValues(self):
        """
        TODO:   Set the default values on the controls.
        """
        if self._prefs.backgroundGridEnabled is True:
            self._cbEnableBackgroundGrid.SetValue(True)
        else:
            self._cbSnapToGrid.SetValue(False)
            self._cbSnapToGrid.Enabled = False
            self._prefs.snapToGrid = False

        if self._prefs.snapToGrid is True:
            self._cbSnapToGrid.SetValue(True)

        self._scGridInterval.SetValue(self._prefs.backgroundGridInterval)
        self._cmbGridLineColor.SetValue(self._prefs.gridLineColor.value)

        gridLineStyles: List[str] = self._gridStyleChoice.GetItems()
        selectedIndex:  int       = gridLineStyles.index(self._prefs.gridLineStyle.value)
        self._gridStyleChoice.SetSelection(selectedIndex)

    def __createSimpleGridOptions(self) -> BoxSizer:

        szrSimple: BoxSizer = BoxSizer(VERTICAL)

        cbEnableBackgroundGrid: CheckBox = CheckBox(self, self.enableBackgroundGridID, _('Enable Background Grid'))
        cbSnapToGrid:           CheckBox = CheckBox(self, self.snapToGridID,           _('Snap to Grid'))

        box:             StaticBox = StaticBox(self, ID_ANY, _("Grid Interval"))
        szrGridInterval: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL | ALIGN_LEFT)

        scGridInterval: SpinCtrl = SpinCtrl(self, self.scGridIntervalID, "")

        szrGridInterval.Add(scGridInterval, 0, LEFT | RIGHT, BackgroundPreferences.HORIZONTAL_GAP)

        szrSimple.Add(cbEnableBackgroundGrid, 0, LEFT | RIGHT, BackgroundPreferences.VERTICAL_GAP)
        szrSimple.Add(cbSnapToGrid,           0, LEFT | BOTTOM, BackgroundPreferences.VERTICAL_GAP)

        szrSimple.AddSpacer(BackgroundPreferences.VERTICAL_GAP)
        szrSimple.Add(szrGridInterval, 0, LEFT | RIGHT | TOP, BackgroundPreferences.VERTICAL_GAP)

        self._cbEnableBackgroundGrid: CheckBox = cbEnableBackgroundGrid
        self._cbSnapToGrid:           CheckBox = cbSnapToGrid
        self._scGridInterval:         SpinCtrl = scGridInterval

        return szrSimple

    def __createGridLineColorContainer(self) -> StaticBoxSizer:
        """
        Creates the grid line selection control inside a container

        Returns:
            The sizer that contains the language selection control
        """
        colorChoices = []
        for cc in MiniOglColorEnum:
            colorChoices.append(cc.value)

        self._cmbGridLineColor: ComboBox = ComboBox(self, self.colorID, choices=colorChoices, style=CB_READONLY)

        box:      StaticBox      = StaticBox(self, ID_ANY, _("Grid Line Color"))
        szrColor: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrColor.Add(self._cmbGridLineColor, 1, LEFT | RIGHT, BackgroundPreferences.MINI_GAP)

        return szrColor

    def __createGridStyleChoice(self) -> StaticBoxSizer:

        gridStyles = [s.value for s in MiniOglPenStyle]

        gridStyleChoice: Choice = Choice(self, ID_ANY, choices=gridStyles)

        box:          StaticBox      = StaticBox(self, ID_ANY, _("Grid Line Style"))
        szrGridStyle: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)
        szrGridStyle.Add(gridStyleChoice, 1, ALL, BackgroundPreferences.HORIZONTAL_GAP)

        self._gridStyleChoice: Choice = gridStyleChoice

        return szrGridStyle

    def onGridLineColorSelectionChanged(self, event: CommandEvent):

        colorValue: str = event.GetString()

        pyutColorEnum: MiniOglColorEnum = MiniOglColorEnum(colorValue)

        self._prefs.gridLineColor = pyutColorEnum

        event.Skip(True)

    def onEnableBackgroundGridChanged(self, event: CommandEvent):

        enabledValue: bool = event.IsChecked()
        BackgroundPreferences.clsLogger.warning(f'onEnableBackgroundGridChanged - {enabledValue}')
        self._prefs.backgroundGridEnabled = enabledValue
        if enabledValue is True:
            self._cbSnapToGrid.Enabled = True
        else:
            self._cbSnapToGrid.SetValue(False)
            self._cbSnapToGrid.Enabled = False
            self._prefs.snapToGrid = False
        event.Skip(True)

    def onSnapToGridChanged(self, event: CommandEvent):

        enabledValue: bool = event.IsChecked()
        BackgroundPreferences.clsLogger.info(f'onSnapToGridChanged - {enabledValue}')
        self._prefs.snapToGrid = enabledValue
        event.Skip(True)

    def onGridIntervalChanged(self, event: SpinEvent):

        newInterval: int = event.GetInt()
        self._prefs.backgroundGridInterval = newInterval
        event.Skip(True)

    def onGridStyleChanged(self, event):

        styleText: str = event.GetString()
        self.clsLogger.warning(f'{styleText=}')

        pyutPenStyle: MiniOglPenStyle = MiniOglPenStyle(styleText)

        self._prefs.gridLineStyle = pyutPenStyle
