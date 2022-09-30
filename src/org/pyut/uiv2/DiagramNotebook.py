
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from copy import copy

from ogl.OglClass import OglClass
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
from org.pyut.ui.umlframes.UmlFrame import UmlObjects

from org.pyut.uiv2.eventengine.Events import EVENT_COPY_SHAPES
from org.pyut.uiv2.eventengine.Events import EVENT_SELECT_ALL_SHAPES
from org.pyut.uiv2.eventengine.Events import CopyShapesEvent
from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.Events import SelectAllShapesEvent

from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine


class DiagramNotebook(Notebook):

    def __init__(self, parentWindow: Window, eventEngine: IEventEngine):

        super().__init__(parentWindow, ID_ANY, style=CLIP_CHILDREN)

        self._eventEngine: IEventEngine = eventEngine
        self.logger:       Logger       = getLogger(__name__)

        self._clipboard: UmlObjects = UmlObjects([])            # will be re-created at every copy and cut

        self._eventEngine.registerListener(pyEventBinder=EVENT_SELECT_ALL_SHAPES, callback=self._onSelectAllShapes)
        self._eventEngine.registerListener(pyEventBinder=EVENT_COPY_SHAPES,       callback=self._onCopy)

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

    # noinspection PyUnusedLocal
    def _onCopy(self, event: CopyShapesEvent):
        """
        Copy the selected UML Objects into an internal clipboard

        TODO : adapt for OglLinks

        Args:
            event:
        """
        selectedUmlObjects: UmlObjects = self._getSelectedUmlObjects()
        if len(selectedUmlObjects) > 0:
            self._clipboard = UmlObjects([])
            # put a copy of the PyutObjects in the clipboard
            for umlObject in selectedUmlObjects:
                if isinstance(umlObject, OglClass):
                    umlObjectCopy = copy(umlObject.pyutObject)
                    umlObjectCopy.setLinks([])              # we don't want to copy the links
                    self._clipboard.append(umlObjectCopy)

            self._updateApplicationStatus(f'Copied {len(self._clipboard)} objects')

    def _getSelectedUmlObjects(self) -> UmlObjects:
        """
        Return the list of selected OglObjects in the diagram.

        Returns:  May be empty
        """
        umlObjects:      UmlObjects = self.getUmlObjects()
        selectedObjects: UmlObjects = UmlObjects([])

        if umlObjects is not None:
            for umlObject in umlObjects:
                if umlObject.IsSelected():
                    selectedObjects.append(umlObject)

        return selectedObjects

    def getUmlObjects(self) -> UmlObjects:
        """
        May be empty

        Returns: Return the list of UmlObjects in the diagram.
        """
        umlFrame:   UmlDiagramsFrame = self.currentNotebookFrame
        umlObjects: UmlObjects       = UmlObjects([])
        if umlFrame is not None:
            umlObjects = umlFrame.getUmlObjects()

        return umlObjects

    def _displayError(self, message: str):

        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption='Error', style=OK | ICON_ERROR)
        booBoo.ShowModal()

    def _updateApplicationStatus(self, statusMessage: str):

        self._eventEngine.sendEvent(eventType=EventType.UpdateApplicationStatus, applicationStatusMsg=statusMessage)
