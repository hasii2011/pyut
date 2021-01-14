
from wx import EVT_TEXT
from wx import TE_MULTILINE

from wx import CommandEvent
from wx import TextCtrl
from wx import Window

from org.pyut.dialogs.textdialogs.BaseDlgEditText import BaseDlgEditText

from org.pyut.model.PyutText import PyutText

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _
[
    ID_TEXT_LINE
] = PyutUtils.assignID(1)


class DlgEditText(BaseDlgEditText):
    """
    Defines a multi-line text control dialog for placing an editing
    text on the UML Diagram


    Sample use:
        dlg = DlgEditText(self._uml, ID_ANY, pyutText)
        dlg.ShowModal()
        dlg.Destroy()
    """
    def __init__(self, parent: Window, dialogIdentifier, pyutText: PyutText):
        """

        Args:
            parent:             parent window to center on
            dialogIdentifier:   An identifier for the dialog
            pyutText:           Model object we are editing
        """
        super().__init__(parent, dialogIdentifier, _("Diagram Text"))

        self.pyutText: PyutText = pyutText

        self._txtCtrl: TextCtrl = TextCtrl(self, ID_TEXT_LINE, self.pyutText.content, size=(300, 80), style=TE_MULTILINE)
        self._txtCtrl.SetFocus()

        self._setupMainDialogLayout(self._txtCtrl)

        self.Bind(EVT_TEXT, self._onTextLineChange, id=ID_TEXT_LINE)

        self.Centre()

    def _onTextLineChange(self, event: CommandEvent):
        """
        Handle changes to the text in the widget identified by TXT_NOTE

        Args:
            event:
        """
        self.pyutText.content = event.GetString()
