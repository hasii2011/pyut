
from typing import List
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
from wx import LEFT
from wx import RIGHT
from wx import StaticBox
from wx import StaticBoxSizer
from wx import VERTICAL

from wx import BoxSizer
from wx import Panel
from wx import Window
from wx import CheckBox
from wx import ComboBox

from org.pyut.ui.widgets.DimensionsContainer import DimensionsContainer

from org.pyut.PyutUtils import PyutUtils

# noinspection PyProtectedMember
from org.pyut.general.Globals import _

from ogl.OglTextFontFamily import OglTextFontFamily
from ogl.OglDimensions import OglDimensions

from org.pyut.preferences.PyutPreferences import PyutPreferences


class TextAttributesContainer(Panel):
    """
    This container is self-contained in that it handles the callbacks on the UI
    controls and knows which preferences items to update
    """

    HORIZONTAL_GAP: int = 5
    MINI_GAP:       int = 3

    def __init__(self, parent: Window):

        super().__init__(parent, ID_ANY)

        [self._cbBoldTextId, self._cbItalicizeTextId, self._cbxFontSelectorId, self._cbxFontSizeSelectorId] = PyutUtils.assignID(4)

        self.logger:       Logger          = getLogger(__name__)
        self._preferences: PyutPreferences = PyutPreferences()
        #
        # Controls we are going to create
        #
        self._cbBoldText:          CheckBox = cast(CheckBox, None)
        self._cbItalicizeText:     CheckBox = cast(CheckBox, None)
        self._cbxFontSelector:     ComboBox = cast(ComboBox, None)
        self._cbxFontSizeSelector: ComboBox = cast(ComboBox, None)

        szrText: BoxSizer = BoxSizer(VERTICAL)

        self._textDimensions: DimensionsContainer = DimensionsContainer(parent=self,
                                                                        displayText=_('Text Width/Height'),
                                                                        valueChangedCallback=self._onTextDimensionsChanged
                                                                        )

        szrText.Add(self._textDimensions, 0, ALL, TextAttributesContainer.HORIZONTAL_GAP)
        szrText.Add(self.__createTextStyleContainer(parent=self), 0, ALL, TextAttributesContainer.HORIZONTAL_GAP)
        szrText.Add(self.__createFontAttributeContainer(parent=self),   0, ALL, TextAttributesContainer.HORIZONTAL_GAP)

        self.SetSizer(szrText)
        self.Fit()

        self._bindControls()
        self._setControlValues()

    def _bindControls(self):

        self.Bind(EVT_CHECKBOX, self._onTextBoldValueChanged,      id=self._cbBoldTextId)
        self.Bind(EVT_CHECKBOX, self._onTextItalicizeValueChanged, id=self._cbItalicizeTextId)

        self.Bind(EVT_COMBOBOX, self._onFontSelectionChanged,     id=self._cbxFontSelectorId)
        self.Bind(EVT_COMBOBOX, self._onFontSizeSelectionChanged, id=self._cbxFontSizeSelectorId)

    def _setControlValues(self):

        self._textDimensions.dimensions = self._preferences.textDimensions
        self._cbBoldText.SetValue(self._preferences.textBold)
        self._cbItalicizeText.SetValue(self._preferences.textItalicize)
        self._cbxFontSelector.SetValue(self._preferences.textFontFamily.value)
        self._cbxFontSizeSelector.SetValue(str(self._preferences.textFontSize))

    def _onTextDimensionsChanged(self, newValue: OglDimensions):
        self._preferences.textDimensions = newValue

    def _onTextBoldValueChanged(self, event: CommandEvent):

        val: bool = event.IsChecked()

        self._preferences.textBold = val

    def _onTextItalicizeValueChanged(self, event: CommandEvent):

        val: bool = event.IsChecked()
        self._preferences.textItalicize = val

    def _onFontSelectionChanged(self, event: CommandEvent):

        newFontName: str          = event.GetString()
        fontEnum:    OglTextFontFamily = OglTextFontFamily(newFontName)

        self._preferences.textFontFamily = fontEnum

    def _onFontSizeSelectionChanged(self, event: CommandEvent):

        newFontSize: str = event.GetString()

        self._preferences.textFontSize = int(newFontSize)

    def __createTextStyleContainer(self, parent: Window) -> BoxSizer:

        styleContainer: BoxSizer = BoxSizer(HORIZONTAL)

        self._cbBoldText      = CheckBox(parent=parent, id=self._cbBoldTextId,      label=_('Bold Text'))
        self._cbItalicizeText = CheckBox(parent=parent, id=self._cbItalicizeTextId, label=_('Italicize Text'))

        styleContainer.Add(self._cbBoldText,      0, ALL, TextAttributesContainer.HORIZONTAL_GAP)
        styleContainer.Add(self._cbItalicizeText, 0, ALL, TextAttributesContainer.HORIZONTAL_GAP)

        return styleContainer

    def __createFontAttributeContainer(self, parent: Window) -> BoxSizer:

        attributeContainer: BoxSizer = BoxSizer(HORIZONTAL)

        attributeContainer.Add(self.__createTextFontSelectorContainer(parent), 0, ALL, TextAttributesContainer.HORIZONTAL_GAP)
        attributeContainer.Add(self.__createTextSizeSelectorContainer(parent), 0, ALL, TextAttributesContainer.HORIZONTAL_GAP)

        return attributeContainer

    def __createTextFontSelectorContainer(self, parent: Window) -> StaticBoxSizer:

        fontChoices = []
        for fontName in OglTextFontFamily:
            fontChoices.append(fontName.value)

        box:     StaticBox      = StaticBox(self, ID_ANY, _("Text Font Family"))
        szrFont: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        self._cbxFontSelector = ComboBox(parent, self._cbxFontSelectorId, choices=fontChoices, style=CB_READONLY)

        szrFont.Add(self._cbxFontSelector, 1, LEFT | RIGHT, TextAttributesContainer.MINI_GAP)

        return szrFont

    def __createTextSizeSelectorContainer(self, parent: Window) -> StaticBoxSizer:

        box:         StaticBox      = StaticBox(self, ID_ANY, _("Font Size"))
        szrFontSize: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        fontSizes: List[str] = ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        self._cbxFontSizeSelector = ComboBox(parent, self._cbxFontSizeSelectorId, choices=fontSizes, style=CB_READONLY)

        szrFontSize.Add(self._cbxFontSizeSelector, 1, LEFT | RIGHT, TextAttributesContainer.MINI_GAP)

        return szrFontSize
