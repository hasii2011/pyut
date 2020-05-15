
from typing import Tuple

from logging import Logger
from logging import getLogger

from wx import Yield as wxYield

from org.pyut.MiniOgl.SelectAnchorPoint import SelectAnchorPoint
from org.pyut.enums.PyutAttachmentPoint import PyutAttachmentPoint

from org.pyut.ogl.OglClass import OglClass

from org.pyut.commands.Command import Command
from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame


class CreateOglInterfaceCommand(Command):

    def __init__(self,  destinationClass: OglClass):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

        # self._createInterfaceLollipop(destinationClass)

    def execute(self):
        self.redo()

    # def _createInterfaceLollipop(self, destinationClass: OglClass):
    #
    #     from org.pyut.general.Mediator import getMediator
    #     from org.pyut.general.Mediator import Mediator
    #
    #     from org.pyut.ogl.OglInterface2 import OglInterface2
    #     from org.pyut.model.PyutInterface import PyutInterface
    #
    #     destinationPosition: Tuple[float, float] = destinationClass.GetPosition()
    #     anchors = destinationClass.GetAnchors()
    #     self.logger.info(f'implementor: {destinationClass} at {destinationPosition}')
    #
    #     med: Mediator = getMediator()
    #
    #     pyutInterface: PyutInterface = PyutInterface(name='Sin Nombre')
    #     oglInterface:  OglInterface2 = OglInterface2(pyutInterface, anchors[0])
    #
    #     umlFrame: UmlClassDiagramsFrame = med.getFileHandling().getCurrentFrame()
    #
    #     self.__createPotentialAttachmentPoints(destinationClass=destinationClass, umlFrame=umlFrame)
    #     med.setStatusText(f'Select attachment point')
    #     wxYield()
    #
    #     x = destinationPosition[0]
    #     y = destinationPosition[1]
    #
    #     umlFrame.addShape(oglInterface, x, y, withModelUpdate=True)
    #     umlFrame.Refresh()
    #
    # def __createPotentialAttachmentPoints(self, destinationClass: OglClass, umlFrame):
    #
    #     dw, dh     = destinationClass.GetSize()
    #
    #     southX, southY = dw / 2, dh
    #     northX, northY = dw / 2, 0
    #     westX, westY   = 0.0, dh / 2
    #     eastX, eastY   = dw, dh / 2
    #
    #     self.__createAnchorHints(destinationClass, southX, southY, PyutAttachmentPoint.SOUTH, umlFrame)
    #     self.__createAnchorHints(destinationClass, northX, northY, PyutAttachmentPoint.NORTH, umlFrame)
    #     self.__createAnchorHints(destinationClass, westX,  westY,  PyutAttachmentPoint.WEST,  umlFrame)
    #     self.__createAnchorHints(destinationClass, eastX,  eastY,  PyutAttachmentPoint.EAST, umlFrame)
    #
    # def __createAnchorHints(self, destinationClass: OglClass, anchorX: float, anchorY: float, attachmentPoint: PyutAttachmentPoint, umlFrame):
    #
    #     anchorHint: SelectAnchorPoint = SelectAnchorPoint(x=anchorX, y=anchorY, attachmentPoint=attachmentPoint, parent=destinationClass)
    #     anchorHint.SetProtected(True)
    #
    #     destinationClass.AddAnchorPoint(anchorHint)
    #     umlFrame.getDiagram().AddShape(anchorHint)
