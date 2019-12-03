
from logging import Logger
from logging import getLogger

from wx import MouseEvent


class ShapeEventHandler:

    def __init__(self):
        self.logger: Logger = getLogger(__name__)
    """
    Let a shape receive mouse events directly.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def OnLeftDown(self, event: MouseEvent):
        """
        Callback for left clicks.

        @param  event
        """
        self.logger.info("Unhandled left down")
        event.Skip()

    def OnLeftUp(self, event: MouseEvent):
        """
        Callback for left clicks.

        @param  event
        """
        self.logger.debug("Unhandled left up")
        event.Skip()

    def OnLeftDClick(self, event: MouseEvent):
        """
        Callback for left double clicks.

        @param  event
        """
        self.logger.debug("Unhandled left double click")
        event.Skip()

    def OnMiddleDown(self, event: MouseEvent):
        """
        Callback for middle clicks.

        @param  event
        """
        self.logger.debug("Unhandled middle down")
        event.Skip()

    def OnMiddleUp(self, event: MouseEvent):
        """
        Callback for middle clicks.

        @param  event
        """
        self.logger.debug("Unhandled middle up")
        event.Skip()

    def OnMiddleDClick(self, event: MouseEvent):
        """
        Callback for middle double clicks.

        @param  event
        """
        self.logger.debug("Unhandled middle double click")
        event.Skip()

    def OnRightDown(self, event: MouseEvent):
        """
        Callback for right clicks.

        @param  event
        """
        self.logger.debug("Unhandled right down")
        event.Skip()

    def OnRightUp(self, event: MouseEvent):
        """
        Callback for right clicks.

        @param  event
        """
        self.logger.debug("Unhandled right up")
        event.Skip()

    def OnRightDClick(self, event: MouseEvent):
        """
        Callback for right double clicks.

        @param  event
        """
        self.logger.debug("Unhandled right double click")
        event.Skip()
