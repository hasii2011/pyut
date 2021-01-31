
from typing import cast

from logging import Logger
from logging import getLogger

from wx import ALL
from wx import CB_READONLY
from wx import CommandEvent
from wx import EVT_CHECKBOX
from wx import EVT_COMBOBOX
from wx import HORIZONTAL
from wx import ID_ANY
from wx import VERTICAL

from wx import BoxSizer
from wx import Panel
from wx import Window
from wx import CheckBox
from wx import ComboBox

from org.pyut.dialogs.preferences.DimensionsContainer import DimensionsContainer
from org.pyut.dialogs.preferences.TextFontEnum import TextFontEnum

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _
from org.pyut.preferences.PyutPreferences import PyutPreferences


class TextAttributesContainer(Panel):
    """
    This container is self-contained in that it handles the callbacks on the UI
    controls and knows which preferences items to update
    """

    HORIZONTAL_GAP: int = 5

    def __init__(self, parent: Window):

        super().__init__(parent, ID_ANY)

        [self._cbBoldTextId, self._cbItalicizeTextId, self._cbxFontSelectionId] = PyutUtils.assignID(3)

        self.logger:       Logger          = getLogger(__name__)
        self._preferences: PyutPreferences = PyutPreferences()

        self._cbBoldText:      CheckBox = cast(CheckBox, None)
        self._cbItalicizeText: CheckBox = cast(CheckBox, None)

        szrText: BoxSizer = BoxSizer(VERTICAL)

        self._textDimensions: DimensionsContainer = DimensionsContainer(parent=self, displayText=_('Text Width/Height'), minValue=100, maxValue=300)

        szrText.Add(self._textDimensions, 0, ALL, TextAttributesContainer.HORIZONTAL_GAP)
        szrText.Add(self.__createTextStyleContainer(parent=self), 0, ALL, TextAttributesContainer.HORIZONTAL_GAP)
        szrText.Add(self.__createTextFontSelector(parent=self),   0, ALL, TextAttributesContainer.HORIZONTAL_GAP)

        self.SetSizer(szrText)
        self.Fit()

        self._bindControls()
        self._setControlValues()
        self._valueChanged: bool = False

    def _bindControls(self):

        self.Bind(EVT_CHECKBOX, self._onTextBoldValueChanged,      id=self._cbBoldTextId)
        self.Bind(EVT_CHECKBOX, self._onTextItalicizeValueChanged, id=self._cbItalicizeTextId)

        self.Bind(EVT_COMBOBOX, self._onFontSelectionChanged, id=self._cbxFontSelectionId)

    def _setControlValues(self):

        self._textDimensions.dimensions = self._preferences.textDimensions
        self._cbBoldText.SetValue(self._preferences.textBold)
        self._cbItalicizeText.SetValue(self._preferences.textItalicize)

    def _onTextBoldValueChanged(self, event: CommandEvent):

        val: bool = event.IsChecked()

        self._valueChanged = True
        self._preferences.textBold = val

    def _onTextItalicizeValueChanged(self, event: CommandEvent):

        val: bool = event.IsChecked()
        self._valueChanged = True
        self._preferences.textItalicize = val

    def _onFontSelectionChanged(self, event: CommandEvent):

        newFontName: str = event.GetString()
        self._valueChanged = True
        self._preferences.textFont = newFontName

    def __createTextStyleContainer(self, parent: Window) -> BoxSizer:

        styleContainer: BoxSizer = BoxSizer(HORIZONTAL)

        self._cbBoldText:      CheckBox = CheckBox(parent=parent, id=self._cbBoldTextId, label=_('Bold Text'))
        self._cbItalicizeText: CheckBox = CheckBox(parent=parent, id=self._cbItalicizeTextId, label=_('Italicize Text'))

        styleContainer.Add(self._cbBoldText, 0, ALL,      TextAttributesContainer.HORIZONTAL_GAP)
        styleContainer.Add(self._cbItalicizeText, 0, ALL, TextAttributesContainer.HORIZONTAL_GAP)

        return styleContainer

    def __createTextFontSelector(self, parent: Window) -> ComboBox:

        fontChoices = []
        for fontName in TextFontEnum:
            fontChoices.append(fontName.value)

        self._cbxFontSelection: ComboBox = ComboBox(parent, self._cbxFontSelectionId, choices=fontChoices, style=CB_READONLY)

        return self._cbxFontSelection
