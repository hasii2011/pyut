
from logging import Logger
from logging import getLogger

from wx import ALL
from wx import CENTER
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EVT_TEXT
from wx import VERTICAL
from wx import HORIZONTAL

from wx import ID_OK

from wx import BoxSizer
from wx import Button
from wx import StaticText
from wx import TextCtrl
from wx import Dialog

from globals import _

from PyutPreferences import PyutPreferences
from PyutUtils1 import assignID


class DlgFEOptions(Dialog):
    """
    This is the option dialog for Fast Edit Tool.

    Display current properties and possible values, save modified values.

    :version: $Revision: 1.4 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """
    def __init__(self, parent):
        """
        Constructor.

        @author Philippe Waelti <pwaelti@eivd.ch>
        @since 1.0
        """
        super().__init__(parent, -1, _("Fast Edit Options"))
        self.logger: Logger = getLogger(__name__)

        self.__prefs = PyutPreferences()
        self.__initCtrl()

        self.Bind(EVT_CLOSE, self.__OnClose)

    def __initCtrl(self):
        """
        Initialize the controls.

        @since 1.0
        """
        # IDs
        [
            self.__editorID
        ] = assignID(1)

        GAP = 10

        sizer = BoxSizer(VERTICAL)

        self.__lblEditor = StaticText(self, -1, _("Editor"))
        self.__txtEditor = TextCtrl(self, -1, size=(100, 20))
        sizer.Add(self.__lblEditor, 0, ALL, GAP)
        sizer.Add(self.__txtEditor, 0, ALL, GAP)

        hs = BoxSizer(HORIZONTAL)
        btnOk = Button(self, ID_OK, _("&OK"))
        hs.Add(btnOk, 0, ALL, GAP)
        sizer.Add(hs, 0, CENTER)

        self.__changed = False

        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        sizer.Fit(self)
        sizer.SetSizeHints(self)

        btnOk.SetDefault()

        self.Bind(EVT_TEXT,   self.__OnText,  id=self.__editorID)
        # self.Bind(EVT_BUTTON, self.__OnCmdOk, id=ID_OK)

        self.__setValues()

        self.Center()
        # self.ShowModal()

    def __setValues(self):
        """
        Set the default values to the controls.

        @since 1.0
        """
        def secureStr(x):
            if x is None:
                return ""
            else:
                return x

        self.__txtEditor.SetValue(secureStr(self.__prefs["EDITOR"]))
        self.__txtEditor.SetInsertionPointEnd()

    # noinspection PyUnusedLocal
    def __OnText(self, event):
        """
        Occurs when text entry changes.

        @since 1.0
        """
        self.__changed = True

    def __OnClose(self, event):
        """
        Callback.

        @since 1.2
        """
        event.Skip()

    def getEditor(self):
        """
        Return the editor string.

        @return String editor : Chosen editor
        @since 1.2
        """
        return self.__txtEditor.GetValue()
