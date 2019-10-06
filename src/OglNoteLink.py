
from wx import ID_YES
from wx import PENSTYLE_LONG_DASH

from wx import Pen

from OglLink import OglLink
from org.pyut.dialogs.DlgRemoveLink import DlgRemoveLink


class OglNoteLink(OglLink):
    """
    A note like link, with dashed line and no arrows.
    To get a new link, you should use the `OglLinkFactory` and specify
    the kind of link you want, OGL_NOTELINK for an instance of this class.

    :version: $Revision: 1.8 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    def __init__(self, srcShape, pyutLink, dstShape):
        """
        Constructor.

        @param OglObject srcShape : Source shape
        @param PyutLinkedObject pyutLink : Conceptual links associated with the graphical links.
        @param OglObject dstShape : Destination shape
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        super().__init__(srcShape, pyutLink, dstShape)
        self.SetDrawArrow(False)
        self.SetPen(Pen("BLACK", 1, PENSTYLE_LONG_DASH))

    # noinspection PyUnusedLocal
    def OnLeftClick(self, x: int, y: int, keys, attachment: int):   # Does not appear to be used
        """
        Event handler for left mouse click.
        This event handler call the link dialog to edit link properties.

        @param  x : X position
        @param  y : Y position
        @param  keys : ...
        @param  attachment : ...
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        # Open dialog to edit link
        dlg = DlgRemoveLink()
        rep = dlg.ShowModal()
        dlg.Destroy()
        if rep == ID_YES:    # destroy link
            # Mediator().removeLink(self) # missing method
            pass
        self._diagram.Refresh()
