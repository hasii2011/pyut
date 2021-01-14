
from org.pyut.model.PyutObject import PyutObject


class PyutText(PyutObject):

    DEFAULT_TEXT:       str  = 'Text to display'    # TODO make this a preference
    DEFAULT_TEXT_SIZE:  int  = 12                   # TODO make this a preference
    DEFAULT_BOLD:       bool = False                # TODO make this a preference
    DEFAULT_ITALICIZED: bool = False                # TODO make this a preference

    def __init__(self, textContent: str = DEFAULT_TEXT):
        """

        Args:
            textContent: The text string to display
        """
        super().__init__()

        self._content:      str = textContent
        self._textSize:     int = PyutText.DEFAULT_TEXT_SIZE
        self._isBold:       bool = PyutText.DEFAULT_BOLD
        self._isItalicized: bool = PyutText.DEFAULT_ITALICIZED

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
