from wx import Button
from wx import CANCEL
from wx import Dialog
from wx import EVT_BUTTON
from wx import EVT_TEXT
from wx import NewIdRef as wxNewIdRef
from wx import OK
from wx import Point
from wx import Size
from wx import StaticText
from wx import TE_MULTILINE
from wx import TextCtrl

from Globals import _

TXT_COMMENT = wxNewIdRef()


class DlgEditComment(Dialog):
    """
    Dialog for the class comment edition.
    """

    def __init__(self, parent, ID, pyutClass):
        """

        Args:
            parent:
            ID:
            pyutClass:
        """

        super().__init__(parent, ID, _("Description Edit"))

        # Associated PyutLink
        self._pyutClass = pyutClass

        self.SetSize(Size(416, 200))

        # init members vars
        self._text = self._pyutClass.getDescription()
        self._returnAction = -1   # describe how the user exited the dialog box

        # labels
        StaticText(self, -1, _("Class description"),  Point(8, 8))

        # text
        self._txtCtrl: TextCtrl = TextCtrl(self, TXT_COMMENT, self._text, Point(8, 24), Size(392, 100), TE_MULTILINE)

        # Set the focus
        self._txtCtrl.SetFocus()

        # text events
        self.Bind(EVT_TEXT, self._onTxtNoteChange, id=TXT_COMMENT)

        # Ok/Cancel
        Button(self, OK, _("&Ok"), Point(120, 140))
        Button(self, CANCEL, _("&Cancel"), Point(208, 140))

        # button events
        self.Bind(EVT_BUTTON, self._onCmdOk, id=OK)
        self.Bind(EVT_BUTTON, self._onCmdCancel, id=CANCEL)

        self.Centre()
        self.ShowModal()

    def _onTxtNoteChange(self, event):
        """
        Event occurring when TXT_COMMENT change.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._text = event.GetString()

    # noinspection PyUnusedLocal
    def _onCmdOk(self, event):
        """
        Handle click on "Ok" button.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        self._pyutClass.setDescription(self._text)

        self._returnAction = OK
        self.Close()

    # noinspection PyUnusedLocal
    def _onCmdCancel(self, event):
        """
        Handle click on "Cancel" button.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._returnAction = CANCEL
        self.Close()

    def getReturnAction(self):
        """
        Return an info on how the user exited the dialog box

        @return : wx.Ok = click on Ok button; wx.Cancel = click on Cancel button
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._returnAction
