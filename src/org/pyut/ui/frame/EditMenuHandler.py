
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from copy import copy

from wx import ClientDC
from wx import CommandEvent

from wx import Menu

from org.pyut.history.commands.DelOglLinkCommand import DelOglLinkCommand
from org.pyut.history.commands.DeleteOglNoteCommand import DeleteOglNoteCommand
from org.pyut.history.commands.DeleteOglObjectCommand import DeleteOglObjectCommand
from org.pyut.model.PyutActor import PyutActor
from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutNote import PyutNote
from org.pyut.model.PyutObject import PyutObject
from org.pyut.model.PyutUseCase import PyutUseCase

from org.pyut.miniogl.Diagram import Diagram

from org.pyut.ogl.OglActor import OglActor
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglUseCase import OglUseCase

from org.pyut.ui.PyutProject import PyutProject
from org.pyut.ui.TreeNotebookHandler import TreeNotebookHandler
from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.frame.BaseMenuHandler import BaseMenuHandler

from org.pyut.history.commands.CommandGroup import CommandGroup
from org.pyut.history.commands.DeleteOglClassCommand import DeleteOglClassCommand

from org.pyut.PyutUtils import PyutUtils

# noinspection PyProtectedMember
from org.pyut.general.Globals import _


from org.pyut.history.HistoryManager import HistoryManager


