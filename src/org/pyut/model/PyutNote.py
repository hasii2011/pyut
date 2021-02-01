
from org.pyut.model.PyutLinkedObject import PyutLinkedObject
from org.pyut.preferences.PyutPreferences import PyutPreferences


class PyutNote(PyutLinkedObject):
    """
    A data model representation of a UML note.

    The legacy code used the base PyutObject's .name property to store the note content.  Modified to
    use a more appropriate property.  In the meantime, `PyutNote` overrides the `PyutObject's` `.getName()` and
    `.setName()` methods and raises exceptions if code calls them.  In this manner, I can catch and change all
    the current code to use the new property
    """
    def __init__(self, theNoteText: str = ''):
        """

        Args:
            theNoteText: The Note
        """
        super().__init__()

        if theNoteText is None or theNoteText == '':
            self._content = PyutPreferences().noteText
        else:
            self._content: str = theNoteText

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, newContent: str):
        self._content = newContent

