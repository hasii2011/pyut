
from typing import NewType
from typing import Tuple
from typing import cast

from wx import FD_OPEN
from wx import FD_MULTIPLE
from wx import FD_CHANGE_DIR
from wx import FD_FILE_MUST_EXIST
from wx import FD_OVERWRITE_PROMPT
from wx import FD_SAVE
from wx import ICON_ERROR
from wx import ID_CANCEL
from wx import OK

from wx import DirDialog
from wx import FileDialog
from wx import FileSelector
from wx import MessageDialog
from wx import Yield as wxYield

from org.pyut.ui.UmlFrame import UmlFrame


class PyutPlugin:

    INPUT_FORMAT_TYPE = NewType('INPUT_FORMAT_TYPE', Tuple[str, str, str])
    OUTPUT_FORMAT_TYPE = NewType('OUTPUT_FORMAT_TYPE', Tuple[str, str, str])

    """
    Standard plugin tools
    """
    def __init__(self, umlFrame: UmlFrame, ctrl):
        """

        Args:
            umlFrame:   PyUt's UML frame
            ctrl:       The mediator to use
        """
        self._umlFrame = umlFrame
        self._ctrl     = ctrl
        self._verbose  = False

    def logMessage(self, module, msg):
        if self._verbose:
            print(f'{module}> {msg}')

    def getInputFormat(self) -> INPUT_FORMAT_TYPE:
        """
        Implementations probably need to override this

        Returns:
            The input format type
        """
        return cast(PyutPlugin.INPUT_FORMAT_TYPE, ("*", "*", "All"))

    def getOutputFormat(self) -> OUTPUT_FORMAT_TYPE:
        """
        Implementations probably need to override this

        Returns:
            The output format type
        """
        return cast(PyutPlugin.OUTPUT_FORMAT_TYPE, ("*", "*", "All"))

    @staticmethod
    def displayNoUmlFrame():
        booBoo: MessageDialog = MessageDialog(parent=None, message='No UML frame', caption='Try Again!', style=OK | ICON_ERROR)
        booBoo.ShowModal()

    def _askForFileImport(self, multiSelect: bool = False, startDirectory: str = None):
        """
        Called by plugin to ask which file must be imported

        Args:
            multiSelect: True to allow multi-file selection

        Returns:
            filename or "" for multiple=False, fileNames[] or
            [] else
            "",
            [] indicates that the user pressed the cancel button
        """

        inputFormat: PyutPlugin.INPUT_FORMAT_TYPE = self.getInputFormat()

        defaultDir:  str = startDirectory

        if defaultDir is None:
            defaultDir = self._ctrl.getCurrentDir()
        if multiSelect:
            dlg = FileDialog(
                self._umlFrame,
                "Choose files to import",
                wildcard=inputFormat[0] + " (*." + inputFormat[1] + ")|*." + inputFormat[1],
                defaultDir=defaultDir,
                style=FD_OPEN | FD_FILE_MUST_EXIST | FD_MULTIPLE | FD_CHANGE_DIR
            )
            dlg.ShowModal()
            if dlg.GetReturnCode() == ID_CANCEL:
                return [], ""

            return dlg.GetFilenames(), dlg.GetDirectory()
        else:
            file = FileSelector(
                "Choose a file to import",
                wildcard=inputFormat[0] + " (*." + inputFormat[1] + ")|*." + inputFormat[1],
                flags=FD_OPEN | FD_FILE_MUST_EXIST | FD_CHANGE_DIR
            )
            return file

    def _askForFileExport(self, defaultFileName: str = '') -> str:
        """
        Called by a plugin to ask for the export file name

        Returns:
        """
        wxYield()

        outputFormat: PyutPlugin.getOutputFormat = self.getOutputFormat()
        wildCard:    str = f'{outputFormat[0]} (*. {outputFormat[1]} )|*.{outputFormat[1]}'
        file:        str = FileSelector("Choose the export file name",
                                        default_filename=defaultFileName,
                                        wildcard=wildCard,
                                        flags=FD_SAVE | FD_OVERWRITE_PROMPT | FD_CHANGE_DIR)

        return file

    def _askForDirectoryImport(self):
        """
        Called by plugin to ask which directory must be imported
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

    def _askForDirectoryExport(self, preferredDefaultPath: str = None):
        """
        Called by plugin to ask for an output directory
        """
        if preferredDefaultPath is None:
            defaultPath: str = self._ctrl.getCurrentDir()
        else:
            defaultPath = preferredDefaultPath

        dirDialog = DirDialog(self._umlFrame, "Choose a destination directory", defaultPath=defaultPath)
        if dirDialog.ShowModal() == ID_CANCEL:
            dirDialog.Destroy()
            return ""
        else:
            directory = dirDialog.GetPath()
            self._ctrl.setCurrentDir(directory)
            dirDialog.Destroy()
            return directory

    def displayNoSelectedUmlObjects(self):
        booBoo: MessageDialog = MessageDialog(parent=None, message='No selected UML objects', caption='Try Again!', style=OK | ICON_ERROR)
        booBoo.ShowModal()
