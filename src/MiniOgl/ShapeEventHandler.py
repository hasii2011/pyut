
from wx import MouseEvent

__all__ = ["ShapeEventHandler"]

DEBUG = 0


class ShapeEventHandler:
    """
    Let a shape receive mouse events directly.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def OnLeftDown(self, event: MouseEvent):
        """
        Callback for left clicks.

        @param  event
        """
        if DEBUG:
            print("Unhandled left down")
        event.Skip()

    def OnLeftUp(self, event: MouseEvent):
        """
        Callback for left clicks.

        @param  event
        """
        if DEBUG:
            print("Unhandled left up")
        event.Skip()

    def OnLeftDClick(self, event: MouseEvent):
        """
        Callback for left double clicks.

        @param  event
        """
        if DEBUG:
            print("Unhandled left double click")
        event.Skip()

    def OnMiddleDown(self, event: MouseEvent):
        """
        Callback for middle clicks.

        @param  event
        """
        if DEBUG:
            print("Unhandled middle down")
        event.Skip()

    def OnMiddleUp(self, event: MouseEvent):
        """
        Callback for middle clicks.

        @param  event
        """
        if DEBUG:
            print("Unhandled middle up")
        event.Skip()

    def OnMiddleDClick(self, event: MouseEvent):
        """
        Callback for middle double clicks.

        @param  event
        """
        if DEBUG:
            print("Unhandled middle double click")
        event.Skip()

    def OnRightDown(self, event: MouseEvent):
        """
        Callback for right clicks.

        @param  event
        """
        if DEBUG:
            print("Unhandled right down")
        event.Skip()

    def OnRightUp(self, event: MouseEvent):
        """
        Callback for right clicks.

        @param  event
        """
        if DEBUG:
            print("Unhandled right up")
        event.Skip()

    def OnRightDClick(self, event: MouseEvent):
        """
        Callback for right double clicks.

        @param  event
        """
        if DEBUG:
            print("Unhandled right double click")
        event.Skip()
