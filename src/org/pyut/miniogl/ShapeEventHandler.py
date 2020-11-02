
from logging import Logger
from logging import getLogger

from wx import MouseEvent


class ShapeEventHandler:

    clsLogger: Logger = getLogger(__name__)

    def __init__(self):
        """
        Let a shape receive mouse events directly.
        """
    def OnLeftDown(self, event: MouseEvent):
        """
        Callback for left clicks.
        Args:
            event:
        """
        ShapeEventHandler.clsLogger.info("Unhandled left down")
        event.Skip()

    def OnLeftUp(self, event: MouseEvent):
        """
        Callback for left clicks.

        Args:
            event:
        """
        ShapeEventHandler.clsLogger.debug("Unhandled left up")
        event.Skip()

    def OnLeftDClick(self, event: MouseEvent):
        """
        Callback for left double clicks.

        @param  event
        """
        ShapeEventHandler.clsLogger.debug("Unhandled left double click")
        event.Skip()

    def OnMiddleDown(self, event: MouseEvent):
        """
        Callback for middle clicks.

        Args:
            event:
        """
        ShapeEventHandler.clsLogger.debug("Unhandled middle down")
        event.Skip()

    def OnMiddleUp(self, event: MouseEvent):
        """
        Callback for middle clicks.

        Args:
            event:
        """
        ShapeEventHandler.clsLogger.debug("Unhandled middle up")
        event.Skip()

    def OnMiddleDClick(self, event: MouseEvent):
        """
        Callback for middle double clicks.

        Args:
            event:
        """
        ShapeEventHandler.clsLogger.debug("Unhandled middle double click")
        event.Skip()

    def OnRightDown(self, event: MouseEvent):
        """
        Callback for right clicks.
        Args:
            event:
        """
        ShapeEventHandler.clsLogger.debug("Unhandled right down")
        event.Skip()

    def OnRightUp(self, event: MouseEvent):
        """
        Callback for right clicks.
        Args:
            event:
        """
        ShapeEventHandler.clsLogger.debug("Unhandled right up")
        event.Skip()

    def OnRightDClick(self, event: MouseEvent):
        """
        Callback for right double clicks.
        Args:
            event:
        """
        ShapeEventHandler.clsLogger.debug("Unhandled right double click")
        event.Skip()
