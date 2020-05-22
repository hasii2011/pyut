
from logging import Logger
from logging import getLogger

from org.pyut.MiniOgl.Common import Common
from org.pyut.MiniOgl.SelectAnchorPoint import SelectAnchorPoint
from org.pyut.MiniOgl.LollipopLine import LollipopLine

from org.pyut.model.PyutInterface import PyutInterface


class OglInterface2(LollipopLine, Common):

    def __init__(self, pyutInterface: PyutInterface,  destinationAnchor: SelectAnchorPoint):

        LollipopLine.__init__(self, destinationAnchor=destinationAnchor)

        self.logger: Logger = getLogger(__name__)

        self._pyutInterface: PyutInterface = pyutInterface

    @property
    def pyutInterface(self) -> PyutInterface:
        return self._pyutInterface

    @pyutInterface.setter
    def pyutInterface(self, theNewValue: PyutInterface):
        self._pyutInterface = theNewValue

    def Inside(self, clickPointX, clickPointY) -> bool:
        """
        Override Shape.Inside

        Args:
            clickPointX: x click coordinate
            clickPointY: y click coordinate

        Returns:  `True` if (x, y) is inside the shape.
        """
        clickDiffStartX, clickDiffStartY, diffX, diffY = self.setupInsideCheck(clickPointX=clickPointX, clickPointY=clickPointY, line=self.lineCoordinates())

        if self.insideBoundingBox(clickDiffStartX, clickDiffStartY, diffX, diffY) and self.insideSegment(clickDiffStartX, clickDiffStartY, diffX, diffY):
            return True

        return False
