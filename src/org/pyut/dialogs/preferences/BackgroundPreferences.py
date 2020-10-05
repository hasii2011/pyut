
from logging import Logger
from logging import getLogger

from wx import ALL
from wx import CB_READONLY
from wx import CheckBox
from wx import EVT_TREE_SEL_CHANGED
from wx import EXPAND
from wx import HORIZONTAL
from wx import ID_ANY
from wx import LEFT
from wx import RIGHT
from wx import SpinCtrl
from wx import StaticBox
from wx import StaticBoxSizer
from wx import TOP

from wx import TR_HAS_BUTTONS
from wx import TR_HIDE_ROOT
from wx import TR_SINGLE
from wx import TreeEvent
from wx import VERTICAL

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

        [self.colorID, self.enableBackgroundGridID, self.scGridIntervalID] = PyutUtils.assignID(3)

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

    def __setControlValues(self):
        """
        TODO:   Set the default values on the controls.
        """
        if self._prefs.backgroundGridEnabled is True:
            self._cbEnableBackgroundGrid.SetValue(True)
        self._scGridInterval.SetValue(self._prefs.backgroundGridInterval)

    def __createSimpleGridOptions(self) -> BoxSizer:

        szrSimple: BoxSizer = BoxSizer(VERTICAL)

        cbEnableBackgroundGrid: CheckBox = CheckBox(self, self.enableBackgroundGridID, _('Enable Background Grid'))

        box:             StaticBox = StaticBox(self, ID_ANY, _("Grid Interval"))
        szrGridInterval: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        scGridInterval: SpinCtrl = SpinCtrl(self, self.scGridIntervalID, "")

        szrGridInterval.Add(scGridInterval, 0, LEFT | RIGHT, BackgroundPreferences.HORIZONTAL_GAP)

        szrSimple.Add(cbEnableBackgroundGrid, 0, LEFT | RIGHT, BackgroundPreferences.VERTICAL_GAP)
        szrSimple.Add(szrGridInterval, 0, LEFT | RIGHT | TOP, BackgroundPreferences.VERTICAL_GAP)

        self._cbEnableBackgroundGrid: CheckBox = cbEnableBackgroundGrid
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

        self.__cmbGridLineColor: ComboBox = ComboBox(self, self.colorID, choices=colorChoices, style=CB_READONLY)

        box:      StaticBox      = StaticBox(self, ID_ANY, _("Grid Line Color"))
        szrColor: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrColor.Add(self.__cmbGridLineColor, 1, LEFT | RIGHT, BackgroundPreferences.MINI_GAP)

        return szrColor

    def __createGridStyleComboTree(self) -> StaticBoxSizer:

        treeList:         TreeCtrl     = TreeCtrl(self, ID_ANY, style=TR_SINGLE | TR_HAS_BUTTONS | TR_HIDE_ROOT)

        treeRoot = treeList.AddRoot("The Root Item")

        treeList.AppendItem(treeRoot, PyutPenStyle.SOLID.value)
        treeList.AppendItem(treeRoot, PyutPenStyle.DOT.value)
        treeList.AppendItem(treeRoot, PyutPenStyle.TRANSPARENT.value)

        dashItem: TreeItemId = treeList.AppendItem(treeRoot, BackgroundPreferences.PEN_STYLE_CATEGORY_DASHED_LINES)
        treeList.AppendItem(dashItem, PyutPenStyle.DOT_DASH.value)
        treeList.AppendItem(dashItem, PyutPenStyle.LONG_DASH.value)
        treeList.AppendItem(dashItem, PyutPenStyle.SHORT_DASH.value)

        hatchItem: TreeItemId = treeList.AppendItem(treeRoot, BackgroundPreferences.PEN_STYLE_CATEGORY_HATCH_LINES)
        hatchStyles = [
            PyutPenStyle.BACKWARD_DIAGONAL_HATCH,
            PyutPenStyle.CROSS_DIAGONAL_HATCH,
            PyutPenStyle.FORWARD_DIAGONAL_HATCH,
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

        self.Bind(EVT_TREE_SEL_CHANGED, self.onSelectionChanged, treeList)
        self._treeList: TreeCtrl = treeList

        return szrGridStyle

    def onSelectionChanged(self, event: TreeEvent):

        item = event.GetItem()
        if item is not None:

            treeList: TreeCtrl = self._treeList
            itemText: str      = treeList.GetItemText(item)

            self.clsLogger.debug(f'OnSelChanged: {itemText}')
            if itemText == BackgroundPreferences.PEN_STYLE_CATEGORY_DASHED_LINES or itemText == BackgroundPreferences.PEN_STYLE_CATEGORY_HATCH_LINES:
                treeList.Unselect()

        event.Skip(True)
