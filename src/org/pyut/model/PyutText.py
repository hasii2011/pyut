
from org.pyut.dialogs.preferences.widgets.TextFontEnum import TextFontEnum

from org.pyut.model.PyutObject import PyutObject

from org.pyut.preferences.PyutPreferences import PyutPreferences


class PyutText(PyutObject):
    """
    The model has to remember additional text attributes
    """

    DEFAULT_TEXT:       str  = 'Text to display'

    def __init__(self, textContent: str = DEFAULT_TEXT):
        """

        Args:
            textContent: The text string to display
        """
        super().__init__()

        preferences: PyutPreferences = PyutPreferences()

        self._content:      str  = textContent
        self._textSize:     int  = preferences.textFontSize
        self._isBold:       bool = preferences.textBold
        self._isItalicized: bool = preferences.textItalicize

        self._textFont:       TextFontEnum = preferences.textFont

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, newContent: str):
        self._content = newContent

    @property
    def textSize(self) -> int:
        return self._textSize

    @textSize.setter
    def textSize(self, newSize: int):
        self._textSize = newSize

    @property
    def isBold(self) -> bool:
        return self._isBold

    @isBold.setter
    def isBold(self, newValue: bool):
        self._isBold = newValue

    @property
    def isItalicized(self) -> bool:
        return self._isItalicized

    @isItalicized.setter
    def isItalicized(self, newValue: bool):
        self._isItalicized = newValue

    @property
    def textFont(self) -> TextFontEnum:
        return self._textFont

    @textFont.setter
    def textFont(self, newValue: TextFontEnum):
        self._textFont = newValue
