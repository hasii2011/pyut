
from logging import Logger
from logging import getLogger

from wx import EVT_TEXT
from wx import ID_ANY

from wx import StaticText
from wx import TextCtrl
from wx import Window

from org.pyut.PyutUtils import PyutUtils

from org.pyut.dialogs.BaseDlgEditText import BaseDlgEditText

from org.pyut.ui.PyutDocument import PyutDocument

from org.pyut.general.Globals import _

[
    TXT_DOCUMENT_NAME
] = PyutUtils.assignID(1)


class DlgEditDocument(BaseDlgEditText):

    def __init__(self, parent: Window, dialogIdentifier, document: PyutDocument):
        """

        Args:
            parent:             The parent window
            dialogIdentifier    An identifier for the dialog
            document:           The UML document we want to edit
        """
        super().__init__(parent, dialogIdentifier, _("Document Edit"))

        self.logger:    Logger       = getLogger(__name__)
        self._document: PyutDocument = document

        label: StaticText = StaticText(self, ID_ANY, _("Document Name"))
        self._nameEntry: TextCtrl = TextCtrl(parent=self, id=TXT_DOCUMENT_NAME, value=document.title)
        self._nameEntry.SetFocus()

        self._setupMainDialogLayout(self._nameEntry, label)

        self.Bind(EVT_TEXT,   self._onDocumentNameChange, id=TXT_DOCUMENT_NAME)

        self.Centre()
        self.ShowModal()

    # noinspection PyUnusedLocal
    def _onDocumentNameChange(self, event):
        self._document.title = event.GetString()
