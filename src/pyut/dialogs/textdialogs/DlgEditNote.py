
from wx import EVT_TEXT
from wx import TE_MULTILINE

from wx import CommandEvent
from wx import TextCtrl
from wx import Window
from wx.lib.sized_controls import SizedPanel

from pyut.dialogs.BaseEditDialog import BaseEditDialog

from pyutmodel.PyutNote import PyutNote

from pyut.uiv2.eventengine.IEventEngine import IEventEngine


class DlgEditNote(BaseEditDialog):
    """
    Defines a multi-line text control dialog for note editing.
    This dialog is used to ask the user to enter the text that will be
    displayed in a UML note.

    Sample use:
        with DlgEditNote(umlFrame, pyutNote) as dlg:
            if dlg.ShowModal() == ID_OK:
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    """
    def __init__(self, parent: Window, eventEngine: IEventEngine, pyutNote: PyutNote):
        """

        Args:
            parent:      parent window to center on
            eventEngine:
            pyutNote:    Model object we are editing
        """
        super().__init__(parent, eventEngine=eventEngine, title="Edit Note")

        self._pyutNote: PyutNote = pyutNote

        sizedPanel: SizedPanel = self.GetContentsPane()

        self._txtCtrl: TextCtrl = TextCtrl(sizedPanel, value=self._pyutNote.content, size=(400, 180), style=TE_MULTILINE)
        self._txtCtrl.SetFocus()

        self._createStandardOkCancelButtonSizer()

        self.Bind(EVT_TEXT, self._onTxtNoteChange, self._txtCtrl)

        self.Centre()

    def _onTxtNoteChange(self, event: CommandEvent):
        """
        Handle changes to the text in the widget identified by TXT_NOTE

        Args:
            event:
        """
        self._pyutNote.content = event.GetString()
        self._markCurrentDiagramAsModified()
