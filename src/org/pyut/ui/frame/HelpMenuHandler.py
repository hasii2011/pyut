
from logging import Logger
from logging import getLogger

from wx import ID_ANY

from wx import CommandEvent
from wx import Menu
from wx import BeginBusyCursor as wxBeginBusyCursor
from wx import EndBusyCursor as wxEndBusyCursor
from wx import Yield as wxYield

from org.pyut.dialogs.DlgAbout import DlgAbout
from org.pyut.dialogs.DlgHelp import DlgHelp
from org.pyut.dialogs.DlgPyutDebug import DlgPyutDebug


from org.pyut.general.PyutVersion import PyutVersion

# noinspection PyProtectedMember
from org.pyut.general.Globals import _

from org.pyut.ui.frame.BaseMenuHandler import BaseMenuHandler

from org.pyut.PyutUtils import PyutUtils


class HelpMenuHandler(BaseMenuHandler):

    PYUT_WIKI: str = 'https://github.com/hasii2011/PyUt/wiki/Pyut'

    def __init__(self, helpMenu: Menu):

        super().__init__(menu=helpMenu)

        self.logger: Logger = getLogger(__name__)

    # noinspection PyUnusedLocal
    def onAbout(self, event: CommandEvent):
        """
        Show the Pyut about dialog

        Args:
            event:
        """
        dlg = DlgAbout(self._parent, ID_ANY, _("About PyUt ") + PyutVersion.getPyUtVersion())
        dlg.ShowModal()
        dlg.Destroy()

    # noinspection PyUnusedLocal
    def onHelpIndex(self, event: CommandEvent):
        """
        Display the help index
        """
        dlgHelp: DlgHelp = DlgHelp(self._parent, ID_ANY, _("Pyut Help"))
        dlgHelp.Show(True)

    # noinspection PyUnusedLocal
    def onHelpVersion(self, event: CommandEvent):
        """
        Check for newer version.
        Args:
            event:
        """
        from org.pyut.general.PyutVersion import PyutVersion
        from org.pyut.general.GithubAdapter import GithubAdapter
        from org.pyut.general.SemanticVersion import SemanticVersion

        wxBeginBusyCursor()
        githubAdapter: GithubAdapter   = GithubAdapter()
        latestVersion: SemanticVersion = githubAdapter.getLatestVersionNumber()

        myVersion: SemanticVersion = SemanticVersion(PyutVersion.getPyUtVersion())
        if myVersion < latestVersion:
            msg = _("PyUt version ") + str(latestVersion) + _(" is available on https://github.com/hasii2011/PyUt/releases")
        else:
            msg = _("No newer version yet !")

        wxEndBusyCursor()
        wxYield()
        PyutUtils.displayInformation(msg, _("Check for newer version"), self._parent)

    # noinspection PyUnusedLocal
    def onHelpWeb(self, event: CommandEvent):
        """

        Args:
            event:
        """
        PyutUtils.displayInformation(f"Please point your browser to {HelpMenuHandler.PYUT_WIKI}", "Pyut's new wiki", self._parent)

    # noinspection PyUnusedLocal
    def onDebug(self, event: CommandEvent):
        """
        Open a dialog to access the Pyut loggers

        Args:
            event:
        """
        with DlgPyutDebug(self._parent, ID_ANY) as dlg:
            dlg.ShowModal()
