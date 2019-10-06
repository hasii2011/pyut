
import wx

from pyutUtils import *

from globals import _

[
    TXT_USECASE
] = assignID(1)


class DlgEditUseCase(wx.Dialog):
    """
    Defines a multiline text control dialog for use case editing.
    This dialog is used to ask the user to enter the text that will be
    displayed into an UML Use case.

    Sample of use::
        dlg = DlgEditUseCase(self._uml, -1, pyutUseCase)
        dlg.Destroy()

    :version: $Revision: 1.5 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """
    def __init__(self, parent, ID, pyutUseCase):
        """
        Constructor.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        super().__init__(parent, ID, _("Use Case Edit"), style=wx.RESIZE_BORDER | wx.CAPTION)

        # Associated PyutUseCase
        self._pyutUseCase = pyutUseCase

        self.SetAutoLayout(True)

        self._text = self._pyutUseCase.getName()
        self._returnAction = -1   # describe how the user exited the dialog box

        label = wx.StaticText(self, -1, _("Use case text"))

        self._txtCtrl = wx.TextCtrl(self, TXT_USECASE, self._text, size=(400, 180), style=wx.TE_MULTILINE)
        self._txtCtrl.SetFocus()

        # text events
        self.Bind(wx.EVT_TEXT, self._onTxtChange, id=TXT_USECASE)

        btnOk = wx.Button(self, wx.OK, _("&Ok"))
        btnOk.SetDefault()
        btnCancel = wx.Button(self, wx.CANCEL, _("&Cancel"))

        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)

        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrButtons.Add(btnOk, 0, wx.RIGHT, 10)
        szrButtons.Add(btnCancel, 0, wx.ALL)

        szrMain = wx.BoxSizer(wx.VERTICAL)
        szrMain.Add(label, 0, wx.BOTTOM, 5)
        szrMain.Add(self._txtCtrl, 1, wx.EXPAND | wx.BOTTOM, 10)
        szrMain.Add(szrButtons, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM)
        # Border
        szrBorder = wx.BoxSizer(wx.VERTICAL)
        szrBorder.Add(szrMain, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(szrBorder)
        szrBorder.Fit(self)

        self.Centre()
        self.ShowModal()

    def _onTxtChange(self, event):
        """
        Event occuring when TXT_NOTE change.

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

        self._pyutUseCase.setName(self._text)
        self._returnAction = wx.OK
        self.Close()

    # noinspection PyUnusedLocal
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
