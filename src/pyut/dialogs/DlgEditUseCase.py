
from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALL
from wx import BOTTOM
from wx import CANCEL
from wx import CAPTION
from wx import EVT_BUTTON
from wx import EVT_TEXT
from wx import EXPAND
from wx import HORIZONTAL
from wx import OK
from wx import RESIZE_BORDER
from wx import RIGHT
from wx import TE_MULTILINE
from wx import VERTICAL

from wx import BoxSizer
from wx import Button
from wx import TextCtrl
from wx import Dialog
from wx import StaticText

from pyut.PyutUtils import PyutUtils

from pyut.general.Globals import _

[
    TXT_USECASE
] = PyutUtils.assignID(1)


class DlgEditUseCase(Dialog):
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
        super().__init__(parent, ID, _("Use Case Edit"), style=RESIZE_BORDER | CAPTION)

        # Associated PyutUseCase
        self._pyutUseCase = pyutUseCase

        self.SetAutoLayout(True)

        self._text: str = self._pyutUseCase.name
        self._returnAction = -1   # describe how the user exited the dialog box

        label = StaticText(self, -1, _("Use case text"))

        self._txtCtrl = TextCtrl(self, TXT_USECASE, self._text, size=(400, 180), style=TE_MULTILINE)
        self._txtCtrl.SetFocus()

        # text events
        self.Bind(EVT_TEXT, self._onTxtChange, id=TXT_USECASE)

        btnOk = Button(self, OK, _("&Ok"))
        btnOk.SetDefault()
        btnCancel = Button(self, CANCEL, _("&Cancel"))

        self.Bind(EVT_BUTTON, self._onCmdOk, id=OK)
        self.Bind(EVT_BUTTON, self._onCmdCancel, id=CANCEL)

        szrButtons = BoxSizer(HORIZONTAL)
        szrButtons.Add(btnOk, 0, RIGHT, 10)
        szrButtons.Add(btnCancel, 0, ALL)

        szrMain = BoxSizer(VERTICAL)
        szrMain.Add(label, 0, BOTTOM, 5)
        szrMain.Add(self._txtCtrl, 1, EXPAND | BOTTOM, 10)
        szrMain.Add(szrButtons, 0, ALIGN_CENTER_HORIZONTAL)
        # Border
        szrBorder = BoxSizer(VERTICAL)
        szrBorder.Add(szrMain, 1, EXPAND | ALL, 10)
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

        self._pyutUseCase.name =self._text
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

        @return : Ok = click on Ok button; Cancel = click on Cancel button
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._returnAction
