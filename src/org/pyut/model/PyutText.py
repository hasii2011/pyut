
from org.pyut.model.PyutObject import PyutObject

from org.pyut.ogl.OglTextFontType import OglTextFontType


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
        self._content:      str  = textContent

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
    def textFont(self) -> OglTextFontType:
        return self._textFont

    @textFont.setter
    def textFont(self, newValue: OglTextFontType):
        self._textFont = newValue
