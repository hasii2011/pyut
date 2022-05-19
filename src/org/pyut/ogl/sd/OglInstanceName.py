
from wx import CANCEL
from wx import CENTRE
from wx import FONTFAMILY_TELETYPE
from wx import FONTSTYLE_ITALIC
from wx import FONTWEIGHT_NORMAL

from wx import Font
from wx import ID_OK
from wx import OK

from wx import TextEntryDialog

from miniogl.ShapeEventHandler import ShapeEventHandler
from miniogl.TextShape import TextShape

from pyutmodel.PyutSDInstance import PyutSDInstance


class OglInstanceName(TextShape, ShapeEventHandler):

    TEXT_SHAPE_FONT_SIZE: int = 12
    """
    TextShape that supports text editing
    """
    def __init__(self, pyutObject: PyutSDInstance, x: int, y: int, text: str, parent=None):
        """
        """
        self._pyutObject = pyutObject

        self._defaultFont = Font(OglInstanceName.TEXT_SHAPE_FONT_SIZE, FONTFAMILY_TELETYPE, FONTSTYLE_ITALIC, FONTWEIGHT_NORMAL)

        TextShape.__init__(self, x, y, text, parent=parent, font=self._defaultFont)

    def OnLeftDClick(self, event):
        """
        """
        dlg = TextEntryDialog(None, "Message", "Enter instance name", self._pyutObject.getInstanceName(), OK | CANCEL | CENTRE)
        if dlg.ShowModal() == ID_OK:
            self._pyutObject.setInstanceName(dlg.GetValue())
        dlg.Destroy()
