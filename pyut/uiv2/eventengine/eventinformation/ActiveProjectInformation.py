
from typing import cast

from dataclasses import dataclass

from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from pyut.uiv2.IPyutProject import IPyutProject


@dataclass
class ActiveProjectInformation:
    """
    Typical use is by the dialogs that edit UML objects
    """
    pyutProject: IPyutProject     = cast(IPyutProject, None)
    umlFrame:    UmlDiagramsFrame = cast(UmlDiagramsFrame, None)
