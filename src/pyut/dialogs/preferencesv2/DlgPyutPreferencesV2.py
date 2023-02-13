
from logging import Logger
from logging import getLogger

from wx import CANCEL
from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import NB_FIXEDWIDTH
from wx import NB_TOP
from wx import OK
from wx import ID_ANY
from wx import ID_OK
from wx import RESIZE_BORDER

from wx import CommandEvent
from wx import Notebook
from wx import Size

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel

from ogl.ui.DefaultValuesPreferencesPage import DefaultValuesPreferencesPage
from ogl.ui.DiagramPreferencesPage import DiagramPreferencesPage

from pyut.dialogs.preferencesv2.GeneralPrefencesPage import GeneralPreferencesPage

from pyut.dialogs.preferencesv2.PositioningPreferencesPage import PositioningPreferencesPage

from pyut.preferences.PyutPreferences import PyutPreferences

from pyutplugins.common.ui.preferences.PluginPreferencesPage import PluginPreferencesPage

class DlgPyutPreferencesV2(SizedDialog):
    """
    This is the preferences dialog for Pyut.  This is version 2 of this dialog from 
    the legacy application.  This version of Pyut added many more preferences.

    Display the current preferences, the possible values, and save modified values.

    This works just like preferences on OS X work.  They are changed
    immediately
    
    To use it from a wxFrame:
    ```python

        dlg = DlgProperties(parent=self, wxId=wx.ID_ANY)
        dlg.ShowModal()
        dlg.Destroy()
    ```
    """
    def __init__(self, parent):
        """
        Args:
            parent:
        """
        style:   int  = DEFAULT_DIALOG_STYLE | RESIZE_BORDER
        dlgSize: Size = Size(440,400)
        super().__init__(parent, ID_ANY, "Preferences", size=dlgSize, style=style)
        self.logger:  Logger          = getLogger(__name__)
        self.__prefs: PyutPreferences = PyutPreferences()

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerProps(expand=True)

        self._createTheControls(sizedPanel=sizedPanel)
        self.SetButtonSizer(self.CreateStdDialogButtonSizer(OK | CANCEL))

        self.Bind(EVT_BUTTON, self.__OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self.__OnClose)
        # self.Fit()
        # self.SetMinSize(self.GetSize())

    def _createTheControls(self, sizedPanel: SizedPanel):
        """
        Initialize the controls and add them each as a notebook page.
        """
        style: int = NB_TOP | NB_FIXEDWIDTH
        book: Notebook = Notebook(sizedPanel, style=style)
        book.SetSizerProps(expand=True, proportion=1)

        generalPreferences:     GeneralPreferencesPage       = GeneralPreferencesPage(book)
        positioningPreferences: PositioningPreferencesPage   = PositioningPreferencesPage(book)
        diagramPreferences:     DiagramPreferencesPage       = DiagramPreferencesPage(book)
        valuePreferences:       DefaultValuesPreferencesPage = DefaultValuesPreferencesPage(book)
        pluginPreferences:      PluginPreferencesPage        = PluginPreferencesPage(book)
        #
        book.AddPage(generalPreferences,     text=generalPreferences.name,     select=True)
        book.AddPage(positioningPreferences, text=positioningPreferences.name, select=False)
        book.AddPage(diagramPreferences,     text=diagramPreferences.name,     select=False)
        book.AddPage(valuePreferences,       text=valuePreferences.name,       select=False)
        book.AddPage(pluginPreferences,      text=pluginPreferences.name,      select=False)

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

        # if self._positioningPreferences.valuesChanged is True:
        #     dlg = MessageDialog(self, "You must restart Pyut for position/size changes", "Warning", OK | ICON_EXCLAMATION)
        #     dlg.ShowModal()
        #     dlg.Destroy()

        pass
