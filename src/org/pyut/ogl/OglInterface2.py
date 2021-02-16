
from logging import Logger
from logging import getLogger

from org.pyut.miniogl.Common import Common
from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint
from org.pyut.miniogl.LollipopLine import LollipopLine

from org.pyut.model.PyutInterface import PyutInterface
from org.pyut.model.PyutObject import PyutObject


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

    @property
    def pyutObject(self) -> PyutObject:
        """
        Synonym for reverse compatibility

        Returns:  The pyut interface
        """
        return self.pyutInterface

    @pyutObject.setter
    def pyutObject(self, newValue: PyutInterface):
        """
        Synonym for reverse compatibility

        Args:
            newValue: The new PyutInterface object
        """
        self._pyutInterface = newValue

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

    def __repr__(self):

        strMe: str = f'OglInterface2 - "{self._pyutInterface.getName()}"'
        return strMe

    def __eq__(self, other):

        if isinstance(other, OglInterface2):
            if self._isSameName(other) is True and self._isSameId(other) is True:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):
        return hash(self._pyutInterface.getName()) + hash(self.GetID())

    def _isSameName(self, other) -> bool:

        ans: bool = False
        if self.pyutInterface.getName() == other.pyutInterface.getName():
            ans = True
        return ans

    def _isSameId(self, other):

        ans: bool = False
        if self.GetID() == other.GetID():
            ans = True
        return ans
