
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from miniogl.Diagram import Diagram
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from oglio.Types import OglActors
from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglNotes
from oglio.Types import OglSDInstances
from oglio.Types import OglSDMessages
from oglio.Types import OglTexts
from oglio.Types import OglUseCases

from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class LayoutEngine:
    """
    A convenience class that knows how to take an OGLDocument
    and place the UML documents on a UML frame
    """
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def layout(self, umlFrame: UmlDiagramsFrame, oglDocument: OglDocument):
        """
        Don't care what type of diagram since those lists will be empty

        Args:
            umlFrame:       A uml diagram frame to populate
            oglDocument:    The OGL Document
        """
        self._layoutOglClasses(umlFrame=umlFrame, oglClasses=oglDocument.oglClasses)
        self._layoutOglLinks(umlFrame=umlFrame, oglLinks=oglDocument.oglLinks)
        self._layoutOglNotes(umlFrame=umlFrame, oglNotes=oglDocument.oglNotes)
        self._layoutOglTexts(umlFrame=umlFrame, oglTexts=oglDocument.oglTexts)

        self._layoutOglActors(umlFrame=umlFrame, oglActors=oglDocument.oglActors)
        self._layoutOglUseCases(umlFrame=umlFrame, oglUseCases=oglDocument.oglUseCases)

        self._layoutOglSDInstances(umlFrame=umlFrame, oglSDInstances=oglDocument.oglSDInstances)
        self._layoutOglSDMessages(umlFrame=umlFrame, oglSDMessages=oglDocument.oglSDMessages)

    def addShape(self, umlFrame: UmlDiagramsFrame, oglObject: OglObject):

        match oglObject:
            case OglLink() as oglObject:
                self._layoutOglLink(umlFrame=umlFrame, oglLink=cast(OglLink, oglObject))
            case OglSDInstance() as oglObject:
                self._layoutOglSDInstance(diagram=umlFrame.getDiagram(), oglSDInstance=cast(OglSDInstance, oglObject))
            case OglSDMessage() as oglObject:
                self._layoutOglSDMessage(diagram=umlFrame.getDiagram(), oglSDMessage=cast(OglSDMessage, oglObject))
            case _:
                self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglObject)

    def _layoutOglClasses(self, umlFrame: UmlDiagramsFrame, oglClasses: OglClasses):
        for oglClass in oglClasses:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglClass, )

    def _layoutOglLinks(self, umlFrame: UmlDiagramsFrame, oglLinks: OglLinks):

        for link in oglLinks:
            oglLink: OglLink = cast(OglLink, link)
            self._layoutOglLink(umlFrame=umlFrame, oglLink=oglLink)

    def _layoutOglNotes(self, umlFrame: UmlDiagramsFrame, oglNotes: OglNotes):
        for oglNote in oglNotes:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglNote)

    def _layoutOglTexts(self, umlFrame: UmlDiagramsFrame, oglTexts: OglTexts):
        for oglText in oglTexts:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglText)

    def _layoutOglActors(self, umlFrame: UmlDiagramsFrame, oglActors: OglActors):
        for oglActor in oglActors:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglActor)

    def _layoutOglUseCases(self, umlFrame: UmlDiagramsFrame, oglUseCases: OglUseCases):
        for oglUseCase in oglUseCases:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglUseCase)

    def _layoutOglSDInstances(self, umlFrame: UmlDiagramsFrame, oglSDInstances: OglSDInstances):
        diagram: Diagram = umlFrame.getDiagram()
        for oglSDInstance in oglSDInstances.values():
            self._layoutOglSDInstance(diagram=diagram, oglSDInstance=oglSDInstance)
        umlFrame.Refresh()

    def _layoutOglSDMessages(self, umlFrame: UmlDiagramsFrame, oglSDMessages: OglSDMessages):
        diagram: Diagram = umlFrame.getDiagram()
        for oglSDMessage in oglSDMessages.values():
            self._layoutOglSDMessage(diagram=diagram, oglSDMessage=oglSDMessage)

    def _layoutOglLink(self, umlFrame: UmlDiagramsFrame, oglLink: OglLink):

        self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglLink)
        # TODO:
        # This is bad mooky here. The Ogl objects were created withing having a Diagram
        # The legacy code deserialized the object while adding them to a frame. This
        # new code deserializes w/o reference to a frame
        # If we don't this the AnchorPoints are not on the diagram and lines ends are not
        # movable.
        if isinstance(oglLink, OglInterface2) is False:
            umlDiagram = umlFrame.diagram

            umlDiagram.AddShape(oglLink.sourceAnchor)
            umlDiagram.AddShape(oglLink.destinationAnchor)
            controlPoints = oglLink.GetControlPoints()
            for controlPoint in controlPoints:
                umlDiagram.AddShape(controlPoint)

    def _layoutOglSDInstance(self, diagram: Diagram, oglSDInstance: OglSDInstance):
        diagram.AddShape(oglSDInstance)

    def _layoutOglSDMessage(self, diagram: Diagram, oglSDMessage: OglSDMessage):
        diagram.AddShape(oglSDMessage)

    def _layoutAnOglObject(self, umlFrame: UmlDiagramsFrame, oglObject: Union[OglObject, OglInterface2, SelectAnchorPoint, OglLink]):
        x, y = oglObject.GetPosition()
        umlFrame.addShape(oglObject, x, y)
