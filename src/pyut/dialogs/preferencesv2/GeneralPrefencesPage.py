
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import Button
from wx import EVT_BUTTON
from wx import EVT_CHECKBOX

from wx import CheckBox
from wx import CommandEvent
from wx import Window

from pyut.PyutUtils import PyutUtils
from pyut.dialogs.preferencesv2.BasePreferencesPage import BasePreferencesPage
from pyut.general.datatypes.ToolBarIconSize import ToolBarIconSize
from pyut.preferences.PyutPreferences import PyutPreferences


@dataclass
class ControlData:
    label:        str      = ''
    initialValue: bool     = False
    instanceVar:  CheckBox = cast(CheckBox, None)
    wxId:         int      = 0


class GeneralPreferencesPage(BasePreferencesPage):
    """
    Implemented using sized components for better platform look and feel
    Using wx IDs to minimize callbacks
    Since these are just a bunch of checkboxes that drive true/false preferences,
    I can encapsulate creating them in a list with a dataclass that hosts all
    the necessary creation information;  How esoteric of me !!!  ;-(
    """

    def __init__(self, parent: Window):
        super().__init__(parent)
        self.SetSizerType('vertical')

        self.logger:  Logger = getLogger(__name__)
        self._change: bool   = False

        [
            self._maximizeWxId,      self._autoResizeWxId,      self._showParamsWxId,            self._showTipsWxId,
            self._centerDiagramWxId, self._toolBarIconSizeWxId, self._loadLastOpenedProjectWxId, self._displayProjectExtensionWxId,
            self._resetTipsWxId,
        ] = PyutUtils.assignID(9)

        self._btnResetTips: Button = cast(Button, None)
        p: PyutPreferences = self._preferences
        self._controlData = [
            ControlData(label='&Full Screen on startup',   initialValue=p.fullScreen,              wxId=self._maximizeWxId),
            ControlData(label='&Resize classes on edit',   initialValue=p.autoResizeShapesOnEdit,  wxId=self._autoResizeWxId),
            ControlData(label='&Show method parameters',   initialValue=p.showParameters,          wxId=self._showParamsWxId),
            ControlData(label='Show &Tips on startup',     initialValue=p.showTipsOnStartup,       wxId=self._showTipsWxId),
            ControlData(label='&Center Diagram View',      initialValue=p.centerDiagram,           wxId=self._centerDiagramWxId),
            ControlData(label='&Large Toolbar Icons',      initialValue=self._isLargeIconSize(),   wxId=self._toolBarIconSizeWxId),
            ControlData(label='Load Last &Opened Project', initialValue=p.loadLastOpenedProject,   wxId=self._loadLastOpenedProjectWxId),
            ControlData(label='Display Project Extension', initialValue=p.displayProjectExtension, wxId=self._displayProjectExtensionWxId)
        ]

        self._createWindow(parent)

    def _createWindow(self, parent: Window) :


        for cd in self._controlData:
            control: ControlData = cast(ControlData, cd)
            control.instanceVar = CheckBox(self, control.wxId, label=control.label)
            control.instanceVar.SetValue(control.initialValue)
            parent.Bind(EVT_CHECKBOX, self._onValueChanged, id=control.wxId)

        self._btnResetTips = Button(self, self._resetTipsWxId, 'Reset Tips')

        parent.Bind(EVT_BUTTON,   self._onResetTips, id=self._resetTipsWxId)

        self._fixPanelSize(panel=self)

    @property
    def name(self) -> str:
        return 'General'

    def _setControlValues(self):
        """
        I don't use this since, I am table driven
        """
        pass

    def _onValueChanged(self, event: CommandEvent):

        eventID:  int = event.GetId()
        newValue: bool = event.IsChecked()
        p:        PyutPreferences = self._preferences

        match eventID:
            case self._maximizeWxId:
                p.fullScreen = newValue
            case self._autoResizeWxId:
                p.autoResizeShapesOnEdit = newValue
            case self._showParamsWxId:
                p.showParameters = newValue
            case self._showTipsWxId:
                p.showTipsOnStartup = newValue
            case self._centerDiagramWxId:
                p.centerDiagram = newValue
            case self._toolBarIconSizeWxId:
                if newValue is True:
                    p.toolBarIconSize = ToolBarIconSize.SIZE_32
                else:
                    p.toolBarIconSize = ToolBarIconSize.SIZE_16
            case self._loadLastOpenedProjectWxId:
                p.loadLastOpenedProject = newValue
            case self._displayProjectExtensionWxId:
                p.displayProjectExtension = newValue
            case _:
                self.logger.error(f'Unknown event ID')

        self._changed = True

    # noinspection PyUnusedLocal
    def _onResetTips(self, event: CommandEvent):
        self._preferences.currentTip = 0

    def _isLargeIconSize(self) -> bool:
        if self._preferences.toolBarIconSize == ToolBarIconSize.SIZE_32:
            return True
        else:
            return False
