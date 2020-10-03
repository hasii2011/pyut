
from logging import Logger
from logging import getLogger

from wx import ALL
from wx import CENTER
from wx import EVT_CLOSE
from wx import EVT_TEXT
from wx import VERTICAL
from wx import HORIZONTAL

from wx import ID_OK
from wx import ID_ANY

from wx import BoxSizer
from wx import Button
from wx import StaticText
from wx import TextCtrl
from wx import Dialog

from org.pyut.general.Globals import _

from org.pyut.preferences.PyutPreferences import PyutPreferences
from org.pyut.PyutUtils import PyutUtils


class DlgFastEditOptions(Dialog):

    GAP: int = 10

    """
    This is the option dialog for Fast Edit Tool.

    Display current properties and possible values, save modified values.

    """
    def __init__(self, parent):
        """
        Constructor.

        """
        super().__init__(parent, ID_ANY, _("Fast Edit Options"))
        self.logger: Logger = getLogger(__name__)

        self.__prefs: PyutPreferences = PyutPreferences()
        self.__initCtrl()

        self.Bind(EVT_CLOSE, self.__OnClose)

    def __initCtrl(self):
        """
        Initialize the controls.
        """
        # IDs
        [
            self.__editorID
        ] = PyutUtils.assignID(1)

        sizer = BoxSizer(VERTICAL)

        self.__lblEditor = StaticText(self, -1, _("Editor"))
        self.__txtEditor = TextCtrl(self, -1, size=(100, 20))
        sizer.Add(self.__lblEditor, 0, ALL, DlgFastEditOptions.GAP)
        sizer.Add(self.__txtEditor, 0, ALL, DlgFastEditOptions.GAP)

        hs = BoxSizer(HORIZONTAL)
        btnOk = Button(self, ID_OK, _("&OK"))
        hs.Add(btnOk, 0, ALL, DlgFastEditOptions.GAP)
        sizer.Add(hs, 0, CENTER)

        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        sizer.Fit(self)
        sizer.SetSizeHints(self)

        btnOk.SetDefault()

        self.Bind(EVT_TEXT, self.__OnText, id=self.__editorID)

        self.__setValues()
        self.Center()

        self.__changed: bool = False

    def __setValues(self):
        """
        Set the default values to the controls.
        """
        # self.__txtEditor.SetValue(secureStr(self.__prefs[PyutPreferences.EDITOR]))
        self.__txtEditor.SetValue(self.__prefs.editor)

        self.__txtEditor.SetInsertionPointEnd()

    # noinspection PyUnusedLocal
    def __OnText(self, event):
        """
        Occurs when text entry changes.
        """
        self.__changed = True

    def __OnClose(self, event):
        """
        Callback.
        """
        event.Skip()

    def getEditor(self) -> str:
        """

        Returns:
            The editor string.
        """
        return self.__txtEditor.GetValue()
