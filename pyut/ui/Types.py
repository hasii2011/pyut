
from typing import List
from typing import NewType
from typing import Tuple
from typing import Union

from wx import Notebook

from pyut.PyutConstants import DiagramsLabels

from pyut.enums.DiagramType import DiagramType

from pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from pyut.ui.umlframes.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame
from pyut.ui.eventengine.IEventEngine import IEventEngine
from pyut.ui.umlframes.UmlUseCaseDiagramsFrame import UmlUseCaseDiagramsFrame

UmlFrameType = Union[UmlClassDiagramsFrame, UmlSequenceDiagramsFrame, UmlUseCaseDiagramsFrame]
Frames = NewType('Frames', List[UmlFrameType])


def createDiagramFrame(parentFrame: Notebook, diagramType: DiagramType,
                       eventEngine: IEventEngine) -> Tuple[UmlFrameType, str]:
    """

    Args:
        parentFrame:
        diagramType:
        eventEngine:

    Returns:  The tuple of the new diagram frame and the default diagram name
    """

    match diagramType:
        case DiagramType.CLASS_DIAGRAM:
            defaultDiagramName: str          = DiagramsLabels[diagramType]
            diagramFrame:       UmlFrameType = UmlClassDiagramsFrame(parentFrame, eventEngine=eventEngine)
        case DiagramType.SEQUENCE_DIAGRAM:
            defaultDiagramName = DiagramsLabels[diagramType]
            diagramFrame       = UmlSequenceDiagramsFrame(parentFrame, eventEngine=eventEngine)
        case DiagramType.USECASE_DIAGRAM:
            defaultDiagramName = DiagramsLabels[diagramType]
            diagramFrame       = UmlUseCaseDiagramsFrame(parentFrame, eventEngine=eventEngine)
        case _:
            print(f'Unsupported diagram type; replacing with class diagram: {diagramType}')
            defaultDiagramName = DiagramsLabels[DiagramType.CLASS_DIAGRAM]
            diagramFrame = UmlClassDiagramsFrame(parentFrame, eventEngine=eventEngine)

    return diagramFrame, defaultDiagramName
