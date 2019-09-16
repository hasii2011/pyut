from wx import Button
from wx import CANCEL
from wx import CAPTION
from wx import Dialog
from wx import EVT_TEXT
from wx import RESIZE_BORDER
from wx import StaticText
from wx import TE_MULTILINE
from wx import TextCtrl

from pyutUtils import assignID

from globals import _
[
    TXT_NOTE
] = assignID(1)


class DlgEditNote(Dialog):
    """
    Defines a multiline text control dialog for note editing.
    This dialog is used to ask the user to enter the text that will be
    displayed into an UML note.

    Sample of use::
        dlg = DlgEditNote(self._uml, -1, pyutNote)
        dlg.Destroy()

    :version: $Revision: 1.5 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    #>------------------------------------------------------------------------

    def __init__(self, parent, ID, pyutNote):
        """
        Constructor.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        wx.Dialog.__init__(self, parent, ID, _("Note Edit"), style=RESIZE_BORDER | CAPTION)

        # Associated PyutLink
        self._pyutNote = pyutNote

        self.SetAutoLayout(True)
        #~ self.SetSize(wx.Size(416, 200))

        #init members vars
        self._text = self._pyutNote.getName()
        self._returnAction = -1   # describe how the user exited the dialog box

        # labels
        label = StaticText(self, -1, _("Note text"))

        # text
        self._txtCtrl = TextCtrl(self, TXT_NOTE, self._text, size=(400, 180), style=TE_MULTILINE)

        # Set the focus
        self._txtCtrl.SetFocus()

        # text events
        self.Bind(EVT_TEXT, self._onTxtNoteChange, id=TXT_NOTE)

        # Ok/Cancel
        btnOk = Button(self, OK, _("&Ok"))
        btnOk.SetDefault()
        btnCancel = Button(self, CANCEL, _("&Cancel"))

        # button events
        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)

        # Sizer for buttons
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrButtons.Add(btnOk, 0, wx.RIGHT, 10)
        szrButtons.Add(btnCancel, 0, wx.ALL)

        # Sizer for all components
        szrMain = wx.BoxSizer(wx.VERTICAL)
        szrMain.Add(label, 0, wx.BOTTOM, 5)
        szrMain.Add(self._txtCtrl, 1, wx.EXPAND|wx.BOTTOM, 10)
        szrMain.Add(szrButtons, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_BOTTOM)

        # Border
        szrBorder = wx.BoxSizer(wx.VERTICAL)
        szrBorder.Add(szrMain, 1, wx.EXPAND|wx.ALL, 10)
        self.SetSizer(szrBorder)
        szrBorder.Fit(self)

        self.Centre()
        self.ShowModal()

    #>------------------------------------------------------------------------

    def _onTxtNoteChange(self, event):
        """
        Event occuring when TXT_NOTE change.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._text = event.GetString()

    #>------------------------------------------------------------------------

    def _onCmdOk(self, event):
        """
        Handle click on "Ok" button.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        self._pyutNote.setName(self._text)

        self._returnAction=wx.OK
        self.Close()


    #>------------------------------------------------------------------------

    def _onCmdCancel(self, event):
        """
        Handle click on "Cancel" button.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._returnAction=wx.CANCEL
        self.Close()

    #>------------------------------------------------------------------------

    def getReturnAction(self):
        """
        Return an info on how the user exited the dialog box

        @return : wx.Ok = click on Ok button; wx.Cancel = click on Cancel button
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._returnAction

