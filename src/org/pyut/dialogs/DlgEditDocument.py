
from logging import Logger
from logging import getLogger

from wx import ALIGN_BOTTOM
from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALL
from wx import BOTTOM
from wx import CAPTION
from wx import EVT_BUTTON
from wx import EVT_TEXT
from wx import EXPAND
from wx import HORIZONTAL
from wx import RESIZE_BORDER
from wx import ID_ANY
from wx import OK
from wx import CANCEL

from wx import Dialog
from wx import RIGHT
from wx import StaticText
from wx import TextCtrl
from wx import Button
from wx import VERTICAL
from wx import Window
from wx import BoxSizer

from org.pyut.PyutUtils import PyutUtils
from org.pyut.ui.PyutDocument import PyutDocument

from org.pyut.general.Globals import _

[
    TXT_DOCUMENT_NAME
] = PyutUtils.assignID(1)


class DlgEditDocument(Dialog):

    def __init__(self, parent: Window, dialogIdentifier, document: PyutDocument):
        """

        Args:
            parent:             The parent window
            dialogIdentifier
            document:           The UML document we want to edit
        """
        super().__init__(parent, dialogIdentifier, _("Document Edit"), style=RESIZE_BORDER | CAPTION)

        self.logger:    Logger       = getLogger(__name__)
        self._document: PyutDocument = document
        self._returnAction = -1   # describe how the user exited the dialog box

        self.SetAutoLayout(True)
        label = StaticText(self, ID_ANY, _("Document Name"))
        self._nameEntry: TextCtrl = TextCtrl(parent=self, id=TXT_DOCUMENT_NAME, value=document.title)
        self._nameEntry.SetFocus()

        btnOk:     Button = Button(self, OK, _("&Ok"))
        btnCancel: Button = Button(self, CANCEL, _("&Cancel"))

        btnOk.SetDefault()

        sizerButtons: BoxSizer = BoxSizer(HORIZONTAL)
        sizerButtons.Add(btnOk, 0, RIGHT, 10)
        sizerButtons.Add(btnCancel, 0, ALL)

        sizerMain: BoxSizer = BoxSizer(VERTICAL)
        sizerMain.Add(label, 0, BOTTOM, 5)
        sizerMain.Add(self._nameEntry, 1, EXPAND | BOTTOM, 10)
        sizerMain.Add(sizerButtons, 0, ALIGN_CENTER_HORIZONTAL | ALIGN_BOTTOM)

        sizerBorder: BoxSizer = BoxSizer(VERTICAL)
        sizerBorder.Add(sizerMain, 1, EXPAND | ALL, 10)
        self.SetSizer(sizerBorder)
        sizerBorder.Fit(self)

        self.Bind(EVT_TEXT,   self._onDocumentNameChange, id=TXT_DOCUMENT_NAME)
        self.Bind(EVT_BUTTON, self._onCmdOk,     id=OK)
        self.Bind(EVT_BUTTON, self._onCmdCancel, id=CANCEL)

        self.Centre()
        self.ShowModal()

    def getReturnAction(self):
        """
        Return an info on how the user exited the dialog box

        Returns:
            wx.Ok = click on Ok button; wx.Cancel = click on Cancel button
        """
        return self._returnAction

    # noinspection PyUnusedLocal
    def _onDocumentNameChange(self, event):
        self.logger.info(f'Howdy')
        self._document.title = event.GetString()

    # noinspection PyUnusedLocal
    def _onCmdOk(self, event):

        self._returnAction = OK
        self.Close()

    # noinspection PyUnusedLocal
    def _onCmdCancel(self, event):
        """
        Handle click on "Cancel" button.
        """
        self._returnAction = CANCEL
        self.Close()
