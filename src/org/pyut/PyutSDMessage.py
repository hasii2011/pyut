
from logging import Logger
from logging import getLogger

from org.pyut.PyutLink import PyutLink

from Globals import _


class PyutSDMessage(PyutLink):
    """
    A message between two lifeline of two CDInstances.
    Note : don't use getxxxTime, but getSrcY, getDstY

    :version: $Revision: 1.11 $
    :author: C.Dutoit
    """

    def __init__(self, message="", src=None, srcTime=0, dst=None, dstTime=0, oglObject=None):
        """
        Constructor.

        @param string message  : for the message
        @param PyutCDInstance src : source of the link
        @param int srcTime : time on the source
        @param PyutCDInstance dst : where goes the link
        @param int dstTime : time on the destination
        @param oglObject : my OGL parent object
        @author C.Dutoit
        @tips : add time scale zoomer ?! and ofset..ter ?
        """
        self.logger: Logger = getLogger(__name__)

        self.logger.debug(f"PyutSDMessage.__init__ {srcTime}, {dstTime}")
        super().__init__(source=src, destination=dst)
        self._message = message
        self._srcTime = srcTime
        self._dstTime = dstTime
        self._oglObject = oglObject

    def setOglObject(self, obj):
        """
        Define the ogl object
        @author C.Dutoit
        """
        self._oglObject = obj

    def getSrcY(self):
        """
        Return Y position on source
        @author C.Dutoit
        """
        return self._srcTime

    def getDstY(self):
        """
        Return Y position on destination
        @author C.Dutoit
        """
        return self._dstTime

    def setSrcY(self):
        """
        Return Y position on source
        @author C.Dutoit
        """
        return self._srcTime

    def setDstY(self):
        """
        Return Y position on destination
        @author C.Dutoit
        """
        return self._dstTime

    def getSrcTime(self):
        """
        Return time on source
        DON'T use it, or only for saving purpose
        @author C.Dutoit
        """
        return self._srcTime

    def getDstTime(self):
        """
        Return time on destination
        DON'T use it, or only for saving purpose
        @author C.Dutoit
        """
        return self._dstTime

    def setSrcTime(self, value, updateOGLObject=True):
        """
        Define time on source
        DON'T use it, or only for saving purpose
        @author C.Dutoit
        """
        self._srcTime = int(value)
        if updateOGLObject and self._oglObject is not None:
            self._oglObject.updatePositions()

    def setDstTime(self, value, updateOGLObject=True):
        """
        Define time on destination
        DON'T use it, or only for saving purpose
        @author C.Dutoit
        """
        self._dstTime = int(value)
        if updateOGLObject and self._oglObject is not None:
            self._oglObject.updatePositions()

    def getSrcID(self):
        """
        Return Y position on source
        @author C.Dutoit
        """
        return self._src.getId()

    def getDstID(self):
        """
        Return Y position on source
        @author C.Dutoit
        """
        return self._dest.getId()

    def getSource(self):
        """
        Return Y position on source
        @author C.Dutoit
        """
        return self._src

    def getDest(self):
        """
        Return Y position on source
        @author C.Dutoit
        """
        return self._dest

    def getMessage(self):
        """
        Return the message as a string
        @return String : message
        @author C.Dutoit
        """
        return self._message

    def setMessage(self, value):
        """
        Define the message
        @param String value : value of the message
        @author C.Dutoit
        """
        self._message = value

    def setSource(self, src=None, srcTime=-1):
        """
        Define the source
        @param src : Source object
        @param srcTime : Time on the source
        @author C.Dutoit
        """
        if src is not None:
            # self._src = src
            PyutLink.setSource(self, src)
        if srcTime != -1:
            self.logger.debug(f"PyutSDMessage - Setting srcTime to: {srcTime}")
            self.setSrcTime(srcTime)

    def setDestination(self, dst=None, dstTime=-1):
        """
        Define the destination
        @param dst : destination object
        @param dstTime : Time on the destination
        @author C.Dutoit
        """
        if dst is not None:
            PyutLink.setDestination(self, dst)
            # self._dest = dst
        if dstTime != -1:
            print("PyutSDMessage - Setting dstTime to ", dstTime)
            self.setDstTime(dstTime)

    def __str__(self):
        """
        String representation.

        @return : string representing this object
        @author C.Dutoit
        """
        return _("(%s) link to %s") % (self._src, self._dest)
