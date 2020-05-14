
from logging import Logger
from logging import getLogger

from org.pyut.MiniOgl.AnchorPoint import AnchorPoint
from org.pyut.MiniOgl.LollipopLine import LollipopLine

from org.pyut.MiniOgl.ShapeEventHandler import ShapeEventHandler
from org.pyut.model.PyutInterface import PyutInterface


class OglInterface2(LollipopLine, ShapeEventHandler):

    def __init__(self, pyutInterface: PyutInterface,  destinationAnchor: AnchorPoint):

        LollipopLine.__init__(self, destinationAnchor=destinationAnchor)

        self.logger: Logger = getLogger(__name__)

        self._pyutInterface: PyutInterface = pyutInterface
