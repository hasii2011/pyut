
from logging import Logger
from logging import getLogger

from wx import ALL
from wx import CB_READONLY
from wx import EVT_CHECKBOX
from wx import EVT_COMBOBOX
from wx import EVT_SPINCTRL
from wx import EVT_TREE_SEL_CHANGED
from wx import EXPAND
from wx import HORIZONTAL
from wx import ID_ANY
from wx import LEFT
from wx import RIGHT
from wx import TOP
from wx import BOTTOM
from wx import TR_HAS_BUTTONS
from wx import TR_HIDE_ROOT
from wx import TR_SINGLE
from wx import VERTICAL
from wx import ALIGN_LEFT

from wx import CheckBox
from wx import CommandEvent
from wx import SpinCtrl
from wx import SpinEvent
from wx import StaticBox
from wx import StaticBoxSizer
from wx import TreeEvent
from wx import TreeCtrl
from wx import BoxSizer
from wx import ComboBox
from wx import Window
from wx import TreeItemId

from org.pyut.dialogs.preferences.PreferencesPanel import PreferencesPanel

from org.pyut.miniogl.PyutColorEnum import PyutColorEnum

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _
from org.pyut.miniogl.PyutPenStyle import PyutPenStyle


class BackgroundPreferences(PreferencesPanel):

    VERTICAL_GAP:   int = 5
    HORIZONTAL_GAP: int = 5

    MINI_GAP: int = 3

    PEN_STYLE_CATEGORY_DASHED_LINES: str = 'Dashed Lines'
    PEN_STYLE_CATEGORY_HATCH_LINES:  str = 'Hatch Lines'

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Window):

        super().__init__(parent=parent)

        [self.enableBackgroundGridID, self.snapToGridID, self.scGridIntervalID, self.colorID] = PyutUtils.assignID(4)

        self._createControls()
        self.__setControlValues()

    def _createControls(self):
        """
        Creates the main control and stashes them as private instance variables
        """
        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        mainSizer.Add(self.__createSimpleGridOptions(),      1, TOP | EXPAND, BackgroundPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__createGridLineColorContainer(), 1, TOP | EXPAND, BackgroundPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__createGridStyleComboTree(),     1, TOP | EXPAND, BackgroundPreferences.VERTICAL_GAP)

        self.SetAutoLayout(True)
        self.SetSizer(mainSizer)

        self.Bind(EVT_TREE_SEL_CHANGED, self.onPenStyleSelectionChanged,      self._treeList)
        self.Bind(EVT_COMBOBOX,         self.onGridLineColorSelectionChanged, self._cmbGridLineColor)

        self.Bind(EVT_CHECKBOX,         self.onEnableBackgroundGridChanged,   self.enableBackgroundGridID)
        self.Bind(EVT_CHECKBOX,         self.onSnapToGridChanged,             self.snapToGridID)

        self.Bind(EVT_SPINCTRL,         self.onGridIntervalChanged,           self._scGridInterval)

    def __setControlValues(self):
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
        for cc in PyutColorEnum:
            colorChoices.append(cc.value)

        self._cmbGridLineColor: ComboBox = ComboBox(self, self.colorID, choices=colorChoices, style=CB_READONLY)

        box:      StaticBox      = StaticBox(self, ID_ANY, _("Grid Line Color"))
        szrColor: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrColor.Add(self._cmbGridLineColor, 1, LEFT | RIGHT, BackgroundPreferences.MINI_GAP)

        return szrColor

    def __createGridStyleComboTree(self) -> StaticBoxSizer:

        treeList:         TreeCtrl     = TreeCtrl(self, ID_ANY, style=TR_SINGLE | TR_HAS_BUTTONS | TR_HIDE_ROOT)

        treeRoot = treeList.AddRoot("The Root Item")

        treeList.AppendItem(treeRoot, PyutPenStyle.SOLID.value)
        treeList.AppendItem(treeRoot, PyutPenStyle.DOT.value)

        dashItem: TreeItemId = treeList.AppendItem(treeRoot, BackgroundPreferences.PEN_STYLE_CATEGORY_DASHED_LINES)
        treeList.AppendItem(dashItem, PyutPenStyle.DOT_DASH.value)
        treeList.AppendItem(dashItem, PyutPenStyle.LONG_DASH.value)
        treeList.AppendItem(dashItem, PyutPenStyle.SHORT_DASH.value)

        hatchItem: TreeItemId = treeList.AppendItem(treeRoot, BackgroundPreferences.PEN_STYLE_CATEGORY_HATCH_LINES)
        hatchStyles = [
            PyutPenStyle.CROSS_HATCH,
            PyutPenStyle.HORIZONTAL_HATCH,
            PyutPenStyle.VERTICAL_HATCH
        ]
        for hStyle in hatchStyles:
            treeList.AppendItem(hatchItem, hStyle.value)

        treeList.ExpandAll()

        box:          StaticBox      = StaticBox(self, ID_ANY, _("Grid Line Style"))
        szrGridStyle: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)
        szrGridStyle.Add(treeList, 1, ALL, BackgroundPreferences.HORIZONTAL_GAP)

        self._treeList: TreeCtrl = treeList

        return szrGridStyle

    def onPenStyleSelectionChanged(self, event: TreeEvent):

        item = event.GetItem()
        if item is not None:

            treeList: TreeCtrl = self._treeList
            itemText: str      = treeList.GetItemText(item)

            self.clsLogger.debug(f'OnSelChanged: {itemText}')
            if itemText == BackgroundPreferences.PEN_STYLE_CATEGORY_DASHED_LINES or itemText == BackgroundPreferences.PEN_STYLE_CATEGORY_HATCH_LINES:
                treeList.Unselect()
            else:
                pyutPenStyle: PyutPenStyle = PyutPenStyle(itemText)
                self._prefs.gridLineStyle = pyutPenStyle

        event.Skip(True)

    def onGridLineColorSelectionChanged(self, event: CommandEvent):

        colorValue: str = event.GetString()

        pyutColorEnum: PyutColorEnum = PyutColorEnum(colorValue)

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
