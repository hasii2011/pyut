
from logging import Logger
from logging import getLogger

from pyutmodel.PyutLink import PyutLink


class PyutSDMessage(PyutLink):
    """
    A message between two lifeline of two SDInstances.
    Note : Use getSrcY, getDstY

    """

    def __init__(self, message="", src=None, srcTime=0, dst=None, dstTime=0, oglObject=None):
        """
        TODO:  add timescale zoomer ?! and offset ?
        Args:
            message: for the message
            src:     source of the link
            srcTime: time on the source
            dst:     where the link goes
            dstTime: time on the destination
            oglObject: OGL parent object
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

        Args:
            dst:        destination object
            dstTime:    Time on the destination
        """
        if dst is not None:
            PyutLink.setDestination(self, dst)
        if dstTime != -1:
            self.logger.debug(f"Setting dstTime to {dstTime}")
            self.setDstTime(dstTime)

    def __str__(self):
        """

        Returns:    string representing this object
        """
        # return _("(%s) link to %s") % (self._src, self._dest)
        return f'{self._src} linked to {self._dest}'
