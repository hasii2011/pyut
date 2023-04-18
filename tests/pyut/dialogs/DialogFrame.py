
from typing import cast

from logging import Logger
from logging import getLogger

from pathlib import Path

from wx import DEFAULT_FRAME_STYLE
from wx import EVT_CLOSE
from wx import EVT_MENU
from wx import EVT_WINDOW_DESTROY
from wx import ID_EXIT
from wx import ID_FILE1

from wx import CloseEvent
from wx import CommandEvent
from wx import FileHistory
from wx import Frame
from wx import Menu
from wx import MenuBar
from wx import OK
from wx import Window
from wx import WindowDestroyEvent

from wx import PostEvent as wxPostEvent
from wx import NewIdRef as wxNewIdRef

from pyut.uiv2.FileHistoryConfiguration import FileHistoryConfiguration

from pyut.uiv2.dialogs.DlgEditProjectHistory import DlgEditProjectHistory


FH_APPLICATION_NAME: str = 'TestADialog'
FH_VENDOR_NAME:      str = 'BadCat'
FH_FILE_NAME:        str = 'testRecentFiles.ini'


class DialogFrame(Frame):

    def __init__(self):

        super().__init__(parent=None, title="Test A Dialog", size=(400, 200), style=DEFAULT_FRAME_STYLE)

        self.logger: Logger = getLogger(__name__)

        self._id_menu_file_manage_file_history: int = wxNewIdRef()
        menuBar:  MenuBar = MenuBar()
        fileMenu: Menu  = Menu()
        fileMenu.Append(self._id_menu_file_manage_file_history, 'Manage Projects')
        fileMenu.AppendSeparator()
        fileMenu.Append(ID_EXIT, "E&xit", "Exit")
        #
        menuBar.Append(fileMenu,  "&File")
        self.SetMenuBar(menuBar)

        self._fileHistory:              FileHistory              = cast(FileHistory, None)
        self._fileHistoryConfiguration: FileHistoryConfiguration = cast(FileHistoryConfiguration, None)

        self._createFileHistoryConfiguration(fileMenu)

        self.Bind(EVT_MENU,  self._onManageFileHistory, id=self._id_menu_file_manage_file_history)

        self.Bind(EVT_WINDOW_DESTROY, self._cleanupFileHistory)
        self.Bind(EVT_MENU, self._onExit, id=ID_EXIT)

        self.CreateStatusBar()

    # noinspection PyUnusedLocal
    def _cleanupFileHistory(self, event: WindowDestroyEvent):
        """
        Take time to persist the file history
        On OS X this gets stored in ~/Library/Preferences
        Nothing I did to the FileHistoryConfiguration object seemed to change that

        Args:
            event:
        """
        self._fileHistory.Save(self._fileHistoryConfiguration)

    # noinspection PyUnusedLocal
    def _onManageFileHistory(self, event: CommandEvent):

        with DlgEditProjectHistory(parent=self, fileHistory=self._fileHistory) as dlg:
            if dlg.ShowModal() == OK:
                return f'Ok'
            else:
                return f'Cancelled'

    def _onExit(self, event: CommandEvent):
        """
        Exit the program

        Args:
            event:
        """
        closeEvent: CloseEvent = CloseEvent(EVT_CLOSE.typeId)

        parent: Window = event.GetEventObject().GetWindow()
        wxPostEvent(parent, closeEvent)

    def _createFileHistoryConfiguration(self, fileMenu):
        # /Users/humberto.a.sanchez.ii/Library/Preferences/testRecentFiles.ini
        fhPath: Path = Path('/Users/humberto.a.sanchez.ii/Library/Preferences/testRecentFiles.ini')
        fhPath.unlink(missing_ok=True)
        self._fileHistory = FileHistory(idBase=ID_FILE1)
        self._fileHistoryConfiguration = FileHistoryConfiguration(appName=FH_APPLICATION_NAME, vendorName=FH_VENDOR_NAME, localFilename=FH_FILE_NAME)
        self._fileHistory.Load(self._fileHistoryConfiguration)
        self._fileHistory.UseMenu(fileMenu)

        try:
            self._fileHistory.AddFileToHistory(filename='/tmp/Ozzee.txt')
            self._fileHistory.AddFileToHistory(filename='/tmp/Fran.java')
            self._fileHistory.AddFileToHistory(filename='/Users/humberto.a.sanchez.ii//bogus.py')
            self._fileHistory.AddFileToHistory(filename='//Users/humberto.a.sanchez.ii/PycharmProjects/pyutplugins/tests/resources/testdata/mermaid/MermaidFields.xml')
            self._fileHistory.AddFileToHistory(filename='/tmp/forty.py')
            self._fileHistory.AddFileToHistory(filename='/tmp/fifty.py')
        except (ValueError, Exception) as e:
            self.logger.error(f'File History error:  {e}')
