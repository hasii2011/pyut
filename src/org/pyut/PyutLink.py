
from logging import Logger
from logging import getLogger

from org.pyut.PyutLinkedObject import PyutLinkedObject
from org.pyut.PyutObject import PyutObject
from org.pyut.enums.OglLinkType import OglLinkType

from org.pyut.general.Globals import _


class PyutLink(PyutObject):
    """
    A standard link between Class or Note.

    A PyutLink represents a UML link between Class in Pyut.

    Example:
    ```python

        myLink  = PyutLink("linkName", OglLinkType.OGL_INHERITANCE, "0", "*")
    ```
    """

    def __init__(self, name="", linkType: OglLinkType = OglLinkType.OGL_INHERITANCE,
                 cardSrc: str = "", cardDest: str = "",
                 bidir: bool = False, source: PyutLinkedObject = None, destination: PyutLinkedObject = None):
        """

        Args:
            name:        The link name
            linkType:    The enum represening the link type
            cardSrc:     The source cardinality
            cardDest:    The destination cardinality
            bidir:      `True` if the link is bidirectional, else `False`
            source:      The source of the link
            destination: The destination of the link
        """
        super().__init__(name)
        self.logger: Logger       = getLogger(__name__)
        self._type:  OglLinkType = linkType

        self._sourceCardinality:      str  = cardSrc
        self._destinationCardinality: str  = cardDest
        self._bidirectional:          bool = bidir

        self._src:  PyutLinkedObject = source
        self._dest: PyutLinkedObject = destination

    def getSrcCard(self) -> str:
        """
        Return a string representing cardinality source.

        @return string source cardinality
        """
        return self._sourceCardinality

    def setSrcCard(self, cardSrc: str):
        """
        Updating source cardinality.

        @param  cardSrc
        """
        self._sourceCardinality = cardSrc

    def getDestCard(self):
        """
        Return a string representing cardinality destination.

        @return string destination cardinality
        """
        return self._destinationCardinality

    def setDestCard(self, cardDest: str):
        """
        Updating destination cardinality.

        @param cardDest
        """
        self._destinationCardinality = cardDest

    def getSource(self):
        """
        Return the source object of the link

        @return object Class or Note
        """
        return self._src

    def setSource(self, source):
        """
        Set the source object of this link.

        @param  source  PyutClass or PyutNote
        """
        self._src = source

    def getDestination(self):
        """
        Return an object destination who is linked to this link.

        @return object Class or Note
        """
        return self._dest

    def setDestination(self, destination):
        """
        Updating destination.

        @param destination -- PyutClass or PyutNote
        """
        self._dest = destination

    def getBidir(self) -> bool:
        """
        To know if the link is bidirectional.

        @return boolean
        """
        return self._bidirectional

    def setBidir(self, bidirectional: bool):
        """
        Updating bidirectional.

        @param bidirectional
        """
        self._bidirectional = bidirectional

    def setType(self, theType: OglLinkType):
        """
        Updating type of link.

        @param  theType : Type of the link
        """
        # Python 3 update
        # if type(theType) == StringType or type(theType) == UnicodeType:
        if type(theType) is int:
            try:
                theType: OglLinkType = OglLinkType(theType)
            except (ValueError, Exception) as e:
                self.logger.error(f'setType: {e}')
                theType = OglLinkType.OGL_INHERITANCE
        self._type = theType

    def getType(self) -> OglLinkType:
        """
        To get the link type.

        @return  : The type of the link
        """
        return self._type

    def __str__(self):
        """
        String representation.

        @return : string representing link
        """
        return _(f'("{self.getName()}") links from {self._src} to {self._dest}')
