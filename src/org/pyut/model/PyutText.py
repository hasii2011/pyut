
from org.pyut.model.PyutObject import PyutObject


class PyutText(PyutObject):

    DEFAULT_TEXT: str = 'Text to display'       # TODO make this a preference

    def __init__(self, textContent: str = DEFAULT_TEXT):
        """

        Args:
            textContent: The text string to display
        """
        super().__init__()

        self._content: str = textContent

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, newContent: str):
        self._content = newContent
