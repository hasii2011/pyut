
from logging import Logger
from logging import getLogger

from pyut.ui.eventengine.IEventEngine import IEventEngine
from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class UmlUseCaseDiagramsFrame(UmlDiagramsFrame):
    """
    This is a marker class to prevent use case symbols from appearing on
    non use case diagrams

    """

    UMLUseCaseFrameNextId: int = 0x00FFF   # UML Class Diagrams Frame ID

    def __init__(self, parent, eventEngine: IEventEngine):

        self.localLogger: Logger = getLogger(__name__)
        super().__init__(parent, eventEngine=eventEngine)

        self._frameId: int = UmlUseCaseDiagramsFrame.UMLUseCaseFrameNextId

    def __repr__(self) -> str:

        debugId: str = f'0x{self._frameId:06X}'
        return f'UmlUseCaseDiagramsFrame:[{debugId=}]'
