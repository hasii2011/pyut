
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import CLIP_CHILDREN
from wx import ICON_ERROR
from wx import ID_ANY
from wx import NO_IMAGE
from wx import OK

from wx import MessageDialog
from wx import Notebook
from wx import Window

from miniogl.Diagram import Diagram

from ogl.OglObject import OglObject

from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from org.pyut.uiv2.eventengine.Events import EVENT_SELECT_ALL_SHAPES
from org.pyut.uiv2.eventengine.Events import SelectAllShapesEvent
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine


class DiagramNotebook(Notebook):

    def __init__(self, parentWindow: Window, eventEngine: IEventEngine):

        super().__init__(parentWindow, ID_ANY, style=CLIP_CHILDREN)

        self._eventEngine: IEventEngine = eventEngine
        self.logger:       Logger       = getLogger(__name__)

        self._eventEngine.registerListener(pyEventBinder=EVENT_SELECT_ALL_SHAPES, callback=self._onSelectAllShapes)

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

    # noinspection PyUnusedLocal
    def _onSelectAllShapes(self, event: SelectAllShapesEvent):
        """
        Select all Ogl shapes on the current frame
        """
        frame: UmlDiagramsFrame = self.GetCurrentPage()

        if frame is None:
            self._displayError("No frame found !")
            return
        diagram: Diagram         = frame.GetDiagram()
        shapes:  List[OglObject] = diagram.GetShapes()
        for oglShape in shapes:
            shape: OglObject = cast(OglObject, oglShape)
            shape.SetSelected(True)

        frame.Refresh()

    def _displayError(self, message: str):

        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption='Error', style=OK | ICON_ERROR)
        booBoo.ShowModal()