class EditMenuHandler(BaseMenuHandler):

    def __init__(self, editMenu: Menu):

        super().__init__(menu=editMenu)

        self.logger:    Logger   = getLogger(__name__)

        self._treeNotebookHandler: TreeNotebookHandler = self._mediator.getFileHandling()
        self._clipboard:           List[PyutObject]    = []

    # noinspection PyUnusedLocal
    def onUndo(self, event: CommandEvent):
        """

        Args:
            event:
        """
        currentFrame = self._treeNotebookHandler.getCurrentFrame()
        if currentFrame is None:
            PyutUtils.displayWarning(msg=_('No selected/available frame'), title=_('Huh!'))
        else:
            historyManager: HistoryManager = currentFrame.getHistory()
            if historyManager.isUndoPossible() is True:
                historyManager.undo()
            else:
                PyutUtils.displayWarning(msg=_('Nothing to undo'), title=_('Huh!'))

    # noinspection PyUnusedLocal
    def onRedo(self, event: CommandEvent):
        """

        Args:
            event:
        """
        currentFrame = self._treeNotebookHandler.getCurrentFrame()
        if currentFrame is None:
            PyutUtils.displayWarning(msg=_('No selected/available frame'), title=_('Huh!'))
        else:
            historyManager: HistoryManager = currentFrame.getHistory()
            if historyManager.isRedoPossible() is True:
                historyManager.redo()
            else:
                PyutUtils.displayWarning(msg=_('Nothing to redo'), title=_('Huh!'))

    # noinspection PyUnusedLocal
    def onCut(self, event: CommandEvent):
        """

        Args:
            event:
        """
        selected = self._mediator.getSelectedShapes()
        if len(selected) > 0:
            self._clipboard = []
        else:
            self.logger.warning(f'No selected objects')
            return

        umlFrame:       UmlClassDiagramsFrame = selected[0].GetDiagram().GetPanel()
        historyManager: HistoryManager        = umlFrame.historyManager
        cmdGroup:       CommandGroup          = CommandGroup("Delete UML object(s)")

        # put the PyutObjects in the clipboard and remove their graphical representation from the diagram
        for obj in selected:

            if isinstance(obj, OglClass):
                oglClass: OglClass              = cast(OglClass, obj)
                cmd:      DeleteOglClassCommand = DeleteOglClassCommand(oglClass)
                cmdGroup.addCommand(cmd)
            elif isinstance(obj, OglNote):
                oglNote: OglNote = cast(OglNote, obj)
                delNoteCmd: DeleteOglNoteCommand = DeleteOglNoteCommand(oglNote)
                cmdGroup.addCommand(delNoteCmd)
            elif isinstance(obj, OglLink):
                oglLink: OglLink = cast(OglLink, obj)
                delOglLinkCmd: DelOglLinkCommand = DelOglLinkCommand(oglLink)
                cmdGroup.addCommand(delOglLinkCmd)
            elif isinstance(obj, OglObject):
                delObjCmd: DeleteOglObjectCommand = DeleteOglObjectCommand(obj)
                cmdGroup.addCommand(delObjCmd)
            else:
                assert False, 'Unknown OGL Object'
            obj.Detach()
            self._clipboard.append(obj.pyutObject)

        historyManager.addCommandGroup(cmdGroup)
        historyManager.execute()

        self.logger.info(f'Cut {len(self._clipboard)} objects')

        self._treeNotebookHandler.setModified(True)
        self._mediator.updateTitle()
        umlFrame.Refresh()

    # noinspection PyUnusedLocal
    def onCopy(self, event: CommandEvent):
        """
        TODO : adapt for OglLinks

        Args:
            event:
        """
        selected = self._mediator.getSelectedShapes()
        if len(selected) > 0:
            self._clipboard = []
        else:
            return

        # put a copy of the PyutObjects in the clipboard
        for obj in selected:
            obj = copy(obj.pyutObject)
            obj.setLinks([])   # we don't want to copy the links
            self._clipboard.append(obj)

        self.logger.info(f'Copied {len(self._clipboard)} objects')

    # noinspection PyUnboundLocalVariable
    # noinspection PyUnusedLocal
    def onPaste(self, event: CommandEvent):
        """

        Args:
            event:
        """
        if len(self._clipboard) == 0:
            return

        self.logger.info(f'Pasting {len(self._clipboard)} objects')
        frame = self._mediator.getUmlFrame()
        if frame == -1:
            PyutUtils.displayError(_("No frame to paste into"))
            return

        # put the objects in the clipboard and remove them from the diagram
        x, y = 100, 100
        for clipboardObject in self._clipboard:
            obj: PyutObject = copy(clipboardObject)
            if isinstance(obj, PyutClass):
                po: OglObject = OglClass(obj)
            elif isinstance(obj, PyutNote):
                po = OglNote(obj)
            elif isinstance(obj, PyutActor):
                po = OglActor(obj)
            elif isinstance(obj, PyutUseCase):
                po = OglUseCase(obj)
            else:
                self.logger.error(f'Error when try to paste object: {obj}')
                return
            self.logger.info(f'Pasting: {po=}')
            self._mediator.getUmlFrame().addShape(po, x, y)
            x += 20
            y += 20

        canvas = po.GetDiagram().GetPanel()
        # the frame that contains the shape
        # specify the canvas on which we will paint
        dc: ClientDC = ClientDC(canvas)
        canvas.PrepareDC(dc)

        self._treeNotebookHandler.setModified(True)
        self._mediator.updateTitle()
        canvas.Refresh()

    # noinspection PyUnusedLocal
    def onSelectAll(self, event: CommandEvent):
        """

        Args:
            event:
        """
        frame: UmlClassDiagramsFrame = self._mediator.getUmlFrame()

        if frame is None:
            PyutUtils.displayError(_("No frame found !"))
            return
        diagram: Diagram         = frame.GetDiagram()
        shapes:  List[OglObject] = diagram.GetShapes()
        for oglShape in shapes:
            shape: OglObject = cast(OglObject, oglShape)
            shape.SetSelected(True)

        frame.Refresh()

    # noinspection PyUnusedLocal
    def onAddPyut(self, event: CommandEvent):
        """
        Add Pyut UML Diagram.

        Args:
            event:
        """
        frame: UmlClassDiagramsFrame = self._mediator.getUmlFrame()
        if self._isDiagramFormOpen(frame) is True:
            frame.addPyutHierarchy()
            self._refreshUI(frame)

    # noinspection PyUnusedLocal
    def onAddOgl(self, event: CommandEvent):
        """
        Add Pyut-Ogl UML Diagram.

        Args:
            event:
        """
        frame: UmlClassDiagramsFrame = self._mediator.getUmlFrame()
        if self._isDiagramFormOpen(frame) is True:
            frame.addOglHierarchy()
            self._refreshUI(frame)

    def _isDiagramFormOpen(self, frame: UmlClassDiagramsFrame) -> bool:
        """
        Does 2 things, Checks and displays the dialog;  Oh well

        Args:
            frame:

        Returns: `True` if there is a frame open else, `False`
        """
        if frame is None:
            PyutUtils.displayWarning(msg=_("Please open a diagram to hold the UML"), title=_('Silly User'), parent=self._parent)
            return False
        else:
            return True

    def _refreshUI(self, frame: UmlClassDiagramsFrame):

        project: PyutProject = self._treeNotebookHandler.getCurrentProject()
        project.setModified(True)
        self._mediator.updateTitle()
        frame.Refresh()
