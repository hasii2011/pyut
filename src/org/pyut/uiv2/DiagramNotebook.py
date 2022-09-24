from logging import Logger

from logging import getLogger

from wx import CLIP_CHILDREN
from wx import ID_ANY
from wx import NO_IMAGE
from wx import Notebook
from wx import Window

from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class DiagramNotebook(Notebook):

    def __init__(self, parentWindow: Window):

        super().__init__(parentWindow, ID_ANY, style=CLIP_CHILDREN)

        self.logger: Logger = getLogger(__name__)

    @property
    def currentNotebookFrame(self) -> UmlDiagramsFrame:
        """
        Get the current frame in the notebook;  May

        Returns:  A UML Diagrams Frame or None
        """
        frame = self.GetCurrentPage()
        return frame

    def AddPage(self, page, text, select=False, imageId=NO_IMAGE):
        """
        Override so we can catch double add;  Originally for debugging

        Args:
            page:
            text:
            select:
            imageId:
        """
        super().AddPage(page, text, select, imageId)
