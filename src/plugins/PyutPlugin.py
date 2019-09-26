
import os

from wx import DirDialog
from wx import FD_OPEN
from wx import FD_MULTIPLE
from wx import FD_CHANGE_DIR
from wx import FD_FILE_MUST_EXIST
from wx import FD_OVERWRITE_PROMPT
from wx import FD_SAVE
from wx import ID_CANCEL

from wx import FileDialog
from wx import FileSelector


class PyutPlugin:
    """
    Standard plugin tools
    """

    def __init__(self, umlFrame, ctrl):
        """
        Constructor.

        @param umlFrame : the umlframe of pyut
        @param  ctrl : mediator to use
        @author C.Dutoit
        """
        self._umlFrame = umlFrame
        self._ctrl     = ctrl
        self._verbose  = False

    def logMessage(self, module, msg):
        if self._verbose:
            print(f'{module}> {msg}')

    def getInputFormat(self):
        """
        Implementations probably need to override this

        Returns: a tuple

        """
        return "*", "*", "All"

    def getOutputFormat(self):
        """
        Implementations probably need to override this

        Returns: A Tuple

        """
        return "*", "*", "All"

    def _askForFileImport(self, multiple=False):
        """
        Called by plugin to ask which file must be imported

        @param Boolean multiple : True for multiple file selection
        @return filename or "" for multiple=False, filenames[] or [] else
                "", [] indicates that the user pressed the cancel button
        @since 1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        inputformat = self.getInputFormat()
        if multiple:
            dlg = FileDialog(
                self._umlFrame,
                "Choose files to import",
                wildcard=inputformat[0] + " (*." + inputformat[1] + ")|*." + inputformat[1],
                defaultDir=self._ctrl.getCurrentDir(),
                style=FD_OPEN | FD_FILE_MUST_EXIST | FD_MULTIPLE | FD_CHANGE_DIR
            )
            dlg.ShowModal()
            if dlg.GetReturnCode() == 5101:  # Cancel
                return [], ""
            return dlg.GetFilenames(), dlg.GetDirectory()
        else:
            file = FileSelector(
                "Choose a file to import",
                wildcard=inputformat[0] + " (*." + inputformat[1] + ")|*." + inputformat[1],
                # default_path = self.__ctrl.getCurrentDir(),
                flags=FD_OPEN | FD_FILE_MUST_EXIST | FD_CHANGE_DIR
            )
            return file

    def _askForFileExport(self):
        """
        Called by plugin to ask which file must be exported

        @since 1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        inputFormat = self.getOutputFormat()
        file = FileSelector(
            "Choose a file name to export",
            wildcard=inputFormat[0] + " (*." + inputFormat[1] + ")|*." + inputFormat[1],
            flags=FD_SAVE | FD_OVERWRITE_PROMPT | FD_CHANGE_DIR
        )
        return file

    def _askForDirectoryImport(self):
        """
        Called by plugin to ask which file must be imported

        @since 1.3
        @return The directory or "" if canceled by user
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        aDirectory = DirDialog(self._umlFrame, "Choose a directory to import", defaultPath=self._ctrl.getCurrentDir())
        # TODO : add this when supported...(cd)         style=wx.DD_NEW_DIR_BUTTON)
        if aDirectory.ShowModal() == ID_CANCEL:
            aDirectory.Destroy()
            return ""
        else:
            directory = aDirectory.GetPath()
            self._ctrl.setCurrentDir(directory)
            aDirectory.Destroy()
            return directory

    def _askForDirectoryExport(self):
        """
        Called by plugin to ask for an output directory

        @since 1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        dirDialog = DirDialog(self._umlFrame, "Choose a destination directory", defaultPath=self._ctrl.getCurrentDir())
        # TODO : add this when supported...(cd)         style=wx.DD_NEW_DIR_BUTTON)
        dirDialog.SetPath(os.getcwd())
        if dirDialog.ShowModal() == ID_CANCEL:
            dirDialog.Destroy()
            return ""
        else:
            directory = dirDialog.GetPath()
            self._ctrl.setCurrentDir(directory)
            dirDialog.Destroy()
            return directory
