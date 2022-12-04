
from typing import List
from typing import NewType
from typing import Tuple
from typing import Union

from wx import Notebook
from wx import CommandProcessor

from pyut.PyutConstants import DiagramsLabels

from pyut.enums.DiagramType import DiagramType

from pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from pyut.ui.umlframes.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

UmlFrameType = Union[UmlClassDiagramsFrame, UmlSequenceDiagramsFrame]
Frames = NewType('Frames', List[UmlFrameType])


def createDiagramFrame(parentFrame: Notebook, diagramType: DiagramType,
                       eventEngine: IEventEngine, commandProcessor: CommandProcessor) -> Tuple[UmlFrameType, str]:
    """

    Args:
        parentFrame:
        diagramType:
        eventEngine:
        commandProcessor:

    Returns:  The tuple of the new diagram frame and the default diagram name
    """

    match diagramType:
        case DiagramType.CLASS_DIAGRAM:
            defaultDiagramName: str          = DiagramsLabels[diagramType]
            diagramFrame:       UmlFrameType = UmlClassDiagramsFrame(parentFrame, eventEngine=eventEngine, commandProcessor=commandProcessor)
        case DiagramType.SEQUENCE_DIAGRAM:
            defaultDiagramName = DiagramsLabels[diagramType]
            diagramFrame       = UmlSequenceDiagramsFrame(parentFrame, eventEngine=eventEngine, commandProcessor=commandProcessor)
        case DiagramType.USECASE_DIAGRAM:
            defaultDiagramName = DiagramsLabels[diagramType]
            diagramFrame       = UmlClassDiagramsFrame(parentFrame, eventEngine=eventEngine, commandProcessor=commandProcessor)
        case _:
            print(f'Unsupported diagram type; replacing with class diagram: {diagramType}')
            defaultDiagramName = DiagramsLabels[DiagramType.CLASS_DIAGRAM]
            diagramFrame = UmlClassDiagramsFrame(parentFrame, eventEngine=eventEngine)

    return diagramFrame, defaultDiagramName
