
from pyutmodel.PyutLinkedObject import PyutLinkedObject


class PyutNote(PyutLinkedObject):
    """
    A data model representation of a UML note.

    The legacy code used the base PyutObject's .name property to store the note content.  Modified to
    use a more appropriate property.  In the meantime, `PyutNote` overrides the `PyutObject's` `.getName()` and
    `.setName()` methods and raises exceptions if code calls them.  In this manner, I can catch and change all
    the current code to use the new property
    """
    def __init__(self, noteText: str = ''):
        """

        Args:
            noteText: The Note
        """
        super().__init__()

        self._content = noteText

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, newContent: str):
        self._content = newContent
