from logging import Logger
from logging import getLogger
from typing import cast

from ogl.OglDimensions import OglDimensions
from ogl.OglTextFontFamily import OglTextFontFamily
from wx import CB_READONLY
from wx import CheckBox
from wx import ComboBox
from wx import StaticBoxSizer
from wx import Window
from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from pyut.preferences.PyutPreferences import PyutPreferences
from pyut.ui.widgets.DimensionsControl import DimensionsControl


class TextAttributesControl(SizedPanel):

    def __init__(self, parent: Window):

        self.logger:       Logger          = getLogger(__name__)
        self._preferences: PyutPreferences = PyutPreferences()
        super().__init__(parent)

        self._textDimensions: DimensionsControl = DimensionsControl(sizedPanel=self,
                                                                    displayText='Text Width/Height',
                                                                    valueChangedCallback=self._onTextDimensionsChanged,
                                                                    setControlsSize=False
                                                                    )
        self._boldText:      CheckBox = cast(CheckBox, None)
        self._italicizeText: CheckBox = cast(CheckBox, None)
        self._fontSelector:  ComboBox = cast(ComboBox, None)

        # self._createTextStyleContainer(self)
        self._createTextFontSelectorContainer(self)
        self._setControlValues()

    def _setControlValues(self):

        self._textDimensions.dimensions = self._preferences.textDimensions
        # self._boldText.SetValue(self._preferences.textBold)
        # self._italicizeText.SetValue(self._preferences.textItalicize)

    def _onTextDimensionsChanged(self, newValue: OglDimensions):
        self._preferences.textDimensions = newValue

    def _createTextStyleContainer(self, parent: SizedPanel):

        stylePanel: SizedPanel = SizedPanel(parent)
        stylePanel.SetSizerType('horizontal')
        stylePanel.SetSizerProps(expand=True, proportion=1)

        self._boldText      = CheckBox(parent=stylePanel, label='Bold Text')
        self._italicizeText = CheckBox(parent=stylePanel, label='Italicize Text')

    def _createTextFontSelectorContainer(self, parent: SizedPanel):

        fontChoices = []
        for fontName in OglTextFontFamily:
            fontChoices.append(fontName.value)

        fontPanel: SizedStaticBox = SizedStaticBox(parent, label='Text Font Family')
        fontPanel.SetSizerType('horizontal')
        fontPanel.SetSizerProps(expand=True, proportion=1)

        self._fontSelector = ComboBox(fontPanel, choices=fontChoices, style=CB_READONLY)
        self._fontSelector.SetSizerProps(expand=True, proportion=1)

