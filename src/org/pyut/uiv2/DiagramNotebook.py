
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from copy import copy

from ogl.OglLink import OglLink
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
from ogl.OglUseCase import OglUseCase
from ogl.OglNote import OglNote
from ogl.OglObject import OglObject


from pyutmodel.PyutActor import PyutActor
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutObject import PyutObject
from pyutmodel.PyutUseCase import PyutUseCase

from org.pyut.history.HistoryManager import HistoryManager
from org.pyut.history.commands.CommandGroup import CommandGroup
from org.pyut.history.commands.DeleteOglClassCommand import DeleteOglClassCommand
from org.pyut.history.commands.DeleteOglNoteCommand import DeleteOglNoteCommand
from org.pyut.history.commands.DeleteOglObjectCommand import DeleteOglObjectCommand
from org.pyut.history.commands.DelOglLinkCommand import DelOglLinkCommand

from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from org.pyut.ui.umlframes.UmlFrame import UmlObject
from org.pyut.ui.umlframes.UmlFrame import UmlObjects

from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine
from org.pyut.uiv2.eventengine.Events import CutShapesEvent

from org.pyut.uiv2.eventengine.Events import EVENT_COPY_SHAPES
from org.pyut.uiv2.eventengine.Events import EVENT_CUT_SHAPES
from org.pyut.uiv2.eventengine.Events import EVENT_PASTE_SHAPES
from org.pyut.uiv2.eventengine.Events import EVENT_SELECT_ALL_SHAPES

from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.Events import CopyShapesEvent
from org.pyut.uiv2.eventengine.Events import PasteShapesEvent
from org.pyut.uiv2.eventengine.Events import SelectAllShapesEvent


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
        self._eventEngine.registerListener(pyEventBinder=EVENT_CUT_SHAPES,        callback=self._onCut)

    @property
    def currentNotebookFrame(self) -> UmlDiagramsFrame:
        """
        Get the current frame in the notebook;  May

        Returns:  A UML Diagrams Frame or None
        """
        frame = self.GetCurrentPage()
        return frame

    @property
    def umlObjects(self) -> UmlObjects:
        """
        May be empty

        Returns: Return the list of UmlObjects in the diagram.
        """
        umlFrame:   UmlDiagramsFrame = self.currentNotebookFrame
        umlObjects: UmlObjects       = UmlObjects([])
        if umlFrame is not None:
            umlObjects = umlFrame.getUmlObjects()

        return umlObjects

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

    # noinspection PyUnusedLocal
    def _onCut(self, event: CutShapesEvent):

        selectedUmlObjects: UmlObjects       = self._getSelectedUmlObjects()
        umlFrame:           UmlDiagramsFrame = self.currentNotebookFrame
        historyManager:     HistoryManager   = umlFrame.historyManager
        cmdGroup:           CommandGroup     = CommandGroup("Delete UML object(s)")

        if len(selectedUmlObjects) > 0:
            self._clipboard = PyutObjects([])
            # put the PyutObjects in the clipboard and remove their graphical representation from the diagram
            for umlObject in selectedUmlObjects:

                self._clipboard.append(umlObject.pyutObject)
                cmdGroup = self._deleteShapeFromFrame(oglObjectToDelete=umlObject, cmdGroup=cmdGroup)

            historyManager.addCommandGroup(cmdGroup)
            historyManager.execute()

            self.logger.info(f'Cut {len(self._clipboard)} objects')

            # self._treeNotebookHandler.setModified(True)
            # self._mediator.updateTitle()
            self._eventEngine.sendEvent(EventType.UMLDiagramModified)  # will also cause title to be updated

            umlFrame.Refresh()

    def _getSelectedUmlObjects(self) -> UmlObjects:
        """
        Return the list of selected OglObjects in the diagram.

        Returns:  May be empty
        """
        umlObjects:      UmlObjects = self.umlObjects
        selectedObjects: UmlObjects = UmlObjects([])

        if umlObjects is not None:
            for umlObject in umlObjects:
                if umlObject.IsSelected():
                    selectedObjects.append(umlObject)

        return selectedObjects

    def _displayError(self, message: str):

        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption='Error', style=OK | ICON_ERROR)
        booBoo.ShowModal()

    def _updateApplicationStatus(self, statusMessage: str):

        self._eventEngine.sendEvent(eventType=EventType.UpdateApplicationStatus, applicationStatusMsg=statusMessage)

    def _deleteShapeFromFrame(self, oglObjectToDelete: UmlObject, cmdGroup: CommandGroup) -> CommandGroup:
        """
        This is the common method to delete a shape from a UML frame. In addition, this method
        adds the appropriate history commands in order to support undo

        Args:
            oglObjectToDelete:  The Ogl object to remove from the frame
            cmdGroup:   The command group to update with an appropriate delete command

        Returns:    The updated command group
        """
        if isinstance(oglObjectToDelete, OglClass):

            oglClass: OglClass = cast(OglClass, oglObjectToDelete)
            cmd: DeleteOglClassCommand = DeleteOglClassCommand(oglClass)
            cmdGroup.addCommand(cmd)
            links = oglClass.links
            for link in links:
                cmdGroup = self._addADeleteLinkCommand(oglLink=link, cmdGroup=cmdGroup)

        elif isinstance(oglObjectToDelete, OglNote):
            oglNote: 'OglNote' = cast(OglNote, oglObjectToDelete)
            delNoteCmd: DeleteOglNoteCommand = DeleteOglNoteCommand(oglNote)
            cmdGroup.addCommand(delNoteCmd)

        elif isinstance(oglObjectToDelete, OglLink):
            oglLink: OglLink = cast(OglLink, oglObjectToDelete)
            cmdGroup = self._addADeleteLinkCommand(oglLink=oglLink, cmdGroup=cmdGroup)

        elif isinstance(oglObjectToDelete, OglObject):
            delObjCmd: DeleteOglObjectCommand = DeleteOglObjectCommand(oglObjectToDelete)
            cmdGroup.addCommand(delObjCmd)

        else:
            assert False, 'Unknown OGL Object'

        oglObjectToDelete.Detach()

        return cmdGroup

    def _addADeleteLinkCommand(self, oglLink: OglLink, cmdGroup: CommandGroup) -> CommandGroup:

        delOglLinkCmd: DelOglLinkCommand = DelOglLinkCommand(oglLink)
        cmdGroup.addCommand(delOglLinkCmd)

        return cmdGroup
