
import wx

from PyutLink import PyutLink
from OglLink import OglLink

from DlgRemoveLink import DlgRemoveLink

from Mediator import Mediator


class OglInheritance(OglLink):
    """
    Graphical OGL representation of an inheritance link.
    This class provide the methods for drawing an inheritance link between
    two classes of an UML diagram. Add labels to an OglLink.

    @version $Revision: 1.4 $
    """

    def __init__(self, srcShape, pyutLink, dstShape):
        """
        Constructor.

        @param OglClass srcShape : Source shape
        @param PyutLink pyutLink : Conceptual links associated with the graphical links.
        @param OglClass dstShape : Destination shape

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        super().__init__(srcShape, pyutLink, dstShape)
        # Arrow must be white inside
        self.SetBrush(wx.WHITE_BRUSH)
        self.SetDrawArrow(True)

    def cleanUp(self):
        """
        Clean up object references before quitting.

        @since 1.4
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        OglLink.cleanUp(self)
        self.ClearArrowsAtPosition()  # remove all arrows

    # noinspection PyUnusedLocal
    def OnLeftClick(self, x, y, keys, attachment):
        """
        Event handler for left mouse click.
        This event handler call the link dialog to edit link properties.

        @param int x : X position
        @param int y : Y position
        @param int keys : ...
        @param int attachment : ...
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # get the shape
        # shape = self.GetShape()
        dlg = DlgRemoveLink()
        rep = dlg.ShowModal()
        dlg.Destroy()
        if rep == wx.ID_YES:  # destroy link
            Mediator().removeLink(self)
        self._diagram.Refresh()
