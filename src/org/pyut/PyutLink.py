
from logging import Logger
from logging import getLogger

from org.pyut.PyutObject import PyutObject

from Globals import _


class PyutLink(PyutObject):
    """
    A standard link between Class or Note.

    A PyutLink represents a UML link between Class in Pyut.

    Example::
        myLink  = PyutLink("linkName", 0, "0", "*")

    :version: $Revision: 1.5 $
    :author: Deve Roux
    :contact: droux@eivd.ch
    """

    def __init__(self, name="", linkType=0, cardSrc="", cardDest="", bidir=0, source=None, destination=None):
        """
        Constructor.

        @param string name     : for the link name
        @param int    linkType     : type of link
        @param string  cardSrc : cardinality of source of link
        @param string  cardDest: cardinality of destination of link
        @param boolean bidir   : design if link is bidirational or not
        @param obj source      : source of the link
        @param obj destination : where goes the link
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        @modified Laurent Burgbacher <lb@alawa.ch>
            added source field
        """
        # PyutObject.__init__(self, name)
        super().__init__(name)
        self.logger: Logger = getLogger(__name__)

        self._type    = linkType
        self._cardSrc = cardSrc
        self._cardDes = cardDest
        self._bidir   = bidir
        self._src     = source
        self._dest    = destination

    def getSrcCard(self) -> str:
        """
        Return a string representing cardinality source.

        @return string source cardinality
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._cardSrc

    def setSrcCard(self, cardSrc: str):
        """
        Updating source cardinality.

        @param  cardSrc
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._cardSrc = cardSrc

    def getDestCard(self):
        """
        Return a string representing cardinality destination.

        @return string destination cardinality
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._cardDes

    def setDestCard(self, cardDest: str):
        """
        Updating destination cardinality.

        @param cardDest
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._cardDes = cardDest

    def getSource(self):
        """
        Return the source object of the link

        @return object Class or Note
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._src

    def setSource(self, source):
        """
        Set the source object of this link.

        @param  source  PyutClass or PyutNote
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._src = source

    def getDestination(self):
        """
        Return an object destination who is linked to this link.

        @return object Class or Note
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._dest

    def setDestination(self, destination):
        """
        Updating destination.

        @param destination -- PyutClass or PyutNote
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._dest = destination

    def getBidir(self) -> bool:
        """
        To know if the link is bidirectional.

        @return boolean
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return self._bidir

    def setBidir(self, bidirectional: bool):
        """
        Updating bidirectional.

        @param bidirectional
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        self._bidir = bidirectional

    def setType(self, theType):
        """
        Updating type of link.

        @param int theType : Type of the link
        @since 1.2
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # Python 3 update
        # if type(theType) == StringType or type(theType) == UnicodeType:
        if type(theType) is str:
            try:
                theType = int(theType)
            except (ValueError, Exception) as e:
                self.logger.error(f'setType: {e}')
                theType = 0
        self._type = theType

    def getType(self):
        """
        To get the link type.

        @return int : The type of the link
        @since 1.2
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._type

    def __str__(self):
        """
        String representation.

        @return : string representing link
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        return _(f'("{self.getName()}") links from {self._src} to {self._dest}')
