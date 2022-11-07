
from typing import Callable
from typing import cast

from dataclasses import dataclass

from pyut.enums.DiagramType import DiagramType
from org.pyut.uiv2.IPyutDocument import IPyutDocument
from org.pyut.uiv2.IPyutProject import IPyutProject

NewProjectDiagramCallback = Callable[[IPyutDocument], None]


@dataclass
class NewProjectDiagramInformation:
    pyutProject:    IPyutProject    = cast(IPyutProject, None)
    diagramType:    DiagramType     = DiagramType.UNKNOWN_DIAGRAM
    diagramName:    str             = ''
    callback:       NewProjectDiagramCallback = cast(NewProjectDiagramCallback, None)

