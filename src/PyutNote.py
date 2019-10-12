
from PyutLinkedObject import PyutLinkedObject


class PyutNote(PyutLinkedObject):
    """
    Data layer representation of a UML note.
    There are currently no supplementary attributes for this class, it
    may just be linked with other objects.

    :version: $Revision: 1.3 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """
    def __init__(self, theNoteText: str = ""):
        """
        Constructor.
        @param  theNoteText : The note

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        super().__init__(theNoteText)
