
from logging import Logger
from logging import getLogger


from wx import CommandEvent

from wx import Menu


from pyut.ui.menuhandlers.BaseMenuHandler import BaseMenuHandler

from pyut.ui.eventengine.Events import EventType
from pyut.ui.eventengine.IEventEngine import IEventEngine


class EditMenuHandler(BaseMenuHandler):

    def __init__(self, editMenu: Menu, eventEngine: IEventEngine | None = None):

        super().__init__(menu=editMenu, eventEngine=eventEngine)

        self.logger:    Logger   = getLogger(__name__)

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
        self._eventEngine.sendEvent(EventType.AddPyutDiagram)

    # noinspection PyUnusedLocal
    def onAddOgl(self, event: CommandEvent):
        """
        Add Pyut-Ogl UML Diagram.

        Args:
            event:
        """
        self._eventEngine.sendEvent(EventType.AddOglDiagram)
