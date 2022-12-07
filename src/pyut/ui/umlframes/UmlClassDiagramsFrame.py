
from typing import cast

from collections import namedtuple

from pyutmodel.ModelTypes import ClassName
from pyutmodel.ModelTypes import Implementors
from pyutmodel.PyutInterface import PyutInterface

from ogl.OglInterface2 import OglInterface2

from wx import CommandProcessor

from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from pyut.ui.umlframes.UmlFrame import UmlObjects

from pyut.general.CustomEvents import ClassNameChangedEvent
from pyut.general.CustomEvents import EVT_CLASS_NAME_CHANGED
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

CreatedClassesType = namedtuple('CreatedClassesType', 'pyutClass, oglClass')


class UmlClassDiagramsFrame(UmlDiagramsFrame):

    cdfDebugId: int = 0x000FF   # UML Class Diagrams Frame Debug ID

    """
    UmlClassDiagramsFrame : a UML class diagram frame.

    This class is the instance of one UML class diagram structure.
    It derives its functionality from UmlDiagramsFrame, but
    it knows the structure of a class diagram and it can load class diagram data.
    """
    def __init__(self, parent, eventEngine: IEventEngine | None = None, commandProcessor: CommandProcessor | None = None):
        """

        Args:
            parent:
            eventEngine: Pyut event engine
        """
        self._cdfDebugId: int = UmlClassDiagramsFrame.cdfDebugId

        UmlClassDiagramsFrame.cdfDebugId += 1

        super().__init__(parent, eventEngine=eventEngine, commandProcessor=commandProcessor)   # type: ignore
        self.newDiagram()

        self.Bind(EVT_CLASS_NAME_CHANGED, self._onClassNameChanged)

    def _onClassNameChanged(self, event: ClassNameChangedEvent):

        oldClassName: ClassName = ClassName(event.oldClassName)
        newClassName: ClassName = ClassName(event.newClassName)
        self.logger.warning(f'{oldClassName=} {newClassName=}')

        umlObjects: UmlObjects = self.getUmlObjects()

        for umlObject in umlObjects:
            if isinstance(umlObject, OglInterface2):
                oglInterface:  OglInterface2 = cast(OglInterface2, umlObject)
                pyutInterface: PyutInterface = oglInterface.pyutInterface

                implementors: Implementors = pyutInterface.implementors

                for idx, implementor in enumerate(implementors):
                    self.logger.warning(f'{idx=} - {pyutInterface.name=} {implementor=}')
                    if implementor == oldClassName:
                        pyutInterface.implementors[idx] = newClassName

    def __repr__(self) -> str:

        debugId: str = f'0x{self._cdfDebugId:06X}'
        return f'UmlClassDiagramsFrame:[{debugId=}]'
