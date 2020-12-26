
from logging import Logger
from logging import getLogger
from typing import cast

from urllib import request

from wx import ID_ANY

from wx import CommandEvent
from wx import Menu
from wx import Window

from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.DlgAbout import DlgAbout
from org.pyut.dialogs.DlgHelp import DlgHelp
from org.pyut.dialogs.DlgPyutDebug import DlgPyutDebug

from org.pyut.general.Mediator import Mediator
from org.pyut.general.PyutVersion import PyutVersion

from org.pyut.general.Globals import _


class HelpMenuHandler:

    PYUT_WIKI: str = 'https://github.com/hasii2011/PyUt/wiki/Pyut'

    def __init__(self, helpMenu: Menu):

        self.logger: Logger = getLogger(__name__)

        self._helpMenu: Menu     = helpMenu
        self._mediator: Mediator = Mediator()
        self._parent:   Window    = self._helpMenu.GetWindow()

    # noinspection PyUnusedLocal
    def onAbout(self, event: CommandEvent):
        """
        Show the about box

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
        # Init
        FILE_TO_CHECK = 'https://github.com/hasii2011/PyUt/releases'     # TODO FIXME  :-)

        # Get file  -- Python 3 update
        f = request.urlopen(FILE_TO_CHECK)
        lstFile = f.readlines()
        f.close()

        # Verify data coherence
        if lstFile[0][:15] != "Last version = " or lstFile[1][:15] != "Old versions = ":
            msg = "Incorrect file on server"
        else:
            latestVersion = lstFile[0][15:]
            oldestVersions = lstFile[1][15:].split()
            print(f'{oldestVersions=}')

            from org.pyut.general.PyutVersion import PyutVersion
            v = PyutVersion.getPyUtVersion()
            if v in oldestVersions:
                msg = _("PyUt version ") + str(latestVersion) + _(" is available on https://github.com/hasii2011/PyUt/releases")
            else:
                msg = _("No newer version yet !")

        # Display dialog box
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
            dlg: DlgPyutDebug = cast(DlgPyutDebug, dlg)
            dlg.ShowModal()
