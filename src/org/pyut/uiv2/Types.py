
from typing import List
from typing import NewType
from typing import Union

from org.pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.umlframes.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame

UmlFrameType = Union[UmlClassDiagramsFrame, UmlSequenceDiagramsFrame]

Frames = NewType('Frames', List[UmlFrameType])
