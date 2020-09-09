
from logging import Logger
from logging import getLogger

from wx import ALL
from wx import CANCEL
from wx import CENTER
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EXPAND
from wx import HORIZONTAL
from wx import ICON_EXCLAMATION
from wx import MessageDialog
from wx import OK
from wx import VERTICAL
from wx import ID_ANY
from wx import ID_OK

from wx import CommandEvent
from wx import Dialog
from wx import BoxSizer
from wx import Button

from wx.lib.agw.fmresources import INB_BORDER
from wx.lib.agw.fmresources import INB_DRAW_SHADOW
from wx.lib.agw.fmresources import INB_SHOW_ONLY_TEXT
from wx.lib.agw.fmresources import INB_BOLD_TAB_SELECTION
from wx.lib.agw.fmresources import INB_FIT_LABELTEXT
from wx.lib.agw.fmresources import INB_FIT_BUTTON

from wx.lib.agw.labelbook import LabelBook

from org.pyut.PyutPreferences import PyutPreferences

from org.pyut.dialogs.preferences.GeneralPreferences import GeneralPreferencesPanel
from org.pyut.dialogs.preferences.MiscellaneousPreferences import MiscellaneousPreferences
from org.pyut.dialogs.preferences.PositioningPreferences import PositioningPreferences

from org.pyut.general.Globals import _


class DlgPyutPreferences(Dialog):
    VERTICAL_GAP:   int = 5
    HORIZONTAL_GAP: int = 5
    """
    This is the preferences dialog for Pyut.  This is version 2 of this dialog from 
    the legacy application.  This version of Pyut added many more preferences.

    Display the current preferences, the possible values, and save modified values.

    This works just like preferences on OS X work.  They are changed
    immediately
    
    To use it from a wxFrame:
    ```python

        dlg = DlgProperties(self, wx.ID_ANY, Mediator())
        dlg.ShowModal()
        dlg.Destroy()
    ```
    """
    def __init__(self, parent, wxId):
        """

        Args:
            parent:
            wxId:
        """
        super().__init__(parent, wxId, _("Preferences"))

        self.logger:    Logger          = getLogger(__name__)
        self.__prefs:   PyutPreferences = PyutPreferences()

        self.book: LabelBook = self._createTheControls()

        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        mainSizer.Add(self._createTheControls(), 1, ALL | EXPAND, DlgPyutPreferences.VERTICAL_GAP)

        mainSizer.Add(self._createButtonsContainer(), 0, CENTER)

        self.SetAutoLayout(True)
        self.SetSizer(mainSizer)

        self.Bind(EVT_BUTTON, self.__OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self.__OnClose)

    def _createTheControls(self) -> LabelBook:
        """
        Initialize the controls.
        """
        style: int = INB_DRAW_SHADOW | INB_SHOW_ONLY_TEXT | INB_FIT_LABELTEXT | INB_BOLD_TAB_SELECTION | INB_FIT_BUTTON | INB_BORDER
        book: LabelBook = LabelBook(self, ID_ANY, agwStyle=style)

        generalPreferences:     GeneralPreferencesPanel  = GeneralPreferencesPanel(parent=self)
        positioningPreferences: PositioningPreferences   = PositioningPreferences(parent=self)
        miscPanel:              MiscellaneousPreferences = MiscellaneousPreferences(parent=self)

        book.AddPage(generalPreferences,     text=_('General'),       select=True)
        book.AddPage(positioningPreferences, text=_('Positioning'),   select=False)
        book.AddPage(miscPanel,              text=_('Miscellaneous'), select=False)

        self._positioningPreferences: PositioningPreferences = positioningPreferences
        return book

    def _createButtonsContainer(self) -> BoxSizer:

        hs: BoxSizer = BoxSizer(HORIZONTAL)

        btnOk: Button = Button(self, ID_OK, _("&OK"))

        # hs.AddSpacer(200)
        hs.Add(btnOk, 0, ALL, DlgPyutPreferences.HORIZONTAL_GAP)

        return hs

    def __OnClose(self, event):

        self.__potentiallyDisplayInfoMessage()
        self.EndModal(CANCEL)
        event.Skip(skip=True)

    # noinspection PyUnusedLocal
    def __OnCmdOk(self, event: CommandEvent):

        self.__potentiallyDisplayInfoMessage()
        self.EndModal(OK)
        event.Skip(skip=True)

    def __potentiallyDisplayInfoMessage(self):

        if self._positioningPreferences.valuesChanged is True:
            dlg = MessageDialog(self, _("You must restart Pyut for position/size changes"), _("Warning"), OK | ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
