
from typing import List

from logging import Logger
from logging import getLogger


from wx import CommandEvent

from wx import Menu

from pyutmodel.PyutObject import PyutObject

from org.pyut.ui.PyutProject import PyutProject
from org.pyut.ui.PyutUI import PyutUI
from org.pyut.ui.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from org.pyut.ui.frame.BaseMenuHandler import BaseMenuHandler

from org.pyut.PyutUtils import PyutUtils

# noinspection PyProtectedMember
from org.pyut.general.Globals import _

from org.pyut.history.HistoryManager import HistoryManager
from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine


class EditMenuHandler(BaseMenuHandler):

    def __init__(self, editMenu: Menu, eventEngine: IEventEngine = None):

        super().__init__(menu=editMenu, eventEngine=eventEngine)

        self.logger:    Logger   = getLogger(__name__)

        self._treeNotebookHandler: PyutUI = self._mediator.getFileHandling()
        self._clipboard:           List[PyutObject]    = []

    # noinspection PyUnusedLocal
    def onUndo(self, event: CommandEvent):
        """

        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.Undo)

    # noinspection PyUnusedLocal
    def onRedo(self, event: CommandEvent):
        """

        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.Redo)

    # noinspection PyUnusedLocal
    def onCut(self, event: CommandEvent):
        """
        May be invoked directly from a menu item or from another component by posting the appropriate event
        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.CutShapes)

    # noinspection PyUnusedLocal
    def onCopy(self, event: CommandEvent):
        """
        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.CopyShapes)

    # noinspection PyUnusedLocal
    def onPaste(self, event: CommandEvent):
        """

        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.PasteShapes)

    # noinspection PyUnusedLocal
    def onSelectAll(self, event: CommandEvent):
        """
        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.SelectAllShapes)

    # noinspection PyUnusedLocal
    def onAddPyut(self, event: CommandEvent):
        """
        Add Pyut UML Diagram.

        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.AddOglDiagram)

    # noinspection PyUnusedLocal
    def onAddOgl(self, event: CommandEvent):
        """
        Add Pyut-Ogl UML Diagram.

        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.AddOglDiagram)

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
        project.modified = True
        self._mediator.updateTitle()
        frame.Refresh()
