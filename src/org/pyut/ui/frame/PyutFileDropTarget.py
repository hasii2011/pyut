
from typing import List
from typing import NewType

from logging import INFO
from logging import Logger
from logging import getLogger

from wx import ICON_ERROR
from wx import OK

from wx import FileDropTarget
from wx import MessageDialog
from wx import Window

from org.pyut.PyutConstants import PyutConstants
from org.pyut.general.Globals import _

from org.pyut.ui.TreeNotebookHandler import TreeNotebookHandler

FileNames = NewType('FileNames', List[str])


class PyutFileDropTarget(FileDropTarget):

    def __init__(self, treeNotebookHandler: TreeNotebookHandler):

        super().__init__()

        self.logger: Logger = getLogger(__name__)
        self.logger.setLevel(INFO)

        self._treeNotebookHandler: TreeNotebookHandler = treeNotebookHandler

    def OnDropFiles(self, x: int, y: int, filenames: FileNames) -> bool:
        """

        Args:
            x:  abscissa of dropped files
            y:  ordinate of dropped files
            filenames:   List of strings which are the full path names of the dropped files
        """

        badFileNameList:  FileNames = FileNames([])
        pyutFileNameList: FileNames = FileNames([])
        xmlFileNameList:  FileNames = FileNames([])

        for fileName in filenames:
            self.logger.info(f'You dropped: {fileName}')
            if fileName.endswith(PyutConstants.PYUT_EXTENSION):
                pyutFileNameList.append(fileName)
            elif fileName.endswith(PyutConstants.XML_EXTENSION):
                xmlFileNameList.append(fileName)
            else:
                badFileNameList.append(fileName)

        self._loadPyutFiles(pyutFileNameList)

        if len(badFileNameList) > 0:
            parent:  Window = self._treeNotebookHandler.notebook
            message: str    = _('Only .put and .xml files are supported')
            caption: str    = _('Unsupported File')
            booBoo: MessageDialog = MessageDialog(parent=parent, message=message, caption=caption, style=OK | ICON_ERROR)
            booBoo.ShowModal()

        return True

    def _loadPyutFiles(self, filenames: FileNames):

        for pyutFileName in filenames:
            self._treeNotebookHandler.openFile(pyutFileName)
