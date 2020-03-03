
from wx import ALIGN_BOTTOM
from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALL
from wx import BOTTOM
from wx import EVT_TEXT
from wx import EXPAND
from wx import ID_ANY
from wx import TE_MULTILINE
from wx import VERTICAL

from wx import CommandEvent
from wx import TextCtrl
from wx import StaticText
from wx import BoxSizer
from wx import Window

from org.pyut.dialogs.BaseDlgEditText import BaseDlgEditText
from org.pyut.model.PyutNote import PyutNote
from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _
[
    TXT_NOTE
] = PyutUtils.assignID(1)


class DlgEditNote(BaseDlgEditText):
    """
    Defines a multi-line text control dialog for note editing.
    This dialog is used to ask the user to enter the text that will be
    displayed in a UML note.

    Sample use:
        dlg = DlgEditNote(self._uml, ID_ANY, pyutNote)
        dlg.Destroy()
    """
    def __init__(self, parent: Window, dialogIdentifier, pyutNote: PyutNote):
        """

        Args:
            parent:             parent window to center on
            dialogIdentifier:   An identifier for the dialog
            pyutNote:           Model object we are editing
        """
        super().__init__(parent, dialogIdentifier, _("Note Edit"))

        self._pyutNote:     PyutNote = pyutNote

        label = StaticText(self, ID_ANY, _("Note text"))

        self._txtCtrl = TextCtrl(self, TXT_NOTE, self._pyutNote.getName(), size=(400, 180), style=TE_MULTILINE)

        self._txtCtrl.SetFocus()

        sizerButtons: BoxSizer = self._createDialogButtons()
        # Sizer for all components
        szrMain: BoxSizer = BoxSizer(VERTICAL)
        szrMain.Add(label, 0, BOTTOM, 5)
        szrMain.Add(self._txtCtrl, 1, EXPAND | BOTTOM, 10)
        szrMain.Add(sizerButtons, 0, ALIGN_CENTER_HORIZONTAL | ALIGN_BOTTOM)

        # Border
        szrBorder: BoxSizer = BoxSizer(VERTICAL)
        szrBorder.Add(szrMain, 1, EXPAND | ALL, 10)
        self.SetSizer(szrBorder)
        szrBorder.Fit(self)

        # Set up the event handlers
        self.Bind(EVT_TEXT, self._onTxtNoteChange, id=TXT_NOTE)

        self.Centre()
        self.ShowModal()

    def _onTxtNoteChange(self, event: CommandEvent):
        """
        Handle when the text in the widget identified by TXT_NOTE change.s

        Args:
            event:
        """
        self._pyutNote.setName(event.GetString())
