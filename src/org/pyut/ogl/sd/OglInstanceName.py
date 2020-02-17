
from wx import CANCEL
from wx import CENTRE
from wx import FONTFAMILY_TELETYPE
from wx import FONTSTYLE_ITALIC
from wx import FONTWEIGHT_NORMAL

from wx import Font
from wx import ID_OK
from wx import OK

from wx import TextEntryDialog

from org.pyut.MiniOgl.ShapeEventHandler import ShapeEventHandler
from org.pyut.MiniOgl.TextShape import TextShape

from org.pyut.PyutSDInstance import PyutSDInstance

from org.pyut.general.Globals import _


class OglInstanceName(TextShape, ShapeEventHandler):

    TEXT_SHAPE_FONT_SIZE: int = 12
    """
    TextShape that supports text editing
    """
    def __init__(self, pyutObject: PyutSDInstance, x: float, y: float, text: str, parent=None):
        """
        """
        self._pyutObject = pyutObject

        self._defaultFont = Font(OglInstanceName.TEXT_SHAPE_FONT_SIZE, FONTFAMILY_TELETYPE, FONTSTYLE_ITALIC, FONTWEIGHT_NORMAL)

        TextShape.__init__(self, x, y, text, parent=parent, font=self._defaultFont)

    def OnLeftDClick(self, event):
        """
        """
        dlg = TextEntryDialog(None, _("Message"), _("Enter message"), self._pyutObject.getInstanceName(), OK | CANCEL | CENTRE)
        if dlg.ShowModal() == ID_OK:
            self._pyutObject.setInstanceName(dlg.GetValue())
        dlg.Destroy()
