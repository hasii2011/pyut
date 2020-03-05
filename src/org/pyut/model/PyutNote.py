
from org.pyut.model.PyutLinkedObject import PyutLinkedObject


class PyutNote(PyutLinkedObject):
    """
    Data layer representation of a UML note.
    There are currently no supplementary attributes for this class, it
    may just be linked with other objects.

    TODO:  fix inappropriate use of the .name attribute to hold the note contents;  Should have a `new` attribute
    """
    def __init__(self, theNoteText: str = ""):
        """

        Args:
            theNoteText: The Note
        """
        super().__init__(name=theNoteText)
