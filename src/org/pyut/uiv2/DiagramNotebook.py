
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from copy import copy

from wx import CLIP_CHILDREN
from wx import ICON_ERROR
from wx import ID_ANY
from wx import NO_IMAGE
from wx import OK

from wx import MessageDialog
from wx import Notebook
from wx import Window

from miniogl.Diagram import Diagram

from ogl.OglActor import OglActor
from ogl.OglClass import OglClass
from ogl.OglNote import OglNote
from ogl.OglUseCase import OglUseCase
from ogl.OglObject import OglObject

from pyutmodel.PyutActor import PyutActor
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutObject import PyutObject
from pyutmodel.PyutUseCase import PyutUseCase

from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from org.pyut.ui.umlframes.UmlFrame import UmlObjects

from org.pyut.uiv2.eventengine.Events import EVENT_COPY_SHAPES
from org.pyut.uiv2.eventengine.Events import EVENT_PASTE_SHAPES
from org.pyut.uiv2.eventengine.Events import EVENT_SELECT_ALL_SHAPES

from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.Events import CopyShapesEvent
from org.pyut.uiv2.eventengine.Events import PasteShapesEvent
from org.pyut.uiv2.eventengine.Events import SelectAllShapesEvent

from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine

PyutObjects = NewType('PyutObjects', List[PyutObject])


class DiagramNotebook(Notebook):

    def __init__(self, parentWindow: Window, eventEngine: IEventEngine):

        super().__init__(parentWindow, ID_ANY, style=CLIP_CHILDREN)

        self._eventEngine: IEventEngine = eventEngine
        self.logger:       Logger       = getLogger(__name__)

        self._clipboard: PyutObjects = PyutObjects([])            # will be re-created at every copy and cut

        self._eventEngine.registerListener(pyEventBinder=EVENT_SELECT_ALL_SHAPES, callback=self._onSelectAllShapes)
        self._eventEngine.registerListener(pyEventBinder=EVENT_COPY_SHAPES,       callback=self._onCopy)
        self._eventEngine.registerListener(pyEventBinder=EVENT_PASTE_SHAPES,      callback=self._onPaste)

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
            self._clipboard = PyutObjects([])
            # put a copy of the PyutObjects in the clipboard
            for umlObject in selectedUmlObjects:
                if isinstance(umlObject, OglClass):
                    umlObjectCopy = copy(umlObject.pyutObject)
                    umlObjectCopy.setLinks([])              # we don't want to copy the links
                    self._clipboard.append(umlObjectCopy)

            self._updateApplicationStatus(f'Copied {len(self._clipboard)} objects')

    # noinspection PyUnusedLocal
    def _onPaste(self, event: PasteShapesEvent):

        if len(self._clipboard) == 0:
            return

        self.logger.info(f'Pasting {len(self._clipboard)} objects')
        if self.currentNotebookFrame is None:
            self._displayError("No frame to paste into")
            return

        # put the objects in the clipboard and remove them from the diagram
        x: int = 100
        y: int = 100
        numbObjectsPasted: int = 0
        for clipboardObject in self._clipboard:
            pyutObject: PyutObject = copy(clipboardObject)
            oglObject:  OglObject  = cast(OglObject, None)
            match pyutObject:
                case PyutClass() as pyutObject:
                    oglObject = OglClass(cast(PyutClass, pyutObject))
                case PyutNote() as pyutObject:
                    oglObject = OglNote(pyutObject)
                case PyutActor() as pyutObject:
                    oglObject = OglActor(pyutObject)
                case PyutUseCase() as pyutObject:
                    oglObject = OglUseCase(pyutObject)
                case _:
                    self.logger.warning(f'Pasting object: {pyutObject} not supported')

            if oglObject is not None:
                self.logger.info(f'Pasting: {oglObject=}')
                self.currentNotebookFrame.addShape(oglObject, x, y)
                numbObjectsPasted += 1
                x += 20
                y += 20

        self.currentNotebookFrame.Refresh()

        self._eventEngine.sendEvent(EventType.UMLDiagramModified)   # will also cause title to be updated
        self._updateApplicationStatus(f'Pasted {numbObjectsPasted} objects')

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
