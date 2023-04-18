from typing import cast

from logging import Logger
from logging import getLogger

from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_TEXT
from wx import ID_ANY
from wx import RA_SPECIFY_ROWS
from wx import STAY_ON_TOP

from wx import Colour
from wx import CommandEvent
from wx import DefaultSize
from wx import Point
from wx import RadioBox
from wx import StaticText
from wx import TextCtrl
from wx import Window

from wx.lib.sized_controls import SizedPanel

from pyut.uiv2.dialogs.BaseEditDialog import BaseEditDialog


class BaseEditParamFieldDialog(BaseEditDialog):
    """
    Common class for laying out controls to edit either a field or a parameter
    """
    basePFDLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Window, title, layoutField: bool=True):
        """

        Args:
            parent:
            title:    The dialog title appropriate for this invocation of the editor
            layoutField: If 'True' includes the visibility radio buttons for a field
        """

        super().__init__(parent, title=title)

        self._rdbVisibility: RadioBox = cast(RadioBox, None)
        self._name:          TextCtrl = cast(TextCtrl, None)
        self._type:          TextCtrl = cast(TextCtrl, None)
        self._defaultValue:  TextCtrl = cast(TextCtrl, None)

        sizedPanel: SizedPanel = self.GetContentsPane()

        self._layoutEditControls(sizedPanel, layoutField)
        self._layoutStandardOkCancelButtonSizer()

        self._normalNameBackgroundColour: Colour = self._name.GetBackgroundColour()

        self.basePFDLogger.warning(f'{self._normalNameBackgroundColour=}')

        self.Bind(EVT_TEXT, self._onNameChange, self._name)
        self.basePFDLogger.info(f'Name change event is registered')

    def _layoutEditControls(self, parent: SizedPanel, layoutField: bool):

        controlsPanel: SizedPanel = SizedPanel(parent)
        controlsPanel.SetSizerType('horizontal')

        if layoutField is True:
            self._rdbVisibility = RadioBox(controlsPanel, ID_ANY, "", Point(35, 30), DefaultSize, ["+", "-", "#"], style=RA_SPECIFY_ROWS)

        gridPanel: SizedPanel = SizedPanel(parent=controlsPanel)
        gridPanel.SetSizerType("grid", {"cols":3}) # 3-column grid layout

        StaticText(gridPanel, label="Name").SetSizerProps(proportion=1)
        StaticText(gridPanel, label="Type").SetSizerProps(proportion=1)
        StaticText(gridPanel, label="Default Value").SetSizerProps(proportion=1)

        self._name         = TextCtrl(gridPanel, value="", size=(140,-1))  #
        self._type         = TextCtrl(gridPanel, value="", size=(100,-1))  #
        self._defaultValue = TextCtrl(gridPanel, value="", size=(80,-1))  #

    # noinspection PyUnusedLocal
    def _onNameChange(self, event: CommandEvent):
        updatedName: str = self._name.GetValue().strip()
        self.basePFDLogger.warning(f'{updatedName=}')
        if  self._name.GetValue().strip() == '':
            self._indicateEmptyTextCtrl(name=self._name)
        else:
            self._indicateNonEmptyTextCtrl(name=self._name, normalBackgroundColor=self._normalNameBackgroundColour)
