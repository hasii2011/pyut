
from logging import Logger
from logging import getLogger

from wx import CommandEvent
from wx import Menu
from wx import BeginBusyCursor as wxBeginBusyCursor
from wx import EndBusyCursor as wxEndBusyCursor
from wx import Yield as wxYield

from semantic_version import Version as SemanticVersion

from pyut import __version__ as pyutVersion

from pyut.ui.dialogs.DlgAbout import DlgAbout
from pyut.ui.dialogs.DlgPyutDebug import DlgPyutDebug

from pyut.ui.frame.BaseMenuHandler import BaseMenuHandler

from pyut.PyutUtils import PyutUtils

from pyut.ui.eventengine.IEventEngine import IEventEngine


class HelpMenuHandler(BaseMenuHandler):

    PYUT_WIKI: str = 'https://github.com/hasii2011/PyUt/wiki/'

    def __init__(self, helpMenu: Menu, eventEngine: IEventEngine | None = None):

        super().__init__(menu=helpMenu, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

    # noinspection PyUnusedLocal
    def onAbout(self, event: CommandEvent):
        """
        Show the Pyut about dialog

        Args:
            event:
        """
        with DlgAbout(self._parent, f"About Pyut {pyutVersion}") as dlg:
            dlg.ShowModal()

    # noinspection PyUnusedLocal
    def onHelpVersion(self, event: CommandEvent):
        """
        Check for newer version.
        Args:
            event:
        """
        from pyut.general.GitHubAdapter import GitHubAdapter

        wxBeginBusyCursor()
        githubAdapter: GitHubAdapter   = GitHubAdapter()
        latestVersion: SemanticVersion = githubAdapter.getLatestVersionNumber()

        myVersion: SemanticVersion = SemanticVersion(pyutVersion)
        # latestVersion.major = 9        Manual test
        if myVersion < latestVersion:
            msg = f"PyUt version {str(latestVersion)} is available on https://github.com/hasii2011/PyUt/releases"
        else:
            msg = "No newer version yet !"

        wxEndBusyCursor()
        wxYield()
        PyutUtils.displayInformation(msg, "Check for newer version", self._parent)

    # noinspection PyUnusedLocal
    def onHelpWeb(self, event: CommandEvent):
        """

        Args:
            event:
        """
        PyutUtils.displayInformation(f"Please point your browser to {HelpMenuHandler.PYUT_WIKI}", "The new Pyut Wiki", self._parent)

    # noinspection PyUnusedLocal
    def onDebug(self, event: CommandEvent):
        """
        Open a dialog to access the Pyut loggers

        Args:
            event:
        """
        with DlgPyutDebug(self._parent) as dlg:
            dlg.ShowModal()
