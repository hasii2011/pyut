
from typing import cast

from logging import Logger
from logging import getLogger

from collections import namedtuple

from wx import MouseEvent

from pyutmodelv2.PyutModelTypes import ClassName
from pyutmodelv2.PyutModelTypes import Implementors

from pyutmodelv2.PyutInterface import PyutInterface

from miniogl.Shape import Shape

from ogl.OglInterface2 import OglInterface2
from wx import PaintEvent

from pyut.ui.umlframes.OrthogonalRoutingDiagnosticMixin import OrthogonalRoutingDiagnosticMixin
from pyut.ui.umlframes.UmlClassDiagramFrameMenuHandler import UmlClassDiagramFrameMenuHandler
from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from pyut.ui.umlframes.UmlFrame import UmlObjects

from pyut.ui.eventengine.Events import ClassNameChangedEvent
from pyut.ui.eventengine.Events import EVENT_CLASS_NAME_CHANGED
from pyut.ui.eventengine.IEventEngine import IEventEngine

CreatedClassesType = namedtuple('CreatedClassesType', 'pyutClass, oglClass')


class UmlClassDiagramsFrame(UmlDiagramsFrame, OrthogonalRoutingDiagnosticMixin):

    UMLFrameNextId: int = 0x000FF   # UML Class Diagrams Frame ID

    """
    UmlClassDiagramsFrame : A UML class diagram frame.

    This class is the instance of one UML class diagram structure.
    It derives its functionality from UmlDiagramsFrame.
    """
    def __init__(self, parent, eventEngine: IEventEngine | None = None):
        """

        Args:
            parent:
            eventEngine: Pyut event engine
        """
        super().__init__(parent, eventEngine=eventEngine)   # type: ignore
        OrthogonalRoutingDiagnosticMixin.__init__(self)

        self.localLogger: Logger = getLogger(__name__)

        self._menuHandler:  UmlClassDiagramFrameMenuHandler = cast(UmlClassDiagramFrameMenuHandler, None)

        UmlClassDiagramsFrame.UMLFrameNextId += 1

        self._frameId: int = UmlClassDiagramsFrame.UMLFrameNextId

        self._eventEngine.registerListener(pyEventBinder=EVENT_CLASS_NAME_CHANGED, callback=self._onClassNameChanged)

    @property
    def frameId(self) -> int:
        return self._frameId

    def OnRightDown(self, event: MouseEvent):

        super().OnRightDown(event=event)

        self.localLogger.debug(f'UmlClassDiagrams.OnRightDown')
        if self._areWeOverAShape(event=event) is False:
            if self._menuHandler is None:
                self._menuHandler = UmlClassDiagramFrameMenuHandler(self)

            self._menuHandler.popupMenu(event=event)

    def OnPaint(self, event: PaintEvent):
        super().OnPaint(event=event)

        OrthogonalRoutingDiagnosticMixin.drawDiagnostics(self, umlFrame=self)

    def _onClassNameChanged(self, event: ClassNameChangedEvent):

        oldClassName: ClassName = ClassName(event.oldClassName)
        newClassName: ClassName = ClassName(event.newClassName)
        self.localLogger.info(f'{oldClassName=} {newClassName=}')

        umlObjects: UmlObjects = self.umlObjects

        for umlObject in umlObjects:
            if isinstance(umlObject, OglInterface2):
                oglInterface:  OglInterface2 = cast(OglInterface2, umlObject)
                pyutInterface: PyutInterface = oglInterface.pyutInterface

                implementors: Implementors = pyutInterface.implementors

                for idx, implementor in enumerate(implementors):
                    self.logger.warning(f'{idx=} - {pyutInterface.name=} {implementor=}')
                    if implementor == oldClassName:
                        pyutInterface.implementors[idx] = newClassName

        event.Skip(True)   # For testability; In reality we are the only handler

    def _areWeOverAShape(self, event: MouseEvent) -> bool:
        answer:         bool  = True
        potentialShape: Shape = self.FindShape(x=event.GetX(), y=event.GetY())
        # Don't popup over a shape
        if potentialShape is None:
            answer = False

        return answer

    def __repr__(self) -> str:

        debugId: str = f'0x{self._frameId:06X}'
        return f'UmlClassDiagramsFrame:[{debugId=}]'
