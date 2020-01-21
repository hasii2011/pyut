
from wx import CANCEL
from wx import CENTRE
from wx import ID_OK
from wx import OK

from wx import TextEntryDialog

from org.pyut.MiniOgl.ShapeEventHandler import ShapeEventHandler
from org.pyut.MiniOgl.TextShape import TextShape


class OglInstanceName(TextShape, ShapeEventHandler):
    """
    TextShape that supports text editing
    """
    def __init__(self, pyutObject, x, y, text, parent=None):
        """
        """
        self._pyutObject = pyutObject
        TextShape.__init__(self, x, y, text, parent)

    def OnLeftDClick(self, event):
        """
        """
        dlg = TextEntryDialog(None, _("Message"), _("Enter message"), self._pyutObject.getInstanceName(), OK | CANCEL | CENTRE)
        if dlg.ShowModal() == ID_OK:
            self._pyutObject.setInstanceName(dlg.GetValue())
        dlg.Destroy()
