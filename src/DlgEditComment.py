
import wx

from globals import _

# from pyutUtils import assignID
from wx import NewId
TXT_COMMENT = NewId()


class DlgEditComment(wx.Dialog):
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

        wx.Dialog.__init__(self, parent, ID, _("Description Edit"))

        # Associated PyutLink
        self._pyutClass = pyutClass

        self.SetSize(wx.Size(416, 200))

        # init members vars
        self._text = self._pyutClass.getDescription()
        self._returnAction = -1   # describe how the user exited the dialog box

        # labels
        wx.StaticText(self, -1, _("Class description"),  wx.Point(8, 8))

        # text
        self._txtCtrl = wx.TextCtrl(self, TXT_COMMENT, self._text, wx.Point(8, 24), wx.Size(392, 100), wx.TE_MULTILINE)

        # Set the focus
        self._txtCtrl.SetFocus()

        # text events
        self.Bind(wx.EVT_TEXT, self._onTxtNoteChange, id=TXT_COMMENT)

        # Ok/Cancel
        wx.Button(self, wx.OK, _("&Ok"), wx.Point(120, 140))
        wx.Button(self, wx.CANCEL, _("&Cancel"), wx.Point(208, 140))

        # button events
        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)

        self.Centre()
        self.ShowModal()

    def _onTxtNoteChange(self, event):
        """
        Event occurring when TXT_COMMENT change.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._text = event.GetString()

    def _onCmdOk(self, event):
        """
        Handle click on "Ok" button.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        self._pyutClass.setDescription(self._text)

        self._returnAction = wx.OK
        self.Close()

    def _onCmdCancel(self, event):
        """
        Handle click on "Cancel" button.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._returnAction = wx.CANCEL
        self.Close()

    def getReturnAction(self):
        """
        Return an info on how the user exited the dialog box

        @return : wx.Ok = click on Ok button; wx.Cancel = click on Cancel button
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._returnAction
