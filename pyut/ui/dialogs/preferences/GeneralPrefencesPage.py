from pathlib import Path
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import EVT_BUTTON
from wx import EVT_CHECKBOX
from wx import EVT_RADIOBOX
from wx import EVT_SPINCTRL
from wx import ID_ANY
from wx import RA_SPECIFY_COLS

from wx import Button
from wx import CheckBox
from wx import CommandEvent
from wx import RadioBox
from wx import SpinCtrl
from wx import SpinEvent
from wx import Window

from wx import NewIdRef as wxNewIdRef


from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from codeallyadvanced.ui.widgets.DirectorySelector import DirectorySelector

from pyut.preferences.FileHistoryPreference import FileHistoryPreference
from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.dialogs.preferences.BasePreferencesPage import BasePreferencesPage

from pyut.general.datatypes.ToolBarIconSize import ToolBarIconSize

# from pyut.resources.img import folder as ImgFolder


@dataclass
class ControlData:
    label:        str      = ''
    initialValue: bool     = False
    instanceVar:  CheckBox = cast(CheckBox, None)
    wxId:         int      = 0


class GeneralPreferencesPage(BasePreferencesPage):
    """
    Implemented using sized components for better platform look and feel
    Since these are a bunch of checkboxes that drive true/false preferences,
    I can encapsulate creating them in a list with a dataclass that hosts all
    the necessary creation information;  How esoteric of me !!!  ;-(
    """
    MAXIMIZE_ID:                  int = wxNewIdRef()
    AUTO_RESIZE_ID:               int = wxNewIdRef()
    SHOW_TIPS_ID:                 int = wxNewIdRef()
    TOOLBAR_ICON_SIZE_ID:         int = wxNewIdRef()
    LOAD_LAST_OPENED_PROJECT_ID:  int = wxNewIdRef()
    DISPLAY_PROJECT_EXTENSION_ID: int = wxNewIdRef()

    def __init__(self, parent: Window):
        super().__init__(parent)
        self.SetSizerType('vertical')

        self.logger:  Logger = getLogger(__name__)
        self._change: bool   = False

        self._btnResetTips:        Button            = cast(Button, None)
        self._virtualWindowWidth:  SpinCtrl          = cast(SpinCtrl, None)
        self._fileHistoryPathPref: RadioBox          = cast(RadioBox, None)
        self._directorySelector:   DirectorySelector = cast(DirectorySelector, None)

        p: PyutPreferences = self._preferences
        self._controlData = [
            ControlData(label='&Full Screen on startup',   initialValue=p.fullScreen,              wxId=GeneralPreferencesPage.MAXIMIZE_ID),
            ControlData(label='&Resize classes on edit',   initialValue=p.autoResizeShapesOnEdit,  wxId=GeneralPreferencesPage.AUTO_RESIZE_ID),
            ControlData(label='Show &Tips on startup',     initialValue=p.showTipsOnStartup,       wxId=GeneralPreferencesPage.SHOW_TIPS_ID),
            ControlData(label='&Large Toolbar Icons',      initialValue=self._isLargeIconSize(),   wxId=GeneralPreferencesPage.TOOLBAR_ICON_SIZE_ID),
            ControlData(label='Load Last &Opened Project', initialValue=p.loadLastOpenedProject,   wxId=GeneralPreferencesPage.LOAD_LAST_OPENED_PROJECT_ID),
            ControlData(label='Display Project Extension', initialValue=p.displayProjectExtension, wxId=GeneralPreferencesPage.DISPLAY_PROJECT_EXTENSION_ID)
        ]

        self._layoutWindow(sizedPanel=self)

    def _layoutWindow(self, sizedPanel: SizedPanel):

        self._layoutTrueFalsePreferences(sizedPanel)

        self._btnResetTips = Button(sizedPanel, ID_ANY, 'Reset Tips')

        self._layoutVWandFHPanel(parentPanel=sizedPanel)

        self._layoutDiagramsDirectory(sizedPanel)

        self._setControlValues()

        sizedPanel.Bind(EVT_SPINCTRL, self._onVirtualWindowWidthChanged,  self._virtualWindowWidth)
        sizedPanel.Bind(EVT_RADIOBOX, self._onFileHistoryPathPrefChanged, self._fileHistoryPathPref)
        sizedPanel.Bind(EVT_BUTTON,   self._onResetTips,                  self._btnResetTips)

        self._fixPanelSize(panel=self)

    @property
    def name(self) -> str:
        return 'General'

    def _layoutTrueFalsePreferences(self, parentPanel: SizedPanel):
        """
        I represent this in the UI with a CheckBox
        Args:
            parentPanel:
        """
        trueFalsePanel: SizedStaticBox = SizedStaticBox(parentPanel, label='')
        trueFalsePanel.SetSizerType('Vertical')
        trueFalsePanel.SetSizerProps(expand=True, proportion=3)

        for cd in self._controlData:
            control: ControlData = cast(ControlData, cd)
            control.instanceVar = CheckBox(trueFalsePanel, id=control.wxId, label=control.label)
            control.instanceVar.SetValue(control.initialValue)
            parentPanel.Bind(EVT_CHECKBOX, self._onTrueFalsePreferenceChanged, control.instanceVar)

    def _layoutVWandFHPanel(self, parentPanel: SizedPanel):
        """
        Layout the virtual window size control and the FileHistory Preference selection
        controls in a horizontal panel

        Args:
            parentPanel:
        """
        hPanel: SizedPanel = SizedPanel(parentPanel)
        hPanel.SetSizerType('horizontal')
        hPanel.SetSizerProps(expand=False, proportion=2)

        self._layoutVirtualWindowWidthControl(parentPanel=hPanel)
        self._layoutFileHistoryPreferenceControl(parentPanel=hPanel)

    def _layoutDiagramsDirectory(self, sizedPanel: SizedPanel):

        dsPanel: SizedStaticBox = SizedStaticBox(sizedPanel, label='Diagrams Directory ')
        dsPanel.SetSizerProps(expand=True, proportion=1)

        self._directorySelector = DirectorySelector(parent=dsPanel, pathChangedCallback=self._pathChangedCallback)
        self._directorySelector.SetSizerProps(expand=True, proportion=1)

    def _layoutVirtualWindowWidthControl(self, parentPanel: SizedPanel):

        wrapperBox: SizedStaticBox = SizedStaticBox(parentPanel, label='Virtual Window Width')
        wrapperBox.SetSizerType('vertical')
        wrapperBox.SetSizerProps(expand=True, proportion=2)

        virtualWindowWidth = SpinCtrl(wrapperBox, id=ID_ANY, min=1000, max=25000, size=(75, 25))

        self._virtualWindowWidth = virtualWindowWidth

    def _layoutFileHistoryPreferenceControl(self, parentPanel: SizedPanel):

        options: List[str] = [
            FileHistoryPreference.SHOW_NEVER.value,
            FileHistoryPreference.SHOW_ALWAYS.value,
            FileHistoryPreference.SHOW_IF_DIFFERENT.value
        ]

        rb: RadioBox = RadioBox(parent=parentPanel,
                                id=ID_ANY,
                                label='File History Path Style',
                                choices=options,
                                majorDimension=1,
                                style=RA_SPECIFY_COLS)

        self._fileHistoryPathPref = rb

    def _setControlValues(self):
        """

        """
        self._directorySelector.directoryPath = self._preferences.diagramsDirectory
        self._virtualWindowWidth.SetValue(self._preferences.virtualWindowWidth)

        chosen: str = self._preferences.fileHistoryDisplay.value
        idx:    int = self._fileHistoryPathPref.FindString(chosen)

        self._fileHistoryPathPref.SetSelection(idx)

    def _onTrueFalsePreferenceChanged(self, event: CommandEvent):

        eventID:  int = event.GetId()
        newValue: bool = event.IsChecked()
        p:        PyutPreferences = self._preferences

        match eventID:
            case GeneralPreferencesPage.MAXIMIZE_ID:
                p.fullScreen = newValue
            case GeneralPreferencesPage.AUTO_RESIZE_ID:
                p.autoResizeShapesOnEdit = newValue
            case GeneralPreferencesPage.SHOW_TIPS_ID:
                p.showTipsOnStartup = newValue
            case GeneralPreferencesPage.TOOLBAR_ICON_SIZE_ID:
                if newValue is True:
                    p.toolBarIconSize = ToolBarIconSize.SIZE_32
                else:
                    p.toolBarIconSize = ToolBarIconSize.SIZE_16
            case GeneralPreferencesPage.LOAD_LAST_OPENED_PROJECT_ID:
                p.loadLastOpenedProject = newValue
            case GeneralPreferencesPage.DISPLAY_PROJECT_EXTENSION_ID:
                p.displayProjectExtension = newValue
            case _:
                self.logger.error(f'Unknown event ID')

        self._changed = True

    # noinspection PyUnusedLocal
    def _onResetTips(self, event: CommandEvent):
        self._preferences.currentTip = 0

    def _onFileHistoryPathPrefChanged(self, event: CommandEvent):

        newValue: str = event.GetString()
        self.logger.info(f'File History Path Preferences changed.  {newValue=}')
        newPreference: FileHistoryPreference = FileHistoryPreference(newValue)
        self._preferences.fileHistoryDisplay = newPreference

    # noinspection PyUnusedLocal
    def _onVirtualWindowWidthChanged(self, event: SpinEvent):

        self._preferences.virtualWindowWidth = self._virtualWindowWidth.GetValue()

    def _pathChangedCallback(self, newPath: Path):
        self._preferences.diagramsDirectory = str(newPath)

    def _isLargeIconSize(self) -> bool:
        if self._preferences.toolBarIconSize == ToolBarIconSize.SIZE_32:
            return True
        else:
            return False
